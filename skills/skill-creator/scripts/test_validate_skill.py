"""Stable unittest entrypoint for the split skill-validator test suite."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import validate_skill_baseline_tests
import validate_skill_cli_tests
import validate_skill_contract_tests
import validate_skill_frontmatter_tests
import validate_skill_reference_tests
import validate_skill_yaml_tests

_TEST_MODULES = (
    validate_skill_frontmatter_tests,
    validate_skill_contract_tests,
    validate_skill_reference_tests,
    validate_skill_yaml_tests,
    validate_skill_cli_tests,
    validate_skill_baseline_tests,
)


def load_tests(
    loader: unittest.TestLoader,
    _tests: unittest.TestSuite,
    _pattern: str | None,
) -> unittest.TestSuite:
    """Aggregate split modules for direct and ``-m unittest`` invocation."""
    suite = unittest.TestSuite()
    for module in _TEST_MODULES:
        suite.addTests(loader.loadTestsFromModule(module))
    return suite


if __name__ == "__main__":
    unittest.main()
