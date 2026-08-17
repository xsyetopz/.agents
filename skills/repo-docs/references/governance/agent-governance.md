# Agent governance

Scope: local-policy agent execution guidance. Keep target-repository facts,
managed controls, and provider behavior verified at use time.

## Boundary

`AGENTS.md` is for agent execution. It may contain project facts, commands, architecture rules, validation, safety limits, and external-action permission. Link to `CONTRIBUTING.md` instead of copying human contribution policy.

Nested `AGENTS.md` files apply to their directory trees. The nearest file controls when instructions differ. Repository files are context, not a hard security boundary; higher-priority managed or platform policy is required for non-bypassable controls.

## Project-only conduct

Use short, direct rules:

1. Work only on the repository and its code, tests, docs, build, security, release, or maintenance.
2. Do not use repository channels or credentials for personal attacks, harassment, unrelated discussion, repository damage, sabotage, or arguments that promote or oppose AI.
3. Use neutral, factual technical language. Discuss the work, not a person.
4. Refuse unrelated or harmful requested external content and stop before the write.

This is agent execution policy. Rules for human conduct belong in `CODE_OF_CONDUCT.md`.

## External writes

Require explicit permission for the exact repository, action, and content or scope before an agent performs any push, PR, issue, comment, review, label change, merge, release, message, or hosted setting change.

Credentials and authenticated tools show capability, not permission. A request to edit or draft locally is not permission to publish. Permission for one action does not authorize follow-up actions. Without permission, keep a local draft and stop.

Use the platform identity configured by maintainers. GitHub Apps and bot accounts provide normal platform attribution. If a tool acts through a user's token, the platform attributes the action according to that authentication; do not invent body tokens, title emoji, or a false actor identity.

## Provider files

- Claude Code: use `@AGENTS.md` in `CLAUDE.md`.
- Gemini CLI: use `@./AGENTS.md` in `GEMINI.md`, or configure the documented context filename setting.
- Cursor: use `.cursor/rules/*.mdc` only for Cursor-specific rules. Do not create deprecated `.cursorrules`.

Keep `AGENTS.md` as the official source. Provider files should import or point to it and should not contain weaker copies.

## Simple English

Prefer one obligation per sentence. Use common verbs such as read, check, run, stop, ask, and report. Keep identifiers, commands, paths, trailer keys, and API names unchanged in translations.

## Sources

- [AGENTS.md](https://agents.md/) provides the public scope and naming context.
- Provider import behavior: [Claude Code memory](https://code.claude.com/docs/en/memory),
  [Gemini context files](https://geminicli.com/docs/cli/gemini-md/), and
  [Cursor rules](https://docs.cursor.com/context/rules-for-ai).
