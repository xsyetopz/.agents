"""Fence-aware Markdown heading and section operations."""

from __future__ import annotations

import re
from dataclasses import dataclass


ATX_HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")
SETEXT_HEADING_RE = re.compile(r"^[ \t]{0,3}(=+|-+)[ \t]*$")
FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})(.*)$")


@dataclass(frozen=True)
class Heading:
    """An ATX heading outside a fenced code block."""

    level: int
    title: str
    start: int
    end: int


def headings(text: str) -> list[Heading]:
    """Return ATX headings while ignoring headings inside code fences."""
    result: list[Heading] = []
    offset = 0
    fence_character: str | None = None
    fence_length = 0
    previous: tuple[str, int, int] | None = None
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        fence = FENCE_RE.match(content)
        if fence_character is None:
            if fence:
                fence_character = fence.group(1)[0]
                fence_length = len(fence.group(1))
                previous = None
            else:
                heading = ATX_HEADING_RE.match(content)
                if heading:
                    title = re.sub(r"[ \t]+#+[ \t]*$", "", heading.group(2)).strip()
                    result.append(
                        Heading(
                            len(heading.group(1)), title, offset, offset + len(line)
                        )
                    )
                    previous = None
                else:
                    setext = SETEXT_HEADING_RE.match(content)
                    if setext and previous:
                        title, start, _ = previous
                        result.append(
                            Heading(
                                1 if setext.group(1)[0] == "=" else 2,
                                title.strip(),
                                start,
                                offset + len(line),
                            )
                        )
                        previous = None
                    elif (
                        content.strip()
                        and len(content) - len(content.lstrip(" \t")) <= 3
                    ):
                        previous = (content, offset, offset + len(line))
                    else:
                        previous = None
        elif (
            fence
            and fence.group(1)[0] == fence_character
            and len(fence.group(1)) >= fence_length
        ):
            if not fence.group(2).strip():
                fence_character = None
                fence_length = 0
                previous = None
        offset += len(line)
    return result


def matching_headings(text: str, title: str, level: int | None = None) -> list[Heading]:
    return [
        heading
        for heading in headings(text)
        if heading.title.casefold() == title.casefold()
        and (level is None or heading.level == level)
    ]


def section_bounds(text: str, heading: Heading) -> tuple[int, int]:
    end = len(text)
    for following in headings(text):
        if following.start >= heading.end and following.level <= heading.level:
            end = following.start
            break
    return heading.start, end


def section(text: str, title: str, level: int = 2) -> str:
    matches = matching_headings(text, title, level)
    if len(matches) != 1:
        raise ValueError(f"document must contain one level-{level} section: {title}")
    start, end = section_bounds(text, matches[0])
    return text[start:end].strip() + "\n"


def replace_section(existing: str, desired: str, title: str) -> str:
    """Replace or append one owned level-2 section."""
    matches = matching_headings(existing, title)
    if len(matches) > 1:
        raise ValueError(f"duplicate Markdown heading: {title}")
    if matches and matches[0].level != 2:
        raise ValueError(f"owned Markdown heading must use level 2: {title}")
    if not matches:
        return (existing.rstrip() + "\n\n" + desired.strip() + "\n").lstrip("\n")
    start, end = section_bounds(existing, matches[0])
    pieces = (existing[:start].rstrip(), desired.strip(), existing[end:].strip())
    return "\n\n".join(piece for piece in pieces if piece) + "\n"


def move_section_to_end(existing: str, desired: str, title: str) -> str:
    """Replace a level-2 section and make it the document's final section."""
    matches = matching_headings(existing, title)
    if len(matches) > 1:
        raise ValueError(f"duplicate Markdown heading: {title}")
    if matches and matches[0].level != 2:
        raise ValueError(f"owned Markdown heading must use level 2: {title}")
    if matches:
        start, end = section_bounds(existing, matches[0])
        existing = "\n\n".join(
            piece
            for piece in (existing[:start].rstrip(), existing[end:].strip())
            if piece
        )
    return (existing.rstrip() + "\n\n" + desired.strip() + "\n").lstrip("\n")


def insert_before_headings(
    existing: str, desired: str, title: str, before: list[str]
) -> str:
    """Replace an owned section and insert it before the first named heading."""
    matches = matching_headings(existing, title)
    if len(matches) > 1:
        raise ValueError(f"duplicate Markdown heading: {title}")
    if matches and matches[0].level != 2:
        raise ValueError(f"owned Markdown heading must use level 2: {title}")
    if matches:
        start, end = section_bounds(existing, matches[0])
        existing = existing[:start].rstrip() + "\n\n" + existing[end:].lstrip()
    target_positions = [
        heading.start
        for heading in headings(existing)
        if any(heading.title.casefold() == item.casefold() for item in before)
    ]
    index = min(target_positions) if target_positions else len(existing)
    pieces = (existing[:index].rstrip(), desired.strip(), existing[index:].lstrip())
    return "\n\n".join(piece for piece in pieces if piece) + "\n"
