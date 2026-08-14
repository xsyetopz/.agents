"""Locale, translation, and CODEOWNERS governance tests."""

from __future__ import annotations

from test_governance_support import GovernanceTestCase, governance, locales


class GovernanceLocaleTests(GovernanceTestCase):
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
        for locale in (
            "en-u-ca-gregory-u-nu-latn",
            "sl-rozaj-rozaj",
            "en-US-Latn",
        ):
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


__all__ = ["GovernanceLocaleTests"]
