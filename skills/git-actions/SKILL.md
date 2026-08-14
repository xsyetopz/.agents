---
name: git-actions
description: Remote GitHub and GitLab API work for repositories, issues, releases, checks, workflows, and artifacts.
---

# Git Actions

Use authenticated GitHub or GitLab APIs for narrowly scoped repository operations and evidence.

## Use this skill

- Read or change GitHub or GitLab repositories, releases, tags, issues, pull or merge requests, checks, workflows, artifacts, or settings.
- Automate pagination, REST or GraphQL requests, rate-limit handling, version lookup, or artifact retrieval.
- Do not use for local Git commands, CI/CD authoring or diagnosis, branching policy, or a page that answers a public read-only question without an API.
- Redirect local Git work to `$git-toolkit`, pipeline work to `$git-ci-cd`, and branching or merge policy to `$git-workflows`.

## Rules

- Treat every request as read-only until the user authorizes the exact remote mutation, target, and effect.
- Resolve host, owner, repository, resource identifier, API version, pagination, and mutation scope before calling.
- Use existing `gh`, `glab`, or credential-helper authentication. Never print, persist, broaden, or transmit tokens.
- Validate URLs, paths, identifiers, GraphQL variables, and JSON. Treat fork and pull-request content as untrusted.
- Check response schema, target identity, resource ID or URL, permissions, and rate-limit caveats.

## Steps

1. Identify platform, host, repository, resource, read/write intent, and required fields.
2. Use the reference router to load matching authentication, REST, GraphQL, or version material.
3. Confirm exact mutation authority before any write, merge, dispatch, delete, publish, or settings change.
4. Make the narrowest API call with explicit fields and pagination.
5. Validate status and response schema, then verify target and resulting effect.
6. Report resource ID or URL, permission limits, and any unverified condition.

## Resources

- Start with the package [reference router](references/index.md).
- Run the package [checker](scripts/check.py) for structural evidence.

## Verify

- Done means the request is schema-checked, permissions and pagination are understood, secrets remain protected, and the remote target and effect are verified.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Capture the request, response status, resource identifier, and authorization boundary without exposing credentials.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark credentials, remote state, authorization, or unavailable API evidence `UNVERIFIED`.
