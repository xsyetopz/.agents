"""Audit orchestration."""

from __future__ import annotations

from pathlib import Path, PurePosixPath

from providers import run_ast_grep

from .discovery import (
    GitInventoryError,
    _git_inventory,
    _is_architecture_candidate,
    artifact_class,
    count_lines,
    git_repository_root,
    is_output_directory_source,
    is_source_bearing,
    iter_audited_files,
)
from .exceptions import (
    load_exceptions,
    load_syntax_rules,
    load_test_source_roots,
)
from .findings import directory_findings, filename_findings, package_manager_findings
from .git_suppressions import git_suppression_findings
from .inline_tests import inline_test_findings
from .records import AnalyzerStatus, ArtifactException, AuditReport, Finding
from .rules import (
    FLAT_CLUSTER_LIMIT,
    HARD_LINE_THRESHOLD,
    SEVERITY_RANK,
    SOFT_LINE_THRESHOLD,
    SOURCE_EXTENSIONS,
    STRONG_LINE_THRESHOLD,
)
from .suppressions import suppression_findings


def audit(
    root: Path, *, soft: int = SOFT_LINE_THRESHOLD, strong: int = STRONG_LINE_THRESHOLD, hard: int = HARD_LINE_THRESHOLD,
    flat_limit: int = FLAT_CLUSTER_LIMIT, include_generated: bool = False,
    exceptions_path: Path | None = None,
) -> tuple[list[Path], list[Finding]]:
    report = audit_report(
        root, soft=soft, strong=strong, hard=hard, flat_limit=flat_limit,
        include_generated=include_generated, exceptions_path=exceptions_path,
    )
    return list(report.files), list(report.findings)


