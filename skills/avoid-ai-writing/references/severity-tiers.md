# Severity Tiers, Context Profiles, and Voice Profiles

Load this to prioritize what to fix and calibrate strictness for the audience.

Scope: local-policy triage guidance. Severity depends on the requested medium,
audience, voice, and evidence; it is not an authorship score.

---

## Severity tiers

Not all AI-isms are equal. When doing a quick pass or triaging a large document,
prioritize by tier:

### P0 — High-impact clarity and credibility risks (fix immediately)

- Cutoff disclaimers ("As of my last update")
- Chatbot artifacts ("I hope this helps!", "Great question!")
- Vague attributions without sources ("Experts believe")
- Significance inflation on routine events
- Hashtag stuffing on `linkedin` and `investor-email` posts (severity varies by
  profile — lower priority on `blog`/`technical-blog`)

### P1 — Noticeable patterned phrasing (fix before publishing)

- Word-list violations (delve, leverage, harness, robust, etc.)
- Template phrases and slot-fill constructions
- "Let's" transition openers
- Synonym cycling within a paragraph
- Formulaic openings ("In the rapidly evolving world of...")
- Bold overuse
- Generic future-narrative closers ("may become one of the most important
  narratives…")
- Social endorsement closers ("This one is worth your time:", "thank me later")
- Lingering-attention claims ("the line I keep coming back to," "I can't stop
  thinking about this")
- Narrated candor ("I would rather flag this than let you discover it later")
- Hedge-stacked predictions ("could potentially," "may eventually")
- Real/actual adjective inflation ("real on-chain tokenomics")
- Moral-adjective category errors ("honest shape," "flagged honestly")
- Invented contrast-pair mirroring ("false precision rather than genuine
  accuracy")
- Bullet lists of bare noun phrases (5+ short adj+noun items, no verbs)
- Tier 3 phrase clustering (≥3 distinct boilerplate phrases in one piece)

### P2 — Stylistic polish (fix when time allows)

- Generic conclusions ("The future looks bright")
- Compulsive rule of three
- Uniform paragraph length
- Copula avoidance (serves as, features, boasts)
- Transition phrases (Moreover, Furthermore, Additionally)
- Em dash frequency (above 1 per 1,000 words) — **style preference, not
  authorship signal.** Measured on pre-2025 corpus, em dashes weakly correlate
  with human writing (9.9% human vs 1.9% machine, lift 0.2). The rate ceiling
  is defensible stylistic advice; do not present it as evidence of AI
  generation in detect mode (#73).
- Hashtag stuffing (`blog`/`technical-blog` profiles)
- Tier 3 phrase repetition (single phrase ≥2× — fine in isolation, suspect in
  stacks)

Use P0+P1 for quick passes. Full audit covers all three tiers.

---

## Context profiles

Pass an optional context hint to adjust rule strictness. If no context is
specified, auto-detect from content cues (short + hashtags = social, code blocks
= technical, salutation = email, default = blog).

### Profile definitions

**`linkedin`** — Short-form social. Punchy fragments, visual formatting matter.

**`blog`** — Default. Standard long-form prose. All rules apply at full
strength.

**`technical-blog`** — Long-form with code, architecture, APIs. Technical terms
get a pass.

**`investor-email`** — High-trust audience. Tighten everything; promotional
language is the biggest risk.

**`docs`** — Documentation, READMEs, guides. Clarity over voice.

**`casual`** — Slack messages, internal notes, quick replies. Only catch the
worst offenders.

### Tolerance matrix

Rules not listed in the table apply at full strength across all profiles.

| Rule | linkedin | blog | technical-blog | investor-email | docs | casual |
| --- | --- | --- | ---- | --- | --- | --- |
| Em dashes | relaxed (2/post OK) | strict | strict | strict | relaxed | skip |
| Bold overuse | relaxed (bold hooks OK) | strict | strict | strict | relaxed | skip |
| Emoji in headers | relaxed (1-2 end-of-line OK) | strict | strict | strict | skip | skip |
| Excessive bullets | skip (lists work) | strict | relaxed (technical lists OK) | strict | skip (docs) | skip |
| Hedging | strict | strict | relaxed ("may" is accurate) | strict | relaxed | skip |
| Word table (full) | strict | strict | **partial** (see below) | strict | relaxed | P0 only |
| Promotional language | relaxed (some sell OK) | strict | strict | **extra strict** | strict | skip |
| Significance inflation | strict | strict | strict | **extra strict** | relaxed | skip |
| Copula avoidance | skip | strict | relaxed | strict | skip | skip |
| Uniform paragraph length | skip (short-form) | strict | strict | strict | relaxed | skip |
| Numbered list inflation | relaxed | strict | relaxed | strict | skip | skip |
| Rhetorical questions | relaxed (1 as hook OK) | strict | strict | strict | strict | skip |
| Transition phrases | skip (short-form) | strict | strict | strict | relaxed | skip |
| Generic conclusions | skip | strict | strict | **extra strict** | skip | skip |
| Hashtag stuffing | strict | strict | strict | **extra strict** | skip | skip |
| Bullet-NP lists | strict | strict | relaxed (tech option lists OK) | strict | relaxed (params OK) | skip |
| Tier 3 phrase clustering | strict | strict | strict | **extra strict** | relaxed | skip |
| Future-narrative closers | strict | strict | strict | **extra strict** | skip | skip |
| Social endorsement closers | strict (share-post tell) | strict | strict | strict | skip | relaxed (1 OK in DM) |
| Hedge-stacked predictions | strict | strict | relaxed ("could" is hedged accuracy) | **extra strict** | relaxed | skip |
| Real/actual inflation | strict | strict | strict | **extra strict** | relaxed | skip |
| Moral-adjective category errors | strict | strict | relaxed | strict | relaxed | skip |
| Invented contrast-pair mirroring | strict | strict | relaxed | strict | relaxed | skip |
| Subjectless fragments and passives | relaxed (fragments are register) | strict | relaxed | strict | skip (docs) | skip |

**Technical-blog word table exceptions:** These terms have legitimate technical
meaning and should not be flagged in technical context: `robust`,
`comprehensive`, `seamless`, `ecosystem`, `leverage` (when discussing actual
platform leverage/APIs), `facilitate`, `underpin`, `streamline`. Still flag:
`delve`, `tapestry`, `beacon`, `embark`, `testament to`, `game-changer`,
`harness`.

**"Extra strict"** means: flag even borderline instances. In investor emails,
a single "thriving ecosystem" can undermine the whole message.

**"Skip"** means: don't audit this category for this profile.

### Auto-detection cues

When no context is specified, infer from these signals:

| Signal | Inferred context |
| -------- | ----------------- |
| Under 300 words + hashtags or mentions | `linkedin` |
| Code blocks, API references, or technical architecture | `technical-blog` |
| Salutation ("Hi [name]", "Dear") + investor/fundraising language | `investor-email` |
| Step-by-step instructions, parameter docs, README structure | `docs` |
| No strong signals | `blog` (safest default) |

When auto-detection conflicts with the text, report the selected profile and the reason.

---

## Voice profiles

Context profiles set *how strict* to be for an audience. Voice profiles set
*how the prose should sound* — the persona. They're independent axes. Voice is
**optional** — if the writer doesn't name one, infer from the input's existing
register.

### Voice profile definitions

fragments allowed. At least one first-person or concrete-anecdote touch.
Near-zero jargon. Keep warm hedges ("honestly," "I think") but cut corporate
ones ("it's worth noting"). *Blog posts, social, community.*

**`professional`** — Active voice for most sentences. Vary sentence length. One
concrete claim per paragraph (a number, a name, a date). Make the ask explicit.
Low tolerance for hedging. *LinkedIn, investor email, sponsor pitches.*

**`technical`** — Prefer plain copulatives ("X is Y") over inflated substitutes.
One idea per sentence; imperative mood for instructions. Jargon is fine, but
define on first use. Tables and lists only for genuinely list-shaped content.
*Docs, technical blog.*

**`warm`** — Address the reader directly ("you") and acknowledge them at least
once. Cut intensifiers ("very," "truly") in favor of stronger verbs. No
performative-empathy openers ("I completely understand how you feel"). Medium
sentences (15–20 words). *Mentorship, onboarding, thank-yous.*

**`blunt`** — Lead with the claim; cut windups. Em-dashes rare; use periods for
emphasis. No padding to hit a rule of three. Near-zero hedging. Short
declaratives, with the occasional long sentence for contrast. *Decision memos,
thought leadership, hard feedback.*

**Calibrate to a sample (optional).** If the writer gives a sample of their own
writing, analyze its sentence-length pattern, contraction rate, paragraph
openings, and recurring word choices, then match those instead of a named
profile.

### How voice composes with context

Voice sets the target; context sets how hard to enforce it. A voice *target*
always applies, even where a context profile would skip that category. Where
both axes govern the same rule and agree, they reinforce. Where they disagree,
resolve toward the **stricter** of the two. Sensible default pairings:
casual↔casual, professional↔linkedin/investor-email,
technical↔docs/technical-blog.

## Sources

- [Package source map](sources.md); verify the linked source record before relying on current or external claims.
