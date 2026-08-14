"""Check catalog selectors and the shared reference contract.

The checker is intentionally structural. It does not judge source snapshots or
behavioral activation; the only tone exceptions are imported source material
and explicit evaluation-case evidence.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

EXPECTED_HEADINGS = [
    "When to use",
    "When NOT to use",
    "Guardrails",
    "Workflow",
    "Quick start",
    "Reference map",
    "Completion",
    "Validation",
    "Related skills",
]
DESCRIPTION_WORDS = (8, 16)
DESCRIPTION_LIMIT = 140
GENERIC_ROOT_NAMES = {"workflow.md", "patterns.md", "tooling.md"}
FORBIDDEN_LABELS = (
    "obvious",
    "terrible",
    "lazy",
    "vibe-coded",
    "smell",
    "killer",
    "on sight",
    "force the user",
)
# Source snapshots and evaluation corpora may retain quoted terms as evidence.
# Authored files outside these paths fail on a newly introduced label.

FRONTMATTER_END = re.compile(r"^\s*---\s*$")
DESCRIPTION_LINE = re.compile(r"^description:\s*(.*)$")
HEADING_LINE = re.compile(r"^##\s+(.+?)\s*$")
WORD = re.compile(r"[A-Za-z0-9]+(?:[+./:-][A-Za-z0-9]+)*")

def parse_frontmatter(path: Path) -> tuple[str, bool, list[str]]:
    """Return description, multiline flag, and parse errors."""
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return "", False, ["missing opening frontmatter delimiter"]
    try:
        end = next(i for i in range(1, len(lines)) if FRONTMATTER_END.match(lines[i]))
    except StopIteration:
        return "", False, ["missing closing frontmatter delimiter"]
    description = ""
    multiline = False
    for i in range(1, end):
        match = DESCRIPTION_LINE.match(lines[i])
        if not match:
            continue
        raw = match.group(1).strip()
        if raw in {">", "|", ">-", "|-", ">+", "|+"}:
            multiline = True
            continuation: list[str] = []
            for line in lines[i + 1 : end]:
                if line.startswith((" ", "\t")):
                    continuation.append(line.strip())
                elif line.strip():
                    break
            description = " ".join(continuation)
        else:
            description = raw.strip("\"'")
            if i + 1 < end and lines[i + 1].startswith((" ", "\t")):
                multiline = True
    if not description:
        errors.append("missing description")
    return description, multiline, errors


def headings(path: Path) -> list[str]:
    """Collect level-two headings outside fenced blocks."""
    result: list[str] = []
    fenced: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        fence = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fenced:
            if fence and fence.group(1)[0] == fenced:
                fenced = None
            continue
        if fence:
            fenced = fence.group(1)[0]
            continue
        match = HEADING_LINE.match(line)
        if match:
            result.append(match.group(1).strip())
    return result


def baseline_tone(relative: str) -> bool:
    if relative.startswith("apple-design-hig/"):
        return True
    return relative.startswith("prompt-engineering/references/issues/")


def check(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    skills_root = root / "skills"
    catalog_mode = skills_root.is_dir()
    if catalog_mode:
        packages = sorted(path.parent for path in skills_root.glob("*/SKILL.md"))
    elif (root / "SKILL.md").is_file():
        packages = [root]
        skills_root = root
    else:
        return [f"No SKILL.md found under {root}"], notes

    for package in packages:
        name = package.name
        relative = f"skills/{name}/SKILL.md" if catalog_mode else "SKILL.md"
        description, multiline, parse_errors = parse_frontmatter(package / "SKILL.md")
        for message in parse_errors:
            errors.append(f"{relative}: {message}")
        words = WORD.findall(description)
        if multiline:
            errors.append(f"{relative}: description must be one line")
        if not DESCRIPTION_WORDS[0] <= len(words) <= DESCRIPTION_WORDS[1]:
            errors.append(
                f"{relative}: description has {len(words)} words; expected "
                f"{DESCRIPTION_WORDS[0]}–{DESCRIPTION_WORDS[1]}"
            )
        if len(description) > DESCRIPTION_LIMIT:
            errors.append(f"{relative}: description exceeds {DESCRIPTION_LIMIT} characters")
        if re.search(r"\buse\s+(?:for|to)\b", description, re.IGNORECASE):
            errors.append(f"{relative}: description uses forbidden 'Use for'/'Use to'")
        found = headings(package / "SKILL.md")
        if found != EXPECTED_HEADINGS:
            errors.append(f"{relative}: H2 order differs from the common contract")

        index = package / "references" / "index.md"
        if not index.is_file():
            prefix = f"skills/{name}" if catalog_mode else name
            errors.append(f"{prefix}: missing references/index.md")
        references = package / "references"
        if references.is_dir():
            for child in sorted(references.iterdir()):
                if child.is_file() and child.name in GENERIC_ROOT_NAMES:
                    prefix = f"skills/{name}" if catalog_mode else name
                    errors.append(
                        f"{prefix}/references/{child.name}: generic root filename"
                    )

    # Review authored Markdown labels, excluding source snapshots and explicit
    # evaluation corpus exceptions. Line-level diagnostics make exceptions auditable.
    for path in sorted(skills_root.glob("**/*.md")):
        rel = path.relative_to(root).as_posix()
        if "/references/official/" in f"/{rel}":
            continue
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            for term in FORBIDDEN_LABELS:
                if not re.search(r"(?<![A-Za-z0-9_-])" + re.escape(term) + r"(?![A-Za-z0-9_-])", line, re.IGNORECASE):
                    continue
                if baseline_tone(rel.removeprefix("skills/")):
                    notes.append(f"BASELINE tone label: {rel}:{line_no} ({term})")
                else:
                    errors.append(f"{rel}:{line_no}: subjective tone label '{term}'")
    return errors, notes


def main(argv: list[str] | None = None) -> int:
    root = Path(argv[0]).resolve() if argv else Path(__file__).resolve().parents[1]
    errors, notes = check(root)
    for note in notes:
        print(note)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"FAIL: {len(errors)} reference-contract error(s)", file=sys.stderr)
        return 1
    print(f"PASS: reference contract ({len(notes)} baseline note(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
