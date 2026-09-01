# .agents

A personal source directory for the user’s `.agents/` folder. It contains
reusable instruction packages, references, deterministic tools, templates, and
Codex interface metadata. Copy only the packages needed for a project or user
account.

Each package has a `SKILL.md` entrypoint, Codex interface metadata, and a
package-local `license.txt`. References, scripts, and assets are included only
when the workflow uses them. Every reference is one level below its package
root and linked directly from the decision step that needs it; packages contain
no reference indexes or reference-to-reference Markdown chains. Deterministic
scripts are executable. Skills keep outputs in established repository formats; custom schema or generated
files require an explicit repository contract.

## Copy a package

User scope:

```bash
mkdir -p ~/.agents/skills
cp -R skills/repository-docs ~/.agents/skills/
```

Project scope:

```bash
mkdir -p .agents/skills
cp -R skills/repository-docs .agents/skills/
```

The pinned Skills CLI can copy one package from GitHub:

```bash
bunx --yes skills@1.5.22 add xsyetopz/.agents \
  --skill repository-docs --agent codex --copy -y

bunx --bun skills@1.5.22 add xsyetopz/.agents \
  --skill repository-docs --agent codex --copy -y
```

GitHub source: [xsyetopz/.agents](https://github.com/xsyetopz/.agents).
For a local checkout, replace `xsyetopz/.agents` with
`/path/to/.agents`.

Replace `repository-docs` with the package name you need.

To inspect a project-scoped install, list the selected agent in JSON. Use
either runner; the project list should include the copied package and
`skills-lock.json` should contain its lock entry:

```bash
bunx --yes skills@1.5.22 list --agent codex --json
test -f .agents/skills/repository-docs/SKILL.md
test -f skills-lock.json
python3 - <<'PY'
import json
from pathlib import Path

lock = json.loads(Path("skills-lock.json").read_text())
assert "repository-docs" in lock.get("skills", {})
PY

bunx --bun skills@1.5.22 list --agent codex --json
test -f .agents/skills/repository-docs/SKILL.md
test -f skills-lock.json
python3 - <<'PY'
import json
from pathlib import Path

lock = json.loads(Path("skills-lock.json").read_text())
assert "repository-docs" in lock.get("skills", {})
PY
```

For the disposable project fixture used above, remove the selected package with
one runner and the pinned command shape `remove --skill <name> --agent codex -y`:

```bash
bunx --yes skills@1.5.22 remove --skill repository-docs --agent codex -y
bunx --bun skills@1.5.22 remove --skill repository-docs --agent codex -y
```

After removal, verify both the list and lock metadata with either runner:

```bash
bunx --yes skills@1.5.22 list --agent codex --json
# In a fixture containing only repository-docs, the output above is [].
bunx --bun skills@1.5.22 list --agent codex --json
# The same selected-only fixture also reports [].
test ! -e .agents/skills/repository-docs
python3 - <<'PY'
import json
from pathlib import Path

lock = json.loads(Path("skills-lock.json").read_text())
assert "repository-docs" not in lock.get("skills", {})
PY
```

In a fixture containing only the selected package, the post-remove list is
`[]`. If the project also has unrelated skills, their list rows and lock
entries remain; only the selected package is removed.

This Codex-only removal command is not a shared-target recipe. If several
agents use the same `.agents` target, run the pinned `list --json` command first,
pass every agent sharing the selected package to `remove`, and verify the
filesystem, list, and lock after the command regardless of its exit status.

Run the disposable CLI smoke probe with either launcher:

```bash
RUNNER=bunx SOURCE="$PWD" bash scripts/skills_cli_smoke.sh
RUNNER=bunx-bun SOURCE="$PWD" bash scripts/skills_cli_smoke.sh
```

## Check the repository

```bash
for d in skills/*; do
  test -f "$d/SKILL.md" || exit 1
  test -f "$d/agents/openai.yaml" || exit 1
  test -f "$d/license.txt" || exit 1
done
python3 scripts/check_python_loc.py
python3 scripts/generate_skill_reports.py --check
uvx ruff@0.16.1 check --isolated skills scripts
find skills -name SKILL.md -print | sort
find skills -type l -print
bash -n scripts/skills_cli_smoke.sh
```
