# Documentation Orbit Over Product Work

**ID**: `documentation-orbit-over-product-work` | **Category**: `docs-orbit`

## Trigger

Use when: the agent keeps updating docs, evidence maps, stale wording, or issue records while the user expects product/runtime work.

## Bad forms — what this looks like

- ❌ `"I found more stale docs, so I am fixing those first."`
- ❌ `"The runtime still needs work, but the evidence trail is cleaner."`
- ❌ Treating `rg` hits in docs as the work queue for a product goal.
- ❌ `Reporting documentation edits as if they changed product behavior.`

## Required behavior

```text
When the active goal is product/runtime work, inspect the product path first: renderer, lifecycle command, manifest, removal, test
Edit docs only when they directly unblock the next product change or record evidence after behavior changed.
If stale docs are found during product work, note them briefly and continue unless they are blocking a product decision.
Report product artifacts changed and command evidence before documentation polish.
Stop documentation sweeps when the user challenges progress direction.
```

## Concrete example

- The user asks whether the agent is working on the product, and the recent work has been mostly stale wording fixes across docs.

**✅ CORRECT** (shortest path):

```text
When the active goal is product/runtime work, inspect the product path first: renderer, lifecycle command, manifest, removal, test
Edit docs only when they directly unblock the next product change or record evidence after behavior changed.
If stale docs are found during product work, note them briefly and continue unless they are blocking a product decision.
```

## Acceptance check

- Product turns change or verify product/runtime artifacts before optional docs. - Documentation-only turns happen only when explicitly requested or when no product edit is needed. - Final reports separate product behavior evidence from documentation consistency.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
