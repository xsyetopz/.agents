---
name: git-workflows
description: Perform local Git operations, recovery, Conventional Commit fallback setup, or team branching, merge, release, and integration policy. Use for local repository state and policy; not for hosted API mutations or CI pipeline implementation.
---

# Git Workflows

Operate local Git and design team integration policy with explicit authority, recovery paths, and observed enforcement.

Define the requested local or team outcome, affected refs and files, recovery point, approval boundary, and completion checks. Read-only inspection and reversible local work may proceed. History rewrites, destructive cleanup, force-pushes, and remote mutations require exact authorization. Return commands, changed state, recovery path, and unresolved hosted or local evidence.

## Start with evidence

1. Inspect repository instructions, status, branch, upstream, relevant diffs, effective configuration, contribution guidance, hooks, and delivery constraints.
2. Classify worktree, history, and remote effects; record `HEAD` and recovery options before amend, rebase, reset, stash deletion, cherry-pick, or migration.

## Workflow

1. Load only the matching local-operation or policy reference from the direct routes below.
   - [Git Archaeology](references/local-archaeology.md) · [Bisect Guide](references/local-bisect-guide.md) · [Conventional Commits fallback](references/local-conventional-commits.md) · [Git Security Tooling](references/local-git-security-tooling.md)
   - [Git Attributes](references/local-gitattributes.md) · [Git Configuration](references/local-gitconfig.md) · [Git Hooks Guide](references/local-hooks-guide.md) · [Patch Workflows](references/local-patch-guide.md)
   - [Interactive Rebase Guide](references/local-rebase-guide.md) · [Reflog Guide](references/local-reflog-guide.md) · [Release Management](references/local-release-management.md) · [Commit Signing](references/local-signing-guide.md)
   - [Git Workflows source map](references/local-sources.md) · [Stash Guide](references/local-stash-guide.md) · [Submodules and Git LFS](references/local-submodule-lfs.md) · [Worktree Guide](references/local-worktree-guide.md)
   - [Branch Protection Rules](references/policy-branch-protection.md) · [Branching Models](references/policy-branching-models.md) · [Merge Strategies](references/policy-merge-strategies.md) · [Git Workflows source map](references/policy-sources.md)
   - [GOOD/RED recovery examples](references/examples.md) (read before changing history, worktree state, hooks, or delivery policy; RED marks a contrast, while GOOD is the recovery pattern)
2. Before staging or committing, make and record the required commit-slicing plan below.
3. Perform the narrowest authorized operation while preserving unrelated changes; obtain exact authorization for force-push, hard reset, clean, destructive deletion, pushed-history rewrite, or remote mutation.
4. For missing commit guidance, use the Conventional Commits fallback and tracked `assets/commit-msg` only after proving no existing owner; invoke accepted and rejected fixtures and verify `core.hooksPath`.

### Required commit-slicing contract

Before staging or committing, record a commit plan for each intended commit:

- **Slice purpose:** the one coherent concern this commit advances.
- **Included paths/hunks:** the explicit files and, where needed, hunks that belong to the slice.
- **Dependency/order:** any earlier slice this one requires and the safe revert order; independent revertability is the default.
- **Validation:** the checks that establish this slice is correct and reviewable.
- **Revert consequence:** what reverting this commit changes and why it does not leave unrelated behavior half-applied.

Each commit must have an explicit file/hunk set, represent one coherent concern, and be safe to revert without leaving unrelated behavior half-applied. Mixed worktrees use explicit staging; a commit is accepted only when its staged diff matches one slice. Replace giant staging patterns with explicit paths or hunks: use file-based staging for separable files and `git add -p` for separable hunks.

Separate mechanical renames, generated artifacts, behavior changes, tests, documentation, and policy changes whenever they can be reviewed or reverted independently. Keep a file's related change together when splitting it would hide the contract. Put generated source and generated output in a dedicated slice when that is the clearest review and revert boundary. Make PR reviewability observable through an understandable, manageable file set, clear mechanical-versus-semantic separation, and commit order that reviewers can follow.

Immediately before each commit, inspect all of the following and correct the slice if any result includes unrelated work:

```text
git diff --cached --check
git diff --cached
git diff --cached --name-status   # staged path inventory
<the proposed commit subject>
```

The subject convention complements this contract; a valid subject never makes a mixed or catch-all staged diff acceptable.

## Validation

1. Run `git diff --check`, applicable repository tests, and final status/history inspection; map policy claims to actual protection, checks, queues, reviews, merges, migration, and rollback evidence.
2. Return commands, changed state, recovery path, and unavailable hook, signature, LFS, hosted-setting, integration, or remote evidence as `UNVERIFIED`.

## Boundaries

- Existing repository-owned commit and contribution guidance wins over fallback policy.
- A tracked client hook applies only where installed and cannot establish hosted merge policy or behavior in other clones.
- Recommend the simplest integration model that meets measured constraints and keep policy distinct from observed enforcement.
- Hosted API work, pipeline implementation, and contributor documentation are separate concerns. Handle them directly when included in the authorized request; never stop to locate or install a companion skill.
- Use established Git mechanisms and repository-owned formats; keep new output in existing forms.
