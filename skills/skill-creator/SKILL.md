---
name: skill-creator
description: >
  Use when creating, rewriting, auditing, debugging, packaging, or validating agent skills and SKILL.md files. Covers the Agent Skills specification, frontmatter, activation descriptions, trigger keywords, skill routing, metadata, agents/openai.yaml, .skill-validator.json, references, scripts, assets, evals, progressive disclosure, installation layout, naming, and behavioral validation. Trigger phrases include create a skill, update every skill, rewrite SKILL.md, fix skill activation, add keywords, improve discoverability, skill not triggering, route this request, validate a skill, package a capability, add a reference, add a script, and author agent instructions. Use current provider prompting guidance for model-specific behavior. Not for tasks unrelated to skill authorship.
---

# Skill Creator

Create a discoverable, bounded, executable skill whose entry instructions are
lean enough to load on every activation and whose behavior can be verified.

## When to use

- Creating, rewriting, splitting, packaging, or validating a skill
- Improving activation descriptions, trigger coverage, or routing boundaries
- Adding references, scripts, assets, evals, validator rules, or OpenAI metadata
- Debugging a skill that does not activate, over-activates, or fails validation
- Adapting skill instructions to current provider guidance and measured failures

## When NOT to use

- Editing domain behavior without changing the skill artifact
- Putting repository-wide conventions in a skill when AGENTS.md is the correct owner
- Encoding a runtime invariant that belongs in permissions, schemas, hooks, or application code

## Agent Skills spec

The current Agent Skills specification defines name and description as the
discovery catalog. The description is therefore the supported routing surface:
include concrete user phrases, commands, artifact names, formats, platforms, and
bounded synonyms. There is no standardized standalone keywords field. Arbitrary
metadata may be ignored during discovery.

Use current official specification guidance when it changes. For a named model or
provider, load current official prompting guidance before making model-specific
claims.

## Prompt design contract

- Start from the skill outcome, authority, tools, evidence, completion condition, and failure cases.
- State each instruction once; move details behind explicit reference-routing conditions.
- Keep activation vocabulary broad within the owned domain and precise at neighboring boundaries.
- Describe concrete actions and outputs instead of broad tone or personality labels.
- Define tool routing, schemas, retries, stopping conditions, and consequential-action approval only when the skill owns them.
- Use examples only for a product requirement or measured gap.
- Treat static keyword checks as routing evidence, not proof of model behavior.
- Test observable tool and filesystem effects separately from the final answer.

## Anatomy of a skill

    skills/<skill-name>/
    ├── SKILL.md
    ├── .skill-validator.json
    ├── LICENSE
    ├── agents/openai.yaml
    ├── references/
    ├── scripts/
    ├── assets/
    └── evals/

### SKILL.md frontmatter

Required fields:

- name: lowercase letters, digits, and single hyphens; matches the directory
- description: 1-1024 characters; says what the skill does, when it triggers,
  key terms, and exclusions. See [frontmatter specification](references/frontmatter-spec.md).

Optional fields are license, compatibility, metadata, and experimental
allowed-tools. See the [frontmatter specification](references/frontmatter-spec.md).

### agents/openai.yaml

Provide interface.display_name, interface.short_description, and a default_prompt
that names the skill as $skill-name. Keep UI metadata concise; do not duplicate the
entire SKILL.md.

### Progressive disclosure

Tier 1 loads name and description. Tier 2 loads SKILL.md on activation. Tier 3
loads references, scripts, and assets only when routed. Keep SKILL.md under 500
lines and focused on decisions required for every invocation.

### .skill-validator.json

Use required_headings and required_files to encode structural contracts. Add
executable validators or evals for behavior that prose cannot prove.

### Required headings convention

Include a clear title, When to use, When NOT to use, workflow or quick start,
reference routing, completion criteria, and validation instructions. Add domain
headings only when they change execution.

## Quick start

1. Identify the skill owner, outcome, neighboring skills, and natural user prompts.
2. Read current official Agent Skills and model-specific prompting guidance.
3. Write a description with high-recall domain terms and explicit exclusions.
4. Write the lean execution contract and route details into references.
5. Add scripts or evals for repeated, deterministic, or behaviorally risky work.
6. Validate structure, routing cases, observable effects, and final answers.
7. Inspect the packaged diff for stale references, duplicate policy, and generated artifacts.

## Reference map

| Need | Load |
|---|---|
| Frontmatter and activation descriptions | references/frontmatter-spec.md |
| OpenAI metadata | references/openai-yaml-spec.md |
| Layout and naming | references/conventions.md |
| Validator behavior | references/validation-guide.md |
| Validation failures | references/troubleshooting.md |
| Model-specific prompt design | prompt-engineering skill and current official provider guidance |

## Completion

Complete when the skill activates for representative positive prompts, remains off
for neighboring negative prompts, follows its workflow in an isolated fixture,
produces the required observable effects and final answer, and passes structural
validation with no unexplained warning.

## Related skills

- prompt-engineering for model-specific instruction design and behavioral evals
- find-skills for ecosystem discovery
- repo-governance for durable repository agent rules
- install-skizzles for installation and packaging workflows
