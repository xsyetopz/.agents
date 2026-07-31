# Inline Command Prose Instead Of Scripts

**ID**: `inline-command-prose-instead-of-scripts` | **Category**: `docs-orbit`

## Trigger

Use when: the agent repeats inline smoke commands, transcript fragments, or prose command recipes instead of consolidating recurring product checks into runnable scripts.

## Bad forms — what this looks like

- ❌ `"Run this inline block again" for recurring lifecycle proof.`
- ❌ `A smoke evidence page made mostly of shell prose when the same behavior should be scripted.`
- ❌ `Updating copied command fragments instead of rerunning the owning script.`
- ❌ `Treating a pasted transcript as the durable verifier.`

## Required behavior

```text
When a command sequence becomes recurring evidence for lifecycle, generated output, ownership, or removal safety, the agent must:
```

## Concrete example

- The agent described repeated smoke commands in documentation instead of first creating a durable lifecycle smoke script.

**✅ CORRECT** (shortest path):

```text
When a command sequence becomes recurring evidence for lifecycle, generated output, ownership, or removal safety, the agent must:
```

## Acceptance check

Recurring product checks are represented by runnable scripts under `scripts/`, and evidence docs point to the script command plus current observed output.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
