#!/usr/bin/env python3
"""Compare protected tokens and high-risk facts before accepting a rewrite."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Inventory:
    urls: tuple[str, ...]
    code: tuple[str, ...]
    numbers: tuple[str, ...]
    paths: tuple[str, ...]
    quoted: tuple[str, ...]
    negation: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    return parser.parse_args()


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise RuntimeError(f"cannot read {path}: {error}") from error


def ordered_unique(values: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def inventory(text: str) -> Inventory:
    code: list[str] = []
    fenced = re.compile(r"\x60\x60\x60[^\n]*\n(.*?)\n\x60\x60\x60", re.DOTALL)
    for match in fenced.finditer(text):
        code.append(match.group(1))
    code.extend(re.findall(r"\x60([^\n\x60]+)\x60", text))
    urls = re.findall(r"https?://[^\s)>\]]+", text)
    numbers = re.findall(r"(?<!\w)(?:\d{4}-\d{1,2}-\d{1,2}|\d+(?:[.,]\d+)?)(?!(?:\w|[.,]\d))", text)
    without_urls = re.sub(r"https?://[^\s)>\]]+", " ", text)
    paths = re.findall(r"(?<!\w)(?:\./|/|~/|[A-Za-z]:[\\\\/])[\w./~@:+-]+", without_urls)
    quoted = re.findall(r'"([^"\n]+)"|“([^”\n]+)”|‘([^’\n]+)’', text)
    flat_quoted = [next(value for value in group if value) for group in quoted]
    negation_words = re.findall(r"\b(?:not|no|never|cannot|can't|won't|without|except|only|neither|nor)\b", text.casefold())
    return Inventory(
        urls=ordered_unique(urls),
        code=ordered_unique(code),
        numbers=ordered_unique(numbers),
        paths=ordered_unique(paths),
        quoted=ordered_unique(flat_quoted),
        negation=tuple(negation_words),
    )


def missing(original: tuple[str, ...], revised: tuple[str, ...]) -> list[str]:
    revised_counts = Counter(revised)
    missing_values: list[str] = []
    for value in original:
        if revised_counts[value] > 0:
            revised_counts[value] -= 1
        else:
            missing_values.append(value)
    return missing_values


def compare(before: Inventory, after: Inventory) -> dict[str, object]:
    lost = {
        field: missing(getattr(before, field), getattr(after, field))
        for field in ("urls", "code", "numbers", "paths", "quoted")
    }
    added = {
        field: missing(getattr(after, field), getattr(before, field))
        for field in ("urls", "code", "numbers", "paths", "quoted")
    }
    negation_changed = before.negation != after.negation
    return {
        "missing": lost,
        "added": added,
        "negation_changed": negation_changed,
        "before": asdict(before),
        "after": asdict(after),
        "clean": not any(lost.values()) and not negation_changed,
    }


def main() -> int:
    arguments = parse_args()
    try:
        result = compare(inventory(read(arguments.original)), inventory(read(arguments.revised)))
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if arguments.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["clean"]:
            print("Protected facts and negation match.")
        else:
            print("Semantic review required.")
            for field, values in result["missing"].items():
                if values:
                    print(f"missing {field}: {values}")
            if result["negation_changed"]:
                print("negation words changed")
    return 0 if result["clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
