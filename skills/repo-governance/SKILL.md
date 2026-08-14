---
name: repo-governance
description: CONTRIBUTING, AGENTS, CODEOWNERS, templates, provider imports, governance policy; excludes docs, branching, and CI implementation.
---

# Repo Governance

## When to use

- Create or update CONTRIBUTING.md, AGENTS.md, CLAUDE.md, CODEOWNERS, provider imports, PR templates, or issue templates.
- Separate human contribution policy from coding-agent execution rules.
- Design nested instruction scope, precedence, ownership, review requirements, or validation.
- Audit governance contracts and add checks for links, imports, ownership, and documented commands.

## When NOT to use

- README.md, CHANGELOG.md, or release notes; route to `repo-docs`.
- Team branching or merge-model selection; route to `git-workflows`.
- CI/CD implementation beyond documenting required checks; route to `git-ci-cd`.

## Guardrails

- Give every rule one audience, canonical owner, scope, precedence, enforcement mechanism, and update path.
- Keep repository-wide defaults at the root and narrower overrides in the smallest owning subtree; import or link instead of duplicating policy.
- Keep instructions executable with commands, paths, evidence, and acceptance conditions; do not claim prose enforces what tooling does not read.
- Permit tool assistance when contributors understand, review, test, and can defend the change; allow maintainers to set narrower learning-oriented rules.
- Require stronger evidence for AI-suggested security fixes, including affected-system or hardware reproduction when applicable.
- Do not guess owners, contacts, bypass actors, hosted settings, or enforcement. Preview external changes and preserve unrelated policy or generated provider files.

## Workflow

1. Inventory governance files, imports, templates, CODEOWNERS rules, branch checks, and nested scopes.
2. Map each rule to audience, owner, scope, precedence, and actual enforcement; resolve conflicts using the narrowest applicable owner.
3. Edit the canonical source and regenerate derived provider files through their owner.
4. Validate links, imports, required sections, ownership patterns, templates, and documented commands.
5. Inspect the final diff for duplicate or unenforceable policy and report advisory rules with no mechanism.

## Quick start

```text
Inventory AGENTS.md, CONTRIBUTING.md, CODEOWNERS, templates, imports, and nested scopes.
Write a read-only plan first when ownership or hosted settings are uncertain.
Validate the canonical file and derived paths before applying any authorized write.
```

Use package templates under `assets/` only as reviewed starting points; project facts and owners must be verified.

## Reference map

- [Reference index](references/index.md) for audience and artifact route selection.
- [Agent governance](references/agent-governance.md) for AGENTS.md scope, imports, and external-action boundaries.
- [Human governance](references/human-governance.md) for contributor, community, security, and provider files.
- [Governance contracts](references/contracts.md) for audience, ownership, assistance, and agent-rule requirements.
- [Issue templates](references/issue-templates.md) for GitHub issue and PR form structure.
- [Standards](references/standards.md) for current provider behavior and primary sources.

## Completion

Complete when every changed rule has one canonical owner, audience and scope are unambiguous, imports and templates resolve, documented commands are valid, applicable checks pass, and advisory gaps are reported.

## Validation

Run from this package root:

```bash
python3 scripts/check.py
python3 -m json.tool evals/evals.json >/dev/null
python3 scripts/governance.py --help
python3 scripts/test_governance.py
```

Use the governance CLI's documented validation mode for a target repository; never weaken a failed check to make a policy appear enforced.

## Related skills

- `repo-docs` for README and CHANGELOG
- `git-workflows` for branching and merge policy
- `git-ci-cd` for pipeline enforcement
- `skill-creator` for reusable agent skills
