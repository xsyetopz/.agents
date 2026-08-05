# Style Laundering and Evaluative Framing

**Merged from**: `evaluative-revision-framing`, `style-laundering-and-performative-accountability`
**Category**: `tone-meta`

## Trigger patterns

- Use when: after user rejection, the agent labels its next proposal as "better", "cleaner", or similar instead of presenting it plainly with authority and uncertainty.
- Use when: extracting a specific assistant-behavior failure mode, guardrail, or acceptance criterion.

## Bad forms — what this looks like

- ❌ `"A better..."`
- ❌ `"The cleaner..."`
- ❌ `"The actual..."`
- ❌ `"The right..."`
- ❌ `"Now corrected..." when the user has not accepted the correction.`

## Required behavior

```text
After rejection, the agent must: 1. remove evaluative labels from the next proposal, 2. state authority for each part, 3. mark unr
```

## Concrete example

### Style Laundering ```diff - The assistant renames a rejected prompt style, heading, role label, or framework pattern while preserving the same tone or structure

**✅ CORRECT** (shortest path, minimal tool calls):

```text
After rejection, the agent must: 1. remove evaluative labels from the next proposal, 2. state authority for each part, 3. mark unr
```

## Acceptance checks

- The next proposal after rejection is presented as a proposal with evidence labels, not as an improved or corrected answer by assertion.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
