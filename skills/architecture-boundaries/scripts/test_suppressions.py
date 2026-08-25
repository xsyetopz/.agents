#!/usr/bin/env python3
"""Regression tests for file-level lint/check suppression detection."""

from __future__ import annotations

import unittest

from architecture_audit import suppression_findings
from test_support import AuditFixture


class SuppressionTests(AuditFixture, unittest.TestCase):
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
                self.assertTrue(
                    any(item.code == "lint-suppression" for item in findings)
                )

    def test_rust_allow_attributes_are_suppressions(self) -> None:
        path = self.write(
            "src/lib.rs",
            content="#![allow(dead_code)]\n#[cfg_attr(test, allow(clippy::unwrap_used))]\nfn helper() {}\n",
        )
        findings = suppression_findings(path, self.root)
        self.assertEqual(
            [item.code for item in findings], ["lint-suppression", "lint-suppression"]
        )
        self.assertIn("line 1", findings[0].message)
        self.assertIn("line 2", findings[1].message)

    def test_warning_pragmas_and_suppress_annotations_are_suppressions(self) -> None:
        cases = {
            "src/native.cpp": '#pragma GCC diagnostic ignored "-Wunused"\n',
            "src/legacy.cs": "#pragma warning disable CS0618\n",
            "src/Legacy.java": '@SuppressWarnings("deprecation")\nclass Legacy {}\n',
        }
        for relative, content in cases.items():
            with self.subTest(relative=relative):
                findings = suppression_findings(
                    self.write(relative, content=content), self.root
                )
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
        self.assertTrue(
            any(
                item.code == "check-bypass" and "line 4" in item.message
                for item in suppression_findings(run_workflow, self.root)
            )
        )

    def test_disabled_linter_severity_is_blocked(self) -> None:
        path = self.write(
            ".eslintrc.json",
            content='{"rules": {"no-console": "off", "no-debugger": 0}}\n',
        )
        findings = suppression_findings(path, self.root)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].code, "lint-severity-disabled")
        self.assertIn("line 1", findings[0].message)
        pyproject = self.write(
            "pyproject.toml", content="[tool.ruff]\nseverity = off\n"
        )
        pyproject_findings = suppression_findings(pyproject, self.root)
        self.assertEqual(
            [item.code for item in pyproject_findings], ["lint-severity-disabled"]
        )

    def test_package_and_multiline_linter_suppressions_are_blocked(self) -> None:
        package = self.write(
            "package.json",
            content='{"scripts":{"test":"npm test || true","lint":"eslint . || :"}}\n',
        )
        package_findings = suppression_findings(package, self.root)
        self.assertEqual([item.code for item in package_findings], ["check-bypass"])
        package.write_text(
            '{"scripts": {\n  "test":\n    "npm test || :"\n}}\n', encoding="utf-8"
        )
        multiline_package_findings = suppression_findings(package, self.root)
        self.assertTrue(
            any(
                item.code == "check-bypass" and "line 3" in item.message
                for item in multiline_package_findings
            )
        )
        multiline = self.write(
            ".eslintrc.json",
            content='{"rules": {\n  "no-console":\n    "off"\n}}\n',
        )
        multiline_findings = suppression_findings(multiline, self.root)
        self.assertTrue(
            any(
                item.code == "lint-severity-disabled" and "line 2" in item.message
                for item in multiline_findings
            )
        )

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
        path = self.write(
            "src/feature.ts", content="const enabled = featureCheck || true;\n"
        )
        self.assertEqual(suppression_findings(path, self.root), [])
        description = self.write(
            "package.json", content='{"description":"npm test || true"}\n'
        )
        self.assertEqual(suppression_findings(description, self.root), [])

    def test_strings_docs_and_non_check_ci_steps_do_not_trigger(self) -> None:
        self.assertEqual(
            suppression_findings(
                self.write(
                    "src/notes.ts",
                    content='const note = "eslint-disable npm test || true";\n',
                ),
                self.root,
            ),
            [],
        )
        self.assertEqual(
            suppression_findings(
                self.write(
                    "src/prose.js",
                    content="// eslint-disable-style waivers are documented here\n",
                ),
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
                self.write(
                    "scripts/echo.sh", content='#!/bin/sh\necho "npm test || true"\n'
                ),
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
        self.write(
            "src/app.ts",
            content="const value = 1;\n// eslint-disable-next-line no-console\n",
        )
        result = self.run_cli("--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = self.json_output(result)
        matches = [
            item for item in payload["findings"] if item["code"] == "lint-suppression"
        ]
        self.assertTrue(matches)
        self.assertTrue(
            any(
                item["path"] == "src/app.ts" and "line 2" in item["message"]
                for item in matches
            )
        )


if __name__ == "__main__":
    unittest.main()
