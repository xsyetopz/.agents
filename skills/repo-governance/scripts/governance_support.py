"""Shared constants and pure rendering helpers for governance planning."""

from __future__ import annotations

import posixpath
import re
from pathlib import Path

import markdown_sections as markdown
from agent_boundaries import find_human_governance_heading
from codeowners import normalize_owners, parse_rules
from legacy_artifacts import LEGACY_MARKER

SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"
PROVIDER_FILES = {
    "CLAUDE.md": "CLAUDE.md.tmpl",
    "GEMINI.md": "GEMINI.md.tmpl",
    ".cursor/rules/agents.mdc": "cursor-rule.mdc.tmpl",
}
HUMAN_SECTIONS = (
    "Contribution requirements",
    "Tool-assisted contributions",
    "Languages",
)
PR_SECTIONS = ("Summary", "Related work", "Validation", "Tool assistance", "Checklist")
AGENT_SECTION = "Agent rules"
README_SECTION = "Contributing and coding agents"


def render(name: str, **values: str) -> str:
    """Render an asset template and reject any unresolved placeholders."""
    text = (ASSETS / name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"{{([A-Z0-9_]+)}}", text)))
    if unresolved:
        raise ValueError(f"unresolved values in {name}: {', '.join(unresolved)}")
    return text.rstrip() + "\n"


def clean_scalar(value: str, label: str) -> str:
    """Validate a command-line value that is expected to be one safe line."""
    result = value.strip()
    if not result or any(character in result for character in ("\n", "\r", "\x00")):
        raise ValueError(f"{label} must be one non-empty line")
    if "{{" in result or LEGACY_MARKER in result:
        raise ValueError(f"{label} contains a reserved sequence")
    return result


def template_section(full: str, title: str) -> str:
    try:
        return markdown.section(full, title)
    except ValueError as error:
        raise ValueError(f"invalid template section {title}: {error}") from error


def link_from(readme: Path, target: Path) -> str:
    parent = readme.parent.as_posix()
    return posixpath.relpath(target.as_posix(), "." if parent == "." else parent)


def locale_links(locales: list[str], readme: Path) -> tuple[str, str, str]:
    non_english = [locale for locale in locales if locale != "en"]
    human = (
        ", ".join(
            f"[{locale}](docs/i18n/{locale}/CONTRIBUTING.md)" for locale in non_english
        )
        or "none"
    )
    agent = (
        ", ".join(
            f"[{locale}](docs/i18n/{locale}/agent-guidance.md)"
            for locale in non_english
        )
        or "none"
    )
    readme_links = (
        ", ".join(
            f"[{locale} human]({link_from(readme, Path(f'docs/i18n/{locale}/CONTRIBUTING.md'))}) "
            f"and [{locale} agent]({link_from(readme, Path(f'docs/i18n/{locale}/agent-guidance.md'))})"
            for locale in non_english
        )
        or "none"
    )
    return human, agent, readme_links


def render_readme_section(readme: Path, locales: list[str]) -> str:
    _, _, translations = locale_links(locales, readme)
    return render(
        "readme-section.md.tmpl",
        README_CONTRIBUTING_LINK=link_from(readme, Path("CONTRIBUTING.md")),
        README_AGENTS_LINK=link_from(readme, Path("AGENTS.md")),
        README_TRANSLATION_LINKS=translations,
    )


def codeowner_entries(readme: Path, owners: list[str]) -> dict[str, str]:
    owner_text = " ".join(owners)
    paths = (
        "/CONTRIBUTING.md",
        "/AGENTS.md",
        "/CLAUDE.md",
        "/GEMINI.md",
        "/.cursor/rules/agents.mdc",
        "/.github/pull_request_template.md",
        "/.github/CODEOWNERS",
        "/docs/i18n/",
        "/" + readme.as_posix(),
    )
    return dict.fromkeys(paths, owner_text)


def parse_codeowners(text: str, governed: set[str] | None = None) -> dict[str, str]:
    return parse_rules(text, governed)


__all__ = [
    "AGENT_SECTION",
    "ASSETS",
    "HUMAN_SECTIONS",
    "PROVIDER_FILES",
    "PR_SECTIONS",
    "README_SECTION",
    "SKILL_ROOT",
    "clean_scalar",
    "codeowner_entries",
    "find_human_governance_heading",
    "link_from",
    "locale_links",
    "normalize_owners",
    "parse_codeowners",
    "parse_rules",
    "render",
    "render_readme_section",
    "template_section",
]
