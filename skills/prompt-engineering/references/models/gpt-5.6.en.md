# GPT-5.6 family

- Canonical identifier: `gpt-5.6`
- Guide language: English
- Evidence status: prompt guide (shared family)
- Retrieved: 2026-08-14

## Prompt recipe

- State the outcome, success criteria, constraints, evidence requirements, and
  completion bar; leave the model room to choose an efficient path.
- Remove repeated instructions, examples, and unrelated tools. Keep behavior
  that changes the result or protects a real invariant.
- Define autonomy and approval boundaries in one place: permit scoped local
  work, and require confirmation for external, destructive, costly, or
  scope-expanding effects.
- Specify the output shape and stopping condition. Preserve required facts,
  caveats, evidence, and next actions when requesting concise output.

## Operational constraints

- Supported reasoning efforts and `text.verbosity` values are surface-specific;
  verify them against the current model documentation before use.
- Expose only task-relevant tools. Use Programmatic Tool Calling for bounded,
  deterministic result reduction, then return semantic judgment and approvals
  to direct model turns.
- Preserve citations and required evidence; report missing support rather than
  guessing. Evaluate program output separately from the final assistant message.
- Keep reusable prompt prefixes stable when prompt caching matters and measure
  cache, token, latency, and cost effects on the target workload.
- Compare modes and efforts on the same representative evaluations. A family
  label is not evidence that one setting is best for a task.

## Official sources

| Type | URL | Retrieved |
| --- | --- | --- |
| GPT-5.6 family prompt guidance | https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6.md | 2026-08-14 |
| General prompt engineering | https://developers.openai.com/api/docs/guides/prompt-engineering.md | 2026-08-14 |
| GPT-5.6 family model guide | https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6 | 2026-08-14 |
