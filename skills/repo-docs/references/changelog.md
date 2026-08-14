# CHANGELOG.md

Use this reference for Keep a Changelog structure, user-facing entries, and
release-history verification. It is based on [Keep a Changelog
1.1.0](https://keepachangelog.com/en/1.1.0/).

## Specification

### Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description.

### Changed
- Changed behavior description.

### Fixed
- Bug fix description.

## [1.0.0] - 2024-01-15

### Added
- Initial release.
```

### Required structure

- The H1 is `# Changelog`.
- The format attribution and versioning statement follow the H1.
- Released versions use `## [X.Y.Z] - YYYY-MM-DD`.
- `[Unreleased]` appears first for an actively developed project and has no date.
- Within a version, use only `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`,
  and `Security`, in that order; omit empty categories.
- Each entry is a `-` bullet describing a user-facing change in imperative mood,
  not an implementation detail.

```markdown
### Fixed
- Crash when opening files larger than 2 GB on Windows.
```

Implementation detail:

```markdown
### Fixed
- Increased the buffer size in FileReader from INT_MAX to LONG_MAX.
```

### Version links

At the bottom, link to version comparisons when release history supports it:

```markdown
[Unreleased]: https://github.com/owner/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/owner/repo/releases/tag/v1.0.0
```

## Verification checklist

### Quick pass

- [ ] H1 is `# Changelog`.
- [ ] Format attribution and versioning statement are present.
- [ ] `[Unreleased]` is at the top for active projects.
- [ ] Version headers use `## [X.Y.Z] - YYYY-MM-DD`.
- [ ] Categories use only the six standard names and the required order.
- [ ] Entries are reverse chronological and describe user-facing changes.
- [ ] Breaking changes are marked.
- [ ] Security fixes use `Security`, not `Fixed`.
- [ ] Version links are present when release comparisons are available.

### Common failure checks

1. A missing version header leaves an entry unscoped; place it under a dated
   `## [X.Y.Z] - YYYY-MM-DD` heading.
2. A nonstandard category such as `Additions`, `Changes`, or `Bugfixes` does not
   satisfy the format; use one of the six names.
3. Implementation language such as “Refactored the parser” does not describe a
   user-facing change; state the observable behavior or omit the entry.
4. A non-reverse-chronological list obscures release order; place newest first.
5. An active project without `[Unreleased]` has no visible staging area; add it at
   the top.
6. A commit-message dump needs condensation into user-facing grouped entries.
7. A released version without a date is incomplete; add an ISO date.
8. Missing format attribution leaves the document's convention unspecified.

## Failure examples

### Missing Unreleased section

For an active project, place unreleased changes in a visible section:

```markdown
## [Unreleased]

### Added
- Dark mode support in the settings panel.

### Fixed
- Crash when opening empty files.
```

### Implementation language

```markdown
### Changed
- Migrated from Webpack to Vite.
- Refactored the authentication middleware.
- Bumped lodash from 4.17.20 to 4.17.21.
```

Use user-facing alternatives:

```markdown
### Changed
- Dev server starts 3x faster.
- Login errors now show a specific message instead of a generic 500.
```

An internal dependency update without user-visible behavior is omitted.

### Wrong category names

| Wrong | Correct |
| --- | --- |
| `### Additions` | `### Added` |
| `### New` | `### Added` |
| `### Changes` | `### Changed` |
| `### Fixes` | `### Fixed` |
| `### Bugs` | `### Fixed` |
| `### Breaking` | `### Changed` with a `BREAKING` prefix |

### Malformed version headers

```markdown
# Missing date
## [1.0.0]

# Missing brackets
## 1.0.0 - 2024-01-15

# Wrong date format
## [1.0.0] - 01/15/2024

# Correct
## [1.0.0] - 2024-01-15
```

### Git log dump

A changelog entry groups user-visible effects rather than commit identifiers:

```markdown
## [2.1.0] - 2024-06-01
- abc1234 Fix login bug
- def5678 Add dark mode
- ghi9012 Update deps
- jkl3456 Merge PR #42
```

Use categories and user-facing descriptions:

```markdown
## [2.1.0] - 2024-06-01

### Added
- Dark mode. Toggle in Settings -> Appearance.

### Fixed
- Login form redirected to the login page with a clear message when the session
  expired.
```

## Edge cases

### First release

A `1.0.0` release may omit empty categories:

```markdown
## [1.0.0] - 2024-01-01

### Added
- Initial release.
```

### Yanked releases

Mark a pulled release with `[YANKED]` and provide the replacement:

```markdown
## [1.2.1] - 2024-03-15 [YANKED]

### Security
- This release contained a regression that exposed admin routes. Upgrade to 1.2.2.
```

### Pre-release versions

Keep pre-releases in the history:

```markdown
## [2.0.0-rc.1] - 2024-05-01
## [2.0.0-beta.2] - 2024-04-15
## [2.0.0-alpha.1] - 2024-04-01
```
