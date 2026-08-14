# Deletion Cleanup Cases

**Category:** `deletion-cleanup`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="deletion-promise-after-borrowed-label"></a>

## deletion-promise-after-borrowed-label

**ID**: `deletion-promise-after-borrowed-label` | **Category**: `deletion-cleanup`

### Trigger

Use when: the agent borrows a user's artifact label, then promises removal before tracing behavior, callers, output, and ownership.

### Observed failure

- ❌ `"It is just a prose script."`
- ❌ `"Nobody needs this."`
- ❌ `"I will remove it and its references" before reading callers.`
- ❌ `Treating a typo, filename, complaint term, or nearby prose as a behavior trace.`
- ❌ `Replacing the artifact with another command that preserves the same unwanted wording gate.`

### Required behavior

```text
Before promising removal or replacement, identify:
observed behavior
direct callers
files written or changed
generated or installed surface
```

### Example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path):

```text
Before promising removal or replacement, identify:
observed behavior
direct callers
```

### Acceptance check

For any challenged artifact, the answer contains a behavior trace before an edit commitment, or explicitly states that no edit commitment is being made until that trace exists.

<a id="invariant-fixation-over-product-behavior"></a>

## invariant-fixation-over-product-behavior

**ID**: `invariant-fixation-over-product-behavior` | **Category**: `deletion-cleanup`

### Trigger

Use when: the agent treats one current literal or setting as the main product focus instead of a constraint inside the larger lifecycle behavior.

### Observed failure

- ❌ "`model = \"gpt-5.5\"` is the main thing."
- ❌ `"The product is done because the model value is correct."`
- ❌ `"Everything else is scope creep because the invariant is satisfied."`
- ❌ `"The generated config literal proves the install system."`
- ❌ "The goal is mostly to ensure `gpt-5.5` is in config."

### Required behavior

```text
When a current literal appears in product docs, the agent must: 1. Keep it out of goal and product-boundary wording unless the use
```

### Example

- The agent treated `model = "gpt-5.5"` as the primary focus when the user was asking why the work had not moved toward actual lifecycle scripts and generated-file ownership.

**✅ CORRECT** (shortest path):

```text
When a current literal appears in product docs, the agent must: 1. Keep it out of goal and product-boundary wording unless the use
```

### Acceptance check

The agent's product updates and final report treat the model setting as one invariant, and separately show evidence for lifecycle command behavior, ownership boundaries, generated files, and removal safety.

<a id="rejected-surface-normalization"></a>

## rejected-surface-normalization

**ID**: `rejected-surface-normalization` | **Category**: `deletion-cleanup`

### Trigger

Use when: the agent keeps rejected, removed, or unwanted surfaces alive as concepts, tests, docs, or proof language.

### Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

### Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

### Example

#### Retired Surface Kept As Concept ```diff - The test says retired docs must not be referenced

**✅ CORRECT** (shortest path):

```text
1. Read relevant file(s) (1 call).
2. Verify references (1 Grep call).
3. State facts, then propose.
```

### Acceptance check

The observable response avoids the trigger pattern and exhibits the required behavior shown by the example.

<a id="transient-cleanup-persistence"></a>

## transient-cleanup-persistence

**ID**: `transient-cleanup-persistence` | **Category**: `deletion-cleanup`

### Trigger

Use when: the agent tries to preserve one-off cleanup for an accidental artifact as product, startup, migration, test, hook, or shared runtime code.

### Observed failure

- ❌ `"I'll move the cleanup to the edge where the mess was created."`
- ❌ `"This is intentionally local cleanup."`
- ❌ `"The shortest fix is a private launch helper."`
- ❌ `Adding a deletion helper for a file that should never be produced.`
- ❌ `Adding tests that make permanent cleanup behavior look intentional.`
- ❌ `Treating narrower placement as enough after the user rejects the cleanup itself.`

### Required behavior

```text
First decide whether the artifact is accidental state or a real compatibility/migration case.
If it is accidental state, remove the bad artifact and the code path that creates, bundles, installs, or references it.
Do not add permanent cleanup code, startup deletion, tests for the deletion helper, hooks, or CI cleaners for one-off mistakes.
If cleanup must run once during the current work, keep it outside product/runtime code and do not commit the cleanup mechanism.
Preserve a cleanup path only when there is explicit source evidence for a recurring external state, an owner, a bounded removal po
```

### Example

- A generated file should not exist. The agent adds a cleanup step to delete it on every run instead of fixing the generator, manifest, ignore rule, or installer ownership path.

**✅ CORRECT** (shortest path):

```text
First decide whether the artifact is accidental state or a real compatibility/migration case.
If it is accidental state, remove the bad artifact and the code path that creates, bundles, installs, or references it.
Do not add permanent cleanup code, startup deletion, tests for the deletion helper, hooks, or CI cleaners for one-off mistakes.
```

### Acceptance check

- The final change removes the accidental artifact route instead of adding a persistent cleanup route. - No new runtime, startup, hook, CI, test, or installer code exists only to delete the one-off artifact. - Tests or smoke checks prove the bad artifact is not produced, bundled, installed, or referenced. - Final reports name the remaining invariant, not a cleanup helper.
