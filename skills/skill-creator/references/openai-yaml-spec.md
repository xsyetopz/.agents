# `agents/openai.yaml` specification

## Required interface block

```yaml
interface:
  display_name: "Skill Creator"
  short_description: "Author and validate portable Agent Skills"
  default_prompt: "Use $skill-creator to author or revise one portable skill."
```

- `display_name`: a concise human-facing title, usually 2–6 words.
- `short_description`: a quoted 25–64-character UI blurb; describe the useful
  action, not a superlative.
- `default_prompt`: a quoted one-sentence invocation that literally names the
  skill as `$skill-name`.

Quote string values and keep keys unquoted. This package's validator checks the
three fields and the literal `$skill-creator` token; it does not claim that all
clients implement this schema.

## Optional fields

Icon paths and brand colors may be added only with real assets and a consuming
client. Tool dependencies are client-specific; do not declare an MCP server or
credential requirement merely for discoverability. Any relative icon path must
exist within the skill root.

## Review checklist

1. Compare the display text with `SKILL.md` scope and description.
2. Check the default prompt does not promise runtime behavior outside this
   skill.
3. Parse/validate after editing; YAML syntax alone does not prove routing.
4. Keep this file short and avoid duplicating workflow details from `SKILL.md`.
