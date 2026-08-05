# Unverified Example Claims

**ID**: `unverified-example-claims` | **Category**: `source-truth`

## Trigger

Use when: the agent changes examples, versions, model names, config keys, or dependency refs based on familiarity instead of verification.

## Concrete example

### Familiar Version Substitution ```diff - The agent changes an example from actions/checkout@v7 to actions/checkout@v4 because v4 feels real

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
