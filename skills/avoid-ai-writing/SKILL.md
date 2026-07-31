---
name: avoid-ai-writing
description: Audit and rewrite content to remove AI writing patterns ("AI-isms"). Use when asked to "remove AI-isms," "clean up AI writing," "edit writing for AI patterns," "audit writing for AI tells," or "make this sound less like AI." Supports detect-only, edit-in-place, and full rewrite modes with optional voice profiles.
license: MIT
metadata:
  author: Conor Bronsdon
  tags: writing editing voice quality
---

# Avoid AI Writing

Audit and rewrite text to remove AI writing patterns that make prose sound
machine-generated. Operates in three modes: **rewrite** (flag + fix),
**detect** (flag only), and **edit** (fix in place with minimal edits).

## What this skill is and isn't

This is a **writing-quality tool**, not a verdict. The patterns here are
statistically more common in LLM output, but humans under deadline pressure, in
unfamiliar genres, or writing in a second language produce the same shapes.
Independent audits of commercial AI detectors have found false-positive rates
above 60% on non-native English writers (Liang et al., Stanford, *Patterns*
2023). Adversarial paraphrase reduces detection accuracy by ~88% (arXiv:
2506.07001, 2025).

**Corpus limitation (#72).** The machine-written corpus used to measure
detection rates (RAID 2024 + HC3 Dec 2022) contains no post-2024 models.
Several rules may be measuring model habits that have shifted. Until a
current-model corpus covering the registers this skill targets (LinkedIn
posts, blog drafts, release notes) lands, treat all measured lift values as
approximations of an older model era.

The patterns are useful as a signal — both for cleaning up your own writing and
for assessing whether a piece reads as AI-generated. Don't make them the sole
basis for a consequential decision (academic integrity, hiring, publication).
Pair the signal with context: who wrote it, what genre, what the writer's
normal voice looks like.

In short: signals, not proof.

## When to use

- User says "remove AI-isms," "clean up AI writing," "make this sound less like AI"
- User says "audit writing for AI tells," "scan this for AI patterns"
- User says "edit this file to remove AI writing"
- User wants to check if text reads as AI-generated
- Content was pasted from a chat UI and needs cleanup

## When NOT to use

- For a single typo or grammar fix not related to AI patterns
- On quoted material, code blocks, or text attributed to someone else
- On text where the writer explicitly wants to preserve AI style

## Modes

**`rewrite`** (default) — Flag AI-isms and rewrite the text to fix them.

**`detect`** — Flag AI-isms only. No rewriting. Use when the writer wants to
see what's flagged and decide what to fix themselves, or when auditing text
you don't want altered.

**`edit`** — Edit a file in place with minimal, targeted edits. Preserve
passages that are already human. Don't edit quoted material or code blocks.
After editing, re-read the file and confirm the flagged patterns are resolved.

### Invocation

Natural language is enough ("rewrite this in a blunt voice for LinkedIn,"
"edit `post.md` in place," "scan this, don't rewrite"). Explicit options:
`[--mode rewrite|detect|edit]`, `[--voice casual|professional|technical|warm|blunt]`,
`[--context linkedin|blog|technical-blog|investor-email|docs|casual]`,
`[--file PATH]`, `[--iterate N]` (max 2). See `references/severity-tiers.md`
for context profiles and voice definitions.

**Iterate to convergence.** Rewrite mode already runs one corrective second
pass. When the writer asks to "iterate" or passes `--iterate N`, repeat the
audit→rewrite cycle until no patterns remain or N passes (cap N at 2).

## Quick start

1. Determine the mode from user's request (rewrite/detect/edit)
2. If the user names a specific context or voice, apply it; otherwise auto-detect
3. Load `references/formatting.md`, `references/word-tables.md`,
   `references/sentence-structure.md`, `references/structural-patterns.md`,
   and `references/rhetoric-patterns.md` to audit against the full pattern
   catalog
4. Load `references/severity-tiers.md` if you need priority guidance or context
   profiles
5. Follow the output format for the chosen mode (below)

## Reference map

| If you need to... | Load |
|---|---|
| Check formatting and typography tells | `references/formatting.md` |
| Replace AI-vocabulary words (Tier 1A/1B/2/3) | `references/word-tables.md` |
| Audit sentence-level phrasing and transitions | `references/sentence-structure.md` |
| Audit paragraph flow and document structure | `references/structural-patterns.md` |
| Check for specific named patterns | `references/rhetoric-patterns.md` |
| Prioritize what to fix first (P0/P1/P2) | `references/severity-tiers.md` |
| Apply audience-specific strictness | `references/severity-tiers.md` (Context profiles) |
| Match a specific voice/persona | `references/severity-tiers.md` (Voice profiles) |
| Understand the spec and structure | `agents/openai.yaml`, `.skill-validator.json` |

## Output format

### Rewrite mode

Return four sections:

1. **Issues found** — bulleted list of every AI-ism identified, with offending
   text quoted
2. **Rewritten version** — full rewritten content. Preserve original structure,
   intent, and all specific technical details
3. **What changed** — brief summary of major edits
4. **Second-pass audit** — re-read the rewrite. Identify and fix any remaining
   tells. If clean, say so

### Detect mode

Return two sections:

1. **Issues found** — bulleted list grouped by severity (P0, P1, P2). Keep Tier
   1B clarity edits visually separate from Tier 1A markers: a wordiness fix is
   a writing suggestion, not evidence about who wrote the text. Per the measured
   data (#71), structural signals (11.7x lift) are the stronger discriminator;
   vocabulary (0.9x) is a convention, not verified authorship evidence.
2. **Assessment** — for each flag, note whether it's a clear problem or a
   judgment call. Call out which to definitely fix vs. worth a second look

### Edit mode

After editing the file in place, return a short report:

1. **Edits made** — bulleted list of changes with before → after. Only the
   spans you touched
2. **Verification** — confirm re-read and resolution. Note anything deliberately
   left alone

### Score interpretation note (#70)

The detector engine's 0-100 score clusters in a narrow band (0-11 on the
current corpus) because the divisor `Math.log2(wordCount/50)` compresses
paragraph-level scores. A score of 4 ("Minimal AI signals") can appear on
fully machine-generated text at paragraph length. Treat the numeric score as a
coarse relative signal; rely on the per-category breakdown and pattern list for
decisions. When the corpus is recalibrated on current-model data (#72), the
score range will be re-normalized to meaningful percentiles.

## Tone calibration

Five principles for human-sounding rewrites:
1. **Vary sentence length** — mix short with long. Fragments are fine
2. **Be concrete** — replace vague claims with numbers, names, dates, or examples
3. **Have a voice** — use first person, state preferences, show reactions where
   appropriate
4. **Cut the neutrality** — humans have opinions. If the piece takes a position,
   take it
5. **Earn your emphasis** — don't tell the reader something is interesting. Make
   it interesting

Removal is half the job. A rewrite that clears every flag but reads sterile is
still recognizably machine output. For encyclopedic, technical, or legal text,
neutral and plain is the correct human voice; don't inject personality there.

If the original writing is already strong, make only the necessary cuts. The
replacement table in `references/word-tables.md` provides defaults, not mandates.

### Never inject these

These must never be **added** to a text that did not already contain them:

- **Fake first person.** "I've seen this a hundred times," "in my experience"
  dropped into prose with no author presence. If the source has no `I`, the
  rewrite has no `I`
- **Manufactured stakes.** "In a world where," "now more than ever"
- **Forced contrarianism.** "Everyone says X, but they're wrong." Only
  legitimate when the source actually argued it
- **Performed candor.** "Let's be honest," "real talk," "here's the thing"
- **Em-dash theatrics.** Dashes staged for drama the content has not earned
- **Staccato conversion.** Chopping ordinary sentences into fragments to
  manufacture rhythm
- **Invented specifics.** A number, name, date, tool, or mechanism the source
  never contained. If the concrete detail is missing, flag the gap — never
  fill it

**The test.** For each edit, ask whether the information came from the source.
Subtraction and sharpening are in scope; addition of stance, personality, or
fact is not. Adapted from isatimur/de-slop's guardrails.

## Related skills

- `impeccable` — frontend interface design and polish
- `skill-creator` — create and validate agent skills

## Validate

```sh
python3 scripts/validate_skill.py skills/avoid-ai-writing
```
