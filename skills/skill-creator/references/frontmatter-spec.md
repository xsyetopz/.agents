# Frontmatter Specification

## Use this reference

Load this reference when frontmatter spec is part of the skill-authoring task. Keep the discovery description precise, the entry instructions lean, details progressively disclosed, and behavior independently verifiable.

Full frontmatter schema per the [Agent Skills
specification](https://agentskills.io/specification).

## name (required)

- 1-64 characters
- Lowercase alphanumeric (`a-z`, `0-9`) and hyphens (`-`)
- Must not start or end with a hyphen
- Must not contain consecutive hyphens (`--`)
- Must match the parent directory name

```yaml
name: git-ci-cd        # valid
name: my-skill         # valid
name: -invalid         # starts with hyphen
name: invalid-         # ends with hyphen
name: invalid--name    # consecutive hyphens
name: Invalid-Name     # uppercase
```

## description (required)

- 1-1024 characters
- Keep discovery descriptions to 80-240 characters in this repository; they are
  loaded every turn and should reserve context for activated skill instructions.
- Describe what the skill does and when to use it
- Include keywords that help agents identify relevant tasks
- Start with "Use when" or "Use for"
- Treat the description as the activation index: include concrete user phrases,
  command names, artifact names, formats, platforms, and common synonyms that
  uniquely belong to the skill.
- There is no standardized standalone `keywords` field. Put routing terms in
  `description`; arbitrary `metadata` keys may not be loaded by a client during
  skill discovery.
- Prefer many precise, bounded terms over broad words such as "code", "help",
  or "workflow" that would activate unrelated skills.

```yaml
description: Use when designing, debugging, or modifying CI/CD pipelines on GitHub Actions, GitLab CI, or Bitbucket Pipelines. Covers workflow syntax, job orchestration, caching, and security.
```

## license (optional)

- License name or reference to a bundled license file
- Keep it short

```yaml
license: MIT
license: Apache-2.0
license: See LICENSE file
```

## compatibility (optional)

- 1-500 characters if provided
- Only include if the skill has specific environment requirements
- Indicate intended product, required system packages, network access needs

```yaml
compatibility: requires git 2.30+, gh CLI, glab CLI
compatibility: intended for macOS and Linux, requires Docker
```

## metadata (optional)

- Arbitrary key-value mapping
- Keys and values are strings
- Use reasonably unique key names to avoid conflicts

```yaml
metadata:
  author: "Jane Smith"
  version: "2.1.0"
  min-agent-version: "1.5"
```

## allowed-tools (optional, experimental)

- Space-separated string of pre-approved tools
- Support varies between agent implementations

```yaml
allowed-tools: Bash Read Write Edit Grep Glob WebSearch
```
