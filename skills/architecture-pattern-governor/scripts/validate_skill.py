#!/usr/bin/env python3
"""Validate the portable structure and internal references of this Agent Skill."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REL_REF_RE = re.compile(r"(?<![A-Za-z0-9_])((?:references|assets|scripts)/[A-Za-z0-9_.-]+)")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\((?!https?://|#|mailto:)([^)]+)\)")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'.")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter has no closing '---'.") from exc

    data: dict[str, str] = {}
    current_parent: str | None = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")):
            # Nested metadata is valid but not needed for required-field checks.
            continue
        if ":" not in raw:
            raise ValueError(f"Malformed frontmatter line: {raw!r}")
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        data[key] = value
        current_parent = key
    return data, "\n".join(lines[end + 1 :])


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_file = root / "SKILL.md"

    if not skill_file.is_file():
        return [f"Missing required file: {skill_file}"], warnings

    text = skill_file.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)], warnings

    name = fm.get("name", "")
    description = fm.get("description", "")
    if not name:
        errors.append("Frontmatter requires non-empty 'name'.")
    elif not NAME_RE.fullmatch(name):
        errors.append("'name' must contain lowercase letters/digits separated by single hyphens.")
    if len(name) > 64:
        errors.append("'name' exceeds 64 characters.")
    if root.name != name:
        errors.append(f"Folder name {root.name!r} must match skill name {name!r}.")

    if not description:
        errors.append("Frontmatter requires non-empty 'description'.")
    if len(description) > 1024:
        errors.append("'description' exceeds 1024 characters.")

    line_count = len(text.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md has {line_count} lines; keep the core under 500 where possible.")
    rough_tokens = len(re.findall(r"\w+|[^\w\s]", text))
    if rough_tokens > 7000:
        warnings.append(f"SKILL.md rough token count is {rough_tokens}; progressive disclosure may be weakened.")

    refs = set(REL_REF_RE.findall(text))
    refs.update(link.split("#", 1)[0] for link in MARKDOWN_LINK_RE.findall(text))
    for rel in sorted(refs):
        target = root / rel
        if not target.exists():
            errors.append(f"Broken relative reference in SKILL.md: {rel}")

    required_sections = [
        "# Architecture Pattern Governor",
        "## Mission",
        "## Non-negotiable conduct",
        "## Mandatory workflow",
        "## Completion condition",
    ]
    for heading in required_sections:
        if heading not in text:
            errors.append(f"Missing required core heading: {heading}")

    # Check internal references from every Markdown file, without trying to resolve code examples.
    for md in sorted(root.rglob("*.md")):
        md_text = md.read_text(encoding="utf-8")
        for link in MARKDOWN_LINK_RE.findall(md_text):
            clean = link.split("#", 1)[0]
            if not clean:
                continue
            target = (md.parent / clean).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                warnings.append(f"Relative link leaves the skill root in {md.relative_to(root)}: {link}")
                continue
            if not target.exists():
                errors.append(f"Broken Markdown link in {md.relative_to(root)}: {link}")

    if not (root / "LICENSE").exists():
        warnings.append("No LICENSE file is present.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors, warnings = validate(root)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"PASS: {root} ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
