"""Validate the repository's One Way Only skill entrypoint contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED_HEADINGS = ["Start with evidence", "Workflow", "Validation", "Boundaries"]
SKILL_REFERENCE = re.compile(r"\$([a-z0-9][a-z0-9-]*)")
VALID_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def frontmatter_name(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    match = re.search(r"(?m)^name:\s*([^\s#]+)\s*$", text[4:end])
    return match.group(1) if match else None


def audit_skill(directory: Path, skill_names: set[str]) -> list[str]:
    issues: list[str] = []
    skill_file = directory / "SKILL.md"
    agent_file = directory / "agents" / "openai.yaml"

    if not skill_file.is_file():
        return [f"{directory.relative_to(ROOT)}: missing SKILL.md"]

    text = skill_file.read_text(encoding="utf-8")
    name = frontmatter_name(text)
    if name is None:
        issues.append(f"{skill_file.relative_to(ROOT)}: missing frontmatter name")
    elif not VALID_NAME.fullmatch(name):
        issues.append(f"{skill_file.relative_to(ROOT)}: invalid skill name {name!r}")
    elif name != directory.name:
        issues.append(
            f"{skill_file.relative_to(ROOT)}: frontmatter name {name!r} does not match folder {directory.name!r}"
        )

    headings = re.findall(r"(?m)^## (.+)$", text)
    if headings != EXPECTED_HEADINGS:
        issues.append(
            f"{skill_file.relative_to(ROOT)}: top-level headings are {headings!r}; expected {EXPECTED_HEADINGS!r}"
        )
    else:
        heading_matches = list(re.finditer(r"(?m)^## (.+)$", text))
        for index, match in enumerate(heading_matches):
            end = (
                heading_matches[index + 1].start()
                if index + 1 < len(heading_matches)
                else len(text)
            )
            if not text[match.end() : end].strip():
                issues.append(
                    f"{skill_file.relative_to(ROOT)}: section {match.group(1)!r} is empty"
                )

    references = sorted(set(SKILL_REFERENCE.findall(text)))
    if references:
        issues.append(
            f"{skill_file.relative_to(ROOT)}: hard companion-skill references are forbidden: {references!r}"
        )

    if not agent_file.is_file():
        issues.append(f"{agent_file.relative_to(ROOT)}: missing UI metadata")
    elif name:
        agent_references = sorted(
            set(SKILL_REFERENCE.findall(agent_file.read_text(encoding="utf-8")))
        )
        unexpected = [reference for reference in agent_references if reference != name]
        if unexpected:
            issues.append(
                f"{agent_file.relative_to(ROOT)}: references other skill names: {unexpected!r}"
            )

    instruction_files = [skill_file]
    if agent_file.is_file():
        instruction_files.append(agent_file)
    references = directory / "references"
    if references.is_dir():
        instruction_files.extend(sorted(references.rglob("*.md")))

    for instruction_file in instruction_files:
        instruction_text = instruction_file.read_text(encoding="utf-8")
        other_names = sorted(
            candidate
            for candidate in skill_names
            if candidate != directory.name
            and re.search(
                rf"(?<![a-z0-9-]){re.escape(candidate)}(?![a-z0-9-])", instruction_text
            )
        )
        if other_names:
            issues.append(
                f"{instruction_file.relative_to(ROOT)}: names companion skills directly: {other_names!r}"
            )

    return issues


def main() -> int:
    issues: list[str] = []
    directories = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    skill_names = {directory.name for directory in directories}
    for directory in directories:
        issues.extend(audit_skill(directory, skill_names))

    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    print(f"OWO skill structure valid for {len(directories)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
