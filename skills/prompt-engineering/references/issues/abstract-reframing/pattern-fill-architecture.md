# Pattern-Fill Architecture

**ID**: `pattern-fill-architecture` | **Category**: `abstract-reframing`

## Trigger

Use when: the agent fills a product or repository architecture with familiar scaffolding terms instead of staying inside the user's stated constraints.

## Bad forms — what this looks like

- ❌ `"v1"`
- ❌ `"first implementation slice"`
- ❌ `"default profile"`
- ❌ `"power profile"`
- ❌ `"dogfood.yaml"`
- ❌ `"crates are the natural place"`

## Required behavior

```text
When the user is defining architecture, the agent must: 1. Treat each correction as a hard constraint for the rest of the turn. 2.
```

## Concrete example

The agent completes an architecture from common repo patterns after the user has already corrected the frame

**✅ CORRECT** (shortest path):

```text
When the user is defining architecture, the agent must: 1. Treat each correction as a hard constraint for the rest of the turn. 2.
```

## Acceptance check

After a correction, the next architecture answer lists only user-stated directories, observed repository facts, and explicitly labelled open questions or proposals. No familiar scaffold term appears unless the response ties it directly to a user statement or current file evidence.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
