from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from test_support import (
    NON_FINITE_FLOAT_SPELLINGS,
    NUMERIC_SCALARS,
    _parse_scalar,
    _split_flow_items,
    _split_mapping_entry,
    check_frontmatter_spec,
    parse_frontmatter,
)


class FrontmatterDescriptionTests(unittest.TestCase):
    def test_folded_description_is_parsed_as_catalog_text(self) -> None:
        metadata, body = parse_frontmatter(
            """---
name: example-skill
description: >
  Use when asked to validate a folded catalog description.
  Covers multiline parsing and whitespace normalization.
metadata:
  author: example
---
# Example Skill
"""
        )

        self.assertEqual(metadata["name"], "example-skill")
        self.assertEqual(
            metadata["description"],
            "Use when asked to validate a folded catalog description. "
            "Covers multiline parsing and whitespace normalization.",
        )
        self.assertEqual(body, "# Example Skill")

    def test_description_limit_uses_full_folded_value(self) -> None:
        metadata, _ = parse_frontmatter(
            "---\nname: example\ndescription: >\n  " + ("x" * 1025) + "\n---\n"
        )
        errors: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            check_frontmatter_spec(metadata, root, errors)

        self.assertIn("'description' exceeds 1024 characters (got 1025).", errors)

    def test_optional_metadata_and_allowed_tools_are_accepted(self) -> None:
        metadata, _ = parse_frontmatter(
            "---\n"
            "name: example\n"
            "description: A valid skill description.\n"
            "license: MIT\n"
            "compatibility: macOS\n"
            "metadata:\n"
            "  author: example\n"
            "  version: '1.0'\n"
            "allowed-tools: Read Grep\n"
            "---\n"
        )
        errors: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            check_frontmatter_spec(metadata, Path(directory) / "example", errors)

        self.assertEqual(metadata["metadata"], {"author": "example", "version": "1.0"})
        self.assertEqual(metadata["allowed-tools"], "Read Grep")
        self.assertEqual(errors, [])

    def test_indented_top_level_frontmatter_line_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unexpected indentation"):
            parse_frontmatter(
                "---\n"
                "name: example\n"
                "description: A valid description.\n"
                "  malformed: ignored-no-more\n"
                "---\n"
            )

    def test_tab_indented_frontmatter_metadata_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "tab indentation"):
            parse_frontmatter(
                "---\n"
                "name: example\n"
                "description: Valid description\n"
                "metadata:\n"
                "\tauthor: example\n"
                "---\n"
            )

    def test_tab_in_plain_frontmatter_scalar_content_is_allowed(self) -> None:
        metadata, _ = parse_frontmatter(
            "---\nname: example\ndescription: Valid\tcontent\n---\n"
        )

        self.assertEqual(metadata["description"], "Valid\tcontent")

    def test_frontmatter_rejects_unsupported_yaml_control_characters(self) -> None:
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
            with (
                self.subTest(codepoint=f"U+{ord(control):04X}"),
                self.assertRaisesRegex(ValueError, "unsupported control character"),
            ):
                parse_frontmatter(
                    "---\r\n"
                    "name: example\r\n"
                    f"description: Invalid{control}content\r\n"
                    "---\r\n"
                )

    def test_frontmatter_allows_permitted_controls_and_unicode(self) -> None:
        metadata, _ = parse_frontmatter(
            "---\r\nname: example\r\ndescription: Valid\tcontent café 😀\r\n---\r\n"
        )

        self.assertEqual(metadata["description"], "Valid\tcontent café 😀")

    def test_frontmatter_non_finite_float_spellings_fail_string_requirement(
        self,
    ) -> None:
        for spelling in NON_FINITE_FLOAT_SPELLINGS:
            with self.subTest(value=spelling):
                metadata, _ = parse_frontmatter(
                    f"---\nname: example\ndescription: {spelling}\n---\n"
                )
                self.assertIsInstance(metadata["description"], float)
                errors: list[str] = []
                check_frontmatter_spec(metadata, Path("example"), errors)

            self.assertTrue(any("description" in error for error in errors), errors)

    def test_quoted_non_finite_float_spellings_remain_strings(self) -> None:
        for spelling in NON_FINITE_FLOAT_SPELLINGS:
            with self.subTest(value=spelling):
                metadata, _ = parse_frontmatter(
                    f'---\nname: example\ndescription: "{spelling}"\n---\n'
                )

            self.assertEqual(metadata["description"], spelling)

    def test_frontmatter_numeric_scalars_fail_string_requirement(self) -> None:
        for spelling, expected in NUMERIC_SCALARS:
            with self.subTest(value=spelling):
                metadata, _ = parse_frontmatter(
                    f"---\nname: example\ndescription: {spelling}\n---\n"
                )
                self.assertEqual(metadata["description"], expected)
                self.assertIs(type(metadata["description"]), type(expected))
                errors: list[str] = []
                check_frontmatter_spec(metadata, Path("example"), errors)

                self.assertTrue(any("description" in error for error in errors), errors)

    def test_quoted_and_tagged_numeric_scalars_remain_strings(self) -> None:
        for spelling, _expected in NUMERIC_SCALARS:
            with self.subTest(value=spelling):
                quoted, _ = parse_frontmatter(
                    f'---\nname: example\ndescription: "{spelling}"\n---\n'
                )
                tagged, _ = parse_frontmatter(
                    f"---\nname: example\ndescription: !!str {spelling}\n---\n"
                )

                self.assertEqual(quoted["description"], spelling)
                self.assertEqual(tagged["description"], spelling)
                self.assertIsInstance(quoted["description"], str)
                self.assertIsInstance(tagged["description"], str)

    def test_unsupported_numeric_looking_scalars_fail_closed(self) -> None:
        for value in ("0b102", "0o8", "0xGG", "1__2", "1_", "1e", "1.0.0"):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(
                    ValueError, "Unsupported YAML (base )?numeric scalar"
                ),
            ):
                _parse_scalar(value)

    def test_normal_numeric_looking_strings_remain_strings(self) -> None:
        for description in (
            "Release v2.0 for 2025 users",
            "0x10 release notes",
        ):
            with self.subTest(value=description):
                metadata, _ = parse_frontmatter(
                    f"---\nname: example\ndescription: {description}\n---\n"
                )

            self.assertEqual(metadata["description"], description)

    def test_invalid_double_quoted_frontmatter_escape_is_rejected(self) -> None:
        invalid_description = 'description: "bad\\q"\n'
        with self.assertRaisesRegex(ValueError, "Invalid double-quoted scalar"):
            parse_frontmatter("---\nname: example\n" + invalid_description + "---\n")

    def test_valid_escaped_double_quote_frontmatter_scalar_is_preserved(self) -> None:
        metadata, _ = parse_frontmatter(
            '---\nname: example\ndescription: "Use \\"quoted\\" wording"\n---\n'
        )

        self.assertEqual(metadata["description"], 'Use "quoted" wording')

    def test_valid_single_quoted_scalar_uses_doubled_quote(self) -> None:
        metadata, _ = parse_frontmatter(
            "---\nname: example\ndescription: 'It''s valid'\n---\n"
        )

        self.assertEqual(metadata["description"], "It's valid")

    def test_single_quoted_backslash_quote_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Backslash-quote"):
            parse_frontmatter(
                "---\nname: example\n" + r"description: 'bad\'quote'" + "\n---\n"
            )

    def test_quoted_scalar_rejects_trailing_text_after_closing_quote(self) -> None:
        for invalid_description in (
            "'foo'bar'",
            "'foo' bar'",
            '"foo"bar"',
            '"foo" bar"',
        ):
            with (
                self.subTest(value=invalid_description),
                self.assertRaisesRegex(ValueError, "Trailing text"),
            ):
                parse_frontmatter(
                    "---\n"
                    "name: example\n"
                    "description: " + invalid_description + "\n---\n"
                )

    def test_mapping_entry_rejects_unbalanced_quote_or_brackets(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unterminated quote"):
            _split_mapping_entry('description: "unterminated')
        with self.assertRaisesRegex(ValueError, "Unbalanced brackets"):
            _split_mapping_entry("metadata: {author: example")

    def test_flow_items_reject_unbalanced_quote_or_brackets(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unterminated quote"):
            _split_flow_items('author: "unterminated')
        with self.assertRaisesRegex(ValueError, "Unbalanced brackets"):
            _split_flow_items("author: [example")

    def test_flow_items_reject_empty_leading_or_repeated_items(self) -> None:
        for value in (",author: example", "author: example,,version: '1.0'"):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(ValueError, "Empty flow item"),
            ):
                _split_flow_items(value)

    def test_flow_items_allow_empty_flow_and_one_trailing_comma(self) -> None:
        self.assertEqual(_split_flow_items(""), [])
        self.assertEqual(_split_flow_items("author: example,"), ["author: example"])

    def test_flow_scalar_rejects_mismatched_delimiters(self) -> None:
        for value in ("{bad]", "[bad}"):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(ValueError, "Mismatched flow delimiters"),
            ):
                _parse_scalar(value)

    def test_plain_scalar_rejects_ambiguous_indicators_and_colon_space(self) -> None:
        for invalid_description in (
            "Use when: building skills",
            ": bad",
            "@bad",
            "`bad",
        ):
            with (
                self.subTest(value=invalid_description),
                self.assertRaisesRegex(ValueError, "Unsupported YAML|Colon followed"),
            ):
                parse_frontmatter(
                    "---\n"
                    "name: example\n"
                    "description: " + invalid_description + "\n---\n"
                )

    def test_plain_scalar_controls_remain_valid(self) -> None:
        metadata, _ = parse_frontmatter(
            "---\nname: example\ndescription: normal:colon\n---\n"
        )

        self.assertEqual(metadata["description"], "normal:colon")
