#!/usr/bin/env python3
"""CLI contract and fail-closed gate regression tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from architecture_audit.cli import parse_args, should_fail
from architecture_audit.records import Finding
from test_support import AuditFixture


class AuditCliTests(AuditFixture, unittest.TestCase):
    def test_inline_test_cli_fails_default_acceptance_gate(self) -> None:
        self.write("src/codec.rs", content="#[test]\nfn round_trip() {}\n")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = self.json_output(result)
        finding = next(
            item for item in payload["findings"] if item["code"] == "inline-test"
        )
        self.assertEqual(finding["evidence"], "syntax")

    def test_structural_inventory_findings_are_blocking_cli_regressions(self) -> None:
        cases: tuple[tuple[str, tuple[str, ...], str], ...] = (
            (
                "flat-cluster",
                tuple(f"src/{letter}.py" for letter in "abcdefghijklmnop"),
                "flat-cluster",
            ),
            (
                "filename-colony",
                (
                    "src/catalog-reader.py",
                    "src/catalog-writer.py",
                    "src/catalog-index.py",
                ),
                "filename-colony",
            ),
            (
                "procedural-suffix",
                (
                    "src/sessionActorHelpers.ts",
                    "src/journalValidation.ts",
                    "src/sessionActorOpen.ts",
                    "src/sessionActorReduce.ts",
                    "src/sessionActorCommit.ts",
                ),
                "procedural-suffix",
            ),
            (
                "microfile-fragmentation",
                tuple(f"src/unit-{index}/unit-{index}.py" for index in range(4)),
                "microfile-fragmentation",
            ),
        )
        for _label, paths, expected_code in cases:
            with (
                self.subTest(expected_code=expected_code),
                tempfile.TemporaryDirectory() as case_dir,
            ):
                case_root = Path(case_dir)
                for path in paths:
                    target = case_root / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("x\n", encoding="utf-8")
                result = self.run_cli("--format", "json", root=case_root)
                self.assertEqual(result.returncode, 1)
                payload = self.json_output(result)
                self.assertTrue(
                    any(item["code"] == expected_code for item in payload["findings"])
                )

    def test_metadata_candidates_are_inventoried_without_source_structural_findings(
        self,
    ) -> None:
        self.write("package.json", content="{}\n")
        self.write("docs/security-tool-contract.md")
        self.write(".github/workflows/security-tool-contract.yml")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 0)
        payload = self.json_output(result)
        self.assertGreaterEqual(payload["audited_files"], 3)
        self.assertFalse(
            any(
                item["code"]
                in {
                    "semantic-token-limit",
                    "flat-cluster",
                    "filename-colony",
                    "procedural-suffix",
                }
                for item in payload["findings"]
            )
        )

    def test_cli_rejects_scope_gate_threshold_and_policy_downgrades(self) -> None:
        self.write("src/codec.py")
        options = (
            ("--exclude", "src/**"),
            ("--allow-scoped-audit", "1"),
            ("--fail-on", "never"),
            ("--allow-partial-audit", "1"),
            ("--soft", "1"),
            ("--strong", "1"),
            ("--hard", "1"),
            ("--flat-limit", "1"),
            ("--policy-file", "policy.json"),
            ("--include-generated", "1"),
        )
        for option, value in options:
            rejected = self.run_cli(option, value, "--format", "json")
            self.assertEqual(rejected.returncode, 2, option)
            self.assertIn("unrecognized arguments", rejected.stderr, option)

        result = self.run_cli("--format", "json")
        payload = self.json_output(result)
        self.assertEqual(payload["scope"], "full")
        self.assertEqual(payload["gate"], "fail-on warning")
        self.assertNotIn("excludes", payload)

    def test_builtin_generated_and_framework_classifications_remain_visible(
        self,
    ) -> None:
        self.write("src/client.g.dart")
        self.write("package.json", content="{}\n")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 0)
        payload = self.json_output(result)
        exemptions = [
            item for item in payload["findings"] if item["code"] == "exempt-artifact"
        ]
        self.assertEqual(
            {item["path"] for item in exemptions}, {"src/client.g.dart", "package.json"}
        )

    def test_generated_and_artifact_paths_still_scan_suppressions_and_structure(
        self,
    ) -> None:
        self.write(
            "src/client.generated.ts",
            content="// eslint-disable-next-line no-console\nconsole.log(1);\n",
        )
        self.write("artifacts/src/Open.ts")
        self.write("artifacts/src/Reduce.ts")
        self.write("artifacts/src/Commit.ts")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = self.json_output(result)
        codes = {item["code"] for item in payload["findings"]}
        self.assertIn("lint-suppression", codes)
        self.assertIn("procedural-suffix", codes)

    def test_three_procedural_phase_files_and_directories_block(self) -> None:
        for phase in ("Open", "Reduce", "Commit"):
            self.write(f"src/{phase}.ts")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "procedural-suffix",
            {item["code"] for item in self.json_output(result)["findings"]},
        )

        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            for phase in ("Open", "Reduce", "Commit"):
                target = case_root / "src" / phase / "actor.ts"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("x\n", encoding="utf-8")
            nested = self.run_cli("--format", "json", root=case_root)
            self.assertEqual(nested.returncode, 1)
            self.assertIn(
                "procedural-directory",
                {item["code"] for item in self.json_output(nested)["findings"]},
            )

    def test_warnings_and_errors_always_fail_the_mandatory_gate(self) -> None:
        error = Finding("error", "x", self.root, "x")
        warning = Finding("warning", "x", self.root, "x")
        notice = Finding("notice", "x", self.root, "x")
        self.assertTrue(should_fail([error]))
        self.assertTrue(should_fail([warning]))
        self.assertFalse(should_fail([notice]))
        self.assertFalse(hasattr(parse_args([]), "fail_on"))

    def test_inventory_and_syntax_findings_gate(self) -> None:
        inventory = Finding("error", "inventory", self.root, "inventory", "inventory")
        syntax = Finding("error", "inline-test", self.root, "inline test", "syntax")
        inventory_warning = Finding(
            "warning", "inventory", self.root, "inventory", "inventory"
        )
        syntax_warning = Finding(
            "warning", "inline-test", self.root, "inline test", "syntax"
        )
        self.assertTrue(should_fail([inventory, syntax]))
        self.assertTrue(should_fail([inventory_warning, syntax_warning]))

    def test_json_cli_is_machine_readable_and_error_exit_is_nonzero(self) -> None:
        self.write("src/run-status-codec.py")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = self.json_output(result)
        self.assertEqual(payload["audited_files"], 1)
        self.assertEqual(payload["audited_paths"], ["src/run-status-codec.py"])
        self.assertIn("findings", payload)


if __name__ == "__main__":
    unittest.main()
