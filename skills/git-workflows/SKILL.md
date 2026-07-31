---
name: git-workflows
description: Use when selecting, designing, or auditing branching models and merge strategies - GitHub Flow, GitFlow, trunk-based development, GitLab Flow, forking workflow, monorepo branching, and release flow integration. Covers when to merge vs squash vs rebase, short-lived branch discipline, and workflow enforcement through branch protection rules. Do not use for local git commands (use git-toolkit) or CI/CD pipeline YAML (use git-ci-cd).
---

# Git Workflows

A branching model is a team contract - it defines how work flows from idea to
production. Pick the wrong one and you get merge hell, broken builds, and
release paralysis. Pick the right one and you ship daily without ceremony.

This skill is opinionated: it recommends specific models for specific team
shapes and rejects patterns that sound reasonable but fail at scale.

## When to use

- Choosing a branching model for a new project or team
- Migrating from one model to another (e.g. GitFlow -> trunk-based)
- Designing a monorepo branching strategy
- Setting up merge strategy enforcement (merge vs squash vs rebase)
- Auditing an existing workflow for bottlenecks, merge conflicts, or release lag
- Configuring branch protection rules to enforce the chosen model

## When NOT to use

- Running git commands - use `git-toolkit`
- Writing CI/CD pipeline YAML - use `git-ci-cd`
- Designing how releases are versioned - see `git-toolkit` skill for release
  management patterns

## Guardrails

A workflow is only as good as its enforcement. Branch protection rules are the
mechanism - the workflow is the policy. Never recommend a workflow without also
recommending the branch protection rules that enforce it.

### Hard rules

1. **No long-lived feature branches.** Any branch that lives more than 2 days is
   a
long-lived branch. It will conflict, diverge, and cause integration pain.
Source: [Trunk-Based Development](https://trunkbaseddevelopment.com/).

2. **Protected main branch.** Direct push to `main`/`master` is blocked. All
changes go through pull requests with required reviews and status checks.
Source: [GitHub branch
protection](https://docs.github.com/en/repositories/configuring-branches-and-
merges-in-your-repository/managing-protected-branches).

3. **Linear history on main.** Squash merge or rebase merge - never a merge
commit that creates a non-linear graph. Linear history makes `git bisect` and
`git revert` reliable.

4. **Delete branches after merge.** Stale branches accumulate, confuse new
contributors, and waste CI minutes. Automate this in repo settings.

## Models

### GitHub Flow - the default for most teams

Source: GitHub's recommended workflow. Simple, pull-request-based, one long-
lived branch (`main`). Feature branches are short-lived, created from `main`,
and merged back via pull request.

- **Branch off:** `main`
- **Merge back:** squash merge or rebase merge
- **Release from:** `main` (continuous delivery) or release branches cut from
  `main`
- **Best for:** Teams of 1-50 developers, continuous deployment, web
  applications
- **Enforcement:** Branch protection on `main` - require PR, require reviews,
  require status checks

### Trunk-Based Development - high-throughput teams

Source: [trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/). All
developers commit to a single branch (`main`/`trunk`) at least once every 24
hours. Short-lived feature branches (hours, not days) for code review. Release
branches are cut from trunk on a just-in-time basis, hardened, and deleted after
release. Alternatively, release directly from trunk with feature flags.

- **Branch off:** `main` (or commit directly for very small teams)
- **Merge back:** squash merge to `main`, daily
- **Release from:** `main` (with feature flags) or short-lived release branches
- **Best for:** Teams of 5-500+ developers, CI/CD pipelines, monorepos
- **Key techniques:** Feature flags, branch by abstraction, comprehensive test
  suite
- **Enforcement:** Branch protection on `main`, required status checks, linear
  history

> "Shared branches off mainline are bad at any release cadence." - trunkbaseddevelopment.com

### GitFlow - legacy, for versioned products with long release cycles

Source: [A successful Git branching model](https://nvie.com/posts/a-successful-
git-branching-model/) (Vincent Driessen, 2010). Two permanent branches: `main`
(production releases) and `develop` (integration). Feature branches from
`develop`, release branches from `develop`, hotfix branches from `main`.
Complex, heavy ceremony.

- **Branch off:** `develop` for features, `main` for hotfixes
- **Merge back:** `--no-ff` merge commits (preserve branch topology)
- **Release from:** `main` (tagged releases)
- **Best for:** Versioned products with scheduled releases (mobile apps, desktop
  software, libraries with major version bumps)
- **Warning:** Overkill for most web applications. Adds ceremony without
  proportional benefit. Trunk-based development achieves the same release
  discipline with less overhead.

### GitLab Flow - environment-based branching

Source: GitLab's recommended workflow. Extends GitHub Flow with environment
branches (`staging`, `production`). Code flows `main -> staging -> production`
through merge requests.

- **Branch off:** `main`
- **Merge back:** squash or rebase to `main`, then merge commits from `main` to
  `staging` to `production`
- **Release from:** `production` branch
- **Best for:** Teams with staged deployment environments, manual QA gates
- **Enforcement:** Branch protection on all environment branches

### Forking workflow - open source, external contributors

Contributors fork the repo, work in their fork, and submit pull requests.
Maintainers merge from forks into the upstream.

- **Branch off:** fork's `main`
- **Merge back:** PR from fork to upstream
- **Best for:** Open source projects with external contributors, large
  organizations with cross-team contributions
- **Enforcement:** Require PR from forks, limit `GITHUB_TOKEN` permissions,
  never use `pull_request_target`

## Merge strategies

| Strategy | History shape | When to use |
|---|---|---|
| **Squash merge** | Linear, one commit per PR | Feature work, bug fixes. Default for GitHub Flow and trunk-based. |
| **Rebase merge** | Linear, all commits preserved | When individual commits in a PR tell a meaningful story. |
| **Merge commit** | Non-linear, preserves branch topology | GitFlow (required by `--no-ff` policy). Avoid otherwise. |

### Enforcement

```bash
# Repository settings -> require linear history
# GitHub: Settings -> Branches -> main -> "Require linear history"
# GitLab: Settings -> Repository -> Protected branches -> "Allowed to merge: Maintainers"
#         with "Merge method: Fast-forward" or "Squash"
```

Set the merge method at the repo level so it can't be overridden per-PR.

## Reference map

| If you need to... | Load |
|---|---|
| Detailed comparison of all branching models | `references/branching-models.md` |
| Merge strategy tradeoffs and enforcement | `references/merge-strategies.md` |
| Branch protection rule templates | `references/branch-protection.md` |

## Related skills

- `git-toolkit` - local git commands: rebase, merge, cherry-pick, bisect
- `git-ci-cd` - CI/CD pipeline configuration that enforces these workflows
- `repo-docs` - CHANGELOG.md and README.md
- `repo-governance` - CONTRIBUTING.md, CODEOWNERS, PR templates

## Validate

```sh
python3 scripts/validate_skill.py skills/git-workflows
```
