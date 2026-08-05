"""Command-line parsing and rendering."""

from __future__ import annotations

import argparse
import collections
import json
import sys
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from .audit import audit_report
from .discovery import is_source_bearing
from .records import AuditReport, Finding


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report deterministic software-architecture risks in a source tree.")
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--tool-timeout", type=float, default=30, help="maximum seconds per configured syntax provider")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    return parser.parse_args(argv)


def should_fail(findings: Sequence[Finding]) -> bool:
    """Return whether the mandatory acceptance gate blocks the audit.

    Warnings and errors, including inventory and advisory evidence, always
    block acceptance. Notices remain visible review output.
    """

    return any(item.severity in {"error", "warning"} for item in findings)


def render_text(root: Path, files: Sequence[Path], findings: Sequence[Finding]) -> None:
    print(f"software-architecture audit: {len(files)} architecture-bearing files")
    print("scope: full repository (filesystem candidates, including untracked files)")
    print("gate: fail-on warning (errors also block; inventory and advisory evidence are enforced)")
    if not findings:
        print("no findings")
        return
    counts = collections.Counter(item.severity for item in findings)
    print("findings: " + ", ".join(f"{name}={counts.get(name, 0)}" for name in ("error", "warning", "notice")))
    for finding in findings:
        try:
            shown = finding.path.relative_to(root)
        except ValueError:
            shown = finding.path
        print(f"{finding.severity}: {finding.code}: {shown}: {finding.message} [{finding.evidence}]")


def render_json(root: Path, report: AuditReport) -> None:
    def shown_path(path: Path) -> str:
        try:
            return str(path.relative_to(root))
        except ValueError:
            return str(path)

    payload = {
        "root": str(root),
        "source_files": sum(is_source_bearing(path, root) for path in report.files),
        "audited_files": len(report.files),
        "audited_paths": [shown_path(path) for path in report.files],
        "scope": "full",
        "gate": "fail-on warning",
        "analyzers": [asdict(item) for item in report.analyzers],
        "findings": [{**asdict(item), "path": shown_path(item.path)} for item in report.findings],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    report = audit_report(root, tool_timeout=args.tool_timeout)
    if report.analyzers and args.output_format == "text":
        print("analyzers: " + ", ".join(f"{item.rule_id}={item.status}" for item in report.analyzers))
    if args.output_format == "json":
        render_json(root, report)
    else:
        render_text(root, report.files, report.findings)
    return 1 if should_fail(report.findings) else 0
