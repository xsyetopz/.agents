---
name: prompt-engineering
description: >
  Design, audit, debug, or adapt prompts and agent instructions. Use current
  provider documentation for named models, measured behavioral failures, and
  executable evaluations rather than generic prompt folklore.
---

# Prompt Engineering

Design and verify prompts as versioned software behavior. Provider guidance for
the named model outranks generic heuristics and this skill's issue corpus.

## When to use

- Writing or revising system prompts, developer instructions, `AGENTS.md`, or
  `SKILL.md`
- Debugging recurring agent behavior or tool-routing failures
- Adapting prompts to a named model, execution mode, or tool surface
- Building behavioral evaluations for prompt changes

## When NOT to use

- Runtime invariants that belong in permissions, schemas, policy engines, or
  application code
- Tool/API failures unrelated to model instructions
- Model selection without an evaluation workload
- A simple answer that needs no reusable prompt artifact

## Source authority

For a named provider or model, read its current official documentation before
giving model-specific advice. Record the URL and retrieval date. Apply sources
in this order:

1. current official documentation for the exact model and product surface;
2. repository contracts and measured local behavior;
3. peer-reviewed or primary research relevant to the failure;
4. this skill's generic guidance and observed issue corpus.

When sources conflict, follow the higher source and state the conflict. Do not
turn unverified model names, benchmark tables, effort tiers, context limits, or
provider behavior into facts. For GPT-5.6, load
`references/openai-gpt-5.6.md` before drafting or auditing.

## Core principles

### 1. Start from a measured outcome

Define the task, target model and surface, available tools, required evidence,
success criteria, and final output. Tie every non-obvious instruction to a
product requirement, observed failure, or evaluated gap.

### 2. Keep the prompt lean

State each instruction once. Keep authority and approval policy in one place.
Expose only relevant tools with concise, precise schemas and error behavior.
Retrieve large reference material on demand instead of duplicating it in the
system prompt.

Remove one instruction group, example group, or tool at a time and rerun the
same representative evaluations. Lower token use or cost counts as an
improvement only when required behavior still passes.

### 3. Define autonomy and approval once

For GPT-5.6 coding agents, use a compact three-part policy:

```text
For requests to answer, explain, review, diagnose, or plan, inspect relevant
materials and report. Implement only when the request also asks for a change.

For requests to change, build, or fix, make the requested in-scope local
changes and run relevant non-destructive validation without asking first.

Require confirmation for external writes, destructive actions, purchases, or
material scope expansion.
```

Name safe local actions when the environment needs them. Repeated variants of
“ask first,” “do not mutate,” and “wait for approval” can over-block expected
local work.

### 4. Use clear constraints, not framing dogma

Positive instructions are useful when they name the desired action or output.
Negative instructions are appropriate for precise boundaries and forbidden
effects. Choose the form that makes the rule least ambiguous; do not apply a
fixed negative-count threshold or claim that mentioning a forbidden action
makes models perform it.

Examples are optional. Keep them when they encode a product requirement or fix
a measured gap. Remove examples that merely repeat instructions. Do not claim
that one example universally outweighs multiple constraints.

### 5. Separate context from authority

Use headings, XML, or fences to identify context, examples, and data. These
delimiters improve interpretation but do not create a security or privilege
boundary. Enforce durable authority with permissions, capabilities, schemas,
reference monitors, or other runtime controls.

### 6. Specify tool routing by task shape

Describe when each tool is used, its input/output shape, evidence requirements,
retry and stopping limits, and which actions require approval. Use direct calls
when one call is sufficient or semantic judgment is needed. Use programmatic
tool calling only for bounded, predictable reductions such as filtering,
joining, ranking, aggregation, or validation.

### 7. Validate behavior, not vocabulary

Run the real model or installed agent in an isolated local fixture. Use natural
user prompts that do not disclose the expected decision. Verify filesystem and
tool effects independently, then evaluate the final answer for required facts,
evidence, caveats, and next actions. Include both no-tool and required-tool
controls, multi-turn pressure, ambiguous wording, and direct authorized work.

