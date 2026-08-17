"""Untracked-file inventory used by the suppression audit."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .discovery import GitInventoryError
from .suppression_rules import _is_ignore_file


def _untracked_candidates(repository: Path, root: Path) -> list[Path]:
    paths: set[Path] = set()
    for candidate in _untracked_paths(repository):
        try:
            candidate.relative_to(root)
        except ValueError:
            try:
                candidate.resolve().relative_to(root.resolve())
            except ValueError:
                continue
        if candidate.is_file() and (
            _is_ignore_file(candidate) or candidate.name.lower() == ".gitignore"
        ):
            paths.add(candidate)
    return sorted(paths, key=str)


def _untracked_paths(repository: Path) -> list[Path]:
    """Return untracked files that Git does not ignore.

    Ignored files are outside the architecture audit boundary, including the
    suppression and destructive-diff evidence pass.  This keeps every audit
    phase on one Git-defined candidate inventory.
    """

    paths: set[Path] = set()
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "ls-files",
                "--others",
                "--exclude-standard",
                "-z",
            ],
            check=False,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitInventoryError(f"Git suppression inventory failed: {exc}") from exc
    if result.returncode != 0:
        detail = (
            os.fsdecode(result.stderr).strip() or f"exit status {result.returncode}"
        )
        raise GitInventoryError(f"Git suppression inventory failed: {detail}")
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        candidate = repository / os.fsdecode(raw.rstrip(b"/"))
        if candidate.is_file():
            paths.add(candidate)
    return sorted(paths, key=str)
