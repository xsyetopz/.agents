---
name: repository-docs
description: Create or audit README, CHANGELOG, release notes, CONTRIBUTING, CODEOWNERS, templates, and repository governance. Use agents-md-creator for AGENTS.md files and dedicated engineering workflows for runtime code, Git, or CI/CD.
---

# Repository Documentation and Governance

Write and audit repository documentation and governance from current repository evidence, explicit ownership, and observed enforcement.

Define the audience, canonical owner, requested artifact, scope, precedence, publication boundary, and acceptance check. Safe local drafting, edits, and validation may proceed. Publication, hosted mutation, and other external effects require exact authorization. Return changed paths, source evidence, checks, and unresolved ownership or enforcement gaps.

## Workflow

1. Identify audience, canonical owner, requested artifacts, scope, precedence, publication boundary, and whether the task is product documentation, governance, or both.
2. Inspect manifests, entrypoints, configuration, examples, tests, release history, language variants, imports, templates, CODEOWNERS, nested scopes, and actual enforcement.
3. Load only the matching documentation or governance reference from the direct routes below.
   - [CHANGELOG.md](references/docs-changelog.md) · [README.md](references/docs-readme.md) · [Repo Docs sources and provenance](references/docs-sources.md)
   - [Governance Contracts](references/governance-contracts.md) · [Human governance](references/governance-human-governance.md) · [Issue Templates](references/governance-issue-templates.md) · [Standards and primary sources](references/governance-standards.md)
   - [GOOD/RED documentation and governance examples](references/examples.md) (read before making a product claim or governance rule; RED marks a contrast, while GOOD is the documentation pattern)
4. Edit the smallest authorized existing surface, preserving public names and released history unless a migration is authorized; update affected variants or name those left stale.
5. Validate links, commands, imports, ownership patterns, version claims, templates, and repository-native checks; run `python3 scripts/audit_changelog.py CHANGELOG.md` or `python3 scripts/audit_semver.py` when their inputs apply.
6. Inspect the final diff for unsupported claims, duplicate policy, stale variants, and unenforced rules; return commands, statuses, changed paths, and hosted, provider, link, or conditional evidence that remains `UNVERIFIED`.

## Gotchas

- Every product claim needs source truth; every rule needs one audience, owner, scope, precedence, enforcement mechanism, and update path.
- Prose describes policy; enforcement requires tooling that reads it. Mark unavailable settings, owners, contacts, benchmarks, or bypass actors as `UNVERIFIED`.
- Publication and hosted mutation require exact authorization after a preview.
- Route AGENTS.md files to `$agents-md-creator`, local Git and team policy to `$git-workflows`, pipelines to `$git-ci-cd`, hosted APIs to `$git-actions`, and reusable-skill work to a dedicated skill-authoring workflow.
- Edit established human-readable formats directly; keep schemas, manifests, registries, and governance trees within existing repository formats.
