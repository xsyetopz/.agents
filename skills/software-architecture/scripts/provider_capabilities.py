"""Capability discovery for fixed, read-only architecture providers."""

from __future__ import annotations

import os
import shutil
from collections.abc import Mapping
from pathlib import Path

from provider_models import PROVIDERS, ProviderSpec
from provider_process import run_process


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


def resolve_executable(
    spec: ProviderSpec, environment: Mapping[str, str] | None = None
) -> str | None:
    environment = environment or os.environ
    override = environment.get(_env_name(spec.provider_id))
    if override:
        return override if Path(override).is_file() else shutil.which(override)
    return next(
        (candidate for name in spec.executables if (candidate := shutil.which(name))),
        None,
    )


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
            version = (
                _clean_version((result.stdout or result.stderr).strip().splitlines()[0])
                if result.status == "ok"
                else "unknown"
            )
            item["status"] = "ready" if result.status == "ok" else result.status
            item["version"] = version
            if result.message:
                item["diagnostic"] = result.message
        report.append(item)
    return report
