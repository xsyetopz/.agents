# Cross-Platform CI Patterns

Patterns that work across GitHub Actions, GitLab CI, and Bitbucket Pipelines.

## Caching dependencies

Every platform uses the lockfile hash as cache key:

```text
GitHub:  ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
GitLab:  key: files: [package-lock.json]
BB:      caches: npm -> node_modules (automatic keying)
```

Principle: cache path = `node_modules/` (or language equivalent), key = hash of
dependency manifest.

## Matrix builds

| Feature | GitHub Actions | GitLab CI | Bitbucket |
| --- | --- | --- | --- |
| Syntax | `strategy.matrix` | `parallel:matrix` | `parallel:` block |
| Fail-fast | `fail-fast: false` | No native - all run | All run |
| Max jobs | 256 | 200 | 100 |

## Artifact sharing

| Platform | Upload | Download |
| --- | --- | --- |
| GitHub | `actions/upload-artifact@v4` | `actions/download-artifact@v4` |
| GitLab | `artifacts:` in job | Automatic - depends on `needs` |
| Bitbucket | `artifacts:` in step | Automatic in subsequent steps |

## Secrets handling

- Never log or echo secrets
- GitHub: masked automatically (but not in debug mode)
- GitLab: masked automatically (except values < 4 chars)
- Bitbucket: masked automatically in output

```bash
# Safe pattern: redirect secret to a file, never to stdout
echo "$SECRET" > /tmp/secret-file
# Never: echo "Using token: $TOKEN"
```

## Conditional jobs

```text
GitHub:  if: github.ref == 'refs/heads/main'
GitLab:  rules: [{if: '$CI_COMMIT_BRANCH == "main"'}]
BB:      Only via branch-specific pipeline sections
```

## Pre-commit CI

Run fast checks first, expensive ones later:

1. Lint (fast, no deps)
2. Type check (medium, needs install)
3. Unit tests (medium, needs install)
4. Integration tests (slow, needs services)
5. Build artifacts (slow)
6. Deploy (conditional on branch)

Structure this as sequential stages with `needs`/`dependencies`.

## Composite actions / templates / includes

- GitHub: composite actions (`action.yml` with `runs.using: composite`)
- GitHub: reusable workflows (`.github/workflows/*.yml` with `on:
  workflow_call`)
- GitLab: `include:` with `local`, `project`, or `template`
- Bitbucket: YAML anchors and `definitions:` (no cross-repo includes)
