---
name: avoid-ai-slop-writing
description: Use this skill when drafting, auditing, rewriting, editing, or translating technical prose and naming surfaces for documentation, READMEs, issues, pull requests, commits, release notes, reports, code comments, filenames, flags, or multilingual developer writing in English, German, Polish, French, or Japanese. Keep facts, voice, commands, identifiers, citations, uncertainty, and justified domain terms unchanged.
---

# Avoid AI Slop Writing

Slop is writing that performs a register, a template, or a mood instead of
stating what the reader needs. Treat every signal as an editing lead, never as
evidence about authorship. The target is clear writing that can still be
technical, cautious, funny, formal, or blunt when the context calls for it.

## When to load

Load this skill when a text artifact is the deliverable or a substantial part
of the deliverable:

- documentation, README files, tutorials, changelogs, and release notes;
- issues, pull requests, commit messages, design notes, and reports;
- code comments, docstrings, prompts, and user-facing product copy;
- editing, auditing, or translating prose in English, German, Polish, French,
  or Japanese.

Do not apply it to ordinary tool commentary, status updates, or a short answer
around an unrelated implementation unless the user asks for a prose audit.

## Modes

- **Draft**: write the requested artifact from the reader's task and context.
- **Audit**: report findings with locations, category, severity, rationale, and
  a possible repair. Do not change the source.
- **Rewrite**: preserve meaning, repair the findings, then audit the result.
- **Edit**: change only the named file or span and report the changed sections.
- **Translate**: preserve commands, identifiers, facts, uncertainty, and scope
  while using natural plain language in the requested locale.

Honor the requested audience, voice, genre, length, and format. Do not turn a
short technical note into an essay.

## Precedence and protected material

When rules conflict, use this order:

1. factual and semantic accuracy;
2. code, commands, identifiers, URLs, file paths, citations, and quoted text;
3. the user's requested voice, format, and locale;
4. precise domain terminology and required legal, medical, security, or
   academic hedges;
5. anti-slop edits.

Do not rewrite these surfaces by default:

- fenced code, inline code, shell commands, regular expressions, URLs, paths,
  API names, package names, product names, test fixtures, or markup syntax;
- quoted or attributed text, policy text, legal text, and source excerpts;
- numbers, dates, units, names, citations, negation, uncertainty, ownership,
  and scope words.

The scanner masks protected spans by default. Use `--all-surfaces` when the
quoted, coded, or named material is itself the editing target; otherwise use
the quote option only for quoted material.

## Plain action vocabulary

Prefer short, ordinary action words across prose, headings, filenames,
identifiers, flags, and generated text. Start with `act`, `add`, `check`,
`clear`, `copy`, `create`, `delete`, `exec`, `find`, `format`/`fmt`, `get`/`read`,
`init`/`start`, `lint`, `load`, `map`, `move`, `parse`, `run`, `save`, `send`,
`set`, `sync`, `test`, `use`, and `write`. These are defaults, not a ban on
precise domain terms or established interface names.

In general text, replace an inflated verb with the shortest verb that names the
operation:

- `validate`/`validation` → `check`/`checks`;
- `utilize`/`utilization` → `use`;
- `leverage`/`harness` → `use`;
- `facilitate` → `help` or `enable`;
- `implement` → `add`, `build`, or name the changed behavior;
- `execute` → `run` when it means run;
- `perform` → `do` or name the operation;
- `ensure` → `make sure` or name the guarantee;
- `determine` → `find` or name the rule;
- `initialize` → `init`, `start`, or `set up`;
- `optimize`/`enhance` → `improve`, `tune`, or name the measured change;
- `verify` → `check` when it does not name a formal proof or contract.

Do not force abbreviations into ordinary sentences: `fmt` belongs in a tool,
flag, or filename when that is the established interface; prose can say
`format`. Keep a term when it names a protocol, API, formal predicate, test
state, or required compatibility surface. In a broad-surface audit, inspect
those names anyway; rename repository-owned names only after updating every
reference and its tests, and leave external contracts unchanged unless the
user requests a migration.

## Workflow

1. Identify the reader, action, locale, artifact type, and requested voice.
2. Mark protected spans and naming surfaces before judging style.
3. Run `python3 scripts/scan_text.py PATH --json` for lexical phrase candidates
   and `python3 scripts/structure_scan.py PATH --json` for Markdown structure.
   The phrase scan is advisory; the structural scan parses blocks and should
   not infer prose quality from isolated regex matches.
4. When the request includes code, comments, docstrings, paths, flags, or
   identifiers, use an AST-aware tool such as `ast-grep`, Tree-sitter, a
   language parser, or the compiler's syntax API when available. Do not use
   prose regexes to infer code structure. Add `--all-surfaces` to the lexical
   scan only when protected technical material is itself the editing target.
