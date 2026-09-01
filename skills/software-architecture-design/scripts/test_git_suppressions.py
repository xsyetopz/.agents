#!/usr/bin/env python3
"""Regression tests for Git-worktree suppression detection."""

from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from architecture_audit import git_suppression_findings
from architecture_audit.discovery import GitInventoryError
from test_support import AuditFixture


class GitSuppressionTests(AuditFixture, unittest.TestCase):
    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )

    def init_git(self) -> None:
        self.git("init", "-q")
        self.git("config", "user.email", "audit@example.invalid")
        self.git("config", "user.name", "Architecture Audit")

    def commit(self, message: str = "baseline") -> None:
        self.git("add", "--all")
        self.git("commit", "-qm", message)

    def test_git_ignore_candidates_stage_unstage_and_untracked_are_blocking(
        self,
    ) -> None:
        self.init_git()
        self.write("README.md", content="baseline\n")
        self.write(".gitignore", content="dist/\n")
        self.write(".eslintignore", content="# baseline\n")
        self.commit()

        self.write(".eslintignore", content="# baseline\nsrc/generated\n")
        self.git("add", ".eslintignore")
        self.write(".stylelintignore", content="src/vendor/**\n")
        self.write(".gitignore", content="dist/\nsrc/**\nignored/.eslintignore\n")
        self.write("ignored/.eslintignore", content="src/vendor/generated/**\n")
        self.write(".ruffignore", content="# comment only\n\n")
        findings = git_suppression_findings(self.root)
        codes = {item.code for item in findings}
        self.assertIn("ignore-pattern-added", codes)
        self.assertIn("gitignore-source-pattern-added", codes)
        lines = {(item.path.name, item.message) for item in findings}
        self.assertTrue(
            any(
                name == ".eslintignore" and "line 2" in message
                for name, message in lines
            )
        )
        self.assertTrue(
            any(
                name == ".stylelintignore" and "line 1" in message
                for name, message in lines
            )
        )
        self.assertTrue(
            any(name == ".gitignore" and "line 2" in message for name, message in lines)
        )
        self.assertFalse(
            any(
                name == ".eslintignore" and "line 1" in message
                for name, message in lines
            )
        )
        self.assertFalse(any(name == ".ruffignore" for name, _ in lines))

    def test_git_destructive_deletions_and_removed_provider_lines_are_blocking(
        self,
    ) -> None:
        self.init_git()
        self.write("tests/test_runner.py", content="def test_runner():\n    pass\n")
        self.write("scripts/check.sh", content="#!/bin/sh\nnpm test\n")
        self.write(
            ".github/workflows/test.yml", content="jobs:\n  test:\n    steps: []\n"
        )
        self.commit()
        self.git("rm", "-q", "tests/test_runner.py")
        self.write("scripts/check.sh", content="#!/bin/sh\necho no-op\n")
        (self.root / ".github/workflows/test.yml").unlink()
        findings = git_suppression_findings(self.root)
        codes = {item.code for item in findings}
        self.assertIn("check-file-deleted", codes)
        self.assertIn("check-provider-removed", codes)
        self.assertTrue(
            any(
                item.path.name == "test_runner.py"
                for item in findings
                if item.code == "check-file-deleted"
            )
        )
        self.assertTrue(
            any(
                item.path.name == "check.sh" and "line 2" in item.message
                for item in findings
                if item.code == "check-provider-removed"
            )
        )
        self.assertTrue(
            any(
                item.path.name == "test.yml"
                for item in findings
                if item.code == "check-file-deleted"
            )
        )

    def test_git_initial_state_and_nonrelevant_changes_are_not_false_positives(
        self,
    ) -> None:
        self.init_git()
        self.write(".eslintignore", content="src/generated\n")
        self.write(".gitignore", content="dist/\n")
        self.write("src/app.py", content="value = 1\n")
        self.write("scripts/check.sh", content="#!/bin/sh\necho ok\n")
        self.commit()
        self.assertEqual(git_suppression_findings(self.root), [])
        self.write(".eslintignore", content="src/generated\n# rationale\n")
        self.write(".gitignore", content="dist/\ndocs/**\n")
        self.write("scripts/check.sh", content="#!/bin/sh\necho still-ok\n")
        self.assertEqual(git_suppression_findings(self.root), [])

    def test_git_suppression_scan_failure_is_blocking(self) -> None:
        self.init_git()
        self.write("README.md", content="baseline\n")
        self.commit()
        with patch(
            "architecture_audit.git_suppression_diff.run_git_diff",
            side_effect=GitInventoryError("test failure"),
        ):
            findings = git_suppression_findings(self.root)
        self.assertEqual(
            [item.code for item in findings], ["git-suppression-scan-failed"]
        )

    def test_git_unrelated_same_parent_replacement_does_not_waive_test_deletion(
        self,
    ) -> None:
        self.init_git()
        self.write(
            "tests/test_security.py",
            content="def test_security():\n    assert 1 == 1\n",
        )
        self.commit()
        self.git("rm", "-q", "tests/test_security.py")
        self.write(
            "tests/test_unrelated.py",
            content="def test_unrelated():\n    assert 2 == 2\n",
        )
        findings = git_suppression_findings(self.root)
        self.assertTrue(
            any(
                item.code == "check-file-deleted"
                and item.path.name == "test_security.py"
                for item in findings
            )
        )

    def test_git_cross_directory_r100_rename_does_not_report_old_test_deletion(
        self,
    ) -> None:
        self.init_git()
        self.write(
            "tests/legacy/test_runner.py",
            content="def test_runner():\n    assert 1 == 1\n",
        )
        self.commit()
        (self.root / "tests/current").mkdir(parents=True)
        self.git("mv", "tests/legacy/test_runner.py", "tests/current/test_runner.py")
        findings = git_suppression_findings(self.root)
        self.assertFalse(any(item.code == "check-file-deleted" for item in findings))

    def test_git_renamed_test_provider_line_does_not_report_removed_provider(
        self,
    ) -> None:
        self.init_git()
        self.write(
            "tests/legacy/test_runner.ts",
            content='import { describe, it } from "vitest";\n\ndescribe("runner", () => it("works", () => undefined));\n',
        )
        self.commit()
        (self.root / "tests/current").mkdir(parents=True)
        self.git("mv", "tests/legacy/test_runner.ts", "tests/current/test_runner.ts")
        findings = git_suppression_findings(self.root)
        self.assertFalse(
            any(item.code == "check-provider-removed" for item in findings)
        )

    def test_git_renamed_provider_removal_is_not_hidden_by_r99_move(self) -> None:
        self.init_git()
        self.write(
            "tests/legacy/check.ts",
            content=(
                "#!/usr/bin/env bun\nbun test\n"
                + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 99))
            ),
        )
        self.commit()
        (self.root / "tests/current").mkdir(parents=True)
        (self.root / "tests/current/check.ts").write_text(
            "#!/usr/bin/env bun\necho provider removed\n"
            + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 99)),
            encoding="utf-8",
        )
        (self.root / "tests/legacy/check.ts").unlink()
        self.git("add", "--all")
        rename_status = self.git(
            "diff", "--cached", "--find-renames=90", "--name-status"
        ).stdout
        self.assertIn("R099", rename_status)
        findings = git_suppression_findings(self.root)
        provider_findings = [
            item for item in findings if item.code == "check-provider-removed"
        ]
        self.assertEqual(len(provider_findings), 1)
        self.assertIn("bun test", provider_findings[0].message)

    def test_git_low_score_same_basename_import_relocation_keeps_r90_boundary(
        self,
    ) -> None:
        self.init_git()
        self.write(
            "tests/legacy/check.ts",
            content=(
                "".join(
                    f'import dep{i} from "../../src/dep{i}";\n' for i in range(1, 6)
                )
                + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 21))
            ),
        )
        self.commit()
        (self.root / "tests/current/nested").mkdir(parents=True)
        (self.root / "tests/current/nested/check.ts").write_text(
            (self.root / "tests/legacy/check.ts")
            .read_text(encoding="utf-8")
            .replace("../../src/", "../../../src/"),
            encoding="utf-8",
        )
        (self.root / "tests/legacy/check.ts").unlink()
        self.git("add", "--all")
        raw = self.git("diff", "--cached", "--find-renames=1", "--name-status").stdout
        self.assertIn("R076", raw)
        self.assertNotIn(
            "R090",
            self.git("diff", "--cached", "--find-renames=90", "--name-status").stdout,
        )
        findings = git_suppression_findings(self.root)
        self.assertFalse(any(item.code == "check-file-deleted" for item in findings))

    def test_git_low_score_same_basename_replacement_stays_blocking(self) -> None:
        self.init_git()
        self.write(
            "tests/legacy/check.ts",
            content=(
                "#!/usr/bin/env bun\nbun test\n"
                + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 99))
            ),
        )
        self.commit()
        (self.root / "tests/current").mkdir(parents=True)
        (self.root / "tests/current/check.ts").write_text(
            "#!/usr/bin/env bun\necho provider removed\n"
            + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 85))
            + "".join(
                f"export const replacement{i} = {i * 10};\n" for i in range(85, 101)
            ),
            encoding="utf-8",
        )
        (self.root / "tests/legacy/check.ts").unlink()
        self.git("add", "--all")
        rename_status = self.git(
            "diff", "--cached", "--find-renames=80", "--name-status"
        ).stdout
        self.assertIn("R082", rename_status)
        self.assertNotIn(
            "R090",
            self.git("diff", "--cached", "--find-renames=90", "--name-status").stdout,
        )
        findings = git_suppression_findings(self.root)
        self.assertTrue(any(item.code == "check-file-deleted" for item in findings))

    def test_git_non_script_rename_provider_text_is_not_a_provider_removal(
        self,
    ) -> None:
        self.init_git()
        self.write(
            "docs/old/guide.md",
            content="vitest is used for examples\n"
            + "".join(f"example {i}\n" for i in range(1, 100)),
        )
        self.commit()
        (self.root / "docs/new").mkdir(parents=True)
        (self.root / "docs/new/guide.md").write_text(
            "examples use another runner\n"
            + "".join(f"example {i}\n" for i in range(1, 100)),
            encoding="utf-8",
        )
        (self.root / "docs/old/guide.md").unlink()
        self.git("add", "--all")
        rename_status = self.git(
            "diff", "--cached", "--find-renames=90", "--name-status"
        ).stdout
        self.assertIn("R", rename_status)
        findings = git_suppression_findings(self.root)
        self.assertFalse(
            any(item.code == "check-provider-removed" for item in findings)
        )

    def test_git_r100_test_move_out_of_check_path_stays_blocking(self) -> None:
        self.init_git()
        self.write(
            "tests/legacy/runner.ts",
            content=(
                'import { describe, it } from "vitest";\n'
                + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 99))
            ),
        )
        self.commit()
        (self.root / "src").mkdir(parents=True)
        (self.root / "src/runner.ts").write_text(
            'import { describe, it } from "vitest";\n'
            + "".join(f"export const invariant{i} = {i};\n" for i in range(1, 99)),
            encoding="utf-8",
        )
        (self.root / "tests/legacy/runner.ts").unlink()
        self.git("add", "--all")
        rename_status = self.git(
            "diff", "--cached", "--find-renames=90", "--name-status"
        ).stdout
        self.assertIn("R100", rename_status)
        findings = git_suppression_findings(self.root)
        self.assertTrue(any(item.code == "check-file-deleted" for item in findings))

    def test_git_real_test_deletion_still_blocks_with_rename_inventory(self) -> None:
        self.init_git()
        self.write(
            "tests/test_runner.py", content="def test_runner():\n    assert 1 == 1\n"
        )
        self.commit()
        self.git("rm", "-q", "tests/test_runner.py")
        findings = git_suppression_findings(self.root)
        self.assertTrue(
            any(
                item.code == "check-file-deleted" and item.path.name == "test_runner.py"
                for item in findings
            )
        )

    def test_git_weak_rename_evidence_does_not_waive_test_deletion(self) -> None:
        self.init_git()
        self.write(
            "tests/test_security.py",
            content="def test_security():\n    assert 1 == 1\n",
        )
        self.commit()
        self.git("rm", "-q", "tests/test_security.py")
        weak_inventory = b"R89\0tests/test_security.py\0tests/test_unrelated.py\0"
        with patch(
            "architecture_audit.git_suppression_diff.run_git_rename_inventory",
            return_value=weak_inventory,
        ):
            findings = git_suppression_findings(self.root)
        self.assertTrue(
            any(
                item.code == "check-file-deleted"
                and item.path.name == "test_security.py"
                for item in findings
            )
        )

    def test_git_malformed_rename_evidence_does_not_waive_test_deletion(self) -> None:
        self.init_git()
        self.write(
            "tests/test_security.py",
            content="def test_security():\n    assert 1 == 1\n",
        )
        self.commit()
        self.git("rm", "-q", "tests/test_security.py")
        malformed_inventory = b"R100\0tests/test_security.py\0tests/test_security.py\0"
        with patch(
            "architecture_audit.git_suppression_diff.run_git_rename_inventory",
            return_value=malformed_inventory,
        ):
            findings = git_suppression_findings(self.root)
        self.assertTrue(
            any(
                item.code == "check-file-deleted"
                and item.path.name == "test_security.py"
                for item in findings
            )
        )

    def test_git_placeholder_replacement_does_not_waive_test_deletion(self) -> None:
        self.init_git()
        self.write("tests/test_security.py", content="def test_security():\n    pass\n")
        self.commit()
        self.git("rm", "-q", "tests/test_security.py")
        self.write("tests/test_placeholder.py", content="value = 1\n")
        self.assertTrue(
            any(
                item.code == "check-file-deleted"
                for item in git_suppression_findings(self.root)
            )
        )

    def test_gitignored_replacement_does_not_waive_test_deletion(self) -> None:
        self.init_git()
        self.write("tests/test_legacy.py", content="def test_old():\n    pass\n")
        self.write(".gitignore", content="tests/test_new.py\n")
        self.commit()
        self.git("rm", "-q", "tests/test_legacy.py")
        self.write("tests/test_new.py", content="def test_new():\n    assert 1 == 1\n")
        self.assertTrue(
            any(
                item.code == "check-file-deleted"
                for item in git_suppression_findings(self.root)
            )
        )


if __name__ == "__main__":
    unittest.main()
