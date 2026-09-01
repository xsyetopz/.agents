#!/usr/bin/env python3
"""Print likely Rust allocation, copy, synchronization, and unsafe review targets."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = {
    "allocation": re.compile(
        r"\b(?:Vec::new|Vec::with_capacity|String::new|format!|Box::new|collect\()"
    ),
    "clone or copy": re.compile(r"\.(?:clone|to_owned|to_vec)\(\)"),
    "synchronization": re.compile(
        r"\b(?:Mutex|RwLock|Condvar|Atomic[A-Za-z0-9_]*|mpsc|channel)\b"
    ),
    "task or thread": re.compile(r"\b(?:spawn|thread::spawn|tokio::spawn)\b"),
    "unsafe boundary": re.compile(
        r"\b(?:unsafe|get_unchecked|unwrap_unchecked|transmute)\b"
    ),
    "durability": re.compile(r"\b(?:sync_all|sync_data|fsync|fdatasync)\b"),
}
SKIP = {".git", "target", "vendor"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: scan_rust_hotpaths.py <repository>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    for path in sorted(root.rglob("*.rs")):
        if any(part in SKIP for part in path.parts):
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
