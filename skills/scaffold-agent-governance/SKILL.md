---
name: scaffold-agent-governance
description: Audit, create, or update standard repository governance for people and coding agents. Use when adding CONTRIBUTING.md, AGENTS.md, provider imports, a pull request template, CODEOWNERS, multilingual governance, tool-assistance disclosure with Git trailers, or strict project-only and external-write rules for agents.
---

# Scaffold Agent Governance

Keep human contribution policy separate from agent execution rules.

- Put rules for contributors and reviewers in `CONTRIBUTING.md`.
- Put rules for coding agents in `AGENTS.md`.
- Use the normal provider files only to import or point to `AGENTS.md`.
- Put hosted enforcement in repository rulesets, branch protection, app permissions, and `CODEOWNERS`.

Repository instructions guide cooperating agents. They cannot override a platform, organization, managed policy, or higher-priority instruction. Do not claim that Markdown can enforce intent or consent.

## Inspect before changing

1. Confirm the repository root, host, main README, contribution process, languages, and existing governance files.
2. Read nested `AGENTS.md` files before editing their directory trees.
3. Treat preview and audit as read-only. Obtain explicit permission before changing governance or hosted settings.
4. Preserve foreign files. Do not replace an existing standard file unless the user approved the exact replacement.
5. Do not create a code of conduct, security contact, support route, DCO requirement, labels, or ruleset from guessed values.

Read [human-governance.md](references/human-governance.md), [agent-governance.md](references/agent-governance.md), and [standards.md](references/standards.md) before changing policy text.

## Use standard files

The default local scaffold creates or updates:

- `CONTRIBUTING.md` for people;
- `AGENTS.md` for coding agents;
- `.github/pull_request_template.md` for normal pull requests;
- `CLAUDE.md` with the documented `@AGENTS.md` import;
- `GEMINI.md` with the documented `@./AGENTS.md` import;
- `.cursor/rules/agents.mdc` using the current Cursor rule format;
- a short README section linking the human and agent files;
- optional `.github/CODEOWNERS` entries when real owners are supplied;
- reviewed translations under `docs/i18n/<locale>/`.

Do not generate private actor/origin tokens, emoji title prefixes, custom AI policy YAML, agent-only issue templates, or a workflow that tries to infer authorship. Do not generate deprecated `.cursorrules`. Do not treat `llms.txt` as governance, and do not generate the non-standard `llms-full.txt`.

Use `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`, `GOVERNANCE.md`, issue forms, DCO, or hosted rules only when the repository has the required policy decision and real contact or owner data. Follow their official formats and licenses.

## Preview and apply

For each non-English locale, prepare two reviewed files: a human contribution translation and an agent-rule translation. Use BCP 47 locale tags.

Preview:

```sh
python3 scripts/governance.py \
  --repo /absolute/path/to/repository \
  --project-name "Project name" \
  --description "One factual project sentence." \
  --locale et \
  --human-translation et=/absolute/path/contributing.et.md \
  --agent-translation et=/absolute/path/agents.et.md
```

Review every created file, section update, import, no-op, conflict, and legacy conflict. Then apply only with explicit permission:

```sh
python3 scripts/governance.py \
  --repo /absolute/path/to/repository \
  --project-name "Project name" \
  --description "One factual project sentence." \
  --locale et \
  --human-translation et=/absolute/path/contributing.et.md \
  --agent-translation et=/absolute/path/agents.et.md \
  --apply --confirm-authorized
```

Use `--readme <relative-path>` for a non-default README. Use repeatable `--before-heading` for translated License or Star History headings. Use repeatable `--codeowner @organization/team` only for verified owners with the required repository access.

The preview reports deletion only for old files that match the prior scaffold's full structure and signatures. Authorized apply removes them after the replacement files are ready. A same-named foreign file is left untouched. The governance audit ignores unrelated `llms.txt` files because they are not governance.

## Human contribution contract

Use simple, neutral language. The human policy must cover change scope, review quality, tests, security and licensing, and meaningful tool assistance.

Use Git trailer syntax for meaningful assistance:

```text
Assisted-by: Tool:Model
```

This is a repository convention built on standard Git trailers and current Linux/LLVM practice. It is not a universal Git trailer key. Never use `Co-authored-by` for a model. Never let an agent add `Signed-off-by`; only the human may sign when the repository has adopted the unchanged DCO.

## Agent execution contract

The agent policy must state all of the following in simple English:

- Work only on the repository and its code, tests, documentation, build, security, release, or maintenance.
- Do not use repository channels or credentials for personal attacks, harassment, unrelated discussion, repository damage, sabotage, or arguments that promote or oppose AI.
- Use neutral, factual, professional technical language. Discuss the work, not a person.
- Refuse unrelated or harmful external content, even when asked, and do not perform the external action.
- Do not push, open or edit a PR or issue, post a comment or review, change labels or settings, merge, release, or send another external message without explicit permission for the exact repository, action, and content or scope.
- Keep a local draft when publication permission is missing. Permission for one action does not authorize another action.
- Use the authenticated human, app, or bot identity configured by the host. Do not invent actor markers or misstate identity.
- Report actual validation. Do not invent tests, review, permission, source information, or results.

These rules limit agent execution. Human conduct belongs in the code of conduct and contribution policy.

## Validate

Run:

```sh
python3 scripts/governance.py \
  --repo /absolute/path/to/repository \
  --locale et \
  --validate-only
```

Validation checks the human/agent split, provider import targets, standard file paths, README ordering, translation paths, CODEOWNERS syntax when requested, and absence of legacy private protocols. It cannot check translation quality, identity, consent, or remote ruleset state.

Report changed paths, conflicts left untouched, removed legacy paths, locales, checks run, and hosted settings that remain unconfigured.
