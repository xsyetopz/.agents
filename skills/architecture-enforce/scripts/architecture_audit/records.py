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
class SyntaxRule:
    rule_id: str
    tool: str
    language: str
    pattern: str
    severity: str
    message: str
    mode: str
    paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class AnalyzerStatus:
    rule_id: str
    tool: str
    status: str
    mode: str
    message: str
    version: str = "unknown"
    command: tuple[str, ...] = ()


@dataclass(frozen=True)
class AuditReport:
    files: tuple[Path, ...]
    findings: tuple[Finding, ...]
    analyzers: tuple[AnalyzerStatus, ...] = ()


@dataclass(frozen=True)
class NamingException:
    rule: str
    path: str
    reason: str
    owner: str
    control: str
    review: str


@dataclass(frozen=True)
class ArtifactException:
    artifact_class: str
    path: str
    reason: str
    owner: str
    control: str
    review: str


@dataclass(frozen=True)
class TestSourceRoot:
    path: str
    reason: str
    owner: str
    control: str
    review: str
