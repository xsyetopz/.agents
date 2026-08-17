# my-dotagents-btw

A personal source directory for the user’s `.agents/` folder. It contains
reusable instruction packages, references, scripts, templates, and evaluation
files. Copy only the packages needed for a project or user account.

## Layout

```text
my-dotagents-btw/
├── skills/                 # reusable instruction packages
│   ├── apple-design-hig/
│   ├── avoid-ai-writing/
│   ├── git-actions/
│   ├── git-ci-cd/
│   ├── git-workflows/
│   ├── no-legacy-cleanup/
│   ├── prompt-engineering/
│   ├── repo-docs/
│   ├── skill-creator/
│   └── software-architecture/
├── evals/                  # disposable evaluation runner
├── docker/                 # evaluator image definition
└── scripts/                # repository checks and install probes
```

Each package has a `SKILL.md` entrypoint, package-local references, a Python 3
checker, and an `evals/evals.json` manifest. `references/index.md` is the
starting point for package documentation. Package tools are Python 3 only.
Skills must not invent custom schema files or custom generated files as outputs.

## Copy a package

User scope:

```bash
mkdir -p ~/.agents/skills
cp -R skills/prompt-engineering ~/.agents/skills/
```

Project scope:

```bash
mkdir -p .agents/skills
cp -R skills/prompt-engineering .agents/skills/
```

The pinned Skills CLI can copy one package from GitHub:

```bash
bunx --yes skills@1.5.22 add xsyetopz/my-dotagents-btw \
  --skill prompt-engineering --agent codex --copy -y

bunx --bun skills@1.5.22 add xsyetopz/my-dotagents-btw \
  --skill prompt-engineering --agent codex --copy -y
```

GitHub source: [xsyetopz/my-dotagents-btw](https://github.com/xsyetopz/my-dotagents-btw).
For a local checkout, replace `xsyetopz/my-dotagents-btw` with
`/path/to/my-dotagents-btw`.

Replace `prompt-engineering` with the package name you need.

To inspect a project-scoped install, list the selected agent in JSON. Use
either runner; the project list should include the copied package and
`skills-lock.json` should contain its lock entry:

```bash
bunx --yes skills@1.5.22 list --agent codex --json
test -f .agents/skills/prompt-engineering/SKILL.md
test -f skills-lock.json
python3 - <<'PY'
import json
from pathlib import Path

lock = json.loads(Path("skills-lock.json").read_text())
assert "prompt-engineering" in lock.get("skills", {})
PY

bunx --bun skills@1.5.22 list --agent codex --json
test -f .agents/skills/prompt-engineering/SKILL.md
test -f skills-lock.json
python3 - <<'PY'
import json
from pathlib import Path

lock = json.loads(Path("skills-lock.json").read_text())
assert "prompt-engineering" in lock.get("skills", {})
PY
```

For the disposable project fixture used above, remove the selected package with
one runner and the pinned command shape `remove --skill <name> --agent codex -y`:

```bash
bunx --yes skills@1.5.22 remove --skill prompt-engineering --agent codex -y
bunx --bun skills@1.5.22 remove --skill prompt-engineering --agent codex -y
```

After removal, verify both the list and lock metadata with either runner:

```bash
bunx --yes skills@1.5.22 list --agent codex --json
# In a fixture containing only prompt-engineering, the output above is [].
bunx --bun skills@1.5.22 list --agent codex --json
# The same selected-only fixture also reports [].
test ! -e .agents/skills/prompt-engineering
python3 - <<'PY'
import json
from pathlib import Path

lock = json.loads(Path("skills-lock.json").read_text())
assert "prompt-engineering" not in lock.get("skills", {})
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
RUNNER=bunx SOURCE="$PWD" bash scripts/skills_cli_smoke.sh
```

## Check the repository

```bash
python3 skills/skill-creator/scripts/check_skill_structure.py "$PWD"
for d in skills/*; do
  (cd "$d" && python3 scripts/check.py) || exit 1
done
python3 scripts/check_python_loc.py
uvx ruff@0.16.1 check --isolated skills scripts
```

Run the disposable static evaluator when Docker or OrbStack is available:

```bash
bash evals/run_container_eval.sh --static-only --all
```
