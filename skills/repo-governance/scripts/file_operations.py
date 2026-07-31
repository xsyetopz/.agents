"""Safe repository paths and transactional file operations."""

from __future__ import annotations

import os
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class Operation:
    path: Path
    action: str
    content: str | None = None
    reason: str | None = None

    def report(self, root: Path) -> dict[str, str]:
        result = {"path": self.path.relative_to(root).as_posix(), "action": self.action}
        if self.reason:
            result["reason"] = self.reason
        return result


@dataclass(frozen=True)
class Snapshot:
    existed: bool
    data: bytes = b""
    mode: int = 0o644


def safe_relative(value: str, label: str) -> Path:
    path = Path(value)
    if path.is_absolute() or path == Path(".") or ".." in path.parts:
        raise ValueError(
            f"{label} must be a repository-relative path without '..': {value}"
        )
    return path


def repo_path(root: Path, relative: str | Path) -> Path:
    relative_path = Path(relative)
    path = root / relative_path
    current = root
    for component in relative_path.parts[:-1]:
        current /= component
        if current.is_symlink():
            raise ValueError(
                f"repository path escapes through a parent symlink: {relative_path}"
            )
        if current.exists() and not current.is_dir():
            raise ValueError(
                f"repository parent component is not a directory: {current.relative_to(root)}"
            )
    if not path.parent.resolve().is_relative_to(root):
        raise ValueError(
            f"repository path escapes through a parent symlink: {relative}"
        )
    return path


def file_conflict(path: Path, label: str) -> Operation | None:
    if path.is_symlink():
        return Operation(path, "conflict", reason=f"{label} is a symlink")
    if path.exists() and not path.is_file():
        return Operation(path, "conflict", reason=f"{label} is not a regular file")
    return None


def assert_unique_paths(operations: list[Operation]) -> None:
    seen: set[Path] = set()
    duplicates: set[Path] = set()
    for operation in operations:
        if operation.path in seen:
            duplicates.add(operation.path)
        seen.add(operation.path)
    if duplicates:
        names = ", ".join(sorted(path.as_posix() for path in duplicates))
        raise ValueError(f"multiple operations target the same path: {names}")


def atomic_write_bytes(path: Path, data: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_write(path: Path, content: str) -> None:
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    atomic_write_bytes(path, content.encode("utf-8"), mode)


def apply_transaction(
    operations: list[Operation], validator: Callable[[], list[str]]
) -> list[str]:
    """Apply a plan atomically at the repository-file level; deletions run last."""
    mutating = [
        operation
        for operation in operations
        if operation.action in {"create", "update", "delete"}
    ]
    assert_unique_paths(mutating)
    snapshots: dict[Path, Snapshot] = {}
    created_directories: set[Path] = set()
    for operation in mutating:
        conflict = file_conflict(operation.path, "operation path")
        if conflict:
            raise ValueError(conflict.reason)
        if operation.path.exists():
            snapshots[operation.path] = Snapshot(
                True,
                operation.path.read_bytes(),
                stat.S_IMODE(operation.path.stat().st_mode),
            )
        else:
            snapshots[operation.path] = Snapshot(False)
        parent = operation.path.parent
        while not parent.exists():
            created_directories.add(parent)
            parent = parent.parent

    def rollback() -> None:
        for path, snapshot in reversed(list(snapshots.items())):
            if snapshot.existed:
                atomic_write_bytes(path, snapshot.data, snapshot.mode)
            elif path.exists() or path.is_symlink():
                if path.is_file() or path.is_symlink():
                    path.unlink()
        for directory in sorted(
            created_directories, key=lambda item: len(item.parts), reverse=True
        ):
            try:
                directory.rmdir()
            except OSError:
                pass

    try:
        for operation in sorted(mutating, key=lambda item: item.action == "delete"):
            if operation.action in {"create", "update"}:
                if operation.content is None:
                    raise ValueError(
                        f"missing content for {operation.action}: {operation.path}"
                    )
                atomic_write(operation.path, operation.content)
            else:
                operation.path.unlink()
        errors = validator()
        if errors:
            rollback()
        return errors
    except BaseException:
        rollback()
        raise
