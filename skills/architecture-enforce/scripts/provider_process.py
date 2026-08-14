"""Bounded subprocess execution for architecture providers."""

from __future__ import annotations

import hashlib
import os
import signal
import subprocess
import time
from pathlib import Path

from provider_models import ProcessResult


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
