# Troubleshooting

## Use this reference

Load this reference when troubleshooting is part of the skill-authoring task. Keep the discovery description precise, the entry instructions lean, details progressively disclosed, and behavior independently verifiable.

Common validation failures and how to fix them.

## "SKILL.md must start with YAML frontmatter delimiter '---'."

SKILL.md is empty or doesn't start with `---`. Add the frontmatter block:

```yaml
---
name: my-skill
description: Use when ...
---
```

## "SKILL.md frontmatter has no closing '---'."

The opening `---` has no matching closing `---`. Add it after the last
frontmatter field.

## "'name' must contain lowercase letters/digits separated by single hyphens."

The `name` field contains uppercase letters, underscores, consecutive hyphens,
or other invalid characters. Fix it to match `^[a-z0-9]+(?:-[a-z0-9]+)*$`.

## "Folder name 'X' must match skill name 'Y'."

Rename either the directory or the frontmatter `name` so they match exactly.

## "Missing required heading: X"

Add the exact heading (with `#` prefix) to SKILL.md. Or remove it from `.skill-
validator.json` `required_headings` if it's no longer relevant.

## "Broken relative reference in SKILL.md: X"

A path referenced in SKILL.md doesn't exist. Either:

- Create the missing file
- Fix the path if it has a typo
- Remove the reference if it's no longer needed

## "Broken Markdown link in X: Y"

A Markdown link in a `.md` file points to a path that doesn't exist under the
skill root. Fix the link target or create the missing file.

## "SKILL.md has N lines; keep the core under 500."

The SKILL.md is getting large. Move detailed content into reference files and
add entries to the reference map.
