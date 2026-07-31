---
name: prompt-engineering
description: >
  Design, audit, debug, or adapt prompts and system instructions for LLMs and agents. Covers model-agnostic principles, model-type-specific guidance, anti-patterns from the LLM issue corpus, and structured prompt architecture. Use when writing AGENTS.md, SKILL.md, system prompts, or any agent-facing instructions.
---

# Prompt Engineering

Design, audit, and adapt prompts for LLMs and agents. Language-agnostic,
model-agnostic, format-agnostic. Grounded in observed failure patterns from a
corpus of 118 real-world LLM behavioral issues.

## When to use

- Writing or revising system prompts, AGENTS.md, SKILL.md, or agent instructions
- Debugging prompts that produce unreliable or systematically wrong behavior
- Adapting prompts for different model architectures (reasoning vs
  non-reasoning, large vs small)
- Auditing existing prompts for known failure patterns
- Designing multi-model pipelines where each model needs different prompting
- Creating or updating reusable prompt templates for a project

## When NOT to use

- For one-shot queries where prompt structure doesn't matter
- For runtime behavior that should be handled by tools or code, not prompt text
- For model selection or benchmarking — this skill covers how to prompt, not
  which model to pick
- When the failure is in the tool layer (API errors, parsing bugs), not the
  prompt

## Core principles

### 1. Chain of command

Define explicit authority levels. System/developer instructions override user
messages; user messages override assistant history. Never let lower-authority
content silently override higher-authority constraints.

For OpenAI: `developer` > `user` > `assistant`. For Anthropic: `system` >
messages. For agent frameworks: AGENTS.md or equivalent system-level
instructions take priority.

### 2. Prefer positive framing — the Pink Elephant Problem

Telling an LLM "don't do X" forces it to process X to know what to avoid, often
making X more likely to appear in the output. This is the **Pink Elephant
Problem** (Ironic Process Theory applied to LLMs). Negative instructions like
"never create duplicate files" or "don't use library X" are unreliable.

**Anthropic's official guidance**: "Tell Claude what to do instead of what not
to do." Reframe prohibitions as positive, explicit commands.

| Negative (less effective) | Positive (more effective) |
|---|---|
| "Don't use mock data." | "Only use real-world data." |
| "Don't use library X for state management." | "Only use library Y for state management." |
| "Avoid creating new files for fixes." | "Apply all fixes to the existing files." |
| "Never output code with overly descriptive comments." | "Write professional, concise code comments." |
| "Do not use markdown in your response." | "Your response should be composed of smoothly flowing prose paragraphs." |

