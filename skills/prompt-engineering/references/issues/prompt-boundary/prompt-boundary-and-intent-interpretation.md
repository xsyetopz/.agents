# Prompt, Boundary, and Intent Interpretation

**ID**: `prompt-boundary-and-intent-interpretation` | **Category**: `prompt-boundary`

## Trigger

Use when: extracting a specific assistant-behavior failure mode, guardrail, or acceptance criterion.

## Concrete example

### Assumption Over Prompt ```diff - The assistant substitutes inferred intent for literal user text

**✅ CORRECT** (shortest path):

```text
1. Read relevant file(s) (1 call).
2. Verify references (1 Grep call).
3. State facts, then propose.
```

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
