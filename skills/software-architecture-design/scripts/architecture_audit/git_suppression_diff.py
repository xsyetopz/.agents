#!/usr/bin/env python3
"""Git diff and rename evidence used by the suppression audit."""

from __future__ import annotations

import ast
import difflib
import os
import posixpath
import re
import subprocess
from collections import Counter
from pathlib import Path

from .discovery import GitInventoryError
from .suppression_rules import (
    _DESTRUCTIVE_PATH_TOKEN,
    _HUNK_HEADER,
    _PROVIDER_INVOCATION,
    _SCRIPT_DIRECTORY_NAMES,
    _SCRIPT_MANIFEST_NAMES,
    _SCRIPT_SUFFIXES,
    DiffEvent,
    _is_comment_or_blank,
    is_linter_config,
    is_workflow,
)

# Git's similarity score is the evidence boundary for suppressing the
# deletion half of a rename. Scores at or above 90 are exact/strong enough
# to distinguish a move from an unrelated replacement. Lower-score path
# pairs are only candidates for the same fixed evidence boundary after
# relocation-only normalization; they never lower the acceptance threshold.
_RENAME_SIMILARITY_THRESHOLD = 90
_RELATIVE_SPECIFIER = re.compile(r"(?P<quote>[\"'])(?P<spec>\.{1,2}/[^\"']+)(?P=quote)")
_IMPORT_CONTEXT = re.compile(r"\b(?:import|export|require|from|dynamic\s+import)\b")


def _decode_git_path(value: str) -> Path | None:
    value = value.rstrip("\r\n")
    if value == "/dev/null":
        return None
    if value.startswith('"') and value.endswith('"'):
        try:
            value = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            value = value[1:-1]
    return Path(value)


def git_diff_events(text: str, repository: Path) -> list[DiffEvent]:
    """Parse zero-context Git diff hunks into added/removed line evidence."""

    events: list[DiffEvent] = []
    old_path: Path | None = None
    new_path: Path | None = None
    deleted = False
    old_line = new_line = 0
    in_hunk = False

    def flush_deleted() -> None:
        if not deleted:
            return
        relative = old_path or new_path
        if relative is not None:
            events.append(DiffEvent(repository / relative, "deleted", 1))

    for raw in text.splitlines():
        if raw.startswith("diff --git "):
            flush_deleted()
            old_path = new_path = None
            deleted = False
            old_line = new_line = 0
            in_hunk = False
            continue
        if raw.startswith("deleted file mode"):
            deleted = True
            continue
        if raw.startswith("--- "):
            old_path = _decode_git_path(raw[4:])
            continue
        if raw.startswith("+++ "):
            new_path = _decode_git_path(raw[4:])
            continue
        match = _HUNK_HEADER.match(raw)
        if match:
            old_line = int(match.group(1))
            new_line = int(match.group(3))
            in_hunk = True
            continue
        if not in_hunk or not raw:
            continue
        path = new_path or old_path
        if path is None:
            continue
        if raw.startswith("+"):
            events.append(DiffEvent(repository / path, "added", new_line, raw[1:]))
            new_line += 1
        elif raw.startswith("-"):
            events.append(DiffEvent(repository / path, "removed", old_line, raw[1:]))
            old_line += 1
        elif raw.startswith(" "):
            old_line += 1
            new_line += 1
    flush_deleted()
    return events


