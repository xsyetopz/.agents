---
name: repo-docs
description: README, CHANGELOG, release notes, repository documentation; excludes governance and API reference generation.
---

# Repo Docs

## Use this skill

- Create, restructure, or audit README.md and translated README variants.
- Verify installation, setup, usage, architecture summaries, examples, badges, links, and support claims.
- Create or correct CHANGELOG.md and release-note entries under the repository's versioning policy.
- Add or run repository documentation checks.

## Rules

- Inspect manifests, entrypoints, configuration, examples, tests, and release
  history before documenting commands or features.
- Run documented commands when practical. Mark unverified commands instead of
  inventing support, benchmarks, compatibility, variables, or roadmap claims.
- Preserve public names and released history unless migration is authorized.
- Update every affected language variant or name the variants left stale.
- Keep claims tied to repository evidence. Follow Keep a Changelog and
  Semantic Versioning when the repository uses them.
- Do not use this skill for CONTRIBUTING.md, AGENTS.md, CODEOWNERS, issue forms,
  pull-request templates, or other governance files; route those to
  `$repo-governance`. Route API reference generation and product manuals to
  their owning tools. Use `$avoid-ai-writing` for a prose-style audit.

## Steps

1. Identify the audience, documentation owner, requested files, and project
   status.
2. Inspect source truth, language variants, and release history. Load the
   matching README or changelog resource.
3. Draft the smallest coherent surface: installation, minimum usage,
   verification, links, and support details that apply.
4. Check links and documented commands. Run repository checks and conditional
   changelog or version audits when their inputs exist.
5. Re-read for unsupported claims, stale translations, duplicated policy, and
   source/documentation drift.

## Resources

- Route selection: [reference index](references/index.md).
- README structure and claims: [README](references/readme.md).
- README verification: [README checklist](references/readme.md#verification-checklist).
- CHANGELOG format and release sections: [CHANGELOG](references/changelog.md).
- CHANGELOG verification: [CHANGELOG checklist](references/changelog.md#verification-checklist).
- Route governance files to `$repo-governance`; route release tags and local
  history to `$git-toolkit`.

## Verify

Run from this package root:

```bash
find . -maxdepth 2 -type f \( -name 'README*' -o -name 'CHANGELOG*' \) -print
git diff --check
python3 scripts/check.py
python3 -m json.tool evals/evals.json >/dev/null
```

When the target files or metadata exist, also run:

```bash
python3 scripts/audit_changelog.py CHANGELOG.md
python3 scripts/audit_semver.py
```

Report skipped conditional checks and any unverified command or link.
