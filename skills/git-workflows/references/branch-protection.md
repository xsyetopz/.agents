# Branch Protection Rules

## Use this reference

Load this reference when branch protection is part of the team integration decision. Compare policy against measured delivery constraints and map every selected rule to repository enforcement.

Branch protection is the enforcement mechanism for branching models. Without it,
a workflow is a suggestion. With it, a workflow is a contract.

Source: [GitHub branch protection
docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)

## Minimum protection for `main` (all models)

```yaml
# GitHub repository ruleset (preferred over legacy branch protection)
# Settings -> Rules -> Rulesets -> New ruleset -> New branch ruleset

target: "refs/heads/main"

rules:
  - type: "pull_request"
    parameters:
      required_approving_review_count: 1
      dismiss_stale_reviews: true
      require_code_owner_review: true

  - type: "required_status_checks"
    parameters:
      strict_required_status_checks: true
      # List of required check names (e.g., "CI / test", "CI / lint")

  - type: "required_linear_history"
    # Blocks merge commits. Only squash and rebase allowed.

  - type: "deletion"
    # Blocks branch deletion

  - type: "non_fast_forward"
    # Blocks force pushes

bypass_actors: []  # No one bypasses - not even admins
```

## Model-specific configurations

### GitHub Flow / Trunk-Based

```yaml
# Additional rules for fast-release models
- type: "required_status_checks"
  parameters:
    strict_required_status_checks: true
    # The branch must be up-to-date with main before merging.
    # This forces rebase onto latest main.

# Require conversation resolution
- type: "required_conversation_resolution"
```

### GitFlow

```yaml
# Protect main AND develop
target: "refs/heads/main"
# ... same as above ...

target: "refs/heads/develop"
rules:
  - type: "pull_request"
    parameters:
      required_approving_review_count: 1
  - type: "required_status_checks"
  - type: "deletion"
  - type: "non_fast_forward"
  # GitFlow does NOT require linear history on develop
```

### GitLab Flow

```yaml
# Protect environment branches with stricter rules as you go right
target: "refs/heads/main"
# Standard protection

target: "refs/heads/staging"
# Same as main + require specific approvers

target: "refs/heads/production"
# Same as staging + require 2 reviews + deployment freeze windows
```

## GitLab equivalent

Source: [GitLab protected
branches](https://docs.gitlab.com/ee/user/project/protected_branches.html)

```yaml
# Settings -> Repository -> Protected branches

main:
  allowed_to_merge:
    - maintainers
  allowed_to_push:
    - no one
  allow_force_push: false
  code_owner_approval_required: true
```

## Tag protection

```yaml
# GitHub: Settings -> Rules -> Rulesets -> New tag ruleset
target: "refs/tags/v*"

rules:
  - type: "deletion"       # Block tag deletion
  - type: "non_fast_forward"  # Block tag overwrite
  - type: "creation"       # Only specific roles can create tags matching v*

# GitLab: Settings -> Repository -> Protected tags
tag: v*
allowed_to_create: maintainers
```

Without tag protection, anyone with write access can delete or move release
tags, silently breaking version resolution for downstream consumers.

## Automated enforcement (API)

```bash
# GitHub CLI - get current rules
gh api /repos/owner/repo/rulesets

# GitHub CLI - get branch protection status
gh api /repos/owner/repo/branches/main/protection

# Check if linear history is required (critical for trunk-based)
gh api /repos/owner/repo/branches/main/protection/required_linear_history
```
