# Git Security Tooling

## Use this reference

Load this reference when tooling is part of the requested local Git state transition. Inspect current status and history first, preserve unrelated work, identify recovery, and verify the resulting state.

Production tools for git safety. Do not invent a pre-commit hook or security
check when a production tool already exists. Sources: [dev.to Git
security](https://dev.to/prankurpandeyy/git-security-best-practices-for-keeping-your-code-safe-1nep),
[git-guardrails](https://git-guardrails.readthedocs.io/en/latest/).

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

From [dev.to Git security best practices](https://dev.to/prankurpandeyy/git-security-best-practices-for-keeping-your-code-safe-1nep):

```bash
git config --global push.useForceIfIncludes true   # force only if tracking matches
git config --global push.default current            # push only current branch
git config --global safe.directory /path/to/repo    # CVE-2022-24765 mitigation
```
