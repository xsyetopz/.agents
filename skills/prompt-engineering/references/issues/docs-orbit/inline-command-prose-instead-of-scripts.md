# Inline Command Prose Instead Of Scripts

**ID**: `inline-command-prose-instead-of-scripts` | **Category**: `docs-orbit`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent repeats inline smoke commands, transcript fragments, or prose command recipes instead of consolidating recurring product checks into runnable scripts.

## Observed failure

- ❌ `"Run this inline block again" for recurring lifecycle proof.`
- ❌ `A smoke evidence page made mostly of shell prose when the same behavior should be scripted.`
- ❌ `Updating copied command fragments instead of rerunning the owning script.`
- ❌ `Treating a pasted transcript as the durable verifier.`

## Required behavior

```text
When a command sequence becomes recurring evidence for lifecycle, generated output, ownership, or removal safety, the agent must:
```

## Example

- The agent described repeated smoke commands in documentation instead of first creating a durable lifecycle smoke script.

**✅ CORRECT** (shortest path):

```text
When a command sequence becomes recurring evidence for lifecycle, generated output, ownership, or removal safety, the agent must:
```

## Acceptance check

Recurring product checks are represented by runnable scripts under `scripts/`, and evidence docs point to the script command plus current observed output.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
