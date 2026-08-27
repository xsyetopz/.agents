#!/usr/bin/env python3
"""Print read-only Cargo profile and toolchain facts as JSON."""

from __future__ import annotations

import json
import sys
from importlib import import_module
from pathlib import Path
from typing import Any, Protocol, cast


class _Tomllib(Protocol):
    TOMLDecodeError: type[ValueError]

    def loads(self, text: str, /) -> dict[str, Any]: ...


def _load_tomllib() -> _Tomllib:
    try:
        return cast(_Tomllib, import_module("tomllib"))
    except ImportError as error:
        raise RuntimeError(
            "Python 3.11+ is required: the standard-library tomllib module is unavailable."
        ) from error


def read_toml(path: Path) -> dict[str, Any]:
    tomllib = _load_tomllib()
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        return {"_error": str(error)}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: audit_cargo_perf.py <repository>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    manifest = root / "Cargo.toml"
    if not manifest.is_file():
        print(f"missing Cargo.toml: {manifest}", file=sys.stderr)
        return 2
    try:
        data = read_toml(manifest)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    toolchains = [
        name
        for name in ("rust-toolchain", "rust-toolchain.toml")
        if (root / name).exists()
    ]
    cargo_configs = [
        str(path.relative_to(root))
        for path in sorted((root / ".cargo").glob("config*"))
    ]
    result = {
        "root": str(root),
        "edition": (data.get("package", {}) or {}).get("edition"),
        "rustVersion": (data.get("package", {}) or {}).get("rust-version"),
        "workspace": data.get("workspace", {}),
        "profiles": data.get("profile", {}),
        "toolchainFiles": toolchains,
        "cargoConfigs": cargo_configs,
    }
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
