"""Run fixed, read-only architecture analysis providers."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from provider_ast import run_ast_grep as _run_ast_grep
from provider_capabilities import capability_report as _capability_report
from provider_graph import run_graph as _run_graph


# CLI for capability discovery and read-only syntax queries.
def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run fixed, read-only architecture analyzers."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    capabilities = subparsers.add_parser(
        "capabilities", help="show available providers"
    )
    capabilities.add_argument("--root", default=".")
    capabilities.add_argument("--format", choices=("json", "text"), default="text")
    query = subparsers.add_parser("ast-query", help="run one ast-grep structural query")
    query.add_argument("--root", default=".")
    query.add_argument("--tool", choices=("ast-grep",), default="ast-grep")
    query.add_argument("--language", required=True)
    query.add_argument("--pattern", required=True)
    query.add_argument("--rule-id", default="ad-hoc-ast-query")
    query.add_argument(
        "--severity", choices=("error", "warning", "notice"), default="warning"
    )
    query.add_argument("--message", default="syntax query matched")
    query.add_argument("--timeout", type=float, default=30)
    query.add_argument("--format", choices=("json", "text"), default="text")
    query.add_argument("paths", nargs="*", default=["."])
    graph = subparsers.add_parser("graph", help="read a package graph from Cargo or Go")
    graph.add_argument("--root", default=".")
    graph.add_argument(
        "--tool", choices=("auto", "cargo-metadata", "go-list"), default="auto"
    )
    graph.add_argument("--timeout", type=float, default=30)
    graph.add_argument("--format", choices=("json", "text"), default="text")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "capabilities":
        report = _capability_report(Path(args.root))
        if args.format == "json":
            print(
                json.dumps(
                    {"schema": "architecture-capabilities/v1", "providers": report},
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            for item in report:
                suffix = (
                    f" ({item.get('version', 'unknown')})"
                    if item.get("version")
                    else ""
                )
                print(
                    f"{item['id']}: {item['status']}{suffix} - {item.get('diagnostic', item.get('path', ''))}"
                )
        return 0
    if args.command == "graph":
        result = _run_graph(Path(args.root), tool=args.tool, timeout_s=args.timeout)
        payload = result.as_dict(Path(args.root))
        if args.format == "json":
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(f"{result.provider}: {result.status}")
            if result.payload is not None:
                print(json.dumps(result.payload, indent=2, sort_keys=True))
            for diagnostic in result.diagnostics:
                print(f"diagnostic: {diagnostic}")
        return {
            "passed": 0,
            "blocked": 3,
            "tool-failed": 4,
            "timeout": 5,
            "invalid-output": 6,
        }.get(result.status, 4)
    result = _run_ast_grep(
        Path(args.root),
        rule_id=args.rule_id,
        language=args.language,
        pattern=args.pattern,
        severity=args.severity,
        message=args.message,
        paths=tuple(args.paths),
        timeout_s=args.timeout,
    )
    payload = result.as_dict(Path(args.root))
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"{result.provider}: {result.status} ({len(result.findings)} findings)")
        for finding in result.findings:
            print(
                f"{finding.path}:{finding.start_line}:{finding.start_column}: {finding.severity}: {finding.message}"
            )
        for diagnostic in result.diagnostics:
            print(f"diagnostic: {diagnostic}")
    return {
        "passed": 0,
        "violations": 1,
        "blocked": 3,
        "tool-failed": 4,
        "timeout": 5,
        "invalid-output": 6,
    }.get(result.status, 4)


if __name__ == "__main__":
    raise SystemExit(main())
