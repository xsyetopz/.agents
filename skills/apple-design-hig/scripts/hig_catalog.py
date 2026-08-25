#!/usr/bin/env python3
"""Fetch the live Apple HIG catalog or one topic as concise Markdown/JSON.

The HIG UI is JavaScript-rendered. Apple publishes the same documentation data
under /tutorials/data, which this helper reads without third-party packages.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterator
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = (
    "https://developer.apple.com/tutorials/data/design/human-interface-guidelines"
)
CANONICAL_BASE_URL = "https://developer.apple.com/design/human-interface-guidelines"
HIG_PREFIX = "doc://com.apple.HIG/design/Human-Interface-Guidelines/"
HIG_PREFIX_LOWER = "doc://com.apple.HIG/design/human-interface-guidelines/"
ROOT_IDENTIFIER = "doc://com.apple.HIG/design/human-interface-guidelines"


def fetch_json(base_url: str, slug: str, timeout: float) -> dict:
    normalized_base = base_url.rstrip("/")
    url = (
        f"{normalized_base}.json"
        if not slug
        else f"{normalized_base}/{slug.strip('/')}.json"
    )
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "apple-design-hig/1.0 (Codex skill)",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"Apple HIG request failed ({error.code}): {url}") from error
    except URLError as error:
        raise RuntimeError(
            f"Apple HIG request could not reach {url}: {error.reason}"
        ) from error
    except TimeoutError as error:
        raise RuntimeError(f"Apple HIG request timed out: {url}") from error
    if not isinstance(payload, dict):
        raise TypeError(f"Apple HIG returned a non-object JSON payload: {url}")
    return payload


def walk(value: object) -> Iterator[dict]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def hig_identifier(value: object) -> bool:
    return isinstance(value, str) and (
        value == ROOT_IDENTIFIER or value.startswith((HIG_PREFIX, HIG_PREFIX_LOWER))
    )


def slug_from_identifier(identifier: str) -> str:
    if identifier == ROOT_IDENTIFIER:
        return ""
    for prefix in (HIG_PREFIX, HIG_PREFIX_LOWER):
        if identifier.startswith(prefix):
            return identifier.removeprefix(prefix).split("#", 1)[0]
    return identifier.split("#", 1)[0]


def topic_records(payload: dict) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    for node in walk(payload):
        identifier = node.get("identifier")
        if not isinstance(identifier, str) or not hig_identifier(identifier):
            continue
        slug = slug_from_identifier(identifier)
        record = records.setdefault(slug, {"slug": slug})
        title = node.get("title")
        if isinstance(title, str) and title:
            record["title"] = title
        abstract = node.get("abstract")
        if isinstance(abstract, list):
            text = "".join(
                part.get("text", "")
                for part in abstract
                if isinstance(part, dict) and isinstance(part.get("text"), str)
            )
            if text:
                record["abstract"] = text
    return records


def child_slugs(payload: dict) -> list[str]:
    result: list[str] = []
    for section in payload.get("topicSections", []):
        if not isinstance(section, dict):
            continue
        for identifier in section.get("identifiers", []):
            if not isinstance(identifier, str) or not hig_identifier(identifier):
                continue
            slug = slug_from_identifier(identifier)
            if slug and slug not in result:
                result.append(slug)
    return result


def slug_title(payload: dict, fallback: str) -> str:
    metadata = payload.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("title"), str):
        return metadata["title"]
    title = payload.get("title")
    return title if isinstance(title, str) else fallback.replace("-", " ").title()


def fetch_catalog(
    base_url: str, timeout: float, deep: bool
) -> tuple[dict[str, dict[str, str]], list[str]]:
    records: dict[str, dict[str, str]] = {}
    queue = [""]
    visited: set[str] = set()
    section_slugs: list[str] = []

    while queue:
        slug = queue.pop(0)
        if slug in visited:
            continue
        visited.add(slug)
        payload = fetch_json(base_url, slug, timeout)
        records.update({**records, **topic_records(payload)})
        children = child_slugs(payload)
        if slug == "":
            section_slugs = children
            queue.extend(children)
        elif deep:
            queue.extend(children)
    return records, section_slugs


def canonical_url(slug: str) -> str:
    return f"{CANONICAL_BASE_URL}/{slug}" if slug else f"{CANONICAL_BASE_URL}/"


def print_catalog(
    records: dict[str, dict[str, str]], sections: list[str], retrieved: str
) -> None:
    print(f"# Apple HIG catalog\n\nRetrieved: {retrieved}\n")
    print(f"Source: {CANONICAL_BASE_URL}/\n")
    section_set = set(sections)
    for slug, record in sorted(records.items()):
        if not slug:
            continue
        if slug not in section_set:
            continue
        title = record.get("title", slug.replace("-", " ").title())
        print(f"- **{title}** - `{slug}` - {canonical_url(slug)}")
    extras = [
        record for slug, record in records.items() if slug not in section_set and slug
    ]
    if extras:
        print("\n## Discovered topics\n")
        for record in sorted(extras, key=lambda item: item.get("title", item["slug"])):
            slug = record["slug"]
            title = record.get("title", slug.replace("-", " ").title())
            abstract = f" - {record['abstract']}" if record.get("abstract") else ""
            print(f"- **{title}** - `{slug}`{abstract}\n  {canonical_url(slug)}")


def print_topic(payload: dict, slug: str, retrieved: str) -> None:
    title = slug_title(payload, slug)
    records = topic_records(payload).get(slug, {})
    print(f"# {title}\n\nRetrieved: {retrieved}\n\n{canonical_url(slug)}\n")
    if records.get("abstract"):
        print(f"{records['abstract']}\n")
    sections = payload.get("primaryContentSections", [])
    headings: list[str] = []
    for node in walk(sections):
        if node.get("type") == "heading" and isinstance(node.get("text"), str):
            headings.append(node["text"])
    if headings:
        print("## Page headings\n")
        for heading in dict.fromkeys(headings):
            print(f"- {heading}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--all", action="store_true", help="Print the current HIG catalog (default)."
    )
    group.add_argument(
        "--topic",
        metavar="SLUG",
        help="Print one live HIG topic, such as foundations or motion.",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Follow nested topic collections while building --all; may make many requests.",
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON for --all."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=argparse.SUPPRESS)
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="HTTP timeout in seconds (default: 20).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    retrieved = datetime.now(timezone.utc).date().isoformat()
    try:
        if args.topic:
            payload = fetch_json(args.base_url, args.topic, args.timeout)
            if args.json:
                print(json.dumps(payload, indent=2, ensure_ascii=False))
            else:
                print_topic(payload, args.topic, retrieved)
            return 0
        records, sections = fetch_catalog(args.base_url, args.timeout, args.deep)
        if args.json:
            print(
                json.dumps(
                    {"retrieved": retrieved, "sections": sections, "topics": records},
                    indent=2,
                    ensure_ascii=False,
                )
            )
        else:
            print_catalog(records, sections, retrieved)
        return 0
    except (RuntimeError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
