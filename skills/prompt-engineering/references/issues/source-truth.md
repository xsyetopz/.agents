# Source Truth Cases

**Category:** `source-truth`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="example-source-version-overwrite"></a>

## example-source-version-overwrite

**ID**: `example-source-version-overwrite` | **Category**: `source-truth`

### Trigger

Use when: the agent treats a version, dependency ref, standard, config value, or generated setting from an example repository as authority to overwrite current local state.

### Observed failure

- ❌ `Changing 1.26.4 to 1.26.3 because an example repo has 1.26.3.`
- ❌ `Treating a sample go.mod, package lock, action ref, model name, or compiler standard as the current desired value.`
- ❌ `Editing generated output without checking the generator owner.`
- ❌ `Downgrading a local value while investigating coverage.`

### Required behavior

```text
Before changing a version-like value, identify whether the source is authoritative, illustrative, stale, generated, user-authored,
```

### Example

- A template repo uses an older language version and the agent copies it over a newer generated value.

**✅ CORRECT** (shortest path):

```text
Before changing a version-like value, identify whether the source is authoritative, illustrative, stale, generated, user-authored,
```

### Acceptance check

Every version/config change is backed by a stated authority trace: source value, current local value, owner, consumer, reach, and reason the change is authorized. Conflicts are reported rather than edited.

<a id="fake-authority-artifact-persistence"></a>

## fake-authority-artifact-persistence

**ID**: `fake-authority-artifact-persistence` | **Category**: `source-truth`

### Trigger

Fake Authority Artifact Persistence

### Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

### Required behavior

```text
Stop after the first correction when the artifact class is unclear.
Inspect existing `_stored` material and real external sources before creating authority artifacts.
Do not create a spec, schema, standard, matrix, benchmark, ADR, migration guide, or API contract unless its source basis is an act
If no real source exists, record that absence in docs or plans, not in the authority directory.
Prefer "missing source" or "not yet specified" over filling the gap with plausible structure.
```

### Example

Fake Authority Artifact Persistence

**✅ CORRECT** (shortest path):

```text
Stop after the first correction when the artifact class is unclear.
Inspect existing `_stored` material and real external sources before creating authority artifacts.
Do not create a spec, schema, standard, matrix, benchmark, ADR, migration guide, or API contract unless its source basis is an act
```

### Acceptance check

- Fake authority artifacts are removed. - Remaining authority artifacts either come from real existing sources or are explicitly requested local definitions. - Any new authority artifact cites its concrete source path, external URL, runtime command, or explicit user approval.

<a id="source-truth-misplacement"></a>

## source-truth-misplacement

**ID**: `source-truth-misplacement` | **Category**: `source-truth`

### Trigger

Use when: the agent frames wrappers, generated output directories, top-level convenience roots, or scripts as source-of-truth instead of keeping source authority in the user-designated source tree.

### Observed failure

- ❌ Treating `scripts/` as installer source authority because an installer command exists.
- ❌ Treating `plugins/`, `skills/`, or `prompts/` as authoring roots while also claiming `src/` is the source of truth.
- ❌ `Treating generated output roots as maintained source.`
- ❌ `"The source belongs wherever the file is emitted."`

### Required behavior

```text
When proposing a tree, the agent must mark each root as one of: 1. source authority, 2. implementation source, 3. generated output
```

### Example

- The agent proposed a PowerShell installer under `scripts/` and then had to be corrected that no one said a `.ps1` script there would be source-of-truth.

**✅ CORRECT** (shortest path):

```text
When proposing a tree, the agent must mark each root as one of: 1. source authority, 2. implementation source, 3. generated output
```

### Acceptance check

The proposed tree states which roots are source-authoritative and which are wrappers or output, and no generated or wrapper root is described as owning product truth without explicit authority.

<a id="stale-product-boundary-as-scope-brake"></a>

## stale-product-boundary-as-scope-brake

**ID**: `stale-product-boundary-as-scope-brake` | **Category**: `source-truth`

### Trigger

Use when: the agent treats an outdated product boundary as authority to reject or narrow the user's clarified product direction.

### Observed failure

- ❌ `"That would be scope creep."`
- ❌ `"The product only allows the current generated file."`
- ❌ "We cannot add hooks/templates because `PRODUCT.md` says no."
- ❌ `"Current implementation is the product boundary."`

### Required behavior

```text
When the user clarifies product direction that conflicts with `PRODUCT.md`, the agent must: 1. Treat the user clarification as cur
```

### Example

- The agent said additional generated templates or hooks would be scope creep because `PRODUCT.md` currently said the only generated file was `.codex/config.toml`.

**✅ CORRECT** (shortest path):

```text
When the user clarifies product direction that conflicts with `PRODUCT.md`, the agent must: 1. Treat the user clarification as cur
```

### Acceptance check

The agent updates the product boundary to separate current generated output from intended product direction, and any final answer names unimplemented surfaces as pending implementation rather than rejected scope.

<a id="unverified-example-claims"></a>

## unverified-example-claims

**ID**: `unverified-example-claims` | **Category**: `source-truth`

### Trigger

Use when: the agent changes examples, versions, model names, config keys, or dependency refs based on familiarity instead of verification.

### Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

### Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

### Example

#### Familiar Version Substitution ```diff - The agent changes an example from actions/checkout@v7 to actions/checkout@v4 because v4 feels real

**✅ CORRECT** (shortest path):

```text
1. Read relevant file(s) (1 call).
2. Verify references (1 Grep call).
3. State facts, then propose.
```

### Acceptance check

The observable response avoids the trigger pattern and exhibits the required behavior shown by the example.

## References

- [Issue corpus index](../issue-corpus-index.md)
- [Official source records](../official-sources.md)
