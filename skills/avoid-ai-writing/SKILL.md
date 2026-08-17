---
name: avoid-ai-writing
description: AI-style prose patterns, rhetoric, formatting, voice-preserving edits; excludes authorship and plagiarism claims.
---

# Avoid AI Writing

Find observable prose patterns and make only the requested edits. Do not infer who wrote the text.

## Use this skill

- Detect formulaic openings, empty intensifiers, generic transitions, repeated syntax, vague attribution, and canned conclusions.
- Edit or rewrite prose while preserving the requested voice, audience, register, facts, citations, terminology, and format.
- Audit sentence, paragraph, document, or Markdown structure.
- Do not use for authorship, plagiarism, originality, policy evasion, factual, medical, legal, citation, or source verification; code cleanup; or exact imitation of a living writer.
- Redirect repository documentation and policy files to `/skill:repo-docs`, and agent prompt design to `/skill:prompt-engineering`.

## Rules

- Report observable language evidence, never authorship probabilities or origin claims.
- Preserve claims, numbers, names, links, citations, code, terminology, and voice unless the request authorizes a change.
- Do not add anecdotes, feelings, uncertainty, slang, deliberate errors, fabricated sources, or new claims to make text seem human.
- Treat word tables as search aids, not deletion lists. Use the narrowest fix.
- Do not invent custom schema files or custom generated files as outputs. Use only established repository-owned formats and canonical inputs.

## Steps

1. Classify the request as `detect`, `edit`, or `rewrite`.
2. Read the complete artifact and record audience, medium, voice, and content that must not change.
3. Use the reference router to load only material matching the observed issue.
4. Tie each finding to a location and concrete rhetorical effect.
5. Apply the smallest edit that fixes the effect.
6. Re-read for factual drift, voice drift, rhythm, formatting, and new repeated patterns.

## Resources

- Start with the package [reference router](references/index.md).
- Load only the routed package-local reference that matches the observable issue.
- Use the package-local checker, contract, and eval manifest when validation is requested.

## Verify

- Done means the requested mode is followed, each material change has observable evidence, and protected facts, citations, and voice remain intact.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Recheck links, terminology, and formatting in the edited artifact.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark factual, medical, legal, citation, source, or behavioral verification `UNVERIFIED` when it was not performed by the owning process.
