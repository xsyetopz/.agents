"""Conservative detection of tests and benchmarks embedded in authored source."""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from functools import lru_cache
from pathlib import Path

from .records import Finding, TestSourceRoot
from .rules import SOURCE_EXTENSIONS

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
    ".bash", ".cr", ".fish", ".jl", ".nim", ".pl", ".pm", ".py", ".pyi", ".pyw",
    ".r", ".rake", ".rb", ".sh", ".t", ".tcl", ".zsh",
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
def _javascript_runner_configured(root: Path) -> bool:
    candidates = [root / "package.json"]
    candidates.extend(root.glob("jest.config.*"))
    candidates.extend(root.glob("vitest.config.*"))
    candidates.extend(root.glob("playwright.config.*"))
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


def is_test_source(
    path: Path, root: Path, configured_roots: Sequence[Path | str | TestSourceRoot] = ()
) -> bool:
    """Return whether a path follows an exact test or benchmark convention."""
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = path
    for configured in configured_roots:
        target = Path(configured.path) if isinstance(configured, TestSourceRoot) else Path(configured)
        if not target.is_absolute():
            target = root / target
        if path == target or target in path.parents:
            return True
    for part in relative.parts[:-1]:
        lower = part.lower()
        if lower == "t":
            if path.suffix.lower() in {".pl", ".pm", ".t"}:
                return True
            continue
        if lower in _TEST_DIRECTORIES:
            return True
    return (
        any(pattern.fullmatch(path.name.lower()) for pattern in _LOWER_TEST_FILE_PATTERNS)
        or any(pattern.fullmatch(path.name) for pattern in _CAMEL_TEST_FILE_PATTERNS)
        or any(pattern.fullmatch(path.name.lower()) for pattern in _BENCHMARK_FILE_PATTERNS)
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
                block_delimiters = (lua_comment.group(0), "]" + lua_comment.group(1) + "]")
            elif strings:
                lua_string = re.match(r"\[(=*)\[", text[index:])
                if lua_string:
                    block_delimiters = (lua_string.group(0), "]" + lua_string.group(1) + "]")
        if block_delimiters and text.startswith(block_delimiters[0], index):
            stop = _nested_block_end(text, index, *block_delimiters)
            if stop is None:
                index += 1
                continue
            output[index:stop] = _blank(text[index:stop])
            index = stop
            continue
        if suffix in {".rb", ".rake", ".gemspec"} and re.match(r"=begin\b", text[index:]):
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
                closing = re.search(rf"(?m)^[ \t]*{re.escape(tag)}[ \t]*(?:\n|$)", text[index + heredoc.end():])
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
            or suffix in _HASH_COMMENT_SUFFIXES and text[index] == "#"
            or suffix in _DASH_COMMENT_SUFFIXES and text.startswith("--", index)
            or suffix in _PERCENT_COMMENT_SUFFIXES and text[index] == "%"
            or suffix in _SEMICOLON_COMMENT_SUFFIXES and text[index] == ";"
        )
        if line_comment:
            stop = text.find("\n", index)
            stop = length if stop < 0 else stop
            output[index:stop] = " " * (stop - index)
            index = stop
            continue
        if strings and text[index] in {"'", '"', "`"}:
            quote = text[index]
            if quote == "'" and suffix == ".rs" and not re.match(
                r"'(?:\\.|[^'\\\n])'", text[index:]
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


def _rules(
    suffix: str, clean: str, comments_only: str, *, js_runner_configured: bool = False
) -> Iterable[tuple[str, re.Pattern[str], str]]:
    flags = re.MULTILINE
    if suffix == ".rs":
        yield "inline-test", re.compile(
            r"#\s*\[\s*(?:(?:async_std|tokio)::test|rstest|test|test_case)\b[^\]]*\]",
            flags,
        ), "Rust test attribute"
        yield "inline-benchmark", re.compile(r"#\s*\[\s*bench\s*\]", flags), "#[bench]"
        yield "inline-test", re.compile(r"\bmod\s+(?:test|tests)\s*\{", flags), "inline test module"
        yield "inline-benchmark", re.compile(
            r"\bmod\s+(?:bench|benches|benchmark|benchmarks)\s*\{", flags
        ), "inline benchmark module"
        yield "inline-test", re.compile(
            r"#\s*\[\s*cfg\s*\([^\]]*\btest\b[^\]]*\)\s*\]\s*"
            r"(?:(?:#\s*\[[^\]]*\])\s*)*"
            r"(?:pub(?:\s*\([^)]*\))?\s+)?(?:async\s+)?(?:"
            r"mod\s+\w+\s*\{|(?:const|enum|fn|impl|static|struct|trait|type|use)\b)",
            flags,
        ), "#[cfg(test)] body item"
    elif suffix == ".zig":
        yield "inline-test", re.compile(r"(?m)^\s*test(?:\s+.*?)?\s*\{"), "test {"
    elif suffix == ".d":
        yield "inline-test", re.compile(r"\bunittest\s*\{", flags), "unittest {"
    elif suffix == ".nim" and re.search(
        r"(?m)^\s*(?:import|from)\s+(?:std/)?unittest\b", clean
    ):
        yield "inline-test", re.compile(r"(?m)^\s*(?:suite|test)\b[^:]*:"), "unittest suite/test block"
    elif suffix in {".erl", ".hrl"} and re.search(
        r"-include(?:_lib)?\s*\(\s*[\"'][^\"']*eunit[^\"']*[\"']\s*\)", comments_only
    ):
        yield "inline-test", re.compile(r"(?m)^\s*[a-z][a-zA-Z0-9_]*_test_?\s*\(\s*\)\s*->"), "EUnit _test function"
        yield "inline-test", re.compile(r"\?(?:assert|assertEqual|assertMatch|assertNot|assertNotEqual)\b"), "EUnit assertion macro"
    elif suffix == ".erl" and re.search(
        r"-include(?:_lib)?\s*\(\s*[\"'][^\"']*common_test[^\"']*[\"']\s*\)", comments_only
    ):
        yield "inline-test", re.compile(r"(?m)^\s*(?:all|init_per_suite|end_per_suite)\s*\("), "Common Test callback"
    elif suffix == ".go":
        yield "inline-test", re.compile(r"(?m)^\s*func\s+Test[A-Z0-9_]\w*\s*\("), "func Test..."
        yield "inline-benchmark", re.compile(r"(?m)^\s*func\s+Benchmark[A-Z0-9_]\w*\s*\("), "func Benchmark..."
    elif suffix in {".py", ".pyi", ".pyw"}:
        yield "inline-test", re.compile(r"(?m)^\s*(?:async\s+)?def\s+test(?:_\w+)?\s*\("), "def test..."
        yield "inline-test", re.compile(
            r"(?m)^\s*class\s+Test\w*\s*\([^)]*(?:TestCase|unittest)[^)]*\):",
        ), "unittest TestCase class"
        yield "inline-benchmark", re.compile(r"(?m)^\s*(?:async\s+)?def\s+benchmark_\w+\s*\("), "def benchmark_..."
        yield "inline-benchmark", re.compile(r"(?m)^\s*@pytest\.mark\.benchmark\b"), "@pytest.mark.benchmark"
        yield "inline-test", re.compile(r"(?m)^\s*@pytest\.mark\.(?:parametrize|asyncio)\b"), "pytest test marker"
    elif suffix in {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts"}:
        if js_runner_configured or re.search(
            r"(?m)^\s*(?:import\b.*\b(?:describe|it|suite)\b.*\bfrom\s*|"
            r"(?:const|let|var)\s+.*\b(?:describe|it|suite)\b.*=\s*require\s*\()\s*"
            r"[\"'][^\"']*(?:bun:test|jest|node:test|vitest|mocha|jasmine)[^\"']*[\"']",
            comments_only,
        ) or re.search(
            r"(?m)^\s*(?:describe|it|suite)(?:\.(?:each|only|skip|concurrent))?\s*\(\s*['\"`][^'\"`\n]+['\"`]\s*,\s*"
            r"(?:async\s+)?(?:function\b|(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>)",
            comments_only,
        ) or re.search(r"(?m)^\s*(?:describe|it|suite)\.(?:each|only|skip|concurrent)\s*\(", comments_only):
            yield "inline-test", re.compile(r"(?m)^\s*(?:describe|it|suite)(?:\.(?:each|only|skip|concurrent))?\s*\("), "test suite/example call"
        yield "inline-test", re.compile(r"(?m)^\s*(?:Bun|Deno)\.test\s*\("), "runtime test call"
        if re.search(
            r"(?m)^\s*(?:import\b.*\btest\b.*\bfrom\s*|"
            r"(?:const|let|var)\s+.*\btest\b.*=\s*require\s*\()\s*"
            r"[\"'][^\"']*(?:bun:test|jest|node:test|vitest)[^\"']*[\"']",
            comments_only,
        ):
            yield "inline-test", re.compile(r"(?m)^\s*test(?:\.(?:each|only|skip|concurrent))?\s*\("), "framework-imported test call"
        if re.search(
            r"(?m)^\s*test(?:\.(?:each|only|skip|concurrent))?\s*\(\s*['\"`][^'\"`\n]+['\"`]\s*,\s*"
            r"(?:async\s+)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>",
            comments_only,
        ) or re.search(r"(?m)^\s*test\.(?:each|only|skip|concurrent)\s*\(", comments_only):
            yield "inline-test", re.compile(r"(?m)^\s*test(?:\.(?:each|only|skip|concurrent))?\s*\("), "structural framework test call"
        yield "inline-benchmark", re.compile(r"(?m)^\s*(?:bench|benchmark)\s*\("), "bench/benchmark call"
    elif suffix in {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"}:
        yield "inline-test", re.compile(r"(?m)^\s*(?:TEST|TEST_F|TEST_P|TYPED_TEST)\s*\("), "C++ test macro"
        yield "inline-test", re.compile(
            r"(?m)^\s*(?:TEST_CASE|TEST_CASE_METHOD|TEST_CASE_TEMPLATE|SCENARIO)\s*\(",
        ), "Catch2/doctest test macro"
        yield "inline-benchmark", re.compile(r"(?m)^\s*BENCHMARK(?:_F)?\s*\("), "C++ benchmark macro"
    elif suffix in {".java", ".kt", ".kts", ".scala", ".groovy"}:
        if re.search(
            r"(?m)^\s*import\s+(?:static\s+)?(?:"
            r"org\.junit(?:\.jupiter\.api)?\.(?:Test|ParameterizedTest|RepeatedTest|\*)|"
            r"org\.testng\.annotations\.(?:Test|\*)|"
            r"kotlin\.test\.(?:Test|\*)|org\.openjdk\.jmh\.annotations\.Benchmark)",
            comments_only,
        ):
            yield "inline-test", re.compile(r"(?m)^\s*@(?:ParameterizedTest|RepeatedTest|Test|TestFactory|TestTemplate|BeforeEach|AfterEach|BeforeAll|AfterAll|Before|After|BeforeMethod|AfterMethod|BeforeClass|AfterClass|DataProvider)\b"), "@Test"
            yield "inline-benchmark", re.compile(r"(?m)^\s*@Benchmark\b"), "@Benchmark"
        yield "inline-test", re.compile(
            r"(?m)^\s*@org\.(?:junit|testng)\.(?:ParameterizedTest|RepeatedTest|Test|TestFactory|TestTemplate|BeforeEach|AfterEach|BeforeAll|AfterAll|Before|After|BeforeMethod|AfterMethod|BeforeClass|AfterClass|DataProvider)\b",
        ), "qualified @Test"
        yield "inline-benchmark", re.compile(
            r"(?m)^\s*@org\.openjdk\.jmh\.annotations\.Benchmark\b",
        ), "qualified @Benchmark"
    elif suffix in {".cs", ".fs", ".fsx", ".vb"}:
        dotnet_framework = re.search(
            r"(?mi)^\s*(?:using|open|imports?)\s+(?:xunit|nunit|microsoft\.visualstudio\.testtools\.unittesting|benchmarkdotnet)\b",
            comments_only,
        )
        if dotnet_framework:
            yield "inline-test", re.compile(r"(?m)^\s*\[(?:Fact|Theory|Test|TestCase|SetUp|TearDown|OneTimeSetUp|OneTimeTearDown)\b"), "[Fact]/[Test]"
            yield "inline-test", re.compile(r"(?m)^\s*\[(?:TestMethod|DataTestMethod|TestInitialize|TestCleanup|ClassInitialize|ClassCleanup)\b"), "[TestMethod]"
            yield "inline-test", re.compile(r"(?m)^\s*\[<(?:Fact|Theory|Test|TestCase)\b[^>]*>\]"), "[<Fact>]/[<Test>]"
            yield "inline-test", re.compile(r"(?mi)^\s*<(?:Fact|Theory|Test|TestCase)\b[^>]*>"), "<Fact>/<Test>"
            yield "inline-benchmark", re.compile(r"(?m)^\s*\[(?:Benchmark|BenchmarkDotNet)\b"), "[Benchmark]"
            yield "inline-benchmark", re.compile(r"(?m)^\s*\[<(?:Benchmark|BenchmarkDotNet)\b[^>]*>\]"), "[<Benchmark>]"
            yield "inline-benchmark", re.compile(r"(?mi)^\s*<(?:Benchmark|BenchmarkDotNet)\b[^>]*>"), "<Benchmark>"
        yield "inline-test", re.compile(
            r"(?m)^\s*\[Xunit\.(?:Fact|Theory)\b",
        ), "qualified .NET test attribute"
        yield "inline-test", re.compile(
            r"(?m)^\s*\[NUnit\.Framework\.(?:Test|TestCase|SetUp|TearDown|OneTimeSetUp|OneTimeTearDown)\b",
        ), "qualified NUnit test attribute"
        yield "inline-test", re.compile(
            r"(?m)^\s*\[Microsoft\.VisualStudio\.TestTools\.UnitTesting\.(?:TestMethod|DataTestMethod|TestInitialize|TestCleanup|ClassInitialize|ClassCleanup)\b",
        ), "qualified MSTest attribute"
    elif suffix == ".swift":
        yield "inline-test", re.compile(r"(?m)^\s*(?:@\w+\s+)*func\s+test(?:[A-Z0-9_]\w*)?\s*\("), "func test..."
        yield "inline-test", re.compile(r"(?m)^\s*@Test\b"), "@Test"
    elif suffix == ".php":
        yield "inline-test", re.compile(r"(?mi)^\s*(?:public\s+)?function\s+test(?:[A-Z0-9_]\w*)?\s*\("), "function test..."
        yield "inline-test", re.compile(r"(?m)^\s*#\[\s*Test\s*\]"), "#[Test]"
    elif suffix in {".rb", ".rake", ".gemspec"}:
        yield "inline-test", re.compile(r"(?m)^\s*def\s+test_\w+"), "def test_..."
        yield "inline-test", re.compile(r"(?m)^\s*(?:describe|context|it)\b.*(?:do|\{)\s*$"), "RSpec example block"
        yield "inline-benchmark", re.compile(r"(?m)^\s*benchmark\b.*(?:do|\{)\s*$"), "benchmark block"
    elif suffix in {".ex", ".exs"} and re.search(r"(?m)^\s*use\s+ExUnit\.Case\b", clean):
        yield "inline-test", re.compile(r"(?m)^\s*(?:describe|test)\b.*\bdo\s*$"), "ExUnit test block"
    elif suffix == ".dart":
        yield "inline-test", re.compile(r"(?m)^\s*(?:group|test|testWidgets)\s*\("), "Dart test call"
        yield "inline-benchmark", re.compile(r"(?m)^\s*(?:benchmark|measure)\s*\("), "Dart benchmark call"
    elif suffix == ".jl":
        yield "inline-test", re.compile(r"(?m)^\s*@(?:test|testset)\b"), "@test/@testset"
        yield "inline-benchmark", re.compile(r"(?m)^\s*@(?:benchmark|btime)\b"), "@benchmark/@btime"
    elif suffix in {".ml", ".mli"}:
        yield "inline-test", re.compile(r"\blet%(?:test|test_unit|expect_test)\b"), "let%test"
        yield "inline-benchmark", re.compile(r"\bBench\.Test\.create\b"), "Bench.Test.create"
    elif suffix in {".hs", ".lhs"} and re.search(
        r"(?m)^\s*import\s+(?:qualified\s+)?(?:Test\.Hspec|Test\.Tasty|Test\.QuickCheck)\b", clean
    ):
        yield "inline-test", re.compile(r"(?m)^\s*(?:describe|it|testCase|testGroup|property|hspec)\b"), "Hspec/Tasty/QuickCheck declaration"
    elif suffix == ".r" and re.search(
        r"(?m)^\s*(?:library|require)\s*\(\s*[\"']testthat[\"']\s*\)|\btestthat::", comments_only
    ):
        yield "inline-test", re.compile(r"(?m)^\s*(?:test_that|test_check)\s*\("), "testthat declaration"
    elif suffix == ".cr" and re.search(r"(?m)^\s*require\s+[\"']spec[\"']", comments_only):
        yield "inline-test", re.compile(r"(?m)^\s*(?:describe|context|it)\b.*\bdo\s*$"), "Crystal spec block"
    elif suffix == ".tcl" and re.search(r"(?m)^\s*package\s+require\s+tcltest\b", clean):
        yield "inline-test", re.compile(r"(?m)^\s*::?tcltest::test\s+|^\s*test\s+\S+\s+\S+"), "tcltest declaration"
    elif suffix == ".sol":
        yield "inline-test", re.compile(r"(?m)^\s*contract\s+\w*Test\b|^\s*function\s+(?:test|invariant)\w*\s*\("), "Foundry test declaration"
    elif suffix == ".v":
        yield "inline-test", re.compile(r"(?m)^\s*fn\s+test_[A-Za-z0-9_]\w*\s*\("), "V test function"
    elif suffix in {".clj", ".cljs", ".cljc"}:
        yield "inline-test", re.compile(r"\(\s*deftest\b"), "(deftest ...)"
        yield "inline-benchmark", re.compile(r"\(\s*(?:bench|quick-bench)\b"), "Criterium benchmark form"
    elif suffix == ".lua":
        yield "inline-test", re.compile(r"(?m)^\s*(?:describe|it)\s*\("), "Busted test call"
    elif suffix in {".pl", ".pm", ".t"} and re.search(
        r"(?m)^\s*use\s+Test::(?:More|Most|Simple)\b", clean
    ):
        yield "inline-test", re.compile(r"(?m)^\s*(?:ok|is|isnt|like|unlike|cmp_ok|subtest)\s*\("), "Test::More assertion"
    elif suffix in {".pl", ".pm", ".t"} and re.search(
        r"(?m)^\s*use\s+Benchmark\b", clean
    ):
        yield "inline-benchmark", re.compile(r"(?m)^\s*(?:timethese|cmpthese)\s*\("), "Perl Benchmark call"
    elif suffix in {".sh", ".bash", ".zsh", ".fish"}:
        yield "inline-test", re.compile(r"(?m)^\s*@test\s+.*\{"), "Bats @test block"
        if re.search(r"(?m)^\s*(?:\.|source)\s+\S*shunit2\b", clean):
            yield "inline-test", re.compile(r"(?m)^\s*test[A-Z0-9_]\w*\s*\(\s*\)\s*\{"), "shUnit test function"


def inline_test_findings(
    path: Path,
    root: Path,
    configured_roots: Sequence[Path | str | TestSourceRoot] = (),
) -> list[Finding]:
    """Find structurally distinctive inline tests in a non-test source file."""
    if is_test_source(path, root, configured_roots):
        return []
    suffix = path.suffix.lower()
    if suffix and suffix not in SOURCE_EXTENSIONS:
        return []
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [Finding(
            "error",
            "inline-test-scan-failed",
            path,
            f"inline test/benchmark scan could not read authored source: {exc}",
            "tooling",
        )]
    if len(source) > 2_000_000 or any(len(line) > 100_000 for line in source.splitlines()):
        return [Finding(
            "error",
            "inline-test-scan-limit",
            path,
            "authored source exceeds the fail-closed inline scan size limit; split or regenerate it before acceptance",
            "tooling",
        )]
    comments_only = _strip_source(source, suffix, strings=False)
    clean = _strip_source(source, suffix)
    findings: list[Finding] = []
    seen: set[tuple[str, int]] = set()
    for code, pattern, evidence in _rules(
        suffix,
        clean,
        comments_only,
        js_runner_configured=_javascript_runner_configured(root),
    ):
        for match in pattern.finditer(clean):
            line = clean.count("\n", 0, match.start()) + 1
            key = code, line
            if key in seen:
                continue
            seen.add(key)
            kind = "benchmark" if code == "inline-benchmark" else "test"
            findings.append(Finding(
                "error",
                code,
                path,
                f"inline {kind} syntax `{evidence}` at line {line}; move it to a conventional {kind} file or directory",
                "syntax",
            ))
    return findings
