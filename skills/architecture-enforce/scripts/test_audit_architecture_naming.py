"""Naming and artifact architecture regression tests."""

from __future__ import annotations

import json
import unittest

import audit_architecture
from test_support import AuditFixture


class AuditArchitectureNamingTests(AuditFixture, unittest.TestCase):

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
