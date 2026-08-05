#!/usr/bin/env python3
"""Run the architecture-design skill's report and evaluation checks.

The entry point keeps the two checks under one capability-owned interface:

    skill_checks.py report REPORT [--mode R3] [--json]
    skill_checks.py eval-cases [PATH]

Both checks remain intentionally small static gates.  They do not replace
architectural review or the repository architecture audit.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Callable

MODE_SECTIONS = {
    "R0": ["Task Contract", "Evidence"],
    "R1": ["Task Contract", "Evidence", "Candidate", "Critical Flow", "Verification"],
    "R2": [
        "Task Contract", "Evidence", "Domain", "Quality-Attribute", "Candidate",
        "Selected Architecture", "Static Structure", "Critical Flow", "Component Contract",
        "Risk", "Implementation Slice", "Verification",
    ],
    "R3": [
        "Task Contract", "Evidence", "Domain", "Quality-Attribute", "Candidate",
        "Decision Matrix", "Selected Architecture", "Static Structure", "Critical Flow",
        "Component Contract", "Data", "Runtime", "Risk", "ADR", "Implementation Slice",
        "Verification", "Deferred",
    ],
    "R4": [
        "Task Contract", "Evidence", "Domain", "Quality-Attribute", "Candidate",
        "Decision Matrix", "Selected Architecture", "Static Structure", "Critical Flow",
        "Component Contract", "Data", "Runtime", "Deployment", "Risk", "ADR",
        "Implementation Slice", "Verification", "Deferred",
    ],
}

PLACEHOLDER_RE = re.compile(r"(?:<[^>]+>|\b(?:TBD|TODO|FIXME|PLACEHOLDER)\b)", re.IGNORECASE)
ID_PATTERNS = {
    "objective": re.compile(r"\bOBJ-\d+\b"),
    "requirement": re.compile(r"\bREQ-\d+\b"),
    "quality": re.compile(r"\bQA-\d+\b"),
    "component": re.compile(r"\bCMP-\d+\b"),
    "risk": re.compile(r"\bRISK-\d+\b"),
}

REQUIRED_EVAL_KEYS = {"id", "category", "prompt", "expected"}
ALLOWED_EVAL_CATEGORIES = {"trigger", "process", "outcome", "style", "efficiency"}
DEFAULT_EVAL_CASES = Path(__file__).resolve().parents[1] / "assets" / "eval-cases.jsonl"


def contains_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^#{{1,6}}\s+.*{re.escape(fragment)}.*$", text, re.I | re.M))


def evaluate(text: str, mode: str) -> tuple[list[str], list[str]]:
    """Return report errors and warnings for the requested rigor mode."""

    errors: list[str] = []
    warnings: list[str] = []

    for section in MODE_SECTIONS[mode]:
        if not contains_heading(text, section):
            errors.append(f"Missing heading containing: {section}")

    placeholder_count = len(PLACEHOLDER_RE.findall(text))
    if placeholder_count:
        errors.append(f"Report contains {placeholder_count} placeholder marker(s).")

    for label, pattern in ID_PATTERNS.items():
        if not pattern.search(text):
            warnings.append(f"No stable {label} identifier found.")

    candidate_headings = re.findall(r"^#{2,6}\s+Candidate\b", text, re.I | re.M)
    baseline_present = bool(re.search(r"do[- ]less|baseline", text, re.I))
    if mode in {"R2", "R3", "R4"} and len(candidate_headings) < 2:
        errors.append("R2+ reports require at least two candidate headings.")
    if mode in {"R1", "R2", "R3", "R4"} and not baseline_present:
        errors.append("A do-less/baseline candidate is required.")

    qa_rows = len(re.findall(r"\bQA-\d+\b", text))
    min_qa = {"R0": 0, "R1": 1, "R2": 3, "R3": 5, "R4": 5}[mode]
    if qa_rows < min_qa:
        errors.append(f"{mode} requires at least {min_qa} quality-attribute scenario references; found {qa_rows}.")

    required_flow_terms = ["invalid input", "failure", "timeout", "cancellation", "recovery", "partial completion"]
    if mode in {"R2", "R3", "R4"}:
        for term in required_flow_terms:
            if term not in text.lower():
                errors.append(f"Critical-flow coverage missing term/concept: {term}")

    if mode in {"R2", "R3", "R4"} and "```mermaid" not in text:
        warnings.append("No Mermaid diagram found; verify that static and dynamic views are still unambiguous.")

    consequence_terms = ["negative", "disadvantage", "liabilit", "accepted cost"]
    if mode in {"R1", "R2", "R3", "R4"} and not any(term in text.lower() for term in consequence_terms):
        errors.append("No explicit negative consequence or accepted liability found.")

    if mode in {"R2", "R3", "R4"}:
        for term in ["state owner", "control authority", "dependency direction", "invariant"]:
            if term not in text.lower():
                errors.append(f"Architecture contract missing concept: {term}")

    if mode in {"R3", "R4"}:
        for term in ["sensitivity", "tradeoff", "migration", "traceability"]:
            if term not in text.lower():
                errors.append(f"R3+ analysis missing concept: {term}")

    if re.search(r"\b(?:Manager|Service|Handler|Engine|Utils)\b", text) and "purpose" not in text.lower():
        warnings.append("Generic component nouns appear without an obvious purpose/contract section.")

    return errors, warnings


def validate_eval_cases(path: Path) -> tuple[list[str], int]:
    """Return JSONL validation errors and the number of non-empty cases."""

    errors: list[str] = []
    seen: set[str] = set()
    count = 0
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        count += 1
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: invalid JSON: {exc}")
            continue
        missing = REQUIRED_EVAL_KEYS - obj.keys()
        if missing:
            errors.append(f"line {line_no}: missing keys {sorted(missing)}")
        case_id = obj.get("id")
        if case_id in seen:
            errors.append(f"line {line_no}: duplicate id {case_id!r}")
        if case_id:
            seen.add(case_id)
        if obj.get("category") not in ALLOWED_EVAL_CATEGORIES:
            errors.append(f"line {line_no}: invalid category {obj.get('category')!r}")
        for key in ("prompt", "expected"):
            if not isinstance(obj.get(key), str) or not obj.get(key, "").strip():
                errors.append(f"line {line_no}: {key} must be a non-empty string")
    return errors, count


def _report_command(args: argparse.Namespace) -> int:
    try:
        text = args.report.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors, warnings = evaluate(text, args.mode)
    passed = not errors and not warnings
    result = {
        "report": str(args.report),
        "mode": args.mode,
        "passed": passed,
        "errors": errors,
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        print("PASS" if passed else "FAILED")

    return 0 if passed else 1


def _eval_cases_command(args: argparse.Namespace) -> int:
    try:
        errors, count = validate_eval_cases(args.path)
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} error(s) across {count} case(s).")
        return 1
    print(f"PASS: {count} unique evaluation cases.")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate architecture reports and architecture-design evaluation cases."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    report = commands.add_parser(
        "report", aliases=["architecture-report"], help="validate an architecture report"
    )
    report.add_argument("report", type=Path)
    report.add_argument("--mode", choices=sorted(MODE_SECTIONS), default="R3")
    report.add_argument("--json", action="store_true")
    report.set_defaults(handler=_report_command)

    eval_cases = commands.add_parser(
        "eval-cases", aliases=["eval"], help="validate bundled JSONL evaluation cases"
    )
    eval_cases.add_argument("path", nargs="?", type=Path, default=DEFAULT_EVAL_CASES)
    eval_cases.set_defaults(handler=_eval_cases_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    handler: Callable[[argparse.Namespace], int] = args.handler
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
