from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from check_skill_structure import root_index_duplicates
from test_support import (
    check_agents_yaml,
    check_broken_references,
    check_duplicate_headers,
    check_frontmatter_spec,
    parse_frontmatter,
    validate,
)


class BaselineValidatorTests(unittest.TestCase):
    def test_metadata_requires_string_keys_and_values(self) -> None:
        metadata, _ = parse_frontmatter(
            "---\n"
            "name: example\n"
            "description: A valid skill description.\n"
            "metadata:\n"
            "  version: 1\n"
            "  2: value\n"
            "---\n"
        )
        errors: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            check_frontmatter_spec(metadata, Path(directory) / "example", errors)

        self.assertIn("'metadata' value for key 'version' must be a string.", errors)
        self.assertIn("'metadata' key 2 must be a string.", errors)

    def test_frontmatter_preserves_quoted_colons_and_flow_metadata(self) -> None:
        metadata, _ = parse_frontmatter(
            "---\n"
            "name: example\n"
            'description: "Use: exact wording"\n'
            "metadata: {author: example, version: '1.0'}\n"
            "---\n"
        )

        self.assertEqual(metadata["description"], "Use: exact wording")
        self.assertEqual(metadata["metadata"], {"author": "example", "version": "1.0"})

    def test_frontmatter_rejects_empty_flow_metadata_items(self) -> None:
        for flow_value in ("{,author: example}", "{author: example,,version: '1.0'}"):
            with (
                self.subTest(value=flow_value),
                self.assertRaisesRegex(ValueError, "Empty flow item"),
            ):
                parse_frontmatter(
                    "---\n"
                    "name: example\n"
                    "description: Valid description\n"
                    f"metadata: {flow_value}\n"
                    "---\n"
                )

    def test_frontmatter_allows_trailing_comma_flow_metadata(self) -> None:
        metadata, _ = parse_frontmatter(
            "---\n"
            "name: example\n"
            "description: Valid description\n"
            "metadata: {author: example,}\n"
            "---\n"
        )

        self.assertEqual(metadata["metadata"], {"author": "example"})

    def test_frontmatter_rejects_flow_plain_punctuation_and_colon(self) -> None:
        for flow_value in (
            "{author: foo[bar]}",
            "{foo[bar]: baz}",
            "{author: normal:colon}",
        ):
            with (
                self.subTest(value=flow_value),
                self.assertRaisesRegex(
                    ValueError, "Unsupported punctuation|Colon is not supported"
                ),
            ):
                parse_frontmatter(
                    "---\n"
                    "name: example\n"
                    "description: Valid description\n"
                    f"metadata: {flow_value}\n"
                    "---\n"
                )

    def test_frontmatter_preserves_nested_supported_flow_values(self) -> None:
        metadata, _ = parse_frontmatter(
            "---\n"
            "name: example\n"
            "description: Valid description\n"
            "metadata: {nested: {ok: [1]}}\n"
            "---\n"
        )

        self.assertEqual(metadata["metadata"], {"nested": {"ok": [1]}})

    def test_whitespace_only_required_values_are_rejected(self) -> None:
        metadata, _ = parse_frontmatter("---\nname: '   '\ndescription: \"   \"\n---\n")
        errors: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            check_frontmatter_spec(metadata, Path(directory) / "   ", errors)

        self.assertIn("Frontmatter requires non-empty 'name'.", errors)
        self.assertIn("Frontmatter requires non-empty 'description'.", errors)

    def test_duplicate_metadata_key_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Duplicate frontmatter metadata key"):
            parse_frontmatter(
                "---\n"
                "name: example\n"
                "description: A valid skill description.\n"
                "metadata:\n"
                "  author: one\n"
                "  author: two\n"
                "---\n"
            )

    def test_duplicate_top_level_frontmatter_key_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Duplicate frontmatter key"):
            parse_frontmatter(
                "---\nname: example\ndescription: first\ndescription: second\n---\n"
            )

    def test_repeated_child_heading_under_different_parents_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide.md").write_text(
                "# Guide\n## iOS\n### Small\n## watchOS\n### Small\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_duplicate_headers(root, errors)

        self.assertEqual(errors, [])

    def test_repeated_heading_under_same_parent_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide.md").write_text(
                "# Guide\n## watchOS\n### Small\n### Small\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_duplicate_headers(root, errors)

        self.assertEqual(len(errors), 1)

    def test_openai_metadata_requires_exact_skill_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "git-toolkit"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface:\n"
                "  display_name: Git Toolkit\n"
                "  short_description: Stage and commit local Git changes\n"
                "  default_prompt: Use $git-workflows to commit.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertIn(
            "agents/openai.yaml default_prompt must mention $git-toolkit.",
            errors,
        )

    def test_skill_without_optional_project_files_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            (root / "SKILL.md").write_text(
                "---\n"
                "name: example\n"
                "description: Use this skill for the example task.\n"
                "---\n"
                "# Example\n",
                encoding="utf-8",
            )

            errors, warnings = validate(root)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, ["No LICENSE file is present."])

    def test_skill_root_reference_is_checked_without_flagging_repository_command(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            (root / "references").mkdir()
            (root / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            text = (
                "# Example\n"
                "Read [the guide](references/guide.md).\n"
                "Run "
                + chr(96)
                + "python3 skills/other/scripts/check.py"
                + chr(96)
                + ".\n"
                "Do not read [outside](../secret.md).\n"
            )
            errors: list[str] = []
            check_broken_references(text, root, errors)

        self.assertEqual(
            errors,
            ["Relative reference leaves skill root in SKILL.md: ../secret.md"],
        )

    def test_resource_reference_trims_terminal_punctuation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            (root / "assets").mkdir()
            (root / "assets" / "template.md").write_text(
                "# Template\n", encoding="utf-8"
            )
            errors: list[str] = []
            check_broken_references("Use ./assets/template.md.\n", root, errors)

        self.assertEqual(errors, [])

    def test_root_index_duplicate_guard_counts_three_leaf_routes(self) -> None:
        names = ("one", "two", "three")
        resources = "## Resources\n" + "\n".join(
            f"- [{name}](references/{name}.md)" for name in names
        )
        index = "\n".join(f"- [{name}]({name}.md)" for name in names)

        self.assertEqual(
            root_index_duplicates(resources, index),
            {f"references/{name}.md" for name in names},
        )


if __name__ == "__main__":
    unittest.main()
