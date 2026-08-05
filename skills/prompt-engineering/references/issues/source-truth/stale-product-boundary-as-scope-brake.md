# Stale Product Boundary As Scope Brake

**ID**: `stale-product-boundary-as-scope-brake` | **Category**: `source-truth`

## Trigger

Use when: the agent treats an outdated product boundary as authority to reject or narrow the user's clarified product direction.

## Bad forms — what this looks like

- ❌ `"That would be scope creep."`
- ❌ `"The product only allows the current generated file."`
- ❌ "We cannot add hooks/templates because `PRODUCT.md` says no."
- ❌ `"Current implementation is the product boundary."`

## Required behavior

```text
When the user clarifies product direction that conflicts with `PRODUCT.md`, the agent must: 1. Treat the user clarification as cur
```

## Concrete example

- The agent said additional generated templates or hooks would be scope creep because `PRODUCT.md` currently said the only generated file was `.codex/config.toml`.

**✅ CORRECT** (shortest path):

```text
When the user clarifies product direction that conflicts with `PRODUCT.md`, the agent must: 1. Treat the user clarification as cur
```

## Acceptance check

The agent updates the product boundary to separate current generated output from intended product direction, and any final answer names unimplemented surfaces as pending implementation rather than rejected scope.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
