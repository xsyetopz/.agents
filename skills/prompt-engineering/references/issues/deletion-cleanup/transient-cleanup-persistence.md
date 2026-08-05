# Transient Cleanup Persistence

**ID**: `transient-cleanup-persistence` | **Category**: `deletion-cleanup`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent tries to preserve one-off cleanup for an accidental artifact as product, startup, migration, test, hook, or shared runtime code.

## Observed failure

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

## Example

- A generated file should not exist. The agent adds a cleanup step to delete it on every run instead of fixing the generator, manifest, ignore rule, or installer ownership path.

**✅ CORRECT** (shortest path):

```text
First decide whether the artifact is accidental state or a real compatibility/migration case.
If it is accidental state, remove the bad artifact and the code path that creates, bundles, installs, or references it.
Do not add permanent cleanup code, startup deletion, tests for the deletion helper, hooks, or CI cleaners for one-off mistakes.
```

## Acceptance check

- The final change removes the accidental artifact route instead of adding a persistent cleanup route. - No new runtime, startup, hook, CI, test, or installer code exists only to delete the one-off artifact. - Tests or smoke checks prove the bad artifact is not produced, bundled, installed, or referenced. - Final reports name the remaining invariant, not a cleanup helper.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
