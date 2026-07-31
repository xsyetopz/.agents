# Rhetoric and Artifact Patterns

Named AI writing patterns covering argument construction, conversational tics,
publication artifacts, and stylistic tells. Load when auditing prose for
specific recurring patterns. For sentence-level rules, see
`sentence-structure.md`. For document structure, see `structural-patterns.md`.

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
Fix: pick one. **Detector note:** the regex uses a narrow gap (modal + at most
one word + hedge adverb), excluding `not`/`never`/`n't` in the intermediate
slot. This prevents false matches on "could not possibly" and inverted
questions.

### "Real/actual" adjective inflation

"Real on-chain tokenomics," "genuine utility." Using `real` / `actual` /
`genuine` / `true` as an empty intensifier implies the rest of the field is
fake without naming what makes this instance the real one. Carve-out: named
contrast ("real on-chain settlement, not bridged IOUs") stays.

### Moral-adjective category errors

AI glues moral adjectives (`honest`, `genuine`, `faithful`) onto non-agentic
technical nouns (`shape`, `number`, `representation`) where the adjective
cannot literally modify the noun. Fix: state the concrete property.

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
"features," "boasts," "presents," "represents." Default to "is" or "has"
unless a more specific verb genuinely adds meaning.

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
expert, study, or leader. Either cite a specific source or drop the
attribution and state the claim directly.

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

Tourism-brochure prose: "nestled within the breathtaking foothills," "a
vibrant hub of innovation." Replace with plain description.

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

"The line I keep coming back to," "I can't stop thinking about this," "this
has been rattling around in my head all week." Claims about the writer's
attention before the reader has any reason to care. Carve-out: when the
sentence says *why* the thing recurred.

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
Only use them when the content genuinely has that many discrete, parallel
items.

### Reasoning chain artifacts

"Let me think step by step," "Breaking this down," "Step 1:," "Here's my
thought process." Chain-of-thought reasoning leaking into published prose.
State the conclusion, then the evidence.

### Sycophantic tone

"Great question!", "Excellent point!", "You're absolutely right!"
Conversational rewards from chat interfaces. Remove entirely.

### Narrated candor

Announcing your own disclosure: "Two caveats I would rather flag than let you
discover later:", "I want to be upfront:", "To be fully transparent:" The
content is "Two caveats:"; the rest advertises forthrightness. The deletion
test: cut the frame. If the sentence loses no information, it was never
content. Carve-out: conflict-of-interest disclosure in journalism/academia/
finance stays.

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

AI latches onto a single metaphor and repeats it across the entire piece:
walls and doors, ecosystem, journey. A human writer uses it and moves on.
Source: tropes.fyi. Fix: use the metaphor once and let it go.

### Content duplication

AI repeats entire paragraphs verbatim, especially in longer output. The same
claim appears twice, rephrased but identical. Source: tropes.fyi. Fix: cut
the duplicate. Before publishing a piece over 500 words, scan for paragraphs
that make the same claim.

### Vocabulary diversity (stylometric)

In longer pieces (200+ words), check the type-token ratio (TTR). Human prose
usually lands around 0.50–0.65. AI text trends flatter, sometimes under 0.40.
A low TTR alone is not proof, but on general prose it's worth a second look.

---

## Self-reference escape hatch

When writing *about* AI writing patterns, quoted examples are exempt from
flagging. Text inside quotation marks, code blocks, or explicitly marked as
illustrative ("for example, AI might write...") should not be rewritten.
