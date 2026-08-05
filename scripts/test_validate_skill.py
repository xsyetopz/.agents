from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from validate_skill import (
    check_agents_yaml,
    check_duplicate_headers,
    check_frontmatter_spec,
    parse_frontmatter,
)


class FrontmatterDescriptionTests(unittest.TestCase):
    def test_folded_description_is_parsed_as_catalog_text(self) -> None:
        metadata, body = parse_frontmatter(
            """---
name: git-toolkit
description: >
  Use when asked to stage, commit, amend, or write a Conventional Commit.
  Covers git add, git commit, status, diff, and restore.
metadata:
  author: example
---
# Git Toolkit
"""
        )

        self.assertEqual(metadata["name"], "git-toolkit")
        self.assertEqual(
            metadata["description"],
            "Use when asked to stage, commit, amend, or write a Conventional Commit. "
            "Covers git add, git commit, status, diff, and restore.",
        )
        self.assertEqual(body, "# Git Toolkit")

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


if __name__ == "__main__":
    unittest.main()
