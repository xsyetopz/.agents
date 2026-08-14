"""Inline-test and audit-threshold regression tests."""

from __future__ import annotations

import json
import unittest

import audit_architecture
from test_support import AuditFixture


class AuditArchitectureInlineTests(AuditFixture, unittest.TestCase):

    def test_inline_rust_tests_and_benchmarks_report_syntax_and_lines(self) -> None:
        findings = self.inline_findings(
            "src/codec.rs",
            "pub fn encode() {}\n\n#[cfg(test)]\nmod tests {\n"
            "    #[test]\n    fn round_trip() {}\n"
            "    #[bench]\n    fn throughput() {}\n}\n",
        )
        self.assertEqual(self.codes(findings), {"inline-test", "inline-benchmark"})
        self.assertTrue(all(item.evidence == "syntax" for item in findings))
        self.assertTrue(any("`inline test module` at line 4" in item.message for item in findings))
        self.assertTrue(any("move it to a conventional benchmark file" in item.message for item in findings))

    def test_inline_rust_bench_modules_and_framework_attributes_are_detected(self) -> None:
        cases = (
            "mod benches {\n}\n",
            "mod benchmarks {\n}\n",
            "#[test_case(1)]\nfn case(value: usize) {}\n",
            "#[rstest]\nfn case() {}\n",
            "#[tokio::test]\nasync fn case() {}\n",
            "#[async_std::test]\nasync fn case() {}\n",
        )
        for content in cases:
            expected = "inline-benchmark" if content.startswith(("mod benches", "mod benchmarks")) else "inline-test"
            self.assertIn(expected, self.codes(self.inline_findings("src/codec.rs", content)))

    def test_inline_rust_external_modules_and_path_modules_are_allowed(self) -> None:
        for content in (
            "#[cfg(test)]\nmod tests;\n",
            '#[cfg(test)]\n#[path = "codec_tests.rs"]\nmod tests;\n',
        ):
            self.assertEqual(self.inline_findings("src/codec.rs", content), [])

    def test_rust_cfg_test_with_intermediate_attribute_is_detected(self) -> None:
        findings = self.inline_findings(
            "src/codec.rs",
            "#[cfg(test)]\n#[allow(dead_code)]\nmod support { }\n",
        )
        self.assertIn("inline-test", self.codes(findings))

    def test_exact_test_paths_are_exempt_without_test_substring_exemption(self) -> None:
        cases = (
            "tests/codec.rs",
            "crate/tests/codec.rs",
            "crate/benches/codec.rs",
            "crate/integration-tests/codec.rs",
            "crate/test-fixtures/codec.rs",
            "src/codec_tests.rs",
            "src/_tests.rs",
            "src/codec/tests.rs",
            "src/codec_bench.rs",
            "src/codec.bench.ts",
            "src/codec.benchmark.js",
            "src/codec_test.ts",
            "src/codec_spec.ts",
            "src/ParserTest.java",
        )
        for relative in cases:
            self.assertEqual(
                self.inline_findings(relative, "#[test]\nfn round_trip() {}\n"),
                [],
                relative,
            )
        findings = self.inline_findings(
            "src/contest/attestation.rs",
            "#[test]\nfn round_trip() {}\n",
        )
        self.assertEqual(self.codes(findings), {"inline-test"})
        contest = self.inline_findings("src/Contest.java", "@Test\nvoid roundTrip() {}\n")
        self.assertEqual(contest, [])

    def test_comments_and_strings_do_not_create_inline_findings(self) -> None:
        cases = {
            "src/codec.rs": (
                '// #[test]\n/* mod tests { #[bench] fn speed() {} } */\n'
                'const NOTE: &str = r#"mod tests { #[test] fn fake() {} }"#;\n'
            ),
            "src/codec.py": (
                '# def test_fake():\n'
                'NOTE = """def test_embedded():\n    pass\n"""\n'
            ),
            "src/codec.ts": (
                '// test("fake", () => {})\n'
                'const note = "describe(\\"fake\\", () => {})";\n'
            ),
        }
        for relative, content in cases.items():
            self.assertEqual(self.inline_findings(relative, content), [], relative)

    def test_language_block_comments_do_not_create_inline_findings(self) -> None:
        cases = {
            "src/codec.d": "/+ unittest { assert(true); } +/\n",
            "src/codec.hs": "import Test.Hspec\n{- describe \"fake\" -}\n",
            "src/codec.jl": "#= @testset \"fake\" begin =#\n",
            "src/codec.lua": "--[=[ describe(\"fake\", function() end) ]=]\nlocal note = [=[it(\"fake\", function() end) ]=]\n",
            "src/codec.nim": "import std/unittest\n#[ suite \"fake\": ]#\n",
            "src/codec.rb": "=begin\ndescribe \"fake\" do\n=end\n",
            "src/codec.sh": "cat <<'EOF'\n@test \"fake\" { true; }\nEOF\n",
        }
        for relative, content in cases.items():
            self.assertEqual(self.inline_findings(relative, content), [], relative)

    def test_unclosed_literals_do_not_hide_later_inline_tests(self) -> None:
        cases = {
            "src/codec.rs": 'const note = "unterminated\n#[test]\nfn round_trip() {}\n',
            "src/codec.py": 'note = "unterminated\ndef test_round_trip():\n    pass\n',
        }
        for relative, content in cases.items():
            self.assertIn("inline-test", self.codes(self.inline_findings(relative, content)), relative)

    def test_rust_lifetimes_do_not_mask_later_inline_tests(self) -> None:
        findings = self.inline_findings(
            "src/codec.rs",
            "fn borrow<'a>(value: &'a str) -> &'a str { value }\n"
            "#[test]\nfn round_trip() {}\n",
        )
        self.assertIn("inline-test", self.codes(findings))

    def test_go_benchmark_suffix_is_not_a_test_source_convention(self) -> None:
        findings = self.inline_findings(
            "src/codec_bench.go",
            "func BenchmarkCodec(b *testing.B) {}\n",
        )
        self.assertIn("inline-benchmark", self.codes(findings))

    def test_perl_t_root_is_language_specific(self) -> None:
        self.assertEqual(
            self.inline_findings("t/codec.t", "use Test::More;\nok(1);\n"),
            [],
        )
        findings = self.inline_findings("t/codec.rs", "#[test]\nfn round_trip() {}\n")
        self.assertIn("inline-test", self.codes(findings))

    def test_java_annotations_require_framework_evidence(self) -> None:
        self.assertEqual(
            self.inline_findings(
                "src/Codec.java",
                "@interface Test {}\n@Test\nvoid productionMethod() {}\n",
            ),
            [],
        )

    def test_additional_framework_markers_are_detected(self) -> None:
        cases = {
            "src/codec.cpp": "TEST_CASE(\"round trip\") {}\n",
            "src/codec.cs": "using Microsoft.VisualStudio.TestTools.UnitTesting;\n[TestMethod]\npublic void RoundTrip() {}\n",
        }
        for relative, content in cases.items():
            self.assertIn("inline-test", self.codes(self.inline_findings(relative, content)), relative)

    def test_global_javascript_test_requires_structural_callback(self) -> None:
        source = 'test("round trip", () => {});\n'
        findings = self.inline_findings("src/codec.ts", source)
        self.assertIn("inline-test", self.codes(findings))
        self.assertEqual(self.inline_findings("src/codec.ts", "test(codec);\n"), [])
        self.assertIn(
            "inline-test",
            self.codes(self.inline_findings("src/codec.ts", 'describe("codec", () => {});\n')),
        )
        self.assertIn(
            "inline-test",
            self.codes(self.inline_findings("src/codec.ts", 'test.each([[1]])("codec", () => {});\n')),
        )

    def test_reviewed_custom_test_source_root_is_exempt_and_visible(self) -> None:
        self.write("qa/Codec.java", content="import org.junit.Test;\n@Test\nvoid roundTrip() {}\n")
        self.write_contract(test_source_roots=[{
            "path": "qa",
            "reason": "JUnit source set declared by the build runner",
            "owner": "quality platform",
            "control": "JUnit source-set discovery check",
            "review": "remove on build runner upgrade",
        }])
        findings = self.findings()
        self.assertIn("inline-test", self.codes(findings))
        self.assertIn("unsupported-test-source-root", self.codes(findings))
        self.assertNotIn("configured-test-source-root", self.codes(findings))

    def test_custom_test_source_root_contract_is_strict_and_stale(self) -> None:
        self.write_contract(test_source_roots=[{
            "path": "qa/*",
            "reason": "JUnit source set declared by the build runner",
            "owner": "quality platform",
            "control": "JUnit source-set discovery check",
            "review": "remove on build runner upgrade",
        }, {
            "path": "missing",
            "reason": "JUnit source set declared by the build runner",
            "owner": "quality platform",
            "control": "JUnit source-set discovery check",
            "review": "remove on build runner upgrade",
        }])
        findings = self.findings()
        self.assertIn("invalid-test-source-root", self.codes(findings))
        self.assertIn("stale-test-source-root", self.codes(findings))

    def test_distinctive_native_inline_test_constructs_are_detected(self) -> None:
        cases = {
            "src/codec.zig": 'test "round trip" { try expect(true); }\n',
            "src/codec.d": "unittest { assert(true); }\n",
            "src/codec.nim": 'import std/unittest\nsuite "codec":\n  test "round trip": discard\n',
            "src/codec.erl": (
                '-include_lib("eunit/include/eunit.hrl").\n'
                "round_trip_test() -> ?assert(true).\n"
            ),
        }
        for relative, content in cases.items():
            self.assertIn("inline-test", self.codes(self.inline_findings(relative, content)), relative)

    def test_explicit_cross_language_test_and_benchmark_markers_are_detected(self) -> None:
        test_cases = {
            "src/codec.go": "func TestRoundTrip(t *testing.T) {}\n",
            "src/codec.py": "def test_round_trip():\n    pass\n",
            "src/codec_unittest.py": "import unittest\nclass TestCodec(unittest.TestCase):\n    pass\n",
            "src/codec.ts": 'import { test } from "vitest";\ntest("round trip", () => {});\n',
            "src/codec.cpp": "TEST(Codec, RoundTrip) {}\n",
            "src/Codec.java": "import org.junit.Test;\n@Test\nvoid roundTrip() {}\n",
            "src/Codec.cs": "using Xunit;\n[Fact]\npublic void RoundTrip() {}\n",
            "src/Codec.swift": "func testRoundTrip() {}\n",
            "src/Codec.php": "public function testRoundTrip() {}\n",
            "src/codec.rb": "def test_round_trip\nend\n",
            "src/codec.ex": 'use ExUnit.Case\ntest "round trip" do\nend\n',
            "src/codec.dart": 'test("round trip", () {});\n',
            "src/codec.jl": '@testset "codec" begin\nend\n',
            "src/codec.ml": "let%test_unit \"codec\" = ()\n",
            "src/codec.clj": "(deftest round-trip (is true))\n",
            "src/codec.lua": 'describe("codec", function() end)\n',
            "src/codec.pl": "use Test::More;\nok(1);\n",
            "src/codec.sh": '@test "codec" { true; }\n',
        }
        for relative, content in test_cases.items():
            self.assertIn("inline-test", self.codes(self.inline_findings(relative, content)), relative)

        benchmark_cases = {
            "src/codec.go": "func BenchmarkCodec(b *testing.B) {}\n",
            "src/codec.ts": 'bench("codec", () => {});\n',
            "src/codec.cpp": "BENCHMARK(run_codec);\n",
            "src/Codec.java": "import org.openjdk.jmh.annotations.Benchmark;\n@Benchmark\npublic void codec() {}\n",
            "src/Codec.cs": "using BenchmarkDotNet.Attributes;\n[Benchmark]\npublic void Codec() {}\n",
            "src/codec.jl": "@benchmark encode(data)\n",
        }
        for relative, content in benchmark_cases.items():
            self.assertIn(
                "inline-benchmark",
                self.codes(self.inline_findings(relative, content)),
                relative,
            )

    def test_framework_words_without_structural_evidence_are_not_flagged(self) -> None:
        cases = {
            "src/codec.ts": 'function test(value: unknown) { return value; }\ntest(codec);\n',
            "src/codec.nim": 'let note = "import unittest; test fake:"\n',
            "src/codec.erl": '% -include_lib("eunit/include/eunit.hrl").\nround_trip_test() -> ok.\n',
            "src/codec.ex": 'test = "not ExUnit"\n',
            "src/codec.pl": 'my $note = "use Test::More; ok(1);";\n',
        }
        for relative, content in cases.items():
            self.assertEqual(self.inline_findings(relative, content), [], relative)

    def test_audit_reports_inline_tests_and_rejects_naming_exceptions_for_them(self) -> None:
        self.write("src/codec.rs", content="#[test]\nfn round_trip() {}\n")
        self.write_contract(naming_exceptions=[self.exception(rule="inline-test", path="src/codec.rs")])
        findings = self.findings()
        self.assertIn("inline-test", self.codes(findings))
        self.assertIn("invalid-naming-exception", self.codes(findings))
        self.assertNotIn("naming-exception", self.codes(findings))

    def test_inline_test_gate_covers_conditional_cfg_and_generated_output_when_requested(self) -> None:
        self.write("src/codec.rs", content="#[cfg(any(test, feature = \"fast\"))]\nfn check() {}\n")
        self.write("generated/codec.rs", content="// @generated\n#[test]\nfn generated_check() {}\n")
        findings = self.findings()
        self.assertIn("inline-test", self.codes(findings))
        self.assertFalse(any(item.path.name == "codec.rs" and item.code == "inline-test" and item.path.parent.name == "generated" for item in findings))
        included = self.findings(include_generated=True)
        self.assertTrue(any(item.path.parent.name == "generated" and item.code == "inline-test" for item in included))

    def test_inline_scan_fails_closed_on_invalid_source_encoding(self) -> None:
        path = self.root / "src" / "codec.rs"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"#[test]\nfn invalid() {}\n\xff")
        findings = audit_architecture.inline_test_findings(path, self.root)
        self.assertEqual([item.code for item in findings], ["inline-test-scan-failed"])
        self.assertEqual(findings[0].evidence, "tooling")
    def test_inline_scan_fails_closed_on_pathological_single_line_source(self) -> None:
        path = self.write("src/bundle.ts", content="x" * 100_001)
        findings = audit_architecture.inline_test_findings(path, self.root)
        self.assertEqual([item.code for item in findings], ["inline-test-scan-limit"])
        self.assertEqual(findings[0].evidence, "tooling")

    def test_line_thresholds_and_visible_generated_exemption(self) -> None:
        self.write("src/large.py", lines=9)
        self.write("src/generated/huge.py", content="# @generated\n" + "x\n" * 19)
        findings = self.findings(soft=3, strong=5, hard=8)
        self.assertEqual([item.path.name for item in findings if item.code == "hard-lines"], ["large.py"])
        self.assertEqual([item.message.split()[0] for item in findings if item.code == "exempt-artifact"], ["generated"])

    def test_generated_inclusion_restores_structural_checks(self) -> None:
        self.write("generated/helpers/utils.py", content="# @generated; do not edit\n")
        excluded = self.findings()
        self.assertEqual(self.codes(excluded), {"exempt-artifact"})
        included = self.findings(include_generated=True)
        self.assertTrue({"generic-directory", "generic-file"} <= self.codes(included))
        self.assertNotIn("exempt-artifact", self.codes(included))

    def test_three_semantic_tokens_fail_across_language_families(self) -> None:
        names = (
            "run-status-codec.ts", "run_status_codec.py", "run-status-codec.rb",
            "run_status_codec.rs", "run_status_codec.go", "run-status-codec.c",
            "run_status_codec.hpp", "run-status-codec.cs", "run-status-codec.java",
            "run-status-codec.kt",
        )
        for name in names:
            self.write(f"src/{name}")
        long_paths = {item.path.name for item in self.findings() if item.code == "semantic-token-limit"}
        self.assertEqual(long_paths, set(names))

    def exception(self, **changes: str) -> dict[str, str]:
        record = {
            "rule": "semantic-token-limit", "path": "src/run-status-codec.py",
            "reason": "compiler-owned public contract", "owner": "platform team",
            "control": "architecture test", "review": "remove after compiler upgrade",
        }
        record.update(changes)
        return record

    def write_contract(self, **sections: object) -> None:
        self.write(".architecture-enforcement.json", content=json.dumps(sections))

    def write_exceptions(self, records: object) -> None:
        self.write_contract(naming_exceptions=records)

    def write_artifact_exceptions(self, records: object) -> None:
        self.write_contract(artifact_exemptions=records)


if __name__ == "__main__":
    unittest.main()
