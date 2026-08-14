"""Build conflict-aware governance file operation plans."""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from pathlib import Path

import markdown_sections as markdown
from agent_boundaries import find_human_governance_heading
from codeowners import normalize_owners
from file_operations import (
    Operation,
    assert_unique_paths,
    file_conflict,
    repo_path,
    safe_relative,
)
from governance_support import (
    AGENT_SECTION,
    HUMAN_SECTIONS,
    PR_SECTIONS,
    PROVIDER_FILES,
    codeowner_entries,
    locale_links,
    parse_codeowners,
    render,
    render_readme_section,
    template_section,
)
from legacy_artifacts import (
    LEGACY_MARKER,
    plan_legacy,
    strip_legacy_blocks,
)
from locales import normalize_locales
from translation_support import discover_locales, parse_translations, reviewed_content


def plan_sections(
    path: Path,
    full: str,
    titles: Iterable[str],
    *,
    final_title: str | None = None,
    reject_human_headings: bool = False,
) -> Operation:
    titles = tuple(titles)
    conflict = file_conflict(path, "standard governance path")
    if conflict:
        return conflict
    if not path.exists():
        return Operation(path, "create", content=full)
    existing = path.read_text(encoding="utf-8")
    try:
        desired = strip_legacy_blocks(existing)
        present = markdown.headings(desired)
        if reject_human_headings:
            human = find_human_governance_heading(present)
            if human:
                raise ValueError(
                    f"{path.name} contains human governance heading: {human.title}"
                )
        for title in titles:
            section = template_section(full, title)
            move_to_end = len(titles) > 1 or title == final_title
            desired = (
                markdown.move_section_to_end(desired, section, title)
                if move_to_end
                else markdown.replace_section(desired, section, title)
            )
    except ValueError as error:
        return Operation(path, "conflict", reason=str(error))
    return Operation(path, "noop" if desired == existing else "update", content=desired)


def plan_readme(
    path: Path, section: str, before: list[str], project_name: str
) -> Operation:
    conflict = file_conflict(path, "README path")
    if conflict:
        return conflict
    existing = (
        path.read_text(encoding="utf-8") if path.exists() else f"# {project_name}\n"
    )
    try:
        desired = markdown.insert_before_headings(
            strip_legacy_blocks(existing),
            section,
            "Contributing and coding agents",
            before,
        )
    except ValueError as error:
        return Operation(path, "conflict", reason=str(error))
    action = (
        "noop"
        if path.exists() and desired == existing
        else ("update" if path.exists() else "create")
    )
    return Operation(path, action, content=desired)


def plan_exact(path: Path, desired: str) -> Operation:
    conflict = file_conflict(path, "provider path")
    if conflict:
        return conflict
    if not path.exists():
        return Operation(path, "create", content=desired)
    if path.read_text(encoding="utf-8") != desired:
        return Operation(
            path,
            "conflict",
            reason="existing provider file differs from the standard import",
        )
    return Operation(path, "noop", content=desired)


def plan_translation(path: Path, desired: str) -> Operation:
    conflict = file_conflict(path, "translation path")
    if conflict:
        return conflict
    if not path.exists():
        return Operation(path, "create", content=desired)
    existing = path.read_text(encoding="utf-8")
    if existing == desired:
        return Operation(path, "noop", content=desired)
    if not existing.startswith(desired.splitlines()[0] + "\n"):
        return Operation(
            path,
            "conflict",
            reason="existing translation is not the expected standard document",
        )
    return Operation(path, "update", content=desired)


def plan_codeowners(path: Path, entries: dict[str, str]) -> Operation:
    conflict = file_conflict(path, "CODEOWNERS path")
    if conflict:
        return conflict
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    try:
        existing = strip_legacy_blocks(original)
        rules = parse_codeowners(existing, set(entries))
    except ValueError as error:
        return Operation(path, "conflict", reason=str(error))
    conflicts = [
        key for key, owners in entries.items() if key in rules and rules[key] != owners
    ]
    if conflicts:
        return Operation(
            path,
            "conflict",
            reason=f"different owners already govern: {', '.join(conflicts)}",
        )
    missing = [(key, owners) for key, owners in entries.items() if key not in rules]
    if not missing:
        return Operation(
            path, "noop" if existing == original else "update", content=existing
        )
    addition = "\n".join(f"{key} {owners}" for key, owners in missing)
    desired = existing.rstrip() + ("\n\n" if existing.strip() else "") + addition + "\n"
    return Operation(path, "update" if path.exists() else "create", content=desired)