def run_git_diff(repository: Path, *, cached: bool) -> str:
    command = [
        "git",
        "-C",
        str(repository),
        "diff",
        "--no-ext-diff",
        "--no-color",
        "--no-renames",
        "--no-prefix",
        "--unified=0",
    ]
    if cached:
        command.append("--cached")
    try:
        result = subprocess.run(
            command, check=False, capture_output=True, text=True, timeout=10
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitInventoryError(f"Git suppression diff failed: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.strip() or f"exit status {result.returncode}"
        raise GitInventoryError(f"Git suppression diff failed: {detail}")
    return result.stdout


def run_git_rename_inventory(repository: Path, *, cached: bool) -> bytes:
    """Return Git's high-confidence rename status inventory for one diff.

    The line-oriented suppression diff intentionally disables rename
    detection so it can retain per-line provider evidence.  Deletion events
    from that diff are therefore paired against this separate, NUL-delimited
    status inventory rather than inferred from adjacent added paths.
    """

    command = [
        "git",
        "-C",
        str(repository),
        "diff",
        "--no-ext-diff",
        "--no-color",
        f"--find-renames={_RENAME_SIMILARITY_THRESHOLD}",
        "--diff-filter=R",
        "--name-status",
        "-z",
        "--no-prefix",
    ]
    if cached:
        command.append("--cached")
    try:
        result = subprocess.run(command, check=False, capture_output=True, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitInventoryError(f"Git rename inventory failed: {exc}") from exc
    if result.returncode != 0:
        detail = (
            os.fsdecode(result.stderr).strip() or f"exit status {result.returncode}"
        )
        raise GitInventoryError(f"Git rename inventory failed: {detail}")
    return result.stdout


def _run_git_no_rename_inventory(repository: Path, *, cached: bool) -> bytes:
    """Return added/deleted paths without asking Git to lower rename evidence."""

    command = [
        "git",
        "-C",
        str(repository),
        "diff",
        "--no-ext-diff",
        "--no-color",
        "--no-renames",
        "--diff-filter=AD",
        "--name-status",
        "-z",
        "--no-prefix",
    ]
    if cached:
        command.append("--cached")
    try:
        result = subprocess.run(command, check=False, capture_output=True, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitInventoryError(f"Git path inventory failed: {exc}") from exc
    if result.returncode != 0:
        detail = (
            os.fsdecode(result.stderr).strip() or f"exit status {result.returncode}"
        )
        raise GitInventoryError(f"Git path inventory failed: {detail}")
    return result.stdout


def git_rename_pairs(
    payload: bytes,
    repository: Path,
) -> set[tuple[Path, Path]]:
    """Parse NUL-delimited Git rename statuses into old/new absolute paths.

    Only an explicit ``R<score>`` status at the configured similarity
    threshold is accepted.  Malformed records are ignored (rather than
    manufacturing a waiver), so the deletion evidence remains fail-closed.
    """

    fields = payload.split(b"\0")
    pairs: set[tuple[Path, Path]] = set()
    index = 0
    while index < len(fields):
        raw_status = fields[index]
        index += 1
        if not raw_status:
            continue
        status = os.fsdecode(raw_status)
        if not status.startswith("R"):
            # ``--diff-filter=R`` should make this unreachable, but consume a
            # path defensively if Git emits a status we did not request.
            if index < len(fields):
                index += 1
            continue
        match = re.fullmatch(r"R(\d{1,3})", status)
        if match is None:
            index += 2
            continue
        similarity = int(match.group(1))
        if similarity > 100 or similarity < _RENAME_SIMILARITY_THRESHOLD:
            index += 2
            continue
        if index + 1 >= len(fields):
            break
        old_raw, new_raw = fields[index : index + 2]
        index += 2
        if not old_raw or not new_raw:
            continue
        old_relative = Path(os.fsdecode(old_raw))
        new_relative = Path(os.fsdecode(new_raw))
        if (
            old_relative.is_absolute()
            or new_relative.is_absolute()
            or ".." in old_relative.parts
            or ".." in new_relative.parts
        ):
            continue
        old = repository / old_relative
        new = repository / new_relative
        if old == new:
            continue
        pairs.add((old, new))
    return pairs


def _git_added_deleted_paths(
    payload: bytes, repository: Path
) -> tuple[set[Path], set[Path]]:
    """Parse a no-rename path inventory into added and deleted paths."""

    fields = payload.split(b"\0")
    added: set[Path] = set()
    deleted: set[Path] = set()
    index = 0
    while index < len(fields):
        raw_status = fields[index]
        index += 1
        if not raw_status:
            continue
        status = os.fsdecode(raw_status)
        if index >= len(fields):
            break
        raw_path = fields[index]
        index += 1
        if not raw_path:
            continue
        relative = Path(os.fsdecode(raw_path))
        if relative.is_absolute() or ".." in relative.parts:
            continue
        path = repository / relative
        if status.startswith("A"):
            added.add(path)
        elif status.startswith("D"):
            deleted.add(path)
    return added, deleted


def _git_blob(repository: Path, path: Path, *, cached: bool, old: bool) -> bytes | None:
    """Read one side of a staged/unstaged path without shell interpolation."""

    try:
        relative = path.relative_to(repository).as_posix()
    except ValueError:
        return None
    if not cached and not old:
        try:
            return path.read_bytes()
        except OSError:
            return None
    revision = "HEAD" if cached and old else ":"
    spec = f"{revision}:{relative}" if revision != ":" else f":{relative}"
    try:
        result = subprocess.run(
            ["git", "-C", str(repository), "show", spec],
            check=False,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def _normalise_relocated_lines(value: bytes, path: Path, repository: Path) -> list[str]:
    """Normalize only relative module references for move proof."""

    try:
        parent = path.parent.relative_to(repository).as_posix()
    except ValueError:
        parent = "."
    lines: list[str] = []
    for raw_line in value.decode("utf-8", errors="replace").splitlines():
        line = raw_line
        if _IMPORT_CONTEXT.search(line):

            def replace_specifier(match: re.Match[str]) -> str:
                specifier = match.group("spec")
                target = posixpath.normpath(posixpath.join(parent, specifier))
                if target == ".." or target.startswith("../"):
                    return match.group(0)
                return f"{match.group('quote')}<repo:{target}>{match.group('quote')}"

            line = _RELATIVE_SPECIFIER.sub(replace_specifier, line)
        lines.append(line)
    return lines


def _relocation_similarity(
    old: bytes, new: bytes, old_path: Path, new_path: Path, repository: Path
) -> float:
    old_lines = _normalise_relocated_lines(old, old_path, repository)
    new_lines = _normalise_relocated_lines(new, new_path, repository)
    return (
        difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False).ratio()
        * 100
    )


def candidate_rename_pairs(
    repository: Path,
    *,
    cached: bool,
    accepted: set[tuple[Path, Path]],
) -> set[tuple[Path, Path]]:
    """Accept same-name D/A pairs only when relocation-only proof reaches R90."""

    added, deleted = _git_added_deleted_paths(
        _run_git_no_rename_inventory(repository, cached=cached), repository
    )
    candidates: set[tuple[Path, Path]] = set()
    for old in deleted:
        matches = [
            new
            for new in added
            if old.name == new.name
            and old.suffix == new.suffix
            and (old, new) not in accepted
        ]
        if len(matches) != 1:
            continue
        new = matches[0]
        if not _is_destructive_path(old, repository) or not _is_destructive_path(
            new, repository
        ):
            continue
        old_blob = _git_blob(repository, old, cached=cached, old=True)
        new_blob = _git_blob(repository, new, cached=cached, old=False)
        if old_blob is None or new_blob is None:
            continue
        if (
            _relocation_similarity(old_blob, new_blob, old, new, repository)
            >= _RENAME_SIMILARITY_THRESHOLD
        ):
            candidates.add((old, new))
    return candidates


def _provider_lines(value: bytes) -> list[tuple[int, str]]:
    return [
        (line_number, line)
        for line_number, line in enumerate(
            value.decode("utf-8", errors="replace").splitlines(), 1
        )
        if _provider_invocation(line)
    ]


def provider_removals_for_rename(
    repository: Path,
    *,
    cached: bool,
    pairs: set[tuple[Path, Path]],
) -> list[tuple[Path, int, str]]:
    """Report provider lines lost across an accepted rename, line by line."""

    removals: list[tuple[Path, int, str]] = []
    for old, new in sorted(pairs, key=lambda pair: (str(pair[0]), str(pair[1]))):
        if not _is_script_path(old):
            continue
        old_blob = _git_blob(repository, old, cached=cached, old=True)
        new_blob = _git_blob(repository, new, cached=cached, old=False)
        if old_blob is None or new_blob is None:
            continue
        remaining = Counter(line.strip() for _, line in _provider_lines(new_blob))
        for line_number, line in _provider_lines(old_blob):
            key = line.strip()
            if remaining[key]:
                remaining[key] -= 1
            else:
                removals.append((old, line_number, line))
    return removals


def _is_destructive_path(path: Path, repository: Path) -> bool:
    try:
        relative = path.relative_to(repository).as_posix()
    except ValueError:
        relative = path.as_posix()
    return (
        bool(_DESTRUCTIVE_PATH_TOKEN.search(relative))
        or is_workflow(path)
        or is_linter_config(path)
    )


def _is_script_path(path: Path) -> bool:
    name = path.name.lower()
    if name in _SCRIPT_MANIFEST_NAMES or is_workflow(path):
        return True
    parts = {part.lower() for part in path.parts}
    if parts & _SCRIPT_DIRECTORY_NAMES:
        return True
    return path.suffix.lower() in _SCRIPT_SUFFIXES and bool(
        _DESTRUCTIVE_PATH_TOKEN.search(name)
        or re.search(r"(?i)(?:^|[._-])(?:build|ci)(?:$|[._-])", name)
    )


def _provider_invocation(line: str) -> bool:
    if _is_comment_or_blank(line):
        return False
    return bool(_PROVIDER_INVOCATION.search(line))
