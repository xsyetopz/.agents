# Release Management

## Use this reference

Load this reference when release management is part of the requested local Git state transition. Inspect current status and history first, preserve unrelated work, identify recovery, and verify the resulting state.

Versioning, tagging, and release automation patterns. Based on [Semantic
Versioning 2.0.0](https://semver.org/).

## Semantic Versioning (SemVer)

Source: [semver.org](https://semver.org/).

Given `MAJOR.MINOR.PATCH`:

- **MAJOR** - incompatible API changes
- **MINOR** - backward-compatible new functionality
- **PATCH** - backward-compatible bug fixes

Pre-release: `1.0.0-alpha.1`, `2.0.0-rc.2`, `1.0.0-beta+exp.sha.5114f85` Build
metadata: `1.0.0+20130313144700` (ignored for precedence)

### SemVer regex

From [semver.org](https://semver.org/#is-there-a-suggested-regular-expression-to-check-a-semver-string):

```regex
^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)
(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?
(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$
```

### SemVer in scripts

```bash
#!/bin/bash
# scripts/check-semver.sh - validate a version string

version="$1"
semver_regex='^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-((0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z-]*)(\.(0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z-]*))*))?(\+([0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*))?$'

if [[ "$version" =~ $semver_regex ]]; then
  echo "valid: $version"
  echo "  major=${BASH_REMATCH[1]}"
  echo "  minor=${BASH_REMATCH[2]}"
  echo "  patch=${BASH_REMATCH[3]}"
  echo "  prerelease=${BASH_REMATCH[5]}"
  echo "  buildmetadata=${BASH_REMATCH[9]}"
else
  echo "INVALID: $version" >&2
  exit 1
fi
```

## Tag conventions

### Lightweight vs annotated

```bash
# Lightweight (pointer to commit) - DO NOT USE for releases
git tag v1.0.0

# Annotated (full object with tagger, date, message) - USE THIS
git tag -a v1.0.0 -m "Release v1.0.0"
```

Annotated tags are required for `git describe` and are the standard for release
tags. They carry metadata: author, date, message, and optionally a GPG
signature.

### Signing tags

```bash
git tag -s v1.0.0 -m "Release v1.0.0"
# Uses the GPG key configured in user.signingkey
```

### Tag naming

```bash
# Standard semver tag
v1.2.3

# Pre-release
v2.0.0-beta.1
v2.0.0-rc.1

# SemVer spec says "v1.2.3" is NOT a semantic version, but prefixing
# with "v" is the universal convention for git tags.
```

### Tag operations

```bash
# Push a specific tag
git push origin v1.0.0

# Push all tags
git push --tags             # pushes both annotated and lightweight
git push --follow-tags      # pushes only annotated tags

# Delete a remote tag (BLOCKED - requires confirmation)
git push --delete origin v1.0.0

# List tags sorted by version
git tag --sort=version:refname

# Show tag message and metadata
git tag -l -n9 v1.0.0
```

## Release branches

### Pattern 1: Release from main (CD)

```bash
# No release branch. Tag main directly.
git checkout main
git pull
git tag -a v1.2.3 -m "Release v1.2.3"
git push --follow-tags
```

Best for: continuous deployment, web applications.

### Pattern 2: Short-lived release branches (trunk-based)

```bash
# Cut a release branch
git checkout -b release/1.2 main

# Harden: cherry-pick critical fixes only
git cherry-pick abc1234  # fix from main

# Tag and release
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# Merge back to main and DELETE the branch
git checkout main
git merge release/1.2
git branch -d release/1.2
```

Best for: teams releasing on a schedule (weekly, biweekly).

### Pattern 3: Long-lived release branches (GitFlow)

```bash
# For versioned products maintaining multiple releases simultaneously
# release/1.x, release/2.x - each receives hotfixes
git checkout release/1.x
git cherry-pick <hotfix-from-main>
git tag -a v1.2.1 -m "Hotfix v1.2.1"
```

Best for: libraries, mobile apps, desktop software with multiple supported
versions.

## Hotfix workflow

```bash
# 1. Find the release tag that introduced the bug
git tag --sort=version:refname | grep "^v1\."

# 2. Create a hotfix branch from that tag
git checkout -b hotfix/critical-bug v1.2.0

# 3. Fix and commit
git commit -m "fix: critical bug in auth middleware"

# 4. Tag the hotfix
git tag -a v1.2.1 -m "Hotfix v1.2.1"

# 5. Push
git push origin v1.2.1

# 6. Merge the fix forward to main
git checkout main
git cherry-pick <hotfix-commit>
```

## Release automation

### Minimum script

```bash
#!/bin/bash
# scripts/release.sh <version>
set -euo pipefail

VERSION="$1"

# Validate semver
echo "$VERSION" | grep -qE '^v?[0-9]+\.[0-9]+\.[0-9]+' || {
  echo "ERROR: invalid version: $VERSION" >&2; exit 1
}

# Ensure on main and clean
BRANCH=$(git branch --show-current)
[ "$BRANCH" = "main" ] || { echo "ERROR: must be on main branch" >&2; exit 1; }
[ -z "$(git status --porcelain)" ] || { echo "ERROR: working tree not clean" >&2; exit 1; }

# Update CHANGELOG (manual step - verify with user)
echo "Update CHANGELOG.md with $VERSION entries, then press enter."
read -r

# Commit and tag
git add CHANGELOG.md
git commit -m "chore: release $VERSION"
git tag -a "$VERSION" -m "Release $VERSION"
git push --follow-tags
```

### Pre-release checklist

Before every release tag:

- [ ] `main` is green (all CI checks passing)
- [ ] CHANGELOG.md updated with this version's entries
- [ ] Version string in source matches (e.g., `version` in `package.json`,
`Cargo.toml`, `pyproject.toml`)
- [ ] No `[Unreleased]` entries left in CHANGELOG.md for this version
- [ ] Tag protection rules active (no tag deletion, no tag overwrite)
- [ ] `git status` is clean
- [ ] Current branch is `main`
