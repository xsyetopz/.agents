# Pattern catalogue

This catalogue is a set of diagnosis prompts. A match is not a violation until
the necessity test is applied. Keep a form when it is literal, technically
precise, required by the user's voice, or supported by a named fact.

## 1. Importance inflation

**Test:** remove the rating word. If the claim keeps the same information, name
the evidence or remove the rating.

Candidates: crucial, essential, vital, paramount, fundamental, foundational,
transformative, groundbreaking, game-changing, unparalleled, unprecedented,
invaluable, indispensable, pivotal, notable, significant, more important than
ever, cannot be overstated, a defining moment, at a crossroads.

Repair: state the dependency, measurement, date, constraint, or observed effect.
Keep a strong word when the same sentence proves the property.

## 2. Magic adverbs and false depth

**Test:** does the adverb describe a measurable manner, or does it make an
ordinary action sound profound?

Candidates: quietly, deeply, fundamentally, remarkably, arguably, clearly,
notably, importantly, thoughtfully, meaningfully, strategically, seamlessly.

Repair: delete it or name what changed. “The fan runs quietly” is literal and
does not need a repair.

## 3. Empty transitions and throat-clearing

**Test:** delete the opener. If the next sentence still connects, delete it.

Candidates: Furthermore, Moreover, Additionally, In summary, In conclusion,
To sum up, It is worth noting, It should be noted, That being said, With that
said, Generally speaking, Needless to say, Certainly, Of course, As mentioned
above, It goes without saying.

Repair: state the relationship directly, or start with the claim.

## 4. Manufactured drama

**Test:** does the framing create tension or a reveal that the facts do not
support?

Candidates: it is not just X, it is Y; this is not X, it is Y; no X, no Y, just
Z; not X, not Y, just Z; the result?; the catch?; the kicker?; the truth is;
the real story is; here's the thing; here's where it gets interesting; let that
sink in; the answer is; the secret is; what this really means is.

Repair: state Y, the result, or the mechanism without the stage direction. Keep
one contrast when it corrects a specific misconception.

## 5. False exclusivity and vague authority

**Test:** can the reader verify the supposed insider fact or attribution?

Candidates: nobody talks about, what most people miss, the hidden cost, the
silent killer, studies show, experts believe, widely regarded, research proves,
everyone knows, the only real solution, the one thing you need to know.

Repair: name the source, sample, mechanism, or scope. Remove the claim when it
cannot be checked.

## 6. Performative register

**Test:** would a plain verb or noun preserve the same technical meaning?

Candidates: delve, utilize, leverage, facilitate, synergize, robust, intricate,
meticulous, streamline, harness, foster, empower, elevate, bolster, enhance,
showcase, unlock, navigate, optimize when it only means improve, landscape,
realm, tapestry, ecosystem, paradigm, synergy, cornerstone, catalyst,
testament, holistic, multifaceted, granular, actionable, impactful, innovative,
comprehensive, state-of-the-art, best-in-class.

Repair: use use, help, reliable, detailed, improve, show, or the named
mechanism. Keep the term for its precise statistical, technical, or literal
meaning.

## 7. Copula avoidance and ornate metaphors

**Test:** does replacing “serves as”, “functions as”, or “stands as” with “is”
preserve the meaning, or is a concrete verb better?

Candidates: serves as, functions as, acts as, stands as, represents, constitutes,
boasts, features, offers a comprehensive, rich tapestry, intricate interplay,
delicate balance, at the intersection of, at the forefront, sets the stage,
brings to life.

Repair: use is, has, rejects, reads, stores, sends, or another observable verb.
Keep a metaphor only when the reader needs the image and it is not repeated.

## 8. Corporate and business filler

**Test:** does the phrase name an action, owner, resource, or result?

Candidates: utilize, leverage, facilitate, synergize, move the needle, circle
back, touch base, align on, low-hanging fruit, bandwidth, action items,
stakeholders, best practices, value proposition, thought leadership, scalable
solution, robust framework, seamless experience.

Repair: name the task, person, system, or measured outcome. Keep an established
term in a business document when the audience needs it.

## 8a. Inflated action names

**Test:** does the word name an operation, or does a shorter verb name the same
operation in this interface?

Candidates: validate, validation, utilize, utilization, leverage, harness,
facilitate, implement, execute, perform, ensure, determine, initialize,
optimize, enhance, verify, and verification.

Repair: prefer `check`, `use`, `help`, `add`, `run`, `init`, `improve`, or the
named operation. Apply the same test to filenames, flags, headings, and
identifiers. Keep a term when it is an exact command, API, formal predicate,
test state, or compatibility contract; in broad-surface mode, still report the
surface so the owner can decide whether a migration is safe.

## 9. False precision

**Test:** can the label be tied to a mechanism, source, number, or reproduction
step?

Candidates: a race condition, a deadlock, a memory leak, a security issue,
studies show, the data proves, a complex problem, a nuanced issue, a
comprehensive solution, everything from X to Y.

Repair: describe the observable sequence, resource, input, output, or source.
Keep a diagnosis when the mechanism is named or the domain term is required.

## 10. Template filling