5. Read the whole artifact once. Check headings, openings, endings, repeated
   sentence shapes, paragraph rhythm, list density, and duplicated claims.
6. Classify each candidate as **clear**, **contextual**, **intentional**, or
   **protected**. A phrase list entry is only a prompt for this decision.
7. Repair clear cases. For contextual cases, name the mechanism, source,
   number, or constraint; otherwise shorten or remove the claim. Keep an
   intentional use when its reason is visible in the same passage.
8. Prefer a direct subject and verb, concrete nouns, measured claims, varied
   sentence length, and one example that does real work. Do not replace slop
   with clipped fragments, fake bluntness, or a new template.
9. Run `python3 scripts/check_semantics.py ORIGINAL REVISED --json`. Resolve
   missing protected tokens, changed numbers, lost negation, changed scope, or
   stale path/flag references before accepting the rewrite. Added wording is
   not proof of a problem.
10. Run both scanners again and read the full result for voice, coherence, and
   accidental repetition. Stop when the text is clean enough for its audience;
   do not chase a zero count at the expense of meaning.

## What to remove

Use [the pattern catalogue](references/pattern-catalogue.md) for the complete
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

- false drama: negative reframes, stacked negations, self-answered questions,
  reveal labels, manufactured suspense, and grand stakes;
- prestige register: ornate metaphors, copula avoidance, business jargon,
  pseudo-technical labels, and figurative engineering slang;
- template pressure: warm-up paragraphs, bold-first bullets, numbered phase
  labels, listicles disguised as prose, generic headings, and signposted
  endings;
- rhythm and composition: repeated sentence openings, tricolon cascades,
  false from X to Y ranges, short-fragment piles, analogy stacking, one-point
  dilution, fractal summaries, duplicated sections, and uniform paragraphs;
- process leakage: chat residue, review history, plan labels, I hope this
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

Use [the action map](references/language-map.md) for English, German, Polish,
French, and Japanese developer actions. Translate the surrounding instruction,
not the command or identifier. Use locale-correct grammar, punctuation,
diacritics, dates, numbers, units, abbreviations, and product terminology.
Avoid idioms and culture-bound jokes when the audience is international.

Web search is restricted. During an active translation, search only for a
localized developer idiom, terminal convention, or official product term that
cannot be resolved from the references. Do not browse for generic synonyms,
AI-detection claims, or style inspiration. Record any source used for a
version-sensitive terminology decision.

## Output contract

- **Draft or rewrite**: return the clean text, a short edit summary, and the
  second-pass semantic/style result.
- **Audit**: return every material finding with location, quoted span,
  category, severity, rationale, and suggested repair; separate protected and
  intentional uses.
- **Edit**: return the path, changed sections, second-pass result, and
  findings deliberately left unchanged.
- **Translate**: return the translation, preserved technical tokens, and any
  unresolved locale question. Ask for native review when the text is
  user-facing, safety-critical, or legally binding.

Keep the report shorter than the edited artifact unless the user asks for a
full diff. Never claim that clean prose proves human authorship.

## References and tools

- [Pattern catalogue](references/pattern-catalogue.md): failure modes,
  structural signals, escape clauses, and repairs.
- [Word choice](references/word-choice.md): Microsoft, Digital.gov, and Apple
  international-style guidance.
- [Language map](references/language-map.md): localized developer actions and
  terminology boundaries.
- [Source index](references/source-index.md): live URLs, retrieval notes,
  attribution, license limits, and corrected records.
- [Repair examples](references/repair-examples.md): context-aware before/after
  examples, including false positives.
- [Phrase corpus](references/phrases.tsv): candidate phrases for the scanner,
  grouped by category and severity. Treat every match as advisory.
- [Seed lexicon](references/seed-lexicon.tsv): MIT-licensed adjective, noun,
  and verb candidates with source metadata.
- `scripts/scan_text.py`: deterministic lexical phrase scan.
- `scripts/structure_scan.py`: parser-backed Markdown block and composition
  scan; use it instead of extending phrase regexes for structural findings.
- `scripts/check_semantics.py`: protected-token and fact inventory comparison.
- `scripts/check_skill.py`: local agentskills structure and self-check.
- `scripts/refresh_seed_lists.py`: explicit-maintenance refresh for the
  MIT-licensed llm-cliches seed lexicon; never run it during an edit.

For tool selection, use the strongest syntax available at the boundary: a
CommonMark or Tree-sitter Markdown parser for document structure, `ast-grep` or
Tree-sitter for source syntax, and a compiler or language-server API for symbol,
type, and reference facts. Use regular expressions only for narrow lexical
candidate collection, never as proof of architecture, syntax, or prose quality.
