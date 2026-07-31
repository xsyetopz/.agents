"""Exact validation for owned Markdown sections."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import markdown_sections as markdown


def exact_sections(path: Path, full: str, titles: Iterable[str]) -> list[str]:
    if not path.is_file() or path.is_symlink():
        return [f"{path.name} must be a regular file"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    ordered_titles = tuple(titles)
    positions: list[int] = []
    for title in ordered_titles:
        try:
            if markdown.section(text, title) != markdown.section(full, title):
                errors.append(f"{path.name} has a modified {title} section")
            positions.append(markdown.matching_headings(text, title, 2)[0].start)
        except ValueError:
            errors.append(f"{path.name} must contain one level-2 {title} section")
    if len(positions) == len(ordered_titles) and positions != sorted(positions):
        errors.append(f"{path.name} has owned sections in a non-standard order")
    return errors
