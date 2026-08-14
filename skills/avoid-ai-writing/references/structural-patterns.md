# Structural Patterns

Paragraph-level and document-level structural AI writing patterns. Load when
auditing text flow, paragraph rhythm, and overall document organization. For
sentence-level rules, see `sentence-structure.md`. For specific named
patterns, see `rhetoric-patterns.md`.

---

## Structural issues

### Rhythm and uniformity

**Structure is the #1 detection signal.** Measured on the repo corpus, rhythm
uniformity discriminates human from machine text at **11.7x lift** — an order
of magnitude stronger than vocabulary (0.9x). This aligns with independent
findings: StoryScope (Russell et al. 2026) reaches 93.2% F1 on discourse-level
features alone (#71). Fixing every word on the Tier 1 list while leaving the
rhythm untouched does not address the structural signal.

- **Sentence length uniformity**: When most sentences are 15–25 words, mix short
  punchy sentences (3–8 words) with longer flowing ones (20+). Fragments work.
- **Paragraph length uniformity**: If every paragraph is 3–5 sentences and
  roughly the same size, vary deliberately. Some paragraphs should be one
  sentence. Some should be longer.
- **Vocabulary repetition vs. synonym cycling**: AI either repeats the same word
  mechanically or cycles through synonyms conspicuously. Human writers repeat
  when the word is right and vary when it's natural.
- **Read-aloud test**: If the text sounds like a text-to-speech engine, it's
  probably too uniform.
- **Missing first-person perspective**: Where appropriate, the writer should
  have opinions. AI is relentlessly neutral.
- **Over-polishing**: Aggressively editing out every irregularity can push human
  writing toward AI statistical profiles. Don't sand away all personality.

### Uniform paragraph length

Vary deliberately. Include some 1-2 sentence paragraphs and some longer ones.
If every paragraph is roughly the same size, fix it.

### Formulaic openings

If the piece opens with broad context before getting to the point ("In the
rapidly evolving world of..."), rewrite to lead with the news or the insight.

### Suspiciously clean grammar

Don't sand away all personality. Deliberate fragments, sentences starting with
"And" or "But," comma splices for effect: if the natural voice uses them, keep
them.

### Paragraph-reshuffle immunity (structure test)

Test by swapping two body paragraphs. If the order does not matter, the text is
a list of points rather than an argument that builds.
Establish a through-line where each paragraph depends on the one before it.

### Treadmill effect / low information density (content test)

Read each paragraph and ask "what's actually new here?" AI prose frequently
restates the premise in fresh words instead of advancing it. When 40-60% can be
cut without information loss, cut it.

### Excessive structure

- Too many headers: more than 3 headings in under 300 words is almost always AI
- Too many list items: 8+ bullet points in under 200 words → should be prose
- Formulaic section headers: "Overview," "Key Points," "Summary" — use headers
  that tell the reader something specific
- Fragmented headers: a heading followed by a one-line warm-up that restates it
  ("## Performance", then "Speed matters.") — cut the warm-up

### When to rewrite from scratch vs. patch

If the text has 5+ flagged vocabulary hits across multiple categories, 3+
distinct pattern categories triggered, and uniform sentence/paragraph length,
patching won't fix it — the structure itself is AI-generated. Advise a full
rewrite.
