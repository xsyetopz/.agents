# Architecture Design

An Agent Skills-compatible workflow for evidence-backed architecture decisions.
It treats MVC, MVU, DDD, pipelines, runtimes, ports and adapters, event-driven
systems, and agent harnesses as candidates against explicit forces rather than
universal templates.

## Outcome

The skill produces an implementable decision, source-topology ownership map,
tradeoff record, migration boundary, and executable verification. Every warning
or error from the required architecture audit blocks acceptance.

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
<user-home>/.agents/skills/architecture-design/
```

### Claude Code project scope

Copy the folder to:

```text
<repo>/.claude/skills/architecture-design/
```

### Claude Code global scope

Copy the folder to:

```text
<user-home>/.claude/skills/architecture-design/
```

The bundled `scripts/install.sh` supports these destinations and refuses to overwrite an existing installation unless `--force` is explicit.

For API or manual import, keep the zip shape as one top-level `architecture-design/` directory containing `SKILL.md`.

## Invocation

- ChatGPT: select the skill with `@` where supported.
- Codex CLI / IDE: use `/skills` or mention the skill with `$` where supported.
- Claude Code: invoke `/architecture-design` or allow description-based activation.

Activation uses the SKILL.md name and description. The description includes
architecture artifacts, quality attributes, topology changes, and common user
phrases; no separate standardized keyword field is required.

## Validation

```bash
# Run these commands from the architecture-design package directory.
python3 scripts/skill_checks.py report path/to/report.md --mode R3
python3 scripts/skill_checks.py eval-cases
python3 scripts/skill_checks_test.py
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

A skill cannot replace permissions, build rules, tests, or review controls. Static
keyword checks prove discovery coverage only; use the validators, paired eval
cases, repository policies, and architecture audit for behavioral enforcement.
