#!/usr/bin/env python3
"""Run the bundled scanner fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scan_text import load_rules, scan


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    cases = json.loads((root / "tests" / "cases.json").read_text(encoding="utf-8"))
    rules = load_rules(root / "references" / "phrases.tsv")
    failures: list[str] = []
    for case in cases:
        findings = scan(case["name"], case["text"], rules, include_quotes=False, hard_only=False)
        matches = {finding.match.casefold() for finding in findings}
        for expected in case.get("must_find", []):
            if expected.casefold() not in matches:
                failures.append(f"{case['name']}: missing {expected!r}")
        for forbidden in case.get("must_not_find", []):
            if forbidden.casefold() in matches:
                failures.append(f"{case['name']}: unexpected {forbidden!r}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Passed {len(cases)} scanner cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
