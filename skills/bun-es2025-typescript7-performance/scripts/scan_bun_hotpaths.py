#!/usr/bin/env python3
"""Print likely JS/TS allocation, copy, and concurrency review targets."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = {
    "spread copy": re.compile(r"(?:\.\.\.|Object\.assign\()"),
    "array combinator": re.compile(r"\.(?:map|filter|flatMap|reduce|concat|slice)\("),
    "JSON boundary": re.compile(r"JSON\.(?:parse|stringify)\("),
    "promise fan-out": re.compile(r"Promise\.(?:all|allSettled|race|any)\("),
    "worker boundary": re.compile(r"\b(?:Worker|postMessage)\b"),
    "byte conversion": re.compile(
        r"\b(?:Buffer\.from|TextEncoder|TextDecoder|ArrayBuffer)\b"
    ),
    "sync durability": re.compile(r"\b(?:fsync|fdatasync|sync)\b"),
}
SKIP = {".git", "node_modules", "dist", "build", "coverage", ".next"}
EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: scan_bun_hotpaths.py <repository>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    for path in sorted(root.rglob("*")):
        if (
            not path.is_file()
            or path.suffix not in EXTENSIONS
            or any(part in SKIP for part in path.parts)
        ):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(lines, 1):
            for label, pattern in PATTERNS.items():
                if pattern.search(line):
                    print(f"{path.relative_to(root)}:{number}: {label}: {line.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
