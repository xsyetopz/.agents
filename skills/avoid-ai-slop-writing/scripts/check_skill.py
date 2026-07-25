#!/usr/bin/env python3
"""Check the local skill layout and self-consistency."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/pattern-catalogue.md",
    "references/phrases.tsv",
    "references/seed-lexicon.tsv",
    "scripts/scan_text.py",
    "scripts/structure_scan.py",
    "scripts/check_semantics.py",
)


def check_tsv(path: Path, fields: int, errors: list[str]) -> None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        errors.append(f"cannot read {path}: {error}")
        return
    for number, line in enumerate(lines, start=1):
        if not line or line.startswith("#"):
            continue
        if len(line.split("\t")) != fields:
            errors.append(f"{path.name}:{number} does not have {fields} TSV fields")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        errors.append("missing SKILL.md")
        print("\n".join(errors))
        return 1
    skill = skill_path.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    if not frontmatter:
        errors.append("SKILL.md has no YAML frontmatter")
    else:
        block = frontmatter.group(1)
        if "name: avoid-ai-slop-writing" not in block:
            errors.append("frontmatter name does not match directory")
        if "description:" not in block:
            errors.append("frontmatter description is missing")
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    check_tsv(root / "references" / "phrases.tsv", 4, errors)
    check_tsv(root / "references" / "seed-lexicon.tsv", 5, errors)
    if len(skill.splitlines()) > 500:
        errors.append("SKILL.md exceeds the progressive-disclosure size target")
    removed_name = "-".join(("plain", "developer", "writing"))
    if removed_name in skill:
        errors.append("skill body contains the removed skill name")
    if errors:
        print("\n".join(f"error: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Skill layout valid: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
