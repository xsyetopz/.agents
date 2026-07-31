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
from .records import AuditReport, Finding
from .rules import FAIL_RANK, SEVERITY_RANK, SOURCE_EXTENSIONS


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report deterministic software-architecture risks in a source tree.")
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--soft", type=int, default=450, help="architectural review line threshold")
    parser.add_argument("--strong", type=int, default=650, help="extraction-plan line threshold")
    parser.add_argument("--hard", type=int, default=800, help="upper authored-source review threshold")
    parser.add_argument("--flat-limit", type=int, default=12, help="direct authored-file count before a flat-cluster warning")
    parser.add_argument("--include-generated", action="store_true", help="include generated/vendor/migration/snapshot and recorded artifact exemptions in structural checks")
    parser.add_argument("--exclude", action="append", default=[], metavar="GLOB", help="exclude a root-relative glob; repeatable (requires --allow-scoped-audit)")
    parser.add_argument("--allow-scoped-audit", action="store_true", help="explicitly acknowledge that --exclude prevents full-repository acceptance proof")
    parser.add_argument("--exceptions", type=Path, help="exception contract (default: ROOT/.architecture-enforcement.json when present)")
    parser.add_argument("--tool-timeout", type=float, default=30, help="maximum seconds per configured syntax provider")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    parser.add_argument("--fail-on", choices=("error", "warning", "notice", "never"), default="error", help="lowest severity that produces exit 1; use warning/notice for reviewed policy gates")
    parser.add_argument("--allow-advisory-audit", action="store_true", help="explicitly acknowledge that --fail-on never is inventory-only and cannot prove acceptance")
    return parser.parse_args(argv)


def should_fail(findings: Sequence[Finding], threshold: str) -> bool:
    if any(item.severity == "error" and item.evidence not in {"inventory", "syntax-advisory", "tooling-advisory"} for item in findings):
        return True
    if threshold == "never":
        return False
    maximum_rank = FAIL_RANK[threshold]
    return any(item.evidence not in {"inventory", "syntax-advisory", "tooling-advisory"} and SEVERITY_RANK[item.severity] <= maximum_rank for item in findings)


def render_text(root: Path, files: Sequence[Path], findings: Sequence[Finding], excludes: Sequence[str] = (), fail_on: str = "error") -> None:
    print(f"software-architecture audit: {len(files)} architecture-bearing files")
    print("scope: " + ("scoped (explicit acknowledgement)" if excludes else "full repository"))
    print("gate: " + ("inventory-only (explicit acknowledgement)" if fail_on == "never" else f"fail-on {fail_on}"))
    print("excludes: " + (", ".join(excludes) if excludes else "none"))
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


def render_json(root: Path, report: AuditReport, excludes: Sequence[str] = (), fail_on: str = "error") -> None:
    def shown_path(path: Path) -> str:
        try:
            return str(path.relative_to(root))
        except ValueError:
            return str(path)

    payload = {"root": str(root), "source_files": sum(path.suffix.lower() in SOURCE_EXTENSIONS for path in report.files), "audited_files": len(report.files), "scope": "scoped" if excludes else "full", "gate": "inventory-only" if fail_on == "never" else f"fail-on {fail_on}", "excludes": list(excludes), "analyzers": [asdict(item) for item in report.analyzers], "findings": [{**asdict(item), "path": shown_path(item.path)} for item in report.findings]}
    print(json.dumps(payload, indent=2, sort_keys=True))


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    if not (0 < args.soft <= args.strong <= args.hard):
        print("error: require 0 < soft <= strong <= hard", file=sys.stderr)
        return 2
    if args.exclude and not args.allow_scoped_audit:
        print("error: --exclude requires --allow-scoped-audit; obtain explicit user approval before narrowing audit scope", file=sys.stderr)
        return 2
    if args.fail_on == "never" and not args.allow_advisory_audit:
        print("error: --fail-on never requires --allow-advisory-audit; obtain explicit user approval before using inventory-only output", file=sys.stderr)
        return 2
    exceptions_path = args.exceptions.resolve() if args.exceptions else None
    if exceptions_path is not None:
        try:
            exceptions_path.relative_to(root)
        except ValueError:
            print("error: --exceptions must be inside the audited repository", file=sys.stderr)
            return 2
    report = audit_report(root, soft=args.soft, strong=args.strong, hard=args.hard, flat_limit=args.flat_limit, include_generated=args.include_generated, excludes=args.exclude, exceptions_path=exceptions_path, tool_timeout=args.tool_timeout)
    if report.analyzers and args.output_format == "text":
        print("analyzers: " + ", ".join(f"{item.rule_id}={item.status}" for item in report.analyzers))
    if args.output_format == "json":
        render_json(root, report, args.exclude, args.fail_on)
    else:
        render_text(root, report.files, report.findings, args.exclude, args.fail_on)
    return 1 if should_fail(report.findings, args.fail_on) else 0
