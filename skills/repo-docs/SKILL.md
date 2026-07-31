---
name: repo-docs
description: Use when creating, auditing, or enforcing repository documentation files - README.md with SEO-adjacent structure and multilingual variants, CHANGELOG.md following Keep a Changelog conventions, and project-level documentation standards. Does not cover CONTRIBUTING.md (use repo-governance) or API reference docs.
---

# Repo Docs

Repository documentation is the public face of a project. README.md is the
landing page that search engines and humans both parse. CHANGELOG.md is the
canonical release record. Both follow strict, verifiable conventions.

## When to use

- Creating a README.md from scratch for a new project
- Auditing an existing README.md for SEO, clarity, and completeness
- Adding or auditing multilingual README translations (README.zh.md,
  README.ja.md, etc.)
- Creating or migrating a CHANGELOG.md to Keep a Changelog format
- Auditing a CHANGELOG.md for format compliance and completeness
- Reviewing a PR that touches README.md or CHANGELOG.md

## When NOT to use

- CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md - use `repo-governance`
- API reference docs, wiki pages, or multi-page documentation sites
- Writing prose style audit - use `writing-cleanup`
- Architecture decision records - use `architecture-design`
- Machine-translating READMEs without a human maintainer to keep them current

## Guardrails

These files are the project's public contract. They must be truthful, complete,
and machine-readable where the conventions specify.

### README.md - hard requirements

A valid README.md must answer, in order:

1. **What is this?** - one-paragraph description that works as a search snippet
2. **Why does it exist?** - the problem it solves, not just a feature list
3. **How do I use it?** - minimum viable install + usage
4. **How do I contribute?** - link to CONTRIBUTING.md
5. **What license?** - link to LICENSE

Missing any of these is a hard fail. A visiting developer should never have to
scroll past the fold to understand whether this project is relevant.

### CHANGELOG.md - hard requirements

Follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 1.1.0. Every
entry must be:

- Under a version header: `## [X.Y.Z] - YYYY-MM-DD`
- Grouped into standard sections: `Added`, `Changed`, `Deprecated`, `Removed`,
`Fixed`, `Security`
- In reverse chronological order (newest first)
- Describing the change from the *user's* perspective, not the implementation

Entries that describe implementation details (`Refactored the FooParser class`)
or omit the version header are rejected.

## Quick start

1. Read the existing file: `cat README.md CHANGELOG.md 2>/dev/null`
2. If README.md exists, audit against the checklist in
   `references/readme-spec.md`
3. If CHANGELOG.md exists, run the audit script:
   ```sh
   python3 scripts/audit_changelog.py CHANGELOG.md
   ```
4. Validate semver strings with:
   ```sh
   python3 scripts/audit_semver.py 1.2.3-alpha.1
   python3 scripts/audit_semver.py --from-changelog CHANGELOG.md
   python3 scripts/audit_semver.py --from-tags
   ```
5. For a new project: write README.md first, then CHANGELOG.md after the first
   release
6. Every change to either file must pass the validator before commit

## Reference map

| If you need to... | Load |
|---|---|
| Full README.md specification and SEO rules | `references/readme-spec.md` |
| Full CHANGELOG.md specification (Keep a Changelog 1.1.0) | `references/changelog-spec.md` |
| README.md audit checklist and common failures | `references/readme-audit.md` |
| CHANGELOG.md audit checklist and common failures | `references/changelog-audit.md` |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/audit_changelog.py` | Validate CHANGELOG.md against Keep a Changelog 1.1.0 |
| `scripts/audit_semver.py` | Validate version strings against SemVer 2.0.0 |

```sh
# Audit a changelog
python3 scripts/audit_changelog.py CHANGELOG.md
python3 scripts/audit_changelog.py CHANGELOG.md --json

# Audit semver
python3 scripts/audit_semver.py 1.0.0 2.1.3-alpha.1
python3 scripts/audit_semver.py --from-tags
python3 scripts/audit_semver.py --from-changelog CHANGELOG.md --json
```

## Related skills

- `repo-governance` - CONTRIBUTING.md, CODEOWNERS, AGENTS.md, PR templates
- `writing-cleanup` - prose style audit for any Markdown file
- `architecture-design` - ADRs and architecture documentation

## Validate

```sh
python3 scripts/validate_skill.py skills/repo-docs
```
