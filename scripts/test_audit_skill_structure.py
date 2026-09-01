from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Protocol, cast


class AuditModule(Protocol):
    ROOT: Path
    SKILLS: Path

    def main(self) -> int: ...


MODULE_PATH = Path(__file__).with_name("audit_skill_structure.py")
SPEC = importlib.util.spec_from_file_location("audit_skill_structure", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
_AUDIT_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(_AUDIT_MODULE)
AUDIT = cast(AuditModule, _AUDIT_MODULE)


def skill_text(name: str, extra_heading: str = "") -> str:
    return f"""---
name: {name}
description: Fixture skill.
---

# Fixture

## Start with evidence

Inspect the fixture.

## Workflow

Perform the fixture operation.

## Validation

Verify the fixture result.

## Boundaries

Preserve unrelated state.
{extra_heading}"""


class SkillStructureAuditTest(unittest.TestCase):
    def run_fixture(self, files: dict[str, str]) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skills = root / "skills"
            for relative, content in files.items():
                path = skills / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            previous_root = AUDIT.ROOT
            previous_skills = AUDIT.SKILLS
            AUDIT.ROOT = root
            AUDIT.SKILLS = skills
            output = io.StringIO()
            try:
                with redirect_stdout(output), redirect_stderr(output):
                    status = AUDIT.main()
            finally:
                AUDIT.ROOT = previous_root
                AUDIT.SKILLS = previous_skills
            return status, output.getvalue()

    def test_accepts_owo_skill_with_self_invocation_metadata(self):
        status, output = self.run_fixture(
            {
                "fixture/SKILL.md": skill_text("fixture"),
                "fixture/agents/openai.yaml": 'interface:\n  default_prompt: "Use $fixture."\n',
            }
        )

        self.assertEqual(0, status)
        self.assertIn("OWO skill structure valid for 1 skills", output)

    def test_rejects_extra_heading_and_companion_reference(self):
        status, output = self.run_fixture(
            {
                "fixture/SKILL.md": skill_text("fixture", "\n\n## Extra\n\nNo."),
                "fixture/agents/openai.yaml": 'interface:\n  default_prompt: "Use $companion."\n',
                "companion/SKILL.md": skill_text("companion"),
                "companion/agents/openai.yaml": 'interface:\n  default_prompt: "Use $companion."\n',
            }
        )

        self.assertEqual(1, status)
        self.assertIn("top-level headings", output)
        self.assertIn("references other skill names", output)
        self.assertIn("names companion skills directly", output)


if __name__ == "__main__":
    unittest.main()
