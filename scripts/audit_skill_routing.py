#!/usr/bin/env python3
"""Audit discovery descriptions for the repository's tracked skills."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from validate_skill import parse_frontmatter

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_TERMS = {
    "apple-design-hig": ("apple hig", "voiceover", "visionos", "sf symbols"),
    "architecture-design": ("architecture", "adr", "bounded contexts", "quality-attribute"),
    "architecture-enforce": ("file shattering", "lint suppression", "source topology", "three or more"),
    "avoid-ai-writing": ("ai-isms", "humanize this", "detect", "rewrite"),
    "git-actions": ("github api", "gitlab api", "pull requests", "workflow dispatch"),
    "git-ci-cd": ("github actions", "gitlab ci", "workflow yaml", "runner"),
    "git-toolkit": ("stage", "commit", "conventional commits", "rebase", "reflog"),
    "git-workflows": ("branching", "merge strategy", "branch protection", "github flow"),
    "prompt-engineering": ("system prompts", "tool routing", "behavioral evals", "gpt-5.6"),
    "repo-docs": ("readme.md", "changelog.md", "keep a changelog", "release notes"),
    "repo-governance": ("contributing.md", "agents.md", "codeowners", "pull-request templates"),
    "skill-creator": ("skill.md", "trigger keywords", "skill routing", "progressive disclosure"),
}

# Discovery descriptions are loaded for every turn, so keep this catalog surface
# compact while leaving enough room for routing terms and one boundary.
MIN_DESCRIPTION_LENGTH = 80
MAX_DESCRIPTION_LENGTH = 240


def tracked_skill_files() -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "skills/*/SKILL.md"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [ROOT / line for line in result.stdout.splitlines() if line]


def main() -> int:
    errors: list[str] = []
    files = tracked_skill_files()
    found = {path.parent.name for path in files}
    if found != set(REQUIRED_TERMS):
        errors.append(
            "routing inventory differs from tracked skills: "
            f"missing={sorted(set(REQUIRED_TERMS) - found)}, "
            f"unmapped={sorted(found - set(REQUIRED_TERMS))}"
        )

    for path in files:
        metadata, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        name = metadata.get("name", path.parent.name)
        description = metadata.get("description", "")
        folded = description.casefold()
        if not MIN_DESCRIPTION_LENGTH <= len(description) <= MAX_DESCRIPTION_LENGTH:
            errors.append(
                f"{name}: description length {len(description)} is outside "
                f"{MIN_DESCRIPTION_LENGTH}-{MAX_DESCRIPTION_LENGTH} compact range"
            )
        for term in REQUIRED_TERMS.get(name, ()):
            if term.casefold() not in folded:
                errors.append(f"{name}: missing routing term {term!r}")

    if errors:
        print("skill routing audit: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"skill routing audit: PASS ({len(files)} tracked skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
