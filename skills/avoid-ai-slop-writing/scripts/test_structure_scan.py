#!/usr/bin/env python3
"""Focused tests for the Markdown structure scanner."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from structure_scan import parse_blocks, structural_findings


class StructureScanTests(unittest.TestCase):
    def test_parses_boundaries_and_protects_fenced_code(self) -> None:
        blocks = parse_blocks("Intro line.\n\n```python\n# Overview\n- **Label**: code\n```\n\n# Summary\n")
        self.assertEqual([block.kind for block in blocks], ["paragraph", "blank", "fence", "fence", "fence", "fence", "blank", "heading"])
        findings = structural_findings("doc.md", "```\n# Summary\n- **Label**: code\n```")
        self.assertEqual(findings, [])

    def test_indented_code_protects_blocks(self) -> None:
        text = "    - **Bold**: not prose\n\n- **Bold**: prose"
        findings = structural_findings("doc.md", text)
        self.assertEqual([finding.line for finding in findings], [3])

    def test_parses_headings_and_lists(self) -> None:
        blocks = parse_blocks("# Summary\n\n- **Result**: details\n1. Item\n")
        self.assertEqual([(block.kind, block.line) for block in blocks if block.kind != "blank"], [("heading", 1), ("list", 3), ("list", 4)])

    def test_reports_and_avoids_bold_first_bullet(self) -> None:
        positive = structural_findings("doc.md", "- **Result**: details\n")
        self.assertTrue(any(item.reason.startswith("bold-first") for item in positive))
        negative = structural_findings("doc.md", "- Result: details\n")
        self.assertFalse(any(item.reason.startswith("bold-first") for item in negative))

    def test_reports_repeated_opening(self) -> None:
        findings = structural_findings("doc.md", "This scanner now reads files.\nThis scanner now checks headings.\nThis scanner now reports patterns.\n")
        self.assertTrue(any(item.reason == "repeated sentence opening" for item in findings))


if __name__ == "__main__":
    unittest.main()
