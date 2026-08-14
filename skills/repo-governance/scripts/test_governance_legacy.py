"""Legacy governance artifact detection and cleanup tests."""

from __future__ import annotations

import json

from test_governance_support import GovernanceTestCase, governance, legacy_artifacts


class GovernanceLegacyTests(GovernanceTestCase):
    def legacy_text(self, relative: str) -> str:
        if relative == ".github/ai-contribution-policy.yml":
            return (
                "# repo-governance:file\n"
                "schema_version: 1\npolicy_version: 1\ncanonical_locale: en\n"
                "mode: review-required\norigin_tokens:\n  - HUMAN-AUTHORED\n  - AI-ASSISTED\n"
                "submission_actor_tokens:\n  - USER-SUBMITTED\n  - AGENT-SUBMITTED\n"
                "required_check: AI contribution policy\n"
            )
        if relative == ".github/workflows/ai-contribution-policy.yml":
            return (
                "# repo-governance:file\nname: AI contribution policy\n"
                "on:\n  pull_request_target:\n    types: [opened, edited, labeled]\n"
                "permissions:\n  contents: read\n  pull-requests: read\n"
                "env:\n  PR_TITLE: ${{ github.event.pull_request.title }}\n"
                "  PR_BODY: ${{ github.event.pull_request.body }}\n"
                "  PR_LABELS_JSON: ${{ toJSON(github.event.pull_request.labels) }}\n"
                "# AI-ASSISTED USER-SUBMITTED AGENT-SUBMITTED\n"
            )
        if relative == ".github/ISSUE_TEMPLATE/agent-submitted.md":
            return (
                "---\nname: Agent-submitted issue\nabout: Work submitted by an agent\n---\n"
                "<!-- repo-governance:file -->\nAGENT-SUBMITTED\n"
                "## Authorization scope\nDescribe the exact authorized action.\n"
                "## Verification\n- [ ] I verified the repository.\n"
                "- [ ] I verified the request.\n"
            )
        if relative == ".cursorrules":
            return (
                "# Canonical repository instructions\n"
                "<!-- repo-governance:file -->\nRead `AGENTS.md` before changing files. Read the nearest nested `AGENTS.md` too.\n"
                "Those files contain the canonical rules for coding agents.\n"
            )
        if relative == "llms.txt":
            return (
                "# Demo\n<!-- repo-governance:file -->\n## Agent guidance\n"
                "Read [AGENTS.md](AGENTS.md) and "
                "[the PR template](.github/pull_request_template.md).\n"
                "The expanded index is [llms-full.txt](llms-full.txt).\n"
                "## Localized policy\nSee docs.\n"
            )
        if relative == "llms-full.txt":
            return (
                "# Demo full guidance\n<!-- repo-governance:file -->\n"
                "## Authority and scope\nOld scope.\n"
                "## Required workflow\nOld workflow.\n"
                "## AI contribution policy\nOld policy.\n"
                "## Localized policy\nOld translations.\n"
            )
        return (
            "<!-- repo-governance:translation:start -->\n"
            "## AI / Coding Agents\n"
            "Source policy: ai-contribution-policy.md; policy version: 1; "
            "canonical locale: en.\n"
            "AI-ASSISTED USER-SUBMITTED AGENT-SUBMITTED\n"
            "<!-- repo-governance:translation:end -->\n"
        )

    def inline_legacy_block(self, kind: str) -> str:
        if kind == "root":
            return (
                "<!-- repo-governance:start -->\n"
                "## AI / Coding Agents\nAI-ASSISTED USER-SUBMITTED AGENT-SUBMITTED\n"
                "<!-- repo-governance:end -->\n"
            )
        if kind == "pr":
            return (
                "<!-- repo-governance:pr:start -->\n"
                "## Contribution origin\nHUMAN-AUTHORED or AI-ASSISTED\n"
                "## Submission actor\nUSER-SUBMITTED or AGENT-SUBMITTED\n"
                "## Verification\n- [ ] Verified.\n"
                "<!-- repo-governance:pr:end -->\n"
            )
        if kind == "readme":
            return (
                "<!-- repo-governance:readme:start -->\n"
                "## AI / Coding Agents\nRead CONTRIBUTING.md, AGENTS.md, and llms.txt.\n"
                "AI-ASSISTED USER-SUBMITTED\n"
                "<!-- repo-governance:readme:end -->\n"
            )
        if kind == "translation":
            return (
                "<!-- repo-governance:translation:start -->\n"
                "# AI / Coding Agents (et)\nSource policy: English root policy.\n"
                "AI-ASSISTED USER-SUBMITTED\n"
                "<!-- repo-governance:translation:end -->\n"
            )
        paths = (
            "/AGENTS.md",
            "/CLAUDE.md",
            "/GEMINI.md",
            "/.cursor/rules/agents.mdc",
            "/llms.txt",
            "/llms-full.txt",
            "/.github/ai-contribution-policy.yml",
            "/.github/pull_request_template.md",
            "/.github/workflows/ai-contribution-policy.yml",
        )
        rules = "".join(f"{path} @old/governance\n" for path in paths)
        return (
            "# repo-governance:codeowners:start\n"
            + rules
            + "# repo-governance:codeowners:end\n"
        )

    def test_only_full_path_specific_legacy_signatures_are_deleted(self) -> None:
        paths = [*governance.LEGACY_PATHS, "docs/ai-contribution-policy.et.md"]
        for relative in paths:
            path = self.repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.legacy_text(relative), encoding="utf-8")
        preview = self.run_cli()
        self.assertEqual(0, preview.returncode, preview.stderr)
        deletions = {
            item["path"]
            for item in json.loads(preview.stdout)["operations"]
            if item["action"] == "delete"
        }
        self.assertEqual(set(paths), deletions)
        applied = self.apply()
        self.assertEqual(0, applied.returncode, applied.stderr)
        for relative in paths:
            self.assertFalse((self.repo / relative).exists())

    def test_incomplete_legacy_signatures_are_preserved(self) -> None:
        missing_fact = {
            ".github/ai-contribution-policy.yml": "schema_version: 1\n",
            ".github/workflows/ai-contribution-policy.yml": (
                "  PR_BODY: ${{ github.event.pull_request.body }}\n"
            ),
            ".github/ISSUE_TEMPLATE/agent-submitted.md": "## Authorization scope\n",
            ".cursorrules": "nearest nested ",
            "llms.txt": "## Localized policy\n",
            "llms-full.txt": "## Required workflow\n",
            "docs/ai-contribution-policy.et.md": "Source policy:",
        }
        for relative, missing in missing_fact.items():
            with self.subTest(relative=relative):
                path = self.repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    self.legacy_text(relative).replace(missing, "", 1),
                    encoding="utf-8",
                )
                self.assertFalse(legacy_artifacts.recognized_legacy(path, self.repo))
                path.unlink()

    def test_marker_only_and_foreign_legacy_named_files_are_preserved_and_do_not_block(
        self,
    ) -> None:
        marker_only = self.repo / "llms.txt"
        marker_only.write_text(
            "<!-- repo-governance:file -->\nValuable project model index.\n",
            encoding="utf-8",
        )
        cursorrules = self.repo / ".cursorrules"
        cursorrules.write_text("Foreign Cursor instructions.\n", encoding="utf-8")
        notes = self.repo / "notes.md"
        notes.write_text("Historical term: USER-SUBMITTED.\n", encoding="utf-8")
        result = self.apply()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Valuable project model index.", marker_only.read_text())
        self.assertEqual("Foreign Cursor instructions.\n", cursorrules.read_text())
        self.assertEqual("Historical term: USER-SUBMITTED.\n", notes.read_text())
        self.assertEqual(0, self.run_cli("--validate-only").returncode)

    def test_each_actual_inline_legacy_block_requires_its_full_body_signature(
        self,
    ) -> None:
        missing_fact = {
            "root": "USER-SUBMITTED ",
            "pr": "## Submission actor",
            "readme": "CONTRIBUTING.md",
            "translation": "Source policy:",
            "codeowners": "/.github/workflows/ai-contribution-policy.yml",
        }
        for kind, missing in missing_fact.items():
            with self.subTest(kind=kind):
                block = self.inline_legacy_block(kind)
                cleaned = legacy_artifacts.strip_legacy_blocks(
                    "Before.\n\n" + block + "\nAfter.\n"
                )
                self.assertEqual("Before.\n\n\nAfter.\n", cleaned)
                incomplete = block.replace(missing, "", 1)
                with self.assertRaisesRegex(ValueError, "incomplete body"):
                    legacy_artifacts.strip_legacy_blocks(incomplete)
                addition = block.replace(
                    next(
                        end
                        for start, end in legacy_artifacts.LEGACY_BLOCKS
                        if start in block
                    ),
                    "Important foreign addition.\n"
                    + next(
                        end
                        for start, end in legacy_artifacts.LEGACY_BLOCKS
                        if start in block
                    ),
                    1,
                )
                with self.assertRaisesRegex(ValueError, "incomplete body"):
                    legacy_artifacts.strip_legacy_blocks(addition)

    def test_foreign_addition_in_root_legacy_block_conflicts_without_writes(
        self,
    ) -> None:
        path = self.repo / "AGENTS.md"
        block = self.inline_legacy_block("root").replace(
            "<!-- repo-governance:end -->",
            "Important foreign addition.\n<!-- repo-governance:end -->",
        )
        original = "# Local agents\n\n" + block + "\nKeep this file.\n"
        path.write_text(original, encoding="utf-8")
        readme_before = (self.repo / "README.md").read_bytes()
        result = self.apply()
        self.assertEqual(2, result.returncode)
        self.assertIn("unrecognized or incomplete body", result.stdout)
        self.assertEqual(original, path.read_text(encoding="utf-8"))
        self.assertEqual(readme_before, (self.repo / "README.md").read_bytes())
        self.assertFalse((self.repo / "CONTRIBUTING.md").exists())

    def test_fenced_legacy_block_example_is_preserved_and_does_not_block_apply(
        self,
    ) -> None:
        example = self.inline_legacy_block("root")
        (self.repo / "AGENTS.md").write_text(
            "# Local agents\n\n```markdown\n" + example + "```\n\nKeep this example.\n",
            encoding="utf-8",
        )
        result = self.apply()
        self.assertEqual(0, result.returncode, result.stderr)
        text = (self.repo / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn(example, text)
        self.assertIn("Keep this example.", text)

    def test_balanced_inline_legacy_blocks_are_removed_but_unbalanced_blocks_conflict(
        self,
    ) -> None:
        (self.repo / "AGENTS.md").write_text(
            "# Local\n\n" + self.inline_legacy_block("root") + "\nKeep me.\n",
            encoding="utf-8",
        )
        result = self.apply()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Keep me.", (self.repo / "AGENTS.md").read_text())
        self.assertNotIn(
            governance.LEGACY_MARKER, (self.repo / "AGENTS.md").read_text()
        )

        path = self.repo / "CONTRIBUTING.md"
        path.write_text(
            path.read_text() + "\n<!-- repo-governance:start -->\n",
            encoding="utf-8",
        )
        result = self.run_cli()
        self.assertEqual(2, result.returncode)
        self.assertIn("unbalanced", result.stdout)


__all__ = ["GovernanceLegacyTests"]
