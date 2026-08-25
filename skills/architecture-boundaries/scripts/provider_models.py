#!/usr/bin/env python3
"""Data contracts shared by architecture analysis providers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# Records shared by the architecture analysis providers.
@dataclass(frozen=True)
class ToolFinding:
    rule_id: str
    severity: str
    message: str
    path: Path
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    evidence: str
    provider: str
    version: str


@dataclass(frozen=True)
class ToolResult:
    operation: str
    status: str
    provider: str
    executable: str | None
    version: str
    argv: tuple[str, ...]
    exit_code: int | None
    duration_ms: int
    findings: tuple[ToolFinding, ...] = ()
    diagnostics: tuple[str, ...] = ()
    stdout_digest: str = ""
    stderr_digest: str = ""
    payload: object | None = None

    def as_dict(self, root: Path) -> dict[str, object]:
        root = root.resolve()

        def relative(path: Path) -> str:
            try:
                return path.resolve().relative_to(root).as_posix()
            except ValueError:
                return path.as_posix()

        result: dict[str, object] = {
            "schema": "architecture-tool-result/v1",
            "operation": self.operation,
            "status": self.status,
            "provider": {
                "id": self.provider,
                "path": self.executable,
                "version": self.version,
            },
            "request": {"argv": list(self.argv)},
            "evidence": {
                "exit_code": self.exit_code,
                "duration_ms": self.duration_ms,
                "stdout_sha256": self.stdout_digest,
                "stderr_sha256": self.stderr_digest,
            },
            "findings": [
                {
                    "rule_id": finding.rule_id,
                    "severity": finding.severity,
                    "message": finding.message,
                    "path": relative(finding.path),
                    "start": {
                        "line": finding.start_line,
                        "column": finding.start_column,
                    },
                    "end": {"line": finding.end_line, "column": finding.end_column},
                    "evidence": finding.evidence,
                    "provider": finding.provider,
                    "version": finding.version,
                }
                for finding in self.findings
            ],
            "diagnostics": list(self.diagnostics),
        }
        if self.payload is not None:
            result["graph"] = self.payload
        return result


# Bounded, shell-free subprocess execution for analysis providers.
@dataclass(frozen=True)
class ProcessResult:
    status: str
    exit_code: int | None
    stdout: str
    stderr: str
    duration_ms: int
    stdout_digest: str
    stderr_digest: str
    message: str = ""


# Capability discovery for fixed, read-only architecture providers.
@dataclass(frozen=True)
class ProviderSpec:
    provider_id: str
    executables: tuple[str, ...]
    capability: str
    version_args: tuple[str, ...] = ("--version",)


PROVIDERS = (
    ProviderSpec("ast-grep", ("ast-grep", "sg"), "syntax"),
    ProviderSpec("semgrep", ("semgrep",), "syntax"),
    ProviderSpec("tree-sitter", ("tree-sitter",), "syntax"),
    ProviderSpec("clangd", ("clangd",), "symbol"),
    ProviderSpec("cargo-metadata", ("cargo",), "package_graph"),
    ProviderSpec("go-list", ("go",), "package_graph", ("version",)),
    ProviderSpec("cmake-file-api", ("cmake",), "build_graph"),
    ProviderSpec("ninja", ("ninja",), "build_graph"),
    ProviderSpec("xmake", ("xmake",), "build_graph"),
    ProviderSpec("conan", ("conan",), "package_graph"),
)
