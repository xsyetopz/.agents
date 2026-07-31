---
name: writing-cleanup
description: Use when drafting, auditing, rewriting, editing, or translating technical prose and naming surfaces — documentation, READMEs, issues, pull requests, commits, release notes, reports, code comments, filenames, flags, or multilingual developer writing in English, German, Polish, French, or Japanese. Keep facts, voice, commands, identifiers, citations, uncertainty, and justified domain terms unchanged.
---

# Writing Cleanup

Remove AI slop from technical writing without changing meaning, facts, or
protected technical material. Slop is writing that performs a register,
template, or mood instead of stating what the reader needs.

## When to use

- Drafting or auditing docs, READMEs, changelogs, release notes
- Rewriting issues, PRs, commit messages, code comments
- Translating developer text across English, German, Polish, French, or Japanese
- Auditing prose for filler, corporate register, template pressure, or structural repetition

## When NOT to use

- Ordinary tool commentary or short status updates (unless asked)
- Code, commands, identifiers, URLs, paths, citations, or quoted text (these are protected)
- Marketing copy where the user explicitly wants promotional language

## Modes

| Mode | Action |
|---|---|
| **Draft** | Write the artifact from the reader's task and context |
| **Audit** | Report findings with location, category, severity, rationale, repair — don't change the source |
| **Rewrite** | Preserve meaning, repair findings, then audit the result |
| **Edit** | Change only the named file/span, report changed sections |
| **Translate** | Preserve commands, identifiers, facts, uncertainty; use natural plain language in the target locale |

## Quick start

1. Identify the reader, action, locale, artifact type, and requested voice.
2. Mark protected spans (code, commands, paths, URLs, identifiers, quoted text) before judging style.
3. Run `python3 scripts/scan_text.py PATH --json` for lexical phrase candidates and `python3 scripts/structure_scan.py PATH --json` for Markdown structure.
4. Classify each candidate as **clear**, **contextual**, **intentional**, or **protected**.
5. Repair clear cases. For contextual cases, name the mechanism, source, or constraint.
6. Run `python3 scripts/check_semantics.py ORIGINAL REVISED --json` to verify no facts changed.

## Precedence

1. Factual and semantic accuracy
2. Code, commands, identifiers, URLs, paths, citations, quoted text
3. User's requested voice, format, and locale
4. Precise domain terminology
5. Anti-slop edits

## Reference map

| If you need to... | Load |
|---|---|
| See failure modes and repairs | `references/pattern-catalogue.md` |
| Full editing rules (what to remove, structural checks, artifact rules) | `references/editing-guide.md` |
| Word choice guidance (Microsoft, Digital.gov, Apple style) | `references/word-choice.md` |
| Localized developer action vocabulary | `references/language-map.md` |
| Before/after repair examples | `references/repair-examples.md` |
| Live source URLs and attribution | `references/source-index.md` |

## Related skills

None — this skill is self-contained.

## Maintenance

```sh
python3 scripts/validate_skill.py          # validate skill structure
python3 scripts/scan_text.py PATH --json   # advisory phrase scan
```
