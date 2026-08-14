# Naming Invention Cases

**Category:** `naming-invention`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="agents-universal-surface-overstatement"></a>

## agents-universal-surface-overstatement

**ID**: `agents-universal-surface-overstatement` | **Category**: `naming-invention`

### Trigger

Use when: the agent turns `.agents/` compatibility into a claim that `.agents/` is the canonical source or root for every generated tool surface.

### Observed failure

- ❌ "`.agents/` is the canonical source of everything."
- ❌ "`.codex/` and `.claude/` are just projections."
- ❌ "The universal intent always flows from `.agents/`."
- ❌ "Generate everything under `.agents/` first."

### Required behavior

```text
When discussing `.agents/`, `.codex/`, and `.claude/`, the agent must: 1. State that `.agents/` is for universal-compatible hooks,
```

### Example

- The agent said `.agents/` is the universal source/runtime surface and `.codex/` and `.claude/` are generated projections.

**✅ CORRECT** (shortest path):

```text
When discussing `.agents/`, `.codex/`, and `.claude/`, the agent must: 1. State that `.agents/` is for universal-compatible hooks,
```

### Acceptance check

The agent describes placement per artifact class: universal-compatible hooks, skills, and scripts may live in `.agents/` or be symlinked with tool paths as required; tool-specific artifacts stay under their native tool surface.

<a id="artifact-naming-without-domain-contract"></a>

## artifact-naming-without-domain-contract

**ID**: `artifact-naming-without-domain-contract` | **Category**: `naming-invention`

### Trigger

Use when: the agent invents file, schema, command, or directory names before proving the artifact has a domain role, producer, consumer, and accepted source format.

### Observed failure

- ❌ `render-plan.schema.json`
- ❌ `external-tool.schema.json`
- ❌ `docs-provider.schema.json`
- ❌ `"schema for runtime things"`
- ❌ `"schema for shared tools"`
- ❌ `Naming files from broad nouns such as provider, runtime, plan, catalog, or manifest without a concrete contract.`

### Required behavior

```text
Before naming a schema, command, config file, manifest, or generated artifact, the agent must identify: 1. the exact source artifa
```

### Example

- The agent proposed `render-plan.schema.json` after the user asked for dry-run generated artifacts, even though the user had not named a render-plan concept.

**✅ CORRECT** (shortest path):

```text
Before naming a schema, command, config file, manifest, or generated artifact, the agent must identify: 1. the exact source artifa
```

### Acceptance check

Every proposed artifact name can be traced to user wording, current repo source, upstream format, or an explicitly marked open proposal with producer and consumer named.

<a id="compatibility-surface-injection"></a>

## compatibility-surface-injection

**ID**: `compatibility-surface-injection` | **Category**: `naming-invention`

### Trigger

Use when: the agent adds compatibility wrappers, migration shims, aliases, fallback commands, or backward-compatible surfaces that the user did not ask for.

### Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

### Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

### Example

#### Compatibility Wrapper Without Request ```diff - The agent keeps the old entrypoint as a compatibility wrapper

**✅ CORRECT** (shortest path):

```text
1. Read relevant file(s) (1 call).
2. Verify references (1 Grep call).
3. State facts, then propose.
```

### Acceptance check

The observable response avoids the trigger pattern and exhibits the required behavior shown by the example.

<a id="entrypoint-and-wrapper-invention"></a>

## entrypoint-and-wrapper-invention

**ID**: `entrypoint-and-wrapper-invention` | **Category**: `naming-invention`

### Trigger

Use when: the agent adds extra scripts, wrappers, or command entrypoints because they are common in repositories rather than required by the product.

### Observed failure

- ❌ Adding `.sh` because repositories often have shell installers.
- ❌ Adding `render`, `verify`, or `eval` scripts because the verbs exist in the lifecycle.
- ❌ `Calling command proliferation "thin wrappers" as if that removes the maintenance cost.`
- ❌ `"Optional wrapper" without a concrete caller.`

### Required behavior

```text
Before proposing an entrypoint or wrapper, the agent must identify: 1. who calls it, 2. what runtime executes it, 3. why an existi
```

### Example

- The agent proposed both `install.ps1` and `install.sh` without a distribution requirement that could not run PowerShell.

**✅ CORRECT** (shortest path):

```text
Before proposing an entrypoint or wrapper, the agent must identify: 1. who calls it, 2. what runtime executes it, 3. why an existi
```

### Acceptance check

Every proposed script has a named caller, delegated source path, test route, and platform reason. Otherwise it is not included in the tree.

<a id="scratch-space-overdesign"></a>

## scratch-space-overdesign

**ID**: `scratch-space-overdesign` | **Category**: `naming-invention`

### Trigger

Use when: the agent predesigns internal layout for gitignored build or scratch directories without a real command lifecycle owning that layout.

### Observed failure

- ❌ `.build/previews/`
- ❌ `.build/targets/`
- ❌ `.build/eval-runs/`
- ❌ `"logs" as a proposed tree item without retention rules.`
- ❌ `Naming scratch children from lifecycle nouns before command behavior exists.`

### Required behavior

```text
For gitignored build or scratch directories, the agent must: 1. name the root only when the user or repo already accepts it, 2. av
```

### Example

- The agent proposed `.build/previews`, `.build/targets`, and `.build/eval-runs` without showing the commands that produce or consume those paths.

**✅ CORRECT** (shortest path):

```text
For gitignored build or scratch directories, the agent must: 1. name the root only when the user or repo already accepts it, 2. av
```

### Acceptance check

Every scratch subdirectory in a proposal has an owning command, producer, consumer, retention rule, and cleanup behavior. Otherwise only the scratch root is named.

<a id="spec-role-hallucination"></a>

## spec-role-hallucination

**ID**: `spec-role-hallucination` | **Category**: `naming-invention`

### Trigger

Spec Role Hallucination

### Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

### Required behavior

```text
Ask what "spec" means only if local evidence does not define it.
Prefer existing format specs, source-backed document contracts, or external schemas over invented product JSON.
Do not create a format spec until its source path, external URL, or explicit user approval is known.
Keep product decisions in `PRODUCT.md` and ADRs.
Keep completion state in `goals/`.
```

### Example

The user meant specs integrated from real existing format specifications or source-backed artifact contracts, not assistant-authored product ledgers or plausible local schema names.

**✅ CORRECT** (shortest path):

```text
Ask what "spec" means only if local evidence does not define it.
Prefer existing format specs, source-backed document contracts, or external schemas over invented product JSON.
Do not create a format spec until its source path, external URL, or explicit user approval is known.
```

### Acceptance check

- `specs/` contains real source-backed specs, not product-governance ledgers or plausible local schema names. - Runtime renderer does not require invented governance specs. - Verifier checks that specs exist and are valid JSON, but does not treat them as product authority unless a current ADR says so.

## References

- [Issue corpus index](../issue-corpus-index.md)
- [Official source records](../official-sources.md)
