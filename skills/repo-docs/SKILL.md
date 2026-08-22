---
name: repo-docs
description: README, CHANGELOG, release notes, CONTRIBUTING, AGENTS, CODEOWNERS, templates, and repository governance audits.
---

# Repository Documentation and Governance

Write and audit repository documentation and governance from current source truth, explicit ownership, and observed enforcement.

## Use this skill

- Create, restructure, or audit README, CHANGELOG, release notes, and translated variants.
- Create or update CONTRIBUTING, AGENTS, CLAUDE, CODEOWNERS, provider imports, pull-request templates, issue templates, and nested instruction scope.
- Separate product documentation, human contribution policy, and coding-agent execution rules while keeping one canonical owner for each rule or claim.
- Do not use for runtime code, branching or merge policy, CI/CD implementation, hosted settings mutation, or reusable skill authoring.
- Redirect local Git and team integration work to `$git-workflows`, CI/CD to `$git-ci-cd`, hosted API calls to `$git-actions`, reusable skills to `$skill-creator`, and prose-style audits to `$avoid-ai-writing`.

## Rules

- Inspect manifests, entrypoints, configuration, examples, tests, release history, governance imports, CODEOWNERS, and nested scope before documenting or changing policy.
- Tie every product claim to source truth and every rule to one audience, canonical owner, scope, precedence, enforcement mechanism, and update path.
- Do not guess support, benchmarks, owners, contacts, bypass actors, hosted settings, or enforcement. Mark unavailable evidence `UNVERIFIED`.
- Preserve public names and released history unless migration is authorized. Update affected variants or name those left stale.
- Do not invent custom schema files or custom generated files as outputs. Edit authorized human-readable repository files directly in established formats; do not emit template-generated governance trees, registries, or manifests.
- Do not claim prose enforces what tooling does not read. Preview external changes and require exact authorization before publication or hosted mutation.

## Steps

1. Identify audience, owner, requested files, scope, precedence, and whether the task concerns product docs, governance, or both.
2. Inspect source truth, release history, language variants, governance imports, templates, CODEOWNERS, nested scopes, and actual enforcement.
3. Load only the matching route from `references/index.md`. Resolve conflicting rules with the narrowest applicable canonical owner.
4. Edit the smallest authorized existing surface directly. Do not generate a custom schema, manifest, registry, or derived file tree.
5. Validate links, commands, imports, ownership patterns, version claims, templates, and repository-native checks when their inputs exist.
6. Inspect the final diff for unsupported claims, stale variants, duplicate policy, and unenforced rules. Report advisory and unverified gaps.

## Resources

- Start with the package [reference router](references/index.md).
- Load only the routed documentation or governance reference needed for the current artifact and audience.

## Verify

- Done means documentation matches source truth, changed rules have one owner and clear scope, affected variants are updated or named, and no custom schema or generated output file was added.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- When target inputs exist, run `python3 scripts/audit_changelog.py CHANGELOG.md`, `python3 scripts/audit_semver.py`, link checks, documented commands, and repository-native governance checks.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark skipped conditional audits, hosted settings, external provider state, unavailable commands, or unchecked links `UNVERIFIED`.
