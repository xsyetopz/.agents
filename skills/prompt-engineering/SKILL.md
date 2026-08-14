---
name: prompt-engineering
description: prompt design, tool routing, behavioral evaluations, named-model guidance; excludes runtime code.
---

# Prompt Engineering

Treat prompts as versioned behavior. Optimize for observable outcomes and
independent evidence, not impressive wording or keyword coverage.

## When to use

- Write or revise system/developer prompts, `AGENTS.md`, `SKILL.md`, or tool descriptions.
- Debug instruction, authority, tool-routing, approval, or output failures.
- Adapt instructions to a named model, mode, API, or agent surface.
- Build prompt ablations, behavioral evaluations, graders, or regression suites.
- Remove duplicated instructions, irrelevant tools, examples, or stale context.

## When NOT to use

- Runtime invariants belonging in permissions, schemas, hooks, policy engines, or code.
- Tool/API defects unrelated to instructions.
- Model selection without a representative evaluation workload.
- A one-off answer that needs no reusable prompt artifact.

## Guardrails

- For named models/providers, use a dated first-party source; the model index labels source gaps explicitly, and no gap may be filled with inference.
- Preserve an explicitly requested model; never invent model names, effort tiers, context limits, pricing, availability, or behavior. Any named family is one conditional route, not a package-wide default.
- Keep authority and approval in one policy; local safe work need not ask repeatedly, while external, destructive, costly, credential, and production effects require confirmation.
- Separate instructions, examples, and untrusted data; delimiters aid interpretation but do not create a security boundary.
- Route only relevant tools and specify trigger, input/output, evidence, stop/retry, and approval boundaries.
- Validate real behavior in an isolated fixture; inspect tool/filesystem effects separately from final-answer quality.

## Workflow

1. Identify target model/surface, prompt owner, baseline, failing behavior, tools, authority, and completion evidence.
2. Fetch official guidance when named-model or current-provider claims matter; make a clause-to-requirement map.
3. State each instruction once. Remove one instruction group, example group, or tool at a time when isolating causality; examples are optional and must earn their context cost.
4. Run static checks and paired baseline/candidate behavioral cases on the same representative evaluations, including no-tool, required-tool, pressure, ambiguous, authorized, and forbidden-effect cases.
5. Run the real model or installed agent when available; inspect program output and final assistant message independently, keep only non-regressing changes, and report source dates, paths, and limits.

## Quick start

1. Run `python3 scripts/check.py` from this package directory.
2. For generic prompt work, load [the official generic snapshot](references/official/openai-prompt-engineering.2026-08-13.md).
3. For named-model work, choose the exact dated and language-matched guide from the [model index](references/models/index.md).
4. For GPT-5.6 work, load [the family guide](references/official/openai-gpt-5.6-sol-prompting.2026-08-13.md), [the model guide](references/official/openai-gpt-5.6-model.2026-08-13.md), and [the provenance manifest](references/official-sources.md).
5. Run `python3 scripts/audit_openai_alignment.py`; run the live audit only when an installed `codex` binary and isolated fixture are available.

## Reference map

Load only the references needed for the target:

- [Reference router](references/index.md) — choose one source, model, template,
  or issue route before opening deeper material.
- [Official source manifest](references/official-sources.md) — URLs, retrieval dates, and snapshot hashes.
- [Generic provider guidance](references/official/openai-prompt-engineering.2026-08-13.md) — model-neutral prompting and API behavior.
- [GPT-5.6 family guide](references/models/gpt-5.6.en.md) — shared family recipe and operational constraints.
- [GPT-5.6 family guidance](references/official/openai-gpt-5.6-sol-prompting.2026-08-13.md) — named GPT-5.6 prompt adaptation.
- [GPT-5.6 model guide](references/official/openai-gpt-5.6-model.2026-08-13.md) — named model/API claims.
- [Named-model index](references/models/index.md) — route to one dated, language-matched guide after selecting the target.
- [Model reasoning guide](references/model-reasoning-guide.md) — conditional model and mode evidence.
- [Prompt templates](references/prompt-templates.md) — reusable structures with only the needed fields.
- [Anti-patterns](references/anti-patterns.md) — broad failure catalog.
- [Issue corpus index](references/issue-corpus-index.md) — load matching observed failures only.
- [Issue taxonomy](references/issues/index.md) — open one category and anchored case after lookup.

## Completion

Complete when current sources support model-specific claims, the candidate is
leaner or more precise without losing requirements, representative behavioral
cases pass, forbidden effects remain absent, and final-answer quality is assessed
separately from tool effects. Do not claim a live run without its evidence.

## Validation

Run from this package directory:

```sh
python3 scripts/check.py
python3 scripts/audit_openai_alignment.py
python3 -m json.tool evals/evals.json >/dev/null
```

Use `python3 scripts/live_codex_audit.py` only for an explicitly available,
network-free installed-Codex fixture; classify missing binary, auth, or model
availability as unverified rather than silently passing.

## Related skills

- `$openai-docs` — fetch current official OpenAI product/model guidance.
- `$prompt-engineering` — route prompt, tool, and behavioral-evaluation work here.
- `$architecture-design` — make structural decisions for agent systems and tool boundaries.
