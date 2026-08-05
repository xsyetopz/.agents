# Scratch Space Overdesign

**ID**: `scratch-space-overdesign` | **Category**: `naming-invention`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent predesigns internal layout for gitignored build or scratch directories without a real command lifecycle owning that layout.

## Observed failure

- ❌ `.build/previews/`
- ❌ `.build/targets/`
- ❌ `.build/eval-runs/`
- ❌ `"logs" as a proposed tree item without retention rules.`
- ❌ `Naming scratch children from lifecycle nouns before command behavior exists.`

## Required behavior

```text
For gitignored build or scratch directories, the agent must: 1. name the root only when the user or repo already accepts it, 2. av
```

## Example

- The agent proposed `.build/previews`, `.build/targets`, and `.build/eval-runs` without showing the commands that produce or consume those paths.

**✅ CORRECT** (shortest path):

```text
For gitignored build or scratch directories, the agent must: 1. name the root only when the user or repo already accepts it, 2. av
```

## Acceptance check

Every scratch subdirectory in a proposal has an owning command, producer, consumer, retention rule, and cleanup behavior. Otherwise only the scratch root is named.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
