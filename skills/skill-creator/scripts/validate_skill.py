#!/usr/bin/env python3
"""Validate an Agent Skill and its optional package distribution contract.

This file remains the stable CLI and import facade.  Parsing, contract, path,
and agents metadata checks live in small sibling modules so the copied package
keeps direct ``python3 scripts/validate_skill.py`` and ``from validate_skill``
entrypoints without a monolithic implementation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agents_yaml import _check_yaml_top_level_syntax, check_agents_yaml
from contract_checks import (
    CODEX_CASE_KEYS,
    COMMON_CONTRACT_FILES,
    COMMON_CONTRACT_HEADINGS,
    CONTRACT_KEYS,
    EVAL_KEYS,
    NAME_RE,
    PACKAGE_CHECK_COMMAND,
    SKILL_MD_LINE_ERROR,
    SKILL_MD_LINE_WARN,
    STATIC_EVAL_KEYS,
    UNAVAILABLE_MARKER_RE,
    _config_entries,
    _non_empty_string,
    _read_json,
    _safe_contract_path,
    check_assets_contract,
    check_common_section_semantics,
    check_file_size,
    check_frontmatter_spec,
    check_progressive_disclosure,
    check_required_evals,
    check_required_files,
    check_required_headings,
    load_config,
)
from frontmatter import _parse_metadata_mapping, parse_frontmatter
from reference_checks import (
    CHANGELOG_VERSION_RE,
    FENCE_RE,
    GLOBAL_PATH_RE,
    HEADING_RE,
    MARKDOWN_LINK_RE,
    REL_REF_RE,
    _check_local_reference,
    _clean_link_target,
    _is_official_snapshot,
    _iter_text_files,
    check_broken_references,
    check_duplicate_entrypoints,
    check_duplicate_headers,
    check_global_path_references,
    check_markdown_links,
    check_symlink_containment,
    strip_fenced_blocks,
    warn_missing_license,
)
from yaml_scalars import (
    YAML_BASE_PREFIX_RE,
    YAML_BINARY_INT_RE,
    YAML_DECIMAL_CANDIDATE_RE,
    YAML_DECIMAL_INT_RE,
    YAML_FLOAT_RE,
    YAML_HEX_INT_RE,
    YAML_NON_FINITE_FLOAT_RE,
    YAML_OCTAL_INT_RE,
    _consume_quoted,
    _leading_whitespace,
    _MetadataMap,
    _next_content_line,
    _parse_quoted_scalar,
    _parse_scalar,
    _reject_tab_indentation,
    _reject_yaml_control_characters,
    _set_metadata_entry,
    _split_flow_items,
    _split_mapping_entry,
    _starts_quote,
    _strip_inline_comment,
    _validate_plain_scalar,
)

# Deliberate re-exports preserve the original module's direct imports while the
# implementations live in package-local modules.
__all__ = [
    "CHANGELOG_VERSION_RE",
    "CODEX_CASE_KEYS",
    "COMMON_CONTRACT_FILES",
    "COMMON_CONTRACT_HEADINGS",
    "CONTRACT_KEYS",
    "EVAL_KEYS",
    "FENCE_RE",
    "GLOBAL_PATH_RE",
    "HEADING_RE",
    "MARKDOWN_LINK_RE",
    "NAME_RE",
    "PACKAGE_CHECK_COMMAND",
    "REL_REF_RE",
    "SKILL_MD_LINE_ERROR",
    "SKILL_MD_LINE_WARN",
    "STATIC_EVAL_KEYS",
    "UNAVAILABLE_MARKER_RE",
    "YAML_BASE_PREFIX_RE",
    "YAML_BINARY_INT_RE",
    "YAML_DECIMAL_CANDIDATE_RE",
    "YAML_DECIMAL_INT_RE",
    "YAML_FLOAT_RE",
    "YAML_HEX_INT_RE",
    "YAML_NON_FINITE_FLOAT_RE",
    "YAML_OCTAL_INT_RE",
    "_MetadataMap",
    "_check_local_reference",
    "_check_yaml_top_level_syntax",
    "_clean_link_target",
    "_config_entries",
    "_consume_quoted",
    "_is_official_snapshot",
    "_iter_text_files",
    "_leading_whitespace",
    "_next_content_line",
    "_non_empty_string",
    "_parse_metadata_mapping",
    "_parse_quoted_scalar",
    "_parse_scalar",
    "_read_json",
    "_reject_tab_indentation",
    "_reject_yaml_control_characters",
    "_safe_contract_path",
    "_set_metadata_entry",
    "_split_flow_items",
    "_split_mapping_entry",
    "_starts_quote",
    "_strip_inline_comment",
    "_validate_plain_scalar",
    "check_agents_yaml",
    "check_assets_contract",
    "check_broken_references",
    "check_common_section_semantics",
    "check_duplicate_entrypoints",
    "check_duplicate_headers",
    "check_file_size",
    "check_frontmatter_spec",
    "check_global_path_references",
    "check_markdown_links",
    "check_progressive_disclosure",
    "check_required_evals",
    "check_required_files",
    "check_required_headings",
    "check_symlink_containment",
    "load_config",
    "parse_frontmatter",
    "strip_fenced_blocks",
    "validate",
    "warn_missing_license",
]


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
