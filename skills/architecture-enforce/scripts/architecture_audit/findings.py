"""Heuristic structural findings."""

from __future__ import annotations

import collections
import os
from collections.abc import Sequence
from pathlib import Path

from .discovery import (
    matches_any,
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
    JS_LOCKFILES,
    STRUCTURAL_DIRECTORIES,
    TEMPORAL_OR_NUMBERED,
)


def filename_findings(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    stem = path.stem.lower()
    tokens = semantic_tokens(path)
    owner_words = semantic_words(path)
    if stem in GENERIC_FILENAMES:
        findings.append(Finding("warning", "generic-file", path, "generic filename obscures capability ownership", "inventory"))
    if TEMPORAL_OR_NUMBERED.search(stem):
        findings.append(Finding("warning", "temporal-file", path, "numbered or temporal filename", "inventory"))
    if CATEGORY_CHAIN.search(stem):
        findings.append(Finding("warning", "category-chain", path, "repeated categorical filename", "inventory"))
    if len(tokens) >= 3:
        findings.append(Finding("warning", "semantic-token-limit", path, f"separator-delimited filename has {len(tokens)} semantic tokens: {', '.join(tokens)}", "inventory"))
    if len(owner_words) >= 2:
        for ancestor in path.relative_to(root).parents:
            if str(ancestor) == ".":
                continue
            owner_tokens = split_semantic_words(ancestor.name)
            if not owner_tokens or owner_tokens[0] in STRUCTURAL_DIRECTORIES:
                continue
            if owner_words and owner_words[0] in owner_tokens:
                findings.append(Finding("warning", "redundant-owner-prefix", path, f"multi-token leaf repeats ancestor owner token '{owner_words[0]}'", "inventory"))
                break
    return findings


def directory_findings(root: Path, files: Sequence[Path], flat_limit: int) -> list[Finding]:
    findings: list[Finding] = []
    by_parent: dict[Path, list[Path]] = collections.defaultdict(list)
    generic_paths: set[Path] = set()
    for path in files:
        by_parent[path.parent].append(path)
        for parent in path.parents:
            if parent == root:
                break
            if parent.name.lower() in GENERIC_BUCKETS:
                generic_paths.add(parent)
    for path in sorted(generic_paths):
        findings.append(Finding("warning", "generic-directory", path, "generic bucket requires explicit ownership justification", "inventory"))
    for parent, children in sorted(by_parent.items(), key=lambda pair: str(pair[0])):
        logical_units: dict[str, set[tuple[str, ...]]] = collections.defaultdict(set)
        for child in children:
            tokens = semantic_words(child)
            if len(tokens) >= 2:
                logical_units[tokens[0]].add(tokens)
        for owner, units in sorted(logical_units.items()):
            if len(units) >= 3:
                findings.append(Finding("warning", "filename-colony", parent / owner, f"{len(units)} sibling logical units share semantic owner token '{owner}'", "inventory"))
        if len(children) >= flat_limit:
            findings.append(Finding("warning", "flat-cluster", parent, f"flat directory contains {len(children)} authored architecture files", "inventory"))
        if parent != root and len(children) == 1:
            try:
                child_dirs = [item for item in parent.iterdir() if item.is_dir() and item.name not in DEFAULT_IGNORED_DIRS]
            except OSError:
                child_dirs = []
            if not child_dirs:
                findings.append(Finding("notice", "single-file-directory", parent, "directory owns one authored source file and no source subdirectories; verify the boundary is toolchain-required or durable", "inventory"))
    return findings


def package_manager_findings(root: Path, excludes: Sequence[str]) -> list[Finding]:
    findings: list[Finding] = []
    for current, dirs, files in os.walk(root):
        base = Path(current)
        dirs[:] = [name for name in dirs if name not in DEFAULT_IGNORED_DIRS and not matches_any(base / name, root, excludes)]
        if "package.json" not in files or matches_any(base / "package.json", root, excludes):
            continue
        present = {manager for manager, names in JS_LOCKFILES.items() if any(name in files for name in names)}
        if len(present) > 1:
            findings.append(Finding("error", "conflicting-lockfiles", base, f"multiple JavaScript package-manager lockfile families: {', '.join(sorted(present))}", "inventory"))
    return findings
