"""Validate the standard governance surface without mutating a repository."""

from __future__ import annotations

from pathlib import Path

import markdown_sections as markdown
from agent_boundaries import is_human_governance_heading
from codeowners import parse_rules
from file_operations import repo_path
from governance_support import (
    AGENT_SECTION,
    HUMAN_SECTIONS,
    PR_SECTIONS,
    PROVIDER_FILES,
    codeowner_entries,
    locale_links,
    render,
    render_readme_section,
    template_section,
)
from legacy_artifacts import validate_no_legacy
from locales import normalize_locales
from section_validation import exact_sections
from translation_support import discover_locales


def validate(
    root: Path, locales: list[str], readme: Path, before: list[str], owners: list[str]
) -> list[str]:
    if not root.is_dir():
        return [f"repository root is not a directory: {root}"]
    errors: list[str] = []
    try:
        discovered = discover_locales(root)
        locales = normalize_locales([*locales[1:], *discovered])
        human_links, agent_links, _ = locale_links(locales, readme)
        values = {
            "PROJECT_NAME": "Validation",
            "DESCRIPTION": "Validation.",
            "HUMAN_TRANSLATION_LINKS": human_links,
            "AGENT_TRANSLATION_LINKS": agent_links,
        }
        contributing = repo_path(root, "CONTRIBUTING.md")
        agents = repo_path(root, "AGENTS.md")
        pr = repo_path(root, ".github/pull_request_template.md")
        errors.extend(
            exact_sections(
                contributing, render("CONTRIBUTING.md.tmpl", **values), HUMAN_SECTIONS
            )
        )
        agent_full = render("AGENTS.md.tmpl", **values)
        errors.extend(exact_sections(agents, agent_full, (AGENT_SECTION,)))
        if agents.is_file() and not agents.is_symlink():
            text = agents.read_text(encoding="utf-8")
            real_headings = markdown.headings(text)
            agent_matches = markdown.matching_headings(text, AGENT_SECTION, 2)
            if len(agent_matches) == 1:
                later_h2 = [
                    heading
                    for heading in real_headings
                    if heading.level == 2 and heading.start > agent_matches[0].start
                ]
                final_text = text[agent_matches[0].start :].strip() + "\n"
                if later_h2 or final_text != template_section(
                    agent_full, AGENT_SECTION
                ):
                    errors.append(
                        "AGENTS.md Agent rules must be the exact final level-2 section"
                    )
            for heading in real_headings:
                if is_human_governance_heading(heading.title, heading.level):
                    errors.append(
                        f"AGENTS.md must not contain human governance heading: {heading.title}"
                    )
        errors.extend(
            exact_sections(pr, render("pull-request-template.md.tmpl"), PR_SECTIONS)
        )
        if contributing.is_file() and markdown.matching_headings(
            contributing.read_text(encoding="utf-8"), AGENT_SECTION
        ):
            errors.append(
                "CONTRIBUTING.md must not contain the coding-agent execution section"
            )
        for relative, asset in PROVIDER_FILES.items():
            path = repo_path(root, relative)
            if (
                not path.is_file()
                or path.is_symlink()
                or path.read_text(encoding="utf-8") != render(asset)
            ):
                errors.append(
                    f"{relative} must exactly match the standard provider import"
                )
        readme_path = repo_path(root, readme)
        if not readme_path.is_file() or readme_path.is_symlink():
            errors.append(
                f"README is missing or is not a regular file: {readme.as_posix()}"
            )
        else:
            text = readme_path.read_text(encoding="utf-8")
            try:
                actual = markdown.section(text, "Contributing and coding agents")
                if actual != render_readme_section(readme, locales):
                    errors.append(
                        "README has a modified Contributing and coding agents section"
                    )
                owned = markdown.matching_headings(
                    text, "Contributing and coding agents", 2
                )[0]
                before_titles = {title.casefold() for title in before}
                for heading in markdown.headings(text):
                    if (
                        heading.title.casefold() in before_titles
                        and owned.start > heading.start
                    ):
                        errors.append(
                            f"README governance section must precede heading: {heading.title}"
                        )
            except (ValueError, IndexError):
                errors.append(
                    "README must contain one level-2 Contributing and coding agents section"
                )
        for locale in locales:
            if locale == "en":
                continue
            for name, root_target in (
                ("CONTRIBUTING.md", "../../../CONTRIBUTING.md"),
                ("agent-guidance.md", "../../../AGENTS.md"),
            ):
                path = repo_path(root, f"docs/i18n/{locale}/{name}")
                if not path.is_file() or path.is_symlink():
                    errors.append(
                        f"reviewed translation is missing: docs/i18n/{locale}/{name}"
                    )
                    continue
                text = path.read_text(encoding="utf-8")
                asset = (
                    "translated-contributing.md.tmpl"
                    if name == "CONTRIBUTING.md"
                    else "translated-agents.md.tmpl"
                )
                sentinel = "__REVIEWED_TRANSLATION_CONTENT__"
                expected_prefix = render(
                    asset, LOCALE=locale, TRANSLATED_CONTENT=sentinel
                ).split(sentinel, 1)[0]
                if (
                    not text.startswith(expected_prefix)
                    or root_target not in expected_prefix
                ):
                    errors.append(
                        f"translation has an invalid root link or locale: docs/i18n/{locale}/{name}"
                    )
        if owners:
            path = repo_path(root, ".github/CODEOWNERS")
            if not path.is_file() or path.is_symlink():
                errors.append(".github/CODEOWNERS is missing")
            else:
                entries = codeowner_entries(readme, owners)
                rules = parse_rules(path.read_text(encoding="utf-8"), set(entries))
                for governed, expected in entries.items():
                    if rules.get(governed) != expected:
                        errors.append(
                            f"CODEOWNERS has missing or different owners for {governed}"
                        )
        errors.extend(validate_no_legacy(root))
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(str(error))
    return errors


__all__ = ["validate"]
