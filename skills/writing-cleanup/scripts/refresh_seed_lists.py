#!/usr/bin/env python3
"""Refresh the bundled MIT seed lexicon during explicit skill maintenance."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


RAW_BASE = "https://raw.githubusercontent.com/nanxstats/llm-cliches/main"
FILES = ("adjectives", "nouns", "verbs")
SOURCE = "nanxstats/llm-cliches"


def fetch_words(name: str, timeout: float) -> list[str]:
    url = f"{RAW_BASE}/{name}.txt"
    request = Request(url, headers={"User-Agent": "writing-cleanup-maintenance/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            content = response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as error:
        raise RuntimeError(f"could not fetch {url}: {error}") from error
    return sorted({line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write references/seed-lexicon.tsv.")
    parser.add_argument("--output", type=Path, default=Path("references/seed-lexicon.tsv"))
    parser.add_argument("--timeout", type=float, default=20.0)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    try:
        values = {name: fetch_words(name, arguments.timeout) for name in FILES}
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    rows = ["# category\tterm\tsource\tlicense\trole"]
    for category, words in values.items():
        for word in words:
            rows.append(f"{category[:-1]}\t{word}\t{SOURCE}\tMIT\tcandidate")
    if arguments.write:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text("\n".join(rows) + "\n", encoding="utf-8")
        print(f"wrote {arguments.output} ({sum(len(words) for words in values.values())} entries)")
    else:
        for name, words in values.items():
            print(f"{name}: {len(words)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
