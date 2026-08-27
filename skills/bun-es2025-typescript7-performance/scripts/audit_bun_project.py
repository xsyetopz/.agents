#!/usr/bin/env python3
"""Print read-only Bun/TypeScript performance-relevant project facts as JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return {"_error": str(error)}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: audit_bun_project.py <repository>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    package = root / "package.json"
    tsconfigs = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("tsconfig*.json")
        if "node_modules" not in path.parts and ".git" not in path.parts
    )
    locks = [
        name
        for name in (
            "bun.lock",
            "bun.lockb",
            "package-lock.json",
            "pnpm-lock.yaml",
            "yarn.lock",
        )
        if (root / name).exists()
    ]
    data = load_json(package) if package.exists() else {}
    dependencies = data.get("devDependencies", {}) if isinstance(data, dict) else {}
    result = {
        "root": str(root),
        "packageJson": package.exists(),
        "packageManager": data.get("packageManager")
        if isinstance(data, dict)
        else None,
        "engines": data.get("engines") if isinstance(data, dict) else None,
        "bunDependency": (data.get("dependencies", {}) or {}).get("bun")
        if isinstance(data, dict)
        else None,
        "typescriptDependency": dependencies.get("typescript"),
        "bunTypesDependency": dependencies.get("@types/bun"),
        "lockfiles": locks,
        "tsconfigs": tsconfigs,
        "scripts": sorted((data.get("scripts", {}) or {}).keys())
        if isinstance(data, dict)
        else [],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
