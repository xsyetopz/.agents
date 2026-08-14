# Grok 4.6
- Canonical identifier: `grok-4.6`
- Guide language: English
- Evidence status: source gap (model/API and engineering guidance; no singular prompt guide)

## Prompt recipe
- State the objective, relevant context, hard constraints, available tools, and required output.
  Give the model a clear completion bar instead of prescribing every intermediate step.
- Keep tool descriptions precise: document accepted inputs, return fields, side effects, and errors.
  Route each tool only when its result is needed for the stated objective.
- For reasoning tasks, name the decision criteria, evidence standard, and stopping condition.
  Ask for the decision or artifact, not hidden chain-of-thought text.
- For agent workflows, define ownership, handoffs, approval boundaries, and final verification.
  Keep independent work parallel only when results cannot change one another.

## Operational constraints
- Use the API identifier `grok-4.6`; the official model profile lists a 500K-token context.
  The profile describes the model as a frontier coding, agentic, and knowledge-work model.
- Supported reasoning levels are `low`, `medium`, `high`, and `xhigh`.
  Select effort from measured task quality and latency, not from the model name alone.
- Keep stable reusable prefixes for prompt caching and pass a stable `prompt_cache_key` when useful.
  For conversation continuity, use the documented `x-grok-conv-id` strategy where appropriate.
- Shorten long conversations before context pressure degrades retrieval and tool selection.
  Preserve the current objective, decisions, assumptions, and unresolved blockers.
- Test direct tool calls and multi-agent orchestration separately from plain text generation.
  Treat tool errors and incomplete results as explicit failure states, not successful evidence.
- No dedicated first-party page titled “prompt guide” was found in this search.
  Treat the cited model, reasoning, text-generation, and caching pages as engineering guidance.

## Official sources
| Type | URL | Retrieved |
| --- | --- | --- |
| Grok 4.6 model profile | https://docs.x.ai/developers/models/grok-4.6 | 2026-08-14 |
| xAI reasoning guidance | https://docs.x.ai/developers/model-capabilities/text/reasoning | 2026-08-14 |
| xAI text-generation guidance | https://docs.x.ai/developers/model-capabilities/text/generate-text | 2026-08-14 |
| xAI prompt caching guidance | https://docs.x.ai/developers/advanced-api-usage/prompt-caching | 2026-08-14 |
