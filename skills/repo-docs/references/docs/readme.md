# README.md

A README is a project's landing page for discovery and evaluation. Use this reference for the minimum structure, source-backed claims, and verification checks that keep the landing page usable.

Scope: local-policy README guidance. Examples and placeholder links are
illustrative; inspect the target repository before asserting support or status.

## Minimum structure

Every README includes these sections in order.

### 1. Title and badges

```markdown
# Project Name

[![CI](https://github.com/owner/repo/actions/workflows/ci.yml/badge.svg)](...)
[![Version](https://img.shields.io/...)](#)
[![License](https://img.shields.io/...)](#)
```

Place two to four relevant badges directly under the title. Badge alt text states the observed status or purpose, such as `CI status` or `Build passing`.

### 2. Description paragraph

Use one self-contained paragraph of two to four sentences answering what the project is and why it exists. Include the primary keyword without repeating the project name from the H1. A useful pattern is:

```markdown
**Project Name** is a <category> that <solves problem> for <audience>.
It <key differentiator> compared to <alternatives>.
```

Avoid unsupported superlatives, unexplained feature lists, and descriptions
that omit the project category or audience.

### 3. Installation

Provide the minimum viable install in one code block. List prerequisites above it. Do not add build-from-source steps when a supported package install exists.

````markdown
## Install

```bash
brew install project-name
```
# or
```bash
npm install project-name
```
````

### 4. Usage

Include one working example that demonstrates the behavior named in the description. Keep it an example rather than a complete command reference.

````markdown
## Usage

```bash
project-name --input file.txt --output result.json
```
````

### 5. Contributing and license

Use one-line links rather than inline policy text:

```markdown
## Contributing

See `CONTRIBUTING.md`.

## License

[MIT](LICENSE)
```

## Search and link checks

### Title and description

- The H1 is the project name, not a tagline.
- The first paragraph is self-contained and 120–160 characters when it serves as the search description.
- The primary keyword appears naturally in the H1, description, at least one `##` heading, and descriptive badge alt text.
- The project name is not repeated redundantly in the description.

### Links

- Internal links use relative paths such as `CONTRIBUTING.md`.
- Links to the project's own docs site, registry, or community use absolute URLs.
- Alternatives are grouped at the end under `## Alternatives` or `## See also`.
- Every internal link resolves; broken badges are removed or corrected.

## Optional sections

Add a section only when the project has the corresponding evidence or need:

| Section | When to add |
| --- | --- |
| `## Features` | The description does not cover the scope. |
| `## Demo` | A screenshot or GIF clarifies the UI. |
| `## Documentation` | Documentation lives outside the README. |
| `## Alternatives` | An honest comparison helps users choose. |
| `## FAQ` | The same questions recur. |
| `## Acknowledgments` | A dependency or funder requires attribution. |

## Verification checklist

- [ ] H1 is the project name.
- [ ] The first paragraph is 120–160 characters and self-contained when used as
      a search description.
- [ ] Install has one working code block and lists prerequisites.
- [ ] Usage has a working example rather than only a flag dump.
- [ ] License links to `LICENSE` and contributing links to `CONTRIBUTING.md`.
- [ ] There are no more than five badges and each has descriptive alt text.
- [ ] No table of contents appears before the description paragraph.
- [ ] Primary keywords occur in the H1, description, a section heading, and badge
      alt text without stuffing.
- [ ] External ecosystem links are absolute and internal links are relative.
- [ ] No links or badges are broken.

## Common failure checks

Treat these as observable conditions with a concrete correction:

1. More than five badges obscure the description; keep only relevant badges.
2. A table of contents before the description displaces the project summary; move it below the summary.
3. A “Quick Start” requiring more than two or three commands is not quick; link to the detailed guide.
4. Platform-specific install instructions without a primary path spread scope; document one supported path and link to the others.
5. A feature list before the description does not identify the project; write the category and audience first.
6. A missing license leaves rights unspecified; add a verified license link or state the project policy.
7. A stale or failing CI badge is evidence of an invalid status; correct or remove it.

## Examples and failure cases

### Description below the fold

A table of contents before the summary hides the answer to “what is it?”:

```markdown
# MyProject

## Table of Contents
1. [Install](#install)
2. [Usage](#usage)

## About
**MyProject** is a command-line tool that converts CSV files to JSON with
streaming support for files up to 10 GB.
```

Move the description directly below the H1 and badges.

### Missing install section

A prerequisite sentence without an install command does not document setup:

```markdown
Requires Go 1.22+.
```

Add a real `## Install` section and link a full install guide when one exists.

### Usage contains only flags

A flag dump does not demonstrate a working path:

```markdown
## Usage
Usage: project [flags] -i, --input string -o, --output string
```

Show a concrete command, an optional large-file variant, and a link to `project --help` for the complete option set.

### Stale or broken badges

A badge that returns 404 or reports an unconfigured build is invalid evidence.
When CI is absent, omit the badge; when the target changes, update or remove it.

## Multilingual READMEs

When a project serves an audience that primarily reads another language, provide translated READMEs only when a maintainer can keep them current.

### File naming

Use the `README` stem with a [BCP 47](https://www.rfc-editor.org/info/bcp47/) language suffix:

| File | Language |
| --- | --- |
| `README.md` | Primary (typically English), canonical version |
| `README.zh.md` | Chinese (simplified) |
| `README.zh-CN.md` | Chinese (simplified, explicit region) |
| `README.zh-TW.md` | Chinese (traditional) |
| `README.ja.md` | Japanese |
| `README.ko.md` | Korean |
| `README.de.md` | German |
| `README.fr.md` | French |
| `README.es.md` | Spanish |
| `README.pt.md` | Portuguese |
| `README.pt-BR.md` | Portuguese (Brazilian) |
| `README.ru.md` | Russian |
| `README.ar.md` | Arabic |

Prefer `README.zh.md` unless a regional distinction matters. Keep an existing project convention such as `README_cn.md` only when changing the name would
break established links.

### Language switcher

The primary README lists available translations after the description:

```markdown
**MyProject** is a tool that does X.

[English](README.md) | [中文](README.zh.md) | [日本語](README.ja.md)
```

### Content parity

Translations keep the same heading structure and order as the primary README. Examples may use locale-appropriate paths and descriptions may emphasize
features relevant to that audience.

### Primary language

The primary README is the source of truth. A translation that may be stale links back to the English version:

```markdown
# MyProject

> This translation may be out of date. See the [English README](README.md)
> for the latest version.
```

### Translation scope and checks

- Do not add a translation when no maintainer can review it or when it would
  become stale faster than it can be updated.
- Monorepo package READMEs use the package name as H1, package-scoped description
  and install command, and a link to the root README.
- Translated files use BCP 47 suffixes such as `README.zh.md`, not ad-hoc names.
- The primary README has a language switcher near the top.
- All translations preserve the primary heading structure.
- Stale translations include a warning linking to the primary README.
- Machine-translated files require a named human maintainer before publication.

## Sources

- [BCP 47](https://www.rfc-editor.org/info/bcp47/) supports the language-tag
  naming guidance in this reference.
