---
name: agents-md-creator
description: Create or audit standard AGENTS.md files from repository evidence, including root and nested scope, precedence, executable commands, boundaries, and validation. Do not use for GitHub custom-agent persona files or general repository documentation.
---

# AGENTS.md Creator

Create the smallest useful instruction chain for coding agents. Treat `AGENTS.md` as plain Markdown project guidance, not as a persona schema, policy engine, or substitute for repository enforcement.

Before writing, read [the format and evidence guide](references/format-and-evidence.md). Re-check current product documentation when the task depends on a specific agent's discovery behavior because implementations can differ.

## Start with evidence

1. Establish the target repository, intended agents, files or subtrees governed, requested compatibility, and whether the task is creation, repair, consolidation, or audit.
2. Inspect the repository before drafting. Use the repository's structural intelligence mechanism when available; otherwise inspect the narrowest relevant manifests, scripts, CI configuration, existing instructions, representative source, and tests.
3. Build the effective instruction chain from repository root to each affected path. Read every applicable `AGENTS.md` and tool-specific override file supported by the target agent. Record conflicts, stale commands, and duplicated rules before editing.

## Workflow

1. Decide placement by scope:
   - Put repository-wide facts and invariants in the root `AGENTS.md`.
   - Put package, language, or subtree-specific guidance in the nearest nested `AGENTS.md`.
   - Do not repeat parent guidance in child files. A child should add or deliberately override only local rules.
2. Draft concise, imperative guidance backed by current evidence. Prioritize exact setup and file-scoped validation commands, project structure and canonical examples, code and test conventions, ownership or architecture boundaries, external-action permissions, and the expected completion report.
3. Edit only authorized instruction files. Preserve unrelated user rules and stronger higher-priority constraints. Do not add provider aliases, symlinks, imports, `AGENTS.override.md`, or compatibility copies unless the requested support scope requires them.

### Format invariants

- Use the exact filename `AGENTS.md` for the portable format. It has no required frontmatter, headings, or schema.
- Use ordinary Markdown. Do not copy YAML frontmatter from GitHub custom-agent files such as `.github/agents/*.agent.md`; that is a different feature and format.
- Write facts and commands that are specific to this repository. Omit generic advice already supplied by the agent platform.
- State one obligation per bullet where practical. Use exact paths, package names, versions, flags, and conditions.
- Never include secrets, credentials, private keys, personal data, or live connection strings.
- Treat prose as guidance, not enforcement. Point to the actual lint, test, policy, ownership, or CI mechanism when one exists.
- If broad version-specific knowledge must always be available, prefer a compact index to repository-local source files over embedding a large manual. Label the source root and retrieval rule clearly.

## Validation

- Confirm every named path, command, tool, version, and canonical example exists or mark it `UNVERIFIED`.
- Run the narrowest safe command that proves each critical command shape when execution is authorized; do not claim an unrun command passed.
- Check root-to-leaf instructions for contradiction, accidental scope expansion, duplicated policy, and obsolete compatibility guidance.
- Confirm nested files are placed above the files they govern and contain only local differences.
- Search the final files for credentials, placeholders, vague absolutes, generated claims, and product-specific syntax presented as portable AGENTS.md behavior.
- Keep the result short enough that critical commands and boundaries remain easy to find. Split by real subtree scope, not arbitrary line count.

1. Validate the effective result against the checklist below and inspect the final diff. Report changed paths, commands checked, target-agent assumptions, and any instruction that remains `UNVERIFIED`.

## Boundaries

- Route GitHub custom-agent persona files to the workflow responsible for that product's current format.
- Do not publish, commit, push, or change hosted settings without explicit authorization for that action.
