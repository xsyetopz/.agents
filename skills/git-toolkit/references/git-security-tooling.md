# Git Security Tooling

Scope: local secret scanning and repository-size tooling. Static application security testing (SAST) can flag candidate secrets but cannot prove whether a token is live or revoked; never upload repository contents or expose findings without authorization.

Production tools for Git safety. Do not invent a pre-commit hook or security
check when a maintained tool already exists. Tool choice and command examples
are local guidance; verify each project's current release and permissions in
the [Git Toolkit source map](sources.md).

## Secret scanning (pre-commit)

- **[gitleaks](https://github.com/gitleaks/gitleaks)** - SAST for secrets in
  Git repos. Pre-commit hook, CI, and CLI scanning.

  ```bash
  gitleaks detect --source . --verbose
  gitleaks protect --staged
  ```

- **[trufflehog](https://github.com/trufflesecurity/trufflehog)** - Scans
  history and branches for high-entropy secrets. Verifies against live APIs.

  ```bash
  trufflehog git file://. --only-verified
  ```

- **[git-secrets](https://github.com/awslabs/git-secrets)** - AWS-maintained
  pre-commit hook. Blocks AWS credentials and custom regex patterns.

  ```bash
  git secrets --install
  git secrets --register-aws
  git secrets --scan-history
  ```

## Hook managers

- **[pre-commit](https://github.com/pre-commit/pre-commit)** - Multi-language
  framework. Configure via `.pre-commit-config.yaml`.

  ```bash
  pre-commit install
  pre-commit run --all-files
  ```

- **[lefthook](https://github.com/evilmartians/lefthook)** - Fast, Go-based.
  Language-agnostic, parallel execution.

  ```bash
  lefthook install
  lefthook run pre-commit
  ```

## History sanitization

`git filter-repo` and BFG rewrite object IDs and can destroy recovery paths. Make a backup, confirm exact paths and authorization, and verify refs before considering the operation complete; remote cleanup remains outside this package and `UNVERIFIED` until checked.

- **[git-filter-repo](https://github.com/newren/git-filter-repo)** - Official
  replacement for `git filter-branch`. Safe secret and large-file purging.

  ```bash
  git filter-repo --path secrets.env --invert-paths
  git filter-repo --strip-blobs-bigger-than 10M
  ```

- **[BFG Repo-Cleaner](https://github.com/rtyley/bfg-repo-cleaner)** - Faster
  alternative for stripping passwords or large binaries.

  ```bash
  bfg --delete-files passwords.txt repo.git
  ```

## Pre-push guard

- **[git_guardrails](https://git-guardrails.readthedocs.io/en/latest/)** --
  Pre-push hook CLI. Detects connectivity loss, unpulled upstream commits,
  excessive local commit count.

  ```bash
  git_guardrails validate --auto-fetch
  ```

## Repository inspection

- **[git-sizer](https://github.com/github/git-sizer)** - Size metrics. Flags
  bloat, large objects, history pollution.

  ```bash
  git-sizer --verbose
  ```

## Built-in Git safety

The following Git settings are local safety guidance; verify the effective scope
and repository policy before changing them:

```bash
git config --global push.useForceIfIncludes true   # force only if tracking matches
git config --global push.default current            # push only current branch
git config --global safe.directory /path/to/repo    # CVE-2022-24765 mitigation
```

## Sources

- [Git Toolkit source map](sources.md) — local Git and hosted-boundary references.
- Tool documentation links in this guide are third-party or project-maintained; verify release, network, and credential behavior before running them.
