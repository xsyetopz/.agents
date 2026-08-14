# AGENTS.md

## Scope and precedence

These instructions apply to the entire `my-agent-skills-btw` repository. A
nested `AGENTS.md`, if introduced later, may narrow rules for its own subtree;
otherwise this file is the canonical repository guidance. Higher-priority system,
developer, and user instructions override this file. Keep each policy in one
canonical owner and update this file when the repository contract changes.

## Agent execution contract

- Work only on this repository and its code, tests, documentation, build,
  security, release, or maintenance.
- Do not use repository channels or credentials for personal attacks,
  harassment, unrelated discussion, repository damage, sabotage, or arguments
  that promote or oppose AI.
- Use neutral, factual, professional technical language. Discuss the work, not a
  person. Refuse unrelated or harmful external content and stop before the
  external action.
- Do not push, open or edit a pull request or issue, post a comment or review,
  change labels or settings, merge, release, or send another external message
  without explicit permission for the exact repository, action, and content or
  scope. Keep a local draft when publication permission is missing.
- Use the authenticated human, app, or bot identity configured by the host. Do
  not invent actor markers or misstate identity.
- Report actual validation. Do not invent tests, review, permission, source
  information, or results.

## Source boundary and catalog

- `skills/` is the sole distributed skill catalog. Each catalog package is an
  independent, portable skill with exactly one root-level `SKILL.md` entrypoint
  and the common package contract below. The approved inventory is:

  ```text
  skills/apple-design-hig/
  skills/architecture-design/
  skills/architecture-enforce/
  skills/avoid-ai-writing/
  skills/git-actions/
  skills/git-ci-cd/
  skills/git-toolkit/
  skills/git-workflows/
  skills/prompt-engineering/
  skills/repo-docs/
  skills/repo-governance/
  skills/skill-creator/
  ```

- `skills/skill-creator/` is the maintained destination authoring skill. It is
  not copied from the old source `/Users/krystian/.agents/skills/skill-creator/`.
- The other eleven packages are imported from the source worktree
  `/Users/krystian/.agents/skills/` only when their files are non-gitignored.
  Include reviewed, nonignored working-tree files and operational resources;
  selection follows that worktree's `.gitignore`, not tracking status alone.
- Explicitly exclude the old source `skill-creator` and every source-gitignored
  root: `design-taste-frontend`, `dry-refactoring`, `find-skills`,
  `full-output-enforcement`, `gpt-taste`, `high-end-visual-design`, `impeccable`,
  `install-skizzles`, `jscpd`, `redesign-existing-projects`, `swiftui-pro`,
  `threejs-to-easeljs`, and `using-easeljs`. Do not import ignored caches such as
  `__pycache__/` or `.ruff_cache/` beneath an included root.
- Do not add a root `SKILL.md`, duplicate package entrypoint, wrapper, alias,
  symlink, or legacy compatibility path. A copied package must remain
  self-contained: runtime instructions, validators, references, scripts, and
  examples may not depend on this checkout, `/Users/krystian/.agents`, or any
  other global/external path. Preserve package-local resources and repair or
  remove escaping links instead of copying them.
- Prefer current implementations and remove obsolete behavior instead of
  adding compatibility shims.

## Common package contract

Every `skills/<name>/` directory is independently copyable and must contain:

```text
SKILL.md
LICENSE
.skill-validator.json
agents/openai.yaml
references/                 # at least one routed, package-relative file
assets/contract.json        # schema_version 1 package contract
evals/evals.json            # schema_version 1 evaluation manifest
scripts/check.py            # stdlib-only copied-package checker
```

`assets/contract.json` is required even when a skill has no other binary or
template asset. Additional assets are allowed only when the skill uses them;
do not add empty or fake assets. `agents/openai.yaml` must retain its validated
`interface.display_name`, `short_description`, and `default_prompt`; the
prompt invokes exactly `$<name>`.

`SKILL.md` has valid two-field frontmatter on line 1, a directory-matching
`name`, a concrete selection-facing `description`, and these exact level-two
headings in this order:

```text
Use this skill
Rules
Steps
Resources
Verify
```

Keep the entrypoint concise and progressively disclosed. `Use this skill` holds
positive triggers, exclusions, and sibling redirects. `Rules` contains only
non-negotiable constraints. `Steps` is one complete executable path. `Resources`
routes package-local references, indexes, assets, and scripts. `Verify` combines
done state, validation commands, evidence, and `UNVERIFIED` conditions. Do not
load every reference by default or duplicate policy between sections. The
five-part sequence is this repository's contract, not an upstream Agent Skills
requirement. The authored Python limit is **500 physical lines per file** under
`skills/`, including tests; no generated/vendor exemption exists.

`evals/evals.json` uses only this schema-by-convention (no results or fabricated
traces):

```json
{
  "schema_version": 1,
  "skill_name": "<name>",
  "static": [{
    "id": "package-contract",
    "command": "python3 scripts/check.py",
    "expect_exit": 0
  }],
  "codex_cases": [
    {"id": "positive-...", "prompt": "...", "expected_outcome": "..."},
    {"id": "near-miss-...", "prompt": "...", "expected_outcome": "..."},
    {"id": "safety-or-failure-...", "prompt": "...", "expected_outcome": "..."}
  ]
}
```

`static` must include the package checker. `codex_cases` must include a
positive, substantive near-miss, and relevant boundary/safety/failure case;
case records contain only `id`, `prompt`, and `expected_outcome`. Run results,
scores, timing, and model traces belong outside the package.

