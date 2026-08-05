"""Git working-tree suppression and destructive-diff evidence."""

from __future__ import annotations

import ast
import os
import re
import subprocess
from pathlib import Path

from .suppressions import (
    _CI_CONTEXT,
    _DESTRUCTIVE_PATH_TOKEN,
    _DiffEvent,
    _GITIGNORE_RELEVANT_PATH,
    _GITIGNORE_SOURCE_EXTENSION,
    _HUNK_HEADER,
    _IGNORE_FILE_NAMES,
    _PROVIDER_INVOCATION,
    _SCRIPT_DIRECTORY_NAMES,
    _SCRIPT_MANIFEST_NAMES,
    _SCRIPT_SUFFIXES,
    _TOOL_IGNORE_FILE,
    _CHECK_BYPASS,
    _finding,
    _is_comment_or_blank,
    _is_ignore_file,
    _is_relevant_gitignore_pattern,
    _is_linter_config,
    _is_workflow,
)

def _git_repository_root(root: Path) -> Path | None:
    """Return the containing Git worktree root, or ``None`` outside Git."""

    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0 or not result.stdout.strip():
        return None
    repository = Path(result.stdout.strip()).resolve()
    try:
        root.resolve().relative_to(repository)
    except ValueError:
        return None
    return repository


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


def _git_diff_events(text: str, repository: Path) -> list[_DiffEvent]:
    """Parse zero-context Git diff hunks into added/removed line evidence."""

    events: list[_DiffEvent] = []
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
            events.append(_DiffEvent(repository / relative, "deleted", 1))

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
            events.append(_DiffEvent(repository / path, "added", new_line, raw[1:]))
            new_line += 1
        elif raw.startswith("-"):
            events.append(_DiffEvent(repository / path, "removed", old_line, raw[1:]))
            old_line += 1
        elif raw.startswith(" "):
            old_line += 1
            new_line += 1
    flush_deleted()
    return events


def _run_git_diff(repository: Path, *, cached: bool) -> str:
    command = [
        "git", "-C", str(repository), "diff", "--no-ext-diff", "--no-color", "--no-renames",
        "--no-prefix", "--unified=0",
    ]
    if cached:
        command.append("--cached")
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout if result.returncode == 0 else ""


def _is_destructive_path(path: Path, repository: Path) -> bool:
    try:
        relative = path.relative_to(repository).as_posix()
    except ValueError:
        relative = path.as_posix()
    return bool(_DESTRUCTIVE_PATH_TOKEN.search(relative)) or _is_workflow(path) or _is_linter_config(path)


def _is_script_path(path: Path) -> bool:
    name = path.name.lower()
    if name in _SCRIPT_MANIFEST_NAMES or _is_workflow(path):
        return True
    parts = {part.lower() for part in path.parts}
    if parts & _SCRIPT_DIRECTORY_NAMES:
        return True
    return path.suffix.lower() in _SCRIPT_SUFFIXES and bool(
        _DESTRUCTIVE_PATH_TOKEN.search(name) or re.search(r"(?i)(?:^|[._-])(?:build|ci)(?:$|[._-])", name)
    )


def _provider_invocation(line: str) -> bool:
    if _is_comment_or_blank(line):
        return False
    return bool(_PROVIDER_INVOCATION.search(line))


def _path_category(path: Path) -> str | None:
    name = path.name.lower()
    if re.search(r"(?:^|[._-])test(?:s|data|ing)?(?:$|[._-])", name):
        return "test"
    if re.search(r"(?:^|[._-])(?:check|checks)(?:$|[._-])", name):
        return "check"
    if re.search(r"(?:^|[._-])(?:lint|lints|linting)(?:$|[._-])", name):
        return "lint"
    return None


def _migration_replacement(deleted: Path, candidates: set[Path]) -> bool:
    category = _path_category(deleted)
    if category is None:
        return False
    for candidate in candidates:
        if candidate.parent != deleted.parent or candidate == deleted:
            continue
        if _path_category(candidate) == category and _replacement_has_evidence(candidate, category):
            return True
    return False


def _replacement_has_evidence(path: Path, category: str) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    if not text.strip():
        return False
    if category == "test":
        if "placeholder" in text.lower() or re.search(r"(?m)^\s*def\s+test\w*\s*\([^)]*\)\s*:\s*pass\s*$", text):
            return False
        if not re.search(r"(?i)\b(?:assert|expect|assertEqual|raises|snapshot|subprocess|run_|invoke|raise)\b", text):
            return False
        return bool(re.search(r"(?im)(?:\bdef\s+test\w*|\bclass\s+\w*(?:test|tests)\b|\b(?:describe|it|test)\s*\(|#\s*\[test\]|@test\b)", text))
    return bool(_PROVIDER_INVOCATION.search(text) or _CHECK_BYPASS.search(text) or _CI_CONTEXT.search(text))


