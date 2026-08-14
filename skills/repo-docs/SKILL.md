---
name: repo-docs
description: README, CHANGELOG, release notes, repository documentation; excludes governance and API reference generation.
---

# Repo Docs

## When to use

- Create, restructure, or audit README.md and translated README variants.
- Verify installation, setup, usage, architecture summaries, examples, badges, links, and support claims.
- Create or correct CHANGELOG.md and release-note entries under the repository's versioning policy.
- Add or run repository documentation checks.

## When NOT to use

- CONTRIBUTING.md, AGENTS.md, CODEOWNERS, issue forms, or pull-request templates; route to `repo-governance`.
- API reference generation from source symbols.
- Product manuals or general prose without a repository-documentation contract.

## Guardrails

- Inspect manifests, entrypoints, configuration, examples, tests, and release history before documenting commands or features.
- Run documented commands when practical; label unverified commands instead of inventing support, benchmarks, compatibility, variables, or roadmap claims.
- Preserve established public names and released history unless migration is explicitly authorized.
- Update every affected language variant or report the exact variants left stale.
- Keep README claims source-backed; use Keep a Changelog categories and Semantic Versioning semantics when the repository does.

## Workflow

1. Identify audience, documentation owner, requested files, and project status.
2. Inspect source truth and load the matching README or changelog reference.
3. Draft the smallest coherent surface with installation, minimum usage, verification, links, and support details that actually apply.
4. Run links, documented commands, changelog, and repository-specific checks; correct failures rather than suppressing them.
5. Re-read the diff for unsupported claims, stale translations, duplicated policy, and source/documentation drift.

## Quick start

```bash
find . -maxdepth 2 -type f \( -name 'README*' -o -name 'CHANGELOG*' \) -print
git diff --check
python3 scripts/check.py
```

Then inspect manifests and executable help before writing a command example.

## Reference map

- [Reference index](references/index.md) for artifact-based route selection.
- [README](references/readme.md) for required landing-page structure and claims.
- [README verification](references/readme.md#verification-checklist) for links, install, usage, and SEO checks.
- [CHANGELOG](references/changelog.md) for Keep a Changelog and release sections.
- [CHANGELOG verification](references/changelog.md#verification-checklist) for release-history validation.

## Completion

Complete when documentation matches current repository behavior, required commands and links are verified or explicitly qualified, related language variants agree, and applicable checks pass with evidence reported.

## Validation

Run from this package root:

```bash
python3 scripts/check.py
python3 -m json.tool evals/evals.json >/dev/null
python3 scripts/audit_changelog.py CHANGELOG.md  # when CHANGELOG.md exists
python3 scripts/audit_semver.py                  # when version metadata is present
```

Do not claim the conditional audits ran when their target files or metadata are absent.

## Related skills

- `repo-governance` for contributor and agent policy
- `avoid-ai-writing` for prose-level style cleanup
- `git-toolkit` for release tags and local history inspection
