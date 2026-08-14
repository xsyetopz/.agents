"""Markdown rendering helpers for Apple HIG DocC payloads."""

from __future__ import annotations

import json
import re
from typing import Any, cast
from urllib.parse import urljoin, urlparse

try:
    from .hig_network import WHATS_NEW_URL, canonical_url
except ImportError:  # Direct ``python3 scripts/harvest_hig.py`` invocation.
    from hig_network import (
        WHATS_NEW_URL,
        canonical_url,
    )

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
LINK_PATTERN = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)(?:\s+[^)]*)?\)")


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


def topic_sections(
    payload: dict[str, Any],
    references: dict[str, Any],
    preceding: list[str] | None = None,
) -> list[str]:
    """Render topic sections while omitting adjacent generated duplicates.

    Apple’s DocC payloads can expose the same ordered links as both a primary
    ``links`` block and a ``Topics`` section.  Keep the first block as the
    source-shaped content and suppress only an immediately adjacent, exact
    duplicate ``Topics`` list.  Other topic sections and unique links remain
    untouched.  ``preceding`` is optional to preserve the historical helper
    API for callers that render topic sections independently.
    """
    output: list[str] = []
    previous = list(preceding or [])
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
            if anchor.casefold() == "topics" and previous[-len(links) :] == links:
                continue
            output.extend([f"## {anchor}", *links])
            previous.extend([f"## {anchor}", *links])
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
    raw_references = payload.get("references")
    refs: dict[str, Any] = (
        cast(dict[str, Any], raw_references)
        if isinstance(raw_references, dict)
        else {}
    )
    abstract = inline_markdown(payload.get("abstract"), refs)
    body = render_content(payload.get("primaryContentSections"), refs)
    content = [f"# {title}"]
    if abstract:
        content.extend([abstract])
    content.extend(body)
    content.extend(topic_sections(payload, refs, body))
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
