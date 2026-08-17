"""Read-only package graph providers for Cargo and Go."""

from __future__ import annotations

import json
from pathlib import Path

from provider_ast import _strict_object
from provider_capabilities import resolve_executable
from provider_models import PROVIDERS, ProcessResult, ProviderSpec, ToolResult
from provider_process import run_process


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
    return (
        (result.stdout or result.stderr).strip().splitlines()[0]
        if result.status == "ok"
        else "unknown"
    )


def _cargo_graph(stdout: str) -> dict[str, object]:
    payload = json.loads(stdout, object_pairs_hook=_strict_object)
    if (
        not isinstance(payload, dict)
        or payload.get("version") != 1
        or not isinstance(payload.get("packages"), list)
        or not isinstance(payload.get("workspace_members"), list)
    ):
        raise ValueError(
            "cargo metadata must contain version 1, packages, and workspace_members"
        )
    return {
        "kind": "package_graph",
        "packages": payload["packages"],
        "workspace_members": payload["workspace_members"],
    }


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
        if not isinstance(payload, dict) or not isinstance(
            payload.get("ImportPath"), str
        ):
            raise TypeError("go list output contains a package without ImportPath")
        packages.append(
            {
                "import_path": payload["ImportPath"],
                "imports": payload.get("Imports", []),
                "deps": payload.get("Deps", []),
            }
        )
        offset = end
    return {"kind": "package_graph", "packages": packages}


def run_graph(root: Path, *, tool: str = "auto", timeout_s: float = 30) -> ToolResult:
    root = root.resolve()
    if tool == "auto":
        tool = (
            "cargo-metadata"
            if (root / "Cargo.toml").exists()
            else "go-list"
            if (root / "go.mod").exists()
            else "cargo-metadata"
        )
    spec = _provider(tool)
    if spec is None:
        return ToolResult(
            "package-graph",
            "blocked",
            tool,
            None,
            "unknown",
            (),
            None,
            0,
            diagnostics=(f"unsupported package graph provider: {tool}",),
        )
    executable = resolve_executable(spec)
    if executable is None:
        return ToolResult(
            "package-graph",
            "blocked",
            tool,
            None,
            "unknown",
            (),
            None,
            0,
            diagnostics=(f"provider executable is unavailable: {tool}",),
        )
    version = _version(executable, root, spec.version_args)
    argv = (
        (executable, "metadata", "--format-version=1", "--no-deps")
        if tool == "cargo-metadata"
        else (executable, "list", "-json", "./...")
    )
    process = run_process(argv, root, timeout_s)
    if process.status != "ok":
        status = "blocked" if process.status == "unavailable" else process.status
        return _graph_result(
            tool, process, status, executable, version, argv, (process.message,)
        )
    if process.exit_code != 0:
        return _graph_result(
            tool,
            process,
            "tool-failed",
            executable,
            version,
            argv,
            (
                process.stderr.strip()
                or f"provider exited with status {process.exit_code}",
            ),
        )
    try:
        payload = (
            _cargo_graph(process.stdout)
            if tool == "cargo-metadata"
            else _go_graph(process.stdout)
        )
    except (json.JSONDecodeError, ValueError, TypeError) as error:
        return _graph_result(
            tool, process, "invalid-output", executable, version, argv, (str(error),)
        )
    return _graph_result(
        tool, process, "passed", executable, version, argv, payload=payload
    )
