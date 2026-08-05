# User Intent Reframing

**ID**: `user-intent-reframing` | **Category**: `abstract-reframing`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent replaces the user's stated complaint with assistant-authored labels, agenda, or solution framing.

## Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

## Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

## Example

### Complaint Converted Into Plan Label ```diff - The agent says it is planning a rollback or simplification because the user criticized bloat

**✅ CORRECT** (shortest path):

```text
1. Read relevant file(s) (1 call).
2. Verify references (1 Grep call).
3. State facts, then propose.
```

## Acceptance check

The observable response avoids the trigger pattern and exhibits the required behavior shown by the example.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
