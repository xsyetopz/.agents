#!/usr/bin/env python3
"""Fail-closed scanning of lint and check suppression constructs."""

from __future__ import annotations

import re
from pathlib import Path

from .records import Finding
from .suppression_rules import (
    _CHECK_BYPASS,
    _CHECK_EXIT_ZERO,
    _CI_BYPASS,
    _CI_CONTEXT,
    _CI_DISABLED,
    _CODE_SUPPRESSIONS,
    _COMMENT_DIRECTIVES,
    _DISABLED_RULE,
    _DOWNGRADED_RULE,
    _PACKAGE_BYPASS,
    _RUST_ALLOW,
    DOCUMENTATION_SUFFIXES,
    _code_without_strings_or_comments,
    _is_comment_or_blank,
    comment_fragment,
    config_suppression,
    finding,
    is_ignore_file,
    is_linter_config,
    is_relevant_gitignore_pattern,
    is_workflow,
    json_brace_delta,
    multiline_disabled_rule,
)


def suppression_findings(path: Path, root: Path | None = None) -> list[Finding]:
    """Find suppression and check-bypass constructs in one candidate file."""

    # Broken or external symlink targets are not authored candidate contents;
    # discovery keeps the link visible, while suppression scanning remains
    # content-based and avoids manufacturing a finding for missing targets.
    if path.is_symlink():
        return []
    suffix = path.suffix.lower()
    if suffix in DOCUMENTATION_SUFFIXES:
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return [
            finding(
                path, 1, f"suppression scan failed: {exc}", "suppression-scan-failed"
            )
        ]

    findings: list[Finding] = []
    workflow = is_workflow(path)
    linter_config = is_linter_config(path)
    package_manifest = path.name.lower() == "package.json"
    package_script_depth: int | None = None
    section = ""
    if path.name.lower() == ".gitignore":
        for line_number, line in enumerate(lines, 1):
            if is_relevant_gitignore_pattern(line):
                findings.append(
                    finding(
                        path,
                        line_number,
                        f"source/test/check/lint path is ignored: {line.strip()}",
                        "gitignore-source-pattern-added",
                    )
                )
    elif is_ignore_file(path):
        for line_number, line in enumerate(lines, 1):
            if not _is_comment_or_blank(line):
                findings.append(
                    finding(
                        path,
                        line_number,
                        f"lint/check ignore pattern is active: {line.strip()}",
                        "ignore-pattern-added",
                    )
                )
    if "baseline" in path.name.lower():
        for line_number, line in enumerate(lines, 1):
            if not _is_comment_or_blank(line):
                findings.append(
                    finding(
                        path,
                        line_number,
                        f"baseline suppression configuration is active: {line.strip()}",
                        "baseline-suppression",
                    )
                )
                break
    for index, line in enumerate(lines):
        line_number = index + 1
        package_script_line = package_script_depth is not None
        if package_manifest:
            scripts_match = re.search(r"[\"']scripts[\"']\s*:", line, re.IGNORECASE)
            if scripts_match:
                package_script_line = True
                package_script_depth = max(
                    0, json_brace_delta(line[scripts_match.end() :])
                )
            elif package_script_depth is not None:
                package_script_depth += json_brace_delta(line)
                if package_script_depth <= 0:
                    package_script_depth = None
        section_match = re.match(r"^\s*\[([^\]]+)\]", line)
        if section_match:
            section = section_match.group(1).lower()
        comment = comment_fragment(line, suffix)
        if comment is not None and any(
            token in comment.lower()
            for token in (
                "disable",
                "ignore",
                "expect-error",
                "nolint",
                "noqa",
                "nowarn",
            )
        ):
            for label, pattern in _COMMENT_DIRECTIVES:
                if pattern.search(comment):
                    findings.append(
                        finding(
                            path,
                            line_number,
                            f"{label} suppression directive: {comment.strip()}",
                        )
                    )
                    break
        if suffix == ".rs" and "allow" in line and _RUST_ALLOW.search(line):
            findings.append(
                finding(path, line_number, f"Rust lint allowance: {line.strip()}")
            )
        if (
            "pragma" in line.lower()
            or "suppress" in line.lower()
            or "nowarn" in line.lower()
        ):
            for label, pattern in _CODE_SUPPRESSIONS:
                if pattern.search(line):
                    findings.append(
                        finding(
                            path, line_number, f"{label} suppression: {line.strip()}"
                        )
                    )
                    break
        code = _code_without_strings_or_comments(line, suffix)
        if "||" in code and _CHECK_BYPASS.search(code):
            findings.append(
                finding(
                    path,
                    line_number,
                    f"lint/check/test command is forced successful with `|| true` or `|| :`: {line.strip()}",
                    "check-bypass",
                )
            )
        if "exit-zero" in code and _CHECK_EXIT_ZERO.search(code):
            findings.append(
                finding(
                    path,
                    line_number,
                    f"lint/check provider is forced successful with `--exit-zero`: {line.strip()}",
                    "check-bypass",
                )
            )
        if package_manifest and package_script_line and _PACKAGE_BYPASS.search(line):
            findings.append(
                finding(
                    path,
                    line_number,
                    f"package lint/check/test script is forced successful: {line.strip()}",
                    "check-bypass",
                )
            )
        if workflow and _CI_BYPASS.search(line):
            context = "\n".join(lines[max(0, index - 8) : index + 9])
            if _CI_CONTEXT.search(context):
                findings.append(
                    finding(
                        path,
                        line_number,
                        f"CI lint/check/test step allows failure: {line.strip()}",
                        "check-bypass",
                    )
                )
        if workflow and _CI_DISABLED.search(line):
            context = "\n".join(lines[max(0, index - 8) : index + 9])
            if _CI_CONTEXT.search(context):
                findings.append(
                    finding(
                        path,
                        line_number,
                        f"CI lint/check/test step is disabled: {line.strip()}",
                        "check-bypass",
                    )
                )
        # Linter rule names and severities are commonly quoted in JSON; use
        # the raw configuration line rather than the string-masked command
        # view above.
        lowered_line = line.lower()
        if (
            linter_config
            and not path.name.lower().startswith("tsconfig")
            and any(token in lowered_line for token in ("off", "false", ": 0", ":0"))
            and _DISABLED_RULE.search(line)
        ):
            findings.append(
                finding(
                    path,
                    line_number,
                    f"linter rule severity is disabled: {line.strip()}",
                    "lint-severity-disabled",
                )
            )
        if (
            linter_config
            and not path.name.lower().startswith("tsconfig")
            and "warn" in lowered_line
            and _DOWNGRADED_RULE.search(line)
        ):
            findings.append(
                finding(
                    path,
                    line_number,
                    f"linter rule severity is downgraded: {line.strip()}",
                    "lint-severity-downgraded",
                )
            )
        if linter_config:
            config_message = config_suppression(path, line, section)
            if config_message is not None:
                findings.append(
                    finding(
                        path,
                        line_number,
                        f"{config_message}: {line.strip()}",
                        "lint-config-suppression",
                    )
                )
            if multiline_disabled_rule(lines, index):
                findings.append(
                    finding(
                        path,
                        line_number,
                        f"linter rule severity is disabled on a continuation line: {line.strip()}",
                        "lint-severity-disabled",
                    )
                )
    return findings
