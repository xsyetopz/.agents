"""Shared fixtures and imports for governance test domains."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("governance.py")
sys.path.insert(0, str(SCRIPT.parent))

import agent_boundaries
import file_operations
import legacy_artifacts
import locales
import markdown_sections

SPEC = importlib.util.spec_from_file_location("governance", SCRIPT)
assert SPEC and SPEC.loader
governance = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = governance
SPEC.loader.exec_module(governance)


class GovernanceTestCase(unittest.TestCase):
    """Base fixture that provides the CLI and temporary repository helpers."""

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


__all__ = [
    "SCRIPT",
    "GovernanceTestCase",
    "agent_boundaries",
    "file_operations",
    "governance",
    "legacy_artifacts",
    "locales",
    "markdown_sections",
]
