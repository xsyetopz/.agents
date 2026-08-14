---
name: prompt-engineering
description: Prompt design, tool routing, behavioral evaluation, and named-model guidance; excludes runtime code.
---

# Prompt Engineering

Treat prompts as versioned behavior. Optimize for observable outcomes and independent evidence.

## Use this skill

- Write or revise system prompts, developer prompts, `AGENTS.md`, `SKILL.md`, or tool descriptions.
- Debug instruction, authority, tool-routing, approval, or output failures.
- Adapt instructions to a named model, provider, mode, API, or agent surface.
- Build prompt ablations, behavioral evaluations, graders, or regression suites.
- Remove duplicated instructions, irrelevant tools, examples, or stale context.
- Do not use for runtime invariants, unrelated tool/API defects, model selection without a representative workload, or one-off answers with no reusable prompt artifact.

## Rules

- For named models and providers, use dated first-party sources. Mark source gaps; do not fill them with inference.
- Preserve explicitly requested models. Never invent names, effort tiers, context limits, pricing, availability, or behavior; a named family is one conditional route, not a package default.
- Keep authority and approval in one policy. External, destructive, costly, credential, and production effects require confirmation.
- Separate instructions, examples, and untrusted data. Delimiters aid interpretation but do not create a security boundary.
- Route only relevant tools and define trigger, input/output, evidence, stop/retry, and approval boundaries.
- Validate real behavior in an isolated fixture and inspect tool/filesystem effects separately from final-answer quality.

## Steps

1. Identify the target model or surface, prompt owner, baseline, failing behavior, tools, authority, and completion evidence.
2. Fetch official guidance when named-model or current-provider claims matter; map each claim to a source.
3. State each instruction once. Remove one instruction, example, or tool group at a time when testing causality.
4. Run static checks and paired baseline/candidate cases, including no-tool, required-tool, pressure, ambiguous, authorized, and forbidden-effect cases.
5. Run the real model or installed agent when available. Inspect program output and the final answer independently, keep only non-regressing changes, and report source dates and limits.

## Resources

- Start with the [reference router](references/index.md).
- Source dates, URLs, and hashes: [official source manifest](references/official-sources.md).
- Generic prompting: [official OpenAI snapshot](references/official/openai-prompt-engineering.2026-08-13.md).
- GPT-5.6 family: [family model guide](references/models/gpt-5.6.en.md), [family prompt guidance](references/official/openai-gpt-5.6-sol-prompting.2026-08-13.md), and [model/API guide](references/official/openai-gpt-5.6-model.2026-08-13.md).
- Named models: [model index](references/models/index.md).
- Reasoning and model comparison: [model reasoning guide](references/model-reasoning-guide.md).
- Reusable structures: [prompt templates](references/prompt-templates.md).
- Failure patterns: [anti-patterns](references/anti-patterns.md), [issue corpus index](references/issue-corpus-index.md), and [issue taxonomy](references/issues/index.md).
- Sibling routes: `$openai-docs` for current official OpenAI product/model guidance and `$architecture-design` for agent-system structure and tool boundaries.

## Verify

- Run `python3 scripts/check.py`, `python3 scripts/audit_openai_alignment.py`, and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Run `python3 scripts/live_codex_audit.py` only with an available installed-Codex isolated fixture; classify missing binary, auth, or model availability as unverified.
- Confirm current sources support model claims, the candidate retains requirements, representative cases pass, forbidden effects remain absent, and final-answer quality is assessed separately from tool effects.
- Do not claim a live run without evidence.
