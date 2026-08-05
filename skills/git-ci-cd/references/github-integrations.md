# GitHub Integrations

## Use this reference

Load this reference when github integrations is part of the pipeline task. Apply it to the actual event trust boundary, job permissions, dependencies, runner, artifacts, and observed pipeline result without suppressing failures.

Automated dependency updates, security scanning, and repository maintenance
bots. These live in the `.github/` directory and complement CI/CD pipelines.

## Dependabot

Source: [GitHub Dependabot docs](https://docs.github.com/en/code-
security/dependabot/dependabot-version-updates/configuring-dependabot-version-
updates)

### Minimum configuration (`.github/dependabot.yml`)

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Complete configuration

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
      time: "09:00"
      timezone: "UTC"
    open-pull-requests-limit: 10
    versioning-strategy: increase
    labels:
      - "dependencies"
      - "npm"
    assignees:
      - "team-maintainers"
    reviewers:
      - "team-maintainers"
    commit-message:
      prefix: "chore(deps)"
      prefix-development: "chore(dev-deps)"
      include: "scope"
    ignore:
      - dependency-name: "chalk"
        versions: ["5.x"]  # Block major version bump
      - dependency-name: "*"
        update-types: ["version-update:semver-patch"]  # Skip patch updates

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Key settings

| Setting | Purpose |
| --- | --- |
| `open-pull-requests-limit` | Cap concurrent PRs (default 5). Raise for active repos, lower for quiet ones |
| `versioning-strategy: increase` | For npm: bump the manifest range, not just the lockfile |
| `ignore` | Block specific packages or version ranges. Use for known-breaking upgrades |
| `commit-message.prefix` | Conventional commits prefix for auto-generated PRs |
| `labels` | Auto-label for filtering and triage |

### Private registries

```yaml
registries:
  npm-github:
    type: npm-registry
    url: https://npm.pkg.github.com
    token: ${{ secrets.DEPENDABOT_NPM_TOKEN }}

updates:
  - package-ecosystem: "npm"
    directory: "/"
    registries:
      - npm-github
    schedule:
      interval: "weekly"
```

### Supported ecosystems

npm, pip, cargo, bundler, composer, mix, maven, gradle, nuget, docker, github-
actions, gomod, terraform, swift, pub, devcontainers, dotnet-sdk.

## CodeQL

Source: [GitHub CodeQL docs](https://docs.github.com/en/code-security/code-
scanning/introduction-to-code-scanning/about-code-scanning-with-codeql)

### Default setup (recommended)

Enable in repo settings: Settings -> Code security -> Code scanning -> CodeQL
analysis -> Default setup. GitHub automatically selects languages and query
suites. No config file needed.

### Advanced setup (`.github/workflows/codeql.yml`)

```yaml
name: "CodeQL"

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '30 1 * * 0'  # Weekly on Sunday

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read

    strategy:
      matrix:
        language: [javascript-typescript, python]

    steps:
      - uses: actions/checkout@<sha>
      - uses: github/codeql-action/init@<sha>
        with:
          languages: ${{ matrix.language }}
      - uses: github/codeql-action/analyze@<sha>
```

### Supported languages

C/C++, C#, Go, Java/Kotlin, JavaScript/TypeScript, Python, Ruby, Rust, Swift,
GitHub Actions workflows.

Note: PHP, Scala are **not** supported.

## Renovate

Source: [Renovate docs](https://docs.renovatebot.com/). Alternative to
Dependabot with more configuration options, monorepo support, and cross-platform
compatibility (GitHub, GitLab, Bitbucket, Azure DevOps).

### Minimum configuration (`renovate.json`)

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"]
}
```

### Opinionated configuration

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    ":separateMajorMinor",
    ":combinePatchMinorUpdates",
    "schedule:weekly"
  ],
  "labels": ["dependencies"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true,
      "automergeType": "pr",
      "platformAutomerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "labels": ["dependencies", "breaking"],
      "assignees": ["team-maintainers"]
    }
  ]
}
```

### Dependabot vs Renovate

| Feature | Dependabot | Renovate |
| --- | --- | --- |
| Setup | GitHub-native, zero config | Config file, more options |
| Monorepo | Basic directory config | First-class monorepo support |
| Auto-merge | No native automerge | Configurable automerge rules |
| Cross-platform | GitHub only | GitHub, GitLab, Bitbucket, Azure DevOps |
| Custom managers | Limited | Extensive (regex managers, custom datasources) |
| Dashboard | GitHub dependency graph + alerts | Dedicated dashboard issue |

Start with Dependabot. Switch to Renovate when you need automerge, monorepo
grouping, or non-GitHub platform support.

## Other integrations

### Stale bot (`.github/workflows/stale.yml`)

```yaml
name: Close stale issues and PRs
on:
  schedule:
    - cron: '30 1 * * *'

jobs:
  stale:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
    steps:
      - uses: actions/stale@<sha>
        with:
          days-before-stale: 60
          days-before-close: 7
          stale-issue-message: 'This issue is stale because it has been open 60 days with no activity.'
          stale-pr-message: 'This PR is stale.'
          exempt-issue-labels: 'pinned,security'
```

### Auto-labeler

Uses `.github/labeler.yml` to auto-label PRs based on changed files:

```yaml
# .github/labeler.yml
docs:
  - changed-files:
    - any-glob-to-any-file: 'docs/**'

tests:
  - changed-files:
    - any-glob-to-any-file: '**/*.test.*'

ci:
  - changed-files:
    - any-glob-to-any-file: '.github/workflows/**'
```
