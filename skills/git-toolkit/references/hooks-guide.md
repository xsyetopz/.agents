# Git Hooks Guide

Scope: local Git hooks and pre-commit validation. A hook is executable code invoked by Git; review every hook before enabling it, keep failures visible, and never install a hook from an untrusted source.

Hooks are scripts that run at specific points in the git workflow.

## Client-side hooks

| Hook | When it runs | Common use |
| --- | --- | --- |
| `pre-commit` | Before commit message editor | Lint, format, check for secrets |
| `commit-msg` | After commit message is saved | Enforce message format |
| `pre-push` | Before push to remote | Run tests, verify no WIP commits |
| `post-commit` | After commit is created | Notification, logging |
| `post-checkout` | After checkout / branch switch | Install dependencies |
| `post-merge` | After a successful merge | Run migrations |

## Server-side hooks

| Hook | When it runs | Common use |
| --- | --- | --- |
| `pre-receive` | Before accepting a push | Reject force pushes, validate commits |
| `update` | Per branch, before accepting | Branch-specific policies |
| `post-receive` | After accepting a push | CI trigger, deploy, notification |

## Hook location

- Default: `.git/hooks/` (not committed, per-clone)
- Configurable: `git config core.hooksPath /path/to/hooks`

To make hooks shared across a team, set `core.hooksPath` to a tracked directory:

```bash
git config core.hooksPath .githooks
```

## Example hooks

### pre-commit - lint staged files

```bash
#!/bin/bash
# .githooks/pre-commit
set -e

# Get list of staged files
files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.js$\|\.ts$' || true)

if [ -n "$files" ]; then
  bunx eslint $files
fi
```

### commit-msg - enforce conventional commits

```bash
#!/bin/bash
# .githooks/commit-msg
commit_regex='^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+\))?: .{1,72}$'

if ! grep -qE "$commit_regex" "$1"; then
  echo "Commit message must follow conventional commits format."
  echo "Example: feat(auth): add login form"
  exit 1
fi
```

### pre-push - run tests

```bash
#!/bin/bash
# .githooks/pre-push
set -e

echo "Running tests before push..."
npm test
```

## Make hooks executable

```bash
chmod +x .githooks/pre-commit .githooks/commit-msg .githooks/pre-push
```

## Skip hooks

```bash
git commit --no-verify -m "..."     # skip pre-commit and commit-msg
git push --no-verify                # skip pre-push
```

Use sparingly - hooks exist for a reason.

## Husky (Node.js)

If the project uses Husky, hooks are in `.husky/` and managed by Husky's install
lifecycle. Don't manually edit `core.hooksPath` in Husky projects.

```bash
# Add a hook with Husky
bunx husky add .husky/pre-commit "npm run lint-staged"
```

## pre-commit framework

The `pre-commit` Python framework manages hooks from a `.pre-commit-
config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
```

Install: `pre-commit install` Run manually: `pre-commit run --all-files`

## Sources

- [Git Toolkit source map](sources.md) — Git command and security references.
- [Git hooks documentation](https://git-scm.com/docs/githooks) — lifecycle and execution semantics.
