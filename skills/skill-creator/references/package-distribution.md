# Package distribution

## Contents

- [Pin and select one skill](#pin-and-select-one-skill)
- [Verify the copy](#verify-the-copy)
- [Removal: version and topology](#removal-version-and-topology)
- [Source and provenance gates](#source-and-provenance-gates)
- [Evidence table](#evidence-table)

## Pin and select one skill

The verified release is `skills@1.5.22` (Node `v26.6.0`, `bunx 12.0.2`, Bun
`1.3.14`, macOS; accessed 2026-08-13). Pin the version, pass the repository or
local source explicitly, select `skill-creator` explicitly, target `codex`, and
copy rather than relying on source-link behavior.

<!-- GREEN: one named skill, pinned version, project-scoped copy -->
```bash
bunx --yes skills@1.5.22 add <owner>/my-agent-skills-btw \
  --skill skill-creator --agent codex --copy -y

bunx --yes skills@1.5.22 add <owner>/my-agent-skills-btw \
  --skill skill-creator --agent codex --copy -y
```

`--list` is a read-only discovery probe and should precede an install when the
source is unfamiliar:

```bash
bunx --yes skills@1.5.22 add <owner>/my-agent-skills-btw \
  --list --skill skill-creator --agent codex -y
```

The CLI's accepted options and source behavior are release-specific. Run
`bunx --yes skills@1.5.22 --help` and
`bunx --yes skills@1.5.22 remove --help` before automating a new pin. Do not
substitute `latest` in reproducible documentation.

Both `bunx --yes skills@1.5.22` (used above) and the Bun launcher form
`bunx --bun skills@1.5.22` resolved the same pinned release in the 2026-08-13
probe; keep one form consistent within a smoke-test script.

## Verify the copy

From a disposable Git-backed project, run:

```bash
bunx --yes skills@1.5.22 list --agent codex --json
test -f .agents/skills/skill-creator/SKILL.md
test ! -L .agents/skills/skill-creator
```

Assert that the JSON reports exactly one project-scoped `skill-creator`, the
directory is a regular copied directory, and the copied package's relative
references resolve. Keep the generated `skills-lock.json` in the fixture while
testing; it is evidence, not a package resource.

## Removal: version and topology

The CLI can report success while leaving a skill in a shared `.agents` target
when only `--agent codex` is supplied. In the 1.5.22 contract probe, the narrow
deletion was:

```bash
bunx --yes skills@1.5.22 remove --skill skill-creator \
  --agent codex cursor github-copilot kimi-code-cli zed -y
```

Use the equivalent `bunx --yes skills@1.5.22` prefix when testing Bun. The
agent list is observed behavior for this release and target layout, not a
portable constant: inspect the pinned `bunx --yes skills@1.5.22 list --json`,
enumerate the agents that share the target, and adapt only after review. Never pass the literal wildcard
`--agent '*'`; 1.5.22 rejects it even though help text describes a wildcard.
Do not use `--all` in a non-empty project: it can remove unrelated skills.

After any removal—regardless of exit code—verify both filesystem and metadata:

```bash
test ! -e .agents/skills/skill-creator
bunx --yes skills@1.5.22 list --agent codex --json
python3 - <<'PY'
import json
from pathlib import Path

lock = Path("skills-lock.json")
data = json.loads(lock.read_text()) if lock.exists() else {"skills": {}}
assert "skill-creator" not in data.get("skills", {})
PY
```

An empty `skills-lock.json` is expected; deletion of the lockfile is not a
requirement. A zero exit code without the filesystem/list/lock assertions is
not removal evidence.

<!-- RED: broad selection or unverifiable removal -->
Unsafe command shapes (not runnable examples):

- unpinned CLI plus `add <owner>/my-agent-skills-btw --all` selects unintended
  skills;
- interactive `remove` is not reproducible; and
- even the pinned `remove skill-creator --agent codex -y` form can silently
  leave a shared-target copy.

The labels describe behavior; color alone is not a security or correctness
signal.

## Source and provenance gates

Before installing an external source, record its canonical URL, publisher,
reviewed commit or release, CLI version, target agent/scope, and install time.
Inspect `SKILL.md`, every referenced file, scripts, manifests, symlinks, and
archive paths first. A moving branch, marketplace popularity, prior scan, or
lock hash is not proof of intent or safety. Run smoke tests in an isolated
fixture with synthetic credentials and no production egress.

## Evidence table

| Claim | Evidence and date | Boundary |
| --- | --- | --- |
| Pin `skills@1.5.22`; `--skill`, `--agent`, and `--copy` are accepted | [Vercel Labs `skills` CLI](https://github.com/vercel-labs/skills) help and disposable npm/Bun probes, accessed 2026-08-13 | Re-probe when changing the pin or source type. |
| Project install targets `./.agents/skills` and writes a lock | Pinned local-source install trace, accessed 2026-08-13 | Global discovery can include unrelated paths; this guide is project scope only. |
| Codex-only removal can leave a shared-target copy; enumerating agents removed it in the probe | Pinned CLI contract probe, accessed 2026-08-13 | Agent names and behavior may change; always verify path, list JSON, and lock. |
| Historical credential/hash portability reports merit extra review | [Vercel issue #523](https://github.com/vercel-labs/skills/issues/523) and [#781](https://github.com/vercel-labs/skills/issues/781), accessed 2026-08-13 | User reports are version-/platform-scoped, not current-version guarantees. |
| Skills are a supply-chain surface | [Skill-Inject](https://arxiv.org/abs/2602.20156), preprint accessed 2026-08-13 | Threat categories motivate review; paper rates are not this package's test result. |
