"""Public inline-test detection API."""

from .inline_test_finder import inline_test_findings
from .inline_test_source import is_test_source

__all__ = ["inline_test_findings", "is_test_source"]
