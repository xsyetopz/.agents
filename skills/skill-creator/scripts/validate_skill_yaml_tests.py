from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from test_support import (
    NON_FINITE_FLOAT_SPELLINGS,
    NUMERIC_SCALARS,
    check_agents_yaml,
)


class OpenAIYamlTests(unittest.TestCase):
    def test_openai_yaml_requires_interface_fields_under_interface_mapping(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface:\n"
                "  display_name: Example\n"
                "  short_description: Too short\n"
                "  default_prompt: Use the wrong skill.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertIn("short_description must be 25-64 characters", "\n".join(errors))
        self.assertIn("default_prompt must mention $example.", "\n".join(errors))

    def test_openai_yaml_fields_outside_interface_do_not_satisfy_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "display_name: Example\n"
                "short_description: This is outside the interface mapping.\n"
                "default_prompt: Use $example.\n"
                "interface:\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        joined = "\n".join(errors)
        self.assertIn("is missing required 'display_name'.", joined)
        self.assertIn("is missing required 'short_description'.", joined)
        self.assertIn("is missing required 'default_prompt'.", joined)

    def test_openai_yaml_accepts_folded_default_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface:\n"
                "  display_name: Example\n"
                "  short_description: Build and validate an example agent skill\n"
                "  default_prompt: >\n"
                "    Use $example to create the requested skill.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)
            self.assertEqual(errors, [])
            path = root / "agents" / "openai.yaml"
            path.write_text(path.read_text().replace("$example", "$example and $wrong"))
            check_agents_yaml(root, errors)
            self.assertIn("must invoke exactly $example", "\n".join(errors))

    def test_openai_yaml_accepts_flow_interface_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface: {display_name: Example, "
                "short_description: 'Build and validate an example skill', "
                "default_prompt: 'Use $example.'}\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertEqual(errors, [])

    def test_openai_yaml_accepts_trailing_comma_flow_interface_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface: {display_name: Example, "
                "short_description: 'Build and validate an example skill', "
                "default_prompt: 'Use $example.',}\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertEqual(errors, [])

    def test_malformed_openai_yaml_flow_mapping_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface: {display_name: Example, display_name: Duplicate}\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertTrue(
            any("malformed 'interface:' mapping" in error for error in errors)
        )

    def test_openai_yaml_rejects_empty_flow_interface_items(self) -> None:
        for flow_value in (
            "{,display_name: Example}",
            "{display_name: Example,,short_description: 'Build and validate an example skill'}",
        ):
            with self.subTest(value=flow_value):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "example"
                    (root / "agents").mkdir(parents=True)
                    (root / "agents" / "openai.yaml").write_text(
                        "interface: " + flow_value + "\n",
                        encoding="utf-8",
                    )
                    errors: list[str] = []
                    check_agents_yaml(root, errors)

                self.assertTrue(any("Empty flow item" in error for error in errors))

    def test_openai_yaml_rejects_flow_plain_punctuation_and_colon(self) -> None:
        for flow_value in (
            "{display_name: foo[bar]}",
            "{foo[bar]: Example}",
            "{display_name: normal:colon}",
        ):
            with self.subTest(value=flow_value):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "example"
                    (root / "agents").mkdir(parents=True)
                    (root / "agents" / "openai.yaml").write_text(
                        "interface: " + flow_value + "\n",
                        encoding="utf-8",
                    )
                    errors: list[str] = []
                    check_agents_yaml(root, errors)

                self.assertTrue(
                    any(
                        "Unsupported punctuation" in error
                        or "Colon is not supported" in error
                        for error in errors
                    )
                )

    def test_openai_yaml_preserves_nested_supported_flow_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface: {display_name: Example, "
                "short_description: 'Build and validate an example skill', "
                "default_prompt: 'Use $example.', nested: {ok: [1]},}\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertEqual(errors, [])

    def test_malformed_openai_yaml_top_level_sequence_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface:\n"
                "  display_name: Example\n"
                "  short_description: Build and validate an example agent skill\n"
                "  default_prompt: Use $example.\n"
                "- invalid-top-level-sequence\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertTrue(any("malformed top-level YAML" in error for error in errors))

    def test_orphan_indentation_before_interface_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "  malformed-orphan\n"
                "interface:\n"
                "  display_name: Example\n"
                "  short_description: Build and validate an example agent skill\n"
                "  default_prompt: Use $example.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertTrue(any("unexpected indentation" in error for error in errors))

    def test_orphan_indentation_after_scalar_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "display_name: Outside\n"
                "  malformed-orphan\n"
                "interface:\n"
                "  display_name: Example\n"
                "  short_description: Build and validate an example agent skill\n"
                "  default_prompt: Use $example.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertTrue(any("unexpected indentation" in error for error in errors))

    def test_invalid_double_quoted_openai_yaml_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            invalid_display_name = '  display_name: "Bad\\q"\n'
            (root / "agents" / "openai.yaml").write_text(
                "interface:\n"
                + invalid_display_name
                + "  short_description: Build and validate an example agent skill\n"
                + "  default_prompt: Use $example.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        joined = "\n".join(errors)
        self.assertIn("Invalid double-quoted scalar", joined)

    def test_tab_indented_openai_yaml_interface_child_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface:\n"
                "\tdisplay_name: Example\n"
                "\tshort_description: Build and validate an example agent skill\n"
                "\tdefault_prompt: Use $example.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertTrue(any("tab indentation" in error for error in errors))

    def test_tab_in_openai_yaml_scalar_content_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface:\n"
                "  display_name: Example\tSkill\n"
                "  short_description: Build and validate an example agent skill\n"
                "  default_prompt: Use $example.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertEqual(errors, [])

    def test_openai_yaml_rejects_unsupported_yaml_control_characters(self) -> None:
        for control in (
            "\x00",
            "\x01",
            "\x07",
            "\x0b",
            "\x0c",
            "\x0e",
            "\x1f",
            "\x7f",
            "\x80",
            "\x9f",
        ):
            with self.subTest(codepoint=f"U+{ord(control):04X}"):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "example"
                    (root / "agents").mkdir(parents=True)
                    (root / "agents" / "openai.yaml").write_text(
                        "interface:\r\n"
                        f"  display_name: Invalid{control}Skill\r\n"
                        "  short_description: Build and validate an example agent skill\r\n"
                        "  default_prompt: Use $example.\r\n",
                        encoding="utf-8",
                    )
                    errors: list[str] = []
                    check_agents_yaml(root, errors)

                self.assertTrue(
                    any("unsupported control character" in error for error in errors)
                )

    def test_openai_yaml_allows_permitted_controls_and_unicode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface:\r\n"
                "  display_name: Example\tSkill café 😀\r\n"
                "  short_description: Build and validate an example agent skill\r\n"
                "  default_prompt: Use $example.\r\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertEqual(errors, [])

    def test_openai_yaml_non_finite_float_spellings_fail_string_requirement(
        self,
    ) -> None:
        for spelling in NON_FINITE_FLOAT_SPELLINGS:
            with self.subTest(value=spelling):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "example"
                    (root / "agents").mkdir(parents=True)
                    (root / "agents" / "openai.yaml").write_text(
                        "interface:\n"
                        f"  display_name: {spelling}\n"
                        "  short_description: Build and validate an example agent skill\n"
                        "  default_prompt: Use $example.\n",
                        encoding="utf-8",
                    )
                    errors: list[str] = []
                    check_agents_yaml(root, errors)

                self.assertTrue(
                    any("missing required 'display_name'" in error for error in errors),
                    errors,
                )

    def test_openai_yaml_preserves_normal_strings_near_non_finite_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface:\n"
                "  display_name: Example .nan skill\n"
                "  short_description: Build and validate an example agent skill\n"
                "  default_prompt: Use $example.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertEqual(errors, [])

    def test_openai_yaml_numeric_scalars_fail_string_requirement(self) -> None:
        for spelling, _expected in NUMERIC_SCALARS:
            with self.subTest(value=spelling):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "example"
                    (root / "agents").mkdir(parents=True)
                    (root / "agents" / "openai.yaml").write_text(
                        "interface:\n"
                        f"  display_name: {spelling}\n"
                        "  short_description: Build and validate an example agent skill\n"
                        "  default_prompt: Use $example.\n",
                        encoding="utf-8",
                    )
                    errors: list[str] = []
                    check_agents_yaml(root, errors)

                self.assertTrue(
                    any("missing required 'display_name'" in error for error in errors),
                    errors,
                )

    def test_openai_yaml_preserves_normal_numeric_looking_strings(self) -> None:
        for display_name in ("Release v2.0 for 2025 users", "0x10 release notes"):
            with self.subTest(value=display_name):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "example"
                    (root / "agents").mkdir(parents=True)
                    (root / "agents" / "openai.yaml").write_text(
                        "interface:\n"
                        f"  display_name: {display_name}\n"
                        "  short_description: Build and validate an example agent skill\n"
                        "  default_prompt: Use $example.\n",
                        encoding="utf-8",
                    )
                    errors: list[str] = []
                    check_agents_yaml(root, errors)

                self.assertEqual(errors, [])

    def test_single_quoted_backslash_quote_openai_yaml_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface:\n"
                + r"  display_name: 'bad\'quote'"
                + "\n"
                + "  short_description: Build and validate an example agent skill\n"
                + "  default_prompt: Use $example.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertTrue(any("Backslash-quote" in error for error in errors))

    def test_mismatched_flow_delimiter_openai_yaml_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface: {bad]\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertTrue(any("Mismatched flow delimiters" in error for error in errors))

    def test_openai_yaml_quoted_scalar_rejects_trailing_text(self) -> None:
        for invalid_display_name in ("'foo'bar'", '"foo"bar"'):
            with self.subTest(value=invalid_display_name):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "example"
                    (root / "agents").mkdir(parents=True)
                    (root / "agents" / "openai.yaml").write_text(
                        "interface:\n"
                        "  display_name: " + invalid_display_name + "\n"
                        "  short_description: Build and validate an example agent skill\n"
                        "  default_prompt: Use $example.\n",
                        encoding="utf-8",
                    )
                    errors: list[str] = []
                    check_agents_yaml(root, errors)

                self.assertTrue(any("Trailing text" in error for error in errors))

    def test_openai_yaml_plain_scalar_rejects_ambiguous_indicators(self) -> None:
        for invalid_display_name in (
            "Use when: building skills",
            ": bad",
            "@bad",
            "`bad",
        ):
            with self.subTest(value=invalid_display_name):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "example"
                    (root / "agents").mkdir(parents=True)
                    (root / "agents" / "openai.yaml").write_text(
                        "interface:\n"
                        "  display_name: " + invalid_display_name + "\n"
                        "  short_description: Build and validate an example agent skill\n"
                        "  default_prompt: Use $example.\n",
                        encoding="utf-8",
                    )
                    errors: list[str] = []
                    check_agents_yaml(root, errors)

                self.assertTrue(
                    any(
                        "Unsupported YAML plain-scalar indicator" in error
                        or "Colon followed" in error
                        for error in errors
                    )
                )

    def test_openai_yaml_plain_scalar_controls_remain_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / "agents").mkdir(parents=True)
            (root / "agents" / "openai.yaml").write_text(
                "interface:\n"
                "  display_name: normal:colon\n"
                "  short_description: Build and validate an example agent skill\n"
                "  default_prompt: Use $example.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_agents_yaml(root, errors)

        self.assertEqual(errors, [])