Package checks consume only the copied package tree and Python standard library.
They must verify frontmatter/headings, required files, routed relative links,
manifest/contract shape, path containment, symlink containment, and absence of
host/global paths or checkout dependencies. A static pass is not a behavioral
activation or security pass.

## Prompt ownership

- `skill-creator` authoring guidance is model-neutral. It defines portable skill
  structure, workflow, validation, and safety; it must not require GPT-5.6 or
  another named model for ordinary skill creation.
- Prompt design and audits, tool-routing policy, behavioral evals, and
  model-family guidance belong to `$prompt-engineering`. GPT-5.6 is one
  optional model family among many; route named-model work there rather than
  duplicating provider guidance in `skill-creator`.
- Official OpenAI prompting pages and Markdown snapshots are owned by
  `prompt-engineering`. Refresh them through `$openai-docs` when a named model
  is intentionally updated; do not create hand-authored model guides in
  `skill-creator`.

## Distribution pin policy

Use the verified Vercel Skills CLI pin `skills@1.5.22` for reproducible examples
and validation:

```bash
npx --yes skills@1.5.22 add xsyetopz/my-dotagents-btw \
  --skill skill-creator --agent codex --copy -y
bunx --bun skills@1.5.22 add xsyetopz/my-dotagents-btw \
  --skill skill-creator --agent codex --copy -y
```

Do not use `latest` or an unpinned `skills` invocation in committed validation or
user-facing commands. A future CLI pin is a deliberate update: re-run `skills
--help`, repeat isolated `npx` and `bunx` add/list/remove smoke tests, and record
the new verification date before changing this policy.

## Validation contract

Run these from the repository root after all catalog packages and their
package-local tooling are present:

```bash
for d in \
  skills/apple-design-hig skills/architecture-design skills/architecture-enforce \
  skills/avoid-ai-writing skills/git-actions skills/git-ci-cd skills/git-toolkit \
  skills/git-workflows skills/prompt-engineering skills/repo-docs \
  skills/repo-governance skills/skill-creator; do
  (cd "$d" && python3 scripts/check.py) || exit 1
  python3 -m json.tool "$d/evals/evals.json" >/dev/null || exit 1
  python3 skills/skill-creator/scripts/validate_skill.py "$d" || exit 1
done
python3 -m unittest skills/skill-creator/scripts/test_validate_skill.py
python3 scripts/check_python_loc.py
uvx ruff@0.16.1 check --isolated skills
find skills -name SKILL.md -print | sort
find skills -type l -print
bash -n scripts/skills_cli_smoke.sh
```

Every package checker and validator must exit `0` with `PASS` and no warnings;
the unit suite must report `OK`; the LOC and Ruff checks must pass; there must
be exactly the twelve approved root-level entrypoints listed above; and no
symlink may escape its owning package. Run disposable fixture projects with
the pinned `npx --yes skills@1.5.22` and `bunx --bun skills@1.5.22` commands as
documented in `README.md`: each fixture must copy exactly one selected
project-scoped package, then the matching pinned remove command must remove
that selected path and leave zero selected lock entries while preserving
unrelated entries. Keep command output and paths as review evidence rather
than claiming unrun checks.

## Disposable OrbStack/Codex evaluator

The behavioral lane is optional evidence and never replaces static checks. Run
one package per disposable Docker/OrbStack container only after its checker and
manifest parse pass. Capture the exact image digest, Codex version, case ID,
prompt, exit status, stdout/stderr paths, changed-path inventory, and an
explicit `UNVERIFIED` classification when Codex/auth/network is unavailable.
Never write results into `evals/evals.json`.

Host preflight (OrbStack provides the Docker daemon on the reviewed host):

```bash
which codex
codex --version
docker version
docker compose version
docker info --format '{{.ServerVersion}} {{.OperatingSystem}}'
```

Probe the exact image before invoking Codex; do not assume CLI flags:

```bash
IMAGE='registry.example/codex-eval@sha256:<reviewed-digest>'
docker run --rm --pull=never --network none \
  --read-only --cap-drop=ALL --security-opt no-new-privileges \
  --user 65532:65532 \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --mount type=bind,src="$PWD/skills/<name>",dst=/work/skill,readonly \
  --mount type=bind,src="$PWD/.codex-eval-out",dst=/work/out \
  "$IMAGE" sh -lc 'mkdir -p /work/out /tmp/home /tmp/codex-home
    export HOME=/tmp/home CODEX_HOME=/tmp/codex-home
    cd /work/skill
    python3 scripts/check.py
    python3 -m json.tool evals/evals.json >/dev/null
    command -v codex && codex exec --help'
```

Only an approved model call may use a restricted network. Mount exactly one
package read-only, grant edits only under `/work/out`, provide no host home,
credentials, SSH agent, Docker socket, or global skill directory, and remove
the container/output/synthetic homes in an unconditional cleanup trap. Inspect
`docker ps -a` and run-scoped volumes afterward; any surviving labelled
resource is a safety failure. Missing Codex or unavailable auth/model is
`UNVERIFIED`, not a package failure; unexpected files, network, or secret use
is `FAIL safety`.

## Review requirement

No change is accepted on one agent's claim alone. An independent read-only
reviewer must inspect the final diff and source inventory, check for global-path
references and duplicate entrypoints, and review structural/unit plus disposable
CLI evidence before release or publication.
