"""Minimal, preservation-oriented GitHub CODEOWNERS support."""

from __future__ import annotations

import re
from collections.abc import Iterable


ACCOUNT_RE = re.compile(r"^@[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def is_owner(value: str) -> bool:
    return bool(ACCOUNT_RE.fullmatch(value) or EMAIL_RE.fullmatch(value))


def normalize_owners(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for raw in values:
        owner = raw.strip()
        if not is_owner(owner):
            raise ValueError(f"invalid GitHub code owner: {raw}")
        if owner.casefold() not in seen:
            result.append(owner)
            seen.add(owner.casefold())
    return result


def parse_rules(text: str, governed: set[str] | None = None) -> dict[str, str]:
    """Parse relevant exact rules and ignore unrelated rules without rewriting them.

    GitHub permits account names, team names, email addresses, ownerless reset
    rules, and comments. The caller preserves the original text verbatim.
    """
    result: dict[str, str] = {}
    for number, raw in enumerate(text.splitlines(), 1):
        content = raw.split("#", 1)[0].strip()
        if not content:
            continue
        parts = content.split()
        path, owners = parts[0], parts[1:]
        if governed is not None and path not in governed:
            continue
        if any(not is_owner(owner) for owner in owners):
            if governed is not None:
                raise ValueError(
                    f"invalid CODEOWNERS owner on line {number} for {path}"
                )
            continue
        result[path] = " ".join(owners)
    return result
