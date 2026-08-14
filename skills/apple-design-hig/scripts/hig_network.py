"""Apple HIG source retrieval and document discovery helpers.

This module intentionally contains no command-line handling.  The historical
``harvest_hig`` module re-exports these helpers so direct imports continue to
work while the CLI stays small.
"""

from __future__ import annotations

import json
import re
import time
from collections import deque
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

CANONICAL_BASE = "https://developer.apple.com/design/human-interface-guidelines"
DATA_BASE = (
    "https://developer.apple.com/tutorials/data/design/human-interface-guidelines"
)
WHATS_NEW_URL = "https://developer.apple.com/design/whats-new/"
HIG_PREFIXES = (
    "doc://com.apple.HIG/design/Human-Interface-Guidelines/",
    "doc://com.apple.HIG/design/human-interface-guidelines/",
)
ROOT_IDENTIFIERS = {
    "doc://com.apple.HIG/design/human-interface-guidelines",
    "doc://com.apple.HIG/design/Human-Interface-Guidelines",
}
USER_AGENT = "apple-design-hig-markdown/2.0 (Codex skill)"
EXPECTED_UNAVAILABLE = {"messages-for-business", "navigation-bars", "touch-bar"}
FILENAME_OVERRIDES = {"patterns": "pattern-catalog"}


class HarvestError(RuntimeError):
    """An Apple source could not be collected or interpreted."""


def retrieved_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def request_bytes(url: str, timeout: float) -> bytes:
    request = Request(
        url, headers={"Accept": "application/json, text/html", "User-Agent": USER_AGENT}
    )
    last_error: HarvestError | None = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=timeout) as response:
                return response.read()
        except HTTPError as error:
            last_error = HarvestError(f"HTTP {error.code}: {url}")
            if 400 <= error.code < 500 and error.code not in {408, 429}:
                break
        except URLError as error:
            last_error = HarvestError(f"request failed for {url}: {error.reason}")
        except TimeoutError:
            last_error = HarvestError(f"request timed out: {url}")
        if attempt < 2:
            time.sleep(0.5 * (attempt + 1))
    raise last_error or HarvestError(f"request failed for {url}")


def document_slug(identifier: Any) -> str | None:
    if not isinstance(identifier, str):
        return None
    identifier = identifier.split("#", 1)[0]
    if identifier in ROOT_IDENTIFIERS:
        return ""
    for prefix in HIG_PREFIXES:
        if identifier.startswith(prefix):
            return identifier.removeprefix(prefix).strip("/")
    return None


def canonical_url(slug: str) -> str:
    return f"{CANONICAL_BASE}/" if not slug else f"{CANONICAL_BASE}/{slug}"


def safe_filename(slug: str) -> str:
    normalized = slug.strip("/")
    name = (
        "index"
        if not normalized
        else FILENAME_OVERRIDES.get(normalized, normalized.replace("/", "--"))
    )
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*(?:--[a-z0-9][a-z0-9-]*)*", name):
        raise HarvestError(f"unsafe HIG slug: {slug!r}")
    return f"{name}.md"


def fetch_json(slug: str, timeout: float, data_base: str = DATA_BASE) -> dict[str, Any]:
    suffix = f"/{slug.strip('/')}" if slug else ""
    url = f"{data_base.rstrip('/')}{suffix}.json"
    try:
        payload = json.loads(request_bytes(url, timeout).decode("utf-8"))
    except json.JSONDecodeError as error:
        raise HarvestError(f"invalid JSON: {url}") from error
    if not isinstance(payload, dict):
        raise HarvestError(f"non-object JSON document: {url}")
    actual = (
        document_slug((payload.get("identifier") or {}).get("url"))
        if isinstance(payload.get("identifier"), dict)
        else None
    )
    requested = slug.strip("/")
    if actual != requested:
        raise HarvestError(f"{requested or '<root>'} redirects to {actual!r}")
    return payload


def walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def child_slugs(payload: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for node in walk(payload.get("topicSections", [])):
        slug = document_slug(node.get("identifier"))
        if slug:
            result.add(slug)
    for identifier in payload.get("references") or {}:
        slug = document_slug(identifier)
        if slug:
            result.add(slug)
    return result


class WhatsNewParser(HTMLParser):
    """Read only Apple's dated topic rows, excluding site navigation."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.row: dict[str, str] | None = None
        self.capture: str | None = None
        self.entries: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        classes = set((values.get("class") or "").split())
        if tag == "tr" and "topic-item" in classes:
            self.row = {
                "title": "",
                "url": "",
                "date": "",
                "type": "",
                "description": "",
            }
        elif self.row is not None and tag == "a" and values.get("href"):
            self.row["url"] = urljoin(WHATS_NEW_URL, values["href"] or "")
            self.capture = "title"
        elif self.row is not None and tag == "p" and "topic-data" in classes:
            self.capture = "type"
        elif self.row is not None and tag == "p" and "topic-date" in classes:
            self.capture = "date"
        elif self.row is not None and "topic-description" in classes:
            self.capture = "description"

    def handle_data(self, data: str) -> None:
        if self.row is not None and self.capture is not None:
            self.row[self.capture] += data

    def handle_endtag(self, tag: str) -> None:
        if self.row is None:
            return
        if tag in {"a", "p", "span"}:
            self.capture = None
        elif tag == "tr":
            entry = {key: " ".join(value.split()) for key, value in self.row.items()}
            entry["type"] = re.sub(
                r"searchterm$", "", entry["type"], flags=re.IGNORECASE
            )
            if entry["title"] and entry["url"]:
                self.entries.append(entry)
            self.row = None


def whats_new_entries(timeout: float) -> list[dict[str, str]]:
    parser = WhatsNewParser()
    parser.feed(request_bytes(WHATS_NEW_URL, timeout).decode("utf-8", errors="replace"))
    return parser.entries


def whats_new_hig_slugs(entries: Iterable[dict[str, str]]) -> set[str]:
    prefix = f"{CANONICAL_BASE}/"
    return {
        entry["url"][len(prefix) :].split("#", 1)[0].strip("/")
        for entry in entries
        if entry["url"].startswith(prefix) and entry["url"] != prefix
    }


def discover(
    timeout: float, workers: int, data_base: str
) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]], set[str]]:
    entries = whats_new_entries(timeout)
    queue: deque[str] = deque([""])
    queue.extend(sorted(whats_new_hig_slugs(entries)))
    documents: dict[str, dict[str, Any]] = {}
    failures: set[str] = set()
    while queue:
        batch: list[str] = []
        while queue and len(batch) < workers:
            slug = queue.popleft()
            if slug not in documents and slug not in failures and slug not in batch:
                batch.append(slug)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(fetch_json, slug, timeout, data_base): slug
                for slug in batch
            }
            for future in as_completed(futures):
                slug = futures[future]
                try:
                    documents[slug] = future.result()
                except HarvestError:
                    if slug:
                        failures.add(slug)
                    else:
                        raise
        for payload in list(documents.values()):
            for slug in child_slugs(payload):
                if slug not in documents and slug not in failures and slug not in queue:
                    queue.append(slug)
    return documents, entries, failures


def reject_unexpected_failures(failures: set[str]) -> None:
    unexpected = failures - EXPECTED_UNAVAILABLE
    if unexpected:
        raise HarvestError(f"live HIG fetches failed: {', '.join(sorted(unexpected))}")
