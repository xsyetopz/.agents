#!/usr/bin/env python3
"""Run fixed, read-only architecture analysis providers."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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
            "provider": {"id": self.provider, "path": self.executable, "version": self.version},
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
                    "start": {"line": finding.start_line, "column": finding.start_column},
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


def _digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run_process(
    argv: tuple[str, ...],
    root: Path,
    timeout_s: float,
    max_output_bytes: int = 4 * 1024 * 1024,
) -> ProcessResult:
    started = time.monotonic()
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "NO_COLOR": "1"})
    try:
        process = subprocess.Popen(
            argv,
            cwd=root,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            start_new_session=True,
        )
    except FileNotFoundError:
        return ProcessResult("unavailable", None, "", "", 0, "", "", f"executable not found: {argv[0]}")
    except OSError as error:
        return ProcessResult("tool-failed", None, "", "", 0, "", "", f"could not launch {argv[0]}: {error}")
    try:
        stdout_bytes, stderr_bytes = process.communicate(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except OSError:
            process.kill()
        stdout_bytes, stderr_bytes = process.communicate()
        duration = int((time.monotonic() - started) * 1000)
        return ProcessResult(
            "timeout",
            None,
            stdout_bytes.decode("utf-8", "replace"),
            stderr_bytes.decode("utf-8", "replace"),
            duration,
            _digest(stdout_bytes),
            _digest(stderr_bytes),
            f"provider exceeded {timeout_s:g}s timeout",
        )
    duration = int((time.monotonic() - started) * 1000)
    if len(stdout_bytes) + len(stderr_bytes) > max_output_bytes:
        return ProcessResult(
            "tool-failed",
            process.returncode,
            "",
            "",
            duration,
            _digest(stdout_bytes),
            _digest(stderr_bytes),
            f"provider output exceeded {max_output_bytes} bytes",
        )
    return ProcessResult(
        "ok",
        process.returncode,
        stdout_bytes.decode("utf-8", "replace"),
        stderr_bytes.decode("utf-8", "replace"),
        duration,
        _digest(stdout_bytes),
        _digest(stderr_bytes),
    )


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


def _env_name(provider_id: str) -> str:
    return "ARCHITECTURE_" + provider_id.upper().replace("-", "_")


def _clean_version(value: str) -> str:
    output: list[str] = []
    escape = False
    for character in value:
        if escape:
            if character.isalpha():
                escape = False
            continue
        if character == "\x1b":
            escape = True
            continue
        output.append(character)
    return "".join(output)


def resolve_executable(spec: ProviderSpec, environment: dict[str, str] | None = None) -> str | None:
    environment = environment or os.environ
    override = environment.get(_env_name(spec.provider_id))
    if override:
        return override if Path(override).is_file() else shutil.which(override)
    return next((candidate for name in spec.executables if (candidate := shutil.which(name))), None)


def capability_report(root: Path) -> list[dict[str, object]]:
    report: list[dict[str, object]] = []
    for spec in PROVIDERS:
        executable = resolve_executable(spec)
        item: dict[str, object] = {
            "id": spec.provider_id,
            "capability": spec.capability,
            "available": executable is not None,
            "path": executable,
        }
        if executable is None:
            item["status"] = "unavailable"
            item["diagnostic"] = f"none of {', '.join(spec.executables)} is on PATH"
        else:
            result = run_process((executable, *spec.version_args), root, timeout_s=3)
            version = _clean_version((result.stdout or result.stderr).strip().splitlines()[0]) if result.status == "ok" else "unknown"
            item["status"] = "ready" if result.status == "ok" else result.status
            item["version"] = version
            if result.message:
                item["diagnostic"] = result.message
        report.append(item)
    return report


# ast-grep provider with strict JSON and repository-bound ranges.
def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def _path(root: Path, value: object) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("match file must be a non-empty string")
    candidate = (root / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"match path escapes repository: {value}") from error
    return candidate


def _finding(
    root: Path,
    raw: dict[str, Any],
    rule_id: str,
    severity: str,
    message: str,
    version: str,
) -> ToolFinding:
    span = raw.get("range")
    if not isinstance(span, dict):
        raise TypeError("match range must be an object")
    start, end = span.get("start"), span.get("end")
    if not isinstance(start, dict) or not isinstance(end, dict):
        raise TypeError("match range start/end must be objects")
    start_line = _integer(start.get("line"), "start line") + 1
    start_column = _integer(start.get("column"), "start column") + 1
    end_line = _integer(end.get("line"), "end line") + 1
    end_column = _integer(end.get("column"), "end column") + 1
    if (end_line, end_column) < (start_line, start_column):
        raise ValueError("match range end precedes start")
    return ToolFinding(
        rule_id,
        severity,
        message,
        _path(root, raw.get("file")),
        start_line,
        start_column,
        end_line,
        end_column,
        "syntax",
        "ast-grep",
        version,
    )


def _ast_result(
    process: ProcessResult,
    *,
    status: str,
    executable: str | None,
    version: str,
    argv: tuple[str, ...],
    findings: tuple[ToolFinding, ...] = (),
    diagnostics: tuple[str, ...] = (),
) -> ToolResult:
    return ToolResult(
        "ast-query",
        status,
        "ast-grep",
        executable,
        version,
        argv,
        process.exit_code,
        process.duration_ms,
        findings,
        diagnostics,
        process.stdout_digest,
        process.stderr_digest,
    )


def run_ast_grep(
    root: Path,
    *,
    rule_id: str,
    language: str,
    pattern: str,
    severity: str,
    message: str,
    paths: tuple[str, ...] = (),
    timeout_s: float = 30,
    executable: str | None = None,
) -> ToolResult:
    root = root.resolve()
    spec = next(item for item in PROVIDERS if item.provider_id == "ast-grep")
    executable = executable or resolve_executable(spec)
    targets = paths or (".",)
    invalid_targets = [target for target in targets if Path(target).is_absolute() or ".." in Path(target).parts]
    if invalid_targets:
        return ToolResult(
            "ast-query",
            "invalid-output",
            "ast-grep",
            executable,
            "unknown",
            (),
            None,
            0,
            diagnostics=(f"query paths must stay within repository: {', '.join(invalid_targets)}",),
        )
    if executable is None:
        return ToolResult(
            "ast-query",
            "blocked",
            "ast-grep",
            None,
            "unknown",
            (),
            None,
            0,
            diagnostics=("ast-grep/sg is unavailable; install it or set ARCHITECTURE_AST_GREP",),
        )
    version_result = run_process((executable, "--version"), root, timeout_s=3)
    version = (version_result.stdout or version_result.stderr).strip().splitlines()[0] if version_result.status == "ok" else "unknown"
    argv = (
        executable,
        "run",
        "--pattern",
        pattern,
        "--lang",
        language,
        "--json=stream",
        "--color",
        "never",
        *targets,
    )
    process = run_process(argv, root, timeout_s)
    if process.status != "ok":
        status = "blocked" if process.status == "unavailable" else process.status
        return _ast_result(
            process,
            status=status,
            executable=executable,
            version=version,
            argv=argv,
            diagnostics=(process.message,),
        )
    if process.exit_code not in (0, 1):
        diagnostic = process.stderr.strip() or f"ast-grep exited with status {process.exit_code}"
        return _ast_result(
            process,
            status="tool-failed",
            executable=executable,
            version=version,
            argv=argv,
            diagnostics=(diagnostic,),
        )
    matches: list[ToolFinding] = []
    try:
        for line_number, line in enumerate(process.stdout.splitlines(), start=1):
            if not line.strip():
                continue
            raw = json.loads(line, object_pairs_hook=_strict_object)
            if not isinstance(raw, dict):
                raise TypeError(f"line {line_number}: match must be an object")
            matches.append(_finding(root, raw, rule_id, severity, message, version))
    except (json.JSONDecodeError, ValueError, TypeError) as error:
        return _ast_result(
            process,
            status="invalid-output",
            executable=executable,
            version=version,
            argv=argv,
            diagnostics=(str(error),),
        )
    return _ast_result(
        process,
        status="violations" if matches else "passed",
        executable=executable,
        version=version,
        argv=argv,
        findings=tuple(matches),
    )


# Read-only package graph providers for Cargo and Go.
def _provider(tool: str) -> ProviderSpec | None:
    return next((item for item in PROVIDERS if item.provider_id == tool), None)


def _graph_result(
    tool: str,
    process: ProcessResult,
    status: str,
    executable: str | None,
    version: str,
    argv: tuple[str, ...],
    diagnostics: tuple[str, ...] = (),
    payload: object | None = None,
) -> ToolResult:
    return ToolResult(
        "package-graph",
        status,
        tool,
        executable,
        version,
        argv,
        process.exit_code,
        process.duration_ms,
        diagnostics=diagnostics,
        stdout_digest=process.stdout_digest,
        stderr_digest=process.stderr_digest,
        payload=payload,
    )


def _version(executable: str, root: Path, args: tuple[str, ...]) -> str:
    result = run_process((executable, *args), root, timeout_s=3)
    return (result.stdout or result.stderr).strip().splitlines()[0] if result.status == "ok" else "unknown"


def _cargo_graph(stdout: str) -> dict[str, object]:
    payload = json.loads(stdout, object_pairs_hook=_strict_object)
    if (
        not isinstance(payload, dict)
        or payload.get("version") != 1
        or not isinstance(payload.get("packages"), list)
        or not isinstance(payload.get("workspace_members"), list)
    ):
        raise ValueError("cargo metadata must contain version 1, packages, and workspace_members")
    return {"kind": "package_graph", "packages": payload["packages"], "workspace_members": payload["workspace_members"]}


def _go_graph(stdout: str) -> dict[str, object]:
    decoder = json.JSONDecoder(object_pairs_hook=_strict_object)
    packages: list[dict[str, object]] = []
    offset = 0
    while offset < len(stdout):
        while offset < len(stdout) and stdout[offset].isspace():
            offset += 1
        if offset == len(stdout):
            break
        payload, end = decoder.raw_decode(stdout, offset)
        if not isinstance(payload, dict) or not isinstance(payload.get("ImportPath"), str):
            raise TypeError("go list output contains a package without ImportPath")
        packages.append({"import_path": payload["ImportPath"], "imports": payload.get("Imports", []), "deps": payload.get("Deps", [])})
        offset = end
    return {"kind": "package_graph", "packages": packages}


def run_graph(root: Path, *, tool: str = "auto", timeout_s: float = 30) -> ToolResult:
    root = root.resolve()
    if tool == "auto":
        tool = "cargo-metadata" if (root / "Cargo.toml").exists() else "go-list" if (root / "go.mod").exists() else "cargo-metadata"
    spec = _provider(tool)
    if spec is None:
        return ToolResult("package-graph", "blocked", tool, None, "unknown", (), None, 0, diagnostics=(f"unsupported package graph provider: {tool}",))
    executable = resolve_executable(spec)
    if executable is None:
        return ToolResult("package-graph", "blocked", tool, None, "unknown", (), None, 0, diagnostics=(f"provider executable is unavailable: {tool}",))
    version = _version(executable, root, spec.version_args)
    argv = (executable, "metadata", "--format-version=1", "--no-deps") if tool == "cargo-metadata" else (executable, "list", "-json", "./...")
    process = run_process(argv, root, timeout_s)
    if process.status != "ok":
        status = "blocked" if process.status == "unavailable" else process.status
        return _graph_result(tool, process, status, executable, version, argv, (process.message,))
    if process.exit_code != 0:
        return _graph_result(tool, process, "tool-failed", executable, version, argv, (process.stderr.strip() or f"provider exited with status {process.exit_code}",))
    try:
        payload = _cargo_graph(process.stdout) if tool == "cargo-metadata" else _go_graph(process.stdout)
    except (json.JSONDecodeError, ValueError, TypeError) as error:
        return _graph_result(tool, process, "invalid-output", executable, version, argv, (str(error),))
    return _graph_result(tool, process, "passed", executable, version, argv, payload=payload)


# CLI for capability discovery and read-only syntax queries.
def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run fixed, read-only architecture analyzers.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    capabilities = subparsers.add_parser("capabilities", help="show available providers")
    capabilities.add_argument("--root", default=".")
    capabilities.add_argument("--format", choices=("json", "text"), default="text")
    query = subparsers.add_parser("ast-query", help="run one ast-grep structural query")
    query.add_argument("--root", default=".")
    query.add_argument("--tool", choices=("ast-grep",), default="ast-grep")
    query.add_argument("--language", required=True)
    query.add_argument("--pattern", required=True)
    query.add_argument("--rule-id", default="ad-hoc-ast-query")
    query.add_argument("--severity", choices=("error", "warning", "notice"), default="warning")
    query.add_argument("--message", default="syntax query matched")
    query.add_argument("--timeout", type=float, default=30)
    query.add_argument("--format", choices=("json", "text"), default="text")
    query.add_argument("paths", nargs="*", default=["."])
    graph = subparsers.add_parser("graph", help="read a package graph from Cargo or Go")
    graph.add_argument("--root", default=".")
    graph.add_argument("--tool", choices=("auto", "cargo-metadata", "go-list"), default="auto")
    graph.add_argument("--timeout", type=float, default=30)
    graph.add_argument("--format", choices=("json", "text"), default="text")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "capabilities":
        report = capability_report(Path(args.root))
        if args.format == "json":
            print(json.dumps({"schema": "architecture-capabilities/v1", "providers": report}, indent=2, sort_keys=True))
        else:
            for item in report:
                suffix = f" ({item.get('version', 'unknown')})" if item.get("version") else ""
                print(f"{item['id']}: {item['status']}{suffix} - {item.get('diagnostic', item.get('path', ''))}")
        return 0
    if args.command == "graph":
        result = run_graph(Path(args.root), tool=args.tool, timeout_s=args.timeout)
        payload = result.as_dict(Path(args.root))
        if args.format == "json":
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(f"{result.provider}: {result.status}")
            if result.payload is not None:
                print(json.dumps(result.payload, indent=2, sort_keys=True))
            for diagnostic in result.diagnostics:
                print(f"diagnostic: {diagnostic}")
        return {"passed": 0, "blocked": 3, "tool-failed": 4, "timeout": 5, "invalid-output": 6}.get(result.status, 4)
    result = run_ast_grep(
        Path(args.root),
        rule_id=args.rule_id,
        language=args.language,
        pattern=args.pattern,
        severity=args.severity,
        message=args.message,
        paths=tuple(args.paths),
        timeout_s=args.timeout,
    )
    payload = result.as_dict(Path(args.root))
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"{result.provider}: {result.status} ({len(result.findings)} findings)")
        for finding in result.findings:
            print(f"{finding.path}:{finding.start_line}:{finding.start_column}: {finding.severity}: {finding.message}")
        for diagnostic in result.diagnostics:
            print(f"diagnostic: {diagnostic}")
    return {"passed": 0, "violations": 1, "blocked": 3, "tool-failed": 4, "timeout": 5, "invalid-output": 6}.get(result.status, 4)


__all__ = ["ToolFinding", "ToolResult", "capability_report", "run_ast_grep", "run_graph"]


if __name__ == "__main__":
    raise SystemExit(main())
