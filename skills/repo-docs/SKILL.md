---
name: repo-docs
description: >
  Use when creating, rewriting, auditing, or enforcing repository documentation, especially README.md, README variants, CHANGELOG.md, release notes, project overviews, installation guides, usage guides, badges, navigation, tables of contents, multilingual documentation, Keep a Changelog structure, Semantic Versioning entries, and documentation validation. Trigger phrases include write the README, update README, fix documentation, audit docs, add installation instructions, document usage, update changelog, release notes, Keep a Changelog, docs drift, and repository documentation. Not for CONTRIBUTING.md, AGENTS.md, CODEOWNERS, pull-request templates, or API reference generation.
---

# Repo Docs

Produce repository documentation that is accurate against the working tree,
scannable for its audience, and mechanically verifiable where possible.

## When to use

- Creating or restructuring README.md and translated README variants
- Auditing installation, setup, usage, architecture overview, examples, or badges
- Creating or correcting CHANGELOG.md and release-note entries
- Adding repository-level documentation checks

## When NOT to use

- CONTRIBUTING.md, AGENTS.md, CODEOWNERS, issue templates, or PR templates; use repo-governance
- API reference generation from source symbols
- Product manuals or general prose without a repository-documentation contract

## Guardrails

- Inspect package manifests, executable entrypoints, configuration, examples, and existing scripts before documenting commands or features.
- Run documented commands when practical; otherwise label them unverified.
- Do not invent support claims, benchmarks, compatibility, roadmap items, environment variables, or installation methods.
- Preserve established public names and release history unless the user requests a migration.
- Update all language variants affected by a shared factual change, or report the exact variants left stale.

### README.md - hard requirements

A README should make project identity, purpose, status, installation, minimum
working usage, configuration, verification, support, license, and links easy to
find when those sections apply. Remove empty boilerplate and duplicate prose.

### CHANGELOG.md - hard requirements

Use Keep a Changelog categories and Semantic Versioning semantics where the
repository follows them. Record user-visible changes, not commit-log noise. Do
not rewrite released history without explicit authorization.

## Quick start

1. Determine audience, documentation owner, project status, and requested files.
2. Inspect source truth: manifests, CLI help, configuration, examples, tests, and releases.
3. Load the matching README or changelog specification.
4. Draft or edit the smallest coherent documentation surface.
5. Run link, command, changelog, and repository-specific checks.
6. Re-read the final diff for unsupported claims and cross-file drift.

## Reference map

| Need | Load |
|---|---|
| README requirements | references/readme-spec.md |
| README audit procedure | references/readme-audit.md |
| CHANGELOG requirements | references/changelog-spec.md |
| CHANGELOG audit procedure | references/changelog-audit.md |

## Scripts

Use repository scripts when applicable:

    python3 skills/repo-docs/scripts/audit_changelog.py CHANGELOG.md
    python3 skills/repo-docs/scripts/audit_semver.py

Do not suppress a failed documentation check. Correct the source, command, link,
or checker.

## Completion

Complete when documentation matches current repository behavior, required commands
and links are verified or explicitly qualified, related language variants agree,
and all applicable documentation checks pass.

## Related skills

- repo-governance for contributor and agent policy
- avoid-ai-writing for prose-level style cleanup
- git-toolkit for release tags and local history inspection
