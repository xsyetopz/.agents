#!/usr/bin/env python3
"""Validate an Agent Skill against the agentskills.io specification.

Enforces:
- SKILL.md frontmatter (name, description, optional fields per spec)
- Directory structure (agents/openai.yaml, .skill-validator.json, LICENSE)
- File size limits (SKILL.md ≤ 500 lines recommended, ≤ 800 hard max)
- Progressive disclosure (monolithic SKILL.md without references/ rejected)
- Internal reference integrity (no broken relative links or refs)
- Heading uniqueness, required headings and files from .skill-validator.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --- Regex constants ---

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REL_REF_RE = re.compile(
    r"(?<![A-Za-z0-9_])((?:references|assets|scripts)/[A-Za-z0-9_.-]+)"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\((?!https?://|#|mailto:)([^)]+)\)")
FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)(?:\s*\{#[^\}]+\})?\s*$")
CHANGELOG_VERSION_RE = re.compile(r"^##\s+\[[\d.]+(?:-[^\]]+)?\]")

SKILL_MD_LINE_WARN = 500
SKILL_MD_LINE_ERROR = 800


# --- Helpers ---

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
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key == "metadata":
            continue  # nested map — skip; full YAML parse out of scope
        data[key] = value
    return data, "\n".join(lines[end + 1:])


def load_config(root: Path) -> dict:
    config_path = root / ".skill-validator.json"
    if config_path.is_file():
        try:
            return json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid .skill-validator.json: {exc}") from exc
    return {}


# --- Spec compliance checks ---

def check_frontmatter_spec(fm: dict, root: Path, errors: list[str]) -> None:
    """Validate frontmatter against the Agent Skills specification."""
    name = fm.get("name", "")
    description = fm.get("description", "")

    # name: required, 1–64 chars, lowercase a-z/0-9/hyphens, no leading/trailing/--
    if not name:
        errors.append("Frontmatter requires non-empty 'name'.")
    else:
        if len(name) > 64:
            errors.append(f"'name' exceeds 64 characters (got {len(name)}).")
        if not NAME_RE.fullmatch(name):
            errors.append(
                "'name' must be lowercase letters/digits separated by single hyphens, "
                "no leading/trailing hyphens, no consecutive hyphens."
            )
        if name.startswith("-") or name.endswith("-"):
            errors.append("'name' must not start or end with a hyphen.")
        if "--" in name:
            errors.append("'name' must not contain consecutive hyphens.")

    # name must match directory name
    if root.name != name:
        errors.append(f"Folder name {root.name!r} must match skill name {name!r}.")

    # description: required, 1–1024 chars
    if not description:
        errors.append("Frontmatter requires non-empty 'description'.")
    elif len(description) > 1024:
        errors.append(f"'description' exceeds 1024 characters (got {len(description)}).")

    # compatibility: optional, max 500 chars if present
    compatibility = fm.get("compatibility", "")
    if compatibility and len(compatibility) > 500:
        errors.append(
            f"'compatibility' exceeds 500 characters (got {len(compatibility)})."
        )


def check_file_size(root: Path, errors: list[str], warnings: list[str]) -> None:
    """Enforce SKILL.md size limits per progressive disclosure guidelines."""
    skill_file = root / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    line_count = len(text.splitlines())

    if line_count > SKILL_MD_LINE_ERROR:
        errors.append(
            f"SKILL.md is {line_count} lines — hard limit is {SKILL_MD_LINE_ERROR}. "
            "Split content into references/ files."
        )
    elif line_count > SKILL_MD_LINE_WARN:
        warnings.append(
            f"SKILL.md has {line_count} lines; spec recommends ≤ {SKILL_MD_LINE_WARN}. "
            "Move detailed material to references/."
        )

    rough_tokens = len(re.findall(r"\w+|[^\w\s]", text))
    if rough_tokens > 7000:
        warnings.append(
            f"SKILL.md rough token count is {rough_tokens}; "
            "progressive disclosure may be weakened."
        )


def check_progressive_disclosure(root: Path, errors: list[str]) -> None:
    """Reject monolithic SKILL.md that violates progressive disclosure."""
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        return

    line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    has_references = (root / "references").is_dir()
    has_agents = (root / "agents").is_dir()

    if line_count > SKILL_MD_LINE_WARN and not has_references:
        errors.append(
            f"SKILL.md is {line_count} lines with no references/ directory. "
            "Split detailed content into references/ per progressive disclosure spec."
        )

    if not has_agents or not (root / "agents" / "openai.yaml").is_file():
        errors.append(
            "Missing required agents/openai.yaml. Every skill must include "
            "an OpenAI-compatible runtime metadata file."
        )


def check_skill_validator_config(root: Path, errors: list[str]) -> None:
    """Require .skill-validator.json."""
    if not (root / ".skill-validator.json").is_file():
        errors.append("Missing required .skill-validator.json.")


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


def check_duplicate_headers(root: Path, errors: list[str]) -> None:
    for md in sorted(root.rglob("*.md")):
        md_text = md.read_text(encoding="utf-8")
        md_unfenced = strip_fenced_blocks(md_text)
        seen: dict[str, int] = {}
        rel = md.relative_to(root)

        # Files that intentionally repeat headers per example/template
        is_changelog = rel.name == "CHANGELOG.md"
        is_worked_examples = "worked-examples" in rel.name.lower()

        for line_no, line in enumerate(md_unfenced.splitlines(), 1):
            m = HEADING_RE.match(line.strip())
            if not m:
                continue
            heading = m.group(0).strip()

            # Version headers in CHANGELOG.md are intentionally repeated
            if is_changelog and bool(CHANGELOG_VERSION_RE.match(heading)):
                continue

            # Level-3+ headers in worked-examples files repeat per example
            if is_worked_examples and heading.startswith("###"):
                continue

            if heading in seen:
                errors.append(
                    f"Duplicate heading in {rel}:{line_no}: "
                    f"{heading!r} (first at line {seen[heading]})"
                )
            else:
                seen[heading] = line_no


def warn_missing_license(root: Path, warnings: list[str]) -> None:
    if not (root / "LICENSE").exists():
        warnings.append("No LICENSE file is present.")


def check_agents_yaml(root: Path, errors: list[str]) -> None:
    """Validate agents/openai.yaml structure."""
    yaml_path = root / "agents" / "openai.yaml"
    if not yaml_path.is_file():
        return  # caught by check_progressive_disclosure
    text = yaml_path.read_text(encoding="utf-8")
    if "interface:" not in text:
        errors.append("agents/openai.yaml is missing required 'interface:' key.")
    if "display_name:" not in text:
        errors.append("agents/openai.yaml is missing required 'display_name'.")
    if "default_prompt:" not in text:
        errors.append("agents/openai.yaml is missing required 'default_prompt'.")
    if "$" not in text:
        warnings = []  # placeholder — add to validate() if needed


# --- Main validation ---

def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    config = load_config(root)
    skill_file = root / "SKILL.md"

    if not skill_file.is_file():
        return [f"Missing required SKILL.md at {skill_file}"], warnings

    text = skill_file.read_text(encoding="utf-8")
    try:
        fm, _body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)], warnings

    # Spec compliance
    check_frontmatter_spec(fm, root, errors)
    check_file_size(root, errors, warnings)
    check_progressive_disclosure(root, errors)
    check_skill_validator_config(root, errors)
    check_agents_yaml(root, errors)

    # Config-driven checks
    check_required_headings(text, config, errors)
    check_required_files(root, config, errors)

    # Reference integrity
    check_broken_references(text, root, errors)
    check_markdown_links(root, errors, warnings)
    check_duplicate_headers(root, errors)

    # Recommendations
    warn_missing_license(root, warnings)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an Agent Skill against the agentskills.io specification."
    )
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