def _untracked_candidates(repository: Path, root: Path) -> list[Path]:
    paths: set[Path] = set()
    for candidate in _untracked_paths(repository):
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            continue
        if candidate.is_file() and (_is_ignore_file(candidate) or candidate.name.lower() == ".gitignore"):
            paths.add(candidate)
    return sorted(paths, key=str)


def _untracked_paths(repository: Path) -> list[Path]:
    paths: set[Path] = set()
    for options in (
        ["ls-files", "--others", "--exclude-standard", "-z"],
        ["ls-files", "--others", "--ignored", "--exclude-standard", "-z"],
    ):
        try:
            result = subprocess.run(
                ["git", "-C", str(repository), *options],
                check=False,
                capture_output=True,
                timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if result.returncode != 0:
            continue
        for raw in result.stdout.split(b"\0"):
            if not raw:
                continue
            candidate = repository / os.fsdecode(raw.rstrip(b"/"))
            if candidate.is_file():
                paths.add(candidate)
    return sorted(paths, key=str)


def git_suppression_findings(root: Path) -> list[Finding]:
    """Report suppression and destructive-evidence changes in a Git worktree.

    Git's committed tree is the baseline implicitly: unchanged files are never
    inspected here.  Both index-vs-HEAD and worktree-vs-index diffs are parsed,
    while untracked ignore files are inspected explicitly because Git does not
    include them in either diff.  Outside a Git worktree this is a no-op.
    """

    repository = _git_repository_root(root)
    if repository is None:
        return []
    findings: list[Finding] = []
    seen: set[tuple[str, str, int, str]] = set()

    def add(code: str, path: Path, line_number: int, message: str) -> None:
        key = (code, str(path), line_number, message)
        if key in seen:
            return
        seen.add(key)
        findings.append(_finding(path, line_number, message, code))

    events: list[_DiffEvent] = []
    for cached in (False, True):
        events.extend(_git_diff_events(_run_git_diff(repository, cached=cached), repository))
    try:
        audit_root = root.resolve()
    except OSError:
        audit_root = root
    untracked = {path for path in _untracked_paths(repository) if path.is_file()}
    added_candidates = {event.path for event in events if event.kind == "added"} | untracked

    for event in events:
        try:
            event.path.resolve().relative_to(audit_root)
        except ValueError:
            continue
        if event.kind == "deleted":
            if _is_destructive_path(event.path, repository) and not _migration_replacement(event.path, added_candidates):
                add("check-file-deleted", event.path, event.line_number, f"test/check/lint/CI file was deleted from the working tree: {event.path.name}")
            continue
        if event.kind == "added":
            if _is_ignore_file(event.path) and not _is_comment_or_blank(event.text):
                add("ignore-pattern-added", event.path, event.line_number, f"lint/check ignore pattern was added: {event.text.strip()}")
            elif event.path.name.lower() == ".gitignore" and _is_relevant_gitignore_pattern(event.text):
                add("gitignore-source-pattern-added", event.path, event.line_number, f"source/test/check/lint path was newly ignored: {event.text.strip()}")
        elif event.kind == "removed" and _is_script_path(event.path) and _provider_invocation(event.text):
            add("check-provider-removed", event.path, event.line_number, f"lint/check/test provider invocation was removed: {event.text.strip()}")

    for path in _untracked_candidates(repository, root):
        if path.name.lower() == ".gitignore":
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError) as exc:
                add("suppression-scan-failed", path, 1, f"Git ignore candidate scan failed: {exc}")
                continue
            for line_number, line in enumerate(lines, 1):
                if _is_relevant_gitignore_pattern(line):
                    add("gitignore-source-pattern-added", path, line_number, f"source/test/check/lint path was newly ignored: {line.strip()}")
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            add("suppression-scan-failed", path, 1, f"Git ignore candidate scan failed: {exc}")
            continue
        for line_number, line in enumerate(lines, 1):
            if not _is_comment_or_blank(line):
                add("ignore-pattern-added", path, line_number, f"lint/check ignore pattern was added: {line.strip()}")
    return findings
