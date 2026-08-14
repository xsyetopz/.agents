"""Translate Apple's HIG DocC JSON into ordinary Markdown references.

The command-line orchestration remains in this compatibility module.  Source
retrieval and Markdown rendering live in sibling modules so callers can reuse
those cohesive pieces without importing the CLI implementation itself.  The
imports below intentionally re-export the historical helper names.
"""

from __future__ import annotations

import argparse
import html
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

try:  # Package imports support namespace-package consumers.
    from .hig_markdown import (
        LINK_PATTERN,
        MEDIA_SUFFIXES,
        absolute_reference_url,
        front_matter,
        inline_markdown,
        markdown_page,
        markdown_table,
        markdown_whats_new,
        reference_urls,
        render_content,
        table_cell,
        title_for,
        topic_sections,
    )
    from .hig_network import (
        CANONICAL_BASE,
        DATA_BASE,
        EXPECTED_UNAVAILABLE,
        HIG_PREFIXES,
        ROOT_IDENTIFIERS,
        USER_AGENT,
        WHATS_NEW_URL,
        HarvestError,
        WhatsNewParser,
        canonical_url,
        child_slugs,
        discover,
        document_slug,
        fetch_json,
        reject_unexpected_failures,
        request_bytes,
        retrieved_date,
        safe_filename,
        walk,
        whats_new_entries,
        whats_new_hig_slugs,
    )
except ImportError:  # Direct ``python3 scripts/harvest_hig.py`` invocation.
    from hig_markdown import (
        LINK_PATTERN,
        MEDIA_SUFFIXES,
        absolute_reference_url,
        front_matter,
        inline_markdown,
        markdown_page,
        markdown_table,
        markdown_whats_new,
        reference_urls,
        render_content,
        table_cell,
        title_for,
        topic_sections,
    )
    from hig_network import (
        CANONICAL_BASE,
        DATA_BASE,
        EXPECTED_UNAVAILABLE,
        HIG_PREFIXES,
        ROOT_IDENTIFIERS,
        USER_AGENT,
        WHATS_NEW_URL,
        HarvestError,
        WhatsNewParser,
        canonical_url,
        child_slugs,
        discover,
        document_slug,
        fetch_json,
        reject_unexpected_failures,
        request_bytes,
        retrieved_date,
        safe_filename,
        walk,
        whats_new_entries,
        whats_new_hig_slugs,
    )

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "references"

__all__ = (
    "CANONICAL_BASE",
    "DATA_BASE",
    "DEFAULT_OUTPUT",
    "EXPECTED_UNAVAILABLE",
    "HIG_PREFIXES",
    "LINK_PATTERN",
    "MEDIA_SUFFIXES",
    "ROOT",
    "ROOT_IDENTIFIERS",
    "USER_AGENT",
    "WHATS_NEW_URL",
    "HarvestError",
    "WhatsNewParser",
    "absolute_reference_url",
    "canonical_url",
    "child_slugs",
    "discover",
    "document_slug",
    "fetch_json",
    "front_matter",
    "harvest",
    "inline_markdown",
    "main",
    "markdown_page",
    "markdown_table",
    "markdown_whats_new",
    "parse_args",
    "parse_front_matter",
    "reference_urls",
    "reject_unexpected_failures",
    "render_content",
    "request_bytes",
    "retrieved_date",
    "safe_filename",
    "table_cell",
    "table_smoke",
    "title_for",
    "topic_sections",
    "validate",
    "walk",
    "whats_new_entries",
    "whats_new_hig_slugs",
)


def parse_front_matter(text: str) -> dict[str, str]:
    """Parse the small YAML-compatible metadata header emitted by the harvester."""

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


def harvest(args: argparse.Namespace) -> int:
    """Fetch live HIG documents and atomically replace the reference directory."""

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


def validate(args: argparse.Namespace) -> int:
    """Validate generated references against the currently discoverable HIG set."""

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
    """Exercise representative table, media, and footnote renderings."""

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
        print(f"error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
