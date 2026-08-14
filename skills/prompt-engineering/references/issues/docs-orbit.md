# Docs Orbit Cases

**Category:** `docs-orbit`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="bare-renderer-snapshot-as-product-goal"></a>

## bare-renderer-snapshot-as-product-goal

**ID**: `bare-renderer-snapshot-as-product-goal` | **Category**: `docs-orbit`

### Trigger

Use when: the agent treats the current minimal renderer output as the intended product instead of a temporary lifecycle exercise.

### Observed failure

- ❌ "The product is just `.codex/config.toml`."
- ❌ `"No hooks, skills, MCP, or templates because the current renderer does not emit them."`
- ❌ `"The current minimal output is the product boundary."`
- ❌ `"Adding real generated files is scope creep."`

### Required behavior

```text
Describe the goal as a control plane for admitted generated surfaces.
Treat the current renderer output as smoke-test content, not destination scope.
Keep hooks, skills, MCP, instructions, templates, and related files in the admitted-surface backlog until implemented.
Require source routing, renderer support, manifest ownership, removal behavior, and dogfood evidence before each surface is genera
```

### Example

- Goal wording implied the current `.codex/config.toml` renderer snapshot was the product boundary.

**✅ CORRECT** (shortest path):

```text
Describe the goal as a control plane for admitted generated surfaces.
Treat the current renderer output as smoke-test content, not destination scope.
Keep hooks, skills, MCP, instructions, templates, and related files in the admitted-surface backlog until implemented.
```

### Acceptance check

Goal and product docs name the intended generated-surface framework and distinguish unimplemented admitted-surface backlog from rejected scope.

<a id="documentation-orbit-over-product-work"></a>

## documentation-orbit-over-product-work

**ID**: `documentation-orbit-over-product-work` | **Category**: `docs-orbit`

### Trigger

Use when: the agent keeps updating docs, evidence maps, stale wording, or issue records while the user expects product/runtime work.

### Observed failure

- ❌ `"I found more stale docs, so I am fixing those first."`
- ❌ `"The runtime still needs work, but the evidence trail is cleaner."`
- ❌ Treating `rg` hits in docs as the work queue for a product goal.
- ❌ `Reporting documentation edits as if they changed product behavior.`

### Required behavior

```text
When the active goal is product/runtime work, inspect the product path first: renderer, lifecycle command, manifest, removal, test
Edit docs only when they directly unblock the next product change or record evidence after behavior changed.
If stale docs are found during product work, note them briefly and continue unless they are blocking a product decision.
Report product artifacts changed and command evidence before documentation polish.
Stop documentation sweeps when the user challenges progress direction.
```

### Example

- The user asks whether the agent is working on the product, and the recent work has been mostly stale wording fixes across docs.

**✅ CORRECT** (shortest path):

```text
When the active goal is product/runtime work, inspect the product path first: renderer, lifecycle command, manifest, removal, test
Edit docs only when they directly unblock the next product change or record evidence after behavior changed.
If stale docs are found during product work, note them briefly and continue unless they are blocking a product decision.
```

### Acceptance check

- Product turns change or verify product/runtime artifacts before optional docs. - Documentation-only turns happen only when explicitly requested or when no product edit is needed. - Final reports separate product behavior evidence from documentation consistency.

<a id="harness-drift-over-product-structure"></a>

## harness-drift-over-product-structure

**ID**: `harness-drift-over-product-structure` | **Category**: `docs-orbit`

### Trigger

Use when: the agent keeps adding smoke cases, wrappers, or verification machinery while the product source and test structure remain thin or missing.

### Observed failure

- ❌ `"I will add one more smoke phase."`
- ❌ `"The smoke script proves this" when the product implementation is still just a thin script.`
- ❌ `Confessing drift with self-analysis instead of naming the current files, missing structure, and next product correction.`
- ❌ `Treating a harness pass as product architecture.`

### Required behavior

```text
Inspect current product source and test layout before adding more harness code.
Add a smoke case only when it proves a concrete product change made in the same turn.
If the product lacks source or test structure, address that structure directly instead of expanding smoke scripts.
When challenged about drift, answer the artifact-state question first and stop unless explicitly told to continue.
```

### Example

- The agent keeps adding lifecycle smoke cases instead of creating a real source and test structure.

**✅ CORRECT** (shortest path):

```text
Inspect current product source and test layout before adding more harness code.
Add a smoke case only when it proves a concrete product change made in the same turn.
If the product lacks source or test structure, address that structure directly instead of expanding smoke scripts.
```

### Acceptance check

- Product-progress turns touch product implementation or intentional test structure before adding broad harness coverage. - Smoke scripts remain small end-to-end checks, not the main place product behavior accumulates. - Reports distinguish product source, tests, smoke, and evidence instead of collapsing them into one proof bucket.

<a id="inline-command-prose-instead-of-scripts"></a>

## inline-command-prose-instead-of-scripts

**ID**: `inline-command-prose-instead-of-scripts` | **Category**: `docs-orbit`

### Trigger

Use when: the agent repeats inline smoke commands, transcript fragments, or prose command recipes instead of consolidating recurring product checks into runnable scripts.

### Observed failure

- ❌ `"Run this inline block again" for recurring lifecycle proof.`
- ❌ `A smoke evidence page made mostly of shell prose when the same behavior should be scripted.`
- ❌ `Updating copied command fragments instead of rerunning the owning script.`
- ❌ `Treating a pasted transcript as the durable verifier.`

### Required behavior

```text
When a command sequence becomes recurring evidence for lifecycle, generated output, ownership, or removal safety, the agent must:
```

### Example

- The agent described repeated smoke commands in documentation instead of first creating a durable lifecycle smoke script.

**✅ CORRECT** (shortest path):

```text
When a command sequence becomes recurring evidence for lifecycle, generated output, ownership, or removal safety, the agent must:
```

### Acceptance check

Recurring product checks are represented by runnable scripts under `scripts/`, and evidence docs point to the script command plus current observed output.
