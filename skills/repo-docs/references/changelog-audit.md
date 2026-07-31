# CHANGELOG.md Audit Checklist

## Quick pass (2 minutes)

- [ ] H1 is `# Changelog` (not "Change Log", "Release Notes", or "History")
- [ ] Format attribution line is present
- [ ] `[Unreleased]` section exists at the top (for active projects)
- [ ] Version headers use `## [X.Y.Z] - YYYY-MM-DD` format
- [ ] Categories use only the 6 standard names
- [ ] Entries are in reverse chronological order
- [ ] Version links at the bottom (recommended)

## Content audit

- [ ] Every entry describes a user-facing change
- [ ] No implementation details (`Refactored X`, `Updated dependency Y`)
- [ ] No commit message dumps
- [ ] Breaking changes are clearly marked
- [ ] Security fixes are in the `Security` category, not `Fixed`

## Common failures and fixes

### Missing Unreleased section

For any project under active development, unreleased changes must be visible:

```markdown
## [Unreleased]

### Added
- Dark mode support in the settings panel.

### Fixed
- Crash when opening empty files.
```

Without this, contributors don't know where to add their changelog entries.

### Implementation language

Bad:

```markdown
### Changed
- Migrated from Webpack to Vite.
- Refactored the authentication middleware.
- Bumped lodash from 4.17.20 to 4.17.21.
```

Good:

```markdown
### Changed
- Dev server starts 3x faster.
- Login errors now show a specific message instead of a generic 500.
- (No user-facing change for lodash bump - omit it.)
```

### Wrong category names

Only these six are valid. Any variation is a hard fail:

| Wrong | Correct |
| --- | --- |
| `### Additions` | `### Added` |
| `### New` | `### Added` |
| `### Changes` | `### Changed` |
| `### Fixes` | `### Fixed` |
| `### Bugs` | `### Fixed` |
| `### Breaking` | `### Changed` (with BREAKING prefix in entry) |

### Version header malformed

```markdown
# Bad - no date
## [1.0.0]

# Bad - no brackets
## 1.0.0 - 2024-01-15

# Bad - wrong date format
## [1.0.0] - 01/15/2024

# Correct
## [1.0.0] - 2024-01-15
```

### Git log dump

This is a changelog, not `git log --oneline`:

Bad:

```markdown
## [2.1.0] - 2024-06-01
- abc1234 Fix login bug
- def5678 Add dark mode
- ghi9012 Update deps
- jkl3456 Merge PR #42
```

Good:

```markdown
## [2.1.0] - 2024-06-01

### Added
- Dark mode. Toggle in Settings -> Appearance.

### Fixed
- Login form would silently fail when the session expired. It now redirects
  to the login page with a clear message.
```

## Edge cases

### First release

A `1.0.0` release can omit `Changed`, `Deprecated`, `Removed`, and `Security` if
there's nothing to report:

```markdown
## [1.0.0] - 2024-01-01

### Added
- Initial release.
```

### YANKED releases

Mark a pulled release with `[YANKED]`:

```markdown
## [1.2.1] - 2024-03-15 [YANKED]

### Security
- This release contained a regression that exposed admin routes. Do not use.
  Upgrade to 1.2.2.
```

### Pre-release versions

```markdown
## [2.0.0-rc.1] - 2024-05-01
## [2.0.0-beta.2] - 2024-04-15
## [2.0.0-alpha.1] - 2024-04-01
```

Keep them in the changelog. They document the path to the final release.
