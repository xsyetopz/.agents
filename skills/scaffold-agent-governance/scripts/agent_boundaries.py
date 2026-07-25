"""Classify headings that belong to human rather than agent governance."""

from __future__ import annotations

import re

from markdown_sections import Heading


HUMAN_GOVERNANCE_HEADINGS = {
    "human contributor conduct",
    "human certification",
    "code of conduct",
    "contributing",
    "contribution requirements",
    "pull requests",
    "responsibility and rights",
    "community conduct",
    "human conduct",
    "contributor conduct",
}


def is_human_governance_heading(title: str, level: int) -> bool:
    """Return whether a level-2 heading defines policy for people."""
    if level != 2:
        return False
    normalized = re.sub(r"[^a-z0-9]+", " ", title.casefold()).strip()
    if normalized in HUMAN_GOVERNANCE_HEADINGS:
        return True
    words = set(normalized.split())
    if "conduct" in words and words & {"human", "community", "contributor", "code"}:
        return True
    human_cue = bool(
        words
        & {
            "human",
            "contributor",
            "contributors",
            "contribution",
            "community",
            "person",
            "people",
        }
    )
    if (
        human_cue
        and "review" in words
        and words
        & {
            "policy",
            "rules",
            "requirements",
            "guidelines",
            "process",
        }
    ):
        return True
    assisted = "assisted" in words or "assistance" in words
    contributors = bool(
        words & {"contribution", "contributions", "contributor", "contributors"}
    )
    return assisted and contributors and bool(words & {"tool", "ai"})


def find_human_governance_heading(headings: list[Heading]) -> Heading | None:
    return next(
        (
            heading
            for heading in headings
            if is_human_governance_heading(heading.title, heading.level)
        ),
        None,
    )
