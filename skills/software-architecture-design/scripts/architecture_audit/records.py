#!/usr/bin/env python3
"""Data records returned by the architecture audit."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: Path
    message: str
    evidence: str = "policy"


@dataclass(frozen=True)
class AuditReport:
    files: tuple[Path, ...]
    findings: tuple[Finding, ...]
