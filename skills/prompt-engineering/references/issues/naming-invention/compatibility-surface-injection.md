# Compatibility Surface Injection

**ID**: `compatibility-surface-injection` | **Category**: `naming-invention`

## Trigger

Use when: the agent adds compatibility wrappers, migration shims, aliases, fallback commands, or backward-compatible surfaces that the user did not ask for.

## Concrete example

### Compatibility Wrapper Without Request ```diff - The agent keeps the old entrypoint as a compatibility wrapper

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
