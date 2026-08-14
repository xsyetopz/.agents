from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_cli_returns_zero_for_valid_open_format_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            (root / "SKILL.md").write_text(
                "---\nname: example\ndescription: A valid example skill.\n---\n# Example\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).with_name("validate_skill.py")),
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS:", result.stdout)

    def test_cli_returns_one_for_missing_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).with_name("validate_skill.py")),
                    directory,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing required SKILL.md", result.stdout)
