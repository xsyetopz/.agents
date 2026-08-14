from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from test_support import (
    check_broken_references,
    check_duplicate_headers,
    check_markdown_links,
    check_skill_creator_references,
    validate,
)
from validate_skill_contract_tests import PackageContractTests


class ReferenceAndYamlTests(unittest.TestCase):
    @staticmethod
    def _router_fixture(directory: str, *, text: str) -> Path:
        root = Path(directory) / "skill-creator"
        references = root / "references"
        references.mkdir(parents=True)
        (references / "index.md").write_text(text, encoding="utf-8")
        return root

    def test_skill_creator_mermaid_requires_github_safe_edges_and_fence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._router_fixture(
                directory,
                text=(
                    "# Skill creator reference router\n\n"
                    "## Authoring\n| When you need | Read |\n| --- | --- |\n| x | [x](x.md) |\n"
                    "## Metadata and routing\n| When you need | Read |\n| --- | --- |\n| x | [x](x.md) |\n"
                    "## Validation and safety\n| When you need | Read |\n| --- | --- |\n| x | [x](x.md) |\n"
                    "## Distribution\n| When you need | Read |\n| --- | --- |\n| x | [x](x.md) |\n"
                ),
            )
            graph = root / "references" / "graph.md"
            graph.write_text(
                "flowchart LR\nA -- no --> B\n\n"
                "```mermaid\nflowchart LR\nA -- no --> B\n```\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_skill_creator_references(root, errors)

        self.assertTrue(any("must be in a ```mermaid fence" in error for error in errors))
        self.assertTrue(any("must use -->|label| syntax" in error for error in errors))

    def test_skill_creator_mermaid_accepts_fenced_label_syntax(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._router_fixture(
                directory,
                text=(
                    "# Skill creator reference router\n\n"
                    "## Authoring\n| When you need | Read |\n| --- | --- |\n| x | [x](x.md) |\n"
                    "## Metadata and routing\n| When you need | Read |\n| --- | --- |\n| x | [x](x.md) |\n"
                    "## Validation and safety\n| When you need | Read |\n| --- | --- |\n| x | [x](x.md) |\n"
                    "## Distribution\n| When you need | Read |\n| --- | --- |\n| x | [x](x.md) |\n"
                ),
            )
            (root / "references" / "graph.md").write_text(
                "```mermaid\nflowchart LR\nA -->|next| B\n```\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_skill_creator_references(root, errors)

        self.assertEqual(errors, [])

    def test_markdown_links_allow_external_urls_but_reject_missing_local_target(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            (root / "SKILL.md").write_text("# Example\n", encoding="utf-8")
            text = (
                "[official](https://example.com/spec)\n"
                "[missing](references/missing.md)\n"
            )
            errors: list[str] = []
            check_broken_references(text, root, errors)

        self.assertEqual(
            errors, ["Broken relative reference in SKILL.md: references/missing.md"]
        )

    def test_official_snapshot_keeps_root_links_and_repeated_page_title_valid(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = PackageContractTests._skill(Path(directory) / "example")
            official = root / "references" / "official" / "page.md"
            official.parent.mkdir(parents=True)
            snapshot = (
                b"# Official page\n"
                b"> For the docs index, see [llms.txt](/llms.txt).\n"
                b"# Official page\n"
            )
            official.write_bytes(snapshot)

            errors, _warnings = validate(root)

            self.assertEqual(official.read_bytes(), snapshot)

        self.assertEqual(errors, [])

    def test_ordinary_package_root_link_remains_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = PackageContractTests._skill(Path(directory) / "example")
            ordinary = root / "references" / "guide.md"
            ordinary.parent.mkdir(parents=True)
            ordinary.write_text("[absolute](/absolute.md)\n", encoding="utf-8")
            errors: list[str] = []
            check_markdown_links(root, errors, [])

        self.assertEqual(
            errors,
            [
                "Relative reference leaves skill root in references/guide.md: /absolute.md"
            ],
        )

    def test_official_snapshot_root_traversal_is_not_treated_as_external(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = PackageContractTests._skill(Path(directory) / "example")
            official = root / "references" / "official" / "page.md"
            official.parent.mkdir(parents=True)
            official.write_text("[outside](/../secret.md)\n", encoding="utf-8")
            errors: list[str] = []
            check_markdown_links(root, errors, [])

        self.assertEqual(
            errors,
            [
                (
                    "Relative reference leaves skill root in "
                    "references/official/page.md: /../secret.md"
                )
            ],
        )

    def test_official_snapshot_duplicate_non_title_heading_is_still_rejected(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = PackageContractTests._skill(Path(directory) / "example")
            official = root / "references" / "official" / "page.md"
            official.parent.mkdir(parents=True)
            official.write_text(
                "# Official page\n## Details\n## Details\n", encoding="utf-8"
            )
            errors: list[str] = []
            check_duplicate_headers(root, errors)

        self.assertEqual(len(errors), 1)
        self.assertIn("references/official/page.md:3", errors[0])

    def test_official_title_exception_does_not_reset_heading_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = PackageContractTests._skill(Path(directory) / "example")
            official = root / "references" / "official" / "page.md"
            official.parent.mkdir(parents=True)
            official.write_text(
                "# Official page\n## Details\n# Official page\n## Details\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            check_duplicate_headers(root, errors)

        self.assertEqual(len(errors), 1)
        self.assertIn("references/official/page.md:4", errors[0])
