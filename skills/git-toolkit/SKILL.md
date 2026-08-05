---
name: git-toolkit
description: >
  Use for local Git repository operations and commit execution: status, diff, add, stage, unstage, commit, Conventional Commits, commit messages, amend, restore, reset, checkout, switch, branch, tag, merge, squash, fixup, interactive rebase, cherry-pick, revert, bisect, blame, log, reflog recovery, stash, worktree, submodule, Git LFS, hooks, signing, patches, release tags, and repository archaeology. Trigger when the user says stage changes, stage all, commit this, commit all, make a commit, conventional commit, amend the commit, squash commits, rebase, undo a commit, recover a branch, inspect Git history, or prepare a patch. Not for GitHub or GitLab APIs, CI/CD YAML, or choosing an organization-wide branching model.
---

# Git Toolkit

Execute local Git work without losing unrelated changes or rewriting shared
history accidentally. Use repository evidence to choose the narrowest command.

## When to use

- Status, diff, staging, unstaging, committing, restoring, branching, tagging, or local merging
- Conventional Commit selection and commit-message construction
- Amend, fixup, squash, rebase, cherry-pick, revert, bisect, reflog, or recovery
- Stashes, worktrees, submodules, Git LFS, hooks, signing, patches, or archaeology
- Release tags and local release-history inspection

## When NOT to use

- GitHub or GitLab API operations; use git-actions
- CI/CD pipeline authoring; use git-ci-cd
- Team branching, merge, or branch-protection policy; use git-workflows
- Push, publish, release, or remote mutation without exact user authorization

## Quick start

1. Read git status --short, current branch, and relevant staged/unstaged diffs.
2. Preserve unrelated user or concurrent changes; stage explicit paths when scope is bounded.
3. Choose the smallest command sequence that achieves the requested state.
4. For a commit, verify the staged diff, run applicable checks, write a truthful message, and commit once.
5. Re-read status and log after mutation.

## Commit workflow

For requests such as stage and commit, commit all, or use Conventional Commits:

1. Determine whether all worktree changes are in scope. If the user says all, include all non-generated changes except artifacts that should never be versioned.
2. Inspect status and diffs before staging.
3. Remove only generated artifacts created by this task; never discard unrelated work.
4. Stage the authorized paths.
5. Run git diff --cached --check and relevant validation.
6. Inspect git diff --cached --stat and enough staged content to choose the message.
7. Use type(optional-scope): imperative summary. Common types are feat, fix, docs, refactor, test, build, ci, chore, perf, style, and revert.
8. Commit, then verify status and the new log entry.

Do not call ordinary repository commits advanced and route around this skill. Stage,
commit, and Conventional Commit requests belong here.

## Guardrails

Classify by effect, not command name.

### Tier 1 - SAFE

Read-only and reversible local work: status, log, diff, show, blame, reflog,
branch/tag listing, format-patch, worktree listing, and non-destructive inspection.
Staging and a new local commit are authorized when the user asked to stage or
commit.

### Tier 2 - CAUTION

Local history or worktree mutation that may require recovery: amend of an unpushed
commit, interactive rebase of unpublished work, mixed/soft reset, stash deletion,
conflict-prone cherry-pick, submodule removal, and LFS migration. State the
consequence and verify the recovery point before execution.

### Tier 3 - BLOCKED

Require explicit confirmation for force push, remote branch deletion, hard reset,
clean, destructive branch deletion, rewriting pushed history, filter-repo,
repository-wide LFS migration, or deleting all stashes. Never infer authorization
from a request to commit.

### Pre-operation checklist

For Tier 2 or Tier 3 operations:

1. Record current branch and HEAD.
2. Inspect status and upstream relation.
3. Identify affected paths and commits.
4. State recovery method.
5. Verify final status and history.

## Command catalog

| Task | Typical commands | Load |
|---|---|---|
| Stage or commit | git status, git diff, git add, git diff --cached, git commit | references/tooling.md |
| Rebase or fixup | git rebase -i, git commit --fixup | references/rebase-guide.md |
| Find regression | git bisect | references/bisect-guide.md |
| Parallel workspace | git worktree | references/worktree-guide.md |
| Save partial work | git stash | references/stash-guide.md |
| Recover commits | git reflog | references/reflog-guide.md |
| Submodules or LFS | git submodule, git lfs | references/submodule-lfs.md |
| Hooks or signing | hook and signing commands | references/hooks-guide.md, references/signing-guide.md |
| Patches | format-patch, am, apply, cherry-pick | references/patch-guide.md |
| History search | log -S, log -G, blame | references/archaeology.md |
| Releases | tags and release history | references/release-management.md |

## Reference map

Use the command-catalog routing above. Also load references/gitconfig.md for team
Git configuration and references/gitattributes.md for EOL, diff, merge, or binary
attribute behavior.

## Completion

Complete when the requested repository state is achieved, unrelated changes remain
intact, staged and committed content matches authorization, validation results are
reported accurately, and status/history confirm the result.

## Related skills

- git-workflows for team branching and merge policy
- git-actions for GitHub and GitLab APIs
- git-ci-cd for pipeline configuration
