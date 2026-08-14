"""Conservative detection of tests and benchmarks embedded in authored source.

The module remains the compatibility façade for historical helper imports;
implementation is split by source normalization, language rules, and finding
assembly.
"""

from . import inline_test_finder as _finder
from . import inline_test_rules as _rules_module
from . import inline_test_source as _source

# Keep historical helper names available to direct imports and diagnostics.
inline_test_findings = _finder.inline_test_findings
_rules = _rules_module._rules
_BENCHMARK_FILE_PATTERNS = _source._BENCHMARK_FILE_PATTERNS
_BLOCK_COMMENT_DELIMITERS = _source._BLOCK_COMMENT_DELIMITERS
_CAMEL_TEST_FILE_PATTERNS = _source._CAMEL_TEST_FILE_PATTERNS
_DASH_COMMENT_SUFFIXES = _source._DASH_COMMENT_SUFFIXES
_HASH_COMMENT_SUFFIXES = _source._HASH_COMMENT_SUFFIXES
_LOWER_TEST_FILE_PATTERNS = _source._LOWER_TEST_FILE_PATTERNS
_OCAML_COMMENT_SUFFIXES = _source._OCAML_COMMENT_SUFFIXES
_PERCENT_COMMENT_SUFFIXES = _source._PERCENT_COMMENT_SUFFIXES
_SEMICOLON_COMMENT_SUFFIXES = _source._SEMICOLON_COMMENT_SUFFIXES
_TEST_DIRECTORIES = _source._TEST_DIRECTORIES
_blank = _source._blank
_javascript_runner_configured = _source._javascript_runner_configured
_nested_block_end = _source._nested_block_end
_strip_source = _source._strip_source
is_test_source = _source.is_test_source

__all__ = ["inline_test_findings", "is_test_source"]
