# Abstract Category Reframing

**ID**: `abstract-category-reframing` | **Category**: `abstract-reframing`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent answers a correction by inventing abstract categories, spaces, layers, trees, namespaces, surfaces, families, or models the user did not state.

## Observed failure

- ❌ `"I over-framed that as..."`
- ❌ `"Better read: ..."`
- ❌ `"This is really a ... model."`
- ❌ `"These are peer ... namespaces."`
- ❌ `"The intended architecture is..."`
- ❌ `"The correct abstraction is..."`

## Required behavior

State the corrected claim in the user's terms. Remove the rejected abstraction before introducing any alternative. If shorthand is necessary, label it as provisional and tie it to user text or current source evidence.

## Example

The agent responds to a correction by replacing the user's concrete point with an assistant-authored abstract structure

**Corrected response:**

```text
The current requirement is <concrete corrected claim>. The earlier category is
not part of the user's model, so it is removed rather than renamed.
```

## Acceptance check

The next response after a correction repeats the user's concrete point without first-person diagnosis or new abstract categories. If an abstraction is necessary, the response labels it as provisional assistant shorthand and ties it to user text or current source evidence.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
