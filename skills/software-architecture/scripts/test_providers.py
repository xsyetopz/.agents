"""Contract tests for executable architecture providers."""

from __future__ import annotations

import json
import stat
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from provider_ast import run_ast_grep


class ArchitectureToolsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name) / "repo with spaces"
        (self.root / "src").mkdir(parents=True)
        (self.root / "src/main.py").write_text("import os\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def fake_provider(
        self, output: str, *, exit_code: int = 0, sleep: float = 0
    ) -> str:
        path = self.root / "fake ast-grep"
        script = textwrap.dedent(
            f"""
            #!/usr/bin/env python3
            import sys
            import time
            if sys.argv[1:] == ["--version"]:
                print("ast-grep test 1.0")
                raise SystemExit(0)
            time.sleep({sleep!r})
            print({output!r}, end="")
            raise SystemExit({exit_code})
            """
        ).lstrip()
        path.write_text(script, encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return str(path)

    def match(self, file: str = "src/main.py") -> str:
        return (
            json.dumps(
                {
                    "file": file,
                    "range": {
                        "start": {"line": 0, "column": 0},
                        "end": {"line": 0, "column": 10},
                    },
                }
            )
            + "\n"
        )

    def test_valid_stream_normalizes_ranges_and_preserves_argv(self) -> None:
        executable = self.fake_provider(self.match())
        result = run_ast_grep(
            self.root,
            rule_id="forbidden-import",
            language="python",
            pattern="import $MODULE",
            severity="error",
            message="boundary violation",
            paths=("src",),
            executable=executable,
        )
        self.assertEqual(result.status, "violations")
        self.assertEqual(
            (result.findings[0].start_line, result.findings[0].start_column), (1, 1)
        )
        self.assertEqual(result.findings[0].path, (self.root / "src/main.py").resolve())
        self.assertIn("--pattern", result.argv)
        self.assertIn("import $MODULE", result.argv)

    def test_empty_success_is_pass(self) -> None:
        executable = self.fake_provider("", exit_code=1)
        result = run_ast_grep(
            self.root,
            rule_id="clean",
            language="python",
            pattern="pass",
            severity="warning",
            message="match",
            executable=executable,
        )
        self.assertEqual(result.status, "passed")

    def test_missing_provider_is_blocked(self) -> None:
        result = run_ast_grep(
            self.root,
            rule_id="missing",
            language="python",
            pattern="pass",
            severity="error",
            message="match",
            executable=str(self.root / "missing"),
        )
        self.assertEqual(result.status, "blocked")

    def test_malformed_and_duplicate_output_never_passes(self) -> None:
        malformed = self.fake_provider("not-json\n")
        duplicate = self.fake_provider('{"file":"src/main.py","file":"src/main.py"}\n')
        for executable in (malformed, duplicate):
            result = run_ast_grep(
                self.root,
                rule_id="bad",
                language="python",
                pattern="pass",
                severity="warning",
                message="match",
                executable=executable,
            )
            self.assertEqual(result.status, "invalid-output")

    def test_outside_path_is_rejected(self) -> None:
        executable = self.fake_provider(self.match("../outside.py"))
        result = run_ast_grep(
            self.root,
            rule_id="escape",
            language="python",
            pattern="pass",
            severity="warning",
            message="match",
            executable=executable,
        )
        self.assertEqual(result.status, "invalid-output")
        self.assertIn("escapes repository", result.diagnostics[0])

    def test_timeout_is_distinct(self) -> None:
        executable = self.fake_provider("", sleep=0.2)
        result = run_ast_grep(
            self.root,
            rule_id="slow",
            language="python",
            pattern="pass",
            severity="warning",
            message="match",
            timeout_s=0.01,
            executable=executable,
        )
        self.assertEqual(result.status, "timeout")


if __name__ == "__main__":
    unittest.main()
