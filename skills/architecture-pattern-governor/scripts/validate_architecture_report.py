#!/usr/bin/env python3
"""Static gate checks for an architecture report produced with this skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

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


def contains_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^#{{1,6}}\s+.*{re.escape(fragment)}.*$", text, re.I | re.M))


def evaluate(text: str, mode: str) -> tuple[list[str], list[str]]:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--mode", choices=sorted(MODE_SECTIONS), default="R3")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        text = args.report.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors, warnings = evaluate(text, args.mode)
    result = {
        "report": str(args.report),
        "mode": args.mode,
        "passed": not errors,
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
        print("PASS" if not errors else "FAILED")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
