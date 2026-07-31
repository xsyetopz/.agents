# User Intent Reframing

**ID**: `user-intent-reframing` | **Category**: `abstract-reframing`

## Trigger

Use when: the agent replaces the user's stated complaint with assistant-authored labels, agenda, or solution framing.

## Concrete example

### Complaint Converted Into Plan Label ```diff - The agent says it is planning a rollback or simplification because the user criticized bloat

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