Compare the candidate with its baseline on the same cases. Static checks for
required files, source citations, duplicate policy, and unsupported claims are
additional gates; keyword presence is not behavioral proof.

### 8. Scale discovery and validation to risk

Use safe local inspection without asking when it can resolve ownership or
context. Read callers, contracts, and tests that affect the result. Re-read or
expand checks when evidence conflicts, the change is risky, or the first check
cannot prove the behavior. Do not use fixed tool-call counts as an engineering
rule.

### 9. Make delegation earn its coordination cost

Default to direct single-agent execution. Delegate only concrete, independent
outcomes that can run concurrently and whose expected gain exceeds coordination
overhead. Do not delegate ownership discovery, command errands, or work the
root can finish directly. If delegation is challenged, stop further spawning
and report active workers, status, whether each met the delegation threshold,
and the direct next action without agreement theatre or self-narration.

## Anti-patterns

The issue corpus records observed failures, not universal model laws. Use it to
generate adversarial cases after identifying a matching trigger. Deduplicate
overlapping entries and preserve the concrete failure, required behavior, and
falsifiable acceptance check. Do not copy complaint language, self-analysis, or
assistant promises into operational prompts.

High-value categories include:

- complaint or quoted content treated as action authority;
- artifact-role questions answered with an edit promise before tracing role;
- social agreement, apology, or therapy-style narration replacing facts;
- static prose checks presented as runtime proof;
- ownership, filenames, architecture, or scope invented before discovery;
- direct authorized work blocked by repeated approval language.

Load `references/issue-corpus-index.md` only when a measured failure maps to the
corpus. Load `references/anti-patterns.md` for a broad audit.

## Prompt architecture template

Use only sections the application needs:

```markdown
# Role and outcome
[Role, goal, and completion criteria]

# Autonomy and approval
[One compact policy]

# Workflow and tools
[Relevant tools, routing, evidence, retries, stopping]

# Output
[Required facts, structure, caveats, and next action]

# Context
[Authoritative inputs and clearly delimited untrusted material]
```

Examples and style sections are conditional on a product requirement or a
measured gap. See `references/prompt-templates.md`.

## Model-type guidance

Do not infer model behavior from a family label alone. Verify the exact model,
mode, supported controls, and current official docs. Keep outcome-focused
prompts across reasoning efforts; do not ask a model to “think harder” or expose
private reasoning. See `references/model-reasoning-guide.md`.

For GPT-5.6 specifically:

- favor lean prompts and one statement per instruction;
- define autonomy and approval in one compact section;
- use `text.verbosity` for an API-level default and prompts for task-specific
  required content;
- describe concrete writing choices instead of broad tone labels;
- compare standard/pro modes and effort levels on the same representative
  workload rather than assuming maximum effort is best;
- test both program output and the final assistant message.

## Audit workflow

1. Identify the target model, product surface, prompt owner, and baseline.
2. Fetch current official model guidance and build a clause-level matrix.
3. Map each prompt instruction to a requirement or measured failure.
4. Remove duplication, unsupported claims, stale examples, and irrelevant tools.
5. Change one instruction group at a time when isolating causality.
6. Run static source/structure checks.
7. Run paired baseline/candidate rollouts with the real local model or agent.
8. Inspect tool effects and final answers separately; keep the candidate only
   when required behavior passes without regression.

## Reference map

| Need | Load |
|---|---|
| Official GPT-5.6 clauses and audit matrix | `references/openai-gpt-5.6.md` |
| Model/mode evidence rules | `references/model-reasoning-guide.md` |
| Reusable structures | `references/prompt-templates.md` |
| Broad observed failure catalog | `references/anti-patterns.md` |
| Category-to-file lookup | `references/issue-corpus-index.md` |

## Validate

From `/Users/krystian/.agents`:

```sh
python3 scripts/validate_skill.py skills/prompt-engineering
python3 skills/prompt-engineering/scripts/audit_openai_alignment.py
python3 skills/prompt-engineering/scripts/live_codex_audit.py
```
