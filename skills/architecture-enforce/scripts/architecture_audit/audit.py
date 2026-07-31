"""Audit orchestration."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path, PurePosixPath

from architecture_tools import run_ast_grep

from .discovery import artifact_class, count_lines, iter_audited_files
from .exceptions import (
    apply_exceptions,
    load_exceptions,
    load_syntax_rules,
    load_test_source_roots,
)
from .findings import directory_findings, filename_findings, package_manager_findings
from .inline_tests import inline_test_findings
from .records import AnalyzerStatus, ArtifactException, AuditReport, Finding
from .rules import SEVERITY_RANK, SOURCE_EXTENSIONS


def audit(
    root: Path, *, soft: int = 450, strong: int = 650, hard: int = 800,
    flat_limit: int = 12, include_generated: bool = False,
    excludes: Sequence[str] = (), exceptions_path: Path | None = None,
) -> tuple[list[Path], list[Finding]]:
    report = audit_report(
        root, soft=soft, strong=strong, hard=hard, flat_limit=flat_limit,
        include_generated=include_generated, excludes=excludes,
        exceptions_path=exceptions_path,
    )
    return list(report.files), list(report.findings)


def audit_report(
    root: Path, *, soft: int = 450, strong: int = 650, hard: int = 800,
    flat_limit: int = 12, include_generated: bool = False,
    excludes: Sequence[str] = (), exceptions_path: Path | None = None,
    tool_timeout: float = 30,
) -> AuditReport:
    files = sorted(iter_audited_files(root, excludes))
    exceptions, artifact_exceptions, exception_findings = load_exceptions(root, exceptions_path)
    configured_test_roots, test_root_findings = load_test_source_roots(root, exceptions_path)
    external_exception_contract = False
    if exceptions_path is not None:
        try:
            exceptions_path.resolve().relative_to(root.resolve())
        except ValueError:
            exception_findings.append(Finding("error", "invalid-exception-file", exceptions_path, "exception contract must be inside the audited repository"))
            exceptions, artifact_exceptions, configured_test_roots = [], [], []
            external_exception_contract = True
    syntax_rules, syntax_findings = ([], []) if external_exception_contract else load_syntax_rules(root, exceptions_path)
    authored: list[Path] = []
    findings: list[Finding] = [*exception_findings, *test_root_findings, *syntax_findings]
    analyzers: list[AnalyzerStatus] = []
    artifact_targets: list[tuple[Path, ArtifactException]] = []
    matched_artifact_targets: set[Path] = set()
    matched_test_roots: set[Path] = set()
    for exception in artifact_exceptions:
        target = root / PurePosixPath(exception.path)
        if not target.exists():
            findings.append(Finding("error", "stale-artifact-exemption", target, f"{exception.artifact_class} artifact exemption target does not exist"))
            continue
        artifact_targets.append((target, exception))
    for index, (left, _) in enumerate(artifact_targets):
        for right, _ in artifact_targets[index + 1:]:
            if left == right or left in right.parents or right in left.parents:
                findings.append(Finding("error", "overlapping-artifact-exemption", root, f"artifact exemption paths overlap: {left.relative_to(root)} and {right.relative_to(root)}"))
    for pattern in excludes:
        findings.append(Finding("warning", "excluded-scope", root, f"excluded glob '{pattern}' makes this a scoped audit, not full-repository acceptance proof"))
    for configured in configured_test_roots:
        target = root / PurePosixPath(configured.path)
        if not target.exists():
            findings.append(Finding("error", "stale-test-source-root", target, f"configured test source root does not exist: {configured.path}"))
        else:
            findings.append(Finding("notice", "configured-test-source-root", target, f"custom test source root excepted; reason={configured.reason}; owner={configured.owner}; control={configured.control}; review={configured.review}"))
    for path in files:
        for configured in configured_test_roots:
            target = root / PurePosixPath(configured.path)
            if path == target or target in path.parents:
                matched_test_roots.add(target)
        recorded = next((item for item in artifact_targets if path == item[0] or item[0] in path.parents), None)
        if recorded and not include_generated:
            target, exception = recorded
            matched_artifact_targets.add(target)
            findings.append(Finding("notice", "exempt-artifact", path, f"{exception.artifact_class} artifact excepted; reason={exception.reason}; owner={exception.owner}; control={exception.control}; review={exception.review}"))
            continue
        kind = artifact_class(path, root)
        if kind and not (include_generated and kind in {"generated", "vendor", "migration", "snapshot"}):
            findings.append(Finding("notice", "exempt-artifact", path, f"{kind} artifact is visibly exempt from authored structural checks"))
            continue
        authored.append(path)
        findings.extend(inline_test_findings(path, root, configured_test_roots))
        if path.suffix.lower() in SOURCE_EXTENSIONS:
            try:
                lines = count_lines(path)
            except OSError as exc:
                findings.append(Finding("warning", "unreadable-file", path, f"could not read file: {exc}", "inventory"))
            else:
                if lines > hard:
                    findings.append(Finding("warning", "hard-lines", path, f"{lines} lines exceeds configured upper review threshold {hard}", "inventory"))
                elif lines > strong:
                    findings.append(Finding("warning", "strong-lines", path, f"{lines} lines requires an extraction plan above {strong}", "inventory"))
                elif lines > soft:
                    findings.append(Finding("notice", "soft-lines", path, f"{lines} lines requires architectural review above {soft}", "inventory"))
        findings.extend(filename_findings(path, root))
    for target, exception in artifact_targets:
        if target not in matched_artifact_targets and not include_generated:
            findings.append(Finding("error", "stale-artifact-exemption", target, f"{exception.artifact_class} artifact exemption contains no audited files"))
    for configured in configured_test_roots:
        target = root / PurePosixPath(configured.path)
        if target.exists() and target not in matched_test_roots:
            findings.append(Finding("error", "stale-test-source-root", target, f"configured test source root contains no audited files: {configured.path}"))
    findings.extend(directory_findings(root, authored, flat_limit))
    findings.extend(package_manager_findings(root, excludes))
    for rule in syntax_rules:
        if rule.tool != "ast-grep":
            analyzers.append(AnalyzerStatus(rule.rule_id, rule.tool, "blocked", rule.mode, "provider is not implemented by this skill"))
            severity = "error" if rule.mode == "required" else "warning"
            evidence = "tooling" if rule.mode == "required" else "tooling-advisory"
            findings.append(Finding(severity, "syntax-tool-blocked", root, f"{rule.rule_id}: provider '{rule.tool}' is unavailable in this skill", evidence))
            continue
        result = run_ast_grep(
            root, rule_id=rule.rule_id, language=rule.language, pattern=rule.pattern,
            severity=rule.severity, message=rule.message, paths=rule.paths,
            timeout_s=tool_timeout,
        )
        analyzers.append(AnalyzerStatus(rule.rule_id, rule.tool, result.status, rule.mode, "; ".join(result.diagnostics), result.version, result.argv))
        if result.status == "violations":
            evidence = "syntax" if rule.mode == "required" else "syntax-advisory"
            findings.extend(Finding(item.severity, f"syntax:{item.rule_id}", item.path, f"{item.message} ({item.start_line}:{item.start_column}-{item.end_line}:{item.end_column})", evidence) for item in result.findings)
        elif result.status != "passed":
            severity = "error" if rule.mode == "required" else "warning"
            detail = "; ".join(result.diagnostics) or result.status
            evidence = "tooling" if rule.mode == "required" else "tooling-advisory"
            findings.append(Finding(severity, f"syntax-{result.status}", root, f"{rule.rule_id}: {detail}", evidence))
    findings = apply_exceptions(root, findings, exceptions)
    findings.sort(key=lambda item: (SEVERITY_RANK[item.severity], str(item.path), item.code))
    return AuditReport(tuple(files), tuple(findings), tuple(analyzers))
