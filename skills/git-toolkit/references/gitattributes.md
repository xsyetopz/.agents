# Git Attributes

`.gitattributes` controls how Git handles files: line endings, diff display,
merge behavior, and archive exports. Source: `gitattributes(5)` man page.

## Line endings

The single most common `.gitattributes` use case. Prevents the dreaded "entire
file shows as changed" diff when Windows and Unix developers collaborate.

```gitattributes
# Auto-detect text files and normalize line endings to LF in the repo
* text=auto

# Explicit binary files - no EOL conversion, no diff text output
*.png binary
*.jpg binary
*.pdf binary
*.zip binary

# Shell scripts must use LF even on Windows
*.sh text eol=lf

# Windows batch files must use CRLF
*.bat text eol=crlf
```

Rules:

- `text=auto` - Git guesses whether a file is text. If yes, normalizes to LF
on commit, converts to platform native on checkout.
- `text eol=lf` - Always LF, even on Windows checkout.
- `text eol=crlf` - Always CRLF, even on Unix checkout.
- `binary` - No EOL conversion, no diff text. For images, archives, compiled
assets.

## Diff drivers

### Generated files - hide from diff by default

```gitattributes
# Lockfiles, generated code - hide diff noise
package-lock.json -diff
pnpm-lock.yaml -diff
*.gen.go -diff
*.pb.go -diff

# Show diff for these, but collapsed by default (GitHub renders collapsed)
*.min.js linguist-generated=true
*.min.css linguist-generated=true
```

### Custom diff patterns

```gitattributes
# Use a custom diff driver for specific file types
*.po diff=po

# Define the driver in the user-level Git config (`git config --global --edit`):
# [diff "po"]
#   textconv = msgcat --no-location --no-wrap
```

### Word-diff for prose

```gitattributes
# Show word-level changes, not line-level, for documentation
*.md diff=markdown
*.txt diff=markdown

# Requires in git config:
# [diff "markdown"]
#   wordRegex = [^[:space:]]+
```

## Merge drivers

### Lockfile merge - always regenerate

```gitattributes
# Never attempt to merge lockfiles - always take ours and regenerate
package-lock.json merge=ours
pnpm-lock.yaml merge=ours

# Requires in git config:
# [merge "ours"]
#   name = Keep our version and regenerate
#   driver = true
```

### Generated code - use a custom merge tool

```gitattributes
*.gen.go merge=regen

# Requires in git config:
# [merge "regen"]
#   name = Regenerate file
#   driver = make generate && git add %
```

## Export control

```gitattributes
# Exclude from git archive (tarball/zipball)
.gitattributes export-ignore
.gitignore export-ignore
.github/ export-ignore
tests/ export-ignore
dev-docs/ export-ignore
```

## Linguist overrides (GitHub language stats)

```gitattributes
# Override GitHub's language detection
*.h linguist-language=C
*.inc linguist-language=PHP

# Mark directories as vendored (excluded from language stats)
vendor/** linguist-vendored
third_party/** linguist-vendored

# Generated code (excluded from diffs by default)
**/generated/** linguist-generated=true
```

## EOL normalization - fixing an existing repo

If a repo already has mixed line endings:

```bash
# 1. Add .gitattributes
# 2. Convert all text files:
git add --renormalize .

# 3. Verify:
git diff --cached --stat

# 4. Commit:
git commit -m "Normalize line endings with .gitattributes"
```

## Full example - modern web project

```gitattributes
# Normalize line endings
* text=auto

# Binary
*.png binary
*.jpg binary
*.gif binary
*.ico binary
*.woff2 binary
*.zip binary

# Lockfiles - hide from diff, never merge
package-lock.json -diff merge=ours
pnpm-lock.yaml -diff merge=ours
yarn.lock -diff merge=ours

# Generated
*.gen.ts linguist-generated=true
*.graphql linguist-generated=true

# Export
.github/ export-ignore
.gitattributes export-ignore
.gitignore export-ignore
```
