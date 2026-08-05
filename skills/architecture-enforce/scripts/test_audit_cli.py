#!/usr/bin/env python3
"""CLI and fail-closed gate regression tests."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import audit_architecture
from test_support import AuditFixture


class AuditCliTests(AuditFixture, unittest.TestCase):
    def test_inline_test_cli_fails_default_acceptance_gate(self) -> None:
        self.write("src/codec.rs", content="#[test]\nfn round_trip() {}\n")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = self.json_output(result)
        finding = next(item for item in payload["findings"] if item["code"] == "inline-test")
        self.assertEqual(finding["evidence"], "syntax")

    def test_structural_inventory_findings_are_blocking_cli_regressions(self) -> None:
        cases: tuple[str, tuple[str, ...], str] = (
            (
                "flat-cluster",
                tuple(f"src/{letter}.py" for letter in "abcdefghijklmnop"),
                "flat-cluster",
            ),
            (
                "filename-colony",
                ("src/catalog-reader.py", "src/catalog-writer.py", "src/catalog-index.py"),
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
            with self.subTest(expected_code=expected_code), tempfile.TemporaryDirectory() as case_dir:
                case_root = Path(case_dir)
                for path in paths:
                    target = case_root / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("x\n", encoding="utf-8")
                result = self.run_cli("--format", "json", root=case_root)
                self.assertEqual(result.returncode, 1)
                payload = self.json_output(result)
                self.assertTrue(any(item["code"] == expected_code for item in payload["findings"]))

    def test_metadata_candidates_are_inventoried_without_source_structural_findings(self) -> None:
        self.write("package.json", content="{}\n")
        self.write("docs/security-tool-contract.md")
        self.write(".github/workflows/security-tool-contract.yml")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 0)
        payload = self.json_output(result)
        self.assertGreaterEqual(payload["audited_files"], 3)
        self.assertFalse(any(item["code"] in {"semantic-token-limit", "flat-cluster", "filename-colony", "procedural-suffix"} for item in payload["findings"]))

    def test_cli_rejects_scope_gate_threshold_and_policy_downgrades(self) -> None:
        self.write("src/codec.py")
        options = (
            ("--exclude", "src/**"),
            ("--allow-scoped-audit", "1"),
            ("--fail-on", "never"),
            ("--allow-advisory-audit", "1"),
            ("--soft", "1"),
            ("--strong", "1"),
            ("--hard", "1"),
            ("--flat-limit", "1"),
            ("--exceptions", "exceptions.json"),
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

    def test_builtin_generated_and_framework_classifications_remain_visible(self) -> None:
        self.write("src/client.g.dart")
        self.write("package.json", content="{}\n")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 0)
        payload = self.json_output(result)
        exemptions = [item for item in payload["findings"] if item["code"] == "exempt-artifact"]
        self.assertEqual({item["path"] for item in exemptions}, {"src/client.g.dart", "package.json"})

    def test_generated_and_artifact_paths_still_scan_suppressions_and_structure(self) -> None:
        self.write("src/client.generated.ts", content="// eslint-disable-next-line no-console\nconsole.log(1);\n")
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
        self.assertIn("procedural-suffix", {item["code"] for item in self.json_output(result)["findings"]})

        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            for phase in ("Open", "Reduce", "Commit"):
                target = case_root / "src" / phase / "actor.ts"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("x\n", encoding="utf-8")
            nested = self.run_cli("--format", "json", root=case_root)
            self.assertEqual(nested.returncode, 1)
            self.assertIn("procedural-directory", {item["code"] for item in self.json_output(nested)["findings"]})

    def test_configured_artifact_and_test_root_waivers_block_and_do_not_suppress(self) -> None:
        self.write("src/client.ts", content="export const value = 1;\n")
        self.write("qa/Codec.java", content="import org.junit.Test;\n@Test\nvoid roundTrip() {}\n")
        self.write(
            ".architecture-enforcement.json",
            content=json.dumps(
                {
                    "artifact_exemptions": [{
                        "class": "generated",
                        "path": "src/client.ts",
                        "reason": "generator output from public api schema",
                        "owner": "api platform",
                        "control": "regeneration diff test",
                        "review": "review on generator upgrade",
                    }],
                    "test_source_roots": [{
                        "path": "qa",
                        "reason": "JUnit source set declared by the build runner",
                        "owner": "quality platform",
                        "control": "JUnit source-set discovery check",
                        "review": "remove on build runner upgrade",
                    }],
                }
            ),
        )
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = self.json_output(result)
        codes = {item["code"] for item in payload["findings"]}
        self.assertIn("unsupported-artifact-exemption", codes)
        self.assertIn("unsupported-test-source-root", codes)
        self.assertIn("inline-test", codes)
        self.assertFalse(any(item["path"] == "src/client.ts" and item["code"] == "exempt-artifact" for item in payload["findings"]))

    def test_warnings_and_errors_always_fail_the_mandatory_gate(self) -> None:
        error = audit_architecture.Finding("error", "x", self.root, "x")
        warning = audit_architecture.Finding("warning", "x", self.root, "x")
        notice = audit_architecture.Finding("notice", "x", self.root, "x")
        self.assertTrue(audit_architecture.should_fail([error]))
        self.assertTrue(audit_architecture.should_fail([warning]))
        self.assertFalse(audit_architecture.should_fail([notice]))
        self.assertFalse(hasattr(audit_architecture.parse_args([]), "fail_on"))

    def test_inventory_and_advisory_tool_findings_gate(self) -> None:
        inventory = audit_architecture.Finding("error", "inventory", self.root, "inventory", "inventory")
        advisory = audit_architecture.Finding("error", "advisory", self.root, "advisory", "syntax-advisory")
        inventory_warning = audit_architecture.Finding("warning", "inventory", self.root, "inventory", "inventory")
        advisory_warning = audit_architecture.Finding("warning", "advisory", self.root, "advisory", "syntax-advisory")
        self.assertTrue(audit_architecture.should_fail([inventory, advisory]))
        self.assertTrue(audit_architecture.should_fail([inventory_warning, advisory_warning]))

    def test_advisory_or_notice_syntax_contracts_are_invalid(self) -> None:
        self.write(
            ".architecture-enforcement.json",
            content=json.dumps(
                {
                    "syntax_rules": [{
                        "id": "no-console",
                        "tool": "ast-grep",
                        "language": "typescript",
                        "pattern": "console.log($$$ARGS)",
                        "severity": "notice",
                        "message": "console use",
                        "mode": "advisory",
                    }],
                }
            ),
        )
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid-syntax-rule", {item["code"] for item in self.json_output(result)["findings"]})

    def test_json_cli_is_machine_readable_and_error_exit_is_nonzero(self) -> None:
        self.write("src/run-status-codec.py")
        self.write(".architecture-enforcement.json", content="{")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = self.json_output(result)
        self.assertEqual(payload["audited_files"], 2)
        self.assertEqual(set(payload["audited_paths"]), {"src/run-status-codec.py", ".architecture-enforcement.json"})
        self.assertIn("findings", payload)

    def test_ignored_untracked_source_remains_in_path_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(["git", "-C", str(case_root), *args], check=True, capture_output=True, text=True)
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / ".gitignore").write_text("src/**\n", encoding="utf-8")
            run("add", ".gitignore")
            run("commit", "-qm", "baseline")
            (case_root / "src").mkdir()
            (case_root / "src/app.ts").write_text("export const value = 1;\n", encoding="utf-8")
            result = self.run_cli("--format", "json", root=case_root)
            self.assertEqual(result.returncode, 1)
            payload = self.json_output(result)
            self.assertIn("src/app.ts", payload["audited_paths"])
            self.assertIn("gitignore-source-pattern-added", {item["code"] for item in payload["findings"]})

    def test_git_output_dirs_reconcile_candidates_without_walking_bulk_or_nested_repos(self) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(["git", "-C", str(case_root), *args], check=True, capture_output=True, text=True)
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / ".gitignore").write_text("dist/ignored/**\n", encoding="utf-8")
            for relative, content in {
                "dist/Open.ts": "export const open = 1;\n",
                "dist/Commit.ts": "export const commit = 1;\n",
            }.items():
                target = case_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            run("add", ".gitignore", "dist/Open.ts", "dist/Commit.ts")
            run("commit", "-qm", "baseline")
            (case_root / "dist/Reduce.ts").write_text("export const reduce = 1;\n", encoding="utf-8")
            (case_root / "dist/.eslintignore").write_text("dist/generated/**\n", encoding="utf-8")
            ignored = case_root / "dist/ignored"
            ignored.mkdir(parents=True)
            for index in range(400):
                (ignored / f"bulk-{index}.bin").write_bytes(b"generated output\n")
            nested = case_root / "nested"
            nested.mkdir()
            subprocess.run(["git", "-C", str(nested), "init", "-q"], check=True, capture_output=True, text=True)
            (nested / "src").mkdir()
            (nested / "src/hidden.ts").write_text("export const hidden = 1;\n", encoding="utf-8")
            # Discovery preserves the caller's lexical root spelling so
            # findings remain stable on macOS /var <-> /private/var aliases.
            resolved_root = case_root.absolute()
            paths = {path.relative_to(resolved_root).as_posix() for path in audit_architecture.iter_audited_files(case_root)}
            self.assertTrue({"dist/Open.ts", "dist/Commit.ts", "dist/Reduce.ts", "dist/.eslintignore"} <= paths)
            self.assertFalse(any(path.startswith("dist/ignored/") for path in paths))
            self.assertNotIn("nested/src/hidden.ts", paths)

    def test_ignored_untracked_output_phases_remain_audited(self) -> None:
        """Pruned output trees still expose ignored authored architecture files."""

        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args], check=True, capture_output=True, text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / ".gitignore").write_text("dist/**\n", encoding="utf-8")
            run("add", ".gitignore")
            run("commit", "-qm", "baseline")
            output = case_root / "dist"
            output.mkdir()
            for phase in ("Open", "Reduce", "Commit"):
                (output / f"{phase}.ts").write_text(f"export const {phase.lower()} = 1;\n", encoding="utf-8")
            result = self.run_cli("--format", "json", root=case_root)
            self.assertEqual(result.returncode, 1)
            payload = self.json_output(result)
            self.assertTrue({f"dist/{phase}.ts" for phase in ("Open", "Reduce", "Commit")} <= set(payload["audited_paths"]))
            codes = {item["code"] for item in payload["findings"]}
            self.assertIn("procedural-suffix", codes)
            self.assertIn("output-directory-source", codes)


if __name__ == "__main__":
    unittest.main()
