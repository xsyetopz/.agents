"""Finding assembly for inline-test detection."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from .inline_test_rules import _rules
from .inline_test_source import (
    _javascript_runner_configured,
    _strip_source,
    is_test_source,
)
from .records import Finding
from .rules import SOURCE_EXTENSIONS


def inline_test_findings(
    path: Path,
    root: Path,
    *,
    inventory: Sequence[Path] | None = None,
) -> list[Finding]:
    """Find structurally distinctive inline tests in a non-test source file."""
    if is_test_source(path, root):
        return []
    suffix = path.suffix.lower()
    if suffix and suffix not in SOURCE_EXTENSIONS:
        return []
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [
            Finding(
                "error",
                "inline-test-scan-failed",
                path,
                f"inline test/benchmark scan could not read authored source: {exc}",
                "tooling",
            )
        ]
    if len(source) > 2_000_000 or any(
        len(line) > 100_000 for line in source.splitlines()
    ):
        return [
            Finding(
                "error",
                "inline-test-scan-limit",
                path,
                "authored source exceeds the fail-closed inline scan size limit; split or regenerate it before acceptance",
                "tooling",
            )
        ]
    comments_only = _strip_source(source, suffix, strings=False)
    clean = _strip_source(source, suffix)
    findings: list[Finding] = []
    seen: set[tuple[str, int]] = set()
    visible_inventory = None if inventory is None else tuple(sorted(inventory, key=str))
    for code, pattern, evidence in _rules(
        suffix,
        clean,
        comments_only,
        js_runner_configured=_javascript_runner_configured(root, visible_inventory),
    ):
        for match in pattern.finditer(clean):
            line = clean.count("\n", 0, match.start()) + 1
            key = code, line
            if key in seen:
                continue
            seen.add(key)
            kind = "benchmark" if code == "inline-benchmark" else "test"
            findings.append(
                Finding(
                    "error",
                    code,
                    path,
                    f"inline {kind} syntax `{evidence}` at line {line}; move it to a conventional {kind} file or directory",
                    "syntax",
                )
            )
    return findings
