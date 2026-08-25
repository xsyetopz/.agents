#!/usr/bin/env python3
"""Language-specific inline-test and benchmark pattern rules."""

from __future__ import annotations

import re
from collections.abc import Iterable


def _rules(
    suffix: str, clean: str, comments_only: str, *, js_runner_configured: bool = False
) -> Iterable[tuple[str, re.Pattern[str], str]]:
    flags = re.MULTILINE
    if suffix == ".rs":
        yield (
            "inline-test",
            re.compile(
                r"#\s*\[\s*(?:(?:async_std|tokio)::test|rstest|test|test_case)\b[^\]]*\]",
                flags,
            ),
            "Rust test attribute",
        )
        yield "inline-benchmark", re.compile(r"#\s*\[\s*bench\s*\]", flags), "#[bench]"
        yield (
            "inline-test",
            re.compile(r"\bmod\s+(?:test|tests)\s*\{", flags),
            "inline test module",
        )
        yield (
            "inline-benchmark",
            re.compile(r"\bmod\s+(?:bench|benches|benchmark|benchmarks)\s*\{", flags),
            "inline benchmark module",
        )
        yield (
            "inline-test",
            re.compile(
                r"#\s*\[\s*cfg\s*\([^\]]*\btest\b[^\]]*\)\s*\]\s*"
                r"(?:(?:#\s*\[[^\]]*\])\s*)*"
                r"(?:pub(?:\s*\([^)]*\))?\s+)?(?:async\s+)?(?:"
                r"mod\s+\w+\s*\{|(?:const|enum|fn|impl|static|struct|trait|type|use)\b)",
                flags,
            ),
            "#[cfg(test)] body item",
        )
    elif suffix == ".zig":
        yield "inline-test", re.compile(r"(?m)^\s*test(?:\s+.*?)?\s*\{"), "test {"
    elif suffix == ".d":
        yield "inline-test", re.compile(r"\bunittest\s*\{", flags), "unittest {"
    elif suffix == ".nim" and re.search(
        r"(?m)^\s*(?:import|from)\s+(?:std/)?unittest\b", clean
    ):
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:suite|test)\b[^:]*:"),
            "unittest suite/test block",
        )
    elif suffix in {".erl", ".hrl"} and re.search(
        r"-include(?:_lib)?\s*\(\s*[\"'][^\"']*eunit[^\"']*[\"']\s*\)", comments_only
    ):
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*[a-z][a-zA-Z0-9_]*_test_?\s*\(\s*\)\s*->"),
            "EUnit _test function",
        )
        yield (
            "inline-test",
            re.compile(
                r"\?(?:assert|assertEqual|assertMatch|assertNot|assertNotEqual)\b"
            ),
            "EUnit assertion macro",
        )
    elif suffix == ".erl" and re.search(
        r"-include(?:_lib)?\s*\(\s*[\"'][^\"']*common_test[^\"']*[\"']\s*\)",
        comments_only,
    ):
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:all|init_per_suite|end_per_suite)\s*\("),
            "Common Test callback",
        )
    elif suffix == ".go":
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*func\s+Test[A-Z0-9_]\w*\s*\("),
            "func Test...",
        )
        yield (
            "inline-benchmark",
            re.compile(r"(?m)^\s*func\s+Benchmark[A-Z0-9_]\w*\s*\("),
            "func Benchmark...",
        )
    elif suffix in {".py", ".pyi", ".pyw"}:
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:async\s+)?def\s+test(?:_\w+)?\s*\("),
            "def test...",
        )
        yield (
            "inline-test",
            re.compile(
                r"(?m)^\s*class\s+Test\w*\s*\([^)]*(?:TestCase|unittest)[^)]*\):",
            ),
            "unittest TestCase class",
        )
        yield (
            "inline-benchmark",
            re.compile(r"(?m)^\s*(?:async\s+)?def\s+benchmark_\w+\s*\("),
            "def benchmark_...",
        )
        yield (
            "inline-benchmark",
            re.compile(r"(?m)^\s*@pytest\.mark\.benchmark\b"),
            "@pytest.mark.benchmark",
        )
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*@pytest\.mark\.(?:parametrize|asyncio)\b"),
            "pytest test marker",
        )
    elif suffix in {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts"}:
        if (
            js_runner_configured
            or re.search(
                r"(?m)^\s*(?:import\b.*\b(?:describe|it|suite)\b.*\bfrom\s*|"
                r"(?:const|let|var)\s+.*\b(?:describe|it|suite)\b.*=\s*require\s*\()\s*"
                r"[\"'][^\"']*(?:bun:test|jest|node:test|vitest|mocha|jasmine)[^\"']*[\"']",
                comments_only,
            )
            or re.search(
                r"(?m)^\s*(?:describe|it|suite)(?:\.(?:each|only|skip|concurrent))?\s*\(\s*['\"`][^'\"`\n]+['\"`]\s*,\s*"
                r"(?:async\s+)?(?:function\b|(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>)",
                comments_only,
            )
            or re.search(
                r"(?m)^\s*(?:describe|it|suite)\.(?:each|only|skip|concurrent)\s*\(",
                comments_only,
            )
        ):
            yield (
                "inline-test",
                re.compile(
                    r"(?m)^\s*(?:describe|it|suite)(?:\.(?:each|only|skip|concurrent))?\s*\("
                ),
                "test suite/example call",
            )
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:Bun|Deno)\.test\s*\("),
            "runtime test call",
        )
        if re.search(
            r"(?m)^\s*(?:import\b.*\btest\b.*\bfrom\s*|"
            r"(?:const|let|var)\s+.*\btest\b.*=\s*require\s*\()\s*"
            r"[\"'][^\"']*(?:bun:test|jest|node:test|vitest)[^\"']*[\"']",
            comments_only,
        ):
            yield (
                "inline-test",
                re.compile(r"(?m)^\s*test(?:\.(?:each|only|skip|concurrent))?\s*\("),
                "framework-imported test call",
            )
        if re.search(
            r"(?m)^\s*test(?:\.(?:each|only|skip|concurrent))?\s*\(\s*['\"`][^'\"`\n]+['\"`]\s*,\s*"
            r"(?:async\s+)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>",
            comments_only,
        ) or re.search(
            r"(?m)^\s*test\.(?:each|only|skip|concurrent)\s*\(", comments_only
        ):
            yield (
                "inline-test",
                re.compile(r"(?m)^\s*test(?:\.(?:each|only|skip|concurrent))?\s*\("),
                "structural framework test call",
            )
        yield (
            "inline-benchmark",
            re.compile(r"(?m)^\s*(?:bench|benchmark)\s*\("),
            "bench/benchmark call",
        )
    elif suffix in {".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".hxx"}:
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:TEST|TEST_F|TEST_P|TYPED_TEST)\s*\("),
            "C++ test macro",
        )
        yield (
            "inline-test",
            re.compile(
                r"(?m)^\s*(?:TEST_CASE|TEST_CASE_METHOD|TEST_CASE_TEMPLATE|SCENARIO)\s*\(",
            ),
            "Catch2/doctest test macro",
        )
        yield (
            "inline-benchmark",
            re.compile(r"(?m)^\s*BENCHMARK(?:_F)?\s*\("),
            "C++ benchmark macro",
        )
    elif suffix in {".java", ".kt", ".kts", ".scala", ".groovy"}:
        if re.search(
            r"(?m)^\s*import\s+(?:static\s+)?(?:"
            r"org\.junit(?:\.jupiter\.api)?\.(?:Test|ParameterizedTest|RepeatedTest|\*)|"
            r"org\.testng\.annotations\.(?:Test|\*)|"
            r"kotlin\.test\.(?:Test|\*)|org\.openjdk\.jmh\.annotations\.Benchmark)",
            comments_only,
        ):
            yield (
                "inline-test",
                re.compile(
                    r"(?m)^\s*@(?:ParameterizedTest|RepeatedTest|Test|TestFactory|TestTemplate|BeforeEach|AfterEach|BeforeAll|AfterAll|Before|After|BeforeMethod|AfterMethod|BeforeClass|AfterClass|DataProvider)\b"
                ),
                "@Test",
            )
            yield "inline-benchmark", re.compile(r"(?m)^\s*@Benchmark\b"), "@Benchmark"
        yield (
            "inline-test",
            re.compile(
                r"(?m)^\s*@org\.(?:junit|testng)\.(?:ParameterizedTest|RepeatedTest|Test|TestFactory|TestTemplate|BeforeEach|AfterEach|BeforeAll|AfterAll|Before|After|BeforeMethod|AfterMethod|BeforeClass|AfterClass|DataProvider)\b",
            ),
            "qualified @Test",
        )
        yield (
            "inline-benchmark",
            re.compile(
                r"(?m)^\s*@org\.openjdk\.jmh\.annotations\.Benchmark\b",
            ),
            "qualified @Benchmark",
        )
    elif suffix in {".cs", ".fs", ".fsx", ".vb"}:
        dotnet_framework = re.search(
            r"(?mi)^\s*(?:using|open|imports?)\s+(?:xunit|nunit|microsoft\.visualstudio\.testtools\.unittesting|benchmarkdotnet)\b",
            comments_only,
        )
        if dotnet_framework:
            yield (
                "inline-test",
                re.compile(
                    r"(?m)^\s*\[(?:Fact|Theory|Test|TestCase|SetUp|TearDown|OneTimeSetUp|OneTimeTearDown)\b"
                ),
                "[Fact]/[Test]",
            )
            yield (
                "inline-test",
                re.compile(
                    r"(?m)^\s*\[(?:TestMethod|DataTestMethod|TestInitialize|TestCleanup|ClassInitialize|ClassCleanup)\b"
                ),
                "[TestMethod]",
            )
            yield (
                "inline-test",
                re.compile(r"(?m)^\s*\[<(?:Fact|Theory|Test|TestCase)\b[^>]*>\]"),
                "[<Fact>]/[<Test>]",
            )
            yield (
                "inline-test",
                re.compile(r"(?mi)^\s*<(?:Fact|Theory|Test|TestCase)\b[^>]*>"),
                "<Fact>/<Test>",
            )
            yield (
                "inline-benchmark",
                re.compile(r"(?m)^\s*\[(?:Benchmark|BenchmarkDotNet)\b"),
                "[Benchmark]",
            )
            yield (
                "inline-benchmark",
                re.compile(r"(?m)^\s*\[<(?:Benchmark|BenchmarkDotNet)\b[^>]*>\]"),
                "[<Benchmark>]",
            )
            yield (
                "inline-benchmark",
                re.compile(r"(?mi)^\s*<(?:Benchmark|BenchmarkDotNet)\b[^>]*>"),
                "<Benchmark>",
            )
        yield (
            "inline-test",
            re.compile(
                r"(?m)^\s*\[Xunit\.(?:Fact|Theory)\b",
            ),
            "qualified .NET test attribute",
        )
        yield (
            "inline-test",
            re.compile(
                r"(?m)^\s*\[NUnit\.Framework\.(?:Test|TestCase|SetUp|TearDown|OneTimeSetUp|OneTimeTearDown)\b",
            ),
            "qualified NUnit test attribute",
        )
        yield (
            "inline-test",
            re.compile(
                r"(?m)^\s*\[Microsoft\.VisualStudio\.TestTools\.UnitTesting\.(?:TestMethod|DataTestMethod|TestInitialize|TestCleanup|ClassInitialize|ClassCleanup)\b",
            ),
            "qualified MSTest attribute",
        )
    elif suffix == ".swift":
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:@\w+\s+)*func\s+test(?:[A-Z0-9_]\w*)?\s*\("),
            "func test...",
        )
        yield "inline-test", re.compile(r"(?m)^\s*@Test\b"), "@Test"
    elif suffix == ".php":
        yield (
            "inline-test",
            re.compile(r"(?mi)^\s*(?:public\s+)?function\s+test(?:[A-Z0-9_]\w*)?\s*\("),
            "function test...",
        )
        yield "inline-test", re.compile(r"(?m)^\s*#\[\s*Test\s*\]"), "#[Test]"
    elif suffix in {".rb", ".rake", ".gemspec"}:
        yield "inline-test", re.compile(r"(?m)^\s*def\s+test_\w+"), "def test_..."
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:describe|context|it)\b.*(?:do|\{)\s*$"),
            "RSpec example block",
        )
        yield (
            "inline-benchmark",
            re.compile(r"(?m)^\s*benchmark\b.*(?:do|\{)\s*$"),
            "benchmark block",
        )
    elif suffix in {".ex", ".exs"} and re.search(
        r"(?m)^\s*use\s+ExUnit\.Case\b", clean
    ):
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:describe|test)\b.*\bdo\s*$"),
            "ExUnit test block",
        )
    elif suffix == ".dart":
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:group|test|testWidgets)\s*\("),
            "Dart test call",
        )
        yield (
            "inline-benchmark",
            re.compile(r"(?m)^\s*(?:benchmark|measure)\s*\("),
            "Dart benchmark call",
        )
    elif suffix == ".jl":
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*@(?:test|testset)\b"),
            "@test/@testset",
        )
        yield (
            "inline-benchmark",
            re.compile(r"(?m)^\s*@(?:benchmark|btime)\b"),
            "@benchmark/@btime",
        )
    elif suffix in {".ml", ".mli"}:
        yield (
            "inline-test",
            re.compile(r"\blet%(?:test|test_unit|expect_test)\b"),
            "let%test",
        )
        yield (
            "inline-benchmark",
            re.compile(r"\bBench\.Test\.create\b"),
            "Bench.Test.create",
        )
    elif suffix in {".hs", ".lhs"} and re.search(
        r"(?m)^\s*import\s+(?:qualified\s+)?(?:Test\.Hspec|Test\.Tasty|Test\.QuickCheck)\b",
        clean,
    ):
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:describe|it|testCase|testGroup|property|hspec)\b"),
            "Hspec/Tasty/QuickCheck declaration",
        )
    elif suffix == ".r" and re.search(
        r"(?m)^\s*(?:library|require)\s*\(\s*[\"']testthat[\"']\s*\)|\btestthat::",
        comments_only,
    ):
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:test_that|test_check)\s*\("),
            "testthat declaration",
        )
    elif suffix == ".cr" and re.search(
        r"(?m)^\s*require\s+[\"']spec[\"']", comments_only
    ):
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:describe|context|it)\b.*\bdo\s*$"),
            "Crystal spec block",
        )
    elif suffix == ".tcl" and re.search(
        r"(?m)^\s*package\s+require\s+tcltest\b", clean
    ):
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*::?tcltest::test\s+|^\s*test\s+\S+\s+\S+"),
            "tcltest declaration",
        )
    elif suffix == ".sol":
        yield (
            "inline-test",
            re.compile(
                r"(?m)^\s*contract\s+\w*Test\b|^\s*function\s+(?:test|invariant)\w*\s*\("
            ),
            "Foundry test declaration",
        )
    elif suffix == ".v":
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*fn\s+test_[A-Za-z0-9_]\w*\s*\("),
            "V test function",
        )
    elif suffix in {".clj", ".cljs", ".cljc"}:
        yield "inline-test", re.compile(r"\(\s*deftest\b"), "(deftest ...)"
        yield (
            "inline-benchmark",
            re.compile(r"\(\s*(?:bench|quick-bench)\b"),
            "Criterium benchmark form",
        )
    elif suffix == ".lua":
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:describe|it)\s*\("),
            "Busted test call",
        )
    elif suffix in {".pl", ".pm", ".t"} and re.search(
        r"(?m)^\s*use\s+Test::(?:More|Most|Simple)\b", clean
    ):
        yield (
            "inline-test",
            re.compile(r"(?m)^\s*(?:ok|is|isnt|like|unlike|cmp_ok|subtest)\s*\("),
            "Test::More assertion",
        )
    elif suffix in {".pl", ".pm", ".t"} and re.search(
        r"(?m)^\s*use\s+Benchmark\b", clean
    ):
        yield (
            "inline-benchmark",
            re.compile(r"(?m)^\s*(?:timethese|cmpthese)\s*\("),
            "Perl Benchmark call",
        )
    elif suffix in {".sh", ".bash", ".zsh", ".fish"}:
        yield "inline-test", re.compile(r"(?m)^\s*@test\s+.*\{"), "Bats @test block"
        if re.search(r"(?m)^\s*(?:\.|source)\s+\S*shunit2\b", clean):
            yield (
                "inline-test",
                re.compile(r"(?m)^\s*test[A-Z0-9_]\w*\s*\(\s*\)\s*\{"),
                "shUnit test function",
            )
