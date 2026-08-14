"""Filesystem preflight and transaction rollback tests."""

from __future__ import annotations

from pathlib import Path
from unittest import mock

from test_governance_support import GovernanceTestCase, file_operations, governance


class GovernanceTransactionTests(GovernanceTestCase):
    def test_parent_symlink_regular_file_and_leaf_collisions_preflight_without_writes(
        self,
    ) -> None:
        outside = self.base / "outside"
        outside.mkdir()
        (self.repo / ".github").symlink_to(outside, target_is_directory=True)
        result = self.apply()
        self.assertEqual(2, result.returncode)
        self.assertIn("escapes through a parent symlink", result.stderr)
        self.assertEqual([], list(outside.iterdir()))
        self.assertFalse((self.repo / "AGENTS.md").exists())

        (self.repo / ".github").unlink()
        (self.repo / ".cursor").write_text("collision\n", encoding="utf-8")
        result = self.apply()
        self.assertEqual(2, result.returncode)
        self.assertIn("parent component is not a directory", result.stderr)
        self.assertFalse((self.repo / "AGENTS.md").exists())

        (self.repo / ".cursor").unlink()
        (self.repo / "AGENTS.md").mkdir()
        result = self.apply()
        self.assertEqual(2, result.returncode)
        self.assertIn("not a regular file", result.stdout)
        self.assertFalse((self.repo / "CONTRIBUTING.md").exists())

    def test_duplicate_output_path_is_rejected_before_mutation(self) -> None:
        result = self.apply("--readme", "AGENTS.md")
        self.assertEqual(2, result.returncode)
        self.assertIn("collides with a governance output", result.stderr)
        self.assertFalse((self.repo / "AGENTS.md").exists())

    def test_transaction_rolls_back_creates_updates_and_deletes_after_validation_failure(
        self,
    ) -> None:
        update = self.repo / "README.md"
        deleted = self.repo / "legacy.txt"
        created = self.repo / "new/created.txt"
        deleted.write_text("legacy\n", encoding="utf-8")
        operations = [
            governance.Operation(update, "update", "changed\n"),
            governance.Operation(deleted, "delete"),
            governance.Operation(created, "create", "created\n"),
        ]
        errors = governance.apply_transaction(
            operations, lambda: ["forced post-apply failure"]
        )
        self.assertEqual(["forced post-apply failure"], errors)
        self.assertEqual(
            "# Demo\n\n## License\n\nMIT license text.\n", update.read_text()
        )
        self.assertEqual("legacy\n", deleted.read_text())
        self.assertFalse(created.exists())
        self.assertFalse(created.parent.exists())

    def test_transaction_rolls_back_runtime_failure_and_runs_deletions_last(
        self,
    ) -> None:
        updated = self.repo / "README.md"
        deleted = self.repo / "legacy.txt"
        created = self.repo / "created.txt"
        deleted.write_text("legacy\n", encoding="utf-8")
        operations = [
            governance.Operation(deleted, "delete"),
            governance.Operation(updated, "update", "changed\n"),
            governance.Operation(created, "create", "created\n"),
        ]
        real_write = file_operations.atomic_write
        calls = 0

        def fail_second(path: Path, content: str) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                self.assertTrue(
                    deleted.exists(),
                    "recognized deletion must be scheduled after writes",
                )
                raise OSError("forced write failure")
            real_write(path, content)

        with (
            mock.patch.object(file_operations, "atomic_write", side_effect=fail_second),
            self.assertRaisesRegex(OSError, "forced write failure"),
        ):
            governance.apply_transaction(operations, list)
        self.assertIn("MIT license text.", updated.read_text())
        self.assertEqual("legacy\n", deleted.read_text())
        self.assertFalse(created.exists())


__all__ = ["GovernanceTransactionTests"]
