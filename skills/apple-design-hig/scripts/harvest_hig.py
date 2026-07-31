#!/usr/bin/env python3
"""Translate Apple's HIG DocC JSON into ordinary Markdown references."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
import time
from collections import deque
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
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
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "references"
MEDIA_SUFFIXES = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".mp4",
    ".mov",
    ".m4v",
    ".wav",
    ".mp3",
)
EXPECTED_UNAVAILABLE = {"messages-for-business", "navigation-bars", "touch-bar"}
LINK_PATTERN = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)(?:\s+[^)]*)?\)")


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
    name = "index" if not slug else slug.strip("/").replace("/", "--")
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


def absolute_reference_url(url: str) -> str:
    return urljoin("https://developer.apple.com", url)


def inline_markdown(items: Any, references: dict[str, Any]) -> str:
    if not isinstance(items, list):
        return ""
    parts: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        kind = item.get("type")
        if kind == "text":
            parts.append(str(item.get("text", "")))
        elif kind in {"strong", "emphasis", "strikethrough", "codeVoice"}:
            text = inline_markdown(item.get("inlineContent"), references)
            if kind == "codeVoice" and not text and isinstance(item.get("code"), str):
                text = item["code"]
            marker = {
                "strong": "**",
                "emphasis": "*",
                "strikethrough": "~~",
                "codeVoice": "`",
            }[kind]
            parts.append(f"{marker}{text}{marker}" if text else "")
        elif kind in {"reference", "link"}:
            identifier = (
                item.get("identifier") or item.get("destination") or item.get("url")
            )
            reference = (
                references.get(identifier, {}) if isinstance(identifier, str) else {}
            )
            text = (
                inline_markdown(item.get("inlineContent"), references)
                or inline_markdown(item.get("overridingTitleInlineContent"), references)
                or inline_markdown(item.get("titleInlineContent"), references)
                or str(item.get("text", ""))
                or (reference.get("title", "") if isinstance(reference, dict) else "")
            )
            url = item.get("url") or (
                reference.get("url") if isinstance(reference, dict) else ""
            )
            if isinstance(url, str) and url:
                parts.append(f"[{text or url}]({absolute_reference_url(url)})")
            elif text:
                parts.append(text)
        elif kind in {"image", "video", "audio"}:
            identifier = item.get("identifier")
            reference = (
                references.get(identifier, {}) if isinstance(identifier, str) else {}
            )
            alt = item.get("alt") or (
                reference.get("alt") if isinstance(reference, dict) else ""
            )
            metadata = item.get("metadata")
            caption = (
                inline_markdown(metadata.get("abstract"), references)
                if isinstance(metadata, dict)
                else ""
            )
            alt_text = str(alt).strip() if alt else ""
            caption_text = caption.strip()
            description_parts = [alt_text] if alt_text else []
            if caption_text and caption_text.casefold() != alt_text.casefold():
                description_parts.append(caption_text)
            description = " ".join(description_parts)
            if description:
                label = {
                    "image": "Image description",
                    "video": "Video description",
                    "audio": "Audio description",
                }[kind]
                parts.append(f"*{label}: {description}*")
        else:
            nested = inline_markdown(item.get("inlineContent"), references)
            if nested:
                parts.append(nested)
            elif isinstance(item.get("text"), str):
                parts.append(item["text"])
    return "".join(parts).strip()


def table_cell(value: Any, references: dict[str, Any]) -> str:
    if isinstance(value, list):
        return " ".join(filter(None, (table_cell(item, references) for item in value)))
    if not isinstance(value, dict):
        return ""
    if isinstance(value.get("inlineContent"), list):
        return inline_markdown(value["inlineContent"], references)
    return " ".join(
        filter(
            None,
            (
                table_cell(value.get(key), references)
                for key in ("content", "items", "columns", "tabs")
            ),
        )
    )


def markdown_table(rows: Any, references: dict[str, Any]) -> str:
    if not isinstance(rows, list):
        return ""
    rendered: list[list[str]] = []
    for row in rows:
        cells = row.get("cells") if isinstance(row, dict) else row
        if isinstance(cells, list):
            values = [
                table_cell(cell, references).replace("|", "\\|").replace("\n", "<br>")
                for cell in cells
            ]
            if any(values):
                rendered.append(values)
    if not rendered:
        return ""
    width = max(len(row) for row in rendered)
    rows = [row + [""] * (width - len(row)) for row in rendered]
    output = [f"| {' | '.join(rows[0])} |", f"| {' | '.join('---' for _ in rows[0])} |"]
    output.extend(f"| {' | '.join(row)} |" for row in rows[1:])
    return "\n".join(output)


def render_content(
    nodes: Any, references: dict[str, Any], indent: int = 0
) -> list[str]:
    if not isinstance(nodes, list):
        return []
    output: list[str] = []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        kind = node.get("type")
        if kind == "heading":
            text = str(node.get("text", "")).strip()
            if text:
                output.append(
                    f"{'#' * min(6, max(2, int(node.get('level', 2))))} {text}"
                )
        elif kind == "paragraph":
            text = inline_markdown(node.get("inlineContent"), references)
            if text:
                output.append(text)
        elif kind == "small":
            text = inline_markdown(node.get("inlineContent"), references)
            if text:
                output.append(f"*{text}*")
        elif kind == "table":
            table = markdown_table(node.get("rows"), references)
            if table:
                output.append(table)
        elif kind == "links":
            for identifier in node.get("items", []):
                reference = (
                    references.get(identifier, {})
                    if isinstance(identifier, str)
                    else {}
                )
                if not isinstance(reference, dict) or not isinstance(
                    reference.get("url"), str
                ):
                    continue
                title = str(reference.get("title") or reference["url"])
                output.append(
                    f"- [{title}]({absolute_reference_url(reference['url'])})"
                )
        elif kind in {"unorderedList", "orderedList"}:
            marker = "1." if kind == "orderedList" else "-"
            for item in node.get("items", []):
                if not isinstance(item, dict):
                    continue
                content = item.get("content")
                text = (
                    " ".join(
                        inline_markdown(child.get("inlineContent"), references)
                        for child in content or []
                        if isinstance(child, dict) and child.get("type") == "paragraph"
                    )
                    if isinstance(content, list)
                    else inline_markdown(item.get("inlineContent"), references)
                )
                if text:
                    output.append(f"{' ' * indent}{marker} {text}")
                if isinstance(content, list):
                    nested = [
                        child
                        for child in content
                        if isinstance(child, dict)
                        and child.get("type") in {"unorderedList", "orderedList"}
                    ]
                    output.extend(render_content(nested, references, indent + 4))
        elif kind in {"codeListing", "code"}:
            code = node.get("code") or node.get("text")
            if isinstance(code, str) and code.strip():
                language = (
                    node.get("syntax") if isinstance(node.get("syntax"), str) else ""
                )
                output.append(f"```{language}\n{code.strip()}\n```")
        elif kind == "aside":
            text = inline_markdown(node.get("content"), references)
            if text:
                output.append(f"> {text}")
        elif kind in {"video", "audio", "image"}:
            text = inline_markdown([node], references)
            if text:
                output.append(text)
        if kind not in {
            "unorderedList",
            "orderedList",
            "aside",
            "small",
            "table",
            "links",
            "video",
            "audio",
            "image",
        }:
            for key in ("content", "columns", "items", "tabs"):
                output.extend(render_content(node.get(key), references))
    return output


def title_for(payload: dict[str, Any], slug: str) -> str:
    metadata = payload.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("title"), str):
        return metadata["title"]
    return slug.replace("-", " ").title() if slug else "Human Interface Guidelines"


def topic_sections(payload: dict[str, Any], references: dict[str, Any]) -> list[str]:
    output: list[str] = []
    for section in payload.get("topicSections", []):
        if not isinstance(section, dict):
            continue
        anchor = str(section.get("anchor") or "Topics").strip()
        if not anchor:
            continue
        links: list[str] = []
        for identifier in section.get("identifiers", []):
            reference = (
                references.get(identifier, {}) if isinstance(identifier, str) else {}
            )
            if not isinstance(reference, dict) or not isinstance(
                reference.get("url"), str
            ):
                continue
            title = str(reference.get("title") or reference["url"])
            links.append(f"- [{title}]({absolute_reference_url(reference['url'])})")
        if links:
            output.extend([f"## {anchor}", *links])
    return output


def reference_urls(payload: dict[str, Any]) -> list[tuple[str, str]]:
    result: set[tuple[str, str]] = set()
    for reference in (payload.get("references") or {}).values():
        if not isinstance(reference, dict) or not isinstance(reference.get("url"), str):
            continue
        url = absolute_reference_url(reference["url"])
        if urlparse(url).path.lower().endswith(MEDIA_SUFFIXES):
            continue
        result.add((url, str(reference.get("title") or url)))
    return sorted(result)


def front_matter(title: str, source: str, retrieved: str) -> str:
    return "\n".join(
        (
            "---",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"source: {source}",
            f"retrieved: {retrieved}",
            "---",
            "",
        )
    )


def markdown_page(slug: str, payload: dict[str, Any], retrieved: str) -> str:
    title = title_for(payload, slug)
    refs = (
        payload.get("references") if isinstance(payload.get("references"), dict) else {}
    )
    abstract = inline_markdown(payload.get("abstract"), refs)
    body = render_content(payload.get("primaryContentSections"), refs)
    content = [f"# {title}"]
    if abstract:
        content.extend([abstract])
    content.extend(body)
    content.extend(topic_sections(payload, refs))
    rendered = "\n\n".join(content).rstrip()
    linked = set(LINK_PATTERN.findall(rendered))
    extra = [
        (url, title) for url, title in reference_urls(payload) if url not in linked
    ]
    if extra:
        rendered += "\n\n## References\n\n" + "\n".join(
            f"- [{title}]({url})" for url, title in extra
        )
    return front_matter(title, canonical_url(slug), retrieved) + rendered + "\n"


def markdown_whats_new(entries: list[dict[str, str]], retrieved: str) -> str:
    lines = ["# What’s New in Apple Design"]
    for entry in entries:
        metadata = "; ".join(
            value
            for value in (entry["date"], entry["type"], entry["description"])
            if value
        )
        lines.append(
            f"- [{entry['title']}]({entry['url']})"
            + (f" - {metadata}" if metadata else "")
        )
    return (
        front_matter("What’s New in Apple Design", WHATS_NEW_URL, retrieved)
        + "\n\n".join(lines)
        + "\n"
    )


def harvest(args: argparse.Namespace) -> int:
    documents, entries, failures = discover(args.timeout, args.workers, args.data_base)
    reject_unexpected_failures(failures)
    retrieved = retrieved_date()
    output = Path(args.output)
    staging = output.with_name(f".{output.name}.staging")
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True)
    for slug, payload in sorted(documents.items()):
        (staging / safe_filename(slug)).write_text(
            markdown_page(slug, payload, retrieved), encoding="utf-8"
        )
    (staging / "whats-new.md").write_text(
        markdown_whats_new(entries, retrieved), encoding="utf-8"
    )
    if output.exists():
        shutil.rmtree(output)
    staging.rename(output)
    print(
        f"harvested {len(documents)} HIG pages and {len(entries)} What’s New entries into {output}"
    )
    if failures:
        print(
            f"historical/unavailable HIG slugs: {', '.join(sorted(failures))}",
            file=sys.stderr,
        )
    return 0


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip().strip('"')
    return result


def validate(args: argparse.Namespace) -> int:
    try:
        documents, entries, failures = discover(
            args.timeout, args.workers, args.data_base
        )
        reject_unexpected_failures(failures)
    except HarvestError as error:
        print(f"validation unavailable: {error}", file=sys.stderr)
        return 1
    output = Path(args.output)
    expected = {safe_filename(slug) for slug in documents} | {"whats-new.md"}
    actual = {path.name for path in output.glob("*.md")} if output.is_dir() else set()
    errors: list[str] = []
    if expected != actual:
        errors.append(
            f"reference inventory differs (expected {len(expected)}, found {len(actual)})"
        )
    for slug, payload in documents.items():
        path = output / safe_filename(slug)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        metadata = parse_front_matter(text)
        if (
            metadata.get("title") != title_for(payload, slug)
            or metadata.get("source") != canonical_url(slug)
            or not metadata.get("retrieved")
        ):
            errors.append(f"invalid front matter: {path.name}")
    whats_new = output / "whats-new.md"
    if not whats_new.is_file():
        errors.append("missing whats-new.md")
    else:
        text = whats_new.read_text(encoding="utf-8")
        metadata = parse_front_matter(text)
        count = sum(line.startswith("- [") for line in text.splitlines())
        if metadata.get("source") != WHATS_NEW_URL or count != len(entries):
            errors.append(
                f"What's New mismatch (expected {len(entries)}, found {count})"
            )
    for path in output.glob("*.md") if output.is_dir() else []:
        text = path.read_text(encoding="utf-8")
        for line_number, target in enumerate(LINK_PATTERN.findall(text), 1):
            parsed = urlparse(html.unescape(target))
            if not parsed.scheme and not target.startswith("#"):
                errors.append(f"relative link in {path.name}:{line_number}: {target}")
            if parsed.scheme and parsed.scheme not in {"http", "https", "mailto"}:
                errors.append(
                    f"unsupported link in {path.name}:{line_number}: {target}"
                )
    if errors:
        print("validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(
        f"validated {len(actual)} Markdown references against {len(documents)} live HIG pages and {len(entries)} What's New entries"
    )
    if failures:
        print(f"historical/unavailable HIG slugs: {', '.join(sorted(failures))}")
    return 0


def table_smoke(args: argparse.Namespace) -> int:
    checks = {
        "app-icons": ("| Platform |", "1024x1024 px"),
        "accessibility": ("| Platform |", "17 pt"),
        "buttons": ("Image description:", "Idle"),
        "researchkit": ("legal advice",),
        "playing-haptics": ("**Success.**",),
    }
    for slug, required in checks.items():
        rendered = markdown_page(
            slug, fetch_json(slug, args.timeout, args.data_base), "smoke-test"
        )
        missing = [text for text in required if text not in rendered]
        if missing:
            print(f"table smoke failed for {slug}: {missing}", file=sys.stderr)
            return 1
    print("table smoke passed for tables, media captions, and footnotes")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("harvest", "validate", "table-smoke"):
        command = commands.add_parser(name)
        command.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
        command.add_argument("--timeout", type=float, default=30.0)
        command.add_argument("--workers", type=int, default=8)
        command.add_argument("--data-base", default=DATA_BASE, help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "harvest":
            return harvest(args)
        if args.command == "validate":
            return validate(args)
        return table_smoke(args)
    except HarvestError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
