"""Shared fixtures for architecture-audit regression modules."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import audit_architecture


class AuditFixture:
    """Reusable filesystem and CLI helpers without inherited test methods."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, lines: int = 1, content: str | None = None) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if content is not None else "x\n" * lines, encoding="utf-8")
        return path

    def findings(self, **kwargs: object) -> list[audit_architecture.Finding]:
        return audit_architecture.audit(self.root, **kwargs)[1]

    @staticmethod
    def codes(findings: list[audit_architecture.Finding]) -> set[str]:
        return {finding.code for finding in findings}

    def inline_findings(self, relative: str, content: str) -> list[audit_architecture.Finding]:
        path = self.write(relative, content=content)
        return audit_architecture.inline_test_findings(path, self.root)

    def run_cli(self, *arguments: str, root: Path | None = None) -> subprocess.CompletedProcess[str]:
        script = Path(audit_architecture.__file__)
        target = root or self.root
        return subprocess.run(
            [sys.executable, str(script), str(target), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    @staticmethod
    def json_output(result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
        return json.loads(result.stdout)
