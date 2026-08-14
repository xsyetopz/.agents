# GitHub Actions

Scope: GitHub Actions workflow YAML, events, jobs, matrices, caches, artifacts, reusable workflows, and runner behavior. A workflow triggered by a pull request (PR) can receive untrusted code; resolve event trust, `permissions`, secrets, and deployment environments before running it.

## Workflow syntax

Minimum viable workflow (pin third-party actions to reviewed commit SHAs in production; the version tags below are illustrative):

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm test
```

## Triggers

| Event | Syntax |
| --- | --- |
| Push to branch | `on: push: branches: [main]` |
| PR opened/synced | `on: pull_request: branches: [main]` |
| Manual trigger | `on: workflow_dispatch: inputs: ...` |
| Scheduled | `on: schedule: [{cron: '0 9 * * 1-5'}]` |
| Tag push | `on: push: tags: ['v*']` |
| Release published | `on: release: types: [published]` |

## Job features

### Matrix strategy

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [20, 22]
      fail-fast: false  # run all combinations even if one fails
    runs-on: ${{ matrix.os }}
```

### Caching

```yaml
- uses: actions/cache@v4
  with:
    path: ${{ runner.temp }}/npm-cache
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Artifacts

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
```

### Job dependencies

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]
  test:
    needs: lint  # runs after lint succeeds
    runs-on: ubuntu-latest
    steps: [...]
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps: [...]
```

## Secrets and environments

```yaml
jobs:
  deploy:
    environment: production  # requires approval, scoped secrets
    steps:
      - run: deploy.sh
        env:
          TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

## Reusable workflows

Caller:

```yaml
jobs:
  call-reusable:
    uses: owner/repo/.github/workflows/reusable.yml@main
    with:
      node-version: '22'
    secrets: inherit
```

Callee (`.github/workflows/reusable.yml`):

```yaml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
```

## Composite actions

`action.yml`:

```yaml
name: Setup and Build
description: Install deps and build
inputs:
  node-version:
    required: true
runs:
  using: composite
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    - run: npm ci
      shell: bash
    - run: npm run build
      shell: bash
```

## Debugging

- Enable debug logging: set secret `ACTIONS_STEP_DEBUG` to `true`
- Enable runner diagnostics: set secret `ACTIONS_RUNNER_DEBUG` to `true`
- Use `act` for local testing: `act pull_request`
- Read raw logs: `gh run view <run-id> --log`
- Common failure: `set -eo pipefail` causes early exit - use
`{ command; } || true` for allowed failures

## Sources

- [Git CI/CD source map](sources.md) — checked provider URLs and freshness limits.
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) — current event, permission, and job syntax.
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) — trust, secrets, and untrusted-code controls.
