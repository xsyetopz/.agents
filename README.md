# my-agent-skills-btw

A standalone, reviewable distribution for a selected catalog of twelve portable
Agent Skills. It retains the maintained authoring skill at
**skills/skill-creator/** and includes eleven user-maintained, non-gitignored
packages imported from the reviewed source worktree. Install any one named
package into a project-scoped **.agents/skills** directory without editing a
personal **~/.agents/** checkout, then remove that package when the project no
longer needs it.

The repository is intentionally self-contained after copy: the installed skill
does not read a validator, reference, or prompt from this repository or from a
global path.

## Outcome and topology

The source hierarchy is a catalog. Every package has exactly one root-level
**SKILL.md** entrypoint and the same required, copyable contract:

~~~text
my-agent-skills-btw/
├── skills/
│   ├── apple-design-hig/               # imported user-maintained package
│   ├── architecture-design/
│   ├── architecture-enforce/
│   ├── avoid-ai-writing/
│   ├── git-actions/
│   ├── git-ci-cd/
│   ├── git-toolkit/
│   ├── git-workflows/
│   ├── prompt-engineering/              # prompt/model guidance owner
│   ├── repo-docs/
│   ├── repo-governance/
│   └── skill-creator/                   # maintained destination package
│       ├── SKILL.md                    # exact common entrypoint headings
│       ├── LICENSE                     # package license
│       ├── .skill-validator.json       # package validation configuration
│       ├── agents/openai.yaml          # required OpenAI surface metadata
│       ├── references/                 # routed guidance, specs, examples
│       ├── assets/contract.json        # required package contract
│       ├── evals/evals.json            # required static/Codex cases
│       └── scripts/check.py            # required copied-package checker
├── scripts/check_python_loc.py         # <=500-line authored Python gate
├── scripts/skills_cli_smoke.sh         # disposable npx/bunx contract probe
├── AGENTS.md                           # repository policy, not a skill
└── README.md
~~~

This is the install/data-flow boundary:

~~~mermaid
flowchart LR
    S["Reviewed checkout or canonical source"] --> C["skills@1.5.22"]
    C -->|add --skill selected-name --agent codex --copy| P["target/.agents/skills/selected-name"]
    P --> D["Codex discovers name + description"]
    D --> I["SKILL.md instructions"]
    I --> R["references/ or scripts/ only when routed"]
    C --> L["target/skills-lock.json"]
    P -->|remove after shared-agent check| X["directory absent"]
    X --> V["selected list row absent; neighbors remain"]
    L --> K["lock is inspected separately: empty, stale, or absent"]
~~~

A copied skill is a regular directory, not a symlink. The graph separates
filesystem/list evidence from generated lock metadata so a stale lock entry
cannot be mistaken for an active installation. The CLI examples below select
the maintained `skill-creator`; substitute any package in the catalog when the
task calls for another skill.

### Catalog selection boundary

The eleven imported packages are the non-gitignored roots from the reviewed
`/Users/krystian/.agents/skills/` worktree. The old source
`skill-creator` is excluded because this checkout maintains its own destination
copy. Source-gitignored roots are also excluded:
`design-taste-frontend`, `dry-refactoring`, `find-skills`,
`full-output-enforcement`, `gpt-taste`, `high-end-visual-design`, `impeccable`,
`install-skizzles`, `jscpd`, `redesign-existing-projects`, `swiftui-pro`,
`threejs-to-easeljs`, and `using-easeljs`. Ignored caches such as
`__pycache__/` and `.ruff_cache/` are omitted even when nested under an included
root. Every copied package keeps exactly one root-level **SKILL.md** and is
self-contained; no source checkout path, global path, or escaping symlink is a
runtime dependency.

## Common package contract

The open Agent Skills format is small, but this distribution deliberately
requires a stronger package contract so a copied directory is independently
checkable. Every `skills/<name>/` package must contain:

```text
SKILL.md
LICENSE
.skill-validator.json
agents/openai.yaml
references/                 # at least one package-relative routed file
assets/contract.json        # required even without other assets
evals/evals.json            # static and Codex case manifest
scripts/check.py            # stdlib-only copied-package checker
```

Additional assets are allowed only when the skill uses them; do not create an
empty or fake asset. The checker must run from the copied package without this
checkout, `/Users/krystian/.agents`, a global skill directory, network access,
or third-party dependencies. It rejects escaping symlinks, host/global paths,
absolute links, nested entrypoints, and out-of-package references. Static
success proves package shape only, not activation quality or security.

### Entrypoint and progressive disclosure

`SKILL.md` starts with valid two-field frontmatter, has a directory-matching
`name` and concrete selection-facing `description`, and uses these exact level-
two headings in order:

```text
When to use
When NOT to use
Guardrails
Workflow
Quick start
Reference map
Completion
Validation
Related skills
```

Keep the entrypoint concise. `Workflow` is the ordered core behavior, `Quick
start` is the smallest executable path, `Reference map` routes only the needed
local file by trigger, and detailed procedures stay one link hop away. Do not
load every reference by default or duplicate policy between sections.

`agents/openai.yaml` retains `interface.display_name`,
`interface.short_description`, and `interface.default_prompt`; the prompt must
invoke exactly `$<name>`. `assets/contract.json` records the common headings,
required files, routed references, and eval IDs.

### Evaluation manifest

`evals/evals.json` uses schema version 1 with exactly these top-level fields:

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

Each manifest has a positive, substantive near-miss, and relevant
boundary/safety/failure case. Case objects contain only `id`, `prompt`, and
`expected_outcome`; never commit results, scores, timings, or model traces.

All authored Python files under `skills/`, including tests, are at most **500
physical lines**. There is no generated/vendor exemption. The repository gate
is `python3 scripts/check_python_loc.py`.

OpenAI describes skills as folders with a **SKILL.md** and bundled resources,
and recommends a selection-facing description with detailed procedure in the
body: [Skills concept](https://developers.openai.com/plugins/concepts/skills)
and [Build skills](https://developers.openai.com/plugins/build/skills).

## Install

The commands below are project-scoped and intentionally pinned to the Vercel
Skills CLI release verified on **2026-08-13** with Node 26.6.0 / npm 12.0.2 and
Bun 1.3.14. This date records an observed contract; it is not a promise that
the pin is permanent. Re-probe help and rerun both launchers before changing
it.

Before changing the pin, capture the launcher and removal contracts again:

~~~bash
npx -y skills@1.5.22 --help
npx -y skills@1.5.22 remove --help
bunx --bun skills@1.5.22 --help
~~~

The repository does not invent a GitHub owner or remote URL. Set **SOURCE** to
a reviewed local checkout, or to the real canonical URL once one is published,
then run the commands from a disposable Git-backed target project. The catalog
names accepted by `--skill` are:

~~~text
apple-design-hig       architecture-design    architecture-enforce
avoid-ai-writing       git-actions            git-ci-cd
git-toolkit            git-workflows          prompt-engineering
repo-docs              repo-governance        skill-creator
~~~

The concrete commands below select the maintained `skill-creator`; replace that
name consistently in add, verification, and remove commands to exercise another
catalog package:

~~~bash
export SOURCE="/absolute/path/to/checked-out/my-agent-skills-btw"
cd "/absolute/path/to/target-project"

# Read-only discovery: exactly the named skill.
npx -y skills@1.5.22 add "$SOURCE" \
  --list --skill skill-creator --agent codex -y

# Copy exactly one skill into .agents/skills; no source-link behavior.
npx -y skills@1.5.22 add "$SOURCE" \
  --skill skill-creator --agent codex --copy -y

# Machine-readable project inventory (ANSI-free JSON).
npx -y skills@1.5.22 list --agent codex --json
~~~

The equivalent Bun launcher uses the verified **--bun** prefix:

~~~bash
# SOURCE and target project are the same variables as above.
bunx --bun skills@1.5.22 add "$SOURCE" \
  --list --skill skill-creator --agent codex -y

bunx --bun skills@1.5.22 add "$SOURCE" \
  --skill skill-creator --agent codex --copy -y

bunx --bun skills@1.5.22 list --agent codex --json
~~~

After a successful add, verify all of the following before using the skill:

~~~bash
test -f .agents/skills/skill-creator/SKILL.md
test ! -L .agents/skills/skill-creator
npx -y skills@1.5.22 list --agent codex --json
~~~

The list JSON should contain a project-scoped row named **skill-creator**;
other pre-existing rows are allowed and must not be changed. The copied
directory should contain the full package-local resource set; do not assume
that a source-tree validator proves the copied package is complete.

## Remove one skill safely

The 1.5.22 CLI has a critical shared-target edge case: **--agent codex**
alone can exit successfully while leaving the copied directory because the
same **.agents/skills** target is shared by other detected agents. The help
text mentions a wildcard, but the literal wildcard was rejected in the verified
probe. Do not use either shortcut.

First inspect the unfiltered project inventory and enumerate every display name
listed for the selected path:

~~~bash
npx -y skills@1.5.22 list --json
~~~

For the verified 1.5.22 target, the explicit removal command is:

~~~bash
npx -y skills@1.5.22 remove --skill skill-creator \
  --agent codex cursor github-copilot kimi-code-cli zed -y

# Bun equivalent:
bunx --bun skills@1.5.22 remove --skill skill-creator \
  --agent codex cursor github-copilot kimi-code-cli zed -y
~~~

Those agent IDs are observed for this CLI release and layout, not a
cross-version constant. If **list --json** reports a different shared set,
stop and adapt the explicit list after review; never broaden the command to
an unbounded selector.

Verify removal by filesystem, list, and lock observations:

~~~bash
test ! -e .agents/skills/skill-creator
npx -y skills@1.5.22 list --agent codex --json  # selected row absent; neighbors allowed
npx -y skills@1.5.22 list --json              # selected row absent; neighbors remain
~~~

Filter the JSON by the selected name and path; do not require the whole
inventory to be empty in a non-empty project:

~~~bash
npx -y skills@1.5.22 list --agent codex --json > /tmp/skills-after-remove.json
python3 - /tmp/skills-after-remove.json <<'PY'
import json
import sys

rows = json.load(open(sys.argv[1], encoding="utf-8"))
assert all(
    row.get("name") != "skill-creator"
    and not row.get("path", "").endswith("/.agents/skills/skill-creator")
    for row in rows
), rows
PY
~~~

Unrelated rows are expected and should be compared with their pre-removal
snapshot. An empty-list expectation is valid only when the fixture explicitly
began with exactly one installed skill.
The repository smoke fixture intentionally begins with an unrelated skill and
expects that row, directory, content digest, and lock entry to remain unchanged.

### Lockfile semantics

A project install creates **skills-lock.json** with a local source and computed
hash. It does not create a project **package-lock.json**, **bun.lock**, or
**bun.lockb** in the verified probes. Removal deletes the copied directory and
the list rows, but lock behavior is topology-sensitive: one verified fixture
left an empty **"skills": {}** map, while another retained a stale
**skill-creator** entry. Both are metadata states, not proof that the directory
is installed.

Treat the directory and **list --json** result as authoritative. For a
disposable non-empty smoke run, a matching-agent removal must leave zero
selected lock entries while preserving every unrelated entry unchanged;
the script fails closed if the selected key is stale, the unrelated key
changes, or the lock disappears. A single-skill fixture may instead classify
an empty or absent lock as clean. The smoke script never silently rewrites a
lockfile; do not commit the generated lock from its temporary fixture as
package source.

## Usage and prompt contract

Invoke the installed workflow explicitly in Codex with **$skill-creator**, or
let the host select it from the **name** and **description** metadata:

~~~text
$skill-creator Create or revise one portable skill for <goal>. Inspect the
target tree first, keep SKILL.md lean, route only the needed reference, run
the package validator and focused tests, and report paths, exit statuses,
source URLs, and any unverified evidence. Do not add wrappers, global paths,
secrets, egress, or compatibility aliases.
~~~

The `skill-creator` entrypoint is model-neutral. Its six-part authoring contract
— **Outcome, Authority, Tools, Evidence, Completion, Failure** — keeps required
output and safety rules in **SKILL.md**, routes variant detail to one reference,
and separates structural checks from behavioral evaluation. It does not require
GPT-5.6 or any other named model for ordinary skill creation.

Prompt design and audits, tool-routing policy, behavioral evals, and all
model-family guidance belong to **$prompt-engineering**. GPT-5.6 is one family
among many; use its guidance only when a task names that family or requires
model-specific evidence. Keep official source snapshots there, downloaded as
Markdown from the OpenAI Developer Docs rather than paraphrased in
`skill-creator`: [generic prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering.md)
and [GPT-5.6 family prompting guidance](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md).
The imported package records the downloaded bytes and provenance under
`skills/prompt-engineering/references/official/` and
`skills/prompt-engineering/references/official-sources.md`.
Use **$openai-docs** to refresh a named-model snapshot; do not freeze model IDs,
limits, pricing, or feature availability from memory. Keeping these pages out of
`skill-creator` prevents named-model context from loading for unrelated authoring
requests and avoids duplicate prompt authority.

## GREEN / RED examples

The labels below describe behavior and rationale; they are not a substitute for
running the checks.

### GREEN — scoped, reviewable installation

~~~text
Pinned skills@1.5.22 + one named skill + project Codex target + --copy +
non-interactive confirmation + post-install list/filesystem checks.
~~~

**Why:** The source, version, skill name, destination, and copy semantics are
explicit. The result can be inspected before activation.

### GREEN — evidence-backed removal

~~~text
Inspect list --json, enumerate the agents sharing the selected path, remove
the named skill, then assert the selected path/name absent, unrelated rows and
files unchanged, and lock state classified.
~~~

**Why:** A successful process exit is not enough when an agent directory is
shared. Independent observations catch a no-op removal and stale metadata.

### RED — broad or moving installation

~~~text
An install that omits the exact CLI pin, selects every discovered skill, or
trusts a moving branch without recording a reviewed revision.
~~~

**Why:** It makes the source set, bytes, and behavior change without an
explicit review boundary. Popularity, a previous scan, or a lock hash alone
does not establish intent or safety.

### RED — Codex-only removal assumption

~~~text
remove --skill skill-creator --agent codex -y
~~~

**Why:** In the verified 1.5.22 shared-target probe this exited 0 while the
directory remained. Enumerate the actual sharing agents, then verify path,
list, and lock state.

## Local validation and smoke test

Run package-local checks and repository gates from the repository root:

~~~bash
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
~~~

Every package checker and validator must print `PASS` and exit `0`; the unit
suite must print `OK`; the LOC and Ruff gates must pass; the inventory must
contain exactly these twelve root-level entrypoints:

~~~text
skills/apple-design-hig/SKILL.md
skills/architecture-design/SKILL.md
skills/architecture-enforce/SKILL.md
skills/avoid-ai-writing/SKILL.md
skills/git-actions/SKILL.md
skills/git-ci-cd/SKILL.md
skills/git-toolkit/SKILL.md
skills/git-workflows/SKILL.md
skills/prompt-engineering/SKILL.md
skills/repo-docs/SKILL.md
skills/repo-governance/SKILL.md
skills/skill-creator/SKILL.md
~~~

Every package must be self-contained and free of escaping symlinks or global
checkout paths. Structural validation proves shape and relative references; it
does not prove activation quality or supply-chain safety.

### Disposable OrbStack/Codex evaluation

Behavioral evaluation is a separate, disposable lane. Static checks and
manifest parsing must pass before a Codex case runs. Record the image digest,
Codex version, exact case ID and prompt, exit status, stdout/stderr paths,
changed-path inventory, and `UNVERIFIED` cases outside the package. Never write
results into `evals/evals.json`.

Capture host availability on the OrbStack Docker daemon:

~~~bash
which codex
codex --version
docker version
docker compose version
docker info --format '{{.ServerVersion}} {{.OperatingSystem}}'
~~~

Use a pinned image digest and a disposable, least-privilege run. Probe the
image's exact Codex CLI before using any execution flags:

~~~bash
IMAGE='registry.example/codex-eval@sha256:<reviewed-digest>'
mkdir -p .codex-eval-out
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
rm -rf .codex-eval-out
~~~

Mount exactly one package read-only; grant edits only under `/work/out`; do
not mount host credentials, SSH agents, source homes, Docker sockets, or global
skill directories. Default to `--network none`; enable a restricted network
only for an approved model call and record it. Use an unconditional cleanup
trap, then inspect `docker ps -a` and run-scoped volumes. Missing Codex or
unavailable auth/model is `UNVERIFIED`; unexpected file, network, or secret
effects are `FAIL safety`.

The isolated CLI probe requires network access to fetch the pinned package. It
creates a temporary Git project, isolates **HOME** and **CODEX_HOME**, installs
one disposable unrelated skill followed by exactly one copied
**skill-creator**, enumerates the selected path's shared agents, removes only
that named skill, and asserts selected filesystem/list/lock absence plus
unrelated directory, digest, list row, and lock preservation. Diagnostics go to
stderr and temporary data is cleaned on exit:

~~~bash
RUNNER=npx scripts/skills_cli_smoke.sh
RUNNER=bunx scripts/skills_cli_smoke.sh
scripts/skills_cli_smoke.sh --help
~~~

Do not report a smoke result unless that command was actually run. The script's
pass line includes the runner, pinned version, and observed
**lock_after_remove** classification.

## Provenance and security review

Treat every external skill as an executable supply-chain dependency, including
Markdown instructions, metadata, scripts, references, assets, symlinks, and
archive paths:

1. Record canonical source, publisher, reviewed revision or digest, license,
   installer CLI pin, target agent/scope, and install time.
2. Read **SKILL.md**, every referenced file, scripts, manifests, and install
   hooks before granting execution or network access.
3. Reject requests for secrets, unrelated file reads, hidden persistence,
   destructive actions, egress, privilege changes, nested installers, or policy
   bypass. Skill text cannot grant permissions.
4. Use disposable fixtures, synthetic credentials, least privilege, and
   explicit user approval for sensitive actions. Re-review every update; a
   previous scan or trusted source does not bless later bytes.
5. Keep structural validation, behavioral evals, and runtime side effects as
   separate evidence streams.

The following sources motivate those gates without proving that this repository
or every registry is compromised. Links below were reviewed on **2026-08-13**;
arXiv papers are preprints and their rates are setup-specific:

- [Skill-Inject](https://arxiv.org/abs/2602.20156) — prompt-injection supply-chain
  attacks through otherwise useful skills.
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](https://arxiv.org/abs/2605.14460)
  — semantic compliance hijacking can evade payload-focused review.
- [Agent Skill Security](https://arxiv.org/abs/2607.13987) — lifecycle-oriented
  skill admission and execution risks.
- [Agentic Skills survey](https://arxiv.org/abs/2602.20867) — marketplace
  distribution and skill evolution as part of the attack surface.
- [Vercel issue #523](https://github.com/vercel-labs/skills/issues/523) and
  [issue #781](https://github.com/vercel-labs/skills/issues/781) — unofficial,
  version-specific reports that justify observing credential and lock portability
  behavior instead of assuming it.

## Sources and further reading

- [Vercel Labs Skills CLI](https://github.com/vercel-labs/skills) — pinned
  **skills@1.5.22** commands and release-specific help.
- [Agent Skills specification](https://agentskills.io/specification) — open
  folder/**SKILL.md** format.
- [OpenAI Skills concept](https://developers.openai.com/plugins/concepts/skills)
  and [Build skills](https://developers.openai.com/plugins/build/skills) —
  workflow boundaries and bundled resources.
- [OpenAI Codex repository](https://github.com/openai/codex) — current
  implementation context for Codex integrations.
- [OpenAI prompt engineering Markdown](https://developers.openai.com/api/docs/guides/prompt-engineering.md)
  and [GPT-5.6 family prompting Markdown](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md)
  — official page downloads owned by **$prompt-engineering**; refresh through
  **$openai-docs** before model-specific edits.

## Contributing

Keep changes within the catalog boundary, run the documented validation, and
request the independent review required by [AGENTS.md](AGENTS.md).

## License

MIT; see [LICENSE](LICENSE). Catalog packages retain any standalone license
copies supplied with their package, including
[skills/skill-creator/LICENSE](skills/skill-creator/LICENSE).
