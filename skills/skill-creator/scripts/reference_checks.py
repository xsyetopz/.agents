"""Reference, path-safety, and Markdown checks for a copied skill package."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})", re.MULTILINE)
REL_REF_RE = re.compile(
    r"(?<![A-Za-z0-9_./])((?:\./)?(?:references|assets|scripts)/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)"
)
# Keep the captured target separate from optional Markdown link titles.  This is
# deliberately not a full Markdown parser; it is a conservative integrity check.
MARKDOWN_LINK_RE = re.compile(
    r"\[[^\]]*\]\(\s*(?!(?i:https?://|ftp://|//|#|mailto:))([^\s)]+)"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)(?:\s*\{#[^\}]+\})?\s*$")
CHANGELOG_VERSION_RE = re.compile(r"^##\s+\[[\d.]+(?:-[^\]]+)?\]")

# Build path fragments rather than embedding a host-specific absolute path.
GLOBAL_PATH_RE = re.compile(
    r"(?ix)(?<![A-Za-z0-9_])"
    r"(?:/(?:Users|home|root)(?:[/\\][^\s`'\"<>)]*)?"
    r"|/(?:private/)?tmp(?:[/\\][^\s`'\"<>)]*)?"
    r"|(?:~|\$HOME)(?:[/\\][^\s`'\"<>)]*)+"
    r"|[A-Za-z]:[/\\](?:Users|home|\.agents|\.codex)[/\\][^\s`'\"<>)]*)"
)


def strip_fenced_blocks(text: str) -> str:
    result: list[str] = []
    in_fence: str | None = None
    for line in text.splitlines(keepends=True):
        if in_fence is None:
            match = FENCE_RE.match(line)
            if match:
                in_fence = match.group(1)[0]
                result.append("\n")
            else:
                result.append(line)
        else:
            match = FENCE_RE.match(line)
            if match and match.group(1)[0] == in_fence and len(match.group(1)) >= 3:
                in_fence = None
                result.append("\n")
    return "".join(result)


def _clean_link_target(raw: str) -> str:
    """Normalize a local Markdown target without interpreting shell syntax."""
    target = unquote(raw.strip()).split("#", 1)[0]
    # A query is not meaningful for a local file and commonly appears in links
    # copied from web pages. Keep query-bearing links as the path before it.
    target = target.split("?", 1)[0]
    return target.rstrip(".,;:!?)]}")


def _is_official_snapshot(path: Path, root: Path) -> bool:
    """Return whether ``path`` is an official docs snapshot in this package."""
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False
    return len(relative.parts) >= 3 and relative.parts[:2] == (
        "references",
        "official",
    )


def _check_local_reference(
    raw: str,
    source: Path,
    root: Path,
    errors: list[str],
    *,
    label: str,
    allow_website_root: bool = False,
) -> None:
    rel = _clean_link_target(raw)
    if not rel:
        return
    # Markdown links may contain angle brackets around paths with spaces. The
    # short regex does not capture those, but stripping here keeps diagnostics
    # useful for direct calls to this helper.
    rel = rel.strip("<>")
    # Official snapshots use website-root paths such as ``/llms.txt``. They are
    # external documentation paths, not files at the root of a copied skill.
    if (
        allow_website_root
        and rel.startswith("/")
        and not rel.startswith("//")
        and ".." not in Path(rel).parts
    ):
        return
    try:
        target = (source / rel).resolve()
    except (OSError, RuntimeError) as exc:
        errors.append(f"Unable to resolve relative reference in {label}: {raw}: {exc}")
        return
    try:
        target.relative_to(root.resolve())
    except ValueError:
        errors.append(f"Relative reference leaves skill root in {label}: {raw}")
        return
    if not target.exists():
        errors.append(f"Broken relative reference in {label}: {raw}")


def check_broken_references(text: str, root: Path, errors: list[str]) -> None:
    unfenced = strip_fenced_blocks(text)
    refs = set(REL_REF_RE.findall(unfenced))
    refs.update(MARKDOWN_LINK_RE.findall(unfenced))
    for relative in sorted(refs):
        _check_local_reference(relative, root, root, errors, label="SKILL.md")


def check_markdown_links(root: Path, errors: list[str], warnings: list[str]) -> None:
    for markdown in sorted(root.rglob("*.md")):
        try:
            text = markdown.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(
                f"Unable to read Markdown file {markdown.relative_to(root)}: {exc}"
            )
            continue
        for link in MARKDOWN_LINK_RE.findall(strip_fenced_blocks(text)):
            clean = _clean_link_target(link)
            if not clean:
                continue
            _check_local_reference(
                clean,
                markdown.parent,
                root,
                errors,
                label=str(markdown.relative_to(root)),
                allow_website_root=_is_official_snapshot(markdown, root),
            )


def _iter_text_files(root: Path):
    """Yield package text files without following links outside ``root``."""
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "\x00" in text:
            continue
        yield path, text


def check_global_path_references(root: Path, errors: list[str]) -> None:
    """Reject host-specific paths that would break a copied skill package."""
    for path, text in _iter_text_files(root):
        for line_no, line in enumerate(text.splitlines(), 1):
            match = GLOBAL_PATH_RE.search(line)
            if match:
                errors.append(
                    "Global/host-specific path in "
                    f"{path.relative_to(root)}:{line_no}: {match.group(0)!r}"
                )


def check_duplicate_entrypoints(root: Path, errors: list[str]) -> None:
    """Allow exactly one case-sensitive ``SKILL.md`` at the skill root."""
    entrypoints = [
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and path.name.casefold() == "skill.md"
    ]
    nested = sorted(path for path in entrypoints if path.parts != ("SKILL.md",))
    if nested:
        errors.append(
            "Duplicate SKILL.md entrypoint(s) nested under skill root: "
            + ", ".join(map(str, nested))
        )


def check_symlink_containment(root: Path, errors: list[str]) -> None:
    """Reject symlinks resolving outside the copied package."""
    root_resolved = root.resolve()
    for path in sorted(root.rglob("*")):
        if not path.is_symlink():
            continue
        try:
            resolved = path.resolve()
        except (OSError, RuntimeError) as exc:
            errors.append(f"Unable to resolve symlink {path.relative_to(root)}: {exc}")
            continue
        try:
            resolved.relative_to(root_resolved)
        except ValueError:
            errors.append(
                f"Symlink leaves skill root: {path.relative_to(root)} -> {resolved}"
            )


def check_duplicate_headers(root: Path, errors: list[str]) -> None:
    for markdown in sorted(root.rglob("*.md")):
        try:
            text = markdown.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(
                f"Unable to read Markdown file {markdown.relative_to(root)}: {exc}"
            )
            continue
        seen: dict[tuple[str, ...], int] = {}
        parents: dict[int, str] = {}
        relative = markdown.relative_to(root)

        # Changelogs and worked examples intentionally repeat headers.
        is_changelog = relative.name == "CHANGELOG.md"
        is_worked_examples = "worked-examples" in relative.name.lower()
        official = _is_official_snapshot(markdown, root)
        official_title: str | None = None

        for line_no, line in enumerate(strip_fenced_blocks(text).splitlines(), 1):
            match = HEADING_RE.match(line.strip())
            if not match:
                continue
            heading = match.group(0).strip()
            level = len(match.group(1))
            title = match.group(2).strip()

            if official and level == 1 and official_title is None:
                official_title = title
            if is_changelog and CHANGELOG_VERSION_RE.match(heading):
                continue
            if is_worked_examples and heading.startswith("###"):
                continue

            for child_level in tuple(parents):
                if child_level >= level:
                    del parents[child_level]
            identity = tuple(
                parents[parent_level]
                for parent_level in sorted(parents)
                if parent_level < level
            ) + (f"h{level}:{title}",)

            if identity in seen:
                # Dated docs snapshots can repeat their page title; non-title
                # headings remain subject to the normal duplicate check.
                if not (official and level == 1 and title == official_title):
                    errors.append(
                        f"Duplicate heading in {relative}:{line_no}: {heading!r} "
                        f"(first at line {seen[identity]})"
                    )
            else:
                seen[identity] = line_no
            parents[level] = title


def warn_missing_license(root: Path, warnings: list[str]) -> None:
    if not (root / "LICENSE").exists():
        warnings.append("No LICENSE file is present.")


__all__ = [
    "GLOBAL_PATH_RE",
    "HEADING_RE",
    "MARKDOWN_LINK_RE",
    "REL_REF_RE",
    "check_broken_references",
    "check_duplicate_entrypoints",
    "check_duplicate_headers",
    "check_global_path_references",
    "check_markdown_links",
    "check_symlink_containment",
    "strip_fenced_blocks",
    "warn_missing_license",
]
