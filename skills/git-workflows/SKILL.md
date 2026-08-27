---
name: git-workflows
description: Use this skill when performing local Git operations, recovery, Conventional Commit fallback setup, or team branching, merge, release, and integration policy; use $git-actions for hosted API mutations and $git-ci-cd for pipeline implementation.
---

# Git Workflows

Operate local Git and design team integration policy with explicit authority, recovery paths, and observed enforcement.

Define the requested local or team outcome, affected refs and files, recovery point, approval boundary, and completion checks. Read-only inspection and reversible local work may proceed. History rewrites, destructive cleanup, force-pushes, and remote mutations require exact authorization. Return commands, changed state, recovery path, and unresolved hosted or local evidence.

## Workflow

1. Inspect repository instructions, status, branch, upstream, relevant diffs, effective configuration, contribution guidance, hooks, and delivery constraints.
2. Classify worktree, history, and remote effects; record `HEAD` and recovery options before amend, rebase, reset, stash deletion, cherry-pick, or migration.
3. Load only the matching local-operation or policy reference from the direct routes below.
   - [Git Archaeology](references/local-archaeology.md) · [Bisect Guide](references/local-bisect-guide.md) · [Conventional Commits fallback](references/local-conventional-commits.md) · [Git Security Tooling](references/local-git-security-tooling.md)
   - [Git Attributes](references/local-gitattributes.md) · [Git Configuration](references/local-gitconfig.md) · [Git Hooks Guide](references/local-hooks-guide.md) · [Patch Workflows](references/local-patch-guide.md)
   - [Interactive Rebase Guide](references/local-rebase-guide.md) · [Reflog Guide](references/local-reflog-guide.md) · [Release Management](references/local-release-management.md) · [Commit Signing](references/local-signing-guide.md)
   - [Git Workflows source map](references/local-sources.md) · [Stash Guide](references/local-stash-guide.md) · [Submodules and Git LFS](references/local-submodule-lfs.md) · [Worktree Guide](references/local-worktree-guide.md)
   - [Branch Protection Rules](references/policy-branch-protection.md) · [Branching Models](references/policy-branching-models.md) · [Merge Strategies](references/policy-merge-strategies.md) · [Git Workflows source map](references/policy-sources.md)
   - [GOOD/RED recovery examples](references/examples.md) (read before changing history, worktree state, hooks, or delivery policy; RED marks a contrast, while GOOD is the recovery pattern)
4. Perform the narrowest authorized operation while preserving unrelated changes; obtain exact authorization for force-push, hard reset, clean, destructive deletion, pushed-history rewrite, or remote mutation.
5. For missing commit guidance, use the Conventional Commits fallback and tracked `assets/commit-msg` only after proving no existing owner; invoke accepted and rejected fixtures and verify `core.hooksPath`.
6. Run `git diff --check`, applicable repository tests, and final status/history inspection; map policy claims to actual protection, checks, queues, reviews, merges, migration, and rollback evidence.
7. Return commands, changed state, recovery path, and unavailable hook, signature, LFS, hosted-setting, integration, or remote evidence as `UNVERIFIED`.

## Gotchas

- Existing repository-owned commit and contribution guidance wins over fallback policy.
- A tracked client hook applies only where installed and cannot establish hosted merge policy or behavior in other clones.
- Recommend the simplest integration model that meets measured constraints and keep policy distinct from observed enforcement.
- Route hosted API work to `$git-actions`, pipeline implementation to `$git-ci-cd`, and contributor documentation or CODEOWNERS to `$repository-documentation`.
- Use established Git mechanisms and repository-owned formats; keep new output in existing forms.
