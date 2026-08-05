#!/usr/bin/env python3
"""Audit progressive-disclosure Markdown for tracked repository skills."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from audit_skill_routing import REQUIRED_TERMS

ROOT = Path(__file__).resolve().parents[1]
ISSUES = ROOT / "skills" / "prompt-engineering" / "references" / "issues"
ISSUE_HEADINGS = (
    "## Use this case",
    "## Trigger",
    "## Observed failure",
    "## Required behavior",
    "## Example",
    "## Acceptance check",
    "## Evaluation use",
)


def tracked_markdown() -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "skills/**/*.md"],
        check=True,
        capture_output=True,
        text=True,
    )
    paths: list[Path] = []
    for line in result.stdout.splitlines():
        path = ROOT / line
        relative = path.relative_to(ROOT)
        if len(relative.parts) < 2 or relative.parts[1] not in REQUIRED_TERMS:
            continue
        if relative.parts[:3] == ("skills", "apple-design-hig", "references"):
            continue
        paths.append(path)
    return paths


def main() -> int:
    errors: list[str] = []
    paths = tracked_markdown()
    for path in paths:
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        if path.name == "SKILL.md":
            continue
        if ISSUES in path.parents:
            for heading in ISSUE_HEADINGS:
                if heading not in text:
                    errors.append(f"{relative}: missing {heading}")
            if "## Efficiency note" in text:
                errors.append(f"{relative}: stale generic efficiency section remains")
            continue
        if "references" in relative.parts and "## Use this reference" not in text:
            errors.append(f"{relative}: missing progressive-disclosure routing")
        if "assets" in relative.parts and path.suffix == ".md":
            if "## Use this template" not in text:
                errors.append(f"{relative}: missing template-use contract")

    package = ROOT / "skills" / "architecture-design"
    package_contracts = {
        package / "README.md": "## Outcome",
        package / "CHANGELOG.md": "## Unreleased",
        package / "SOURCE-MANIFEST.md": "## Evidence policy",
    }
    for path, heading in package_contracts.items():
        if heading not in path.read_text(encoding="utf-8"):
            errors.append(f"{path.relative_to(ROOT)}: missing {heading}")

    index = (
        ROOT / "skills" / "prompt-engineering" / "references" / "issue-corpus-index.md"
    ).read_text(encoding="utf-8")
    indexed = set(re.findall(r"`(issues/[^`]+\.md)`", index))
    actual = {
        path.relative_to(ISSUES.parent).as_posix()
        for path in ISSUES.rglob("*.md")
    }
    if indexed != actual:
        errors.append(
            "prompt issue index mismatch: "
            f"missing={sorted(actual - indexed)}, stale={sorted(indexed - actual)}"
        )

    if errors:
        print("skill Markdown audit: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"skill Markdown audit: PASS ({len(paths)} tracked files, Apple generated references excluded)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
