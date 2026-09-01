# AGENTS.md format and evidence guide

Read this reference before creating or materially revising an `AGENTS.md` file.

## Portable format

- The portable filename is `AGENTS.md` and the content is ordinary Markdown.
- The format defines no mandatory frontmatter, headings, or field schema.
- A root file should contain repository-wide guidance. Nested files should contain only guidance for their directory subtree; when instructions conflict, the closest applicable file takes precedence.
- The user's explicit request and higher-priority platform instructions still outrank repository guidance.

Do not confuse the portable format with GitHub custom-agent persona files. GitHub's `.github/agents/*.agent.md` format uses frontmatter and persona-specific configuration; copy none of that syntax into a portable `AGENTS.md` unless a separate tool contract explicitly requires it.

## Codex-specific discovery

For Codex, distinguish portable guidance from Codex configuration:

- Codex reads global guidance from `CODEX_HOME`, preferring `AGENTS.override.md` over `AGENTS.md` at that level.
- In a project, Codex walks from the project root to the current working directory and includes at most one applicable instruction file per directory. It checks `AGENTS.override.md` before `AGENTS.md`, then configured fallback names.
- Deeper files appear later in the instruction chain and override conflicting parent guidance.
- Codex has a configurable combined-byte limit, so splitting by meaningful subtree scope can preserve relevant guidance.

These are Codex implementation details, not requirements of the portable AGENTS.md format. Verify current documentation before relying on them for another product or a changed Codex configuration.

## Evidence-first content

Derive instructions from current repository evidence instead of a generic template:

| Guidance | Preferred evidence |
| --- | --- |
| Setup and package manager | lockfiles, manifests, tool-version files, bootstrap scripts |
| Fast validation commands | package scripts, task runners, test configuration, CI jobs |
| Project map and ownership | manifests, workspace configuration, CODEOWNERS, module boundaries |
| Code conventions | formatter/linter config and representative maintained files |
| Test expectations | nearby tests, test configuration, CI gates |
| Generated or vendor boundaries | generator headers, build scripts, ignore files, repository docs |
| External-action permissions | explicit user or organization policy, never inferred from available credentials |

Prefer exact, file-scoped commands that provide quick feedback. Include full-suite commands only with their prerequisites and expected use. A command copied from stale prose is not verified until it matches current scripts or succeeds in an appropriate environment.

## High-value sections

Use only sections supported by the repository. Common high-value content includes:

1. Exact setup and navigation commands.
2. Fast lint, type-check, unit-test, and focused-test commands.
3. A compact project map with canonical files to imitate and legacy files to avoid.
4. Local code, testing, architecture, and generated-file constraints.
5. Security, destructive-action, dependency, publication, and hosted-write boundaries.
6. The acceptance checks and evidence expected in the final report.

Avoid slogans such as "write clean code," exhaustive documentation copies, speculative architecture, unsupported coverage targets, and rules that merely restate platform policy.

## Retrieval and context size

Vercel's Next.js evaluation found that a compact documentation index embedded in `AGENTS.md` outperformed optional skill retrieval for its tested version-specific API tasks. Treat that as evidence for one useful pattern, not a universal benchmark: when agents repeatedly need broad version-matched knowledge, keep the source material in repository-local files and put a compact, searchable index plus a retrieval instruction in `AGENTS.md`. Do not paste an entire manual into persistent context.

## Sources

- [AGENTS.md open format and examples](https://agents.md/)
- [OpenAI: Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Vercel: AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- [GitHub: Lessons from over 2,500 repositories](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [agentsmd.io best practices](https://agentsmd.io/agents-md-best-practices)
- [Community AGENTS.md best-practices gist](https://gist.github.com/0xfauzi/7c8f65572930a21efa62623557d83f6e)

Use the first two sources as authority for the portable format and Codex behavior. Treat the remaining sources as empirical or community guidance and verify their recommendations against the target repository and agent.
