"""Regression checks for the architecture-design validation gate."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

SCRIPT = Path(__file__).with_name("skill_checks.py")


class SkillChecksGateTests(unittest.TestCase):
    def test_clean_report_passes(self) -> None:
        with TemporaryDirectory() as temporary:
            report = Path(temporary) / "clean.md"
            report.write_text(
                "# Task Contract\nOBJ-1 REQ-1 QA-1 CMP-1 RISK-1\n\n# Evidence\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "report",
                    str(report),
                    "--mode",
                    "R0",
                    "--json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual(payload["errors"], [])
        self.assertEqual(payload["warnings"], [])

    def test_report_warnings_fail_closed(self) -> None:
        with TemporaryDirectory() as temporary:
            report = Path(temporary) / "warnings.md"
            report.write_text("# Task Contract\n\n# Evidence\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "report",
                    str(report),
                    "--mode",
                    "R0",
                    "--json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertEqual(len(payload["errors"]), 0)
        self.assertEqual(len(payload["warnings"]), 5)


if __name__ == "__main__":
    unittest.main()
