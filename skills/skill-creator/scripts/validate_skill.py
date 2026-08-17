#!/usr/bin/env python3
"""Validate an Agent Skill and its optional package distribution contract.

This module owns the command-line entrypoint. Parsing and focused checks live
in their package-local modules and are imported only where they are used.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agents_yaml import check_agents_yaml
from check_skill_structure import check_skill_creator_references
from contract_checks import (
    check_assets_contract,
    check_file_size,
    check_frontmatter_spec,
    check_progressive_disclosure,
    check_required_evals,
    check_required_files,
    check_required_headings,
    load_config,
)
from frontmatter import parse_frontmatter
from reference_checks import (
    check_broken_references,
    check_duplicate_entrypoints,
    check_duplicate_headers,
    check_global_path_references,
    check_markdown_links,
    check_symlink_containment,
    warn_missing_license,
)


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    root = root.resolve()
    if not root.is_dir():
        return [f"Skill root is not a directory: {root}"], warnings
    try:
        config = load_config(root)
    except (TypeError, ValueError) as exc:
        return [str(exc)], warnings
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        return [f"Missing required SKILL.md at {skill_file}"], warnings

    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"Unable to read SKILL.md: {exc}"], warnings
    try:
        frontmatter, _body = parse_frontmatter(text)
    except (TypeError, ValueError) as exc:
        return [str(exc)], warnings

    # Agent Skills specification and package-local contract checks.
    check_frontmatter_spec(frontmatter, root, errors)
    check_file_size(root, errors, warnings)
    check_progressive_disclosure(root, errors)
    check_agents_yaml(root, errors)
    check_required_headings(text, config, errors)
    check_required_files(root, config, errors)
    contract = check_assets_contract(root, config, text, errors)
    check_required_evals(root, config, errors, contract)

    # Reference and portability checks.
    check_broken_references(text, root, errors)
    check_markdown_links(root, errors, warnings)
    check_duplicate_headers(root, errors)
    check_duplicate_entrypoints(root, errors)
    check_symlink_containment(root, errors)
    check_global_path_references(root, errors)
    check_skill_creator_references(root, errors)
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
