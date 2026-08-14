# Model Reasoning Guide

## Use this reference

Load this reference when model reasoning guide is material to a measured prompt or agent-behavior failure. Apply current provider guidance first, state each instruction once, and verify observable effects separately from the final answer.

Use model-specific claims only when current first-party documentation supports
them. Model names, modes, effort values, defaults, context limits, and benchmark
results change independently and must not be copied from an undated comparison
table into a prompt contract.

## Evidence record

For each named model, record:

- provider and exact model identifier;
- product surface or API;
- official documentation URL and retrieval date;
- supported execution modes and controls relevant to the task;
- local evaluation workload and baseline;
- unresolved or provider-defined behavior.

If any item is unverified, describe it as unknown. Do not fill it from model
family resemblance.

## Prompting across reasoning modes

Keep prompts outcome-focused: goal, relevant context, constraints, required
evidence, success criteria, tool contracts, and output format. Reasoning effort
changes model work; it does not justify different task requirements or requests
for private chain-of-thought.

Use explicit workflow steps when the application requires an observable order,
approval boundary, handoff, or retry limit. Do not add step-by-step instructions
solely because a model is labeled non-reasoning, and do not remove necessary
workflow constraints solely because it is labeled reasoning.

Compare modes and efforts on the same representative workload. Measure task
success and final-answer completeness before tokens, latency, or cost. Do not
assume the highest effort is the best tradeoff.

## GPT-5.6 family (conditional)

When the target is GPT-5.6, use the exact dated snapshots and provenance in
`official/openai-gpt-5.6-sol-prompting.2026-08-13.md`,
`official/openai-gpt-5.6-model.2026-08-13.md`, and
`official-sources.md`. These are one family-specific evidence route, not a
default for unrelated models. Refresh or replace the snapshots before making a
new current-model claim; official documentation remains authoritative.

Apply only the clauses relevant to the named model, mode, and product surface:

- keep prompts lean and state each instruction once;
- keep autonomy and approval in one place;
- use examples only for product requirements or measured gaps;
- specify concrete response requirements instead of broad brevity or tone labels;
- route programmatic tool calling only for bounded predictable reductions;
- evaluate program output separately from the final assistant message;
- compare modes and efforts on the same representative tasks.

## Other providers

Fetch current first-party documentation for the exact target. Keep provider
advice separate from OpenAI guidance. Generic recommendations in this skill are
heuristics until measured on the target workload.

## Cross-model review

A different model family can provide useful diversity, but family diversity is
not proof of correctness. Reviewers need the same evidence, rubric, blinded
inputs where appropriate, and deterministic acceptance gates. Final acceptance
remains tied to the target model's real execution environment.
