"""File discovery and filename normalization."""

from __future__ import annotations

import fnmatch
import os
import re
import subprocess
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
    SOURCE_BEARING_CONFIG_EXTENSIONS,
    SOURCE_BEARING_DIRECTORIES,
    SOURCE_BEARING_IDL_EXTENSIONS,
    SOURCE_EXTENSIONS,
)

OUTPUT_DIRECTORIES = {
    "artifacts",
    "bazel-bin",
    "bazel-out",
    "bazel-testlogs",
    "build",
    "cmake-build-debug",
    "cmake-build-release",
    "coverage",
    "deriveddata",
    "dist",
    "obj",
    "out",
    "reports",
    "target",
    "tmp",
    ".tmp",
}


class GitInventoryError(RuntimeError):
    """Raised when Git cannot provide the worktree's tracked/non-ignored inventory."""


def _git_metadata_exists(root: Path) -> bool:
    """Return whether ``root`` is inside a Git worktree boundary."""

    current = root.absolute()
    return any((parent / ".git").exists() for parent in (current, *current.parents))


def matches_any(path: Path, root: Path, patterns: Sequence[str]) -> bool:
    relative = path.relative_to(root).as_posix()
    return any(
        fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(path.name, pattern)
        for pattern in patterns
    )


def git_repository_root(root: Path) -> Path | None:
    """Return the containing worktree root, or ``None`` outside Git."""

    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        if _git_metadata_exists(root):
            raise GitInventoryError(f"Git repository discovery failed: {exc}") from exc
        return None
    if result.returncode != 0 or not result.stdout.strip():
        if _git_metadata_exists(root):
            detail = result.stderr.strip() or f"exit status {result.returncode}"
            raise GitInventoryError(f"Git repository discovery failed: {detail}")
        return None
    repository = Path(result.stdout.strip()).resolve()
    try:
        root.resolve().relative_to(repository)
    except ValueError:
        return None
    return repository


def _is_nested_repository(path: Path, root: Path) -> bool:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    current = root.resolve()
    for part in relative.parts:
        current /= part
        if current == root.resolve():
            continue
        if (current / ".git").exists():
            return True
    return False


def _is_architecture_candidate(path: Path) -> bool:
    name = path.name
    extensionless_script = False
    if not path.suffix:
        try:
            with path.open("rb") as handle:
                extensionless_script = handle.read(2) == b"#!"
        except OSError:
            pass
    return (
        path.suffix.lower() in ARCHITECTURE_EXTENSIONS
        or extensionless_script
        or name.lower() in RESERVED_FILES
        or any(fnmatch.fnmatch(name.lower(), pattern) for pattern in RESERVED_PATTERNS)
    )


def _visible_paths(repository: Path, root: Path, payload: bytes) -> set[Path]:
    """Convert Git's NUL-delimited paths into scoped visible files.

    The Git query includes tracked files even when an ignore pattern matches
    them, so the candidate filter must not discard default ignored directory
    names.  Untracked ignored files never appear in the query.
    """

    candidates: set[Path] = set()
    try:
        root_from_repository = root.resolve().relative_to(repository.resolve())
    except ValueError:
        root_from_repository = None
    for raw in payload.split(b"\0"):
        if not raw:
            continue
        repo_relative = Path(os.fsdecode(raw))
        path = repository / repo_relative
        try:
            if root_from_repository is None:
                relative = repo_relative.relative_to(root)
            else:
                relative = repo_relative.relative_to(root_from_repository)
        except ValueError:
            # A caller may use a lexical repository spelling that differs from
            # Git's resolved worktree path.  Resolve the directory boundary,
            # never the candidate itself, so tracked symlinks remain visible.
            try:
                relative = repo_relative.relative_to(
                    root.resolve().relative_to(repository.resolve())
                )
            except ValueError:
                continue
        if not path.is_file() and not path.is_symlink():
            continue
        # Keep the caller's lexical root spelling (macOS commonly exposes
        # /var and /private/var aliases) so findings can safely use
        # ``path.relative_to(root)`` without changing their reported path.
        candidates.add(root / relative)
    return candidates


