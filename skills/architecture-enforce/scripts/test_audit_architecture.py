"""Compatibility entrypoint for architecture audit regression tests."""

from __future__ import annotations

import unittest

from test_audit_architecture_inline import AuditArchitectureInlineTests
from test_audit_architecture_naming import AuditArchitectureNamingTests

__all__ = ["AuditArchitectureInlineTests", "AuditArchitectureNamingTests"]


def __getattr__(name: str):
    # Keep legacy imports resolvable without exposing a duplicate TestCase to
    # unittest's module discovery when this façade is run directly.
    if name == "AuditArchitectureTests":
        return AuditArchitectureInlineTests
    raise AttributeError(name)


if __name__ == "__main__":
    unittest.main()
