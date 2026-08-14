---
name: repo-docs
description: README, CHANGELOG, release notes, repository documentation; excludes governance and API reference generation.
---

# Repo Docs

Write and audit repository documentation from current source truth.

## Use this skill

- Create, restructure, or audit README.md and translated README variants.
- Verify installation, setup, usage, architecture summaries, examples, badges, links, and support claims.
- Create or correct CHANGELOG.md and release-note entries under the repository's versioning policy.
- Add or run repository documentation checks.
- Do not use for CONTRIBUTING.md, AGENTS.md, CODEOWNERS, issue forms, pull-request templates, API reference generation, or product manuals.
- Redirect governance files to `$repo-governance`, release tags and local history to `$git-toolkit`, prose-style audits to `$avoid-ai-writing`, and pipeline work to `$git-ci-cd`.

## Rules

- Inspect manifests, entrypoints, configuration, examples, tests, and release history before documenting commands or features.
- Run documented commands when practical. Mark unverified commands instead of inventing support, benchmarks, compatibility, variables, or roadmap claims.
- Preserve public names and released history unless migration is authorized.
- Update every affected language variant or name variants left stale.
- Keep claims tied to repository evidence. Follow Keep a Changelog and Semantic Versioning when the repository uses them.

## Steps

1. Identify audience, documentation owner, requested files, and project status.
2. Inspect source truth, language variants, and release history; use the reference router to select README or changelog guidance.
3. Draft the smallest coherent surface: installation, minimum usage, verification, links, and support details that apply.
4. Check links and documented commands. Run repository checks and conditional changelog or version audits when inputs exist.
5. Re-read for unsupported claims, stale translations, duplicated policy, and source or documentation drift.

## Resources

- Start with the package [reference router](references/index.md).
- Run the package [checker](scripts/check.py) and conditional documentation audits when their inputs exist.

## Verify

- Done means documented commands and links match source truth, affected variants are updated or named, and unsupported claims are absent.
- Run `find . -maxdepth 2 -type f \( -name 'README*' -o -name 'CHANGELOG*' \) -print`, `git diff --check`, `python3 scripts/check.py`, and `python3 -m json.tool evals/evals.json >/dev/null`.
- When target files or metadata exist, also run `python3 scripts/audit_changelog.py CHANGELOG.md` and `python3 scripts/audit_semver.py`.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark skipped conditional audits, unavailable commands, or unchecked links `UNVERIFIED`.
