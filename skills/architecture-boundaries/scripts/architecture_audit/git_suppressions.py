#!/usr/bin/env python3
"""Git working-tree suppression and destructive-diff evidence."""

from __future__ import annotations

from pathlib import Path

from . import git_suppression_diff as _diff
from . import git_suppression_inventory as _inventory
from . import suppression_rules as _rules
from .discovery import GitInventoryError, git_repository_root
from .records import Finding


def git_suppression_findings(root: Path) -> list[Finding]:
    """Report suppression and destructive-evidence changes in a Git worktree.

    Git's committed tree is the baseline implicitly: unchanged files are never
    inspected here.  Both index-vs-HEAD and worktree-vs-index diffs are parsed,
    while non-ignored untracked ignore files are inspected explicitly because
    Git does not include them in either diff.  Outside a Git worktree this is a
    no-op.
    """

    try:
        repository = git_repository_root(root)
    except GitInventoryError as exc:
        return [
            Finding("error", "git-suppression-scan-failed", root, str(exc), "tooling")
        ]
    if repository is None:
        return []
    findings: list[Finding] = []
    seen: set[tuple[str, str, int, str]] = set()

    def add(code: str, path: Path, line_number: int, message: str) -> None:
        key = (code, str(path), line_number, message)
        if key in seen:
            return
        seen.add(key)
        findings.append(_rules._finding(path, line_number, message, code))

    events_by_diff: dict[bool, list[_rules._DiffEvent]] = {}
    accepted_pairs_by_diff: dict[bool, set[tuple[Path, Path]]] = {}
    provider_pairs_by_diff: dict[bool, set[tuple[Path, Path]]] = {}
    try:
        for cached in (False, True):
            events_by_diff[cached] = _diff._git_diff_events(
                _diff._run_git_diff(repository, cached=cached), repository
            )
            high_confidence = _diff._git_rename_pairs(
                _diff._run_git_rename_inventory(repository, cached=cached), repository
            )
            accepted = high_confidence | _diff._candidate_rename_pairs(
                repository, cached=cached, accepted=high_confidence
            )
            provider_pairs_by_diff[cached] = accepted
            accepted_pairs_by_diff[cached] = {
                pair
                for pair in accepted
                if _diff._is_destructive_path(pair[0], repository)
                and _diff._is_destructive_path(pair[1], repository)
            }
    except GitInventoryError as exc:
        return [
            Finding("error", "git-suppression-scan-failed", root, str(exc), "tooling")
        ]
    try:
        audit_root = root.resolve()
    except OSError:
        audit_root = root
    for cached, events in events_by_diff.items():
        pairs = accepted_pairs_by_diff[cached]
        rename_sources = {old for old, _ in pairs}
        for event in events:
            try:
                event.path.resolve().relative_to(audit_root)
            except ValueError:
                continue
            if event.kind == "deleted":
                if (
                    _diff._is_destructive_path(event.path, repository)
                    and event.path not in rename_sources
                ):
                    add(
                        "check-file-deleted",
                        event.path,
                        event.line_number,
                        f"test/check/lint/CI file was deleted from the working tree: {event.path.name}",
                    )
                continue
            if event.kind == "added":
                if _rules._is_ignore_file(
                    event.path
                ) and not _rules._is_comment_or_blank(event.text):
                    add(
                        "ignore-pattern-added",
                        event.path,
                        event.line_number,
                        f"lint/check ignore pattern was added: {event.text.strip()}",
                    )
                elif (
                    event.path.name.lower() == ".gitignore"
                    and _rules._is_relevant_gitignore_pattern(event.text)
                ):
                    add(
                        "gitignore-source-pattern-added",
                        event.path,
                        event.line_number,
                        f"source/test/check/lint path was newly ignored: {event.text.strip()}",
                    )
            elif (
                event.kind == "removed"
                and event.path not in rename_sources
                and _diff._is_script_path(event.path)
                and _diff._provider_invocation(event.text)
            ):
                add(
                    "check-provider-removed",
                    event.path,
                    event.line_number,
                    f"lint/check/test provider invocation was removed: {event.text.strip()}",
                )

        for path, line_number, text in _diff._provider_removals_for_rename(
            repository, cached=cached, pairs=provider_pairs_by_diff[cached]
        ):
            add(
                "check-provider-removed",
                path,
                line_number,
                f"lint/check/test provider invocation was removed: {text.strip()}",
            )

    try:
        untracked_candidates = _inventory._untracked_candidates(repository, root)
    except GitInventoryError as exc:
        return [
            Finding("error", "git-suppression-scan-failed", root, str(exc), "tooling")
        ]
    for path in untracked_candidates:
        if path.name.lower() == ".gitignore":
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError) as exc:
                add(
                    "suppression-scan-failed",
                    path,
                    1,
                    f"Git ignore candidate scan failed: {exc}",
                )
                continue
            for line_number, line in enumerate(lines, 1):
                if _rules._is_relevant_gitignore_pattern(line):
                    add(
                        "gitignore-source-pattern-added",
                        path,
                        line_number,
                        f"source/test/check/lint path was newly ignored: {line.strip()}",
                    )
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            add(
                "suppression-scan-failed",
                path,
                1,
                f"Git ignore candidate scan failed: {exc}",
            )
            continue
        for line_number, line in enumerate(lines, 1):
            if not _rules._is_comment_or_blank(line):
                add(
                    "ignore-pattern-added",
                    path,
                    line_number,
                    f"lint/check ignore pattern was added: {line.strip()}",
                )
    return findings
