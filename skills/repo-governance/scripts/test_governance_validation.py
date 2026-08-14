"""Exact governance validation behavior tests."""

from __future__ import annotations

from test_governance_support import GovernanceTestCase, markdown_sections


class GovernanceValidationTests(GovernanceTestCase):
    def test_validate_requires_exact_human_pr_agent_and_readme_sections(self) -> None:
        self.assertEqual(0, self.apply().returncode)
        cases = (
            (
                "CONTRIBUTING.md",
                "Run the relevant checks",
                "Run some checks",
                "modified Contribution requirements section",
            ),
            (
                ".github/pull_request_template.md",
                "## Related work",
                "## Related items",
                "level-2 Related work section",
            ),
            (
                "AGENTS.md",
                "Discuss the work, not a person.",
                "Discuss anything.",
                "modified Agent rules section",
            ),
            (
                "README.md",
                "before submitting a change",
                "before changing anything",
                "modified Contributing and coding agents section",
            ),
        )
        originals = {}
        for relative, old, new, expected in cases:
            path = self.repo / relative
            originals[path] = path.read_text()
            with self.subTest(relative=relative):
                path.write_text(originals[path].replace(old, new), encoding="utf-8")
                result = self.run_cli("--validate-only")
                self.assertEqual(1, result.returncode)
                self.assertIn(expected, result.stdout)
                path.write_text(originals[path], encoding="utf-8")

    def test_validate_rejects_reordered_pull_request_sections(self) -> None:
        self.assertEqual(0, self.apply().returncode)
        path = self.repo / ".github/pull_request_template.md"
        text = path.read_text(encoding="utf-8")
        summary = markdown_sections.section(text, "Summary")
        related = markdown_sections.section(text, "Related work")
        path.write_text(
            text.replace(summary + "\n" + related, related + "\n" + summary),
            encoding="utf-8",
        )
        result = self.run_cli("--validate-only")
        self.assertEqual(1, result.returncode)
        self.assertIn("non-standard order", result.stdout)


__all__ = ["GovernanceValidationTests"]
