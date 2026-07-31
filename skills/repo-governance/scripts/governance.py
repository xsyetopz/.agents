#!/usr/bin/env python3
"""Preview, apply, and validate standard repository governance files."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from pathlib import Path
from typing import Iterable

import markdown_sections as markdown
from agent_boundaries import find_human_governance_heading, is_human_governance_heading
from codeowners import normalize_owners, parse_rules
from file_operations import (
    Operation,
    apply_transaction,
    assert_unique_paths,
    file_conflict,
    repo_path,
    safe_relative,
)
from legacy_artifacts import (
    LEGACY_MARKER,
    LEGACY_PATHS as LEGACY_PATHS,
    LEGACY_TOKENS as LEGACY_TOKENS,
    plan_legacy,
    strip_legacy_blocks,
    validate_no_legacy,
)
from locales import normalize_locales
from section_validation import exact_sections
from translation_support import discover_locales, parse_translations, reviewed_content


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
    text = (ASSETS / name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"{{([A-Z0-9_]+)}}", text)))
    if unresolved:
        raise ValueError(f"unresolved values in {name}: {', '.join(unresolved)}")
    return text.rstrip() + "\n"


def clean_scalar(value: str, label: str) -> str:
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
            strip_legacy_blocks(existing), section, README_SECTION, before
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
                actual = markdown.section(text, README_SECTION)
                if actual != render_readme_section(readme, locales):
                    errors.append(
                        "README has a modified Contributing and coding agents section"
                    )
                owned = markdown.matching_headings(text, README_SECTION, 2)[0]
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
                rules = parse_codeowners(path.read_text(encoding="utf-8"), set(entries))
                for governed, expected in entries.items():
                    if rules.get(governed) != expected:
                        errors.append(
                            f"CODEOWNERS has missing or different owners for {governed}"
                        )
        errors.extend(validate_no_legacy(root))
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(str(error))
    return errors


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--repo", required=True, type=Path, help="target repository root"
    )
    result.add_argument(
        "--project-name", help="human project name; defaults to the directory name"
    )
    result.add_argument("--description", help="one factual project sentence")
    result.add_argument(
        "--readme", default="README.md", help="repository-relative primary README"
    )
    result.add_argument(
        "--before-heading",
        action="append",
        default=[],
        help="README heading that governance must precede",
    )
    result.add_argument(
        "--locale",
        action="append",
        default=[],
        help="BCP 47 locale; repeatable; English is always root",
    )
    result.add_argument(
        "--human-translation", action="append", default=[], metavar="LOCALE=ABS_PATH"
    )
    result.add_argument(
        "--agent-translation", action="append", default=[], metavar="LOCALE=ABS_PATH"
    )
    result.add_argument(
        "--codeowner",
        action="append",
        default=[],
        help="verified @user, @organization/team, or email",
    )
    result.add_argument(
        "--apply", action="store_true", help="apply a conflict-free preview"
    )
    result.add_argument(
        "--confirm-authorized",
        action="store_true",
        help="confirm permission to change governance",
    )
    result.add_argument(
        "--validate-only", action="store_true", help="validate without changing files"
    )
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        root = args.repo.resolve()
        args.project_name = clean_scalar(args.project_name or root.name, "project name")
        args.description = clean_scalar(
            args.description or f"Repository guidance for {args.project_name}.",
            "description",
        )
        args.before_heading = [
            clean_scalar(value, "README heading") for value in args.before_heading
        ]
        locales = normalize_locales(args.locale)
        readme = safe_relative(args.readme, "README")
        owners = normalize_owners(args.codeowner)
        headings = args.before_heading or ["License", "Star History"]
        if args.validate_only:
            errors = validate(root, locales, readme, headings, owners)
            print(
                json.dumps(
                    {"valid": not errors, "errors": errors},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0 if not errors else 1
        root, locales, operations = build_plan(args)
        conflicts = [
            operation for operation in operations if operation.action == "conflict"
        ]
        report: dict[str, object] = {
            "repository": str(root),
            "apply": args.apply,
            "operations": [operation.report(root) for operation in operations],
        }
        if conflicts:
            print(json.dumps(report, ensure_ascii=False, indent=2))
            print("Refusing to apply because conflicts exist.", file=sys.stderr)
            return 2
        if not args.apply:
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0
        if not args.confirm_authorized:
            print(json.dumps(report, ensure_ascii=False, indent=2))
            print(
                "--apply requires --confirm-authorized after explicit governance approval.",
                file=sys.stderr,
            )
            return 2
        errors = apply_transaction(
            operations, lambda: validate(root, locales, readme, headings, owners)
        )
        report.update(
            {"valid": not errors, "errors": errors, "rolled_back": bool(errors)}
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if not errors else 1
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
