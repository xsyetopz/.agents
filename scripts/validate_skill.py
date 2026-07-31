#!/usr/bin/env python3
"""Validate the portable structure and internal references of an Agent Skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REL_REF_RE = re.compile(
    r"(?<![A-Za-z0-9_])((?:references|assets|scripts)/[A-Za-z0-9_.-]+)"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\((?!https?://|#|mailto:)([^)]+)\)")
FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})", re.MULTILINE)


def strip_fenced_blocks(text: str) -> str:
    result: list[str] = []
    in_fence: str | None = None
    for line in text.splitlines(keepends=True):
        if in_fence is None:
            m = FENCE_RE.match(line)
            if m:
                in_fence = m.group(1)[0]
                result.append("\n")
            else:
                result.append(line)
        else:
            m = FENCE_RE.match(line)
            if m and m.group(1)[0] == in_fence and len(m.group(1)) >= 3:
                in_fence = None
                result.append("\n")
    return "".join(result)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'.")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter has no closing '---'.") from exc

    data: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")):
            continue
        if ":" not in raw:
            raise ValueError(f"Malformed frontmatter line: {raw!r}")
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, "\n".join(lines[end + 1 :])


def load_config(root: Path) -> dict:
    config_path = root / ".skill-validator.json"
    if config_path.is_file():
        try:
            return json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid .skill-validator.json: {exc}") from exc
    return {}


def check_frontmatter(fm: dict, root: Path, errors: list[str]) -> None:
    name = fm.get("name", "")
    description = fm.get("description", "")
    if not name:
        errors.append("Frontmatter requires non-empty 'name'.")
    elif not NAME_RE.fullmatch(name):
        errors.append(
            "'name' must contain lowercase letters/digits separated by single hyphens."
        )
    if len(name) > 64:
        errors.append("'name' exceeds 64 characters.")
    if root.name != name:
        errors.append(f"Folder name {root.name!r} must match skill name {name!r}.")
    if not description:
        errors.append("Frontmatter requires non-empty 'description'.")
    if len(description) > 1024:
        errors.append("'description' exceeds 1024 characters.")


def check_size(text: str, warnings: list[str]) -> None:
    line_count = len(text.splitlines())
    if line_count > 500:
        warnings.append(
            f"SKILL.md has {line_count} lines; keep the core under 500 where possible."
        )
    rough_tokens = len(re.findall(r"\w+|[^\w\s]", text))
    if rough_tokens > 7000:
        warnings.append(
            f"SKILL.md rough token count is {rough_tokens}; progressive disclosure may be weakened."
        )


def check_required_headings(text: str, config: dict, errors: list[str]) -> None:
    unfenced = strip_fenced_blocks(text)
    for heading in config.get("required_headings", []):
        if heading not in unfenced:
            errors.append(f"Missing required heading: {heading}")


def check_required_files(root: Path, config: dict, errors: list[str]) -> None:
    for relative in config.get("required_files", []):
        if not (root / relative).is_file():
            errors.append(f"Missing required file: {relative}")


def check_broken_references(text: str, root: Path, errors: list[str]) -> None:
    unfenced = strip_fenced_blocks(text)
    refs = set(REL_REF_RE.findall(unfenced))
    refs.update(link.split("#", 1)[0] for link in MARKDOWN_LINK_RE.findall(unfenced))
    for rel in sorted(refs):
        if not (root / rel).exists():
            errors.append(f"Broken relative reference in SKILL.md: {rel}")


def check_markdown_links(root: Path, errors: list[str], warnings: list[str]) -> None:
    for md in sorted(root.rglob("*.md")):
        md_text = md.read_text(encoding="utf-8")
        md_unfenced = strip_fenced_blocks(md_text)
        for link in MARKDOWN_LINK_RE.findall(md_unfenced):
            clean = link.split("#", 1)[0]
            if not clean:
                continue
            target = (md.parent / clean).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                warnings.append(
                    f"Relative link leaves the skill root in {md.relative_to(root)}: {link}"
                )
                continue
            if not target.exists():
                errors.append(f"Broken Markdown link in {md.relative_to(root)}: {link}")


def warn_missing_license(root: Path, warnings: list[str]) -> None:
    if not (root / "LICENSE").exists():
        warnings.append("No LICENSE file is present.")


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    config = load_config(root)
    skill_file = root / "SKILL.md"

    if not skill_file.is_file():
        return [f"Missing required file: {skill_file}"], warnings

    text = skill_file.read_text(encoding="utf-8")
    try:
        fm, _body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)], warnings

    check_frontmatter(fm, root, errors)
    check_size(text, warnings)
    check_required_headings(text, config, errors)
    check_required_files(root, config, errors)
    check_broken_references(text, root, errors)
    check_markdown_links(root, errors, warnings)
    warn_missing_license(root, warnings)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Agent Skill structure.")
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Skill root directory (default: current working directory).",
    )
    args = parser.parse_args()
    errors, warnings = validate(args.root.resolve())

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"PASS: {args.root.resolve()} ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