def _git_inventory(repository: Path, root: Path) -> set[Path]:
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
            ],
            check=False,
            capture_output=True,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitInventoryError(f"Git inventory failed: {exc}") from exc
    if result.returncode != 0:
        detail = (
            os.fsdecode(result.stderr).strip() or f"exit status {result.returncode}"
        )
        raise GitInventoryError(f"Git inventory failed: {detail}")
    return _visible_paths(repository, root, result.stdout)


def _git_candidates(repository: Path, root: Path) -> set[Path]:
    """Return architecture-bearing files from Git's complete visible inventory."""

    return {
        path
        for path in _git_inventory(repository, root)
        if _is_architecture_candidate(path)
    }


def iter_audited_files(root: Path) -> Iterable[Path]:
    """Yield architecture candidates while honoring Git's ignored-file set.

    In Git worktrees, Git supplies the complete tracked/non-ignored untracked
    candidate inventory, so ignored files and directories are never traversed.
    Outside Git, the complete filesystem is walked because no ignore index is
    available.
    """

    # Do not resolve symlinks here.  Temporary roots on macOS are commonly
    # addressed through /var while ``Path.resolve`` yields /private/var;
    # preserving the caller's absolute spelling keeps every yielded finding
    # relative to the root supplied to the public API.
    root = root.absolute()
    repository = git_repository_root(root)
    if repository is not None:
        yield from sorted(_git_candidates(repository, root), key=str)
        return

    candidates: set[Path] = set()
    for current, dirs, files in os.walk(root):
        base = Path(current)
        if base != root and _is_nested_repository(base, root):
            dirs[:] = []
            continue
        filtered: list[str] = []
        for name in dirs:
            child = base / name
            if name in DEFAULT_IGNORED_DIRS or _is_nested_repository(child, root):
                continue
            filtered.append(name)
        dirs[:] = filtered
        for name in files:
            path = base / name
            if _is_architecture_candidate(path):
                candidates.add(path)
    yield from sorted(candidates, key=str)


def is_source_bearing(path: Path, root: Path) -> bool:
    """Return whether a candidate is an authored source unit for structure checks.

    The walker inventories documentation, manifests, and other architecture
    metadata so the audit remains transparent.  Structural heuristics apply
    only to source-bearing paths: code, IDL/schema, or configuration located
    under a source-owned directory.  This removes obvious metadata/ephemeral
    noise without introducing a user-controlled exclusion mechanism.
    """

    extension = path.suffix.lower()
    if extension in SOURCE_EXTENSIONS or extension in SOURCE_BEARING_IDL_EXTENSIONS:
        return True
    if not extension:
        try:
            with path.open("rb") as handle:
                return handle.read(2) == b"#!"
        except OSError:
            return False
    if extension not in SOURCE_BEARING_CONFIG_EXTENSIONS:
        return False
    # Exact tool/framework manifests are metadata even when nested in a
    # package directory.  ``artifact_class`` still reports them visibly.
    if path.name.lower() in RESERVED_FILES or any(
        fnmatch.fnmatch(path.name.lower(), pattern) for pattern in RESERVED_PATTERNS
    ):
        return False
    try:
        ancestors = {part.lower() for part in path.relative_to(root).parts[:-1]}
    except ValueError:
        return False
    return bool(ancestors & SOURCE_BEARING_DIRECTORIES)


def is_output_directory_source(path: Path, root: Path) -> bool:
    """Return whether authored source is placed beneath an output directory."""

    try:
        parents = path.relative_to(root).parts[:-1]
    except ValueError:
        return False
    return is_source_bearing(path, root) and any(
        part.lower() in OUTPUT_DIRECTORIES for part in parents
    )


