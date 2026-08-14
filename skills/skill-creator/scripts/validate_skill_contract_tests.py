from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from test_support import (
    check_duplicate_entrypoints,
    check_global_path_references,
    check_required_files,
    check_required_headings,
    validate,
)


class PackageContractTests(unittest.TestCase):
    """The package contract is opt-in; the open format remains minimal."""

    @staticmethod
    def _skill(root: Path, *, body: str = "# Example\n") -> Path:
        root.mkdir(parents=True, exist_ok=True)
        (root / "SKILL.md").write_text(
            "---\n"
            "name: example\n"
            "description: Use this skill for the example task.\n"
            "---\n" + body,
            encoding="utf-8",
        )
        return root

    def test_required_headings_and_files_are_enforced_from_local_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            (root / ".skill-validator.json").write_text(
                json.dumps(
                    {
                        "required_headings": ["# Example", "## Required"],
                        "required_files": ["references/guide.md", "scripts/check.py"],
                    }
                ),
                encoding="utf-8",
            )
            errors, _ = validate(root)

        self.assertIn("Missing required heading: ## Required", errors)
        self.assertIn("Missing required file: references/guide.md", errors)
        self.assertIn("Missing required file: scripts/check.py", errors)

    def test_required_heading_match_is_exact_and_ignores_fenced_examples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(
                Path(directory) / "example",
                body=("## Required but different\n```md\n## Required\n```\n"),
            )
            errors: list[str] = []
            check_required_headings(
                (root / "SKILL.md").read_text(encoding="utf-8"),
                {"required_headings": ["## Required"]},
                errors,
            )

        self.assertEqual(errors, ["Missing required heading: ## Required"])

    def test_common_heading_contract_rejects_aliases_and_reordering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(
                Path(directory) / "example",
                body=(
                    "# Example\n## Use this skill\n## Rules\n## Verify\n"
                    "## Steps\n## Resources\n## Workflow\n"
                ),
            )
            errors: list[str] = []
            check_required_headings(
                (root / "SKILL.md").read_text(encoding="utf-8"),
                {
                    "required_headings": [
                        "# Example",
                        "## Use this skill",
                        "## Rules",
                        "## Steps",
                        "## Resources",
                        "## Verify",
                    ]
                },
                errors,
            )

        self.assertEqual(
            errors,
            [
                (
                    "SKILL.md H2 headings must use the exact common order: "
                    "Use this skill, Rules, Steps, Resources, Verify"
                )
            ],
        )

    def test_required_file_cannot_escape_skill_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            errors: list[str] = []
            check_required_files(
                root,
                {"required_files": ["../outside.txt", str(Path(directory) / "x")]},
                errors,
            )

        self.assertEqual(len(errors), 2)
        self.assertTrue(all("leaves skill root" in error for error in errors))

    def test_assets_contract_accepts_common_schema_and_routed_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(
                Path(directory) / "example",
                body="[Guide](references/guide.md)\n",
            )
            (root / "references").mkdir()
            (root / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (root / ".skill-validator.json").write_text(
                json.dumps({"required_files": ["assets/contract.json"]}),
                encoding="utf-8",
            )
            (root / "assets").mkdir()
            (root / "assets" / "contract.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "skill_name": "example",
                        "required_headings": [
                            "Use this skill",
                            "Rules",
                            "Steps",
                            "Resources",
                            "Verify",
                        ],
                        "required_files": [
                            "SKILL.md",
                            "LICENSE",
                            ".skill-validator.json",
                            "agents/openai.yaml",
                            "references",
                            "assets/contract.json",
                            "evals/evals.json",
                            "scripts/check.py",
                        ],
                        "reference_paths": ["references/guide.md"],
                        "eval_case_ids": [
                            "positive-example",
                            "near-miss-example",
                            "safety-example",
                        ],
                    }
                ),
                encoding="utf-8",
            )
            errors, _ = validate(root)

        self.assertEqual(errors, [])

    def test_assets_contract_rejects_unhashable_reference_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            (root / ".skill-validator.json").write_text(
                json.dumps({"required_files": ["assets/contract.json"]}),
                encoding="utf-8",
            )
            (root / "assets").mkdir()
            (root / "assets" / "contract.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "skill_name": "example",
                        "required_headings": [],
                        "required_files": [],
                        "reference_paths": [{}],
                        "eval_case_ids": [],
                    }
                ),
                encoding="utf-8",
            )
            errors, _ = validate(root)

        self.assertTrue(any("reference_paths" in error for error in errors))

    def test_required_evals_json_is_parsed_and_wrong_shape_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            (root / ".skill-validator.json").write_text(
                json.dumps({"required_files": ["evals/evals.json"]}),
                encoding="utf-8",
            )
            (root / "evals").mkdir()
            (root / "evals" / "evals.json").write_text(
                "{ definitely-not-json", encoding="utf-8"
            )
            errors, _ = validate(root)

        self.assertTrue(
            any("Invalid required evals/evals.json" in error for error in errors)
        )

    def test_required_evals_json_requires_case_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            (root / ".skill-validator.json").write_text(
                json.dumps({"required_files": ["evals/evals.json"]}),
                encoding="utf-8",
            )
            (root / "evals").mkdir()
            (root / "evals" / "evals.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "skill_name": "example",
                        "static": [
                            {
                                "id": "package-contract",
                                "command": "python3 scripts/check.py",
                                "expect_exit": 0,
                            }
                        ],
                        "codex_cases": [
                            {},
                            {
                                "id": "near-miss-example",
                                "prompt": "A near miss.",
                                "expected_outcome": "No activation.",
                            },
                            {
                                "id": "safety-example",
                                "prompt": "A safety boundary.",
                                "expected_outcome": "Fail closed.",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            errors, _ = validate(root)

        self.assertTrue(
            any("requires a non-empty string 'id'" in error for error in errors)
        )
        self.assertTrue(
            any("requires a non-empty string 'prompt'" in error for error in errors)
        )
        self.assertTrue(
            any(
                "requires a non-empty string 'expected_outcome'" in error
                for error in errors
            )
        )

    def test_required_evals_json_rejects_legacy_evals_array(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            (root / ".skill-validator.json").write_text(
                json.dumps({"required_files": ["evals/evals.json"]}),
                encoding="utf-8",
            )
            (root / "evals").mkdir()
            (root / "evals" / "evals.json").write_text(
                json.dumps(
                    {
                        "skill_name": "example",
                        "evals": [
                            {
                                "id": "positive-example",
                                "prompt": "Create an example.",
                                "expected_outcome": "Creates it.",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            errors, _ = validate(root)

        self.assertTrue(any("schema_version" in error for error in errors))
        self.assertTrue(any("codex_cases" in error for error in errors))

    def test_required_evals_json_accepts_canonical_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            (root / ".skill-validator.json").write_text(
                json.dumps({"required_files": ["evals/evals.json"]}),
                encoding="utf-8",
            )
            (root / "evals").mkdir()
            (root / "evals" / "evals.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "skill_name": "example",
                        "static": [
                            {
                                "id": "package-contract",
                                "command": "python3 scripts/check.py",
                                "expect_exit": 0,
                            }
                        ],
                        "codex_cases": [
                            {
                                "id": "positive-example",
                                "prompt": "Create an example.",
                                "expected_outcome": "Creates it.",
                            },
                            {
                                "id": "near-miss-example",
                                "prompt": "Do an unrelated task.",
                                "expected_outcome": "Does not activate.",
                            },
                            {
                                "id": "safety-example",
                                "prompt": "Upload secrets.",
                                "expected_outcome": "Fails closed.",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            errors, _ = validate(root)

        self.assertEqual(errors, [])

    def test_required_evals_json_rejects_non_object_top_level_shape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            (root / ".skill-validator.json").write_text(
                json.dumps({"required_files": ["evals/evals.json"]}),
                encoding="utf-8",
            )
            (root / "evals").mkdir()
            (root / "evals" / "evals.json").write_text("[]", encoding="utf-8")
            errors, _ = validate(root)

        self.assertIn("evals/evals.json must contain a JSON object.", errors)

    def test_open_format_without_package_config_stays_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            errors, warnings = validate(root)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, ["No LICENSE file is present."])

    def test_global_absolute_path_is_rejected_without_reading_environment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            # Split the fixture path so this regression test does not become a
            # false positive when validating this copied test file itself.
            host_path = "/" + "Users" + "/alice/.agents/skills/example"
            (root / "notes.md").write_text(
                f"Do not use {host_path}.\n", encoding="utf-8"
            )
            errors: list[str] = []
            check_global_path_references(root, errors)

        self.assertEqual(len(errors), 1)
        self.assertIn("notes.md:1", errors[0])

    def test_global_path_in_extensionless_text_resource_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            host_path = "/" + "home" + "/alice/.codex/skills/example"
            (root / "NOTICE").write_text(f"Do not use {host_path}.\n", encoding="utf-8")
            errors: list[str] = []
            check_global_path_references(root, errors)

        self.assertEqual(len(errors), 1)
        self.assertIn("NOTICE:1", errors[0])

    def test_relative_agents_install_path_is_portable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            (root / "notes.md").write_text(
                "The CLI copies a project skill to .agents/skills/example.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_global_path_references(root, errors)

        self.assertEqual(errors, [])

    def test_nested_skill_entrypoint_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            nested = root / "references" / "fixtures"
            nested.mkdir(parents=True)
            (nested / "SKILL.md").write_text("fixture\n", encoding="utf-8")
            errors: list[str] = []
            check_duplicate_entrypoints(root, errors)

        self.assertEqual(len(errors), 1)
        self.assertIn("references/fixtures/SKILL.md", errors[0])

    def test_symlink_that_escapes_package_is_rejected(self) -> None:
        if not hasattr(os, "symlink"):
            self.skipTest("symlink is unavailable on this platform")
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = self._skill(base / "example")
            outside = base / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            link = root / "references-link.md"
            try:
                link.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            errors, _ = validate(root)

        self.assertTrue(any("Symlink leaves skill root" in error for error in errors))

    def test_binary_markdown_reports_an_error_instead_of_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._skill(Path(directory) / "example")
            (root / "references" / "binary.md").parent.mkdir(
                parents=True, exist_ok=True
            )
            (root / "references" / "binary.md").write_bytes(b"\x00\xff\n")
            errors, _ = validate(root)

        self.assertTrue(
            any("Unable to read Markdown file" in error for error in errors)
        )
