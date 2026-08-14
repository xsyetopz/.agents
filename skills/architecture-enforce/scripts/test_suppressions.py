"""Regression tests for fail-closed lint/check suppression detection."""

from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from architecture_audit import git_suppression_findings, suppression_findings
from architecture_audit.discovery import GitInventoryError
from test_support import AuditFixture


class SuppressionTests(AuditFixture, unittest.TestCase):
    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )

    def init_git(self) -> None:
        self.git("init", "-q")
        self.git("config", "user.email", "audit@example.invalid")
        self.git("config", "user.name", "Architecture Audit")

    def commit(self, message: str = "baseline") -> None:
        self.git("add", "--all")
        self.git("commit", "-qm", message)

    def test_comment_directives_report_the_exact_source_line(self) -> None:
        cases = {
            "src/app.ts": "const value = 1;\n// eslint-disable-next-line no-console\n",
            "src/view.tsx": "const value = 1;\n/* biome-ignore lint/suspicious/noExplicitAny */\n",
            "src/types.ts": "const value = 1;\n// @ts-ignore\n",
            "src/expected.ts": "const value = 1;\n// @ts-expect-error\n",
            "src/deno.ts": "const value = 1;\n// deno-lint-ignore no-explicit-any\n",
            "src/native.cpp": "int value = 1;\n// NOLINTNEXTLINE(readability-identifier-naming)\n",
            "src/check.py": "value = 1\n# noqa: F401\n",
            "src/typing.py": "value = 1\n# type: ignore[arg-type]\n",
            "src/lint.py": "value = 1\n# pylint: disable=invalid-name\n",
            "src/rules.rb": "value = 1\n# rubocop:disable Style/IfUnlessModifier\n",
            "src/rules.swift": "let value = 1\n// swiftlint:disable identifier_name\n",
            "src/rules.kt": "val value = 1\n// ktlint-disable standard:property-naming\n",
            "src/rules.go": "package rules\n//nolint:errcheck\n",
            "src/check.sh": "#!/bin/sh\n# shellcheck disable=SC2086\n",
            "src/check.dart": "void f() {}\n// ignore_for_file: avoid_print\n",
            "src/check_pyright.py": "value = 1\n# pyright: ignore\n",
            "src/check_lint.go": "package check\n//lint:ignore U1000 generated compatibility\n",
            "src/check.php": "<?php\n/** @phpstan-ignore-next-line */\n$x = 1;\n",
        }
        for relative, content in cases.items():
            with self.subTest(relative=relative):
                path = self.write(relative, content=content)
                findings = suppression_findings(path, self.root)
                self.assertTrue(findings, relative)
                self.assertTrue(all(item.severity == "error" for item in findings))
                self.assertTrue(any("line 2" in item.message for item in findings))
                self.assertTrue(any(item.code == "lint-suppression" for item in findings))

    def test_rust_allow_attributes_are_suppressions(self) -> None:
        path = self.write("src/lib.rs", content="#![allow(dead_code)]\n#[cfg_attr(test, allow(clippy::unwrap_used))]\nfn helper() {}\n")
        findings = suppression_findings(path, self.root)
        self.assertEqual([item.code for item in findings], ["lint-suppression", "lint-suppression"])
        self.assertIn("line 1", findings[0].message)
        self.assertIn("line 2", findings[1].message)

    def test_warning_pragmas_and_suppress_annotations_are_suppressions(self) -> None:
        cases = {
            "src/native.cpp": "#pragma GCC diagnostic ignored \"-Wunused\"\n",
            "src/legacy.cs": "#pragma warning disable CS0618\n",
            "src/Legacy.java": "@SuppressWarnings(\"deprecation\")\nclass Legacy {}\n",
        }
        for relative, content in cases.items():
            with self.subTest(relative=relative):
                findings = suppression_findings(self.write(relative, content=content), self.root)
                self.assertEqual([item.code for item in findings], ["lint-suppression"])

    def test_shell_check_commands_and_ci_failure_tolerance_are_blocked(self) -> None:
        shell = self.write("scripts/check.sh", content="#!/bin/sh\nnpm test || true\n")
        shell_findings = suppression_findings(shell, self.root)
        self.assertEqual([item.code for item in shell_findings], ["check-bypass"])
        self.assertIn("line 2", shell_findings[0].message)

        workflow = self.write(
            ".github/workflows/ci.yml",
            content=(
                "jobs:\n"
                "  unit-tests:\n"
                "    steps:\n"
                "      - run: npm run lint\n"
                "        continue-on-error: true\n"
            ),
        )
        workflow_findings = suppression_findings(workflow, self.root)
        self.assertEqual([item.code for item in workflow_findings], ["check-bypass"])
        self.assertIn("line 5", workflow_findings[0].message)
        run_workflow = self.write(
            ".github/workflows/run.yml",
            content="jobs:\n  check:\n    steps:\n      - run: ./scripts/check.sh || true\n",
        )
        self.assertTrue(any(item.code == "check-bypass" and "line 4" in item.message for item in suppression_findings(run_workflow, self.root)))

    def test_disabled_linter_severity_is_blocked(self) -> None:
        path = self.write(
            ".eslintrc.json",
            content='{"rules": {"no-console": "off", "no-debugger": 0}}\n',
        )
        findings = suppression_findings(path, self.root)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].code, "lint-severity-disabled")
        self.assertIn("line 1", findings[0].message)
        pyproject = self.write("pyproject.toml", content="[tool.ruff]\nseverity = off\n")
        pyproject_findings = suppression_findings(pyproject, self.root)
        self.assertEqual([item.code for item in pyproject_findings], ["lint-severity-disabled"])

    def test_package_and_multiline_linter_suppressions_are_blocked(self) -> None:
        package = self.write("package.json", content='{"scripts":{"test":"npm test || true","lint":"eslint . || :"}}\n')
        package_findings = suppression_findings(package, self.root)
        self.assertEqual([item.code for item in package_findings], ["check-bypass"])
        package.write_text('{"scripts": {\n  "test":\n    "npm test || :"\n}}\n', encoding="utf-8")
        multiline_package_findings = suppression_findings(package, self.root)
        self.assertTrue(any(item.code == "check-bypass" and "line 3" in item.message for item in multiline_package_findings))
        multiline = self.write(
            ".eslintrc.json",
            content='{"rules": {\n  "no-console":\n    "off"\n}}\n',
        )
        multiline_findings = suppression_findings(multiline, self.root)
        self.assertTrue(any(item.code == "lint-severity-disabled" and "line 2" in item.message for item in multiline_findings))

    def test_tool_config_suppressions_are_blocked(self) -> None:
        cases = {
            ".flake8": "[flake8]\nignore = E501\n",
            "mypy.ini": "[mypy]\nignore_errors = True\n",
            "tsconfig.json": '{"compilerOptions":{"skipLibCheck":true}}\n',
            ".golangci.yml": "linters:\n  disable-all: true\n",
            "pyproject.toml": '[tool.ruff.lint]\nignore = ["E501", "F401"]\n',
        }
        for relative, content in cases.items():
            with self.subTest(relative=relative):
                path = self.write(relative, content=content)
                findings = suppression_findings(path, self.root)
                self.assertTrue(findings, relative)
                self.assertTrue(all(item.severity == "error" for item in findings))
                self.assertTrue(all("line " in item.message for item in findings))
        select = self.write("ruff.toml", content='[lint]\nselect = ["E", "F", "I"]\n')
        self.assertEqual(suppression_findings(select, self.root), [])

    def test_false_positive_check_expression_is_not_a_bypass(self) -> None:
        path = self.write("src/feature.ts", content="const enabled = featureCheck || true;\n")
        self.assertEqual(suppression_findings(path, self.root), [])
        description = self.write("package.json", content='{"description":"npm test || true"}\n')
        self.assertEqual(suppression_findings(description, self.root), [])

    def test_strings_docs_and_non_check_ci_steps_do_not_trigger(self) -> None:
        self.assertEqual(
            suppression_findings(
                self.write("src/notes.ts", content='const note = "eslint-disable npm test || true";\n'),
                self.root,
            ),
            [],
        )
        self.assertEqual(
            suppression_findings(
                self.write("src/prose.js", content="// eslint-disable-style waivers are documented here\n"),
                self.root,
            ),
            [],
        )
        self.assertEqual(
            suppression_findings(
                self.write("docs/example.md", content="<!-- eslint-disable -->\n"),
                self.root,
            ),
            [],
        )
        self.assertEqual(
            suppression_findings(
                self.write("scripts/echo.sh", content='#!/bin/sh\necho "npm test || true"\n'),
                self.root,
            ),
            [],
        )
        workflow = self.write(
            ".github/workflows/build.yml",
            content="jobs:\n  build:\n    continue-on-error: true\n    steps:\n      - run: make\n",
        )
        self.assertEqual(suppression_findings(workflow, self.root), [])

    def test_audit_cli_fails_on_suppression_with_line_evidence(self) -> None:
        self.write("src/app.ts", content="const value = 1;\n// eslint-disable-next-line no-console\n")
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = self.json_output(result)
        matches = [item for item in payload["findings"] if item["code"] == "lint-suppression"]
        self.assertTrue(matches)
        self.assertTrue(any(item["path"] == "src/app.ts" and "line 2" in item["message"] for item in matches))

    def test_git_ignore_candidates_stage_unstage_and_untracked_are_blocking(self) -> None:
        self.init_git()
        self.write("README.md", content="baseline\n")
        self.write(".gitignore", content="dist/\n")
        self.write(".eslintignore", content="# baseline\n")
        self.commit()

        self.write(".eslintignore", content="# baseline\nsrc/generated\n")
        self.git("add", ".eslintignore")
        self.write(".stylelintignore", content="src/vendor/**\n")
        self.write(".gitignore", content="dist/\nsrc/**\nignored/.eslintignore\n")
        self.write("ignored/.eslintignore", content="src/vendor/generated/**\n")
        self.write(".ruffignore", content="# comment only\n\n")
        findings = git_suppression_findings(self.root)
        codes = {item.code for item in findings}
        self.assertIn("ignore-pattern-added", codes)
        self.assertIn("gitignore-source-pattern-added", codes)
        lines = {(item.path.name, item.message) for item in findings}
        self.assertTrue(any(name == ".eslintignore" and "line 2" in message for name, message in lines))
        self.assertTrue(any(name == ".stylelintignore" and "line 1" in message for name, message in lines))
        self.assertTrue(any(name == ".gitignore" and "line 2" in message for name, message in lines))
        self.assertFalse(any(name == ".eslintignore" and "line 1" in message for name, message in lines))
        self.assertFalse(any(name == ".ruffignore" for name, _ in lines))

    def test_git_destructive_deletions_and_removed_provider_lines_are_blocking(self) -> None:
        self.init_git()
        self.write("tests/test_runner.py", content="def test_runner():\n    pass\n")
        self.write("scripts/check.sh", content="#!/bin/sh\nnpm test\n")
        self.write(".github/workflows/test.yml", content="jobs:\n  test:\n    steps: []\n")
        self.commit()
        self.git("rm", "-q", "tests/test_runner.py")
        self.write("scripts/check.sh", content="#!/bin/sh\necho no-op\n")
        (self.root / ".github/workflows/test.yml").unlink()
        findings = git_suppression_findings(self.root)
        codes = {item.code for item in findings}
        self.assertIn("check-file-deleted", codes)
        self.assertIn("check-provider-removed", codes)
        self.assertTrue(any(item.path.name == "test_runner.py" for item in findings if item.code == "check-file-deleted"))
        self.assertTrue(any(item.path.name == "check.sh" and "line 2" in item.message for item in findings if item.code == "check-provider-removed"))
        self.assertTrue(any(item.path.name == "test.yml" for item in findings if item.code == "check-file-deleted"))

    def test_git_initial_state_and_nonrelevant_changes_are_not_false_positives(self) -> None:
        self.init_git()
        self.write(".eslintignore", content="src/generated\n")
        self.write(".gitignore", content="dist/\n")
        self.write("src/app.py", content="value = 1\n")
        self.write("scripts/check.sh", content="#!/bin/sh\necho ok\n")
        self.commit()
        self.assertEqual(git_suppression_findings(self.root), [])
        self.write(".eslintignore", content="src/generated\n# rationale\n")
        self.write(".gitignore", content="dist/\ndocs/**\n")
        self.write("scripts/check.sh", content="#!/bin/sh\necho still-ok\n")
        self.assertEqual(git_suppression_findings(self.root), [])

    def test_git_suppression_scan_failure_is_blocking(self) -> None:
        self.init_git()
        self.write("README.md", content="baseline\n")
        self.commit()
        with patch("architecture_audit.git_suppressions._run_git_diff", side_effect=GitInventoryError("test failure")):
            findings = git_suppression_findings(self.root)
        self.assertEqual([item.code for item in findings], ["git-suppression-scan-failed"])

    def test_git_unrelated_same_parent_replacement_does_not_waive_test_deletion(self) -> None:
        self.init_git()
        self.write("tests/test_security.py", content="def test_security():\n    assert 1 == 1\n")
        self.commit()
        self.git("rm", "-q", "tests/test_security.py")
        self.write("tests/test_unrelated.py", content="def test_unrelated():\n    assert 2 == 2\n")
        findings = git_suppression_findings(self.root)
        self.assertTrue(any(item.code == "check-file-deleted" and item.path.name == "test_security.py" for item in findings))

    def test_git_cross_directory_r100_rename_does_not_report_old_test_deletion(self) -> None:
        self.init_git()
        self.write("tests/legacy/test_runner.py", content="def test_runner():\n    assert 1 == 1\n")
        self.commit()
        (self.root / "tests/current").mkdir(parents=True)
        self.git("mv", "tests/legacy/test_runner.py", "tests/current/test_runner.py")
        findings = git_suppression_findings(self.root)
        self.assertFalse(any(item.code == "check-file-deleted" for item in findings))

    def test_git_renamed_test_provider_line_does_not_report_removed_provider(self) -> None:
        self.init_git()
        self.write(
            "tests/legacy/test_runner.ts",
            content='import { describe, it } from "vitest";\n\ndescribe("runner", () => it("works", () => undefined));\n',
        )
        self.commit()
        (self.root / "tests/current").mkdir(parents=True)
        self.git("mv", "tests/legacy/test_runner.ts", "tests/current/test_runner.ts")
        findings = git_suppression_findings(self.root)
        self.assertFalse(any(item.code == "check-provider-removed" for item in findings))

    def test_git_renamed_provider_removal_is_not_hidden_by_r99_move(self) -> None:
        self.init_git()
        self.write(
            "tests/legacy/check.ts",
            content=(
                "#!/usr/bin/env bun\nbun test\n"
                + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 99))
            ),
        )
        self.commit()
        (self.root / "tests/current").mkdir(parents=True)
        (self.root / "tests/current/check.ts").write_text(
            "#!/usr/bin/env bun\necho provider removed\n"
            + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 99)),
            encoding="utf-8",
        )
        (self.root / "tests/legacy/check.ts").unlink()
        self.git("add", "--all")
        rename_status = self.git("diff", "--cached", "--find-renames=90", "--name-status").stdout
        self.assertIn("R099", rename_status)
        findings = git_suppression_findings(self.root)
        provider_findings = [item for item in findings if item.code == "check-provider-removed"]
        self.assertEqual(len(provider_findings), 1)
        self.assertIn("bun test", provider_findings[0].message)

    def test_git_low_score_same_basename_import_relocation_keeps_r90_boundary(self) -> None:
        self.init_git()
        self.write(
            "tests/legacy/check.ts",
            content=(
                "".join(f'import dep{i} from "../../src/dep{i}";\n' for i in range(1, 6))
                + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 21))
            ),
        )
        self.commit()
        (self.root / "tests/current/nested").mkdir(parents=True)
        (self.root / "tests/current/nested/check.ts").write_text(
            (self.root / "tests/legacy/check.ts").read_text(encoding="utf-8").replace(
                "../../src/", "../../../src/"
            ),
            encoding="utf-8",
        )
        (self.root / "tests/legacy/check.ts").unlink()
        self.git("add", "--all")
        raw = self.git("diff", "--cached", "--find-renames=1", "--name-status").stdout
        self.assertIn("R076", raw)
        self.assertNotIn("R090", self.git("diff", "--cached", "--find-renames=90", "--name-status").stdout)
        findings = git_suppression_findings(self.root)
        self.assertFalse(any(item.code == "check-file-deleted" for item in findings))

    def test_git_low_score_same_basename_replacement_stays_blocking(self) -> None:
        self.init_git()
        self.write(
            "tests/legacy/check.ts",
            content=(
                "#!/usr/bin/env bun\nbun test\n"
                + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 99))
            ),
        )
        self.commit()
        (self.root / "tests/current").mkdir(parents=True)
        (self.root / "tests/current/check.ts").write_text(
            "#!/usr/bin/env bun\necho provider removed\n"
            + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 85))
            + "".join(f"export const replacement{i} = {i * 10};\n" for i in range(85, 101)),
            encoding="utf-8",
        )
        (self.root / "tests/legacy/check.ts").unlink()
        self.git("add", "--all")
        rename_status = self.git("diff", "--cached", "--find-renames=80", "--name-status").stdout
        self.assertIn("R082", rename_status)
        self.assertNotIn("R090", self.git("diff", "--cached", "--find-renames=90", "--name-status").stdout)
        findings = git_suppression_findings(self.root)
        self.assertTrue(any(item.code == "check-file-deleted" for item in findings))

    def test_git_non_script_rename_provider_text_is_not_a_provider_removal(self) -> None:
        self.init_git()
        self.write(
            "docs/old/guide.md",
            content="vitest is used for examples\n" + "".join(f"example {i}\n" for i in range(1, 100)),
        )
        self.commit()
        (self.root / "docs/new").mkdir(parents=True)
        (self.root / "docs/new/guide.md").write_text(
            "examples use another runner\n" + "".join(f"example {i}\n" for i in range(1, 100)),
            encoding="utf-8",
        )
        (self.root / "docs/old/guide.md").unlink()
        self.git("add", "--all")
        rename_status = self.git("diff", "--cached", "--find-renames=90", "--name-status").stdout
        self.assertIn("R", rename_status)
        findings = git_suppression_findings(self.root)
        self.assertFalse(any(item.code == "check-provider-removed" for item in findings))

    def test_git_r100_test_move_out_of_check_path_stays_blocking(self) -> None:
        self.init_git()
        self.write(
            "tests/legacy/runner.ts",
            content=(
                'import { describe, it } from "vitest";\n'
                + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 99))
            ),
        )
        self.commit()
        (self.root / "src").mkdir(parents=True)
        (self.root / "src/runner.ts").write_text(
            'import { describe, it } from "vitest";\n'
            + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 99)),
            encoding="utf-8",
        )
        (self.root / "tests/legacy/runner.ts").unlink()
        self.git("add", "--all")
        rename_status = self.git("diff", "--cached", "--find-renames=90", "--name-status").stdout
        self.assertIn("R100", rename_status)
        findings = git_suppression_findings(self.root)
        self.assertTrue(any(item.code == "check-file-deleted" for item in findings))

    def test_git_real_test_deletion_still_blocks_with_rename_inventory(self) -> None:
        self.init_git()
        self.write("tests/test_runner.py", content="def test_runner():\n    assert 1 == 1\n")
        self.commit()
        self.git("rm", "-q", "tests/test_runner.py")
        findings = git_suppression_findings(self.root)
        self.assertTrue(any(item.code == "check-file-deleted" and item.path.name == "test_runner.py" for item in findings))

    def test_git_weak_rename_evidence_does_not_waive_test_deletion(self) -> None:
        self.init_git()
        self.write("tests/test_security.py", content="def test_security():\n    assert 1 == 1\n")
        self.commit()
        self.git("rm", "-q", "tests/test_security.py")
        weak_inventory = b"R89\0tests/test_security.py\0tests/test_unrelated.py\0"
        with patch("architecture_audit.git_suppressions._run_git_rename_inventory", return_value=weak_inventory):
            findings = git_suppression_findings(self.root)
        self.assertTrue(any(item.code == "check-file-deleted" and item.path.name == "test_security.py" for item in findings))

    def test_git_malformed_rename_evidence_does_not_waive_test_deletion(self) -> None:
        self.init_git()
        self.write("tests/test_security.py", content="def test_security():\n    assert 1 == 1\n")
        self.commit()
        self.git("rm", "-q", "tests/test_security.py")
        malformed_inventory = b"R100\0tests/test_security.py\0tests/test_security.py\0"
        with patch("architecture_audit.git_suppressions._run_git_rename_inventory", return_value=malformed_inventory):
            findings = git_suppression_findings(self.root)
        self.assertTrue(any(item.code == "check-file-deleted" and item.path.name == "test_security.py" for item in findings))

    def test_git_placeholder_replacement_does_not_waive_test_deletion(self) -> None:
        self.init_git()
        self.write("tests/test_security.py", content="def test_security():\n    pass\n")
        self.commit()
        self.git("rm", "-q", "tests/test_security.py")
        self.write("tests/test_placeholder.py", content="value = 1\n")
        self.assertTrue(any(item.code == "check-file-deleted" for item in git_suppression_findings(self.root)))

    def test_gitignored_replacement_does_not_waive_test_deletion(self) -> None:
        self.init_git()
        self.write("tests/test_legacy.py", content="def test_old():\n    pass\n")
        self.write(".gitignore", content="tests/test_new.py\n")
        self.commit()
        self.git("rm", "-q", "tests/test_legacy.py")
        self.write("tests/test_new.py", content="def test_new():\n    assert 1 == 1\n")
        self.assertTrue(any(item.code == "check-file-deleted" for item in git_suppression_findings(self.root)))


if __name__ == "__main__":
    unittest.main()
