"""Shared validator imports and scalar fixtures for split test modules."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from agents_yaml import check_agents_yaml
from check_skill_structure import check_skill_creator_references
from contract_checks import (
    check_frontmatter_spec,
    check_required_files,
    check_required_headings,
)
from frontmatter import parse_frontmatter
from reference_checks import (
    check_broken_references,
    check_duplicate_entrypoints,
    check_duplicate_headers,
    check_global_path_references,
    check_markdown_links,
)
from validate_skill import validate
from yaml_scalars import _parse_scalar, _split_flow_items, _split_mapping_entry

NON_FINITE_FLOAT_SPELLINGS = tuple(
    f"{sign}.{kind}"
    for sign in ("", "+", "-")
    for kind in ("inf", "Inf", "INF", "nan", "NaN", "NAN")
)
NUMERIC_SCALARS = (
    ("0", 0),
    ("00", 0),
    ("01", 1),
    ("012", 12),
    ("+012", 12),
    ("-012", -12),
    ("0_1", 1),
    ("0b10", 2),
    ("+0B1_0", 2),
    ("-0b1_0", -2),
    ("0o10", 8),
    ("+0O1_0", 8),
    ("-0o1_0", -8),
    ("0x10", 16),
    ("+0Xf_F", 255),
    ("-0xF_f", -255),
    ("1.5", 1.5),
    ("1.", 1.0),
    (".5", 0.5),
    (".5e2", 50.0),
    ("1e2", 100.0),
    ("-1_000.5", -1000.5),
    ("+1.5e-2", 0.015),
)

__all__ = [
    "NON_FINITE_FLOAT_SPELLINGS",
    "NUMERIC_SCALARS",
    "_parse_scalar",
    "_split_flow_items",
    "_split_mapping_entry",
    "check_agents_yaml",
    "check_broken_references",
    "check_duplicate_entrypoints",
    "check_duplicate_headers",
    "check_frontmatter_spec",
    "check_global_path_references",
    "check_markdown_links",
    "check_required_files",
    "check_required_headings",
    "check_skill_creator_references",
    "parse_frontmatter",
    "validate",
]
