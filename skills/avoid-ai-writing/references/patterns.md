# AI Writing Patterns — Detection Catalog

Complete catalog of AI writing patterns to remove or fix. Load this when auditing
or rewriting text. See `severity-tiers.md` for priority levels and
context-dependent strictness.

---

## Formatting

### Em dashes (— and --)

Replace with commas, periods, parentheses, or rewrite as two sentences. Target:
zero. Hard max: one per 1,000 words. Catch both the Unicode em dash (—) and the
double-hyphen substitute (--).

Carve-outs (don't count toward the rate):

- List separator: `- **Term** — description` or `- [- link text] — description`
  where the em dash separates a bold lead term or markdown link from its gloss.
- Changelog version headings: `## [3.21.0] — 2026-07-30` (Keep-a-Changelog
  format). Adapted from #67.
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

---

## Sentence structure

### "It's not X — it's Y" / negative parallelism

Rewrite as a direct positive statement. Max one per piece. Includes the
split-sentence form ("The headline isn't the speed. The real story is Y."),
the multi-negation countdown ("It's not the price. It's not the features.
It's the trust."), and the tailing negation ("The options come from the
selected item, no guessing."). Carve-out: negations enumerating spec
constraints in a list ("no dependencies, no telemetry") are list content, not
a reveal.

### Hollow intensifiers

Cut `genuine` / `genuinely`, `real` (as in "a real improvement"), `truly`,
`quite frankly`, `to be honest`, `let's be clear`, `it's worth noting that`.
Just state the fact.

### Vague endorsement ("worth [verb]ing")

Cut or replace `worth reading`, `worth paying attention to`, `worth a look`,
`worth exploring`. Say *why* something matters instead.

### Hedging

Cut `perhaps`, `could potentially`, `it's important to note that`, `to be
clear`. Make the point directly.

### Missing bridge sentences

Each paragraph should connect to the last. If paragraphs could be rearranged
without the reader noticing, add connective tissue.

### Compulsive rule of three

Vary groupings. Use two items, four items, or a full sentence instead of
triads. Max one "adjective, adjective, and adjective" pattern per piece.

---

## Words and phrases to replace

Words are organized into three tiers based on how reliably they signal
AI-generated text. Adapted from brandonwise/humanizer's vocabulary research.

**Caveat.** The "appears far more often in AI text" claim behind Tier 1A is
inherited, not measured in this repo. Measured against the repo's own machine
corpus (RAID 2024 + HC3 Dec 2022, 779 units), the entire Tier 1 vocabulary table
has a lift of **0.9** — it fires slightly *more* often on human writing than
machine writing. Structural signals (rhythm uniformity) discriminate at 11.7x
lift (#71). The word list is useful as writing advice, but in detect mode,
present it as a convention, not a verified statistic. Until the corpus covers
current-model output (#72), treat 1A as well-supported convention.

**Match inflected forms.** Each entry covers the listed word *and* its
morphological variants — adverb (`-ly`), gerund/participle (`-ing`), plural,
comparative/superlative, and verb conjugations — unless a variant carries a
distinct, legitimate meaning.

### Tier 1A — AI frequency markers

Always replace. A cluster is evidence about how a passage was produced.

| Replace | With |
| --- | --- |
| delve / delve into | explore, dig into, look at |
| landscape (metaphor) | field, space, industry, world |
| tapestry | (describe the actual complexity) |
| realm | area, field, domain |
| paradigm | model, approach, framework |
| embark | start, begin |
| beacon | (rewrite entirely) |
| testament to | shows, proves, demonstrates |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete, full |
| cutting-edge | latest, newest, advanced |
| leverage (verb) | use |
| pivotal | important, key, critical |
| underscores | highlights, shows |
| meticulous / meticulously | careful, detailed, precise |
| seamless / seamlessly | smooth, easy, without friction |
| game-changer / game-changing | describe what specifically changed and why it matters |
| hit differently / hits different | (say what specifically changed, or cut) |
| watershed moment | turning point, shift (or describe what changed) |
| marking a pivotal moment | (state what happened) |
| the future looks bright | (cut — say something specific or nothing) |
| only time will tell | (cut — say something specific or nothing) |
| nestled | is located, sits, is in |
| vibrant | (describe what makes it active, or cut) |
| thriving | growing, active (or cite a number) |
| despite challenges… continues to thrive | (name the challenge and the response, or cut) |
| showcasing | showing, demonstrating (or cut the clause) |
| deep dive / dive into | look at, examine, explore |
| unpack / unpacking | explain, break down, walk through |
| bustling | busy, active (or cite what makes it busy) |
| intricate / intricacies | complex, detailed (or name the specific complexity) |
| complexities | (name the actual complexities, or use "problems" / "details") |
| ever-evolving | changing, growing (or describe how) |
| enduring | lasting, long-running (or cite how long) |
| daunting | hard, difficult, challenging |
| holistic / holistically | complete, full, whole (or describe what's included) |
| actionable | practical, useful, concrete |
| impactful | effective, significant (or describe the impact) |
| learnings | lessons, findings, takeaways |
| thought leader / thought leadership | expert, authority (or describe their actual contribution) |
| best practices | what works, proven methods, standard approach |
| at its core | (cut — just state the thing) |
| synergy / synergies | (describe the actual combined effect) |
| interplay | relationship, connection, interaction |
| keen (as intensifier) | interested, eager, enthusiastic (or cut) |
| genuinely / genuine (as intensifier) | (cut — just state the fact) |
| symphony (metaphor) | (describe the actual coordination or combination) |
| embrace (metaphor) | adopt, accept, use, switch to |
| load-bearing *(metaphor)* | essential, critical, necessary — or say what breaks if you remove it |

**load-bearing allowlist (#56).** Flip from denylist to allowlist: flag
`load-bearing` only when it modifies an abstract noun (assumption, claim,
invariant, premise, argument, idea, concept, notion, theory, reasoning, logic,
structure, element, frame, foundation). This fails closed — literal structural
nouns (wall, beam, column, capacity, masonry, etc.) are never flagged. Known
gap: predicative use ("the argument is load-bearing") is not caught by the
allowlist but is rare in AI text relative to attributive use.

**Compounds requiring hyphens.** Unhyphenated "load bearing" is ordinary English
("the load bearing down on the bridge") — only the hyphenated compound is the
tell.

### Tier 1B — Clarity edits

Wordiness and formality, not authorship evidence. Same fix, weaker claim.

| Replace | With |
| --- | --- |
| utilize | use |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| features (verb) | has, includes |
| boasts | has |
| presents (inflated) | is, shows, gives |
| commence | start, begin |
| ascertain | find out, determine, learn |
| endeavor | effort, attempt, try |

In `detect` mode, report 1A and 1B separately. Presenting a wordiness fix as
authorship evidence is the error this split prevents.

### Tier 2 — Flag when 2+ appear in the same paragraph

These words are legitimate on their own. Two or more together means the
paragraph needs a rewrite.

| Replace | With |
| --- | --- |
| harness | use, take advantage of |
| navigate / navigating | work through, handle, deal with |
| foster | encourage, support, build |
| elevate | improve, raise, strengthen |
| unleash | release, enable, unlock |
| streamline | simplify, speed up |
| empower | enable, let, allow |
| bolster | support, strengthen, back up |
| spearhead | lead, drive, run |
| resonate / resonates with | connect with, appeal to, matter to |
| revolutionize | change, transform, reshape |
| facilitate / facilitates | enable, help, allow, run |
| underpin | support, form the basis of |
| nuanced | specific, subtle, detailed |
| crucial | important, key, necessary |
| multifaceted | (describe the actual facets, or cut) |
| ecosystem (metaphor) | system, community, network, market |
| myriad | many, numerous (or give a number) |
| plethora | many, a lot of (or give a number) |
| encompass | include, cover, span |
| catalyze | start, trigger, accelerate |
| reimagine | rethink, redesign, rebuild |
| galvanize | motivate, rally, push |
| augment | add to, expand, supplement |
| cultivate | build, develop, grow |
| illuminate | clarify, explain, show |
| elucidate | explain, clarify, spell out |
| juxtapose | compare, contrast, set side by side |
| paradigm-shifting | (describe what actually shifted) |
| transformative / transformation | (describe what changed and how) |
| cornerstone | foundation, basis, key part |
| paramount | most important, top priority |
| poised (to) | ready, set, about to |
| burgeoning | growing, emerging (or cite a number) |
| nascent | new, early-stage, emerging |
| quintessential | typical, classic, defining |
| overarching | main, central, broad |
| quietly | cut, or name the concrete contrast |
| deeply *(significance collocations only)* | cut, or name what specifically runs deep |
| underpinning / underpinnings | basis, foundation, what supports |

### Tier 3 — Flag only at high density

Normal words. Flag when saturated — a sign AI filled space with vague praise.

| Word | What to do |
| --- | --- |
| significant / significantly | Replace some with specifics: numbers, comparisons, examples |
| innovative / innovation | Describe what's actually new |
| effective / effectively | Say how or cite a metric |
| dynamic / dynamics | Name the actual forces or changes |
| scalable / scalability | Describe what scales and to what |
| compelling | Say why it compels |
| unprecedented | Name the precedent it breaks (or cut) |
| exceptional / exceptionally | Cite what makes it an exception |
| remarkable / remarkably | Say what's worth remarking on |
| sophisticated | Describe the sophistication |
| instrumental | Say what role it played |
| world-class / state-of-the-art / best-in-class | Cite a benchmark or comparison |
| verbatim | Usually redundant with the verb — cut it. Carve-out: legal/research/QA registers |

### Tier 3 phrases — Flag at density or in clusters

Multi-word boilerplate. Flag at 2+ uses of the same phrase, plus a cluster rule:
3+ distinct phrases from this table in one piece is a strong signal.

| Phrase | What to do |
| --- | --- |
| emerging sector / space / category | Name the actual sector |
| the integration of (X with Y) | Describe what's being integrated |
| the intersection of (X and Y) | Pick the specific overlap that matters |
| community-driven | Name what the community does |
| long-term sustainability | Cite the time horizon and constraint |
| user engagement | Name the action |
| decentralized compute | Specify the architecture or cut |
| (sustainable) reward emissions | Cite the emission schedule and sink |
| tokenized incentive structures | Describe the actual mechanism |
| designed for long-term [X] | Cut "designed for" — state the property |

---

## Template phrases (avoid)

Slot-fill constructions that signal generated text:

- "a [adjective] step towards [adjective] AI infrastructure" → describe the
  specific capability
- "Whether you're [X] or [Y]" → false-breadth. Pick the audience or cut
- "I recently had the pleasure of [verb]-ing" → just say what happened

---

## Transition phrases to remove or rewrite

- "Moreover" / "Furthermore" / "Additionally" → restructure or use "and," "also"
- "In today's [X]" / "In an era where" → cut or state specific context
- "It's worth noting that" / "Notably" → just state the fact
- "Here's what's interesting" / "Here's what caught my eye" → let the content
  signal its own importance. If you need a lead-in, make it specific
- "In conclusion" / "In summary" / "To summarize" → your conclusion should be
  obvious
- "When it comes to" → just talk about the thing directly
- "At the end of the day" → cut
- "That said" / "That being said" → cut or use "but," "yet," "however"

---

## Structural issues

### Rhythm and uniformity

**Structure is the #1 detection signal.** Measured on the repo corpus, rhythm
uniformity discriminates human from machine text at **11.7x lift** — an order of
magnitude stronger than vocabulary (0.9x). This aligns with independent
findings: StoryScope (Russell et al. 2026) reaches 93.2% F1 on discourse-level
features alone (#71). If you fix every word on the Tier 1 list but leave the
rhythm untouched, the text still reads as AI-generated.

- **Sentence length uniformity**: If most sentences are 15–25 words, mix short
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

Can you swap two body paragraphs without breaking the piece? If the order
doesn't matter, you've written a list of points, not an argument that builds.
Establish a through-line where each paragraph depends on the one before it.

### Treadmill effect / low information density (content test)

Read each paragraph and ask "what's actually new here?" AI prose frequently
restates the premise in fresh words instead of advancing it. If you could cut
40-60% and lose no information, cut it.

### Excessive structure

- Too many headers: more than 3 headings in under 300 words is almost always AI
- Too many list items: 8+ bullet points in under 200 words → should be prose
- Formulaic section headers: "Overview," "Key Points," "Summary" — use headers
  that tell the reader something specific
- Fragmented headers: a heading followed by a one-line warm-up that restates it
  ("## Performance", then "Speed matters.") — cut the warm-up

---

## Specific patterns

### Significance inflation

Phrases like "marking a pivotal moment in the evolution of..." inflate routine
events. State what happened and let the reader judge significance. If the
sentence still works after deleting the inflation clause, delete it.

### Aphorism formulas

Slot-fill profundity: "X is the language of Y," "X is the currency of Z." The
formula turns an ordinary claim into something that sounds quotable. Replace
with the concrete claim it gestures at. Carve-out: quotations and established
idioms stay.

### Generic future-narrative closers

"May become one of the most important narratives of the next market cycle."
Grammatically a prediction but contains no testable content. Fix: pick the
falsifiable version.

### Hedge-stacked predictions (#69)

Stacking a modal with a hedge adverb: "could potentially create," "may
eventually unlock," "might ultimately transform." Each hedge cancels the next.
Fix: pick one. **Detector note:** the regex uses a narrow gap
(modal + at most one word + hedge adverb), excluding `not`/`never`/`n't` in the
intermediate slot. This prevents false matches on "could not possibly" and
inverted questions.

### "Real/actual" adjective inflation

"Real on-chain tokenomics," "genuine utility." Using `real` / `actual` /
`genuine` / `true` as an empty intensifier implies the rest of the field is fake
without naming what makes this instance the real one. Carve-out: named contrast
("real on-chain settlement, not bridged IOUs") stays.

### Moral-adjective category errors

AI glues moral adjectives (`honest`, `genuine`, `faithful`) onto non-agentic
technical nouns (`shape`, `number`, `representation`) where the adjective cannot
literally modify the noun. Fix: state the concrete property.

### Hashtag stuffing

6+ hashtags on a single short post is near-universal in LLM-generated social
content. The categorical ones (#AI #Crypto #Web3 #Innovation) do nothing for
discoverability and read as bot output. Fix: 2-3 specific tags max, or none.

### Bullet lists of bare noun phrases

5+ consecutive bullet items where each item is a short (≤6 word) adjective-plus
noun phrase with no verb. The tell is the *symmetry*: every item is the same
grammatical shape. Fix: convert to prose, or vary items so each carries a
different shape of information. Carve-out: genuine list content (changelog
entries, todo lists, parameter docs).

### Copula avoidance

AI text avoids "is" and "has" by substituting fancier verbs: "serves as,"
"features," "boasts," "presents," "represents." Default to "is" or "has" unless
a more specific verb genuinely adds meaning.

### Subjectless fragments and agentless passives

"No configuration file needed." "The results are preserved automatically."
Name the actor when it clarifies. Prefer active voice. Carve-out: terse
reference registers (README feature lists, changelog entries, commit subjects).

### Synonym cycling

AI rotates synonyms to avoid repeating a word: "developers… engineers…
practitioners… builders" in the same paragraph. Human writers repeat the
clearest word. If the same noun appears three times and that's the right word,
keep all three.

### Anaphora abuse

Repeating the same sentence opening across multiple sentences: "They assume
that users will pay... They assume that developers will build... They assume
that ecosystems will emerge..." Source: tropes.fyi. Fix: collapse into a
single statement with a list. One instance of deliberate anaphora can be
effective; three is a pattern recognition failure.

### Vague attributions

"Experts believe," "Studies show," "Research suggests" — without naming the
expert, study, or leader. Either cite a specific source or drop the attribution
and state the claim directly.

### Filler phrases

- "It is important to note that" → just state it
- "In terms of" → rewrite
- "The reality is that" → cut or just state the claim

### Generic conclusions

"The future looks bright," "Only time will tell," "One thing is certain" —
filler disguised as conclusions. Cut them.

### Chatbot artifacts

"I hope this helps!", "Certainly!", "Absolutely!", "Great question!", "Feel
free to reach out," "Let me know if you need anything else" — conversational
tics from chat interfaces. Remove entirely. Also: "In this article, we will
explore…" — AI-generated meta-narration.

### "Let's" constructions

"Let's explore," "Let's take a look," "Let's break this down" — false-
collaborative opener. Just start with the point.

### Patronizing analogy ("Think of it as...")

"Think of it as...", "It's like a...", "Picture it this way:" — AI defaults to
teacher mode even for expert audiences. Source: tropes.fyi. Fix: state the
concept directly.

### Notability name-dropping

AI piles on prestigious citations: "cited in The New York Times, BBC, Financial
Times, and The Hindu." One specific reference beats four name-drops. Related —
**historical analogy stacking**: rapid-fire lists of past technologies to borrow
their weight. Name the one parallel that does analytical work.

### Vague third-party validation

"An outside party put us on top," "independent testing confirms," "analysts
agree." The authority is faceless. Fix: name the source, the test, and the
result. Carve-out: specifically attributed, checkable validation stays.

### Superficial -ing analyses

Strings of present participles as pseudo-analysis: "symbolizing the region's
commitment to progress, reflecting decades of investment." Replace with
specific facts or cut entirely.

### Promotional language

Tourism-brochure prose: "nestled within the breathtaking foothills," "a vibrant
hub of innovation." Replace with plain description.

### Formulaic challenges

"Despite challenges, [subject] continues to thrive." Name the actual challenge
and the actual response, or cut.

### Speculative scenario openers

"Imagine a world where…", "Picture a future in which…" AI opens an argument
with a hypothetical that lists desirable outcomes instead of making a claim.
Fix: cut the hypothetical and state the real claim. Carve-out: fiction, thought
experiments with stated payoff, and instructional "imagine you have a sorted
array" stay.

### False ranges

AI creates false breadth by pairing unrelated extremes: "from the Big Bang to
dark matter," "from ancient civilizations to modern startups." List the actual
topics or pick the one that matters.

### Inline-header lists / Bold-first bullets

Bullet lists where each item starts with a bold header: "**Performance:**
Performance improved by..." Strip the bold header and write the point directly.

### List-label periods

In bulleted lists with short labels, LLMs end the label with a period instead
of a colon. "**Intros.** Years of conferences..." → "**Intros:** years of
conferences..." Carve-outs: when the label span is a full sentence on its own,
the period is correct.

### Title case headings (#62)

AI over-capitalizes headings. Use sentence case for subheadings. **Detector
note:** the regex now matches both plain-text title-case lines and Markdown
headings (prefixed `#{1,6}`). Fix: `/^(?:#{1,6}\s+)?([A-Z][a-z]+(?:\s+(?:[A-Z][a-z]+|and|or|of|the|in|for|to|a|an))+\s+[A-Z][a-z]+)\s*$/gm`

### Hyphenated-pair overuse

AI stacks compound modifiers: "a high-quality, well-architected, future-proof
solution." Cut to the modifier that actually matters. Also: hyphenated before
the noun, unhyphenated after a linking verb — AI frequently gets this wrong.

### Cutoff disclaimers

"While specific details are limited based on available information," "As of my
last update." Model limitations leaking into prose. Never publish a sentence
that admits the writer didn't look something up.

### Speculative gap-filling

When the model lacks a fact, it fills the gap with hedged speculation:
"maintains a relatively low public profile," "appears to have studied." These
are guesses formatted as statements. Cut the speculation or replace with a
sourced fact.

### Unfilled placeholders

Bracketed slot-fillers shipped to production: `[Your Name]`, `[INSERT SOURCE
URL]`, `2025-XX-XX`. Near-definitive evidence of unedited AI boilerplate. Fill
them in or delete the sentence.

### Chatbot citation markup leaks

Internal citation tokens: `citeturn0search0`, `contentReference[oaicite:0]`,
`oai_citation`, `grok_card`. These are fingerprints. Strip every markup token.

### AI-tool URL parameters

Tracking parameters auto-appended by AI tools: `utm_source=chatgpt.com`,
`utm_source=copilot.com`, `utm_source=claude.ai`, `referrer=grok.com`. Strip
the parameter from every URL.

### Novelty inflation

"He introduced a term," "She coined the phrase," "a failure mode nobody talks
about." Most ideas are applications of existing concepts. Describe what the
person *did with* the concept. Also flag invented labels: pseudo-analytical
compound terms coined mid-sentence ("the supervision paradox," "the
context-collapse problem").

### Infomercial engagement hooks

"The catch?", "The kicker?", "Here's the thing.", "Plot twist:", "The result?".
Delete the hook and state the thing. Also: fake-candid register openers
("Honestly?", "Real talk:") as standalone openers.

### Social endorsement closers

The curatorial sign-off LLMs append to social posts: "This one is worth your
time:", "Don't sleep on this one.", "Thank me later." Say *what* the thing is
and *who* it's for, then drop the CTA.

### Emotional flatline

"What surprised me most," "I was fascinated to discover," "What struck me was."
Tell-don't-show for emotions. If you claim an emotion, the writing around it
should earn it. Otherwise cut the claim.

### Lingering-attention claims

"The line I keep coming back to," "I can't stop thinking about this," "this has
been rattling around in my head all week." Claims about the writer's attention
before the reader has any reason to care. Carve-out: when the sentence says
*why* the thing recurred.

### False concession structure

"While X is impressive, Y remains a challenge." AI uses this to sound balanced
without weighing anything. Make the concession specific or pick a side.

### Invented contrast-pair mirroring

One half of a contrast pair is a legitimate term of art; the other is the AI
inventing its mirror for parallelism. "False precision rather than genuine
accuracy." Fix: reach for an actual opposite or drop the contrast structure.

### Rhetorical question openers

"But what does this mean for developers?" / "So why should you care?" AI uses
rhetorical questions to stall. If you know the answer, just say it.

### Parenthetical hedging

"(and, increasingly, Z)" / "(or, more precisely, Y)". If the aside matters,
give it its own sentence.

### Numbered list inflation

"Three key takeaways" / "Five things to know." AI defaults to numbered lists.
Only use them when the content genuinely has that many discrete, parallel items.

### Reasoning chain artifacts

"Let me think step by step," "Breaking this down," "Step 1:," "Here's my
thought process." Chain-of-thought reasoning leaking into published prose.
State the conclusion, then the evidence.

### Sycophantic tone

"Great question!", "Excellent point!", "You're absolutely right!" Conversational
rewards from chat interfaces. Remove entirely.

### Narrated candor

Announcing your own disclosure: "Two caveats I would rather flag than let you
discover later:", "I want to be upfront:", "To be fully transparent:" The
content is "Two caveats:"; the rest advertises forthrightness. The deletion
test: cut the frame. If the sentence loses no information, it was never content.
Carve-out: conflict-of-interest disclosure in journalism/academia/finance stays.

### Acknowledgment loops

"You're asking about," "To answer your question," "That's a great question.
The..." AI restates the prompt before answering. Just answer.

### Confidence calibration phrases

"It's worth noting that," "Interestingly," "Surprisingly," "Importantly,"
"Certainly," "Undoubtedly" — AI signals how the reader should feel. One
"notably" in 2,000 words is fine. Three in 500 words is AI-style stacking.
Related — **persuasive-authority tropes**: "the real question is," "at its
core," "fundamentally," "make no mistake," "the truth is." Cut the trope and
lead with the substance.

### Self-labeling significance

"That last move is the contrarian one," "This is the interesting part," "That
third bullet is the real story." The label does the work the content was
supposed to do. Fix: let the explanation carry itself.

### Wall-of-text replies (missing line breaks)

In conversational registers, LLMs default to a single dense block. A reply-
length text (< 150 words) with 4+ sentences as one unbroken paragraph. Fix:
break at thought boundaries. Carve-out: formal long-form prose where a single
dense paragraph is correct.

### Recap-flattery opener

Replying by summarizing someone's own work back at them with praise before
getting to the point: "Thanks for all the legwork here — the migration script
and the rollback plan you worked through are what made this possible." Fix:
substance first, one plain clause of thanks without the recap.

### Diff-anchored writing

Documentation narrating a change instead of describing the thing as it is:
"This function was added to replace the previous approach." A reader without
commit history gets archaeology. Fix: describe current behavior. Carve-out:
changelogs, release notes, migration guides, decision records.

### Manufactured punchlines and staccato drama

Three or more same-shape fragments in a row, each carrying manufactured drama:
"It had no preference for symmetry. No aesthetic prior. No nostalgia for human
taste. The old rules were gone." Fix: keep the one fragment that earns its
emphasis.

### Dead metaphor

AI latches onto a single metaphor and repeats it across the entire piece: walls
and doors, ecosystem, journey. A human writer uses it and moves on. Source:
tropes.fyi. Fix: use the metaphor once and let it go.

### Content duplication

AI repeats entire paragraphs verbatim, especially in longer output. The same
claim appears twice, rephrased but identical. Source: tropes.fyi. Fix: cut
the duplicate. Before publishing a piece over 500 words, scan for paragraphs
that make the same claim.

### Vocabulary diversity (stylometric)

In longer pieces (200+ words), check the type-token ratio (TTR). Human prose
usually lands around 0.50–0.65. AI text trends flatter, sometimes under 0.40.
A low TTR alone is not proof, but on general prose it's worth a second look.

### When to rewrite from scratch vs. patch

If the text has 5+ flagged vocabulary hits across multiple categories, 3+
distinct pattern categories triggered, and uniform sentence/paragraph length,
patching won't fix it — the structure itself is AI-generated. Advise a full
rewrite.

---

## Self-reference escape hatch

When writing *about* AI writing patterns, quoted examples are exempt from
flagging. Text inside quotation marks, code blocks, or explicitly marked as
illustrative ("for example, AI might write...") should not be rewritten.
