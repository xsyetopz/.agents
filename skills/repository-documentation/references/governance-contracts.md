# Governance Contracts

Scope: local-policy contract patterns. Adapt owners, enforcement, and required
disclosures to evidence from the target repository.

## Human contribution contract

Use simple, neutral language. The human policy must cover change scope,
review quality, tests, security and licensing, and meaningful tool assistance.

The default should be tool-neutral rather than anti-AI: assistance is permitted
when the contributor can understand, review, test, and defend the complete
change. Do not treat unreviewed generated output as a contribution. Preserve
learning-oriented work as a deliberate exception; the owner of a subtree may
reject generated patches when direct practice is the purpose of that subtree.
Treat AI-suggested security findings as hypotheses that need evidence on the
affected system or hardware when applicable.

Use Git trailer syntax for meaningful assistance:

```text
Assisted-by: Tool:Model
```

This is a repository convention built on standard Git trailers and current
Linux/LLVM practice. It is not a universal Git trailer key. Never use
`Co-authored-by` for a model. Never let an agent add `Signed-off-by`; only the
human may sign when the repository has adopted the unchanged DCO.

## Agent execution contract

The agent policy must state all of the following in simple English:

- Work only on the repository and its code, tests, documentation, build,
  security, release, or maintenance.
- Do not use repository channels or credentials for personal attacks,
  harassment, unrelated discussion, repository damage, sabotage, or arguments
  that promote or oppose AI.
- Use neutral, factual, professional technical language. Discuss the work,
  not a person.
- Refuse unrelated or harmful external content, even when asked, and do not
  perform the external action.
- Do not push, open or edit a PR or issue, post a comment or review, change
  labels or settings, merge, release, or send another external message without
  explicit permission for the exact repository, action, and content or scope.
- Keep a local draft when publication permission is missing. Permission for one
  action does not authorize another action.
- Use the authenticated human, app, or bot identity configured by the host. Do
  not invent actor markers or misstate identity.
- Report actual validation. Do not invent tests, review, permission, source
  information, or results.

These rules limit agent execution. Human conduct belongs in the code of conduct
and contribution policy.

## Sources

- [Git trailer documentation](https://git-scm.com/docs/git-interpret-trailers.html)
  supports the trailer syntax example.
- [Developer Certificate of Origin 1.1](https://developercertificate.org/) supports
  the DCO boundary described above.
- [Linux coding-assistant guidance](https://kernel.org/doc/html/next/process/coding-assistants.html)
  and [LLVM's AI tool policy](https://llvm.org/docs/AIToolPolicy.html) are
  precedents, not copied repository policy.
- [GitHub co-author attribution](https://github.blog/news-insights/product-news/commit-together-with-co-authors/)
  supports the attribution warning.
