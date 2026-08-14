"""Enforce the repository's per-file authored Python size limit."""

from __future__ import annotations

import sys
from pathlib import Path

LIMIT = 500
ROOT = Path(__file__).resolve().parents[1]


def python_files() -> list[Path]:
    """Return package Python files, excluding interpreter caches."""

    return sorted(
        path
        for path in (ROOT / "skills").rglob("*.py")
        if "__pycache__" not in path.parts
    )


def line_count(path: Path) -> int:
    """Count physical source lines without depending on the host locale."""

    return len(path.read_text(encoding="utf-8").splitlines())


def main() -> int:
    """Print a deterministic result and return a process status."""

    oversized = [(path, line_count(path)) for path in python_files()]
    oversized = [(path, count) for path, count in oversized if count > LIMIT]
    if oversized:
        for path, count in oversized:
            print(
                f"FAIL: {path.relative_to(ROOT)} has {count} lines (limit {LIMIT})",
                file=sys.stderr,
            )
        return 1

    count = len(python_files())
    print(f"PASS: {count} skills Python files are <= {LIMIT} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
