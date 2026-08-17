"""Check catalog selectors and the shared skill section contract.

The checker validates headings, section content, and verification markers. It
does not judge source snapshots or behavioral activation; the only tone
exceptions are imported source material and explicit evaluation-case evidence.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

EXPECTED_HEADINGS = [
    "Use this skill",
    "Rules",
    "Steps",
    "Resources",
    "Verify",
]
PACKAGE_CHECK_COMMAND = "python3 scripts/check.py"
UNAVAILABLE_MARKER_RE = re.compile(
    r"\b(?:unverified|unavailable|not\s+(?:run|available|executed|verified)|skipped)\b",
    re.IGNORECASE,
)
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
HEADING_LINE = re.compile(r"^##\s+(.+?)(?:\s*\{#[^}]+\})?\s*$")
WORD = re.compile(r"[A-Za-z0-9]+(?:[+./:-][A-Za-z0-9]+)*")
ROOT_REFERENCE_LINK = re.compile(
    r"\[[^\]]*\]\(\s*((?:\./)?references/[A-Za-z0-9_.-]+"
    r"(?:/[A-Za-z0-9_.-]+)*\.md)"
)
INDEX_REFERENCE_LINK = re.compile(
    r"\[[^\]]*\]\(\s*((?:\./)?(?:references/)?[A-Za-z0-9_.-]+"
    r"(?:/[A-Za-z0-9_.-]+)*\.md)"
)
MERMAID_FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
MERMAID_DECLARATION_RE = re.compile(r"^\s*(?:flowchart|graph)\b", re.IGNORECASE)
MERMAID_LEGACY_LABEL_RE = re.compile(r"--\s+[^|>\n]+?\s+-->")


def _common_section_bodies(text: str) -> dict[str, str]:
    """Return body text for common H2 sections outside fenced headings."""
    lines = text.splitlines()
    positions: list[tuple[str, int]] = []
    fence: str | None = None
    for index, line in enumerate(lines):
        fence_match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is not None:
            if fence_match and fence_match.group(1)[0] == fence:
                fence = None
            continue
        if fence_match:
            fence = fence_match.group(1)[0]
            continue
        match = HEADING_LINE.match(line)
        if match:
            positions.append((match.group(1).strip(), index))

    bodies: dict[str, str] = {}
    for position, (title, start) in enumerate(positions):
        if title not in EXPECTED_HEADINGS:
            continue
        end = (
            positions[position + 1][1] if position + 1 < len(positions) else len(lines)
        )
        bodies[title] = "\n".join(lines[start + 1 : end]).strip()
    return bodies


def check_common_section_semantics(text: str) -> list[str]:
    """Check section content and explicit verification limits."""
    bodies = _common_section_bodies(text)
    errors = [
        f"SKILL.md section '## {title}' must not be empty."
        for title in EXPECTED_HEADINGS
        if not bodies.get(title)
    ]
    verify = bodies.get("Verify", "")
    if PACKAGE_CHECK_COMMAND not in verify:
        errors.append(
            f"SKILL.md section '## Verify' must include {PACKAGE_CHECK_COMMAND}."
        )
    if not UNAVAILABLE_MARKER_RE.search(verify):
        errors.append(
            "SKILL.md section '## Verify' must classify unavailable evidence "
            "with UNVERIFIED, unavailable, not run, or skipped."
        )
    return errors


def _without_fenced_blocks(text: str) -> str:
    lines: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is not None:
            if marker and marker.group(1)[0] == fence:
                fence = None
            continue
        if marker:
            fence = marker.group(1)[0]
            continue
        lines.append(line)
    return "\n".join(lines)


def root_index_duplicates(skill_text: str, index_text: str) -> set[str]:
    """Return leaf links repeated in Resources and references/index.md."""
    resources = _without_fenced_blocks(
        _common_section_bodies(skill_text).get("Resources", "")
    )
    root_links = {
        match.removeprefix("./") for match in ROOT_REFERENCE_LINK.findall(resources)
    }
    indexed: set[str] = set()
    for match in INDEX_REFERENCE_LINK.findall(_without_fenced_blocks(index_text)):
        target = match.removeprefix("./")
        if not target.startswith("references/"):
            target = f"references/{target}"
        indexed.add(target)
    root_links.discard("references/index.md")
    indexed.discard("references/index.md")
    return root_links & indexed


def _mermaid_blocks(
    text: str,
) -> tuple[list[tuple[int, list[tuple[int, str]]]], list[str]]:
    """Return Mermaid fences and errors for unterminated fenced blocks."""
    blocks: list[tuple[int, list[tuple[int, str]]]] = []
    errors: list[str] = []
    opening: tuple[str, int, int, list[tuple[int, str]]] | None = None
    for line_no, line in enumerate(text.splitlines(), 1):
        match = MERMAID_FENCE_RE.match(line)
        if opening is None:
            if not match:
                continue
            info = match.group(2).strip().lower()
            if info == "mermaid":
                opening = (match.group(1)[0], len(match.group(1)), line_no, [])
            continue
        character, length, start, body = opening
        if match and match.group(1)[0] == character and len(match.group(1)) >= length:
            blocks.append((start, body))
            opening = None
        else:
            body.append((line_no, line))
    if opening is not None:
        errors.append(f"Unterminated Mermaid fence at line {opening[2]}")
    return blocks, errors


def check_skill_creator_references(root: Path, errors: list[str]) -> None:
    """Check catalog selectors and standard GitHub Mermaid syntax."""
    if root.name != "skill-creator":
        return
    for markdown in sorted((root / "references").rglob("*.md")):
        relative = markdown.relative_to(root)
        if (
            "official" in relative.parts
            or "generated" in relative.parts
            or markdown.name.endswith((".snapshot.md", ".generated.md"))
        ):
            continue
        try:
            text = markdown.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"Unable to read {relative}: {exc}")
            continue
        blocks, fence_errors = _mermaid_blocks(text)
        for message in fence_errors:
            errors.append(f"{relative}: {message}")
        for start, body in blocks:
            if not any(line.strip() for _line_no, line in body):
                errors.append(f"{relative}:{start}: Mermaid fence is empty")
            for line_no, line in body:
                if MERMAID_LEGACY_LABEL_RE.search(line):
                    errors.append(
                        f"{relative}:{line_no}: Mermaid edge labels must use -->|label| syntax"
                    )
        unfenced = _without_fenced_blocks(text)
        for line_no, line in enumerate(unfenced.splitlines(), 1):
            if MERMAID_DECLARATION_RE.match(line):
                errors.append(
                    f"{relative}:{line_no}: Mermaid declarations must be in a ```mermaid fence"
                )


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
    return relative.startswith("apple-design-hig/")


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
            errors.append(
                f"{relative}: description exceeds {DESCRIPTION_LIMIT} characters"
            )
        if re.search(r"\buse\s+(?:for|to)\b", description, re.IGNORECASE):
            errors.append(f"{relative}: description uses forbidden 'Use for'/'Use to'")
        skill_text = (package / "SKILL.md").read_text(encoding="utf-8")
        found = headings(package / "SKILL.md")
        if found != EXPECTED_HEADINGS:
            errors.append(f"{relative}: H2 order differs from the common contract")
        else:
            for message in check_common_section_semantics(skill_text):
                errors.append(f"{relative}: {message}")

        index = package / "references" / "index.md"
        if not index.is_file():
            prefix = f"skills/{name}" if catalog_mode else name
            errors.append(f"{prefix}: missing references/index.md")
        else:
            duplicates = root_index_duplicates(
                skill_text, index.read_text(encoding="utf-8")
            )
            if len(duplicates) >= 3:
                errors.append(
                    f"{relative}: Resources repeats {len(duplicates)} leaf links "
                    "already routed by references/index.md; keep at most two"
                )
        references = package / "references"
        if references.is_dir():
            for child in sorted(references.iterdir()):
                if child.is_file() and child.name in GENERIC_ROOT_NAMES:
                    prefix = f"skills/{name}" if catalog_mode else name
                    errors.append(
                        f"{prefix}/references/{child.name}: generic root filename"
                    )
        check_skill_creator_references(package, errors)

    # Review authored Markdown labels, excluding source snapshots and explicit
    # evaluation corpus exceptions. Line-level diagnostics make exceptions auditable.
    for path in sorted(skills_root.glob("**/*.md")):
        rel = path.relative_to(root).as_posix()
        if "/references/official/" in f"/{rel}":
            continue
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            for term in FORBIDDEN_LABELS:
                if not re.search(
                    r"(?<![A-Za-z0-9_-])" + re.escape(term) + r"(?![A-Za-z0-9_-])",
                    line,
                    re.IGNORECASE,
                ):
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
