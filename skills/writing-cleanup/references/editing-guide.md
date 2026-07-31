# Editing Guide

## What to remove

Use [the pattern catalogue](pattern-catalogue.md) for the complete
set of families and escape clauses. In human-facing prose, remove or rewrite
empty transitions, canned greetings, generic closers, process residue,
corporate filler, praise without evidence, vague attributions, and signposted
conclusions. Examples include Furthermore, Moreover, Additionally, In summary,
In conclusion, Delve, Seamlessly, Utilize, Synergize, Leverage, Facilitate,
Robust, Intricate, Meticulously, Pivotal, Notable, Thereby, and Herein when
they add no exact meaning.

Do not make a universal ban from a single word. Robust can be a statistical
property, granular can describe real granularity, facilitate can name a precise
causal role, validate can name a formal predicate, and pivotal can be justified
by evidence. The necessity test is: can the reader point to the property,
mechanism, source, contract, or constraint in this context? If not, use the
plain statement.

## Structural checks

Look beyond vocabulary:

- **false drama**: negative reframes, stacked negations, self-answered questions,
  reveal labels, manufactured suspense, and grand stakes;
- **prestige register**: ornate metaphors, copula avoidance, business jargon,
  pseudo-technical labels, and figurative engineering slang;
- **template pressure**: warm-up paragraphs, bold-first bullets, numbered phase
  labels, listicles disguised as prose, generic headings, and signposted
  endings;
- **rhythm and composition**: repeated sentence openings, tricolon cascades,
  false from X to Y ranges, short-fragment piles, analogy stacking, one-point
  dilution, fractal summaries, duplicated sections, and uniform paragraphs;
- **process leakage**: chat residue, review history, plan labels, I hope this
  helps, references only this session can resolve, or comments that explain
  how the text was produced rather than what the code does.

One deliberate instance can be valid. Repetition, clustering, or a form that
adds no information is the finding.

## Artifact-specific rules

- **Docs and READMEs**: open with what the thing does or how to run it. Prefer
  an imperative and a worked example. Headings name content.
- **Issues and pull requests**: state the observed behavior, mechanism, scope,
  evidence, and requested change. Drop praise sandwiches and plan labels.
- **Commits**: make the subject describe the change for a reader who never saw
  the conversation. Add a body only when the subject cannot carry the reason.
- **Code comments**: keep a comment only when the code cannot show the reason,
  invariant, constraint, or non-obvious consequence. Remove banners, value
  echoes, and review history.
- **Reports and academic prose**: name the source, sample, method, and limit.
  Keep hedges that carry uncertainty; remove hedges that only soften a claim.
- **Marketing or personal writing**: preserve the requested register, but
  still remove accidental repetition, fake vulnerability, and unsupported
  superlatives unless the user explicitly wants promotional language.

## Translation and web policy

Use [the action map](language-map.md) for English, German, Polish,
French, and Japanese developer actions. Translate the surrounding instruction,
not the command or identifier. Use locale-correct grammar, punctuation,
diacritics, dates, numbers, units, abbreviations, and product terminology.
Avoid idioms and culture-bound jokes when the audience is international.

Web search is restricted. During an active translation, search only for a
localized developer idiom, terminal convention, or official product term that
cannot be resolved from the references. Do not browse for generic synonyms,
AI-detection claims, or style inspiration. Record any source used for a
version-sensitive terminology decision.
