#!/usr/bin/env python3
"""Audit a repository for the Bun 1.4 package-management baseline."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

OLD_LOCKFILES = (
    "bun.lockb",
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pnpm-lock.yaml",
    "yarn.lock",
)
FOREIGN_COMMAND = re.compile(
    r"(?<![A-Za-z0-9_-])(?:npm|npx|pnpm|pnpx|yarn)(?![A-Za-z0-9_-])"
)
OLD_BUN = re.compile(
    r"(?:\bbun(?:-version)?\s*[:=@]?\s*[\"']?1\.[0-3](?:\.\d+)?\b|"
    r"oven/bun:1\.[0-3](?:\.\d+)?\b)",
    re.IGNORECASE,
)
BUN_MANAGER = re.compile(r"^bun@(\d+)\.(\d+)(?:\.(\d+))?(?:[-+].*)?$")
TEXT_SUFFIXES = {
    ".bash",
    ".cjs",
    ".js",
    ".json",
    ".jsonc",
    ".mjs",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".yaml",
    ".yml",
    ".zsh",
}
IGNORED_DIRS = {
    ".git",
    ".next",
    ".turbo",
    "build",
    "coverage",
    "dist",
    "fixtures",
    "node_modules",
    "vendor",
}


def bun_version() -> str:
    try:
        result = subprocess.run(
            ["bun", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("bun --version failed") from exc
    return result.stdout.strip()


def version_at_least_14(raw: str) -> bool:
    match = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?", raw)
    return bool(match and (int(match[1]), int(match[2])) >= (1, 4))


def is_ignored(path: Path, root: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.relative_to(root).parts)


def active_files(root: Path) -> list[Path]:
    seeds = [
        root / ".github",
        root / ".gitlab-ci.yml",
        root / ".circleci",
        root / ".azure-pipelines",
        root / "azure-pipelines.yml",
        root / "bitbucket-pipelines.yml",
        root / ".devcontainer",
        root / ".husky",
        root / "deploy",
        root / "deployment",
        root / "infrastructure",
        root / "k8s",
        root / "helm",
        root / "scripts",
        root / "bin",
        root / "bunfig.toml",
        root / "mise.toml",
        root / ".tool-versions",
        root / "Makefile",
        root / "Taskfile.yml",
        root / "justfile",
        root / "lefthook.yml",
        root / "turbo.json",
        root / "nx.json",
        root / "fly.toml",
        root / "netlify.toml",
        root / "render.yaml",
        root / "railway.json",
        root / "serverless.yml",
        root / "vercel.json",
        root / "wrangler.toml",
        root / "Procfile",
    ]
    for pattern in (
        "Dockerfile*",
        "compose*.yaml",
        "compose*.yml",
        "docker-compose*.yaml",
        "docker-compose*.yml",
    ):
        seeds.extend(root.glob(pattern))
    found: set[Path] = set()
    for seed in seeds:
        if seed.is_file():
            found.add(seed)
            continue
        if not seed.is_dir():
            continue
        for path in seed.rglob("*"):
            if is_ignored(path, root) or not path.is_file():
                continue
            if path.suffix.lower() in TEXT_SUFFIXES or path.name.startswith(
                "Dockerfile"
            ):
                found.add(path)
    return sorted(found)


def read_package(path: Path, errors: list[str], root: Path) -> dict[str, object]:
    label = path.relative_to(root)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label} cannot be read: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{label} must contain an object")
        return {}
    return value


def workspace_patterns(package: dict[str, object]) -> list[str]:
    value = package.get("workspaces", [])
    if isinstance(value, dict):
        value = value.get("packages", [])
    if not isinstance(value, list):
        return []
    return [
        item for item in value if isinstance(item, str) and not item.startswith("!")
    ]


def package_files(root: Path, package: dict[str, object]) -> list[Path]:
    paths = {root / "package.json"}
    for pattern in workspace_patterns(package):
        if Path(pattern).is_absolute() or ".." in Path(pattern).parts:
            continue
        for match in root.glob(pattern):
            candidate = match / "package.json" if match.is_dir() else match
            if (
                candidate.name == "package.json"
                and candidate.is_file()
                and not is_ignored(candidate, root)
            ):
                paths.add(candidate)
    return sorted(paths)


def check_package(
    path: Path,
    package: dict[str, object],
    errors: list[str],
    root: Path,
) -> None:
    label = path.relative_to(root)
    manager = package.get("packageManager")
    if isinstance(manager, str):
        match = BUN_MANAGER.fullmatch(manager)
        if not match:
            errors.append(
                f"{label} packageManager is not a valid Bun version: {manager}"
            )
        elif (int(match[1]), int(match[2])) < (1, 4):
            errors.append(f"{label} packageManager is below Bun 1.4: {manager}")
    scripts = package.get("scripts", {})
    if isinstance(scripts, dict):
        for name, command in scripts.items():
            if isinstance(command, str) and FOREIGN_COMMAND.search(command):
                errors.append(
                    f"{label} script {name!r} invokes a foreign package manager"
                )


def audit(root: Path) -> tuple[list[str], str]:
    errors: list[str] = []
    try:
        version = bun_version()
    except RuntimeError as exc:
        return [str(exc)], "unavailable"
    if not version_at_least_14(version):
        errors.append(f"Bun {version} is below 1.4.0")

    if not (root / "bun.lock").is_file():
        errors.append("bun.lock is missing")
    for name in OLD_LOCKFILES:
        if (root / name).exists():
            errors.append(f"competing or legacy lockfile remains: {name}")

    root_path = root / "package.json"
    if not root_path.is_file():
        errors.append("package.json is missing")
        root_package: dict[str, object] = {}
    else:
        root_package = read_package(root_path, errors, root)
    for path in package_files(root, root_package):
        package = (
            root_package if path == root_path else read_package(path, errors, root)
        )
        check_package(path, package, errors, root)

    for path in active_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read {path.relative_to(root)}: {exc}")
            continue
        relative = path.relative_to(root)
        if OLD_BUN.search(text):
            errors.append(f"Bun version below 1.4 remains in {relative}")
        if FOREIGN_COMMAND.search(text):
            errors.append(f"foreign package-manager command remains in {relative}")
    return errors, version


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.repository).resolve()
    if not root.is_dir():
        print(f"ERROR: repository is not a directory: {root}", file=sys.stderr)
        return 2
    errors, version = audit(root)
    for message in errors:
        print(f"ERROR: {message}", file=sys.stderr)
    if errors:
        print(f"FAIL: {len(errors)} issue(s)", file=sys.stderr)
        return 1
    print(
        f"PASS: Bun {version}; scanned Bun 1.4 checks passed; manual inventory remains"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
