# Frontmatter specification

Scope: `SKILL.md` metadata, selector terms, and routing boundaries. Confirm
portable fields against the [Agent Skills specification](https://agentskills.io/specification);
this catalog adds a narrower description convention.

## Required fields

```yaml
---
name: skill-name
description: artifact nouns, domain terms, bounded exclusion
---
```

Catalog entrypoints use exactly these two fields. The validator still accepts
the optional fields below for generic open-format fixtures and clients that
consume them; do not add them to a catalog skill unless a target client needs
them.

### `name`

- Use 1–64 lowercase letters or digits joined by single hyphens.
- Match the parent directory exactly; reject leading, trailing, or repeated hyphens.

### `description`

- Use one plain, one-line scalar with 8–16 words and at most 140 characters.
- List artifacts, actions, platforms, or domain terms that distinguish activation.
- State the nearest boundary with a short exclusion such as `excludes local Git APIs` or `remote only`.
- Do not begin with `Use for` or `Use to`; avoid workflow prose, promises, or subjective labels.
- Keep the open-format ceiling of 1024 characters in mind; the catalog target is intentionally narrower.

Keyword-style descriptions are selectors, not miniature workflows. Keep
positive triggers, exclusions, and sibling redirects in the `Use this skill`
section of the entrypoint body.

## Optional fields

`license`, `compatibility`, `metadata`, and client-specific `allowed-tools` are
optional. Add only fields consumed by the target client; metadata keys and
values remain strings. Do not add model IDs, permissions, or capability claims
for discoverability alone.

## Routing test

Use at least three substantive positive prompts and three neighboring
near-misses. A static keyword check measures text shape only; it does not prove
model activation. Keep fixed cases in `evals/evals.json` and record run evidence
outside the manifest.
