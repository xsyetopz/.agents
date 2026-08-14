"""Preview, apply, and validate standard repository governance files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

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
from governance_planning import (
    build_plan,
    plan_codeowners,
    plan_exact,
    plan_readme,
    plan_sections,
    plan_translation,
)
from governance_support import (
    AGENT_SECTION,
    ASSETS,
    HUMAN_SECTIONS,
    PR_SECTIONS,
    PROVIDER_FILES,
    README_SECTION,
    SKILL_ROOT,
    clean_scalar,
    codeowner_entries,
    link_from,
    locale_links,
    parse_codeowners,
    render,
    render_readme_section,
    template_section,
)
from governance_validation import validate
from legacy_artifacts import (
    LEGACY_MARKER,
    LEGACY_PATHS,
    LEGACY_TOKENS,
    plan_legacy,
    strip_legacy_blocks,
    validate_no_legacy,
)
from locales import normalize_locales
from section_validation import exact_sections
from translation_support import discover_locales, parse_translations, reviewed_content


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


__all__ = [
    "AGENT_SECTION",
    "ASSETS",
    "HUMAN_SECTIONS",
    "LEGACY_MARKER",
    "LEGACY_PATHS",
    "LEGACY_TOKENS",
    "PROVIDER_FILES",
    "PR_SECTIONS",
    "README_SECTION",
    "SKILL_ROOT",
    "Operation",
    "apply_transaction",
    "assert_unique_paths",
    "build_plan",
    "clean_scalar",
    "codeowner_entries",
    "discover_locales",
    "exact_sections",
    "file_conflict",
    "find_human_governance_heading",
    "is_human_governance_heading",
    "link_from",
    "locale_links",
    "main",
    "markdown",
    "normalize_locales",
    "normalize_owners",
    "parse_codeowners",
    "parse_rules",
    "parse_translations",
    "parser",
    "plan_codeowners",
    "plan_exact",
    "plan_legacy",
    "plan_readme",
    "plan_sections",
    "plan_translation",
    "render",
    "render_readme_section",
    "repo_path",
    "reviewed_content",
    "safe_relative",
    "strip_legacy_blocks",
    "template_section",
    "validate",
    "validate_no_legacy",
]
