# Formatting Rules

Typography and visual formatting patterns that signal AI-generated text. Load
when auditing document-level formatting, layout, and typographic tells.

Scope: local-policy editing heuristics. The corpus note below is an internal
observation, not evidence of authorship.

---

## Em dashes (— and --)

Replace with commas, periods, parentheses, or rewrite as two sentences. Target:
zero. Hard max: one per 1,000 words. Catch both the Unicode em dash (—) and the
double-hyphen substitute (--).

Carve-outs (don't count toward the rate):

- List separator: `- **Term** — description` or `- [- link text] — description`
  where the em dash separates a bold lead term or markdown link from its gloss.
- Changelog version headings: `## [3.21.0] — 2026-07-30` (see [Keep a
  Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)). Adapted from #67.
- Bold-lead parentheticals in lists: `- **Lingering-attention claims**
  (\`lingering-attention\`) — the share-post frame...` where a parenthetical or
  inline code follows the bold lead before the em dash. Adapted from #67.

Only the list-item form qualifies: a mid-sentence splice still counts, a
line-initial `**Bold lead** — full sentence` outside a list still counts, and
the double-hyphen substitute is never carved out.

**Measured signal note.** On the repo corpus (RAID 2024 + HC3 Dec 2022), em
dashes fire on 9.9% of human paragraphs and 1.9% of machine paragraphs — lift
0.2. Em dashes weakly correlate with human authorship on this pre-2025 corpus.
Treat the rate ceiling as stylistic advice (em-dash pileups make prose
breathless), not an authorship signal. Mention the human correlation in detect
mode. Remeasure when the corpus covers current models (#72, #73).

### Bold overuse

Strip bold from most phrases. One bolded phrase per major section at most, or
none. If something's important enough to bold, restructure the sentence to lead
with it instead.

### Emoji in headers

Remove entirely. No `## 🚀 What This Means`. Exception: social posts may use one
or two emoji sparingly — at the end of a line, never mid-sentence.

### Excessive bullet lists

Convert bullet-heavy sections into prose paragraphs. Bullets only for genuinely
list-like content (feature comparisons, step-by-step instructions, API
parameters).

### Curly quotation marks and apostrophes

Curly quotes (U+201C/U+201D) and apostrophes (U+2018/U+2019) are a *weak*
paste-from-chat signal — meaningful in plain-text contexts (code comments,
commit messages, plaintext drafts) where nothing auto-curls. Word, Google Docs,
macOS, and iOS curl quotes by default, so most human prose contains them. Don't
flag curly apostrophes (U+2019) on their own. Replace with straight quotes in
plain-text/code; leave them in finished publications and locale-correct
punctuation (French « », German „ ").

### Immaculate typography in casual registers

Same tier as curly quotes — a *weak*, register-scoped signal. Perfect spacing,
punctuation, and capitalization in a context where humans type fast (issue/PR
comments, chat, DMs) is corroborating evidence, not proof. When editing a
human's casual text, preserve their typos, contractions, and idiosyncratic
capitalization rather than correcting them.

### Title case headings (#62)

AI over-capitalizes headings. Use sentence case for subheadings. **Detector
note:** the regex now matches both plain-text title-case lines and Markdown
headings (prefixed `#{1,6}`):
`/^(?:#{1,6}\s+)?([A-Z][a-z]+(?:\s+(?:[A-Z][a-z]+|and|or|of|the|in|for|to|a|an))+\s+[A-Z][a-z]+)\s*$/gm`

### Inline-header lists / Bold-first bullets

Bullet lists where each item starts with a bold header: "**Performance:**
Performance improved by..." Strip the bold header and write the point directly.

### List-label periods

In bulleted lists with short labels, LLMs end the label with a period instead
of a colon. "**Intros.** Years of conferences..." → "**Intros:** years of
conferences..." Carve-outs: when the label span is a full sentence on its own,
the period is correct.

### Hyphenated-pair overuse

AI stacks compound modifiers: "a high-quality, well-architected, future-proof
solution." Cut to the modifier that actually matters. Also: hyphenated before
the noun, unhyphenated after a linking verb — AI frequently gets this wrong.

## Sources

- [Package source map](sources.md); verify the linked source record before relying on current or external claims.
