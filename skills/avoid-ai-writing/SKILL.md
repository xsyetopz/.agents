---
name: avoid-ai-writing
description: AI-style prose patterns, rhetoric, formatting, voice-preserving edits; excludes authorship and plagiarism claims.
---

# Avoid AI Writing

Find concrete rhetoric and formatting defects, then make only the changes authorized by the requested mode. Do not infer who authored text.

## When to use

- Detect formulaic openings, empty intensifiers, generic transitions, repetitive syntax, vague attribution, or canned conclusions.
- Edit or rewrite prose while preserving a named voice, audience, register, facts, citations, terminology, and requested format.
- Audit a generated draft at sentence, paragraph, structural, or Markdown level.

## When NOT to use

- Authorship or AI-origin detection, plagiarism, originality scoring, or policy-evasion requests.
- Factual, legal, medical, citation, or source verification as the primary task.
- Code cleanup or documentation architecture without a prose-style request.
- Exact imitation of a living writer; preserve user-provided traits instead.

## Guardrails

- Report observable language evidence, never authorship probabilities or origin claims.
- Preserve claims, numbers, names, links, citations, code, terminology, and user-specified voice unless explicitly authorized to change them.
- Do not add anecdotes, feelings, uncertainty, slang, deliberate errors, fabricated sources, or new claims to appear human.
- Treat word tables as search aids, not automatic deletion lists; choose the narrowest correction that fixes the observed effect.

## Workflow

1. Classify the mode: Detect, Edit, or Rewrite; infer the narrowest mode if unspecified.
2. Establish audience, medium, voice traits, and preservation constraints.
3. Read the complete artifact, then load only relevant pattern references.
4. Identify evidence by location and explain its concrete rhetorical effect.
5. Apply surgical edits or rewrite while retaining meaning and constraints.
6. Re-read for factual drift, voice drift, rhythm, formatting, and newly repeated patterns.

## Quick start

Choose `detect`, `edit`, or `rewrite`; read the whole artifact; then load [rhetoric patterns](references/rhetoric-patterns.md), [sentence structure](references/sentence-structure.md), or [formatting](references/formatting.md) as needed. Use [severity tiers](references/severity-tiers.md) to calibrate findings.

## Reference map

- [Reference index](references/index.md) for trigger-based route selection.
- High-signal words and phrases: [word tables](references/word-tables.md).
- Sentence rhythm and syntax: [sentence structure](references/sentence-structure.md).
- Rhetorical evidence: [rhetoric patterns](references/rhetoric-patterns.md).
- Headings and document shape: [structural patterns](references/structural-patterns.md).
- Markdown and layout: [formatting](references/formatting.md).
- Severity, audience, and voice calibration: [severity tiers](references/severity-tiers.md).

## Completion

Complete when the requested mode is honored, each material change is tied to an observed effect, preserved content remains intact, and a final read finds no factual, voice, rhythm, or formatting regression.

## Validation

Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package. Static checks cover package structure only; prose quality and authorship boundaries still require review of the result.

## Related skills

- `$repo-docs` for README and changelog structure.
- `$prompt-engineering` for agent-facing prompt design.
- `$repo-governance` for durable contributor and policy documents.
