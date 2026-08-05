# Invariant Fixation Over Product Behavior

**ID**: `invariant-fixation-over-product-behavior` | **Category**: `deletion-cleanup`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent treats one current literal or setting as the main product focus instead of a constraint inside the larger lifecycle behavior.

## Observed failure

- ❌ "`model = \"gpt-5.5\"` is the main thing."
- ❌ `"The product is done because the model value is correct."`
- ❌ `"Everything else is scope creep because the invariant is satisfied."`
- ❌ `"The generated config literal proves the install system."`
- ❌ "The goal is mostly to ensure `gpt-5.5` is in config."

## Required behavior

```text
When a current literal appears in product docs, the agent must: 1. Keep it out of goal and product-boundary wording unless the use
```

## Example

- The agent treated `model = "gpt-5.5"` as the primary focus when the user was asking why the work had not moved toward actual lifecycle scripts and generated-file ownership.

**✅ CORRECT** (shortest path):

```text
When a current literal appears in product docs, the agent must: 1. Keep it out of goal and product-boundary wording unless the use
```

## Acceptance check

The agent's product updates and final report treat the model setting as one invariant, and separately show evidence for lifecycle command behavior, ownership boundaries, generated files, and removal safety.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
