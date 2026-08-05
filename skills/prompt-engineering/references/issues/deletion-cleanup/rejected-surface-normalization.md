# Rejected Surface Normalization

**ID**: `rejected-surface-normalization` | **Category**: `deletion-cleanup`

## Trigger

Use when: the agent keeps rejected, removed, or unwanted surfaces alive as concepts, tests, docs, or proof language.

## Concrete example

### Retired Surface Kept As Concept ```diff - The test says retired docs must not be referenced

**✅ CORRECT** (shortest path):

```text
1. Read relevant file(s) (1 call).
2. Verify references (1 Grep call).
3. State facts, then propose.
```

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
