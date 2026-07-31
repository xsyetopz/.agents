"""Parse Markdown blocks and report structural prose candidates without regexes."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from dataclasses import asdict
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    """Compatible with ``scan_text.Finding``."""

    source: str
    line: int
    column: int
    match: str
    category: str
    severity: str
    reason: str
    replacement: str


@dataclass(frozen=True)
class Block:
    kind: str
    line: int
    lines: tuple[str, ...]


def _indent(text: str) -> int:
    return len(text) - len(text.lstrip(" "))


def _fence(text: str) -> str | None:
    stripped = text.lstrip(" ")
    if _indent(text) > 3 or not stripped or stripped[0] not in "`~":
        return None
    marker = stripped[0]
    count = 0
    for character in stripped:
        if character != marker:
            break
        count += 1
    return marker if count >= 3 else None


def _heading(text: str) -> str | None:
    stripped = text.lstrip(" ")
    if _indent(text) > 3 or not stripped.startswith("#"):
        return None
    count = 0
    for character in stripped:
        if character != "#":
            break
        count += 1
    if not 1 <= count <= 6 or len(stripped) == count or not stripped[count].isspace():
        return None
    return stripped[count:].strip().rstrip("#").rstrip()


def _quote(text: str) -> str | None:
    stripped = text.lstrip(" ")
    if stripped.startswith(">"):
        return stripped[1:].lstrip(" ")
    return None


def _list(text: str) -> str | None:
    stripped = text.lstrip(" ")
    if not stripped:
        return None
    if stripped[0] in "-*+" and len(stripped) > 1 and stripped[1].isspace():
        return stripped[2:].lstrip()
    position = 0
    while position < len(stripped) and stripped[position].isdigit():
        position += 1
    if position and position < len(stripped) and stripped[position] in ".)":
        if position + 1 < len(stripped) and stripped[position + 1].isspace():
            return stripped[position + 2:].lstrip()
    return None


def parse_blocks(text: str) -> list[Block]:
    """Build the Markdown block types relevant to structural prose checks."""

    blocks: list[Block] = []
    paragraph: list[str] = []
    paragraph_line = 0
    in_fence: str | None = None

    def flush() -> None:
        nonlocal paragraph, paragraph_line
        if paragraph:
            blocks.append(Block("paragraph", paragraph_line, tuple(paragraph)))
            paragraph = []

    for number, line in enumerate(text.splitlines(), start=1):
        fence = _fence(line)
        if in_fence:
            flush()
            blocks.append(Block("fence", number, (line,)))
            if fence == in_fence:
                in_fence = None
            continue
        if fence:
            flush()
            blocks.append(Block("fence", number, (line,)))
            in_fence = fence
            continue
        if not line.strip():
            flush()
            blocks.append(Block("blank", number, (line,)))
            continue
        if _indent(line) >= 4:
            flush()
            blocks.append(Block("code", number, (line,)))
            continue
        heading = _heading(line)
        if heading is not None:
            flush()
            blocks.append(Block("heading", number, (heading,)))
            continue
        quote = _quote(line)
        if quote is not None:
            flush()
            blocks.append(Block("quote", number, (quote,)))
            continue
        item = _list(line)
        if item is not None:
            flush()
            blocks.append(Block("list", number, (item,)))
            continue
        if not paragraph:
            paragraph_line = number
        paragraph.append(line.strip())
    flush()
    return blocks


def _words(text: str) -> list[str]:
    words: list[str] = []
    current: list[str] = []
    for character in text.casefold():
        if character.isalpha():
            current.append(character)
        elif current:
            words.append("".join(current))
            current = []
    if current:
        words.append("".join(current))
    return words


def _normal(text: str) -> str:
    return " ".join(text.split()).casefold()


def _phase_label(text: str) -> bool:
    words = _words(text)
    if not words or words[0] not in {"phase", "stage", "step", "track"}:
        return False
    index = 0
    while index < len(text) and text[index].isspace():
        index += 1
    while index < len(text) and text[index].isalpha():
        index += 1
    while index < len(text) and text[index].isspace():
        index += 1
    digit_start = index
    while index < len(text) and text[index].isdigit():
        index += 1
    return index > digit_start and index < len(text) and text[index] == ":"


def _bold_first(text: str) -> bool:
    if not text.startswith("**"):
        return False
    end = text.find("**", 2)
    if end < 2:
        return False
    tail = text[end + 2:].lstrip()
    return bool(tail) and tail[0] in ":-–"


def _is_generic_heading(text: str) -> bool:
    generic = {"introduction", "overview", "conclusion", "key takeaways", "summary"}
    normalized = _normal(text)
    return normalized in generic or normalized.removeprefix("the ") in generic


def _eligible(block: Block, include_quotes: bool) -> bool:
    return block.kind in {"paragraph", "list"} or (include_quotes and block.kind == "quote")


def _make(source: str, line: int, match: str, category: str, reason: str, replacement: str) -> Finding:
    return Finding(source, line, 1, match, category, "structural", reason, replacement)


def structural_findings(source: str, text: str, include_quotes: bool = False) -> list[Finding]:
    """Return advisory findings from parsed Markdown structure and text tokens."""

    blocks = parse_blocks(text)
    findings: list[Finding] = []
    body = [block for block in blocks if _eligible(block, include_quotes)]

    for block in blocks:
        content = " ".join(block.lines)
        if block.kind == "list" and _bold_first(content):
            findings.append(_make(source, block.line, content, "format", "bold-first bullet may repeat its own sentence", "write the fact as the bullet"))
        if block.kind in {"paragraph", "list"} and _phase_label(content):
            findings.append(_make(source, block.line, content, "format", "numbered phase label may be a disguised template", "name the topic or use a real list"))
        if block.kind == "heading" and _is_generic_heading(content):
            findings.append(_make(source, block.line, content, "format", "generic heading may fill a template slot", "name the heading's content"))

    dash_count = sum(line.count("—") + line.count("–") for block in body for line in block.lines)
    if dash_count >= 3:
        findings.append(_make(source, 1, f"{dash_count} dash characters", "format", "dash density may signal repeated reframe or decoration", "inspect each dash in context"))

    paragraphs = [block for block in body if block.kind == "paragraph"]
    copies = Counter(_normal(" ".join(block.lines)) for block in paragraphs)
    for paragraph, count in copies.items():
        if count > 1 and len(paragraph) > 40:
            line = next(block.line for block in paragraphs if _normal(" ".join(block.lines)) == paragraph)
            findings.append(_make(source, line, paragraph[:120], "composition", "duplicated paragraph or section", "keep one complete statement"))

    starts: list[tuple[int, str]] = []
    for block in body:
        for offset, line in enumerate(block.lines):
            sentence: list[str] = []
            for character in line:
                sentence.append(character)
                if character in ".!?":
                    words = _words("".join(sentence))
                    if len(words) >= 2:
                        starts.append((block.line + offset, " ".join(words[:3])))
                    sentence = []
            words = _words("".join(sentence))
            if len(words) >= 2:
                starts.append((block.line + offset, " ".join(words[:3])))
    counts = Counter(value for _, value in starts)
    for opening, count in counts.items():
        if count >= 3:
            line = next(number for number, value in starts if value == opening)
            findings.append(_make(source, line, opening, "rhythm", "repeated sentence opening", "vary the syntax or keep the repetition only when it adds contrast"))

    candidates: list[tuple[int, str]] = []
    for block in body:
        candidates.extend((block.line + offset, line.strip()) for offset, line in enumerate(block.lines))
    for index in range(len(candidates) - 2):
        group = candidates[index:index + 3]
        if group[2][0] != group[0][0] + 2:
            continue
        texts = [line for _, line in group]
        if all(text and len(_words(text)) <= 5 and text[-1] not in ".:;" for text in texts):
            findings.append(_make(source, group[0][0], " / ".join(texts), "rhythm", "cluster of short fragments", "join the claim or keep one deliberate short sentence"))
            break
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Markdown files to scan; omit for stdin.")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--include-quotes", action="store_true", help="include blockquotes")
    arguments = parser.parse_args()
    paths = arguments.paths or ["-"]
    findings: list[Finding] = []
    for value in paths:
        if value == "-":
            findings.extend(structural_findings("<stdin>", sys.stdin.read(), arguments.include_quotes))
            continue
        path = Path(value)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            parser.error(f"cannot read {path}: {error}")
        findings.extend(structural_findings(str(path), text, arguments.include_quotes))
    if arguments.json:
        print(json.dumps({"findings": [asdict(item) for item in findings], "count": len(findings)}, ensure_ascii=False, indent=2))
    else:
        for finding in findings:
            print(f"{finding.source}:{finding.line}:{finding.column}: {finding.category}/{finding.severity}: {finding.match!r} -> {finding.replacement} ({finding.reason})")
        if not findings:
            print("No structural findings.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
