---
name: repo-governance
description: Use when auditing, creating, or updating repository governance files for humans and coding agents — CONTRIBUTING.md, AGENTS.md, provider imports, pull-request templates, CODEOWNERS, multilingual policy, or Git assistance trailers.
---

# Repo Governance

Keep human contribution policy separate from agent execution rules.
`CONTRIBUTING.md` is for people; `AGENTS.md` is for coding agents.
Provider files (`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/agents.mdc`) import `AGENTS.md`.
Hosted enforcement lives in repository rulesets, branch protection, and `CODEOWNERS`.

## When to use

- Creating or auditing `CONTRIBUTING.md`, `AGENTS.md`, pull-request templates
- Adding `CODEOWNERS` entries for governed files
- Setting up multilingual governance translations
- Splitting an existing combined policy into human vs. agent files
- Validating existing governance files for compliance

## When NOT to use

- Writing a code of conduct, security policy, or support guide — requires real contact data
- Inventing `CODEOWNERS`, teams, or hosted rules from guessed values
- Generating non-standard files like `llms.txt` or deprecated `.cursorrules`

## Quick start

1. **Inspect first**: confirm the repository root, host, README, languages, and existing governance files.
2. **Read the references** before changing policy:
   [human-governance.md](references/human-governance.md),
   [agent-governance.md](references/agent-governance.md),
   [contracts.md](references/contracts.md),
   [standards.md](references/standards.md).
3. **Preview**:
   ```sh
   python3 scripts/governance.py --repo /path/to/repo --project-name "Name" --description "One sentence."
   ```
4. **Apply with permission only**: add `--apply --confirm-authorized` after reviewing every proposed operation.

## Reference map

| If you need to... | Load |
|---|---|
| Understand human contribution policy requirements | `references/human-governance.md` |
| Understand agent execution rule requirements | `references/agent-governance.md` |
| See the full human and agent contract templates | `references/contracts.md` |
| Check standards and file format requirements | `references/standards.md` |

## Related skills

None — this skill is self-contained. For architecture governance, use `architecture-design` or `architecture-enforce`.

## Validate

```sh
python3 scripts/governance.py --repo /path/to/repo --validate-only
```

Reports changed paths, conflicts, legacy artifacts, and unconfigured hosted settings.
