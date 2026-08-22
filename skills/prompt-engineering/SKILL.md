---
name: prompt-engineering
description: Agent prompt design, intent, authority, corrections, tool routing, direct responses, behavioral evaluation, and model guidance.
---

# Prompt Engineering

Design prompts from observed behavior, real authority, and measurable outcomes.

## Use this skill

- Write or revise system prompts, developer prompts, `AGENTS.md`, `SKILL.md`, tool descriptions, and prompt-owned examples.
- Diagnose agents that misread intent, invent facts or architecture, ignore corrections, misuse tools, narrate themselves, or claim unsupported blockers.
- Design behavioral evaluations for prompt changes and compare prompt versions on the same workload.
- Use dated first-party sources when an explicitly named model or provider is in scope.
- Do not use for unrelated runtime defects, repository architecture, documentation-only cleanup, or model selection without a representative workload.
- Redirect runtime and product boundaries to `$software-architecture`, repository prose to `$repo-docs`, and CI behavior to `$git-ci-cd`.

## Rules

- A question, complaint, correction, negative finding, pasted error, or stated goal is not edit authority. Answer or clarify, then stop unless the user explicitly requested a change or execution.
- Inspect the actual prompt owner and the challenged artifact before diagnosing it. Trace callers, consumers, reads, writes, side effects, source authority, and uncovered behavior before proposing removal or replacement.
- Keep user requirements, observed repository facts, verified external facts, open questions, and agent proposals distinct.
- Preserve the user's concrete correction. Remove the rejected assumption instead of renaming it or wrapping it in a new abstraction.
- Do not invent files, directories, schemas, manifests, wrappers, compatibility paths, model identifiers, effort levels, capabilities, or source-of-truth claims.
- Use a named skill, workflow, generator, or source through its documented native route. Report an unavailable route; do not substitute manual parsing or a familiar alternative.
- Keep responses direct. Lead with the requested result or observed fact. Omit apologies, praise, self-analysis, repeated prompt text, and process narration unless the user asks for them.
- Test observable behavior. Do not use phrase scans, heading checks, or documentation consistency as proof of runtime, tool, installation, or mutation behavior.
- Do not invent custom schema files or custom generated files as outputs. Use only established repository-owned formats and canonical inputs.

## Steps

1. Identify the prompt owner, target agent or model surface, explicit request, allowed effects, baseline behavior, consumers, and completion evidence.
2. Read the complete owning prompt and the minimum callers, tool contracts, repository instructions, and failing exchanges needed to establish the behavior.
3. Record working evidence as user requirements, observed facts, verified external facts, open questions, and proposals. Do not promote one category into another.
4. Rewrite the smallest owning prompt surface. State each rule once, use concrete triggers and actions, preserve exact user terms, and remove conflicting or unsupported guidance.
5. Compare baseline and candidate on the same natural cases: answer-only, correction, missing artifact, ambiguous authority, authorized change, required tool, forbidden effect, and genuine blocker.
6. Inspect tool and filesystem effects separately from the final response. Keep the change only when required behavior passes without a material regression.

## Resources

- Start with [references/index.md](references/index.md) and open only the route needed for the task.
- The router owns generic workflow, communication, evaluation, and conditional provider-source routes. Do not load them all by default.

## Verify

- Done means the owning prompt changed, representative baseline and candidate cases were compared, required effects occurred, forbidden effects did not occur, and the final response met the task without unsupported claims.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Run the repository validator and relevant behavioral lane when available. Record the exact prompt version, fixture, model or agent surface, commands, outputs, and changed paths outside `evals/evals.json`.
- Static package checks prove structure only. Mark unavailable model, authentication, network, native skill route, or live behavioral evidence `UNVERIFIED`.
