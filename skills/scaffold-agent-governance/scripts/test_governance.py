from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("governance.py")
sys.path.insert(0, str(SCRIPT.parent))
import agent_boundaries  # noqa: E402
import file_operations  # noqa: E402
import legacy_artifacts  # noqa: E402
import locales  # noqa: E402
import markdown_sections  # noqa: E402

SPEC = importlib.util.spec_from_file_location("governance", SCRIPT)
assert SPEC and SPEC.loader
governance = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = governance
SPEC.loader.exec_module(governance)


class GovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        (self.repo / "README.md").write_text(
            "# Demo\n\n## License\n\nMIT license text.\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(self, *extra: str) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(SCRIPT),
            "--repo",
            str(self.repo),
            "--project-name",
            "Demo",
            "--description",
            "Demo builds reliable widgets.",
            *extra,
        ]
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            command, text=True, capture_output=True, env=env, check=False
        )

    def apply(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return self.run_cli(*extra, "--apply", "--confirm-authorized")

    def translation(self, name: str, text: str) -> Path:
        path = self.base / name
        path.write_text(text, encoding="utf-8")
        return path

    def locale_args(self, locale: str = "et") -> tuple[str, ...]:
        human = self.translation(
            f"human-{locale}.md", "## Panustamine\n\nKontrollige muudatust.\n"
        )
        agent = self.translation(
            f"agent-{locale}.md", "## Agendi reeglid\n\nTöötage ainult projektiga.\n"
        )
        return (
            "--locale",
            locale,
            "--human-translation",
            f"{locale}={human}",
            "--agent-translation",
            f"{locale}={agent}",
        )

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
        (self.repo / "CONTRIBUTING.md").write_text(
            "# Local\n\n~~~md\n## Tool-assisted contributions\n~~~\n",
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

    def test_codeowners_preserves_standard_syntax_and_governs_itself(self) -> None:
        github = self.repo / ".github"
        github.mkdir()
        original = (
            "# Existing\n"
            "/src/ @org/source source@example.com # source owners\n"
            "/generated/ # ownerless reset\n"
            "docs/** @docs/team\n"
        )
        (github / "CODEOWNERS").write_text(original, encoding="utf-8")
        result = self.apply(
            "--codeowner", "governance@example.com", "--codeowner", "@org/governance"
        )
        self.assertEqual(0, result.returncode, result.stderr)
        text = (github / "CODEOWNERS").read_text(encoding="utf-8")
        self.assertTrue(text.startswith(original))
        owners = "governance@example.com @org/governance"
        self.assertIn(f"/.github/CODEOWNERS {owners}", text)
        self.assertEqual("", governance.parse_codeowners(original)["/generated/"])
        self.assertEqual(
            "@org/source source@example.com",
            governance.parse_codeowners(original)["/src/"],
        )

    def test_codeowners_conflicting_governed_reset_is_rejected(self) -> None:
        github = self.repo / ".github"
        github.mkdir()
        (github / "CODEOWNERS").write_text(
            "/AGENTS.md # explicit reset\n", encoding="utf-8"
        )
        result = self.apply("--codeowner", "@org/governance")
        self.assertEqual(2, result.returncode)
        self.assertIn("different owners already govern", result.stdout)
        self.assertFalse((self.repo / "AGENTS.md").exists())

    def test_locale_preferred_values_case_normalization_and_duplicate_validation(
        self,
    ) -> None:
        expected = {
            "en-GB-oed": "en-GB-oxendict",
            "i-klingon": "tlh",
            "art-lojban": "jbo",
            "no-bok": "nb",
            "sgn-BE-FR": "sfb",
            "zh-min-nan": "nan",
            "iw": "he",
            "in": "id",
            "ji": "yi",
            "en-Qaai-BU": "en-Zinh-MM",
            "en-DD": "en-DE",
            "en-FX": "en-FR",
            "pt-TP": "pt-TL",
            "ar-YD": "ar-YE",
            "fr-ZR": "fr-CD",
        }
        for raw, normalized in expected.items():
            with self.subTest(raw=raw):
                self.assertEqual(normalized, locales.normalize_locale_tag(raw))
        self.assertEqual(
            "x-private-demo", locales.normalize_locale_tag("X-PRIVATE-DEMO")
        )
        self.assertEqual("qaai", locales.normalize_locale_tag("Qaai"))
        self.assertEqual("bu", locales.normalize_locale_tag("BU"))
        self.assertEqual("en-x-bu-qaai", locales.normalize_locale_tag("en-X-BU-QAAI"))
        for locale in ("en-u-ca-gregory-u-nu-latn", "sl-rozaj-rozaj", "en-US-Latn"):
            with self.subTest(locale=locale), self.assertRaises(ValueError):
                locales.normalize_locale_tag(locale)
        self.assertEqual(["en", "tlh"], locales.normalize_locales(["i-klingon", "tlh"]))

    def test_new_locale_requires_paired_reviewed_translations(self) -> None:
        human = self.translation(
            "human-et.md", "## Panustamine\n\nVaadake muudatus üle.\n"
        )
        result = self.run_cli("--locale", "et", "--human-translation", f"et={human}")
        self.assertEqual(2, result.returncode)
        self.assertIn("requires both reviewed translations", result.stderr)

    def test_validate_discovers_locales_without_cli_and_requires_pair_and_links(
        self,
    ) -> None:
        self.assertEqual(0, self.apply(*self.locale_args()).returncode)
        valid = self.run_cli("--validate-only")
        self.assertEqual(0, valid.returncode, valid.stdout)
        (self.repo / "docs/i18n/et/agent-guidance.md").unlink()
        invalid = self.run_cli("--validate-only")
        self.assertEqual(1, invalid.returncode)
        self.assertIn("reviewed translation is missing", invalid.stdout)

    def test_validate_discovered_locale_requires_root_and_readme_links(self) -> None:
        self.assertEqual(0, self.apply(*self.locale_args()).returncode)
        agents = self.repo / "AGENTS.md"
        agents.write_text(
            agents.read_text().replace("docs/i18n/et/agent-guidance.md", "wrong.md"),
            encoding="utf-8",
        )
        readme = self.repo / "README.md"
        readme.write_text(
            readme.read_text().replace("docs/i18n/et/CONTRIBUTING.md", "wrong.md"),
            encoding="utf-8",
        )
        result = self.run_cli("--validate-only")
        self.assertEqual(1, result.returncode)
        self.assertIn("modified Agent rules section", result.stdout)
        self.assertIn("modified Contributing and coding agents section", result.stdout)

    def test_validate_discovered_translation_requires_exact_root_link_wrapper(
        self,
    ) -> None:
        self.assertEqual(0, self.apply(*self.locale_args()).returncode)
        path = self.repo / "docs/i18n/et/agent-guidance.md"
        path.write_text(
            path.read_text().replace("../../../AGENTS.md", "../../../OTHER.md"),
            encoding="utf-8",
        )
        result = self.run_cli("--validate-only")
        self.assertEqual(1, result.returncode)
        self.assertIn("translation has an invalid root link or locale", result.stdout)

    def test_parent_symlink_regular_file_and_leaf_collisions_preflight_without_writes(
        self,
    ) -> None:
        outside = self.base / "outside"
        outside.mkdir()
        (self.repo / ".github").symlink_to(outside, target_is_directory=True)
        result = self.apply()
        self.assertEqual(2, result.returncode)
        self.assertIn("escapes through a parent symlink", result.stderr)
        self.assertEqual([], list(outside.iterdir()))
        self.assertFalse((self.repo / "AGENTS.md").exists())

        (self.repo / ".github").unlink()
        (self.repo / ".cursor").write_text("collision\n", encoding="utf-8")
        result = self.apply()
        self.assertEqual(2, result.returncode)
        self.assertIn("parent component is not a directory", result.stderr)
        self.assertFalse((self.repo / "AGENTS.md").exists())

        (self.repo / ".cursor").unlink()
        (self.repo / "AGENTS.md").mkdir()
        result = self.apply()
        self.assertEqual(2, result.returncode)
        self.assertIn("not a regular file", result.stdout)
        self.assertFalse((self.repo / "CONTRIBUTING.md").exists())

    def test_duplicate_output_path_is_rejected_before_mutation(self) -> None:
        result = self.apply("--readme", "AGENTS.md")
        self.assertEqual(2, result.returncode)
        self.assertIn("collides with a governance output", result.stderr)
        self.assertFalse((self.repo / "AGENTS.md").exists())

    def test_transaction_rolls_back_creates_updates_and_deletes_after_validation_failure(
        self,
    ) -> None:
        update = self.repo / "README.md"
        deleted = self.repo / "legacy.txt"
        created = self.repo / "new/created.txt"
        deleted.write_text("legacy\n", encoding="utf-8")
        operations = [
            governance.Operation(update, "update", "changed\n"),
            governance.Operation(deleted, "delete"),
            governance.Operation(created, "create", "created\n"),
        ]
        errors = governance.apply_transaction(
            operations, lambda: ["forced post-apply failure"]
        )
        self.assertEqual(["forced post-apply failure"], errors)
        self.assertEqual(
            "# Demo\n\n## License\n\nMIT license text.\n", update.read_text()
        )
        self.assertEqual("legacy\n", deleted.read_text())
        self.assertFalse(created.exists())
        self.assertFalse(created.parent.exists())

    def test_transaction_rolls_back_runtime_failure_and_runs_deletions_last(
        self,
    ) -> None:
        updated = self.repo / "README.md"
        deleted = self.repo / "legacy.txt"
        created = self.repo / "created.txt"
        deleted.write_text("legacy\n", encoding="utf-8")
        operations = [
            governance.Operation(deleted, "delete"),
            governance.Operation(updated, "update", "changed\n"),
            governance.Operation(created, "create", "created\n"),
        ]
        real_write = file_operations.atomic_write
        calls = 0

        def fail_second(path: Path, content: str) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                self.assertTrue(
                    deleted.exists(),
                    "recognized deletion must be scheduled after writes",
                )
                raise OSError("forced write failure")
            real_write(path, content)

        with mock.patch.object(
            file_operations, "atomic_write", side_effect=fail_second
        ):
            with self.assertRaisesRegex(OSError, "forced write failure"):
                governance.apply_transaction(operations, lambda: [])
        self.assertIn("MIT license text.", updated.read_text())
        self.assertEqual("legacy\n", deleted.read_text())
        self.assertFalse(created.exists())

    def legacy_text(self, relative: str) -> str:
        if relative == ".github/ai-contribution-policy.yml":
            return (
                "# scaffold-agent-governance:file\n"
                "schema_version: 1\npolicy_version: 1\ncanonical_locale: en\n"
                "mode: review-required\norigin_tokens:\n  - HUMAN-AUTHORED\n  - AI-ASSISTED\n"
                "submission_actor_tokens:\n  - USER-SUBMITTED\n  - AGENT-SUBMITTED\n"
                "required_check: AI contribution policy\n"
            )
        if relative == ".github/workflows/ai-contribution-policy.yml":
            return (
                "# scaffold-agent-governance:file\nname: AI contribution policy\n"
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
                "<!-- scaffold-agent-governance:file -->\nAGENT-SUBMITTED\n"
                "## Authorization scope\nDescribe the exact authorized action.\n"
                "## Verification\n- [ ] I verified the repository.\n"
                "- [ ] I verified the request.\n"
            )
        if relative == ".cursorrules":
            return (
                "# Canonical repository instructions\n"
                "<!-- scaffold-agent-governance:file -->\n"
                "Read `AGENTS.md` before changing files. Read the nearest nested `AGENTS.md` too.\n"
                "Those files contain the canonical rules for coding agents.\n"
            )
        if relative == "llms.txt":
            return (
                "# Demo\n<!-- scaffold-agent-governance:file -->\n## Agent guidance\n"
                "Read [AGENTS.md](AGENTS.md) and "
                "[the PR template](.github/pull_request_template.md).\n"
                "The expanded index is [llms-full.txt](llms-full.txt).\n"
                "## Localized policy\nSee docs.\n"
            )
        if relative == "llms-full.txt":
            return (
                "# Demo full guidance\n<!-- scaffold-agent-governance:file -->\n"
                "## Authority and scope\nOld scope.\n"
                "## Required workflow\nOld workflow.\n"
                "## AI contribution policy\nOld policy.\n"
                "## Localized policy\nOld translations.\n"
            )
        return (
            "<!-- scaffold-agent-governance:translation:start -->\n"
            "## AI / Coding Agents\n"
            "Source policy: ai-contribution-policy.md; policy version: 1; "
            "canonical locale: en.\n"
            "AI-ASSISTED USER-SUBMITTED AGENT-SUBMITTED\n"
            "<!-- scaffold-agent-governance:translation:end -->\n"
        )

    def inline_legacy_block(self, kind: str) -> str:
        if kind == "root":
            return (
                "<!-- scaffold-agent-governance:start -->\n"
                "## AI / Coding Agents\nAI-ASSISTED USER-SUBMITTED AGENT-SUBMITTED\n"
                "<!-- scaffold-agent-governance:end -->\n"
            )
        if kind == "pr":
            return (
                "<!-- scaffold-agent-governance:pr:start -->\n"
                "## Contribution origin\nHUMAN-AUTHORED or AI-ASSISTED\n"
                "## Submission actor\nUSER-SUBMITTED or AGENT-SUBMITTED\n"
                "## Verification\n- [ ] Verified.\n"
                "<!-- scaffold-agent-governance:pr:end -->\n"
            )
        if kind == "readme":
            return (
                "<!-- scaffold-agent-governance:readme:start -->\n"
                "## AI / Coding Agents\nRead CONTRIBUTING.md, AGENTS.md, and llms.txt.\n"
                "AI-ASSISTED USER-SUBMITTED\n"
                "<!-- scaffold-agent-governance:readme:end -->\n"
            )
        if kind == "translation":
            return (
                "<!-- scaffold-agent-governance:translation:start -->\n"
                "# AI / Coding Agents (et)\nSource policy: English root policy.\n"
                "AI-ASSISTED USER-SUBMITTED\n"
                "<!-- scaffold-agent-governance:translation:end -->\n"
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
            "# scaffold-agent-governance:codeowners:start\n"
            + rules
            + "# scaffold-agent-governance:codeowners:end\n"
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
            "<!-- scaffold-agent-governance:file -->\nValuable project model index.\n",
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
            "<!-- scaffold-agent-governance:end -->",
            "Important foreign addition.\n<!-- scaffold-agent-governance:end -->",
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
            path.read_text() + "\n<!-- scaffold-agent-governance:start -->\n",
            encoding="utf-8",
        )
        result = self.run_cli()
        self.assertEqual(2, result.returncode)
        self.assertIn("unbalanced", result.stdout)

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
        originals: dict[Path, str] = {}
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


if __name__ == "__main__":
    unittest.main()
