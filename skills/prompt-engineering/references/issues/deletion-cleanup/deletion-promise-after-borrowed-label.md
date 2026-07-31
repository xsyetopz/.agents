# Deletion Promise After Borrowed Label

**ID**: `deletion-promise-after-borrowed-label` | **Category**: `deletion-cleanup`

## Trigger

Use when: the agent borrows a user's artifact label, then promises removal before tracing behavior, callers, output, and ownership.

## Bad forms — what this looks like

- ❌ `"It is just a prose script."`
- ❌ `"Nobody needs this."`
- ❌ `"I will remove it and its references" before reading callers.`
- ❌ `Treating a typo, filename, complaint term, or nearby prose as a behavior trace.`
- ❌ `Replacing the artifact with another command that preserves the same unwanted wording gate.`

## Required behavior

```text
Before promising removal or replacement, identify:
observed behavior
direct callers
files written or changed
generated or installed surface
```

## Concrete example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path):

```text
Before promising removal or replacement, identify:
observed behavior
direct callers
```

## Acceptance check

For any challenged artifact, the answer contains a behavior trace before an edit commitment, or explicitly states that no edit commitment is being made until that trace exists.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
