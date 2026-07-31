# Abstract Category Reframing

**ID**: `abstract-category-reframing` | **Category**: `abstract-reframing`

## Trigger

Use when: the agent answers a correction by inventing abstract categories, spaces, layers, trees, namespaces, surfaces, families, or models the user did not state.

## Bad forms — what this looks like

- ❌ `"I over-framed that as..."`
- ❌ `"Better read: ..."`
- ❌ `"This is really a ... model."`
- ❌ `"These are peer ... namespaces."`
- ❌ `"The intended architecture is..."`
- ❌ `"The correct abstraction is..."`

## Required behavior

```text
When corrected, the agent must: 1. State the concrete corrected claim in the user's terms. 2. Remove the rejected abstraction befo
```

## Concrete example

The agent responds to a correction by replacing the user's concrete point with an assistant-authored abstract structure

**✅ CORRECT** (shortest path):

```text
When corrected, the agent must: 1. State the concrete corrected claim in the user's terms. 2. Remove the rejected abstraction befo
```

## Acceptance check

The next response after a correction repeats the user's concrete point without first-person diagnosis or new abstract categories. If an abstraction is necessary, the response labels it as provisional assistant shorthand and ties it to user text or current source evidence.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
