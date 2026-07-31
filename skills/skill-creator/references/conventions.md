# Conventions

Naming and structure conventions observed across skills in this repository.

## Naming

- Skill directory name = `name` in frontmatter
- Lowercase letters, digits, single hyphens only: `git-ci-cd`, `swiftui-pro`
- Use `-` not `_` or camelCase
- Keep names under 40 characters where practical - 64 is the hard max

## Directory layout

```text
skills/<name>/
├── SKILL.md                # Always present. Entry point with YAML frontmatter.
├── .skill-validator.json   # Always present. Custom validation rules.
├── LICENSE                 # Recommended. Standard open-source license.
├── agents/                 # Required. Product-specific config for runtimes.
│   └── openai.yaml         # OpenAI-compatible runtime metadata.
├── references/             # Progressive disclosure. Load on demand.
│   └── *.md
├── scripts/                # Executable tooling (Python, shell, Node).
├── assets/                 # Static resources (images, templates, configs).
└── evals/                  # Evaluation fixtures for testing skill behavior.
```

Every skill must include `agents/openai.yaml` with at minimum:

```yaml
interface:
  display_name: "Human-Facing Title"
  short_description: "25-64 char blurb for UI lists"
  default_prompt: "Use $skill-name to do X."
```

## SKILL.md structure

1. YAML frontmatter (`---` delimiters, `name` + `description` required;
   `license`, `compatibility`, `metadata`, `allowed-tools` optional)
2. `# Skill Name` heading
3. One-paragraph overview of what the skill does
4. `## When to use` - bullet list of concrete triggers
5. `## When NOT to use` - bullet list of boundaries
6. `## Quick start` - numbered steps, the shortest path to a result
7. `## Reference map` - table: task -> reference file to load
8. `## Related skills` - cross-references with one-line rationale
9. `## Validate` - command to run the validator

## Progressive disclosure

- SKILL.md stays under 500 lines. Reference files carry the detail.
- The reference map tells the model which file to load for which task.
- Reference files are standalone - each answers one category of question
  without requiring another reference to make sense.

## Description style

- Start with "Use when" or "Use for" - describes the trigger, not the skill
  itself
- One sentence, active voice
- Avoid adjectives like "powerful", "comprehensive", "easy"
- List concrete domains or artifacts: "Covers X, Y, Z."
