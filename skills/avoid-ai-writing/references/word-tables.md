# Word Replacement Tables

The vocabulary replacement catalog organized by detection tier. Load when
auditing or rewriting to check individual words and phrases against the known
AI-vocabulary lists.

Scope: local-policy vocabulary guidance. Word choices are editing cues, not
standalone authorship evidence.

**Caveat.** The "appears far more often in AI text" claim behind Tier 1A is
inherited, not measured in this repo. Measured against the repo's own machine
corpus (RAID 2024 + HC3 Dec 2022, 779 units), the entire Tier 1 vocabulary
table has a lift of **0.9** — it fires slightly *more* often on human writing
than machine writing. Structural signals (rhythm uniformity) discriminate at
11.7x lift (#71). The word list is useful as writing advice, but in detect
mode, present it as a convention, not a verified statistic. Until the corpus
covers current-model output (#72), treat 1A as well-supported convention.

**Match inflected forms.** Each entry covers the listed word *and* its
morphological variants — adverb (`-ly`), gerund/participle (`-ing`), plural,
comparative/superlative, and verb conjugations — unless a variant carries a
distinct, legitimate meaning.

---

## Tier 1A — AI frequency markers

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

**load-bearing allowlist (#56).** Flag `load-bearing` only when it modifies
an abstract noun (assumption, claim, invariant, premise, argument, idea,
concept, notion, theory, reasoning, logic, structure, element, frame,
foundation). This fails closed — literal structural nouns are never flagged.
Known gap: predicative use ("the argument is load-bearing") is not caught by
the allowlist but is rare in AI text relative to attributive use.

**Compounds requiring hyphens.** Unhyphenated "load bearing" is ordinary
English — only the hyphenated compound is the tell.

---

## Tier 1B — Clarity edits

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

---

## Tier 2 — Flag when 2+ appear in the same paragraph

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

---

## Tier 3 — Flag only at high density

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

---

## Tier 3 phrases — Flag at density or in clusters

Multi-word boilerplate. Flag at 2+ uses of the same phrase, plus a cluster
rule: 3+ distinct phrases from this table in one piece is a strong signal.

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

## Sources

- [Package source map](sources.md); verify the linked source record before relying on current or external claims.
