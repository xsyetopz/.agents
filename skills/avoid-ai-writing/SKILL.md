---
name: avoid-ai-writing
description: AI-style prose patterns, rhetoric, formatting, voice-preserving edits; excludes authorship and plagiarism claims.
---

# Avoid AI Writing

Find observable prose patterns and make only the requested edits. Do not infer
who wrote the text.

## Use this skill

- Detect formulaic openings, empty intensifiers, generic transitions, repeated
  syntax, vague attribution, and canned conclusions.
- Edit or rewrite prose while preserving the requested voice, audience,
  register, facts, citations, terminology, and format.
- Audit sentence, paragraph, document, or Markdown structure.

## Rules

- Report observable language evidence, never authorship probabilities or origin
  claims.
- Preserve claims, numbers, names, links, citations, code, terminology, and
  voice unless the request authorizes a change.
- Do not add anecdotes, feelings, uncertainty, slang, deliberate errors,
  fabricated sources, or new claims to make text seem human.
- Treat word tables as search aids, not deletion lists. Use the narrowest fix.
- Do not use this skill for authorship, plagiarism, originality, policy
  evasion, factual or legal verification, code cleanup, or exact imitation of a
  living writer. Route README and changelog structure to `$repo-docs`, policy
  files to `$repo-governance`, and agent prompt design to `$prompt-engineering`.

## Steps

1. Classify the request as `detect`, `edit`, or `rewrite`.
2. Read the complete artifact and record audience, medium, voice, and content
   that must not change.
3. Load only the references matching the observed issue.
4. Tie each finding to a location and concrete rhetorical effect.
5. Apply the smallest edit that fixes the effect.
6. Re-read for factual drift, voice drift, rhythm, formatting, and new
   repeated patterns.

## Resources

- Route selection: [reference index](references/index.md).
- Words and phrases: [word tables](references/word-tables.md).
- Sentence rhythm and syntax: [sentence structure](references/sentence-structure.md).
- Rhetorical evidence: [rhetoric patterns](references/rhetoric-patterns.md).
- Headings and document shape: [structural patterns](references/structural-patterns.md).
- Markdown and layout: [formatting](references/formatting.md).
- Severity and voice calibration: [severity tiers](references/severity-tiers.md).

## Verify

Run from this package root:

```bash
python3 scripts/check.py
python3 -m json.tool evals/evals.json >/dev/null
```

Pass the package checks, then confirm that the requested mode was followed,
each material change has evidence, and protected facts and voice remain intact.