**Test:** would the sentence exist if the document had no expected essay slot?

Candidates: In today's fast-paced world; Introduction; Overview; Key
takeaways; Conclusion; In conclusion; To summarize; The following sections;
bold-first bullets whose label repeats the sentence; generic benefit tails.

Repair: open with the task, name the heading's content, or stop at the last
sentence that adds information.

## 11. Reframe, negation, and concession loops

**Test:** count repeated contrasts and concessions. One can clarify; a cluster
manufactures a rhythm.

Candidates: not because X but because Y; while X has limitations, it is still
excellent; despite its challenges; it is less about X and more about Y; X, not
Y; the question is not X, the question is Y.

Repair: state the positive claim and its boundary. Keep a necessary correction
to a named misconception.

## 12. Rhetorical question and reveal labels

**Test:** is the question a real request for information?

Candidates: What does this mean? Why does this matter? Why should you care? The
problem? The result? The tradeoff? The fix? The takeaway? The bottom line?

Repair: turn the answer into a sentence. Keep a question when the artifact is
actually eliciting a response.

## 13. Anaphora and tricolon cascades

**Test:** mark repeated sentence openings or three-item rhythms. Repetition is
the finding only when it clusters without adding contrast or memory.

Candidates: They assume... They assume... They assume...; Every X, every Y,
every Z; workflows, decisions, and interactions; adjective, adjective, and
adjective chains; four- or five-part lists presented as a rhetorical beat.

Repair: combine clauses, vary the syntax, or keep the list as a factual list.

## 14. False ranges and analogy stacking

**Test:** does “from X to Y” describe a real scale? Does each analogy add a
distinct mapping?

Candidates: from innovation to transformation; from the code to the culture;
think of it as; it is like; imagine a world where; a Swiss Army knife for;
bridge, journey, landscape, and ecosystem metaphors in one passage.

Repair: list the concrete items or explain one mapping. Drop metaphors that do
not reduce cognitive work.

## 15. Fragments, mic drops, and fake bluntness

**Test:** are short standalone lines doing work, or manufacturing emphasis?

Candidates: Full stop. Period. Let that sink in. Read that again. It matters.
This works. That scales. No excuses. One sentence paragraphs repeated in a row.

Repair: join the fragment to the claim or keep one deliberate short sentence.
Do not “humanize” by making prose artificially choppy.

## 16. Listicle and phase disguises

**Test:** does prose hide a numbered list or announce an artificial march?

Candidates: First..., second..., third... in continuous prose; Phase 1, Stage 2,
Step 3, Track A; “the first takeaway”, “the second takeaway”; bold labels that
repeat the following sentence.

Repair: use headings or bullets when the structure helps, or write by topic
without announcing a countdown.

## 17. Process leakage and chat residue

**Test:** would the text exist if it had always been a finished artifact?

Candidates: I hope this helps; feel free to reach out; as requested; per review
feedback; as mentioned above; now also handles; the user asked; in this pass;
the next step is; conversation-only references; comments that explain a review.

Repair: state the finished behavior, constraint, or decision. Keep provenance
when the artifact is a review record and the history is the subject.

## 18. Praise sandwich and fake vulnerability

**Test:** does a compliment or confession delay a direct technical judgment?

Candidates: Great suggestion! That said...; X is a solid step in the right
direction, but...; I may be biased; to be honest; this is not a rant; I love
how; thoughtfully designed; a masterclass in.

Repair: state the judgment and evidence. Keep a personal voice when it is
specific and requested, not as a polished substitute for substance.

## 19. Promotional and growth language

**Test:** is the praise supported by a property the reader can verify?

Candidates: vibrant, world-class, hidden gem, treasure trove, game changer,
transformative, unlock potential, unleash, democratize, supercharge, flywheel,
build a moat, at the heart of, a beacon of, a gateway to.

Repair: name the feature, audience, metric, price, constraint, or observed
result. Preserve explicit marketing copy when the user wants marketing copy.

## 20. Composition defects

**Test:** compare claims across the whole artifact, not just one sentence.

Look for duplicated paragraphs, one-point dilution, fractal summaries that
repeat each section, dead metaphors, unsupported generic conclusions, missing
transitions after over-deletion, uniform paragraph lengths, excessive boldface,
title-case headings in ordinary prose, em-dash piles, and decorative Unicode.

Repair: keep the first complete statement, merge genuinely distinct evidence,
remove repeated summaries, and restore only transitions that name a real
relationship.

## 21. Technical and locale carve-outs

Do not flag a term solely because it appears in a list. Keep a protocol, API,
command, statistical property, formal invariant, legal phrase, quoted source,
product name, or established locale term. For translations, preserve developer
tokens and use [the language map](language-map.md). The correct repair may be
“keep unchanged.”

## Severity

- **hard**: mechanical filler or process residue with no visible information;
- **contextual**: candidate needs a necessity, evidence, or domain check;
- **structural**: repetition, formatting, or composition pattern;
- **protected**: detected inside a surface that should not be rewritten;
- **intentional**: user-requested voice or a precise term with a visible reason.

Report severity and rationale. Never turn a count into an authorship,
employment, academic-integrity, or safety decision.
