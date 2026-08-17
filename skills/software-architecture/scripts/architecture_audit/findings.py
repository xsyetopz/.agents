"""Heuristic structural findings."""

from __future__ import annotations

import collections
import os
from collections.abc import Collection, Sequence
from pathlib import Path

from .discovery import (
    OUTPUT_DIRECTORIES,
    _git_inventory,
    count_lines,
    git_repository_root,
    semantic_tokens,
    semantic_words,
    split_semantic_words,
)
from .records import Finding
from .rules import (
    CATEGORY_CHAIN,
    DEFAULT_IGNORED_DIRS,
    GENERIC_BUCKETS,
    GENERIC_FILENAMES,
    GENERIC_PROCEDURAL_SUFFIXES,
    JS_LOCKFILES,
    MICROFILE_MAX_LINES,
    MICROFILE_MIN_SIBLINGS,
    PROCEDURAL_PHASES,
    STRUCTURAL_DIRECTORIES,
    TEMPORAL_OR_NUMBERED,
)


def filename_findings(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    stem = path.stem.lower()
    tokens = semantic_tokens(path)
    owner_words = semantic_words(path)
    if stem in GENERIC_FILENAMES:
        findings.append(
            Finding(
                "warning",
                "generic-file",
                path,
                "generic filename obscures capability ownership",
                "inventory",
            )
        )
    if len(owner_words) >= 2 and owner_words[-1] in GENERIC_PROCEDURAL_SUFFIXES:
        findings.append(
            Finding(
                "warning",
                "procedural-suffix",
                path,
                f"filename ends with generic procedural suffix '{owner_words[-1]}'; name the durable capability instead",
                "inventory",
            )
        )
    if TEMPORAL_OR_NUMBERED.search(stem):
        findings.append(
            Finding(
                "warning",
                "temporal-file",
                path,
                "numbered or temporal filename",
                "inventory",
            )
        )
    if CATEGORY_CHAIN.search(stem):
        findings.append(
            Finding(
                "warning",
                "category-chain",
                path,
                "repeated categorical filename",
                "inventory",
            )
        )
    if len(tokens) >= 3:
        findings.append(
            Finding(
                "warning",
                "semantic-token-limit",
                path,
                f"separator-delimited filename has {len(tokens)} semantic tokens: {', '.join(tokens)}",
                "inventory",
            )
        )
    if len(owner_words) >= 2:
        for ancestor in path.relative_to(root).parents:
            if str(ancestor) == ".":
                continue
            owner_tokens = split_semantic_words(ancestor.name)
            if not owner_tokens or owner_tokens[0] in STRUCTURAL_DIRECTORIES:
                continue
            if owner_words and owner_words[0] in owner_tokens:
                findings.append(
                    Finding(
                        "warning",
                        "redundant-owner-prefix",
                        path,
                        f"multi-token leaf repeats ancestor owner token '{owner_words[0]}'",
                        "inventory",
                    )
                )
                break
    return findings


def _filesystem_child_directories(parent: Path) -> list[Path]:
    try:
        return [
            item
            for item in parent.iterdir()
            if item.is_dir() and item.name not in DEFAULT_IGNORED_DIRS
        ]
    except OSError:
        return []


def directory_findings(
    root: Path,
    files: Sequence[Path],
    flat_limit: int,
    *,
    inventory: Sequence[Path] | None = None,
) -> list[Finding]:
    findings: list[Finding] = []
    by_parent: dict[Path, list[Path]] = collections.defaultdict(list)
    by_grandparent: dict[Path, list[Path]] = collections.defaultdict(list)
    generic_paths: set[Path] = set()
    visible_child_dirs: dict[Path, set[Path]] = collections.defaultdict(set)
    if inventory is not None:
        for path in inventory:
            try:
                relative_parts = path.relative_to(root).parts[:-1]
            except ValueError:
                continue
            parent = root
            for part in relative_parts:
                child = parent / part
                visible_child_dirs[parent].add(child)
                parent = child
    for path in files:
        by_parent[path.parent].append(path)
        if path.parent != root:
            by_grandparent[path.parent.parent].append(path.parent)
        for parent in path.parents:
            if parent == root:
                break
            if parent.name.lower() in GENERIC_BUCKETS:
                generic_paths.add(parent)
    for path in sorted(generic_paths):
        findings.append(
            Finding(
                "warning",
                "generic-directory",
                path,
                "generic bucket requires explicit ownership justification",
                "inventory",
            )
        )
    for parent, children in sorted(by_parent.items(), key=lambda pair: str(pair[0])):
        logical_units: dict[str, set[tuple[str, ...]]] = collections.defaultdict(set)
        for child in children:
            tokens = semantic_words(child)
            if len(tokens) >= 2:
                logical_units[tokens[0]].add(tokens)
        for owner, units in sorted(logical_units.items()):
            if len(units) >= 3:
                findings.append(
                    Finding(
                        "warning",
                        "filename-colony",
                        parent / owner,
                        f"{len(units)} sibling logical units share semantic owner token '{owner}'",
                        "inventory",
                    )
                )
        phase_files = [
            child
            for child in children
            if semantic_words(child) in {(phase,) for phase in PROCEDURAL_PHASES}
        ]
        if len(phase_files) >= len(PROCEDURAL_PHASES):
            for child in sorted(phase_files, key=str):
                phase = semantic_words(child)[0]
                findings.append(
                    Finding(
                        "warning",
                        "procedural-suffix",
                        child,
                        f"single-token procedural phase '{phase}' is not a durable capability boundary",
                        "inventory",
                    )
                )
        if len(children) >= flat_limit:
            findings.append(
                Finding(
                    "warning",
                    "flat-cluster",
                    parent,
                    f"flat directory contains {len(children)} authored architecture files",
                    "inventory",
                )
            )
        if len(children) >= MICROFILE_MIN_SIBLINGS:
            try:
                all_micro = all(
                    count_lines(child) <= MICROFILE_MAX_LINES for child in children
                )
            except OSError:
                all_micro = False
            if all_micro:
                findings.append(
                    Finding(
                        "warning",
                        "microfile-fragmentation",
                        parent,
                        f"flat directory contains {len(children)} microfiles; consolidate by durable capability",
                        "inventory",
                    )
                )
        if parent != root and len(children) == 1:
            child_dirs = (
                [
                    item
                    for item in visible_child_dirs.get(parent, set())
                    if item.name not in DEFAULT_IGNORED_DIRS
                ]
                if inventory is not None
                else _filesystem_child_directories(parent)
            )
            if not child_dirs:
                findings.append(
                    Finding(
                        "notice",
                        "single-file-directory",
                        parent,
                        "directory owns one authored source file and no source subdirectories; verify the boundary is toolchain-required or durable",
                        "inventory",
                    )
                )
    # A cluster of tiny, one-file directories usually signals ceremonial
    # splitting rather than independently owned boundaries.  Keep the signal
    # conservative: require several sibling directories and a genuinely small
    # source unit, while allowing legitimate larger modules to stand alone.
    for grandparent, child_parents in sorted(
        by_grandparent.items(), key=lambda pair: str(pair[0])
    ):
        unique_parents = sorted(set(child_parents), key=str)
        micro_dirs: list[Path] = []
        for parent in unique_parents:
            children = by_parent.get(parent, [])
            if len(children) != 1:
                continue
            child_dirs = (
                [
                    item
                    for item in visible_child_dirs.get(parent, set())
                    if item.name not in DEFAULT_IGNORED_DIRS
                ]
                if inventory is not None
                else _filesystem_child_directories(parent)
            )
            if child_dirs:
                continue
            try:
                if count_lines(children[0]) <= MICROFILE_MAX_LINES:
                    micro_dirs.append(parent)
            except OSError:
                continue
        if len(micro_dirs) >= MICROFILE_MIN_SIBLINGS:
            findings.append(
                Finding(
                    "warning",
                    "microfile-fragmentation",
                    grandparent,
                    f"{len(micro_dirs)} sibling directories each contain one microfile; consolidate by durable capability",
                    "inventory",
                )
            )
        phase_dirs = [
            parent
            for parent in unique_parents
            if parent.name.lower() in PROCEDURAL_PHASES
            and len(by_parent.get(parent, [])) == 1
            and not (
                [
                    item
                    for item in visible_child_dirs.get(parent, set())
                    if item.name not in DEFAULT_IGNORED_DIRS
                ]
                if inventory is not None
                else _filesystem_child_directories(parent)
            )
        ]
        if len(phase_dirs) >= len(PROCEDURAL_PHASES):
            findings.append(
                Finding(
                    "warning",
                    "procedural-directory",
                    grandparent,
                    f"phase directories {', '.join(sorted(item.name for item in phase_dirs))} split one microfile each; consolidate by durable capability",
                    "inventory",
                )
            )
            findings.append(
                Finding(
                    "warning",
                    "microfile-fragmentation",
                    grandparent,
                    f"{len(phase_dirs)} procedural phase directories each contain one microfile; consolidate by durable capability",
                    "inventory",
                )
            )
    return findings


def package_manager_findings(
    root: Path,
    inventory: Sequence[Path] | None = None,
) -> list[Finding]:
    def findings_for_inventory(visible: Collection[Path]) -> list[Finding]:
        findings: list[Finding] = []
        package_dirs = sorted(
            {path.parent for path in visible if path.name == "package.json"}, key=str
        )
        for base in package_dirs:
            names = {path.name for path in visible if path.parent == base}
            present = {
                manager
                for manager, locks in JS_LOCKFILES.items()
                if names.intersection(locks)
            }
            if len(present) > 1:
                findings.append(
                    Finding(
                        "error",
                        "conflicting-lockfiles",
                        base,
                        f"multiple JavaScript package-manager lockfile families: {', '.join(sorted(present))}",
                        "inventory",
                    )
                )
        return findings

    if inventory is not None:
        return findings_for_inventory(inventory)
    repository = git_repository_root(root)
    if repository is not None:
        return findings_for_inventory(_git_inventory(repository, root))
    findings: list[Finding] = []
    ignored_dirs = DEFAULT_IGNORED_DIRS | (
        OUTPUT_DIRECTORIES if repository is not None else set()
    )
    for current, dirs, files in os.walk(root):
        base = Path(current)
        if repository is not None and base != root and (base / ".git").exists():
            dirs[:] = []
            continue
        dirs[:] = [
            name
            for name in dirs
            if name not in ignored_dirs and not (base / name / ".git").exists()
        ]
        if "package.json" not in files:
            continue
        present = {
            manager
            for manager, names in JS_LOCKFILES.items()
            if any(name in files for name in names)
        }
        if len(present) > 1:
            findings.append(
                Finding(
                    "error",
                    "conflicting-lockfiles",
                    base,
                    f"multiple JavaScript package-manager lockfile families: {', '.join(sorted(present))}",
                    "inventory",
                )
            )
    return findings
