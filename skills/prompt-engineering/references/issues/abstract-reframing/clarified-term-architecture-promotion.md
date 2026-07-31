# Clarified Term Architecture Promotion

**ID**: `clarified-term-architecture-promotion` | **Category**: `abstract-reframing`

## Trigger

Use when: the agent treats a user's clarification of a term as authorization to make that term a first-class architecture, directory, product surface, or naming convention.

## Bad forms — what this looks like

- ❌ `"Since you use this term, it should be top-level."`
- ❌ `"This is a real product concept now."`
- ❌ "Add `<term>/`."
- ❌ "Make `<term>.yaml`."
- ❌ "First-class `<term>` surface."
- ❌ `Treating a clarification as a naming decision.`

## Required behavior

```text
When the user defines or clarifies a term, the agent must: 1. Treat the definition as context for understanding the user's sentenc
```

## Concrete example

The agent promotes a clarified term into first-class architecture because the user explained what the term means

**✅ CORRECT** (shortest path):

```text
When the user defines or clarifies a term, the agent must: 1. Treat the definition as context for understanding the user's sentenc
```

## Acceptance check

After a user clarifies a term, the next architecture answer uses the term only to preserve meaning, not as a new file-tree element. If placement is needed, the answer either uses an existing user-approved location or asks for the naming decision explicitly.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
