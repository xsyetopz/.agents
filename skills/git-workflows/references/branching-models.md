# Branching Models

Comparative analysis of branching models. Source data from
[trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/), [GitHub
Flow](https://docs.github.com/en/get-started/using-git/github-flow), [nvie.com
GitFlow](https://nvie.com/posts/a-successful-git-branching-model/), [GitLab
Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html).

## Comparison matrix

| Model | Long-lived branches | Feature branch lifespan | Release strategy | Team size sweet spot | Merge hell risk |
| --- | --- | --- | --- | --- | --- |
| GitHub Flow | 1 (`main`) | Hours to 1 day | CD from `main` | 1-50 | Low (short branches) |
| Trunk-Based | 1 (`main`) | Hours (or direct commit) | CD from `main` or short-lived release branches | 5-500+ | Very low (daily integration) |
| GitFlow | 2 (`main`, `develop`) | Days to weeks | Scheduled from `develop` through release branches | 5-50 | Medium (long branches) |
| GitLab Flow | 1 + env branches | Hours to 1 day | Staged through environment branches | 10-100 | Low (short branches) |
| Forking | 1 (per fork) | Days to weeks | Upstream maintainer merges | 50+ (OSS) | High (divergent forks) |

## GitHub Flow - detailed

The default for most GitHub-hosted projects. One rule: anything in the `main`
branch is deployable.

**Branch lifecycle:**

```text
main
  ├── feature/login-form  (hours)
  │   ├── commit
  │   └── PR -> squash merge -> delete branch
  ├── fix/typo            (minutes)
  │   └── PR -> squash merge -> delete branch
  └── feature/api-v2      (hours)
      └── PR -> squash merge -> delete branch
```

**When it breaks:**

- Feature branches live more than 2 days -> conflicts pile up
- CI is slow (more than 10 min) -> developers batch work into larger PRs
- No branch protection on `main` -> direct pushes bypass review
- Release process is manual and ceremonial -> `main` stops being deployable

**Enforcement:**

```yaml
# GitHub branch protection for main
required_pull_request_reviews:
  required_approving_review_count: 1
  dismiss_stale_reviews: true
required_status_checks:
  strict: true  # branch must be up to date
required_linear_history: true
```

## Trunk-Based Development - detailed

From [trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/):

> "A source-control branching model, where developers collaborate on code in a
> single branch called 'trunk' and resist any pressure to create other
> long-lived development branches."

Key insight: the dividing line between "small team" and "scaled" is commit rate,
not team size. When commits to trunk happen frequently enough that manual review
becomes a bottleneck, you introduce short-lived feature branches for review --
but never for artifact creation or publication.

**Release strategies:**

1. **Release from trunk** (CD): every commit to trunk is a release candidate.
Feature flags control what's live. Bug fixes are "fix forward" - commit to
trunk, deploy immediately.

2. **Release branches** (scheduled): cut from trunk on a schedule (daily,
   weekly),
hardened with bug fixes cherry-picked back to trunk, deleted after release.
Google uses this at scale with 35,000+ developers on a single trunk.

**Required techniques (from trunkbaseddevelopment.com):**

- Feature flags for hedging on release order
- Branch by abstraction for large changes
- Comprehensive automated test suite (pre-commit and CI)
- Build server that verifies every commit post-merge

## GitFlow - detailed

Two permanent branches. Heavy ceremony. Only justified when:

- You ship versioned products (mobile apps, desktop software, libraries)
- You need to maintain multiple release lines simultaneously
- Your release cycle is measured in weeks or months

**Branch types:**

```graph
graph TD
  main[main] --> m1((●)) --> m2((●)) --> m3((●))
  m1 --> r1((●)) --> r2((●))
  m1 --> d1((●)) --> d2((●)) --> d3((●)) --> d4((●)) --> d5((●))
  d2 --> f1((●)) --> f2((●)) --> f3((●))
  d4 --> r3((●)) --> r4((●))
```

**Anti-patterns (when GitFlow is wrong):**

- Web applications - you don't maintain multiple versions simultaneously
- Continuous deployment - release branches add days of delay
- Small teams (< 5) - the ceremony exceeds the benefit
- Microservices - each service deploys independently; GitFlow assumes a
  monolith

## Forking workflow - detailed

The standard for open source. Every contributor works in their own fork.
Maintainers pull from forks into the upstream.

**Fork PR safety (critical):**

Per [trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/) and GitHub
security docs, never use `pull_request_target` for fork PRs - it gives the PR
code full write access to the upstream repo. Always use `pull_request` with
`permissions: contents: read`.

## Decision flowchart

```graph
graph TD
  A{Is the project open source with external contributors?} -->|Yes| B[Forking workflow]
  A -->|No| C{Do you ship versioned products with long release cycles?}
  C -->|Yes| D[GitFlow\n(but question this - is trunk-based with release branches sufficient?)]
  C -->|No| E{Do you deploy continuously with feature flags?}
  E -->|Yes| F[Trunk-Based Development]
  E -->|No| G[GitHub Flow\n(the safe default)]
```
