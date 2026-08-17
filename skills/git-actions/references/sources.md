# Git Actions source map

This map separates provider documentation from local operating guidance. A
`Checked` date means the linked page was opened while this package was revised
on 2026-08-14; an unmarked or `UNVERIFIED` entry still needs a fresh check
before relying on a current provider claim. Local safety rules in the package
are not provider guarantees.

| Scope | Authoritative source | Status |
| --- | --- | --- |
| GitHub REST API endpoints, versions, and response contracts | [GitHub REST API documentation](https://docs.github.com/en/rest) | Checked 2026-08-14 |
| GitHub GraphQL schema and query/mutation behavior | [GitHub GraphQL API documentation](https://docs.github.com/en/graphql) | Checked 2026-08-14 |
| GitHub credentials and token choices | [GitHub authentication documentation](https://docs.github.com/en/authentication) | Checked 2026-08-14 |
| GitHub REST pagination and link headers | [Using pagination in the REST API](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api) | Checked 2026-08-14 |
| GitHub CLI (`gh`) API invocation | [GitHub CLI `gh api` manual](https://cli.github.com/manual/gh_api) | Checked 2026-08-14 |
| GitLab REST and GraphQL API entry points | [GitLab API documentation](https://docs.gitlab.com/api/) | Checked 2026-08-14 |
| GitLab REST authentication and token headers | [GitLab REST API authentication](https://docs.gitlab.com/api/rest/authentication/) | Checked 2026-08-14 |
| GitLab pagination, including keyset limits | [GitLab REST API](https://docs.gitlab.com/api/rest/) | Checked 2026-08-14 |
| GitLab CLI (`glab`) authentication and pagination | [GitLab CLI documentation](https://docs.gitlab.com/cli/) | Checked 2026-08-14 |
| Git command and reference boundary (local behavior only) | [Git reference](https://git-scm.com/docs) | Checked 2026-08-14 |
| Bitbucket hosted API boundary (not handled by this skill) | [Bitbucket Cloud REST API](https://developer.atlassian.com/cloud/bitbucket/rest/intro/) | UNVERIFIED in this pass |
| Semantic Versioning (SemVer) release-label standard | [Semantic Versioning 2.0.0](https://semver.org/) | UNVERIFIED in this pass |
| Secret-handling control baseline | [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | UNVERIFIED in this pass |

GitHub, GitLab, and their CLIs can change defaults, permissions, pagination,
rate limits, and field names. If authentication, provider access, or response
validation is unavailable, report the result as `UNVERIFIED` rather than
inferring remote state. Bitbucket and other hosted providers are outside this
skill; route pipeline work to `/skill:git-ci-cd`.
