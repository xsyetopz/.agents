# Source Truth Misplacement

**ID**: `source-truth-misplacement` | **Category**: `source-truth`

## Trigger

Use when: the agent frames wrappers, generated output directories, top-level convenience roots, or scripts as source-of-truth instead of keeping source authority in the user-designated source tree.

## Bad forms — what this looks like

- ❌ Treating `scripts/` as installer source authority because an installer command exists.
- ❌ Treating `plugins/`, `skills/`, or `prompts/` as authoring roots while also claiming `src/` is the source of truth.
- ❌ `Treating generated output roots as maintained source.`
- ❌ `"The source belongs wherever the file is emitted."`

## Required behavior

```text
When proposing a tree, the agent must mark each root as one of: 1. source authority, 2. implementation source, 3. generated output
```

## Concrete example

- The agent proposed a PowerShell installer under `scripts/` and then had to be corrected that no one said a `.ps1` script there would be source-of-truth.

**✅ CORRECT** (shortest path):

```text
When proposing a tree, the agent must mark each root as one of: 1. source authority, 2. implementation source, 3. generated output
```

## Acceptance check

The proposed tree states which roots are source-authoritative and which are wrappers or output, and no generated or wrapper root is described as owning product truth without explicit authority.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
