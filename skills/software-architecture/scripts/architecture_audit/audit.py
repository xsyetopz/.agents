"""Audit orchestration."""

from __future__ import annotations

from pathlib import Path

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
from .findings import directory_findings, filename_findings, package_manager_findings
from .git_suppressions import git_suppression_findings
from .inline_tests import inline_test_findings
from .records import AuditReport, Finding
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
    root: Path,
    *,
    soft: int = SOFT_LINE_THRESHOLD,
    strong: int = STRONG_LINE_THRESHOLD,
    hard: int = HARD_LINE_THRESHOLD,
    flat_limit: int = FLAT_CLUSTER_LIMIT,
    include_generated: bool = False,
) -> tuple[list[Path], list[Finding]]:
    report = audit_report(
        root,
        soft=soft,
        strong=strong,
        hard=hard,
        flat_limit=flat_limit,
        include_generated=include_generated,
    )
    return list(report.files), list(report.findings)


def audit_report(
    root: Path,
    *,
    soft: int = SOFT_LINE_THRESHOLD,
    strong: int = STRONG_LINE_THRESHOLD,
    hard: int = HARD_LINE_THRESHOLD,
    flat_limit: int = FLAT_CLUSTER_LIMIT,
    include_generated: bool = False,
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
            visible_inventory = tuple(
                sorted(_git_inventory(repository, audit_root), key=str)
            )
            files = sorted(
                (
                    path
                    for path in visible_inventory
                    if _is_architecture_candidate(path)
                ),
                key=str,
            )
    except GitInventoryError as exc:
        files = []
        visible_inventory = ()
        inventory_failure = Finding(
            "error", "git-inventory-failed", root, str(exc), "tooling"
        )
    authored: list[Path] = []
    findings = [inventory_failure] if inventory_failure is not None else []
    findings.extend(git_suppression_findings(root))
    if policy_overridden:
        findings.append(
            Finding(
                "error",
                "unsupported-policy-override",
                root,
                "architecture thresholds are fixed policy and cannot be overridden for acceptance",
            )
        )
    for path in files:
        kind = artifact_class(path, root)
        if is_output_directory_source(path, root):
            findings.append(
                Finding(
                    "error",
                    "output-directory-source",
                    path,
                    "authored source is hidden beneath an output directory; move it to a durable source owner",
                    "policy",
                )
            )
            authored.append(path)
            findings.extend(filename_findings(path, root))
            continue
        if kind:
            # Built-in artifact classifications remain visible exemptions, but
            # generated/configured contents cannot hide lint suppressions.
            findings.extend(suppression_findings(path, root))
            if kind == "framework" or not (
                include_generated
                and kind in {"generated", "vendor", "migration", "snapshot"}
            ):
                findings.append(
                    Finding(
                        "notice",
                        "exempt-artifact",
                        path,
                        f"{kind} artifact is visibly exempt from authored structural checks",
                    )
                )
                continue
        findings.extend(suppression_findings(path, root))
        if not is_source_bearing(path, root):
            # Metadata and documentation remain in ``report.files`` for
            # inventory visibility but do not form authored structural units.
            continue
        authored.append(path)
        findings.extend(inline_test_findings(path, root, inventory=visible_inventory))
        if path.suffix.lower() in SOURCE_EXTENSIONS:
            try:
                lines = count_lines(path)
            except OSError as exc:
                findings.append(
                    Finding(
                        "warning",
                        "unreadable-file",
                        path,
                        f"could not read file: {exc}",
                        "inventory",
                    )
                )
            else:
                if lines > hard:
                    findings.append(
                        Finding(
                            "warning",
                            "hard-lines",
                            path,
                            f"{lines} lines exceeds policy upper review threshold {hard}",
                            "inventory",
                        )
                    )
                elif lines > strong:
                    findings.append(
                        Finding(
                            "warning",
                            "strong-lines",
                            path,
                            f"{lines} lines requires an extraction plan above policy threshold {strong}",
                            "inventory",
                        )
                    )
                elif lines > soft:
                    findings.append(
                        Finding(
                            "notice",
                            "soft-lines",
                            path,
                            f"{lines} lines requires architectural review above policy threshold {soft}",
                            "inventory",
                        )
                    )
        findings.extend(filename_findings(path, root))
    findings.extend(
        directory_findings(root, authored, flat_limit, inventory=visible_inventory)
    )
    if inventory_failure is None:
        findings.extend(package_manager_findings(root, inventory=visible_inventory))
    findings.sort(
        key=lambda item: (SEVERITY_RANK[item.severity], str(item.path), item.code)
    )
    return AuditReport(tuple(files), tuple(findings))
