# Full Source Application Downgrade

**ID**: `full-source-application-downgrade` | **Category**: `prompt-boundary`

## Trigger

Use when: the agent is told to fully apply a named prompt guide, issue corpus, spec, policy, or source, but treats it as optional inspiration or applies only visible concepts.

## Bad forms — what this looks like

- ❌ `I applied some concepts from the guide.`
- ❌ `I mostly followed it.`
- ❌ `I used the spirit of the prompt guide.`
- ❌ `The visible concepts are covered.`
- ❌ `Full application is approximated by these rules.`
- ❌ `Completing a subset and calling it done.`

## Required behavior

```text
Treat explicit words such as "full", "fully", "literal", "complete", and "according to the guide" as hard scope constraints.
Read the named source before acting.
Extract the source's required structure, target surfaces, stop rules, output contract, and acceptance criteria.
Map each required source element to the exact artifact category the user requested.
Do not replace source requirements with familiar concepts, summaries, or partial approximations.
```

## Concrete example

- A prompt guide defines Role, Personality, Goal, Success criteria, Constraints, Output, and Stop rules; the agent copies only outcome-first and validation language.

**✅ CORRECT** (shortest path):

```text
Treat explicit words such as "full", "fully", "literal", "complete", and "according to the guide" as hard scope constraints.
Read the named source before acting.
Extract the source's required structure, target surfaces, stop rules, output contract, and acceptance criteria.
```

## Acceptance check

Before reporting completion, the agent can point to every required element from the named source and show where it was applied, intentionally not applicable, or blocked. No completion claim uses partial-application language when the user requested full application.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
