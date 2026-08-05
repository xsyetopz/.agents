# Model Reasoning Guide

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

## GPT-5.6

The canonical details for this skill are in `openai-gpt-5.6.md`, sourced from
current official OpenAI documentation. The controlling practices are:

- lean prompts, each instruction stated once;
- compact autonomy and approval policy in one place;
- examples only for product requirements or measured gaps;
- concrete response requirements instead of broad brevity or tone labels;
- task-specific routing for programmatic tool calling;
- separate evaluation of program output and final assistant message;
- standard/pro and effort comparisons on the same representative tasks.

OpenAI's live documentation is authoritative if this reference becomes stale.

## Other providers

Fetch current first-party documentation for the exact target. Keep provider
advice separate from OpenAI guidance. Generic recommendations in this skill are
heuristics until measured on the target workload.

## Cross-model review

A different model family can provide useful diversity, but family diversity is
not proof of correctness. Reviewers need the same evidence, rubric, blinded
inputs where appropriate, and deterministic acceptance gates. Final acceptance
remains tied to the target model's real execution environment.
