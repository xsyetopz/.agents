---
name: repo-governance
description: CONTRIBUTING, AGENTS, CODEOWNERS, templates, provider imports, governance policy; excludes docs, branching, and CI implementation.
---

# Repo Governance

Define repository policy with explicit audiences, ownership, scope, and enforcement.

## Use this skill

- Create or update CONTRIBUTING.md, AGENTS.md, CLAUDE.md, CODEOWNERS, provider imports, pull-request templates, or issue templates.
- Separate human contribution policy from coding-agent execution rules.
- Design nested instruction scope, precedence, ownership, review requirements, or validation.
- Audit governance contracts and add checks for links, imports, ownership, and documented commands.
- Do not use for README, CHANGELOG, release notes, branching or merge models, CI/CD implementation, or reusable skill authoring.
- Redirect repository docs to `$repo-docs`, branch policy to `$git-workflows`, CI/CD to `$git-ci-cd`, reusable skills to `$skill-creator`, and local Git history to `$git-toolkit`.

## Rules

- Give every rule one audience, canonical owner, scope, precedence, enforcement mechanism, and update path.
- Keep repository defaults at the root and narrower overrides in the smallest owning subtree. Import or link instead of duplicating policy.
- Make instructions executable with commands, paths, evidence, and acceptance conditions. Do not claim prose enforces what tooling does not read.
- Permit tool assistance when contributors understand, review, test, and can defend the change. Maintainers may set narrower learning rules.
- Treat AI-suggested security fixes as hypotheses. Require reproduction on the affected system or hardware when applicable.
- Do not guess owners, contacts, bypass actors, hosted settings, or enforcement. Preview external changes and preserve unrelated or generated files.

## Steps

1. Inventory governance files, imports, templates, CODEOWNERS rules, branch checks, and nested scopes.
2. Map each rule to audience, owner, scope, precedence, and actual enforcement. Resolve conflicts with the narrowest applicable owner.
3. Edit the canonical source. Regenerate derived provider files through their owner.
4. Validate links, imports, required sections, ownership patterns, templates, and documented commands.
5. Inspect the final diff for duplicate or unenforceable policy. Report advisory rules with no enforcement mechanism.

## Resources

- Start with the package [reference router](references/index.md).
- Run the package [governance CLI](scripts/governance.py) and [checker](scripts/check.py) for evidence.
- Use reviewed package templates under `assets/` only after verifying project facts and owners.

## Verify

- Done means changed rules have one owner, clear scope, resolving imports, valid commands, and reported advisory gaps.
- Run `python3 scripts/check.py`, `python3 -m json.tool evals/evals.json >/dev/null`, `python3 scripts/governance.py --help`, and `python3 scripts/test_governance.py` from this package.
- Use the governance CLI's documented validation mode for a target repository; never weaken a failed check to make a policy appear enforced.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark target-repository settings, external provider state, or unavailable governance evidence `UNVERIFIED`.
