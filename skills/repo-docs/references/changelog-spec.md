# CHANGELOG.md Specification

Based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

## Format

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

## Required structure

### Header

The H1 is `# Changelog`. The next lines are the format attribution and
versioning statement (see above). These are mandatory - they tell readers the
format.

### Version sections

Each version is a `##` heading:

```markdown
## [X.Y.Z] - YYYY-MM-DD
```

The version must be in brackets, the date in ISO 8601 (YYYY-MM-DD). Unreleased
changes go under `## [Unreleased]` at the top. No date on `[Unreleased]`.

### Change categories

Within each version, changes are grouped under `###` headings. Only these six
are valid:

| Category | What goes here |
| --- | --- |
| `Added` | New features |
| `Changed` | Changes in existing functionality |
| `Deprecated` | Soon-to-be-removed features |
| `Removed` | Removed features |
| `Fixed` | Bug fixes |
| `Security` | Vulnerability fixes |

Omit empty categories. Order them as listed above.

### Change entries

Each entry is a bullet point (`-`). Use the imperative mood. Describe from the
user's perspective, not the implementation:

```markdown
### Fixed
- Crash when opening files larger than 2 GB on Windows.
```

Not:

```markdown
### Fixed
- Increased the buffer size in FileReader from INT_MAX to LONG_MAX.
```

### Version links

At the bottom, link to version comparisons:

```markdown
[Unreleased]: https://github.com/owner/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/owner/repo/releases/tag/v1.0.0
```

These are not mandatory but strongly recommended - they let readers see the
exact diff for each version.

## Anti-patterns - reject on sight

1. **No version header**: every entry must be under a `## [X.Y.Z] - YYYY-MM-DD`
2. **Wrong category names**: `Additions` instead of `Added`, `Changes` instead
of `Changed`, `Bugfixes` instead of `Fixed`
3. **Implementation language**: "Refactored the parser", "Updated dependencies"
(user-facing: "Improved error messages for malformed input")
4. **Non-reverse chronological**: newest version must be first
5. **Missing Unreleased section**: a project under active development must have
`[Unreleased]` at the top
6. **Git log dump**: a list of commit messages is not a changelog. Condense,
group, and describe in user terms.
7. **No date on release**: every released version must have a date
8. **No format attribution**: the opening statement is required
