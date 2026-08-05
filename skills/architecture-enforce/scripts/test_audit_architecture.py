#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest

import audit_architecture
from test_support import AuditFixture


class AuditArchitectureTests(AuditFixture, unittest.TestCase):

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

    def test_mixed_separators_and_architecture_config_are_audited(self) -> None:
        self.write("config/repository-security_tools.json")
        self.write("config/security.tool-runtime.yaml")
        paths = {item.path.name for item in self.findings() if item.code == "semantic-token-limit"}
        self.assertEqual(paths, {"repository-security_tools.json", "security.tool-runtime.yaml"})

    def test_test_spec_benchmark_and_declaration_suffixes_are_normalized(self) -> None:
        clean = (
            "test_run_codec.py", "run_codec_test.go", "run-codec.spec.ts",
            "run_codec_test.py", "run-codec.d.ts", "run-codec.d.mts",
            "run-codec.d.cts", "run_codec.pyi", "RunCodecTests.cs",
        )
        for name in clean:
            self.write(f"src/{name}")
        self.assertNotIn("semantic-token-limit", self.codes(self.findings()))

    def test_semantic_words_are_not_stripped_as_suffixes(self) -> None:
        for name in (
            "run-codec-runtime.ts", "run-codec-service.py", "run-codec-v1.rs",
            "run-codec-support.go", "security-tool-spec.ts", "security-tool-test.py",
            "security-tool-benchmark.rs",
        ):
            self.write(f"src/{name}")
        paths = {item.path.name for item in self.findings() if item.code == "semantic-token-limit"}
        self.assertEqual(len(paths), 7)

    def test_go_platform_markers_are_normalized(self) -> None:
        for name in ("packet_codec_linux_amd64.go", "packet_codec_windows.go", "packet_codec_test.go"):
            self.write(f"src/{name}")
        self.write("src/security_tool_amd64_linux.go")
        self.write("src/security_tool_unix.go")
        findings = self.findings()
        flagged = {item.path.name for item in findings if item.code == "semantic-token-limit"}
        self.assertNotIn("packet_codec_linux_amd64.go", flagged)
        self.assertEqual(flagged, {"security_tool_amd64_linux.go", "security_tool_unix.go"})

    def test_only_toolchain_defined_platform_markers_are_normalized(self) -> None:
        self.write("src/security-tool.jvm.kt")
        self.write("src/cloud-crypto-native.ts")
        findings = self.findings()
        paths = {item.path.name for item in findings if item.code == "semantic-token-limit"}
        self.assertNotIn("security-tool.jvm.kt", paths)
        self.assertIn("cloud-crypto-native.ts", paths)

    def test_platform_test_header_and_declaration_variants_deduplicate_logical_units(self) -> None:
        for name in (
            "destination-reader.ts", "destination-reader.test.ts", "destination-reader.d.ts",
            "destination_reader.go", "destination_reader_linux.go", "destination-reader.h",
            "destination-writer.ts", "destination-parser.ts",
        ):
            self.write(f"src/{name}")
        colonies = [item for item in self.findings(flat_limit=99) if item.code == "filename-colony"]
        self.assertEqual(len(colonies), 1)
        self.assertIn("3 sibling logical units", colonies[0].message)

    def test_exactly_three_sibling_units_form_colony_below_flat_limit(self) -> None:
        for name in ("catalog-reader.py", "catalog-writer.py", "catalog-index.py"):
            self.write(f"src/{name}")
        findings = self.findings(flat_limit=50)
        self.assertIn("filename-colony", self.codes(findings))
        self.assertNotIn("flat-cluster", self.codes(findings))

    def test_two_sibling_units_do_not_form_colony(self) -> None:
        self.write("src/rollout-plan.py")
        self.write("src/rollout-state.py")
        self.assertNotIn("filename-colony", self.codes(self.findings(flat_limit=50)))

    def test_redundant_ancestor_owner_is_an_error(self) -> None:
        self.write("src/security/security-policy.ts")
        self.write("src/security-tools/security-runtime.ts")
        self.write("src/repository-security/security-contract.ts")
        paths = {item.path.relative_to(self.root).as_posix() for item in self.findings() if item.code == "redundant-owner-prefix"}
        self.assertEqual(paths, {
            "src/security/security-policy.ts",
            "src/security-tools/security-runtime.ts",
            "src/repository-security/security-contract.ts",
        })

    def test_structural_directories_and_one_token_facades_are_not_owner_repetition(self) -> None:
        self.write("src/src-parser.py")
        self.write("src/security/security.py")
        self.write("tests/tests-support.py")
        self.assertNotIn("redundant-owner-prefix", self.codes(self.findings()))

    def test_camel_and_pascal_names_are_not_universally_word_counted(self) -> None:
        self.write("src/SecurityToolRuntime.java")
        self.write("src/securityToolRuntime.kt")
        self.write("src/HTTPServerCodec.cs")
        self.assertNotIn("semantic-token-limit", self.codes(self.findings()))

    def test_camel_and_pascal_names_participate_in_colony_and_owner_checks(self) -> None:
        for name in ("DestinationReader.java", "DestinationWriter.java", "DestinationParser.java"):
            self.write(f"src/destination/{name}")
        findings = self.findings(flat_limit=99)
        self.assertIn("filename-colony", self.codes(findings))
        redundant = {item.path.name for item in findings if item.code == "redundant-owner-prefix"}
        self.assertEqual(redundant, {"DestinationReader.java", "DestinationWriter.java", "DestinationParser.java"})

    def test_pascal_test_companions_deduplicate_from_source_units(self) -> None:
        for name in ("DestinationReader.java", "DestinationReaderTest.java", "DestinationReaderTests.java"):
            self.write(f"src/{name}")
        self.write("src/DestinationWriter.java")
        self.assertNotIn("filename-colony", self.codes(self.findings(flat_limit=99)))

    def test_camel_ancestor_words_participate_in_redundancy_checks(self) -> None:
        self.write("src/SecurityTools/SecurityRuntime.java")
        self.write("src/RepositorySecurity/SecurityContract.cs")
        paths = {item.path.name for item in self.findings() if item.code == "redundant-owner-prefix"}
        self.assertEqual(paths, {"SecurityRuntime.java", "SecurityContract.cs"})

    def test_manifest_migration_snapshot_and_vendor_exemption_bypasses_are_blocked(self) -> None:
        self.write("package.json", content="{}\n")
        self.write("migrations/20260101010101_create_security_tool.sql")
        self.write("snapshots/security-tool-contract.json")
        self.write("vendor/security-tool-contract.c")
        self.write_artifact_exceptions([
            {
                "class": "migration", "path": "migrations",
                "reason": "migration runner requires ordered timestamp filenames", "owner": "data platform",
                "control": "migration runner discovery test", "review": "remove on runner replacement",
            },
            {
                "class": "snapshot", "path": "snapshots",
                "reason": "golden snapshot contract for the public api", "owner": "quality platform",
                "control": "snapshot diff test", "review": "remove on runner upgrade",
            },
            {
                "class": "vendor", "path": "vendor",
                "reason": "upstream package source retained for offline builds", "owner": "supply chain",
                "control": "checksum and license gate", "review": "review on upstream version upgrade",
            },
        ])
        findings = self.findings()
        messages = [item.message for item in findings if item.code == "exempt-artifact"]
        self.assertEqual(len(messages), 2)
        self.assertTrue(all(message.startswith("framework") for message in messages))
        self.assertIn("unsupported-artifact-exemption", self.codes(findings))

    def test_timestamp_shape_does_not_self_exempt_an_authored_file(self) -> None:
        self.write("src/20260101_security-tool-contract.py")
        findings = self.findings()
        self.assertIn("semantic-token-limit", self.codes(findings))
        self.assertFalse(any(item.code == "exempt-artifact" for item in findings))

    def test_authored_schema_fixture_and_generated_phrases_do_not_self_exempt(self) -> None:
        self.write("schemas/security-tool-contract.proto")
        self.write("fixtures/security-tool-contract.json")
        self.write("src/security-tool-contract.py", content="# The policy says do not edit generated files.\n")
        findings = self.findings()
        flagged = {item.path.name for item in findings if item.code == "semantic-token-limit"}
        self.assertEqual(flagged, {"security-tool-contract.proto", "security-tool-contract.py"})
        self.assertNotIn("security-tool-contract.json", flagged)
        self.assertNotIn("exempt-artifact", {
            item.code for item in findings if item.path.name in flagged
        })

    def test_artifact_directory_names_do_not_self_exempt_authored_files(self) -> None:
        for directory in ("generated", "vendor", "snapshots"):
            self.write(f"src/{directory}/security-tool-contract.py")
        findings = self.findings()
        flagged = [item for item in findings if item.code == "semantic-token-limit"]
        self.assertEqual(len(flagged), 3)
        self.assertFalse(any(item.code == "exempt-artifact" for item in findings))

    def test_generated_headers_and_companion_patterns_are_visible_exemptions(self) -> None:
        self.write("src/client.g.dart")
        self.write("src/Widget.Designer.cs")
        self.write("src/bindings.pb.go")
        self.write("src/generated-client.ts", content="// Code generated by protoc. DO NOT EDIT.\n")
        exemptions = {item.path.name for item in self.findings() if item.code == "exempt-artifact"}
        self.assertEqual(exemptions, {"client.g.dart", "Widget.Designer.cs", "bindings.pb.go", "generated-client.ts"})

    def test_supported_language_config_idl_and_doc_extensions_are_audited(self) -> None:
        names = (
            "run-status-codec.ml", "run-status-codec.mli", "security-tool-contract.st",
            "security-tool-runtime.conf", "security-tool-contract.thrift",
            "security-tool-boundary.adoc",
        )
        for name in names:
            self.write(f"src/{name}")
        self.write("NAMESPACE")
        self.write("DESCRIPTION")
        findings = self.findings()
        flagged = {item.path.name for item in findings if item.code == "semantic-token-limit"}
        self.assertEqual(flagged, set(names) - {"security-tool-boundary.adoc"})
        reserved = {item.path.name for item in findings if item.code == "exempt-artifact"}
        self.assertTrue({"NAMESPACE", "DESCRIPTION"} <= reserved)

    def test_extensionless_and_skill_reserved_files_are_visible_exemptions(self) -> None:
        self.write("Makefile")
        self.write("Dockerfile")
        self.write("agents/openai.yaml")
        findings = [item for item in self.findings() if item.code == "exempt-artifact"]
        self.assertEqual({item.path.name for item in findings}, {"Makefile", "Dockerfile", "openai.yaml"})

    def test_extensionless_shebang_scripts_receive_filename_checks(self) -> None:
        self.write("scripts/security-tool-runtime", content="#!/bin/sh\nexit 0\n")
        findings = self.findings()
        self.assertTrue(any(
            item.code == "semantic-token-limit" and item.path.name == "security-tool-runtime"
            for item in findings
        ))

    def test_generic_temporal_category_and_lockfile_checks_remain(self) -> None:
        self.write("src/helpers/utils.py")
        self.write("src/final-parser.rb")
        self.write("src/service-helper.ts")
        self.write("package.json", content="{}\n")
        self.write("package-lock.json")
        self.write("pnpm-lock.yaml")
        self.assertTrue(
            {"generic-directory", "generic-file", "temporal-file", "category-chain", "conflicting-lockfiles"}
            <= self.codes(self.findings())
        )

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

    def test_exact_exception_becomes_visible_notice(self) -> None:
        self.write("src/run-status-codec.py")
        self.write_exceptions([self.exception()])
        findings = self.findings()
        self.assertIn("semantic-token-limit", self.codes(findings))
        self.assertIn("unsupported-naming-exception", self.codes(findings))
        self.assertNotIn("naming-exception", self.codes(findings))

    def test_colony_exception_targets_exact_directory(self) -> None:
        for name in ("catalog-reader.py", "catalog-writer.py", "catalog-index.py"):
            self.write(f"src/{name}")
        self.write_exceptions([self.exception(rule="filename-colony", path="src/catalog")])
        findings = self.findings(flat_limit=99)
        self.assertIn("filename-colony", self.codes(findings))
        self.assertIn("unsupported-naming-exception", self.codes(findings))

    def test_malformed_unknown_overbroad_and_stale_exceptions_are_errors(self) -> None:
        bad_records = [
            self.exception(path="src/*.py"), self.exception(rule="flat-cluster"),
            self.exception(path="../outside.py"), self.exception(path="src/missing-file.py"),
            {"rule": "semantic-token-limit", "path": "src/a.py"},
        ]
        self.write_exceptions(bad_records)
        findings = self.findings()
        invalid = [item for item in findings if item.code == "invalid-naming-exception"]
        self.assertEqual(len(invalid), 4)
        self.assertEqual(len([item for item in findings if item.code == "stale-naming-exception"]), 0)
        self.assertIn("unsupported-naming-exception", self.codes(findings))
        self.assertTrue(audit_architecture.should_fail(findings))

    def test_low_quality_exception_rationale_is_rejected(self) -> None:
        self.write("src/run-status-codec.py")
        self.write_exceptions([self.exception(reason="legacy", owner="x", control="none", review="never")])
        findings = self.findings()
        self.assertIn("invalid-naming-exception", self.codes(findings))
        self.assertIn("semantic-token-limit", self.codes(findings))

    def test_length_padded_low_quality_exception_is_rejected(self) -> None:
        self.write("src/run-status-codec.py")
        self.write_exceptions([self.exception(
            reason="legacy compatibility path retained for convenience",
            control="manual review checklist", review="permanent quarterly review",
        )])
        findings = self.findings()
        self.assertIn("invalid-naming-exception", self.codes(findings))
        self.assertIn("semantic-token-limit", self.codes(findings))

    def test_artifact_exception_contract_rejects_bad_or_stale_records(self) -> None:
        self.write("generated/client.generated.ts", content="// generated output\n")
        records = [
            {
                "class": "generated", "path": "generated/*", "reason": "generator output from public api schema",
                "owner": "api platform", "control": "regeneration diff test", "review": "review on generator upgrade",
            },
            {
                "class": "unknown", "path": "generated", "reason": "generator output from public api schema",
                "owner": "api platform", "control": "regeneration diff test", "review": "review on generator upgrade",
            },
            {
                "class": "generated", "path": "missing", "reason": "generator output from public api schema",
                "owner": "api platform", "control": "regeneration diff test", "review": "review on generator upgrade",
            },
        ]
        self.write_artifact_exceptions(records)
        findings = self.findings()
        self.assertEqual(len([item for item in findings if item.code == "invalid-artifact-exemption"]), 2)
        self.assertEqual(len([item for item in findings if item.code == "stale-artifact-exemption"]), 1)

    def test_colony_exceptions_are_scoped_by_proposed_owner_path(self) -> None:
        for owner in ("catalog", "rollout"):
            for role in ("reader", "writer", "index"):
                self.write(f"src/{owner}-{role}.py")
        self.write_exceptions([self.exception(
            rule="filename-colony", path="src/rollout",
            reason="published rollout plugin paths", owner="release platform",
            control="plugin path contract test", review="remove in plugin v3",
        )])
        findings = self.findings(flat_limit=99)
        colony_paths = {item.path.relative_to(self.root).as_posix() for item in findings if item.code == "filename-colony"}
        self.assertEqual(colony_paths, {"src/catalog", "src/rollout"})
        self.assertNotIn("naming-exception", self.codes(findings))
        self.assertIn("unsupported-naming-exception", self.codes(findings))

    def test_invalid_exception_json_is_an_error(self) -> None:
        self.write(".architecture-enforcement.json", content="{")
        self.assertIn("invalid-exception-file", self.codes(self.findings()))


if __name__ == "__main__":
    unittest.main()
