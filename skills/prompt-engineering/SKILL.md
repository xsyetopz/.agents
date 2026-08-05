---
name: prompt-engineering
description: >
  Use to design or audit system prompts, tool routing, behavioral evals, or GPT-5.6 instructions; not runtime code or model selection alone.
---

# Prompt Engineering

Treat prompts as versioned software behavior. Optimize for required observable
outcomes, not for impressive wording or static keyword coverage.

## When to use

- Writing or revising system/developer prompts, AGENTS.md, SKILL.md, or tool descriptions
- Debugging recurring instruction, authority, tool-routing, approval, or output failures
- Adapting instructions to a named model, mode, API, or agent surface
- Building prompt ablations, behavioral evaluations, graders, and regression suites
- Reducing duplicated instructions, irrelevant tools, examples, or context

## When NOT to use

- Runtime invariants that belong in permissions, schemas, hooks, policy engines, or code
- Tool/API defects unrelated to instructions
- Model selection without a representative evaluation workload
- A one-off answer that needs no reusable prompt artifact

## Source authority

For named models or providers, fetch current official guidance before editing.
Apply evidence in this order:

1. current official documentation for the exact model and product surface;
2. repository contracts and measured local behavior;
3. primary research relevant to the failure;
4. this skill's generic guidance and issue corpus.

Record source URL and retrieval date. Preserve an explicitly requested model.
Do not invent model names, effort tiers, context limits, pricing, availability, or
behavior. For GPT-5.6, load references/openai-gpt-5.6.md and refresh the live model
guidance before material model-specific changes.

Begin a named-model audit with the official sources used, retrieval date, and a
plain statement that current official guidance overrides conflicting generic
prompt advice.

## Core principles

### 1. Specify outcome and evidence

Define task, target model/surface, available tools, observable effects, required
evidence, completion condition, and final answer. Tie each non-obvious instruction
to a product requirement, security boundary, or measured failure.

### 2. Keep the prompt lean

State each instruction once. Keep authority and approval in one place. Expose only
relevant tools with precise schemas and error behavior. Retrieve large references
on demand. Remove one instruction group, example group, or tool at a time and
rerun the same representative evaluations; resource savings count only when
behavior still passes. Examples are optional and must earn their context cost.

### 3. Define autonomy and approval once

For coding agents, use one compact policy equivalent to:

    Read, explain, review, diagnose, or plan requests inspect and report.
    Change, build, or fix requests make safe in-scope local changes and validate.
    External, destructive, costly, credential, production, or material scope expansion requires confirmation.

Adapt it to the product's actual authority model. Do not repeat variants that make
safe local work ask for approval unnecessarily.

### 4. Use precise constraints

Positive and negative instructions are both valid when they define concrete
behavior. Choose the least ambiguous form. Describe writing choices and required
facts rather than broad personality or tone labels. Use examples only when they
encode a product requirement or repair a measured gap.

### 5. Separate context from authority

Use semantic headings, XML, or fences to identify instructions, examples, and
untrusted data. Delimiters aid interpretation; they do not create a security
boundary. Enforce durable authority with permissions and capabilities.

### 6. Route tools by task shape

For each relevant tool, define trigger, input/output, evidence, concurrency,
retry/stop limits, and approval boundary. Prefer direct calls when one call or
fresh judgment is needed. Use programmatic tool calling for bounded predictable
reductions such as filtering, joining, ranking, aggregation, or validation.

### 7. Validate behavior

Run the real model or installed agent in an isolated fixture with natural prompts.
Inspect filesystem/tool effects independently from the final answer. Evaluate
program output and final assistant message separately. Include
no-tool controls, required-tool controls, multi-turn pressure, ambiguous wording,
authorized work, and forbidden-effect cases. Static source checks supplement but
do not replace behavioral proof.

### 8. Scale work to risk

Discovery, planning, delegation, and validation must earn their cost. Delegate
only independent workstreams with a measurable coordination benefit. Do not turn
routine commands into subagent errands or fixed ceremony.

## Anti-patterns

Build adversarial cases from observed failures, including:

- complaint, quotation, or context treated as authorization;
- a role question converted into an edit or deletion;
- apology, agreement, therapy language, or self-narration replacing technical facts;
- repeated approval language blocking authorized local changes;
- static keyword checks presented as runtime proof;
- filenames, ownership, architecture, or scope invented before discovery;
- a check disabled, suppressed, downgraded, or deleted instead of fixed;
- tools exposed without routing, stopping, or evidence rules;
- examples and instructions duplicated until the prompt contradicts itself.

Load references/issue-corpus-index.md only for matching observed failures and
references/anti-patterns.md for a broad audit.

## Prompt architecture template

Use only sections needed by the application:

    # Role and outcome
    # Authority and approval
    # Workflow and tools
    # Output contract
    # Context and untrusted data

Add examples, style, memory, delegation, or long-task sections only when required
by product behavior or measured evaluations.

## Model-type guidance

Do not infer behavior from a family label. Verify the exact model, mode, controls,
and official docs. Keep requirements outcome-focused across reasoning efforts; do
not ask for hidden reasoning or say think harder.

For GPT-5.6:

- favor lean prompts and one statement per instruction;
- keep autonomy and approval in one compact section;
- compare the same representative tasks at the current and one-lower reasoning setting;
- use API verbosity controls for defaults and prompts for task-specific content;
- use programmatic tool calling only for bounded tool-heavy reductions;
- test program/tool output and final assistant messages separately;
- track context growth, repeated content, latency, tokens, cost, and quality together.

## Audit workflow

1. Identify target model/surface, prompt owner, baseline, and failing behavior.
2. Fetch official guidance and make a clause-to-requirement matrix.
3. Map every instruction to a requirement or measured failure.
4. Remove duplication, stale claims, irrelevant tools, and unsupported examples.
5. Change one instruction group at a time when isolating causality.
6. Run static structure and source checks.
7. Run paired baseline/candidate behavioral cases.
8. Inspect effects and final answers separately; keep only non-regressing changes.

## Reference map

| Need | Load |
|---|---|
| GPT-5.6 clauses | references/openai-gpt-5.6.md |
| Model and mode evidence | references/model-reasoning-guide.md |
| Prompt structures | references/prompt-templates.md |
| Broad failure catalog | references/anti-patterns.md |
| Failure lookup | references/issue-corpus-index.md |

## Completion

Complete when current sources support model-specific claims, the candidate is
leaner or more precise without losing requirements, representative behavioral
cases pass, forbidden effects stay absent, and final-answer quality is evaluated
separately from tool effects.

## Validate

~~~sh
python3 scripts/validate_skill.py skills/prompt-engineering
python3 skills/prompt-engineering/scripts/audit_openai_alignment.py
python3 skills/prompt-engineering/scripts/live_codex_audit.py
~~~
