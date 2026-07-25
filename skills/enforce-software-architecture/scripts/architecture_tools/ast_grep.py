"""ast-grep provider with strict JSON and repository-bound ranges."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .capabilities import PROVIDERS, resolve_executable
from .runner import ProcessResult, run_process
from .tool_records import ToolFinding, ToolResult


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


def _finding(root: Path, raw: dict[str, Any], rule_id: str, severity: str, message: str, version: str) -> ToolFinding:
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
    return ToolFinding(rule_id, severity, message, _path(root, raw.get("file")), start_line, start_column, end_line, end_column, "syntax", "ast-grep", version)


def _result(rule_id: str, process: ProcessResult, *, status: str, executable: str | None, version: str, argv: tuple[str, ...], findings: tuple[ToolFinding, ...] = (), diagnostics: tuple[str, ...] = ()) -> ToolResult:
    return ToolResult("ast-query", status, "ast-grep", executable, version, argv, process.exit_code, process.duration_ms, findings, diagnostics, process.stdout_digest, process.stderr_digest)


def run_ast_grep(root: Path, *, rule_id: str, language: str, pattern: str, severity: str, message: str, paths: tuple[str, ...] = (), timeout_s: float = 30, executable: str | None = None) -> ToolResult:
    root = root.resolve()
    spec = next(item for item in PROVIDERS if item.provider_id == "ast-grep")
    executable = executable or resolve_executable(spec)
    targets = paths or (".",)
    invalid_targets = [target for target in targets if Path(target).is_absolute() or ".." in Path(target).parts]
    if invalid_targets:
        return ToolResult("ast-query", "invalid-output", "ast-grep", executable, "unknown", (), None, 0, diagnostics=(f"query paths must stay within repository: {', '.join(invalid_targets)}",))
    if executable is None:
        return ToolResult("ast-query", "blocked", "ast-grep", None, "unknown", (), None, 0, diagnostics=("ast-grep/sg is unavailable; install it or set ARCHITECTURE_AST_GREP",))
    version_result = run_process((executable, "--version"), root, timeout_s=3)
    version = (version_result.stdout or version_result.stderr).strip().splitlines()[0] if version_result.status == "ok" else "unknown"
    argv = (executable, "run", "--pattern", pattern, "--lang", language, "--json=stream", "--color", "never", *targets)
    process = run_process(argv, root, timeout_s)
    if process.status != "ok":
        status = "blocked" if process.status == "unavailable" else process.status
        return _result(rule_id, process, status=status, executable=executable, version=version, argv=argv, diagnostics=(process.message,))
    if process.exit_code not in (0, 1):
        diagnostic = process.stderr.strip() or f"ast-grep exited with status {process.exit_code}"
        return _result(rule_id, process, status="tool-failed", executable=executable, version=version, argv=argv, diagnostics=(diagnostic,))
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
        return _result(rule_id, process, status="invalid-output", executable=executable, version=version, argv=argv, diagnostics=(str(error),))
    return _result(rule_id, process, status="violations" if matches else "passed", executable=executable, version=version, argv=argv, findings=tuple(matches))
