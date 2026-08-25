# Merge Strategies

Scope: merge method selection and revert implications for local Git and hosted review systems. A pull request (PR) or merge request (MR) button is provider UI; the equivalent local command does not prove that the hosted repository permits or records the same method.

When to squash, rebase, or merge-commit. Based on git's actual merge behavior
and the linear history requirements of trunk-based development.

## Strategy comparison

| Strategy | Git command | Result on `main` | Revert safety | Bisect safety | Commit attribution |
| --- | --- | --- | --- | --- | --- |
| Squash merge | `git merge --squash` + `git commit` | One squashed commit | Single `git revert` | ≤ 1 bisect step | Single author (merger) |
| Rebase merge | `git rebase main && git merge --ff-only` | All original commits | Per-commit revert | Granular bisect | Original authors |
| Merge commit | `git merge --no-ff` | Merge commit + all originals | Revert merge commit | Crosses branch boundary | Original authors |

## Squash merge - default for feature work

```bash
# GitHub: "Squash and merge" button
# GitLab: "Squash commits when merge request is accepted"
# CLI:
git merge --squash feature/login && git commit -m "feat: add login form (#42)"
```

**When to use:**

- Feature branches with WIP commits (`wip`, `fix typo`, `address review`)
- Bug fix branches with a single coherent change
- Any PR where the individual commit history is noise, not signal

**When NOT to use:**

- When individual commits in the branch tell a meaningful story
- When you need to preserve multiple authors' attribution
- When the branch contains logically separate changes that should remain
  separate

## Rebase merge - when commits tell a story

```bash
# GitHub: "Rebase and merge" button
# GitLab: "Merge commit with semi-linear history" or "Fast-forward merge"
# CLI:
git checkout feature/story
git rebase main
git checkout main
git merge --ff-only feature/story
```

**When to use:**

- Each commit in the branch is a logical, self-contained change
- Multiple authors contributed distinct pieces
- You need granular `git bisect` capability

**Enforcement:**

```bash
# Require branch to be up to date before merge (GitHub)
# Settings -> Branches -> main -> "Require branches to be up to date before merging"
# This forces a rebase onto the latest main before merge.
```

## Merge commit - GitFlow only

```bash
git merge --no-ff feature/large-module
```

**When to use:**

- GitFlow (required by `--no-ff` policy - preserves the branch topology)
- Monorepo merges where you want to revert an entire feature at once

**When NOT to use:**

- Trunk-based or GitHub Flow - adds noise to history, complicates bisect
- Any workflow that requires linear history

## Revert strategies by strategy

### Squash merge revert

```bash
git revert <squash-commit-hash>
# Single revert, clean. The entire PR is undone in one commit.
```

### Rebase merge revert

```bash
git revert <commit-1> <commit-2> <commit-3>
# Must revert each commit individually, in reverse order.
# If commit order matters, this is painful.
```

### Merge commit revert

```bash
git revert -m 1 <merge-commit-hash>
# -m 1 means "revert to the first parent" (main's side).
# This undoes the entire merge but preserves the merge as a historical fact.
```

## Linear history enforcement

Both trunk-based development and GitHub Flow recommend linear history. Enforce
it at the repo level - not by convention:

```bash
# GitHub: Settings -> Branches -> main -> "Require linear history"
# This blocks merge commits on the protected branch.
# Only squash and rebase merges are allowed.

# GitLab: Settings -> Repository -> Protected branches ->
# "Allowed to merge: Maintainers" with "Merge method: Fast-forward merge"
# or "Merge method: Squash commits"
```

## Monorepo considerations

In a monorepo, merge strategy affects the entire repository's history, not just
one package's. Prefer:

- **Squash merge** for most PRs - keeps history clean at repo scale
- **Rebase merge** when a PR spans multiple packages with logically separate
  commits
- **Never** merge commit - in a monorepo, merge commits create meaningless
branch topology (the branch touched 3 packages; which one was it "about"?)

## Sources

- Git Workflows source map (see `policy-sources.md`) — provider, Git, and standards references.
- [Git reference](https://git-scm.com/docs) — merge, rebase, and revert semantics.
