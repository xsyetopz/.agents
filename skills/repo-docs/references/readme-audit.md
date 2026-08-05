# README.md Audit Checklist

## Use this reference

Load this reference when readme audit is part of the repository documentation task. Verify every command, link, version, and product claim against current repository source truth.

## Quick pass (2 minutes)

- [ ] H1 is the project name, not a tagline
- [ ] First paragraph is 120-160 characters and self-contained
- [ ] Install section exists and is one code block
- [ ] Usage section exists with a working example
- [ ] License section links to LICENSE file
- [ ] Contributing section links to CONTRIBUTING.md
- [ ] No more than 5 badges
- [ ] No table of contents before the description paragraph
- [ ] No broken links

## SEO audit

- [ ] Primary keyword appears in: H1, description paragraph, at least one `##`
  heading
- [ ] Description paragraph doesn't repeat the project name redundantly
- [ ] Badge alt text is descriptive (`Build status`, not `CI`)
- [ ] External links to docs/registry are absolute URLs
- [ ] Internal links are relative paths

## Common failures and fixes

### "What is it?" buried below the fold

Bad:

```markdown
# MyProject

## Table of Contents
1. [Install](#install)
2. [Usage](#usage)
...

## About
MyProject is a tool for...
```

Good:

```markdown
# MyProject

**MyProject** is a command-line tool that converts CSV files to JSON with
streaming support for files up to 10 GB. It's an alternative to `csvjson`
that doesn't require loading the entire file into memory.

## Install
...
```

### Missing install section

"If you have Go 1.22+, run `go install`" is spam. Add an actual `## Install`
section. Link to a full install guide if the project has one.

### Usage section is just a flag dump

Bad:

````markdown
## Usage
```

Usage: project [flags] -i, --input string    Input file -o, --output string
Output file -v, --verbose         Verbose output

```
````

Good:

````markdown
## Usage

Convert a CSV to JSON:
```bash
project --input data.csv --output data.json
```

For large files, add `--stream`:

```bash
project --input large.csv --output large.json --stream
```

See `project --help` for all options.
````

### Stale or broken badges

A badge that shows `build: failing` or returns 404 is worse than no badge. If CI
isn't set up, don't add the badge. If the badge breaks, remove it - don't leave
a red X on the project's landing page.

## Edge cases

### Monorepo READMEs

Each package in a monorepo needs its own README with:

- Package name as H1
- One-paragraph description scoped to that package
- Install scoped to that package (`npm install @scope/package`)
- Link to the root README for project-level context

### README in a non-English project

The primary README should still be in English for search discoverability. Add
translated READMEs as `README.zh-CN.md`, `README.ja.md`, etc., with a language
switcher at the top of the English README.

### Multilingual audit checks

- [ ] Translated READMEs use BCP 47 suffixes: `README.zh.md`, not
  `README_chinese.md`
- [ ] Primary README has a language switcher at the top
- [ ] All translations maintain the same heading structure as the primary
- [ ] Outdated translations have a staleness warning linking to the primary
- [ ] No machine translations without a human maintainer
