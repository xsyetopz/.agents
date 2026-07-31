#!/usr/bin/env python3
"""Find candidate slop phrases across text and naming surfaces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from structure_scan import structural_findings as parsed_structural_findings


@dataclass(frozen=True)
class Rule:
    category: str
    severity: str
    phrase: str
    replacement: str
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class Finding:
    source: str
    line: int
    column: int
    match: str
    category: str
    severity: str
    reason: str
    replacement: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Files to scan; omit for stdin.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--hard-only", action="store_true", help="Exclude contextual and structural candidates.")
    parser.add_argument("--include-quotes", action="store_true", help="Scan Markdown blockquotes.")
    parser.add_argument("--all-surfaces", action="store_true", help="Scan code, commands, paths, filenames, flags, identifiers, and quoted text.")
    parser.add_argument("--include-seed-lexicon", action="store_true", help="Add the structured seed lexicon as contextual candidates.")
    parser.add_argument("--phrase-file", type=Path, help="Phrase corpus; defaults to references/phrases.tsv.")
    parser.add_argument("--seed-file", type=Path, help="Structured seed lexicon; defaults to references/seed-lexicon.tsv.")
    return parser.parse_args()


def read_sources(paths: list[str]) -> list[tuple[str, str]]:
    if not paths or paths == ["-"]:
        return [("<stdin>", sys.stdin.read())]
    sources: list[tuple[str, str]] = []
    for raw_path in paths:
        if raw_path == "-":
            sources.append(("<stdin>", sys.stdin.read()))
            continue
        path = Path(raw_path)
        try:
            sources.append((str(path), path.read_text(encoding="utf-8")))
        except OSError as error:
            raise RuntimeError(f"cannot read {path}: {error}") from error
    return sources


def load_rules(path: Path) -> tuple[Rule, ...]:
    rules: list[Rule] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise RuntimeError(f"cannot read phrase corpus {path}: {error}") from error
    for number, line in enumerate(lines, start=1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 4:
            raise RuntimeError(f"{path}:{number}: expected four tab-separated fields")
        category, severity, phrase, replacement = fields
        boundary = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
        rules.append(
            Rule(
                category=category,
                severity=severity,
                phrase=phrase,
                replacement=replacement,
                pattern=re.compile(boundary, re.IGNORECASE),
            )
        )
    return tuple(rules)


def load_seed_rules(path: Path) -> tuple[Rule, ...]:
    rules: list[Rule] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise RuntimeError(f"cannot read seed lexicon {path}: {error}") from error
    for number, line in enumerate(lines, start=1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 5:
            raise RuntimeError(f"{path}:{number}: expected five tab-separated fields")
        category, term, source, license_name, role = fields
        if role != "candidate":
            continue
        rules.append(
            Rule(
                category=f"seed-{category}",
                severity="contextual",
                phrase=term,
                replacement="name the specific property",
                pattern=re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE),
            )
        )
    return tuple(rules)


def blank_ranges(line: str, include_quotes: bool, all_surfaces: bool) -> str:
    masked = list(line)

    if all_surfaces:
        return line

    def blank(match: re.Match[str]) -> None:
        for index in range(match.start(), match.end()):
            if masked[index] != "\n":
                masked[index] = " "

    if not include_quotes and line.lstrip().startswith(">"):
        return " " * len(line)
    for pattern in (
        re.compile(r"https?://[^\s)>\]]+"),
        re.compile(r"\x60[^\n\x60]*\x60"),
        re.compile(r"\[[^\]\n]+\]\([^)]+\)"),
    ):
        for match in pattern.finditer(line):
            blank(match)
    if not include_quotes:
        for pattern in (
            re.compile(r'"[^"\n]*"'),
            re.compile(r"“[^”\n]*”"),
            re.compile(r"‘[^’\n]*’"),
        ):
            for match in pattern.finditer(line):
                blank(match)
    return "".join(masked)


def mask_protected(text: str, include_quotes: bool, all_surfaces: bool = False) -> list[str]:
    if all_surfaces:
        return text.splitlines()
    visible: list[str] = []
    in_fence = False
    fence_marker = "\x60\x60\x60"
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(fence_marker) or stripped.startswith("~~~"):
            in_fence = not in_fence
            visible.append(" " * len(line))
            continue
        visible.append(" " * len(line) if in_fence else blank_ranges(line, include_quotes, all_surfaces))
    return visible


def phrase_findings(source: str, text: str, rules: tuple[Rule, ...], include_quotes: bool, hard_only: bool, all_surfaces: bool) -> list[Finding]:
    findings: list[Finding] = []
    visible_lines = mask_protected(text, include_quotes, all_surfaces)
    original_lines = text.splitlines()
    for line_number, visible in enumerate(visible_lines, start=1):
        original = original_lines[line_number - 1]
        for rule in rules:
            if hard_only and rule.severity != "hard":
                continue
            for match in rule.pattern.finditer(visible):
                if rule.phrase.casefold() == "quietly" and re.search(r"\b(?:runs|run|operates|plays)\s+$", visible[:match.start()], re.IGNORECASE):
                    continue
                findings.append(
                    Finding(
                        source=source,
                        line=line_number,
                        column=match.start() + 1,
                        match=original[match.start():match.end()],
                        category=rule.category,
                        severity=rule.severity,
                        reason="literal candidate; apply the necessity test",
                        replacement=rule.replacement,
                    )
                )
    return findings


def filename_findings(source: str, rules: tuple[Rule, ...], hard_only: bool) -> list[Finding]:
    name = Path(source).name
    findings: list[Finding] = []
    for rule in rules:
        if hard_only and rule.severity != "hard":
            continue
        match = re.search(re.escape(rule.phrase), name, re.IGNORECASE)
        if match:
            findings.append(
                Finding(
                    source=source,
                    line=0,
                    column=1,
                    match=name,
                    category=rule.category,
                    severity=rule.severity,
                    reason="literal candidate in filename; apply the necessity test",
                    replacement=rule.replacement,
                )
            )
    return findings


def structural_findings(source: str, text: str, include_quotes: bool, all_surfaces: bool) -> list[Finding]:
    del all_surfaces
    return [Finding(**asdict(item)) for item in parsed_structural_findings(source, text, include_quotes)]


def scan(source: str, text: str, rules: tuple[Rule, ...], include_quotes: bool, hard_only: bool, all_surfaces: bool = False) -> list[Finding]:
    findings = phrase_findings(source, text, rules, include_quotes, hard_only, all_surfaces)
    if not hard_only and not all_surfaces:
        findings.extend(structural_findings(source, text, include_quotes, False))
    if all_surfaces:
        findings.extend(filename_findings(source, rules, hard_only))
    unique: dict[tuple[str, int, int, str], Finding] = {}
    for finding in findings:
        key = (finding.source, finding.line, finding.column, finding.match.casefold())
        unique.setdefault(key, finding)
    return sorted(unique.values(), key=lambda item: (item.source, item.line, item.column, item.category))


def emit(findings: list[Finding], as_json: bool) -> None:
    if as_json:
        print(json.dumps({"findings": [asdict(item) for item in findings], "count": len(findings)}, ensure_ascii=False, indent=2))
        return
    if not findings:
        print("No candidate findings.")
        return
    for finding in findings:
        print(f"{finding.source}:{finding.line}:{finding.column}: {finding.category}/{finding.severity}: {finding.match!r} -> {finding.replacement} ({finding.reason})")


def main() -> int:
    arguments = parse_args()
    root = Path(__file__).resolve().parents[1]
    phrase_path = arguments.phrase_file or root / "references" / "phrases.tsv"
    seed_path = arguments.seed_file or root / "references" / "seed-lexicon.tsv"
    try:
        rules = load_rules(phrase_path)
        if arguments.include_seed_lexicon:
            rules += load_seed_rules(seed_path)
        findings: list[Finding] = []
        for source, text in read_sources(arguments.paths):
            findings.extend(
                scan(
                    source,
                    text,
                    rules,
                    arguments.include_quotes or arguments.all_surfaces,
                    arguments.hard_only,
                    arguments.all_surfaces,
                )
            )
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    emit(findings, arguments.json)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
