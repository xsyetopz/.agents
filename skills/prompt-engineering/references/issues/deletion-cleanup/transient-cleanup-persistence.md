# Transient Cleanup Persistence

**ID**: `transient-cleanup-persistence` | **Category**: `deletion-cleanup`

## Trigger

Use when: the agent tries to preserve one-off cleanup for an accidental artifact as product, startup, migration, test, hook, or shared runtime code.

## Bad forms — what this looks like

- ❌ `"I'll move the cleanup to the edge where the mess was created."`
- ❌ `"This is intentionally local cleanup."`
- ❌ `"The shortest fix is a private launch helper."`
- ❌ `Adding a deletion helper for a file that should never be produced.`
- ❌ `Adding tests that make permanent cleanup behavior look intentional.`
- ❌ `Treating narrower placement as enough after the user rejects the cleanup itself.`

## Required behavior

```text
First decide whether the artifact is accidental state or a real compatibility/migration case.
If it is accidental state, remove the bad artifact and the code path that creates, bundles, installs, or references it.
Do not add permanent cleanup code, startup deletion, tests for the deletion helper, hooks, or CI cleaners for one-off mistakes.
If cleanup must run once during the current work, keep it outside product/runtime code and do not commit the cleanup mechanism.
Preserve a cleanup path only when there is explicit source evidence for a recurring external state, an owner, a bounded removal po
```

## Concrete example

- A generated file should not exist. The agent adds a cleanup step to delete it on every run instead of fixing the generator, manifest, ignore rule, or installer ownership path.

**✅ CORRECT** (shortest path):

```text
First decide whether the artifact is accidental state or a real compatibility/migration case.
If it is accidental state, remove the bad artifact and the code path that creates, bundles, installs, or references it.
Do not add permanent cleanup code, startup deletion, tests for the deletion helper, hooks, or CI cleaners for one-off mistakes.
```

## Acceptance check

- The final change removes the accidental artifact route instead of adding a persistent cleanup route. - No new runtime, startup, hook, CI, test, or installer code exists only to delete the one-off artifact. - Tests or smoke checks prove the bad artifact is not produced, bundled, installed, or referenced. - Final reports name the remaining invariant, not a cleanup helper.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
