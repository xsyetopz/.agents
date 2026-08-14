# Bitbucket Pipelines

Scope: Bitbucket Pipelines YAML (a human-readable configuration format), step execution, caches, artifacts, services, and deployments. Pull request (PR) triggers, variables, and deployment permissions are provider settings; validate them in the target workspace before relying on these examples.

## Pipeline syntax

Minimum viable `bitbucket-pipelines.yml`:

```yaml
image: node:22

pipelines:
  default:
    - step:
        name: Build and Test
        script:
          - npm ci
          - npm test
  pull-requests:
    '**':
      - step:
          name: PR Check
          script:
            - npm ci
            - npm test
```

## Triggers

| Event | Syntax |
| --- | --- |
| Push to any branch | `pipelines.default` |
| Specific branch | `pipelines.branches: {main: [...]}` |
| Pull request | `pipelines.pull-requests: {'**': [...]}` |
| Tag push | `pipelines.tags: {'v*': [...]}` |
| Manual trigger | `pipelines.custom: {deploy: [...]}` |

## Job features

### Parallel steps

```yaml
pipelines:
  default:
    - parallel:
        - step:
            name: Lint
            script:
              - npm run lint
        - step:
            name: Type Check
            script:
              - npm run typecheck
```

### Caching

```yaml
definitions:
  caches:
    npm: node_modules

pipelines:
  default:
    - step:
        caches:
          - npm
        script:
          - npm ci
```

### Artifacts

```yaml
pipelines:
  default:
    - step:
        name: Build
        script:
          - npm run build
        artifacts:
          - dist/**
```

## Services (sidecar containers)

```yaml
pipelines:
  default:
    - step:
        name: Integration Tests
        services:
          - postgres
        script:
          - npm test
definitions:
  services:
    postgres:
      image: postgres:16
      variables:
        POSTGRES_DB: test
        POSTGRES_USER: test
        POSTGRES_PASSWORD: test
```

## Environments and deployment

```yaml
pipelines:
  branches:
    main:
      - step:
          name: Deploy
          deployment: production
          script:
            - ./deploy.sh
```

## Debugging

- View logs: Repository -> Pipelines -> click the step
- Re-run: Pipeline detail page -> Rerun
- Download logs: Pipeline step -> Download
- Pipeline variables set in Repository Settings -> Pipelines -> Variables

## Sources

- [Git CI/CD source map](sources.md) — provider URLs and checked freshness.
- [Get started with Bitbucket Pipelines](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/) — current syntax and execution model.