def build_plan(args: argparse.Namespace) -> tuple[Path, list[str], list[Operation]]:
    root = args.repo.resolve()
    if not root.is_dir():
        raise ValueError(f"repository root is not a directory: {root}")
    readme = safe_relative(args.readme, "README")
    cli_locales = normalize_locales(args.locale)
    discovered = discover_locales(root)
    locales = normalize_locales([*cli_locales[1:], *discovered])
    human = parse_translations(args.human_translation, "human translation")
    agent = parse_translations(args.agent_translation, "agent translation")
    allowed = set(locales) - {"en"}
    extra = sorted((set(human) | set(agent)) - allowed)
    if extra:
        raise ValueError(
            f"translation provided for undeclared locale(s): {', '.join(extra)}"
        )
    for locale in allowed:
        paired = locale in human and locale in agent
        if (locale in human) != (locale in agent):
            raise ValueError(
                f"each locale requires both reviewed translations: {locale}"
            )
        if locale in cli_locales and locale not in discovered and not paired:
            raise ValueError(
                f"each new locale requires both reviewed translations: {locale}"
            )
        if locale in discovered and not paired:
            for name in ("CONTRIBUTING.md", "agent-guidance.md"):
                path = repo_path(root, f"docs/i18n/{locale}/{name}")
                if not path.is_file() or path.is_symlink():
                    raise ValueError(
                        f"existing locale requires both regular translation files: {locale}"
                    )
    fixed_targets = {
        Path("CONTRIBUTING.md"),
        Path("AGENTS.md"),
        Path("CLAUDE.md"),
        Path("GEMINI.md"),
        Path(".cursor/rules/agents.mdc"),
        Path(".github/pull_request_template.md"),
    }
    if readme in fixed_targets:
        raise ValueError(
            f"README path collides with a governance output: {readme.as_posix()}"
        )
    human_links, agent_links, _ = locale_links(locales, readme)
    values = {
        "PROJECT_NAME": args.project_name,
        "DESCRIPTION": args.description,
        "HUMAN_TRANSLATION_LINKS": human_links,
        "AGENT_TRANSLATION_LINKS": agent_links,
    }
    headings = args.before_heading or ["License", "Star History"]
    operations = plan_legacy(root)
    operations.append(
        plan_sections(
            repo_path(root, "CONTRIBUTING.md"),
            render("CONTRIBUTING.md.tmpl", **values),
            HUMAN_SECTIONS,
        )
    )
    operations.append(
        plan_sections(
            repo_path(root, "AGENTS.md"),
            render("AGENTS.md.tmpl", **values),
            (AGENT_SECTION,),
            final_title=AGENT_SECTION,
            reject_human_headings=True,
        )
    )
    operations.append(
        plan_sections(
            repo_path(root, ".github/pull_request_template.md"),
            render("pull-request-template.md.tmpl"),
            PR_SECTIONS,
        )
    )
    operations.append(
        plan_readme(
            repo_path(root, readme),
            render_readme_section(readme, locales),
            headings,
            args.project_name,
        )
    )
    for relative, asset in PROVIDER_FILES.items():
        operations.append(plan_exact(repo_path(root, relative), render(asset)))
    for locale in allowed:
        if locale not in human:
            continue
        operations.append(
            plan_translation(
                repo_path(root, f"docs/i18n/{locale}/CONTRIBUTING.md"),
                render(
                    "translated-contributing.md.tmpl",
                    LOCALE=locale,
                    TRANSLATED_CONTENT=reviewed_content(locale, human[locale]),
                ),
            )
        )
        operations.append(
            plan_translation(
                repo_path(root, f"docs/i18n/{locale}/agent-guidance.md"),
                render(
                    "translated-agents.md.tmpl",
                    LOCALE=locale,
                    TRANSLATED_CONTENT=reviewed_content(locale, agent[locale]),
                ),
            )
        )
    owners = normalize_owners(args.codeowner)
    codeowners_path = repo_path(root, ".github/CODEOWNERS")
    if owners:
        operations.append(
            plan_codeowners(codeowners_path, codeowner_entries(readme, owners))
        )
    elif codeowners_path.is_file() and LEGACY_MARKER in codeowners_path.read_text(
        encoding="utf-8"
    ):
        operations.append(plan_codeowners(codeowners_path, {}))
    assert_unique_paths(operations)
    return root, locales, operations


__all__ = [
    "build_plan",
    "plan_codeowners",
    "plan_exact",
    "plan_readme",
    "plan_sections",
    "plan_translation",
]
