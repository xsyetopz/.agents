---
name: avoid-ai-writing
description: >
  Use to detect AI-isms or humanize this/rewrite prose while preserving voice; not plagiarism, authorship, or factuality analysis.
---

# Avoid AI Writing

Find concrete prose defects and repair only what the requested mode authorizes.
Do not claim to determine whether a human or model authored text.

## What this skill is and isn't

This is a style and rhetoric audit. It identifies observable patterns such as
formulaic openings, empty intensifiers, repetitive sentence shapes, generic
transitions, unnecessary headings, vague attribution, and canned conclusions.
It is not an AI detector and must not assign authorship probabilities.

## When to use

- The user asks to remove AI-isms, robotic tone, generic phrasing, or canned prose
- Editing should preserve a named voice, audience, register, or publication style
- The user wants findings only, surgical edits, or a complete rewrite
- A generated draft needs a concrete rhetoric and sentence-level audit

## When NOT to use

- Authorship detection, plagiarism detection, or policy-evasion requests
- Factual, legal, medical, citation, or originality verification as the primary task
- Code cleanup or documentation architecture without a prose-style request
- A request to imitate a living writer exactly; preserve user-provided traits instead

## Modes

- **Detect:** report evidence and suggested corrections; do not modify text.
- **Edit:** make the smallest local changes that remove identified patterns.
- **Rewrite:** rebuild the passage while preserving facts, intent, constraints, and voice.

If the user does not choose, infer the narrowest mode from the request. A request
to audit or identify means Detect. A request to clean up or edit means Edit. A
request to rewrite means Rewrite.

### Invocation

Natural language is sufficient. Optional controls include:

- mode: detect, edit, or rewrite
- audience and medium
- voice sample or explicit voice traits
- preserve list: facts, citations, headings, terminology, length, formatting
- tolerance: conservative, balanced, or aggressive

## Quick start

1. Establish mode, audience, voice, and preservation constraints.
2. Read the whole artifact before editing isolated lines.
3. Load only the relevant pattern references.
4. Identify evidence by location and explain the concrete effect.
5. Apply the narrowest correction that fixes the effect.
6. Re-read for meaning, factual drift, voice drift, rhythm, formatting, and new repetition.

## Editing rules

- Preserve claims, numbers, citations, names, code, links, and domain terminology unless explicitly asked to change them.
- Replace empty abstraction with specific meaning already supported by the source.
- Vary sentence structure only when rhythm is actually repetitive.
- Remove headings only when they fragment a short argument; keep headings that aid navigation.
- Do not add personal anecdotes, emotions, slang, uncertainty, or opinions not present in the source.
- Do not introduce deliberate errors to appear human.
- Treat word lists as search aids, not automatic deletion rules.

## Reference map

| Need | Load |
|---|---|
| High-signal words and phrases | references/word-tables.md |
| Sentence rhythm and syntax | references/sentence-structure.md |
| Rhetorical patterns | references/rhetoric-patterns.md |
| Structural and heading patterns | references/structural-patterns.md |
| Markdown and formatting | references/formatting.md |
| Finding severity | references/severity-tiers.md |

## Output format

### Rewrite mode

Return the rewritten artifact first. Follow with a short change note only when it
helps review or the user asks for one.

### Detect mode

Report a compact table:

| Location | Evidence | Effect | Suggested correction | Severity |
|---|---|---|---|---|

Do not reproduce long source passages.

### Edit mode

Return the edited artifact or apply the edit in place. List only material changes
and unresolved ambiguities.

### Score interpretation note (#70)

If a tool emits a style score, describe it as heuristic coverage of configured
patterns. It is not authorship probability and does not prove human or AI origin.

## Tone calibration

Infer tone from the source and audience. Prefer concrete writing choices such as
shorter sentences, direct verbs, fewer headings, or retained technical terms over
broad labels such as warm, professional, or human.

### Never inject these

- fabricated experiences, quotations, sources, or personal feelings
- fake uncertainty, typos, grammatical errors, or random slang
- therapy language, social validation, or apology unless the source requires it
- new claims added only to make prose seem less generated

## Completion

Complete when the requested mode is honored, every material change is supported by
an identified prose effect, preserved content remains intact, and a final read
finds no new rhetorical or formatting regression.

## Related skills

- repo-docs for README and CHANGELOG structure
- prompt-engineering for agent-facing instructions
- repo-governance for AGENTS.md and contributor policy