**When negative constraints are appropriate**: use them sparingly for hard
boundaries — unethical behavior, safety rules, or cases where a positive
alternative would be ambiguous. Anthropic's system prompts use third-person
descriptive statements ("Claude does not provide information that could be
used...") rather than imperative negative commands.

**The "Show, Don't Tell" principle**: background context and character traits
given to a model tend to leak into the output as explicit statements. If you
tell the model "this character has a strict moral code," expect dialogue about
morals. Instead, show the trait through actions and let the model infer it from
context. Give the background as implicit context, not stated rules.

### 3. Examples over prohibitions

One good example does more work than ten negative constraints. When output
format or behavior is nuanced, include 1–3 concrete examples showing the
desired output. This is especially important for creative writing, tone
control, and format adherence.

When providing examples:
- Label each example explicitly with IDs
- Show diverse inputs, not just the happy path
- Match example format exactly to the expected output format
- Reasoning models (Kimi K3, DeepSeek V4 Pro, GPT-5.6 Sol) often perform better
  zero-shot — try without examples first

### 4. Efficiency — shortest path, no overthinking

Every tool call has a cost in time and context. Take the minimal path:

- **Verify once, act once**. Don't re-read the same file. Don't re-grep the same
  pattern. One read + one grep should cover 90% of verification.
- **Parallel reads**. When you need multiple files, read them in one batch — not
  one per turn.
- **If the answer is obvious, give it**. Don't search for 10 related issues,
  load 5 reference files, and check 3 anti-patterns before answering a simple
  question. Trust the trigger → recognize the pattern → act.
- **Cut to the chase**. Skip narration ("I'll now check..."), skip
  self-analysis ("I made X when..."), skip process logging. The user wants
  the correction, not the story of how you got there.
- **One tool call that reads the right file beats three that read wrong ones**.
  If you're not sure which file to read, ask rather than guessing and then
  correcting.

Counter-example of overthinking:
```
# WRONG — 8 tool calls for a simple correction
1. Read SKILL.md
2. Grep for "complaint" in all files
3. Read anti-patterns.md
4. Read issue-corpus-index.md
5. Read complaint-is-not-authorization.md
6. Re-read SKILL.md (same file again!)
7. Narrate the analysis for 3 paragraphs
8. Finally propose the fix
```

```
# RIGHT — 2 tool calls
1. Read the file the user pointed at
2. Grep for callers
→ State the fix. Done.
```

### 5. Prompt as kernel, not operating system

The prompt should define behavior, priorities, and routing — not carry all
knowledge. Long prompts that encode the entire system become fragile. Instead:

- Keep the prompt lean: identity, instructions, decision rules, output format
- Retrieve knowledge on demand (files, docs, context packets)
- Use reference files and progressive disclosure rather than inlining everything
- A shorter prompt that retrieves context is more reliable than a mega-prompt
  that encodes it all

### 6. Structure with delimiters

Use Markdown headings and XML tags to separate sections. Delimiters help models
distinguish instructions from examples from context. Position cacheable content
at the beginning of the prompt.

Preferred delimiters:
- XML tags for structured data blocks: `<example>`, `<context>`, `<input>`,
  `<output>`
- Markdown headings for instruction sections: `# Identity`, `## Instructions`
- Triple backticks for code or verbatim content

### 7. Version prompts in code

Store prompts in version-controlled files alongside the code they govern. Use
typed arguments or template variables for dynamic values. Test with
representative fixtures and evaluation checks before changing production
prompts.

## Model-type guidance

Different model architectures need different prompting strategies. The table
below summarizes key families and their prompting implications.

| Model type | Families | Prompting approach |
|---|---|---|
| Reasoning (always-on) | Kimi K3 | High-level goals, no step-by-step. Thinking always active; control output constraints only. |
| Reasoning (toggleable) | DeepSeek V4 Pro/Flash, GLM-5.2, GPT-5.6, Qwen3.6 27B | Goal-oriented in reasoning mode; explicit steps in non-reasoning mode. |
| Adaptive thinking | MiniMax-M3 | Effort labels enable/disable thinking mode; don't try to tune depth. Structure but don't over-specify. |
| Non-reasoning | GLM-4.7-Flash (non-reasoning mode) | Explicit, detailed step-by-step instructions. Few-shot examples are high-impact. |
| Small models (<30B active) | Qwen3.6 27B, GLM-4.7-Flash, gpt-oss-120b | Single objective per prompt. Short, concrete instructions with acceptance criteria. Avoid open-ended tasks. |

**Reasoning effort controls**:

- Models that support `reasoning_effort`: Kimi K3 (low/high/max), DeepSeek V4
  (high/max), GLM-5.2 (low/high/max), GPT-5.6 (low/medium/high/xhigh/max),
  Qwen3.6 27B (low/high/max), gpt-oss-120b (low/medium/high)
- Models where effort labels don't tune depth: MiniMax-M3 (only toggles adaptive
  thinking on/off), Kimi K2.7 Code (fixed reasoning), GLM-4.7-Flash (reasoning
  mode toggle)
- Higher effort = deeper internal reasoning, not different output structure.
  Don't change prompt format when changing effort level.

See `references/model-reasoning-guide.md` for detailed per-model guidance.

## Prompt architecture template

A well-structured prompt follows this template. Adapt section order and detail
to the target model type (see model-type guidance above).

```markdown
# Identity
You are a [role]. Your primary goal is [goal].

# Instructions
- [Positive instruction 1: what to do]
- [Positive instruction 2: what to do]
- [Positive instruction 3: what to do]

# Hard boundaries (use sparingly)
- Do not [hard ethical/safety boundary only]

# Output format
[Describe expected output structure, format, and constraints. Use positive
 framing: "Output as plain JSON" not "Don't use markdown."]

# Examples
<input_example id="example-1">
[Concrete example input]
</input_example>

<output_example id="example-1">
[Expected output for that input — one good example outweighs ten constraints]
</output_example>

# Context
[Relevant data, documents, or reference material. Position near end
 for prompt caching benefits. Keep this section lean — retrieve on demand.]
```

## Anti-patterns

