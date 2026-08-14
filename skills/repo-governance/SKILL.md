---
name: repo-governance
description: CONTRIBUTING, AGENTS, CODEOWNERS, templates, provider imports, governance policy; excludes docs, branching, and CI implementation.
---

# Repo Governance

## Use this skill

- Create or update CONTRIBUTING.md, AGENTS.md, CLAUDE.md, CODEOWNERS, provider imports, PR templates, or issue templates.
- Separate human contribution policy from coding-agent execution rules.
- Design nested instruction scope, precedence, ownership, review requirements, or validation.
- Audit governance contracts and add checks for links, imports, ownership, and documented commands.

## Rules

- Give every rule one audience, canonical owner, scope, precedence, enforcement
  mechanism, and update path.
- Keep repository defaults at the root and narrower overrides in the smallest
  owning subtree. Import or link instead of duplicating policy.
- Make instructions executable with commands, paths, evidence, and acceptance
  conditions. Do not claim prose enforces what tooling does not read.
- Permit tool assistance when contributors understand, review, test, and can
  defend the change. Maintainers may set narrower learning rules.
- Treat AI-suggested security fixes as hypotheses. Require reproduction on the
  affected system or hardware when applicable.
- Do not guess owners, contacts, bypass actors, hosted settings, or enforcement.
  Preview external changes and preserve unrelated or generated files.
- Do not use this skill for README, CHANGELOG, or release notes (use
  `$repo-docs`), branching or merge models (use `$git-workflows`), CI/CD
  implementation (use `$git-ci-cd`), or reusable skill authoring (use
  `$skill-creator`).

## Steps

1. Inventory governance files, imports, templates, CODEOWNERS rules, branch
   checks, and nested scopes.
2. Map each rule to its audience, owner, scope, precedence, and actual
   enforcement. Resolve conflicts with the narrowest applicable owner.
3. Edit the canonical source. Regenerate derived provider files through their
   owner.
4. Validate links, imports, required sections, ownership patterns, templates,
   and documented commands.
5. Inspect the final diff for duplicate or unenforceable policy. Report
   advisory rules with no enforcement mechanism.

## Resources

- Route selection: [reference index](references/index.md).
- Agent scope and external actions: [agent governance](references/agent-governance.md).
- Human and provider files: [human governance](references/human-governance.md).
- Audience, ownership, and assistance rules: [governance contracts](references/contracts.md).
- GitHub issue and PR forms: [issue templates](references/issue-templates.md).
- Current provider behavior and primary sources: [standards](references/standards.md).
- Use reviewed package templates under `assets/`; verify project facts and
  owners before filling them.

## Verify

Run from this package root:

```bash
python3 scripts/check.py
python3 -m json.tool evals/evals.json >/dev/null
python3 scripts/governance.py --help
python3 scripts/test_governance.py
```

Use the governance CLI's documented validation mode for a target repository.
Never weaken a failed check to make a policy appear enforced. Confirm changed
rules have one owner, clear scope, resolving imports, valid commands, and
reported advisory gaps.
