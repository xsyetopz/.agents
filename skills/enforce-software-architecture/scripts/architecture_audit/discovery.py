"""File discovery and filename normalization."""

from __future__ import annotations

import fnmatch
import os
import re
from collections.abc import Iterable, Sequence
from pathlib import Path

from .rules import (
    ARCHITECTURE_EXTENSIONS,
    DEFAULT_IGNORED_DIRS,
    GENERATED_HEADER,
    GENERATED_NAME_PATTERNS,
    GO_ARCH_MARKERS,
    GO_OS_MARKERS,
    KOTLIN_PLATFORM_MARKERS,
    RESERVED_FILES,
    RESERVED_PATTERNS,
)


def matches_any(path: Path, root: Path, patterns: Sequence[str]) -> bool:
    relative = path.relative_to(root).as_posix()
    return any(fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(path.name, pattern) for pattern in patterns)


def iter_audited_files(root: Path, excludes: Sequence[str]) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        base = Path(current)
        dirs[:] = [name for name in dirs if name not in DEFAULT_IGNORED_DIRS and not matches_any(base / name, root, excludes)]
        for name in files:
            path = base / name
            extensionless_script = False
            if not path.suffix:
                try:
                    with path.open("rb") as handle:
                        extensionless_script = handle.read(2) == b"#!"
                except OSError:
                    pass
            if (path.suffix.lower() in ARCHITECTURE_EXTENSIONS or extensionless_script or name.lower() in RESERVED_FILES or any(fnmatch.fnmatch(name.lower(), pattern) for pattern in RESERVED_PATTERNS)) and not matches_any(path, root, excludes):
                yield path


def count_lines(path: Path) -> int:
    with path.open("rb") as handle:
        return sum(1 for _ in handle)


def artifact_class(path: Path, root: Path) -> str | None:
    name = path.name.lower()
    if name in RESERVED_FILES or any(fnmatch.fnmatch(name, pattern) for pattern in RESERVED_PATTERNS):
        return "framework"
    if any(fnmatch.fnmatch(name, pattern) for pattern in GENERATED_NAME_PATTERNS):
        return "generated"
    try:
        header = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:5]
    except OSError:
        return None
    return "generated" if any(GENERATED_HEADER.search(line) for line in header) else None


def normalized_leaf(path: Path) -> str:
    suffix = path.suffix
    leaf = path.name[:-len(suffix)] if suffix else path.name
    ext = suffix.lower()
    lowered = leaf.lower()
    if ext in {".cts", ".mts", ".ts"}:
        for marker in (".test-d", ".spec-d", ".test", ".spec", "_test", "_spec", ".d"):
            if lowered.endswith(marker):
                leaf, lowered = leaf[:-len(marker)], lowered[:-len(marker)]
                break
    elif ext in {".cjs", ".js", ".jsx", ".mjs", ".tsx"}:
        for marker in (".test", ".spec", "_test", "_spec"):
            if lowered.endswith(marker):
                leaf, lowered = leaf[:-len(marker)], lowered[:-len(marker)]
                break
    elif ext in {".py", ".pyi", ".pyw"}:
        if lowered.startswith("test_"):
            leaf, lowered = leaf[5:], lowered[5:]
        elif lowered.endswith("_test"):
            leaf, lowered = leaf[:-5], lowered[:-5]
    elif (ext == ".rb" and lowered.endswith(("_spec", "_test"))) or (ext in {".dart", ".exs"} and lowered.endswith("_test")):
        leaf, lowered = leaf[:-5], lowered[:-5]
    elif ext == ".rs" and lowered.endswith("_tests"):
        leaf, lowered = leaf[:-6], lowered[:-6]
    elif ext == ".go":
        if lowered.endswith("_test"):
            leaf, lowered = leaf[:-5], lowered[:-5]
        parts = leaf.split("_")
        lowered_parts = [part.lower() for part in parts]
        if len(parts) >= 3 and lowered_parts[-2] in GO_OS_MARKERS and lowered_parts[-1] in GO_ARCH_MARKERS:
            leaf = "_".join(parts[:-2])
        elif len(parts) >= 2 and lowered_parts[-1] in GO_OS_MARKERS | GO_ARCH_MARKERS:
            leaf = "_".join(parts[:-1])
    elif ext in {".kt", ".kts"}:
        parts = re.split(r"([._])", leaf)
        if len(parts) >= 3 and parts[-1].lower() in KOTLIN_PLATFORM_MARKERS and parts[-2] in {".", "_"}:
            leaf = "".join(parts[:-2])
    if ext in {".cs", ".fs", ".fsi", ".fsx", ".java", ".kt", ".kts", ".php", ".scala", ".swift"}:
        match = re.search(r"(?:Tests?|Specs?)$", leaf)
        if match and match.start() > 0:
            leaf = leaf[:match.start()]
    return leaf


def semantic_tokens(path: Path) -> tuple[str, ...]:
    return tuple(token.lower() for token in re.split(r"[-_.]+", normalized_leaf(path)) if token)


def split_semantic_words(value: str) -> tuple[str, ...]:
    words: list[str] = []
    for token in (part for part in re.split(r"[-_.]+", value) if part):
        parts = re.findall(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+", token, re.ASCII)
        words.extend(part.lower() for part in (parts or [token]))
    return tuple(words)


def semantic_words(path: Path) -> tuple[str, ...]:
    return split_semantic_words(normalized_leaf(path))
