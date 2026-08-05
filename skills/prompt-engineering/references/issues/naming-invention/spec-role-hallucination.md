# Spec Role Hallucination

**ID**: `spec-role-hallucination` | **Category**: `naming-invention`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Spec Role Hallucination

## Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

## Required behavior

```text
Ask what "spec" means only if local evidence does not define it.
Prefer existing format specs, source-backed document contracts, or external schemas over invented product JSON.
Do not create a format spec until its source path, external URL, or explicit user approval is known.
Keep product decisions in `PRODUCT.md` and ADRs.
Keep completion state in `goals/`.
```

## Example

The user meant specs integrated from real existing format specifications or source-backed artifact contracts, not assistant-authored product ledgers or plausible local schema names.

**✅ CORRECT** (shortest path):

```text
Ask what "spec" means only if local evidence does not define it.
Prefer existing format specs, source-backed document contracts, or external schemas over invented product JSON.
Do not create a format spec until its source path, external URL, or explicit user approval is known.
```

## Acceptance check

- `specs/` contains real source-backed specs, not product-governance ledgers or plausible local schema names. - Runtime renderer does not require invented governance specs. - Verifier checks that specs exist and are valid JSON, but does not treat them as product authority unless a current ADR says so.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
