#!/usr/bin/env python3
"""Validate bundled JSONL evaluation cases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = {"id", "category", "prompt", "expected"}
ALLOWED_CATEGORIES = {"trigger", "process", "outcome", "style", "efficiency"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "eval-cases.jsonl",
    )
    args = parser.parse_args()

    errors: list[str] = []
    seen: set[str] = set()
    count = 0
    for line_no, raw in enumerate(args.path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        count += 1
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: invalid JSON: {exc}")
            continue
        missing = REQUIRED - obj.keys()
        if missing:
            errors.append(f"line {line_no}: missing keys {sorted(missing)}")
        case_id = obj.get("id")
        if case_id in seen:
            errors.append(f"line {line_no}: duplicate id {case_id!r}")
        if case_id:
            seen.add(case_id)
        if obj.get("category") not in ALLOWED_CATEGORIES:
            errors.append(f"line {line_no}: invalid category {obj.get('category')!r}")
        for key in ("prompt", "expected"):
            if not isinstance(obj.get(key), str) or not obj.get(key, "").strip():
                errors.append(f"line {line_no}: {key} must be a non-empty string")

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s) across {count} case(s).")
        return 1
    print(f"PASS: {count} unique evaluation cases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
