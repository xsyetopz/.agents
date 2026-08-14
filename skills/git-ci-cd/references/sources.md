# Git CI/CD source map

This map records current provider references for pipeline syntax and trust
boundaries. A `Checked` date means the page was opened while this package was
revised on 2026-08-14; an unmarked or `UNVERIFIED` entry must be checked before
relying on a current provider claim. Local recommendations remain guidance,
not proof that a hosted pipeline is configured or safe.

| Scope | Authoritative source | Status |
| --- | --- | --- |
| GitHub Actions concepts, runners, and workflow execution | [GitHub Actions documentation](https://docs.github.com/en/actions) | Checked 2026-08-14 |
| GitHub Actions YAML syntax, events, permissions, and concurrency | [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | Checked 2026-08-14 |
| GitHub Actions secrets, forks, and untrusted code | [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) | Checked 2026-08-14 |
| GitHub dependency and supply-chain integrations | [GitHub supply-chain security](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain) | Checked 2026-08-14 |
| GitHub code scanning and CodeQL | [GitHub code scanning](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning) | Checked 2026-08-14 |
| GitLab CI/CD syntax and runners | [Get started with GitLab CI/CD](https://docs.gitlab.com/ci/) | Checked 2026-08-14 |
| GitLab pipeline architecture, rules, and includes | [GitLab pipeline architecture](https://docs.gitlab.com/ci/pipelines/pipeline_architectures/) | Checked 2026-08-14 |
| Bitbucket Pipelines syntax, steps, artifacts, and deployments | [Get started with Bitbucket Pipelines](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/) | Checked 2026-08-14 |
| GitHub Mermaid rendering and fenced diagram syntax | [Creating Mermaid diagrams on GitHub](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams#creating-mermaid-diagrams) | Checked 2026-08-14; canonical `/en/` page for the supplied URL |
| Git reference for local reproduction and command semantics | [Git reference](https://git-scm.com/docs) | Checked 2026-08-14 |
| Bitbucket variable and secret behavior | [Bitbucket variables and secrets](https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/) | UNVERIFIED in this pass |

Provider limits, runner images, action versions, cache semantics, and secret
masking can change. Validate syntax with the provider's current linter or run,
inspect permissions and logs, and mark hosted execution, isolation, or deploy
behavior `UNVERIFIED` when it was not observed. Local application failures are
not CI evidence; route them to the owning application skill.
