#!/usr/bin/env python3
"""Path and source normalization helpers for inline-test detection."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

_TEST_DIRECTORIES = {
    "__test__",
    "__tests__",
    "bench",
    "benches",
    "benchmark",
    "benchmarks",
    "e2e",
    "e2e-test",
    "e2e-tests",
    "e2e_test",
    "e2e_tests",
    "acceptance_test",
    "acceptance_tests",
    "component_test",
    "component_tests",
    "contract_test",
    "contract_tests",
    "fixtures",
    "fixture",
    "integration_test",
    "integration_tests",
    "integration-test",
    "integration-tests",
    "load_test",
    "load_tests",
    "performance_test",
    "performance_tests",
    "property_test",
    "property_tests",
    "spec",
    "specs",
    "test",
    "testdata",
    "test_data",
    "test-data",
    "test-fixture",
    "test-fixtures",
    "testfixtures",
    "test_fixtures",
    "test_support",
    "test-support",
    "test_helpers",
    "test-helpers",
    "testthat",
    "tests",
    "unit_test",
    "unit_tests",
    "unit-test",
    "unit-tests",
}

_LOWER_TEST_FILE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern)
    for pattern in (
        r"(?:^test_.+|.+_tests?|tests?)\.py$",
        r".+_test\.go$",
        r"(?:^test_.+|.+_tests?|tests?)\.rs$",
        r"_tests?\.rs$",
        r"(?:test[-_].+|.+[-_](?:test|tests|spec|specs)|.+\.(?:test|spec))\.[cm]?[jt]sx?$",
        r"(?:^test_.+|.+_tests?|tests?)\.(?:c|cc|cpp|cxx|h|hh|hpp|hxx)$",
        r"(?:test[-_].+|.+[-_](?:test|tests|spec|specs))\.(?:java|kt|kts|scala|groovy)$",
        r"(?:test[-_].+|.+[-_](?:test|tests|spec|specs))\.(?:cs|fs|fsx|vb)$",
        r"(?:test[-_].+|.+[-_](?:test|tests))\.swift$",
        r"(?:test[-_].+|.+[-_](?:test|tests))\.php$",
        r"(?:test_.+|.+_(?:test|spec))\.rb$",
        r".+_test\.exs$",
        r".+_test\.dart$",
        r"(?:runtests|test_.+|.+_test)\.jl$",
        r"(?:test_.+|.+_tests?)\.(?:ml|mli)$",
        r".+_test\.(?:clj|cljs|cljc)$",
        r"(?:test_.+|.+_(?:test|spec))\.lua$",
        r".+\.t$",
        r"(?:test_.+|.+_test)\.(?:sh|bash|zsh|fish)$",
        r"(?:test_.+|.+_test)\.(?:zig|d|nim|erl)$",
        r".+_tests\.erl$",
        r"(?:test_.+|.+_test)\.(?:hs|lhs|r|cr|tcl|sol|v)$",
    )
)

_BENCHMARK_FILE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern)
    for pattern in (
        r".+_(?:bench|benchmark|benchmarks)\.rs$",
        r"_(?:bench|benchmark|benchmarks)\.rs$",
        r".+\.(?:bench|benchmark)\.(?:c|cc|cpp|cxx|js|jsx|mjs|cjs|rs|ts|tsx|mts|cts|zig)$",
    )
)

_CAMEL_TEST_FILE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern)
    for pattern in (
        r".+(?:Test|Tests|Spec|Specs)\.(?:java|kt|kts|scala|groovy)$",
        r".+(?:Test|Tests|Spec|Specs)\.(?:cs|fs|fsx|vb)$",
        r".+(?:Test|Tests)\.swift$",
        r".+Test\.php$",
        r".+(?:Benchmark|Benchmarks)\.(?:java|kt|kts|scala|groovy|cs|fs|fsx|vb|swift)$",
    )
)

_HASH_COMMENT_SUFFIXES = {
    ".bash",
    ".cr",
    ".fish",
    ".jl",
    ".nim",
    ".pl",
    ".pm",
    ".py",
    ".pyi",
    ".pyw",
    ".r",
    ".rake",
    ".rb",
    ".sh",
    ".t",
    ".tcl",
    ".zsh",
}
_DASH_COMMENT_SUFFIXES = {".hs", ".lhs", ".lua"}
_PERCENT_COMMENT_SUFFIXES = {".erl", ".hrl"}
_SEMICOLON_COMMENT_SUFFIXES = {".clj", ".cljs", ".cljc"}
_OCAML_COMMENT_SUFFIXES = {".fs", ".fsi", ".fsx", ".ml", ".mli"}
_BLOCK_COMMENT_DELIMITERS = {
    ".d": ("/+", "+/"),
    ".hs": ("{-", "-}"),
    ".lhs": ("{-", "-}"),
    ".jl": ("#=", "=#"),
    ".lua": ("--[[", "]]"),
    ".nim": ("#[", "]#"),
}


@lru_cache(maxsize=64)
def _javascript_runner_configured(
    root: Path, inventory: tuple[Path, ...] | None = None
) -> bool:
    package = root / "package.json"
    candidates = [package] if inventory is None or package in inventory else []
    if inventory is None:
        candidates.extend(root.glob("jest.config.*"))
        candidates.extend(root.glob("vitest.config.*"))
        candidates.extend(root.glob("playwright.config.*"))
    else:
        candidates.extend(
            path
            for path in inventory
            if path.parent == root
            and any(
                path.match(pattern)
                for pattern in (
                    "jest.config.*",
                    "vitest.config.*",
                    "playwright.config.*",
                )
            )
        )
    for candidate in candidates:
        try:
            text = candidate.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if candidate.name != "package.json" or re.search(
            r"(?:vitest|jest|@jest/globals|node:test|@playwright/test)",
            text,
            re.IGNORECASE,
        ):
            return True
    return False


def is_test_source(path: Path, root: Path) -> bool:
    """Return whether a path follows a built-in test or benchmark convention."""
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = path
    for part in relative.parts[:-1]:
        lower = part.lower()
        if lower == "t":
            if path.suffix.lower() in {".pl", ".pm", ".t"}:
                return True
            continue
        if lower in _TEST_DIRECTORIES:
            return True
    return (
        any(
            pattern.fullmatch(path.name.lower())
            for pattern in _LOWER_TEST_FILE_PATTERNS
        )
        or any(pattern.fullmatch(path.name) for pattern in _CAMEL_TEST_FILE_PATTERNS)
        or any(
            pattern.fullmatch(path.name.lower()) for pattern in _BENCHMARK_FILE_PATTERNS
        )
    )


def _blank(text: str) -> str:
    return "".join("\n" if character == "\n" else " " for character in text)


def _nested_block_end(text: str, index: int, start: str, end: str) -> int | None:
    depth = 1
    cursor = index + len(start)
    while cursor < len(text) and depth:
        if text.startswith(start, cursor):
            depth += 1
            cursor += len(start)
        elif text.startswith(end, cursor):
            depth -= 1
            cursor += len(end)
        else:
            cursor += 1
    return cursor if depth == 0 else None


def _strip_source(text: str, suffix: str, *, strings: bool = True) -> str:
    """Blank comments and quoted strings while retaining offsets and newlines."""
    output = list(text)
    index = 0
    length = len(text)
    while index < length:
        if suffix == ".rs" and text[index] == "r":
            raw = re.match(r'r(#{0,255})"', text[index:])
            if raw:
                delimiter = '"' + raw.group(1)
                end = text.find(delimiter, index + raw.end())
                if end < 0:
                    index += 1
                    continue
                stop = end + len(delimiter)
                output[index:stop] = _blank(text[index:stop])
                index = stop
                continue
        block_delimiters = _BLOCK_COMMENT_DELIMITERS.get(suffix)
        if suffix == ".lua":
            lua_comment = re.match(r"--\[(=*)\[", text[index:])
            if lua_comment:
                block_delimiters = (
                    lua_comment.group(0),
                    "]" + lua_comment.group(1) + "]",
                )
            elif strings:
                lua_string = re.match(r"\[(=*)\[", text[index:])
                if lua_string:
                    block_delimiters = (
                        lua_string.group(0),
                        "]" + lua_string.group(1) + "]",
                    )
        if block_delimiters and text.startswith(block_delimiters[0], index):
            stop = _nested_block_end(text, index, *block_delimiters)
            if stop is None:
                index += 1
                continue
            output[index:stop] = _blank(text[index:stop])
            index = stop
            continue
        if suffix in {".rb", ".rake", ".gemspec"} and re.match(
            r"=begin\b", text[index:]
        ):
            line_start = text.rfind("\n", 0, index) + 1
            if line_start == index:
                match = re.search(r"(?m)^=end\b.*(?:\n|$)", text[index:])
                if match is None:
                    index += 1
                    continue
                stop = index + match.end()
                output[index:stop] = _blank(text[index:stop])
                index = stop
                continue
        if suffix in {".bash", ".fish", ".sh", ".zsh"} and text.startswith("<<", index):
            heredoc = re.match(
                r"<<-?\s*(?:(['\"])([A-Za-z_][A-Za-z0-9_]*)\1|([A-Za-z_][A-Za-z0-9_]*))",
                text[index:],
            )
            if heredoc:
                tag = heredoc.group(2) or heredoc.group(3)
                closing = re.search(
                    rf"(?m)^[ \t]*{re.escape(tag)}[ \t]*(?:\n|$)",
                    text[index + heredoc.end() :],
                )
                if closing is None:
                    index += 2
                    continue
                stop = index + heredoc.end() + closing.end()
                output[index:stop] = _blank(text[index:stop])
                index = stop
                continue
        if text.startswith("/*", index):
            depth = 1
            cursor = index + 2
            while cursor < length and depth:
                if text.startswith("/*", cursor):
                    depth += 1
                    cursor += 2
                elif text.startswith("*/", cursor):
                    depth -= 1
                    cursor += 2
                else:
                    cursor += 1
            if depth:
                index += 1
                continue
            output[index:cursor] = _blank(text[index:cursor])
            index = cursor
            continue
        if suffix in _OCAML_COMMENT_SUFFIXES and text.startswith("(*", index):
            depth = 1
            cursor = index + 2
            while cursor < length and depth:
                if text.startswith("(*", cursor):
                    depth += 1
                    cursor += 2
                elif text.startswith("*)", cursor):
                    depth -= 1
                    cursor += 2
                else:
                    cursor += 1
            if depth:
                index += 1
                continue
            output[index:cursor] = _blank(text[index:cursor])
            index = cursor
            continue
        line_comment = (
            text.startswith("//", index)
            or suffix in _HASH_COMMENT_SUFFIXES
            and text[index] == "#"
            or suffix in _DASH_COMMENT_SUFFIXES
            and text.startswith("--", index)
            or suffix in _PERCENT_COMMENT_SUFFIXES
            and text[index] == "%"
            or suffix in _SEMICOLON_COMMENT_SUFFIXES
            and text[index] == ";"
        )
        if line_comment:
            stop = text.find("\n", index)
            stop = length if stop < 0 else stop
            output[index:stop] = " " * (stop - index)
            index = stop
            continue
        if strings and text[index] in {"'", '"', "`"}:
            quote = text[index]
            if (
                quote == "'"
                and suffix == ".rs"
                and not re.match(r"'(?:\\.|[^'\\\n])'", text[index:])
            ):
                index += 1
                continue
            triple = text.startswith(quote * 3, index)
            delimiter = quote * (3 if triple else 1)
            cursor = index + len(delimiter)
            closed = False
            while cursor < length:
                if text.startswith(delimiter, cursor):
                    cursor += len(delimiter)
                    closed = True
                    break
                if not triple and text[cursor] == "\\":
                    cursor += 2
                else:
                    cursor += 1
            if not closed:
                index += 1
                continue
            output[index:cursor] = _blank(text[index:cursor])
            index = cursor
            continue
        index += 1
    return "".join(output)