The skill embeds a deduplicated catalog of LLM behavioral failure modes,
consolidated from 118 observed patterns into 54 focused entries across 18
categories. Each entry includes concrete bad forms, required behavior, and
falsifiable acceptance checks extracted from real-world agent interactions.

| # | Category | Entries | Core failure |
|---|---|---|---|
| 1 | Pink Elephant / Negative Backfire | 1 | "Don't do X" primes model to do X |
| 2 | Show, Don't Tell Leakage | 1 | Background rules leak into explicit output |
| 3 | Social Mirror / Verbatim Echo | 1 | Prompt labels echoed verbatim in output |
| 4 | Artifact-Role Confusion | 4 | Answers "why?" with removal promise, not role |
| 5 | Complaint Mirroring & Feedback Misuse | 3 | Treats frustration as authorization/evidence |
| 6 | Scope, Consent & Agency | 4 | Turns proposal/question into decision without consent |
| 7 | Abstract Reframing & Pattern-Fill | 5 | Replaces concrete correction with new abstraction |
| 8 | Need Claims & Utility Verdicts | 2 | Declares artifact unnecessary before tracing role |
| 9 | Script & Tool Role Evasion | 3 | Answers script challenge with removal before trace |
| 10 | Prose Policing & Runtime-Proof | 2 | Creates tooling to check wording, not behavior |
| 11 | Tone, Meta-Commentary & Self-Confession | 2 | Narrates process, confesses, adds therapeutic language |
| 12 | Prompt Boundary & Intent | 4 | Misinterprets instruction scope, treats policy as optional |
| 13 | Deletion & Cleanup Reflexes | 4 | Preserves cleanup paths for mistakes instead of removing them |
| 14 | Documentation Orbit & Harness Drift | 4 | Updates docs while product work is expected |
| 15 | Memory & State Confusion | 3 | Conflates chat context with persistent memory |
| 16 | Naming, Spec & Architecture Invention | 6 | Invents names/specs before proving domain role |
| 17 | Source Truth, Version & Example Claims | 5 | Treats example values as authority; changes from familiarity |
| 18 | Other Structural Failures | 3 | SRP violations, conclusion smuggling, proposal churn |

**See `references/anti-patterns.md` for the full catalog** — every entry with
bad forms, required behavior, and acceptance checks. Use
`references/issue-corpus-index.md` for quick category-to-file lookup.

## Prompt auditing workflow

When auditing an existing prompt against the issue corpus:

1. **Read the prompt** — note its stated purpose, target model type, and density
   of negative instructions.
2. **Run the anti-pattern checklist** — scan `references/anti-patterns.md` and
   mark every pattern the prompt could trigger.
3. **Check model compatibility** — verify the prompting strategy matches the
   target model's reasoning mode (see `references/model-reasoning-guide.md`).
4. **Reframe negatives to positives** — for every "do NOT," ask: can this be
   restated as a positive "only do X"? Keep only hard-boundary negatives.
5. **Add examples** — for any nuanced behavior, add 1–3 concrete examples of the
   desired output rather than piling on more constraints.
6. **Test with adversarial inputs** — try inputs designed to trigger each
   anti-pattern. Confirm the prompt resists them.
7. **Version the change** — store the revised prompt with a clear commit message
   naming which anti-patterns were addressed.

## Reference map

| If you need to... | Load |
|---|---|
| Understand model reasoning modes, effort controls, and per-family prompting | `references/model-reasoning-guide.md` |
| Audit a prompt against all 118+ failure patterns with bad forms and checks | `references/anti-patterns.md` |
| Quick-search any issue by keyword | `references/issue-lookup.md` |
| Browse issues by category with trigger conditions | `references/issue-corpus-index.md` |
| See prompt templates for specific tasks | `references/prompt-templates.md` |
| Dive into a specific issue with diff-style (❌→✅) contrast | `references/issues/<category>/<id>.md` |

## Related skills

- `skill-creator` — authoring agent skills with SKILL.md
- `avoid-ai-writing` — removing AI-isms from generated prose
- `architecture-design` — system prompts as architectural decisions
- `repo-governance` — AGENTS.md and governance documents
- `kf-adversarial-review` — adversarial review of generated output
- `kf-process-fix` — fixing root causes of recurring failures

## Validate

From the repository root:

```sh
python3 scripts/validate_skill.py skills/prompt-engineering
```
