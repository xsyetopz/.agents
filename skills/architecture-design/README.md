# Architecture Design

A strict Agent Skills–compatible architecture-analysis skill for cross-domain software design. It treats MVC, MVU, DDD, pipelines, runtimes, ports-and-adapters, event-driven systems, and agent harnesses as responses to explicit forces rather than universal templates.

## Correct filename and directory shape

The required filename is exactly `SKILL.md`, uppercase, inside a skill folder whose name matches the `name` field:

```text
architecture-design/
├── SKILL.md
├── references/
├── assets/
└── scripts/
```

## Installation

### Codex repository scope

Copy the folder to:

```text
<repo>/.agents/skills/architecture-design/
```

### Codex global scope

Copy the folder to:

```text
~/.agents/skills/architecture-design/
```

### Claude Code project scope

Copy the folder to:

```text
<repo>/.claude/skills/architecture-design/
```

### Claude Code global scope

Copy the folder to:

```text
~/.claude/skills/architecture-design/
```

The bundled `scripts/install.sh` supports these destinations and refuses to overwrite an existing installation unless `--force` is explicit.

For API or manual import, keep the zip shape as one top-level `architecture-design/` directory containing `SKILL.md`.

## Invocation

- ChatGPT: select the skill with `@` where supported.
- Codex CLI / IDE: use `/skills` or mention the skill with `$` where supported.
- Claude Code: invoke `/architecture-design` or allow description-based activation.

## Validation

```bash
python3 scripts/validate_skill.py skills/architecture-design
python3 skills/architecture-design/scripts/skill_checks.py report path/to/report.md --mode R3
python3 skills/architecture-design/scripts/skill_checks.py eval-cases
python3 skills/architecture-design/scripts/skill_checks_test.py
```

The report gate is fail-closed: any warning or error produces a non-zero exit
and a JSON result with `"passed": false`.

## What is included

- Normative, gate-based workflow
- Cross-domain pattern catalogue
- Fifty domain mappings
- Mermaid flowgraphs
- DDD and MVC applicability rules
- ADR, quality-scenario, component-contract, and architecture-report templates
- Static validators
- Eval cases for trigger and output behavior
- Curated primary and academic references
- Five worked cross-domain architecture examples
- Codex `AGENTS.md` and Claude Code `CLAUDE.md` integration snippets

## Limits

A skill can strongly constrain behavior but cannot guarantee perfect compliance or override higher-priority host instructions. Use the validators, eval cases, repository policies, tests, and review gates for enforcement beyond prompting.
