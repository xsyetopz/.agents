# Validation guide

## Structural checks

```bash
python3 skills/skill-creator/scripts/validate_skill.py skills/skill-creator
python3 -m unittest skills/skill-creator/scripts/test_validate_skill.py
find skills -name SKILL.md -print
```

Expected source-tree evidence is exit 0 with `PASS`, unit tests reporting `OK`,
and exactly `skills/skill-creator/SKILL.md`. A package-local validator may also
be run directly from a copied skill fixture; use its help/output rather than
assuming a global path.

## Bundled parser scope

The validator is Python-stdlib-only and intentionally implements a strict
subset of YAML for frontmatter and `agents/openai.yaml`. Double-quoted scalars
must use JSON-compatible escapes; invalid or unsupported escapes (for example
`\q`), unterminated quotes, unbalanced brackets, and unsupported flow
constructs fail closed. Single-quoted scalars may escape a quote only as
`''`; backslashes (including backslash-quote) are rejected in this subset.
Flow delimiters must match (`{}` versus `[]`) and flow-looking scalars must
parse as one of the supported flow forms, never fall back to plain text. The
plain-scalar subset rejects ambiguous indicator-leading values (`:`, `@`,
backtick, and unsupported YAML indicators) and colon followed by whitespace;
`normal:colon` remains valid. Empty flow objects/lists are valid, as is one
trailing comma; leading or repeated separators fail closed. Inside flow maps
and lists, unquoted plain scalars cannot contain flow punctuation (`[]{},`)
or any colon; quote such values explicitly. The supported mapping,
block-scalar, and small flow forms are sufficient for this package contract,
but this is not a claim of full YAML conformance. Use a conforming YAML parser
when a skill needs broader YAML features; do not weaken the bundled gate to
accept syntax it cannot parse. Tabs are not accepted as indentation in
frontmatter or `agents/openai.yaml`; tabs after the first non-whitespace
character remain scalar content. Raw C0 controls are rejected except TAB
(U+0009), LF (U+000A), and CR (U+000D); DEL and C1 controls U+007F–U+009F
are rejected as well. Ordinary Unicode remains valid. Unquoted YAML core
non-finite float spellings such as `.nan`, `.inf`, and their case/sign
variants parse as floats; quote them when the value is intended to be text.
Unquoted decimal integers (including leading-zero forms), binary `0b...`,
octal `0o...`, hexadecimal `0x...`, and finite decimal/scientific floats
resolve to numeric values as well. Quote a numeric-looking value or prefix it
with `!!str` when it is intended to remain text; malformed numeric-looking
forms fail closed.

## What to check

- `SKILL.md` exists, starts/ends frontmatter correctly, and has valid
  `name`/`description`; the directory name matches `name`.
- `SKILL.md` stays under 500 lines for this package and uses references for
  detail. A hard implementation limit may be stricter; report the actual value.
- Configured headings are exact and outside fenced blocks; duplicate headings
  are rejected where the validator supports them.
- Configured `required_files` resolve under the skill root. These package files
  are not open-format universal requirements.
- Relative links and `references/`, `assets/`, and `scripts/` paths resolve under
  the skill root. External HTTPS links are allowed but should be reviewed.
- `agents/openai.yaml`, when present, has its three package-required interface
  fields and the exact `$skill-creator` invocation token. Keep selector descriptions
  one-line, keyword-style, and within the catalog word/character target.
- No root assumptions, host-specific absolute paths, symlinks to a global checkout, wrappers,
  aliases, or duplicate `SKILL.md` entrypoints exist.

## Structural versus behavioral evidence

Static checks prove metadata, headings, files, and links. They do **not** prove
model activation, reference selection, command identity, filesystem effects,
safe tool use, or answer quality. Run behavioral evals from `evals/evals.json`
in clean comparable contexts and record commands, changed paths, exit status,
network/secret events, and final response quality separately.

For CLI distribution, use disposable project fixtures and the exact pinned
commands in [package distribution](package-distribution.md). Validate the
copied package itself; a source pass does not prove copy independence.

## Exit classification

- **PASS:** exit 0, no unexplained warnings, and all configured contracts hold.
- **FAIL:** non-zero, missing resource, broken link, duplicate entrypoint, or
  any safety invariant violated.
- **UNVERIFIED:** a behavioral, network, or external-source check was not run;
  report it rather than converting absence of evidence into a pass.
