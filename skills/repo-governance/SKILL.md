---
name: repo-governance
description: >
  Use when creating, rewriting, auditing, splitting, or enforcing repository governance for humans and coding agents. Covers CONTRIBUTING.md, AGENTS.md, CLAUDE.md, instruction imports, nested agent rules, CODEOWNERS, pull-request templates, issue templates, contributor workflow, review ownership, repository policy, multilingual governance, Git assistance trailers, and provider-specific instruction files. Trigger phrases include contributor guide, agent instructions, repository rules, coding-agent policy, CODEOWNERS, PR template, issue template, governance audit, instruction precedence, nested AGENTS.md, and who owns this code. Not for README.md or CHANGELOG.md content.
---

# Repo Governance

Create a small, enforceable governance surface with explicit owners, scope,
precedence, and verification. Put human workflow in human-facing files and agent
execution rules in agent-facing files.

## When to use

- Creating or updating CONTRIBUTING.md, AGENTS.md, CLAUDE.md, CODEOWNERS, PR templates, or issue templates
- Separating human contributor policy from coding-agent instructions
- Designing nested instruction scope and provider imports
- Auditing ownership, review requirements, change protocol, or conflicting rules
- Adding validation for governance contracts

## When NOT to use

- README.md, CHANGELOG.md, or release notes; use repo-docs
- Team branching-model selection; use git-workflows
- CI/CD implementation beyond documenting the required checks; use git-ci-cd

## Governance contract

- Identify the audience, owner, scope, precedence, enforcement mechanism, and update path for every rule.
- Keep one canonical statement for each policy; import or link instead of duplicating divergent copies.
- Put repository-wide defaults at the root and narrower overrides in the smallest owning subtree.
- Keep instructions executable: name commands, paths, evidence, and acceptance conditions.
- Do not convert preferences into universal prohibitions or claim tooling enforces prose that it does not read.
- Preserve unrelated existing policy and generated provider files unless their canonical source is changed.

## Quick start

1. Inventory existing governance files, imports, templates, CODEOWNERS rules, and branch checks.
2. Map each rule to audience, scope, owner, and actual enforcement.
3. Resolve contradictions using repository precedence and the narrowest applicable owner.
4. Edit the canonical file; regenerate derived files through their owner.
5. Validate links, imports, required sections, ownership patterns, and documented commands.
6. Inspect the final diff for duplicated or unenforceable policy.

## Output contract

Report changed governance surfaces, scope and precedence, enforcement points,
validation evidence, and any rule that remains advisory because no mechanism owns
it.

## Reference map

| Need | Load |
|---|---|
| Agent instruction structure | references/agent-governance.md |
| Human contributor policy | references/human-governance.md |
| Governance contracts | references/contracts.md |
| Issue and PR templates | references/issue-templates.md |
| Standards and validation | references/standards.md |

## Completion

Complete when every changed rule has one canonical owner, audience and scope are
unambiguous, imports and templates resolve, documented commands are valid, and
applicable governance checks pass.

## Related skills

- repo-docs for README and CHANGELOG
- git-workflows for branching and merge policy
- git-ci-cd for pipeline enforcement
- skill-creator for reusable agent skills
