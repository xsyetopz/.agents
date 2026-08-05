# Unverified Example Claims

**ID**: `unverified-example-claims` | **Category**: `source-truth`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent changes examples, versions, model names, config keys, or dependency refs based on familiarity instead of verification.

## Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

## Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

## Example

### Familiar Version Substitution ```diff - The agent changes an example from actions/checkout@v7 to actions/checkout@v4 because v4 feels real

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
