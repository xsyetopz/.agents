"""Governance document planning and README behavior tests."""

from __future__ import annotations

import json

from test_governance_support import (
    GovernanceTestCase,
    agent_boundaries,
    governance,
    markdown_sections,
)


class GovernanceDocumentTests(GovernanceTestCase):
    def test_preview_is_read_only_and_apply_requires_authorization(self) -> None:
        before = (self.repo / "README.md").read_bytes()
        preview = self.run_cli()
        self.assertEqual(0, preview.returncode, preview.stderr)
        self.assertTrue(
            any(
                item["action"] == "create"
                for item in json.loads(preview.stdout)["operations"]
            )
        )
        self.assertEqual(before, (self.repo / "README.md").read_bytes())
        unauthorized = self.run_cli("--apply")
        self.assertEqual(2, unauthorized.returncode)
        self.assertIn("--confirm-authorized", unauthorized.stderr)
        self.assertFalse((self.repo / "AGENTS.md").exists())

    def test_apply_creates_exact_surface_and_is_idempotent(self) -> None:
        result = self.apply()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])
        self.assertEqual(
            "@AGENTS.md\n", (self.repo / "CLAUDE.md").read_text(encoding="utf-8")
        )
        self.assertEqual(
            "@./AGENTS.md\n", (self.repo / "GEMINI.md").read_text(encoding="utf-8")
        )
        self.assertEqual(
            governance.render("cursor-rule.mdc.tmpl"),
            (self.repo / ".cursor/rules/agents.mdc").read_text(encoding="utf-8"),
        )
        agents = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(
            "Agent rules",
            [
                heading.title
                for heading in markdown_sections.headings(agents)
                if heading.level == 2
            ][-1],
        )
        second = self.run_cli()
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual(
            {"noop"},
            {item["action"] for item in json.loads(second.stdout)["operations"]},
        )

    def test_existing_documents_update_all_owned_sections_and_preserve_unrelated_sections(
        self,
    ) -> None:
        (self.repo / "CONTRIBUTING.md").write_text(
            "# Local\n\nKeep preface.\n\n## Tool-assisted contributions\n\nOld.\n\n## Local process\n\nKeep local.\n",
            encoding="utf-8",
        )
        (self.repo / "AGENTS.md").write_text(
            "# Local\n\n## Agent rules\n\nOld.\n\n## Local agent note\n\nKeep this before the rules.\n",
            encoding="utf-8",
        )
        github = self.repo / ".github"
        github.mkdir()
        (github / "pull_request_template.md").write_text(
            "## Local field\n\nKeep.\n\n## Summary\n\nOld.\n", encoding="utf-8"
        )
        result = self.apply()
        self.assertEqual(0, result.returncode, result.stderr)
        contributing = (self.repo / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("Keep preface.", contributing)
        self.assertIn("## Local process\n\nKeep local.", contributing)
        for title in governance.HUMAN_SECTIONS:
            self.assertEqual(
                1, len(markdown_sections.matching_headings(contributing, title, 2))
            )
        agents = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Keep this before the rules.", agents)
        self.assertTrue(
            agents.rstrip().endswith(
                markdown_sections.section(agents, governance.AGENT_SECTION).rstrip()
            )
        )
        pull_request = (github / "pull_request_template.md").read_text(encoding="utf-8")
        self.assertIn("## Local field\n\nKeep.", pull_request)
        for title in governance.PR_SECTIONS:
            self.assertEqual(
                1, len(markdown_sections.matching_headings(pull_request, title, 2))
            )

    def test_fenced_fake_headings_are_text_not_sections(self) -> None:
        (self.repo / "AGENTS.md").write_text(
            "# Local\n\n```markdown\n## Agent rules\n## Tool-assisted contributions\n```\n\nKeep example.\n",
            encoding="utf-8",
        )
        tilde_fence = chr(0x7E) * 3
        (self.repo / "CONTRIBUTING.md").write_text(
            f"# Local\n\n{tilde_fence}md\n## Tool-assisted contributions\n{tilde_fence}\n",
            encoding="utf-8",
        )
        result = self.apply()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            1,
            len(
                markdown_sections.matching_headings(
                    (self.repo / "AGENTS.md").read_text(), "Agent rules", 2
                )
            ),
        )
        self.assertEqual(
            1,
            len(
                markdown_sections.matching_headings(
                    (self.repo / "CONTRIBUTING.md").read_text(),
                    "Tool-assisted contributions",
                    2,
                )
            ),
        )

    def test_setext_headings_are_discovered_outside_fences(self) -> None:
        text = (
            "```md\nAgent rules\n-----------\n```\n\nAgent rules\n-----------\nBody.\n"
        )
        matches = markdown_sections.matching_headings(text, "Agent rules", 2)
        self.assertEqual(1, len(matches))
        self.assertEqual(
            "Agent rules\n-----------\nBody.\n",
            markdown_sections.section(text, "Agent rules"),
        )

    def test_real_duplicate_wrong_level_and_human_agent_heading_conflict(self) -> None:
        cases = (
            ("# Agent rules\n\nWrong.\n", "owned Markdown heading must use level 2"),
            (
                "## Agent rules\n\nOne.\n\n## Agent rules\n\nTwo.\n",
                "duplicate Markdown heading",
            ),
            (
                "## Contribution requirements\n\nHuman rules.\n",
                "contains human governance heading",
            ),
        )
        for index, (content, expected) in enumerate(cases):
            with self.subTest(index=index):
                (self.repo / "AGENTS.md").write_text(content, encoding="utf-8")
                result = self.run_cli()
                self.assertEqual(2, result.returncode)
                self.assertIn(expected, result.stdout)
                (self.repo / "AGENTS.md").unlink()

    def test_human_governance_heading_classifier_and_reviewer_reproduction(
        self,
    ) -> None:
        human_headings = (
            "Human contributor conduct",
            "Code of conduct",
            "Contributing",
            "Contribution requirements",
            "Pull requests",
            "Responsibility and rights",
            "Community conduct",
            "Human conduct",
            "Contribution review policy",
            "Tool-assisted contributor rules",
        )
        for title in human_headings:
            with self.subTest(title=title):
                self.assertTrue(agent_boundaries.is_human_governance_heading(title, 2))
        self.assertFalse(
            agent_boundaries.is_human_governance_heading("Human certification", 3)
        )
        for title in (
            "Review process",
            "Agent review workflow",
            "Review and validation",
        ):
            with self.subTest(allowed=title):
                self.assertFalse(agent_boundaries.is_human_governance_heading(title, 2))
        (self.repo / "AGENTS.md").write_text(
            "# Local agents\n\n## Human contributor conduct\n\nBe respectful.\n\n"
            "## Agent rules\n\nOld rules.\n",
            encoding="utf-8",
        )
        result = self.apply()
        self.assertEqual(2, result.returncode)
        self.assertIn(
            "human governance heading: Human contributor conduct", result.stdout
        )
        self.assertFalse((self.repo / "CONTRIBUTING.md").exists())

    def test_validate_rejects_agent_contradiction_or_content_after_exact_section(
        self,
    ) -> None:
        self.assertEqual(0, self.apply().returncode)
        path = self.repo / "AGENTS.md"
        original = path.read_text(encoding="utf-8")
        path.write_text(
            original + "\nExtra instruction that weakens the rules.\n", encoding="utf-8"
        )
        result = self.run_cli("--validate-only")
        self.assertEqual(1, result.returncode)
        self.assertIn("modified Agent rules section", result.stdout)
        path.write_text(
            original + "\n## Appendix\n\nContradictory rule.\n", encoding="utf-8"
        )
        result = self.run_cli("--validate-only")
        self.assertEqual(1, result.returncode)
        self.assertIn("exact final level-2 section", result.stdout)
        path.write_text(
            original + "\n# Later document\n\nContradictory rule.\n", encoding="utf-8"
        )
        result = self.run_cli("--validate-only")
        self.assertEqual(1, result.returncode)
        self.assertIn("exact final level-2 section", result.stdout)

    def test_foreign_provider_conflict_preserves_all_files(self) -> None:
        (self.repo / "CLAUDE.md").write_text(
            "Foreign instructions.\n", encoding="utf-8"
        )
        result = self.apply()
        self.assertEqual(2, result.returncode)
        self.assertEqual(
            "Foreign instructions.\n",
            (self.repo / "CLAUDE.md").read_text(encoding="utf-8"),
        )
        self.assertFalse((self.repo / "AGENTS.md").exists())

    def test_readme_root_and_nested_links_are_relative_and_exact(self) -> None:
        self.assertEqual(0, self.apply(*self.locale_args()).returncode)
        root_text = (self.repo / "README.md").read_text(encoding="utf-8")
        root_section = markdown_sections.section(root_text, governance.README_SECTION)
        self.assertIn("[`CONTRIBUTING.md`](CONTRIBUTING.md)", root_section)
        self.assertIn("[et human](docs/i18n/et/CONTRIBUTING.md)", root_section)

        nested_repo = self.base / "nested-repo"
        nested_repo.mkdir()
        self.repo = nested_repo
        docs = nested_repo / "docs"
        docs.mkdir()
        (docs / "README.md").write_text(
            "# Docs\n\n## License\n\nKeep.\n", encoding="utf-8"
        )
        result = self.apply("--readme", "docs/README.md", *self.locale_args("fr"))
        self.assertEqual(0, result.returncode, result.stderr)
        section = markdown_sections.section(
            (docs / "README.md").read_text(), governance.README_SECTION
        )
        self.assertIn("[`CONTRIBUTING.md`](../CONTRIBUTING.md)", section)
        self.assertIn("[`AGENTS.md`](../AGENTS.md)", section)
        self.assertIn("[fr human](i18n/fr/CONTRIBUTING.md)", section)

    def test_readme_reanchors_before_real_heading_but_ignores_fenced_heading(
        self,
    ) -> None:
        (self.repo / "README.md").write_text(
            "# Demo\n\n```md\n## License\n```\n\n## License\n\nReal.\n\n## Contributing and coding agents\n\nOld.\n",
            encoding="utf-8",
        )
        result = self.apply()
        self.assertEqual(0, result.returncode, result.stderr)
        headings = markdown_sections.headings((self.repo / "README.md").read_text())
        positions = {
            heading.title: heading.start for heading in headings if heading.level == 2
        }
        self.assertLess(positions[governance.README_SECTION], positions["License"])

    def test_readme_validation_matches_lowercase_before_heading(self) -> None:
        (self.repo / "README.md").write_text(
            "# Demo\n\n## license\n\nMIT license text.\n", encoding="utf-8"
        )
        self.assertEqual(0, self.apply().returncode)
        path = self.repo / "README.md"
        text = path.read_text(encoding="utf-8")
        section = markdown_sections.section(text, governance.README_SECTION)
        without = text.replace(section + "\n", "", 1).rstrip()
        path.write_text(without + "\n\n" + section, encoding="utf-8")
        result = self.run_cli("--validate-only")
        self.assertEqual(1, result.returncode)
        self.assertIn("must precede heading: license", result.stdout)


__all__ = ["GovernanceDocumentTests"]
