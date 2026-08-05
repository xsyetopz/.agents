# Harness Drift Over Product Structure

**ID**: `harness-drift-over-product-structure` | **Category**: `docs-orbit`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent keeps adding smoke cases, wrappers, or verification machinery while the product source and test structure remain thin or missing.

## Observed failure

- ❌ `"I will add one more smoke phase."`
- ❌ `"The smoke script proves this" when the product implementation is still just a thin script.`
- ❌ `Confessing drift with self-analysis instead of naming the current files, missing structure, and next product correction.`
- ❌ `Treating a harness pass as product architecture.`

## Required behavior

```text
Inspect current product source and test layout before adding more harness code.
Add a smoke case only when it proves a concrete product change made in the same turn.
If the product lacks source or test structure, address that structure directly instead of expanding smoke scripts.
When challenged about drift, answer the artifact-state question first and stop unless explicitly told to continue.
```

## Example

- The agent keeps adding lifecycle smoke cases instead of creating a real source and test structure.

**✅ CORRECT** (shortest path):

```text
Inspect current product source and test layout before adding more harness code.
Add a smoke case only when it proves a concrete product change made in the same turn.
If the product lacks source or test structure, address that structure directly instead of expanding smoke scripts.
```

## Acceptance check

- Product-progress turns touch product implementation or intentional test structure before adding broad harness coverage. - Smoke scripts remain small end-to-end checks, not the main place product behavior accumulates. - Reports distinguish product source, tests, smoke, and evidence instead of collapsing them into one proof bucket.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
