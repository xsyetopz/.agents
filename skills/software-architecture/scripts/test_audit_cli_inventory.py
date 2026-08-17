"""CLI regression tests for Git-backed audit inventory."""

from __future__ import annotations

import importlib
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import DEFAULT, patch

from architecture_audit.audit import audit_report
from architecture_audit.discovery import GitInventoryError, iter_audited_files
from test_support import AuditFixture


class AuditCliInventoryTests(AuditFixture, unittest.TestCase):
    def test_ignored_untracked_source_is_excluded_but_tracked_source_remains(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args],
                check=True,
                capture_output=True,
                text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / ".gitignore").write_text("src/**\n", encoding="utf-8")
            tracked = case_root / "src/tracked.ts"
            tracked.parent.mkdir()
            tracked.write_text("export const tracked = 1;\n", encoding="utf-8")
            run("add", ".gitignore")
            run("add", "-f", "src/tracked.ts")
            run("commit", "-qm", "baseline")
            (case_root / "src/ignored.ts").write_text(
                "// eslint-disable-next-line no-console\nconsole.log('ignored');\n",
                encoding="utf-8",
            )
            paths = {
                path.relative_to(case_root.absolute()).as_posix()
                for path in iter_audited_files(case_root)
            }
            self.assertIn("src/tracked.ts", paths)
            self.assertNotIn("src/ignored.ts", paths)
            result = self.run_cli("--format", "json", root=case_root)
            payload = self.json_output(result)
            self.assertIn("src/tracked.ts", payload["audited_paths"])
            self.assertNotIn("src/ignored.ts", payload["audited_paths"])
            self.assertFalse(
                any(item["path"] == "src/ignored.ts" for item in payload["findings"])
            )
            self.assertIn(
                "gitignore-source-pattern-added",
                {item["code"] for item in payload["findings"]},
            )

    def test_tracked_source_inside_ignored_directory_remains_auditable(self) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args],
                check=True,
                capture_output=True,
                text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / ".gitignore").write_text("node_modules/**\n", encoding="utf-8")
            tracked = case_root / "node_modules/owned/tracked.ts"
            tracked.parent.mkdir(parents=True)
            tracked.write_text("export const tracked = 1;\n", encoding="utf-8")
            run("add", ".gitignore")
            run("add", "-f", "node_modules/owned/tracked.ts")
            run("commit", "-qm", "baseline")
            paths = {
                path.relative_to(case_root.absolute()).as_posix()
                for path in iter_audited_files(case_root)
            }
            self.assertIn("node_modules/owned/tracked.ts", paths)

    def test_tracked_broken_symlink_remains_inventoried(self) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args],
                check=True,
                capture_output=True,
                text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            link = case_root / "src/tracked-link.ts"
            link.parent.mkdir()
            link.symlink_to("missing.ts")
            run("add", "src/tracked-link.ts")
            run("commit", "-qm", "baseline")
            paths = {
                path.relative_to(case_root.absolute()).as_posix()
                for path in iter_audited_files(case_root)
            }
            self.assertIn("src/tracked-link.ts", paths)

    def test_ignored_package_manifests_are_not_scanned_for_lock_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args],
                check=True,
                capture_output=True,
                text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / ".gitignore").write_text("ignored/**\n", encoding="utf-8")
            run("add", ".gitignore")
            run("commit", "-qm", "baseline")
            ignored = case_root / "ignored"
            ignored.mkdir()
            (ignored / "package.json").write_text("{}\n", encoding="utf-8")
            (ignored / "package-lock.json").write_text("{}\n", encoding="utf-8")
            (ignored / "yarn.lock").write_text("# ignored\n", encoding="utf-8")
            result = self.run_cli("--format", "json", root=case_root)
            self.assertEqual(result.returncode, 0)
            payload = self.json_output(result)
            self.assertNotIn("ignored/package.json", payload["audited_paths"])
            self.assertNotIn(
                "conflicting-lockfiles", {item["code"] for item in payload["findings"]}
            )

    def test_tracked_package_lockfiles_remain_visible_to_package_checks(self) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args],
                check=True,
                capture_output=True,
                text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / "package.json").write_text("{}\n", encoding="utf-8")
            (case_root / "package-lock.json").write_text("{}\n", encoding="utf-8")
            (case_root / "yarn.lock").write_text("# tracked\n", encoding="utf-8")
            run("add", ".")
            run("commit", "-qm", "baseline")
            result = self.run_cli("--format", "json", root=case_root)
            self.assertEqual(result.returncode, 1)
            self.assertIn(
                "conflicting-lockfiles",
                {item["code"] for item in self.json_output(result)["findings"]},
            )

    def test_git_inventory_failure_does_not_fall_back_to_ignored_files(self) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args],
                check=True,
                capture_output=True,
                text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / ".gitignore").write_text("ignored/**\n", encoding="utf-8")
            run("add", ".gitignore")
            run("commit", "-qm", "baseline")
            ignored = case_root / "ignored/source.ts"
            ignored.parent.mkdir()
            ignored.write_text("export const ignored = 1;\n", encoding="utf-8")

            def fail_discovery(
                command: list[str], *args: object, **kwargs: object
            ) -> object:
                if command[:4] == ["git", "-C", str(case_root), "rev-parse"]:
                    raise subprocess.TimeoutExpired(command, 10)
                return DEFAULT

            with (
                patch(
                    "architecture_audit.discovery.subprocess.run",
                    side_effect=fail_discovery,
                    wraps=subprocess.run,
                ),
                self.assertRaises(GitInventoryError),
            ):
                list(iter_audited_files(case_root))

    def test_inventory_failure_reports_a_blocking_finding(self) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args],
                check=True,
                capture_output=True,
                text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / ".gitignore").write_text("ignored/**\n", encoding="utf-8")
            run("add", ".gitignore")
            run("commit", "-qm", "baseline")
            ignored = case_root / "ignored/source.ts"
            ignored.parent.mkdir()
            ignored.write_text("export const ignored = 1;\n", encoding="utf-8")
            audit_module = importlib.import_module("architecture_audit.audit")
            with patch.object(
                audit_module,
                "_git_inventory",
                side_effect=GitInventoryError("test failure"),
            ):
                report = audit_report(case_root)
            self.assertEqual(
                {item.code for item in report.findings}, {"git-inventory-failed"}
            )
            self.assertEqual(report.files, ())

    def test_tracked_deep_directories_are_used_for_topology_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args],
                check=True,
                capture_output=True,
                text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            for relative in ("src/Open/actor.ts", "src/Open/nested/deeper/actor.ts"):
                path = case_root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("export const value = 1;\n", encoding="utf-8")
            run("add", ".")
            run("commit", "-qm", "baseline")
            report = audit_report(case_root)
            self.assertFalse(
                any(
                    item.code == "single-file-directory"
                    and item.path == case_root / "src/Open"
                    for item in report.findings
                )
            )

    def test_git_output_dirs_reconcile_candidates_without_walking_bulk_or_nested_repos(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args],
                check=True,
                capture_output=True,
                text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / ".gitignore").write_text("dist/ignored/**\n", encoding="utf-8")
            for relative, content in {
                "dist/Open.ts": "export const open = 1;\n",
                "dist/Commit.ts": "export const commit = 1;\n",
            }.items():
                target = case_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            run("add", ".gitignore", "dist/Open.ts", "dist/Commit.ts")
            run("commit", "-qm", "baseline")
            (case_root / "dist/Reduce.ts").write_text(
                "export const reduce = 1;\n", encoding="utf-8"
            )
            (case_root / "dist/.eslintignore").write_text(
                "dist/generated/**\n", encoding="utf-8"
            )
            ignored = case_root / "dist/ignored"
            ignored.mkdir(parents=True)
            for index in range(400):
                (ignored / f"bulk-{index}.bin").write_bytes(b"generated output\n")
            nested = case_root / "nested"
            nested.mkdir()
            subprocess.run(
                ["git", "-C", str(nested), "init", "-q"],
                check=True,
                capture_output=True,
                text=True,
            )
            (nested / "src").mkdir()
            (nested / "src/hidden.ts").write_text(
                "export const hidden = 1;\n", encoding="utf-8"
            )
            # Discovery preserves the caller's lexical root spelling so
            # findings remain stable on macOS /var <-> /private/var aliases.
            resolved_root = case_root.absolute()
            paths = {
                path.relative_to(resolved_root).as_posix()
                for path in iter_audited_files(case_root)
            }
            self.assertTrue(
                {
                    "dist/Open.ts",
                    "dist/Commit.ts",
                    "dist/Reduce.ts",
                    "dist/.eslintignore",
                }
                <= paths
            )
            self.assertFalse(any(path.startswith("dist/ignored/") for path in paths))
            self.assertNotIn("nested/src/hidden.ts", paths)

    def test_ignored_untracked_output_phases_are_not_audited(self) -> None:
        """Ignored output trees are omitted from every audit phase."""

        with tempfile.TemporaryDirectory() as case_dir:
            case_root = Path(case_dir)
            run = lambda *args: subprocess.run(
                ["git", "-C", str(case_root), *args],
                check=True,
                capture_output=True,
                text=True,
            )
            run("init", "-q")
            run("config", "user.email", "audit@example.invalid")
            run("config", "user.name", "Architecture Audit")
            (case_root / ".gitignore").write_text("dist/**\n", encoding="utf-8")
            run("add", ".gitignore")
            run("commit", "-qm", "baseline")
            output = case_root / "dist"
            output.mkdir()
            for phase in ("Open", "Reduce", "Commit"):
                (output / f"{phase}.ts").write_text(
                    f"export const {phase.lower()} = 1;\n", encoding="utf-8"
                )
            paths = {
                path.relative_to(case_root.absolute()).as_posix()
                for path in iter_audited_files(case_root)
            }
            self.assertFalse(
                {f"dist/{phase}.ts" for phase in ("Open", "Reduce", "Commit")} & paths
            )
            result = self.run_cli("--format", "json", root=case_root)
            self.assertEqual(result.returncode, 0)
            payload = self.json_output(result)
            self.assertFalse(
                {f"dist/{phase}.ts" for phase in ("Open", "Reduce", "Commit")}
                & set(payload["audited_paths"])
            )
            codes = {item["code"] for item in payload["findings"]}
            self.assertNotIn("procedural-suffix", codes)
            self.assertNotIn("output-directory-source", codes)


if __name__ == "__main__":
    unittest.main()
