# Architecture Pattern Governor

A strict Agent Skills–compatible architecture-analysis skill for cross-domain software design. It treats MVC, MVU, DDD, pipelines, runtimes, ports-and-adapters, event-driven systems, and agent harnesses as responses to explicit forces rather than universal templates.

## Correct filename and directory shape

The required filename is exactly `SKILL.md`, uppercase, inside a skill folder whose name matches the `name` field:

```text
architecture-pattern-governor/
├── SKILL.md
├── references/
├── assets/
└── scripts/
```

## Installation

### Codex repository scope

Copy the folder to:

```text
<repo>/.agents/skills/architecture-pattern-governor/
```

### Codex global scope

Copy the folder to:

```text
~/.agents/skills/architecture-pattern-governor/
```

### Claude Code project scope

Copy the folder to:

```text
<repo>/.claude/skills/architecture-pattern-governor/
```

### Claude Code global scope

Copy the folder to:

```text
~/.claude/skills/architecture-pattern-governor/
```

The bundled `scripts/install.sh` supports these destinations and refuses to overwrite an existing installation unless `--force` is explicit.

For API or manual import, keep the zip shape as one top-level `architecture-pattern-governor/` directory containing `SKILL.md`.

## Invocation

- ChatGPT: select the skill with `@` where supported.
- Codex CLI / IDE: use `/skills` or mention the skill with `$` where supported.
- Claude Code: invoke `/architecture-pattern-governor` or allow description-based activation.

## Validation

```bash
python3 scripts/validate_skill.py .
python3 scripts/validate_architecture_report.py path/to/report.md --mode R3
python3 scripts/validate_eval_cases.py
```

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
