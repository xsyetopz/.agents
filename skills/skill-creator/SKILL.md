---
name: skill-creator
description: Use when creating, editing, or validating agent skills in this repository. Covers SKILL.md frontmatter, directory layout, reference files, validator configuration, naming conventions, and progressive disclosure patterns. Do not use for tasks unrelated to authoring skills.
---

# Skill Creator

Create skills that are self-contained, validatable, and easy to maintain. Every
skill lives in its own directory under `skills/` with a `SKILL.md` entry point.
Match the conventions of existing skills - follow the patterns, not the
content.

## When to use

- Creating a new skill from scratch
- Adding references, scripts, or assets to an existing skill
- Auditing a skill for structural compliance
- Updating `.skill-validator.json` or frontmatter
- Debugging validation failures from the skill validator

## When NOT to use

- Editing skill *content* that doesn't change structure - use the domain skill
  instead
- Tasks unrelated to skill authorship

## Agent Skills spec

Skills follow the [Agent Skills
specification](https://agentskills.io/specification). The full spec defines
progressive disclosure, optional directories, and a standard frontmatter schema.
This repository extends it with a local validator.

## Anatomy of a skill

```
skills/<skill-name>/
├── SKILL.md                  # Required. Entry point with YAML frontmatter.
├── .skill-validator.json     # Repository extension. Custom validation rules.
├── LICENSE                   # Recommended.
├── agents/                   # Product-specific config for agent runtimes.
│   └── openai.yaml           # OpenAI-compatible runtime metadata.
├── references/               # Optional. Progressive disclosure files.
│   └── some-guide.md
├── scripts/                  # Optional. Executable tooling.
├── assets/                   # Optional. Static resources.
└── evals/                    # Optional. Evaluation fixtures.
```

### SKILL.md frontmatter

Full schema per the Agent Skills spec:

```yaml
---
name: skill-name           # Required. 1-64 chars, lowercase a-z/0-9/hyphens.
                           # No leading/trailing hyphens, no consecutive --.
description: ...           # Required. 1-1024 chars. What it does and when.
license: MIT               # Optional. License name or bundled file reference.
compatibility: ...         # Optional. Max 500 chars. Environment requirements.
metadata:                  # Optional. Arbitrary key-value pairs.
  author: "Name"
  version: "1.0"
allowed-tools: Bash Read   # Optional (experimental). Space-separated tools.
---
```

Rules enforced by the validator:
- `name`: `^[a-z0-9]+(?:-[a-z0-9]+)*$`, must match directory name
- `description`: non-empty, ≤ 1024 chars
- `compatibility`: ≤ 500 chars if present
- SKILL.md must start with `---` delimiter

### agents/openai.yaml

Every skill includes an `agents/openai.yaml` for OpenAI-compatible runtimes.
This file is read by the machine, not the agent. Minimum form:

```yaml
interface:
  display_name: "Human-Facing Title"
  short_description: "25-64 char blurb for UI lists"
  default_prompt: "Use $skill-name to do X."
```

The `default_prompt` must mention the skill as `$skill-name`. Optional fields:
`icon_small`, `icon_large`, `brand_color`, and `dependencies.tools` for MCP
servers.

### Progressive disclosure

Skills are loaded in tiers to save context:

1. **Metadata** (~100 tokens): `name` + `description` loaded at startup for all
   skills
2. **Instructions** (< 5000 tokens recommended): full `SKILL.md` body loaded on
   activation
3. **Resources** (as needed): files in `references/`, `scripts/`, `assets/`
   loaded on demand

Keep `SKILL.md` under 500 lines. Move detailed material to reference files.

### .skill-validator.json

```json
{
  "required_headings": [
    "# Skill Name",
    "## When to use",
    "## When NOT to use"
  ],
  "required_files": []
}
```

- `required_headings` - exact Markdown headings (with `#` prefix) that must
  appear in SKILL.md
- `required_files` - relative paths that must exist in the skill directory

### Required headings convention

Every SKILL.md should include at minimum:
- `# Skill Name` - title matching the skill name
- `## When to use` - concrete triggers, not vague categories
- `## When NOT to use` - boundaries that prevent misapplication

Common optional headings:
- `## Quick start` - the shortest path to a working result
- `## Reference map` - table mapping tasks to reference files
- `## Related skills` - cross-references to sibling skills
- `## Validate` - command to run the validator

## Quick start

1. Create the directory: `mkdir -p skills/<name>/{references,agents}`
2. Write `SKILL.md` with frontmatter and required headings
3. Write `.skill-validator.json` with `required_headings`
4. Write `agents/openai.yaml` with `interface` block
5. Validate: run the validator from the repo root against `skills/<name>`
6. Add references, scripts, or assets as needed - validate after each change

## Reference map

| If you need to... | Load |
|---|---|
| Read the full Agent Skills specification | [agentskills.io/specification](https://agentskills.io/specification) |
| Understand the openai.yaml format and fields | `references/openai-yaml-spec.md` |
| See complete frontmatter field descriptions | `references/frontmatter-spec.md` |
| Understand validation rules in detail | `references/validation-guide.md` |
| See the naming and structure conventions | `references/conventions.md` |
| Debug common validation failures | `references/troubleshooting.md` |

## Related skills

- `find-skills` - discover and install skills from the ecosystem
- `writing-cleanup` - audit and improve skill prose
- `repo-governance` - governance files for humans and agents

## Validate

From the repository root:

```sh
python3 scripts/validate_skill.py skills/<skill-name>
```
