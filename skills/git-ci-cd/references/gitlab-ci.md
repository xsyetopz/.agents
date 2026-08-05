# GitLab CI

## Use this reference

Load this reference when gitlab ci is part of the pipeline task. Apply it to the actual event trust boundary, job permissions, dependencies, runner, artifacts, and observed pipeline result without suppressing failures.

## Pipeline syntax

Minimum viable `.gitlab-ci.yml`:

```yaml
stages:
  - build
  - test

variables:
  NODE_VERSION: "22"

build:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

test:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm test
```

## Triggers

| Event | Syntax |
| --- | --- |
| Push to branch | `rules: [{if: '$CI_PIPELINE_SOURCE == "push"'}]` |
| Merge request | `rules: [{if: '$CI_PIPELINE_SOURCE == "merge_request_event"'}]` |
| Tag push | `rules: [{if: '$CI_COMMIT_TAG'}]` |
| Scheduled | `rules: [{if: '$CI_PIPELINE_SOURCE == "schedule"'}]` |
| Manual (Web UI) | `rules: [{when: manual}]` |

## Job features

### Parallel matrix

```yaml
test:
  stage: test
  image: node:${NODE_VERSION}
  parallel:
    matrix:
      - NODE_VERSION: ["20", "22"]
        PLATFORM: [linux, macos]
  script:
    - echo "Testing on $PLATFORM with Node $NODE_VERSION"
```

### Caching

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/

# Per-job cache with a computed key
build:
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - node_modules/
```

### Artifacts

```yaml
build:
  artifacts:
    name: "build-${CI_COMMIT_REF_SLUG}"
    paths:
      - dist/
    expire_in: 1 week
```

### Job dependencies

```yaml
stages:
  - lint
  - test
  - deploy

lint:
  stage: lint

test:
  stage: test
  needs: [lint]  # runs after lint

deploy:
  stage: deploy
  needs: [test]
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

## Environments and secrets

```yaml
deploy:
  stage: deploy
  environment:
    name: production
  script:
    - deploy.sh
  variables:
    TOKEN: $DEPLOY_TOKEN  # CI/CD variable, masked in logs
```

## Templates with `include`

```yaml
# Include from the same project
include:
  - local: .gitlab/ci/templates.yml

# Include from another project
include:
  - project: group/shared-ci
    file: /templates/build.yml
    ref: main

# Include official template
include:
  - template: Security/SAST.gitlab-ci.yml
```

## Debugging

- View job logs in the GitLab UI: Build -> Pipelines -> job -> raw log
- Use `gitlab-ci-local` for local testing: `npm install -g gitlab-ci-local &&
  gitlab-ci-local`
- Enable debug: set CI/CD variable `CI_DEBUG_TRACE` to `true`
- Masked variables: GitLab automatically masks values in logs - don't rely on
it for short secrets (under 4 chars aren't masked)
