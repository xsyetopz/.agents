# my-dotagents-btw

A personal source directory for the user’s `.agents/` folder. It contains
reusable instruction packages, references, scripts, templates, and evaluation
files. Copy only the packages needed for a project or user account.

## Layout

```text
my-dotagents-btw/
├── skills/                 # reusable instruction packages
│   ├── apple-design-hig/
│   ├── architecture-design/
│   ├── architecture-enforce/
│   ├── avoid-ai-writing/
│   ├── git-actions/
│   ├── git-ci-cd/
│   ├── git-toolkit/
│   ├── git-workflows/
│   ├── prompt-engineering/
│   ├── repo-docs/
│   ├── repo-governance/
│   └── skill-creator/
├── evals/                  # disposable evaluation runner
├── docker/                 # evaluator image definition
└── scripts/                # repository checks and install probes
```

Each package has a `SKILL.md` entrypoint, package-local references, a checker,
and an `evals/evals.json` manifest. `references/index.md` is the starting point
for package documentation.

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
npx --yes skills@1.5.22 add xsyetopz/my-dotagents-btw \
  --skill prompt-engineering --agent codex --copy -y

bunx --bun skills@1.5.22 add xsyetopz/my-dotagents-btw \
  --skill prompt-engineering --agent codex --copy -y
```

GitHub source: [xsyetopz/my-dotagents-btw](https://github.com/xsyetopz/my-dotagents-btw).
For a local checkout, replace `xsyetopz/my-dotagents-btw` with
`/path/to/my-dotagents-btw`.

Replace `prompt-engineering` with the package name you need.

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