def count_lines(path: Path) -> int:
    with path.open("rb") as handle:
        return sum(1 for _ in handle)


def artifact_class(path: Path, root: Path) -> str | None:
    name = path.name.lower()
    if name in RESERVED_FILES or any(
        fnmatch.fnmatch(name, pattern) for pattern in RESERVED_PATTERNS
    ):
        return "framework"
    if any(fnmatch.fnmatch(name, pattern) for pattern in GENERATED_NAME_PATTERNS):
        return "generated"
    try:
        header = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:5]
    except OSError:
        return None
    return (
        "generated" if any(GENERATED_HEADER.search(line) for line in header) else None
    )


def normalized_leaf(path: Path) -> str:
    suffix = path.suffix
    leaf = path.name[: -len(suffix)] if suffix else path.name
    ext = suffix.lower()
    lowered = leaf.lower()
    if ext in {".cts", ".mts", ".ts"}:
        for marker in (".test-d", ".spec-d", ".test", ".spec", "_test", "_spec", ".d"):
            if lowered.endswith(marker):
                leaf, lowered = leaf[: -len(marker)], lowered[: -len(marker)]
                break
    elif ext in {".cjs", ".js", ".jsx", ".mjs", ".tsx"}:
        for marker in (".test", ".spec", "_test", "_spec"):
            if lowered.endswith(marker):
                leaf, lowered = leaf[: -len(marker)], lowered[: -len(marker)]
                break
    elif ext in {".py", ".pyi", ".pyw"}:
        if lowered.startswith("test_"):
            leaf, lowered = leaf[5:], lowered[5:]
        elif lowered.endswith("_test"):
            leaf, lowered = leaf[:-5], lowered[:-5]
    elif (ext == ".rb" and lowered.endswith(("_spec", "_test"))) or (
        ext in {".dart", ".exs"} and lowered.endswith("_test")
    ):
        leaf, lowered = leaf[:-5], lowered[:-5]
    elif ext == ".rs" and lowered.endswith("_tests"):
        leaf, lowered = leaf[:-6], lowered[:-6]
    elif ext == ".go":
        if lowered.endswith("_test"):
            leaf, lowered = leaf[:-5], lowered[:-5]
        parts = leaf.split("_")
        lowered_parts = [part.lower() for part in parts]
        if (
            len(parts) >= 3
            and lowered_parts[-2] in GO_OS_MARKERS
            and lowered_parts[-1] in GO_ARCH_MARKERS
        ):
            leaf = "_".join(parts[:-2])
        elif len(parts) >= 2 and lowered_parts[-1] in GO_OS_MARKERS | GO_ARCH_MARKERS:
            leaf = "_".join(parts[:-1])
    elif ext in {".kt", ".kts"}:
        parts = re.split(r"([._])", leaf)
        if (
            len(parts) >= 3
            and parts[-1].lower() in KOTLIN_PLATFORM_MARKERS
            and parts[-2] in {".", "_"}
        ):
            leaf = "".join(parts[:-2])
    if ext in {
        ".cs",
        ".fs",
        ".fsi",
        ".fsx",
        ".java",
        ".kt",
        ".kts",
        ".php",
        ".scala",
        ".swift",
    }:
        match = re.search(r"(?:Tests?|Specs?)$", leaf)
        if match and match.start() > 0:
            leaf = leaf[: match.start()]
    return leaf


def semantic_tokens(path: Path) -> tuple[str, ...]:
    return tuple(
        token.lower() for token in re.split(r"[-_.]+", normalized_leaf(path)) if token
    )


def split_semantic_words(value: str) -> tuple[str, ...]:
    words: list[str] = []
    for token in (part for part in re.split(r"[-_.]+", value) if part):
        parts = re.findall(
            r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+", token, re.ASCII
        )
        words.extend(part.lower() for part in (parts or [token]))
    return tuple(words)


def semantic_words(path: Path) -> tuple[str, ...]:
    return split_semantic_words(normalized_leaf(path))
