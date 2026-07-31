# Validation Guide

Full rules enforced by the skill validator (`validate_skill.py` in the repo
root).

## Frontmatter checks

- SKILL.md must exist and start with `---`
- `name` must be non-empty, match `^[a-z0-9]+(?:-[a-z0-9]+)*$`, ≤ 64 chars
- `name` must equal the directory name
- `description` must be non-empty, ≤ 1024 chars

## Size warnings

- SKILL.md line count > 500: emits a warning
- Rough token count > 7000: emits a warning (progressive disclosure may be
  weakened)

## Required headings

Configured via `.skill-validator.json` `required_headings` array. Each string is
an exact Markdown heading (e.g. `"# Skill Name"`, `"## When to use"`). Headings
inside fenced code blocks are excluded from the check.

## Required files

Configured via `.skill-validator.json` `required_files` array. Each string is a
path relative to the skill root. Useful for mandating LICENSE, scripts, or
specific assets.

## Broken references

The validator scans SKILL.md (outside fenced blocks) for:

- Relative references matching `(references|assets|scripts)/[A-Za-z0-9_.-]+`
- Markdown links whose URL starts with a relative path (not `http://`,
`https://`, `#`, or `mailto:`)

Every found reference must resolve to an existing file or directory under the
skill root.

## Markdown link checks

All `.md` files in the skill directory are scanned for relative Markdown links.
Any link that targets a non-existent path within the skill root is an error.
Links that leave the skill root produce a warning.

## LICENSE warning

Missing `LICENSE` file at the skill root emits a warning (not an error).

## Exit codes

- 0: pass (no errors, warnings allowed)
- 1: fail (at least one error)
