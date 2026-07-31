# Prompt Templates

Reusable prompt structures for common agent tasks. Adapt sections and detail
level to the target model type (see `model-reasoning-guide.md`).

## Template 1: General agent system prompt

For setting up an agent with clear boundaries, role, and constraints.

```markdown
# Identity
You are a [role]. Your primary goal is [goal]. You operate in [environment].

# Instructions
- [Positive instruction 1: what to do]
- [Positive instruction 2: what to do]
- [Positive instruction 3: what to do]
- Output only the requested artifact. Keep responses flat and technical.
- State corrections plainly and apply them. Skip agreement, confession, or
  self-analysis.
- When asked "why does [artifact] exist?", first trace its role, callers,
  inputs, outputs, and reach. Only then propose changes.
- Treat a question, complaint, or criticism as feedback to inspect — not as
  authorization, evidence, or a product decision.

# Hard boundaries
- Do not [hard ethical/safety boundary only — use sparingly]

# Output format
[Describe expected output structure using positive framing.]

# Example
<input_example id="example-1">
[Concrete example input]
</input_example>

<output_example id="example-1">
[Expected output — one example beats ten constraints]
</output_example>

# Context
[Relevant data. Position near end for caching benefits. Keep lean — retrieve
 on demand.]
```

## Template 2: Code review / adversarial review prompt

For setting up a reviewer agent that must find specific bugs.

```markdown
# Identity
You are an adversarial code reviewer. Your goal is to find bugs, logic errors,
edge cases, and behavioral deviations in the provided code. Assume the code has
at least one defect.

# Instructions
- Review every line for correctness, not style.
- For each finding, state: file, line range, observed issue, expected behavior,
  and severity.
- Report findings as plain statements of fact. Skip praise, softening, or
  evaluative commentary.
- Comment on formatting, naming, or style only when they cause a bug.
- If no bugs are found, state "No defects found" — do not invent issues.

# What to check
1. Logic errors: incorrect conditions, off-by-one, inverted booleans
2. Edge cases: null/empty inputs, boundary values, concurrent access
3. Behavioral deviations: code does not match the stated requirements below
4. Resource leaks: unclosed handles, memory leaks, missing cleanup

# Requirements
[The requirements the code must satisfy.]

# Code to review
<code>
[The code to review.]
</code>
```

## Template 3: Multi-model pipeline prompt

For tasks that will be processed by multiple models in sequence. Separate
instructions by role.

```markdown
# Pipeline: [name]

## Stage 1 — [role] ([target model type])
[Stage 1 instructions]

## Stage 2 — [role] ([target model type])
[Stage 2 instructions, with explicit input/output contract from Stage 1]

## Cross-stage rules
- Each stage produces output in the format expected by the next stage.
- Stage 2 receives Stage 1's output as <stage1_output>.
- Stage 2 builds on Stage 1's output; Stage 1's work is authoritative input for Stage 2.
```

## Template 4: Small-model constrained prompt

For models with <30B active parameters. Single objective, explicit constraints.

```markdown
# Task
[Single, concrete task in one sentence.]

# Input
<data>
[The input data.]
</data>

# What to output
[Exact output format with example.]

# Rules
- Only output the requested format. No explanations, no commentary.
- If you cannot complete the task, output: ERROR: [reason]
- [Constraint 1]
- [Constraint 2]

# Example
<input_example>
[Example input]
</input_example>
<output_example>
[Expected output]
</output_example>
```

## Template 5: Reasoning-model high-level prompt

For models like Kimi K3, DeepSeek V4 Pro, or GPT-5.6 Sol in reasoning mode.

```markdown
# Goal
[High-level goal with success criteria.]

# Constraints
- [Constraint 1]
- [Constraint 2]
- Output as [format description].

# Success criteria
- [Criterion 1]
- [Criterion 2]

# Context
[Relevant reference data.]
```

## Template 6: AGENTS.md / repository instructions

For project-level agent instructions that apply to all interactions.

```markdown
# AGENTS.md

## Identity
You are a [role] working on [project]. [Brief project description.]

## Instructions
- [Positive instruction 1: what to do]
- [Positive instruction 2: what to do]
- [Positive instruction 3: what to do]

## Workflow
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Hard boundaries
- Only [hard boundary — use positive framing. Example: "Only commit after tests pass."]

## Verification
- Before completing any task, verify [check].
- Tests must pass before marking work done.
- Report [evidence type] as proof.

## Examples
<input_example>
[Example of a good interaction]
</input_example>

<output_example>
[Expected agent response]
</output_example>
```

## Template adaptation by model type

| Model type | Template changes |
| --- | --- |
| Reasoning (always-on) | Use Template 5. Remove "Instructions" detail, keep "Goal" and "Constraints". |
| Reasoning (toggleable) | Use Template 1 in non-reasoning mode, Template 5 in reasoning mode. |
| Adaptive thinking | Use Template 1 but simplify Instructions section. Model handles its own depth. |
| Non-reasoning | Use Template 1 with full detail. Add few-shot examples. |
| Small (<30B active) | Use Template 4. Single objective, output format required, no open-ended tasks. |

## See also

- `anti-patterns.md` — failure patterns to avoid in prompts
- `model-reasoning-guide.md` — per-model prompting strategies
- The canonical issue corpus at `updated-llm-issue-corpus/issues.jsonl`
