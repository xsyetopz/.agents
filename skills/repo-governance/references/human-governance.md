# Human governance

Scope: local-policy human-governance guidance. Verify contacts, owners,
provider behavior, and hosted settings before publication or mutation.

## Purpose

Use recognized community-health files for people. Do not put human conduct, review authority, or contribution ownership in `AGENTS.md`.

## Standard files

- `CONTRIBUTING.md`: contribution scope, setup, tests, review, rights, and tool-assistance disclosure.
- `CODE_OF_CONDUCT.md`: human community behavior and enforcement. Use a named published code, such as Contributor Covenant 3.0, only with the required reporting and enforcement contacts and license attribution.
- `SECURITY.md`: supported versions and a private vulnerability-reporting route.
- `SUPPORT.md`: help and usage routes that do not belong in bug reports.
- `GOVERNANCE.md`: maintainer roles, decisions, and escalation when the project needs them.
- `.github/pull_request_template.md`: normal PR information and checklist.
- `.github/ISSUE_TEMPLATE/*.yml`: issue-type forms. Do not create actor-specific forms.
- `.github/CODEOWNERS`: path-based review ownership using verified users or teams.

GitHub recognizes these files in specific locations. Prefer the repository root for official human documents and `.github/` for provider templates and CODEOWNERS.

## Tool assistance

Keep the policy tool-neutral rather than anti-AI. Judge the change by relevance,
technical quality, rights, security, tests, and human review. AI assistance may
be used when the contributor understands, reviews, tests, and can defend the
complete change; require contributor review of changes produced with tool
assistance. Do not use
writing style or a detector as proof of tool use.

Allow maintainers to define narrower path or task rules. A learning-oriented
subtree may reject generated patches when contributor practice is the purpose;
the narrowest applicable rule wins. Treat AI-suggested security findings as
hypotheses and require reproduction on the affected system or hardware when
applicable.

Use a normal Git trailer for meaningful assistance:

```text
Assisted-by: Tool:Model
```

Git defines the trailer structure, but `Assisted-by` is a repository convention rather than a universal Git key. Linux and LLVM use this convention. Apache projects may use `Generated-by`. Select one documented convention and use it consistently.

Do not use `Co-authored-by` for a model. GitHub treats that trailer as account attribution. Do not let an agent add `Signed-off-by`; the human may sign only when the repository has adopted the unchanged DCO and the human can certify it.

## Hosted controls

Local files do not configure branch protection. With separate authorization, use repository rulesets or protected branches to require pull requests, reviews, code-owner review, status checks, resolved conversations, and protection from force pushes or deletion. Use read-only Actions permissions by default. Give apps and bots only the permissions they need.

Do not guess owners, contacts, labels, bypass actors, or enforcement settings. Preview every hosted change.

## Sources

- [GitHub community-health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
  supports the file-location guidance.
- [Git trailer documentation](https://git-scm.com/docs/git-interpret-trailers.html)
  supports the trailer syntax example.
- [Developer Certificate of Origin 1.1](https://developercertificate.org/),
  [Linux coding-assistant guidance](https://kernel.org/doc/html/next/process/coding-assistants.html),
  and [LLVM's AI tool policy](https://llvm.org/docs/AIToolPolicy.html) are
  cited precedents, not copied policy.
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
  supports the hosted-controls distinction.
