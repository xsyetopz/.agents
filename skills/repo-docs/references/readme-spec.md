# README.md Specification

A README.md is the project's landing page. It serves two audiences: search
engines (discovery) and developers (evaluation). Good structure serves both.

## Required sections

In order. Every README must have all five.

### 1. Title and badges

```markdown
# Project Name

[![CI](https://github.com/owner/repo/actions/workflows/ci.yml/badge.svg)](...)
[![Version](https://img.shields.io/...)](#)
[![License](https://img.shields.io/...)](#)
```

Badges go directly under the title. Keep it to 2-4 relevant ones. Badge alt text
must be descriptive - not just "CI" but "CI status" or "Build passing".

### 2. Description paragraph

A single paragraph, 2-4 sentences, that answers "what is this and why does it
exist." This paragraph is the search snippet - it must contain the primary
keyword and be self-contained.

```markdown
**Project Name** is a <category> that <solves problem> for <audience>.
It <key differentiator> compared to <alternatives>.
```

Anti-patterns:

- "A blazingly fast..." - meaningless without a baseline
- "A modern..." - modern relative to what?
- Feature lists before the description - tell me what it IS first

### 3. Installation

Minimum viable install. One code block. No build-from-source unless that's the
only option.

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

If there are prerequisites, list them above the install command.

### 4. Usage

A single, working example. Not a reference - just enough to prove the tool does
what the description says.

````markdown
## Usage

```bash
project-name --input file.txt --output result.json
```
````

### 5. Contributing and License

Links, not inline text. These sections are one line each.

```markdown
## Contributing

See `CONTRIBUTING.md`.

## License

[MIT](LICENSE)
```

## SEO rules

### Title

The H1 (`# Project Name`) is the `<title>` tag equivalent. It must be the
project name, not a tagline. GitHub appends `org/project` automatically.

### Description paragraph

The first paragraph after the H1 is the meta description. It must:

- Be 120-160 characters (visible in search results)
- Include the primary keyword naturally
- Not repeat the project name (redundant with the title)

### Keywords

Keywords appear in:

1. The H1 title
2. The description paragraph
3. Section headings (`## Install`, `## Usage`)
4. Badge alt text

Search engines weight these positions highest. Do not stuff keywords.

### Link structure

- Internal links are relative: use `CONTRIBUTING.md` as the target path
- External links to the project's own ecosystem (docs site, package registry,
community) are absolute
- Cross-reference links to alternatives are at the end, under `## Alternatives`
or `## See also`

## Optional sections

Add only when the project genuinely needs them:

| Section | When to add |
| --- | --- |
| `## Features` | The description doesn't cover the scope |
| `## Demo` | A screenshot or GIF clarifies the UI |
| `## Documentation` | Docs live outside the README |
| `## Alternatives` | Honest comparison helps users choose |
| `## FAQ` | The same questions come up repeatedly |
| `## Acknowledgments` | Required by dependencies or funding |

## Anti-patterns - reject on sight

1. **Wall of badges**: more than 5 badges buries the content
2. **Table of contents before the description**: search engines index the ToC,
not the project
3. **"Quick Start" that requires 10 steps**: quick means 2-3 commands
4. **Install instructions for every platform**: pick the primary one; link to
docs for others
5. **Feature list instead of description**: features answer "what can it do?",
not "what IS it?"
6. **No license**: unlicensed means proprietary; developers will move on
7. **Stale CI badge**: a broken badge is worse than no badge

## Multilingual READMEs

When a project serves an audience that primarily reads a language other than
English, provide translated READMEs with language-tagged filenames.

### File naming

Use the `README` stem with a language suffix. The suffix follows [BCP
47](https://tools.ietf.org/html/bcp47) language tags, using the shortest
practical form:

| File | Language |
| --- | --- |
| `README.md` | Primary (typically English) - the canonical version |
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

Prefer `README.zh.md` over `README.zh-CN.md` unless the distinction matters. Use
`README_cn.md` or `README-zh.md` only if the project already has that convention
-- the dot-separated BCP 47 form is the recommended default.

### Language switcher

The primary README must list available translations at the top, after the
description paragraph:

```markdown
**MyProject** is a tool that does X.

[English](README.md) | [中文](README.zh.md) | [日本語](README.ja.md)
```

GitHub recognizes this pattern and renders it as a language picker in the
repository header for recognized languages.

### Content parity

Translated READMEs must keep the same structure (same headings, same order) as
the primary README. Content can diverge - examples may use locale-appropriate
paths, and descriptions may emphasize features relevant to that audience.

### Primary language

The primary README is the source of truth. If there's a conflict between a
translation and the primary README, the primary README wins. Translations should
note their freshness relative to the primary:

```markdown
# MyProject

> This translation may be out of date. See the [English README](README.md)
> for the latest version.
```

### When NOT to add translations

- The project is small and the maintainer doesn't speak the target language --
machine-translated READMEs are worse than no translation
- The primary README changes frequently - stale translations mislead users
- No one has volunteered to maintain the translation - abandon it rather than
let it rot
