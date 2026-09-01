#!/usr/bin/env python3
"""Flag nearby-justification gaps for common unsafe Rust constructs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

UNSAFE = re.compile(r"\bunsafe\b|\b(?:get_unchecked|unwrap_unchecked|transmute)\b")
SAFETY = re.compile(r"//\s*SAFETY:\s*\S+")
SKIP = {".git", "target", "vendor"}


def justified(lines: list[str], index: int) -> bool:
    start = max(0, index - 3)
    end = min(len(lines), index + 2)
    return any(SAFETY.search(line) for line in lines[start:end])


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_unsafe_justifications.py <repository>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    failures = 0
    for path in sorted(root.rglob("*.rs")):
        if any(part in SKIP for part in path.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(lines):
            if UNSAFE.search(line) and not justified(lines, index):
                print(
                    f"{path.relative_to(root)}:{index + 1}: missing nearby SAFETY: justification"
                )
                failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