def audit_report(
    root: Path, *, soft: int = SOFT_LINE_THRESHOLD, strong: int = STRONG_LINE_THRESHOLD, hard: int = HARD_LINE_THRESHOLD,
    flat_limit: int = FLAT_CLUSTER_LIMIT, include_generated: bool = False,
    exceptions_path: Path | None = None,
    tool_timeout: float = 30,
) -> AuditReport:
    # Acceptance audits cover Git's complete tracked/non-ignored worktree
    # inventory. Scope is fixed by Git and cannot be reduced by callers.
    policy_overridden = (
        soft != SOFT_LINE_THRESHOLD
        or strong != STRONG_LINE_THRESHOLD
        or hard != HARD_LINE_THRESHOLD
        or flat_limit != FLAT_CLUSTER_LIMIT
    )
    inventory_failure: Finding | None = None
    visible_inventory: tuple[Path, ...] | None = None
    try:
        audit_root = root.absolute()
        repository = git_repository_root(audit_root)
        if repository is None:
            files = sorted(iter_audited_files(root))
        else:
            visible_inventory = tuple(sorted(_git_inventory(repository, audit_root), key=str))
            files = sorted((path for path in visible_inventory if _is_architecture_candidate(path)), key=str)
    except GitInventoryError as exc:
        files = []
        visible_inventory = ()
        inventory_failure = Finding("error", "git-inventory-failed", root, str(exc), "tooling")
    exceptions, artifact_exceptions, exception_findings = load_exceptions(root, exceptions_path, inventory=visible_inventory)
    configured_test_roots, test_root_findings = load_test_source_roots(root, exceptions_path, inventory=visible_inventory)
    external_exception_contract = False
    if exceptions_path is not None:
        try:
            exceptions_path.resolve().relative_to(root.resolve())
        except ValueError:
            exception_findings.append(Finding("error", "invalid-exception-file", exceptions_path, "exception contract must be inside the audited repository"))
            exceptions, artifact_exceptions, configured_test_roots = [], [], []
            external_exception_contract = True
    syntax_rules, syntax_findings = ([], []) if external_exception_contract else load_syntax_rules(root, exceptions_path, inventory=visible_inventory)
    authored: list[Path] = []
    findings: list[Finding] = [
        *([inventory_failure] if inventory_failure is not None else []),
        *exception_findings,
        *test_root_findings,
        *syntax_findings,
    ]
    findings.extend(git_suppression_findings(root))
    if policy_overridden:
        findings.append(Finding("error", "unsupported-policy-override", root, "architecture thresholds are fixed policy and cannot be overridden for acceptance"))
    if exceptions_path is not None:
        findings.append(Finding("error", "unsupported-policy-file", exceptions_path, "acceptance audits cannot select an alternate exception or policy file"))
    if exceptions:
        findings.append(Finding("error", "unsupported-naming-exception", root, "naming and structural findings cannot be waived by exception entries"))
    if artifact_exceptions:
        findings.append(Finding("error", "unsupported-artifact-exemption", root, "acceptance audits use only deterministic generated/framework classification; configured artifact exemptions cannot waive findings"))
    if configured_test_roots:
        findings.append(Finding("error", "unsupported-test-source-root", root, "acceptance audits use built-in test-source conventions; configured test source roots cannot waive inline-test findings"))
    analyzers: list[AnalyzerStatus] = []
    artifact_targets: list[tuple[Path, ArtifactException]] = []
    matched_artifact_targets: set[Path] = set()
    visible_paths = None if visible_inventory is None else {path.absolute() for path in visible_inventory}
    for exception in artifact_exceptions:
        target = root / PurePosixPath(exception.path)
        if visible_paths is not None and target.absolute() not in visible_paths:
            continue
        if not target.exists():
            findings.append(Finding("error", "stale-artifact-exemption", target, f"{exception.artifact_class} artifact exemption target does not exist"))
            continue
        artifact_targets.append((target, exception))
    for index, (left, _) in enumerate(artifact_targets):
        for right, _ in artifact_targets[index + 1:]:
            if left == right or left in right.parents or right in left.parents:
                findings.append(Finding("error", "overlapping-artifact-exemption", root, f"artifact exemption paths overlap: {left.relative_to(root)} and {right.relative_to(root)}"))
    for configured in configured_test_roots:
        target = root / PurePosixPath(configured.path)
        if visible_paths is not None and target.absolute() not in visible_paths:
            continue
        if not target.exists():
            findings.append(Finding("error", "stale-test-source-root", target, f"configured test source root does not exist: {configured.path}"))
    for path in files:
        recorded = next((item for item in artifact_targets if path == item[0] or item[0] in path.parents), None)
        if recorded:
            matched_artifact_targets.add(recorded[0])
        kind = artifact_class(path, root)
        if is_output_directory_source(path, root):
            findings.append(Finding(
                "error",
                "output-directory-source",
                path,
                "authored source is hidden beneath an output directory; move it to a durable source owner",
                "policy",
            ))
            authored.append(path)
            findings.extend(filename_findings(path, root))
            continue
        if kind:
            # Built-in artifact classifications remain visible exemptions, but
            # generated/configured contents cannot hide lint suppressions.
            findings.extend(suppression_findings(path, root))
            if kind == "framework" or not (include_generated and kind in {"generated", "vendor", "migration", "snapshot"}):
                findings.append(Finding("notice", "exempt-artifact", path, f"{kind} artifact is visibly exempt from authored structural checks"))
                continue
        findings.extend(suppression_findings(path, root))
        if not is_source_bearing(path, root):
            # Metadata and documentation remain in ``report.files`` for
            # inventory visibility but do not form authored structural units.
            continue
        authored.append(path)
        # Configured test-source roots are intentionally not passed here: a
        # policy file cannot suppress the built-in inline-test gate.
        findings.extend(inline_test_findings(path, root, inventory=visible_inventory))
        if path.suffix.lower() in SOURCE_EXTENSIONS:
            try:
                lines = count_lines(path)
            except OSError as exc:
                findings.append(Finding("warning", "unreadable-file", path, f"could not read file: {exc}", "inventory"))
            else:
                if lines > hard:
                    findings.append(Finding("warning", "hard-lines", path, f"{lines} lines exceeds policy upper review threshold {hard}", "inventory"))
                elif lines > strong:
                    findings.append(Finding("warning", "strong-lines", path, f"{lines} lines requires an extraction plan above policy threshold {strong}", "inventory"))
                elif lines > soft:
                    findings.append(Finding("notice", "soft-lines", path, f"{lines} lines requires architectural review above policy threshold {soft}", "inventory"))
        findings.extend(filename_findings(path, root))
    for target, exception in artifact_targets:
        if target not in matched_artifact_targets and not include_generated:
            findings.append(Finding("error", "stale-artifact-exemption", target, f"{exception.artifact_class} artifact exemption contains no audited files"))
    findings.extend(directory_findings(root, authored, flat_limit, inventory=visible_inventory))
    if inventory_failure is None:
        findings.extend(package_manager_findings(root, inventory=visible_inventory))
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
    findings.sort(key=lambda item: (SEVERITY_RANK[item.severity], str(item.path), item.code))
    return AuditReport(tuple(files), tuple(findings), tuple(analyzers))
