# Source Truth Misplacement

**ID**: `source-truth-misplacement` | **Category**: `source-truth`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent frames wrappers, generated output directories, top-level convenience roots, or scripts as source-of-truth instead of keeping source authority in the user-designated source tree.

## Observed failure

- ❌ Treating `scripts/` as installer source authority because an installer command exists.
- ❌ Treating `plugins/`, `skills/`, or `prompts/` as authoring roots while also claiming `src/` is the source of truth.
- ❌ `Treating generated output roots as maintained source.`
- ❌ `"The source belongs wherever the file is emitted."`

## Required behavior

```text
When proposing a tree, the agent must mark each root as one of: 1. source authority, 2. implementation source, 3. generated output
```

## Example

- The agent proposed a PowerShell installer under `scripts/` and then had to be corrected that no one said a `.ps1` script there would be source-of-truth.

**✅ CORRECT** (shortest path):

```text
When proposing a tree, the agent must mark each root as one of: 1. source authority, 2. implementation source, 3. generated output
```

## Acceptance check

The proposed tree states which roots are source-authoritative and which are wrappers or output, and no generated or wrapper root is described as owning product truth without explicit authority.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
