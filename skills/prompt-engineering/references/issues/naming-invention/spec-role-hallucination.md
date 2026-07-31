# Spec Role Hallucination

**ID**: `spec-role-hallucination` | **Category**: `naming-invention`

## Trigger

Spec Role Hallucination

## Required behavior

```text
Ask what "spec" means only if local evidence does not define it.
Prefer existing format specs, source-backed document contracts, or external schemas over invented product JSON.
Do not create a format spec until its source path, external URL, or explicit user approval is known.
Keep product decisions in `PRODUCT.md` and ADRs.
Keep completion state in `goals/`.
```

## Concrete example

The user meant specs integrated from real existing format specifications or source-backed artifact contracts, not assistant-authored product ledgers or plausible local schema names.

**✅ CORRECT** (shortest path):

```text
Ask what "spec" means only if local evidence does not define it.
Prefer existing format specs, source-backed document contracts, or external schemas over invented product JSON.
Do not create a format spec until its source path, external URL, or explicit user approval is known.
```

## Acceptance check

- `specs/` contains real source-backed specs, not product-governance ledgers or plausible local schema names. - Runtime renderer does not require invented governance specs. - Verifier checks that specs exist and are valid JSON, but does not treat them as product authority unless a current ADR says so.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
