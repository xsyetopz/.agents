# Prompt engineering reference router

Use this router before opening a deeper reference. Select the narrowest route,
load only that route, and keep provider/model material conditional. Generic
source records and evidence rules are the default; a provider or model route
never establishes a default model, API, or behavior.

## When you need | Read

### Generic source and provenance

| When you need | Read |
| --- | --- |
| Snapshot dates, URLs, hashes, or source ownership | [official-sources.md](official-sources.md) |
| The package's model identity, evidence, and source-record fields | [models/catalog.json](models/catalog.json) |
| Prompt audit workflow, evidence separation, or reasoning-mode comparison | [model-reasoning-guide.md](model-reasoning-guide.md) |
| Reusable prompt structure and approval boundaries | [prompt-templates.md](prompt-templates.md) |
| GitHub-rendered Mermaid syntax and diagram constraints | [GitHub Mermaid documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams#creating-mermaid-diagrams) |
| A measured behavior failure category | [anti-patterns.md](anti-patterns.md), then [issue-lookup.md](issue-lookup.md) |
| One anchored issue case | [issues/index.md](issues/index.md), then [issue-corpus-index.md](issue-corpus-index.md) |

### Conditional provider and model routes

Open these only after the request names the provider/model or a representative
evaluation requires it. Verify the exact provider identifier and current source
before relying on any profile, routing, effort, availability, or pricing claim.

| When you need | Read |
| --- | --- |
| Generic OpenAI API prompting (conditional) | [official/openai-prompt-engineering.2026-08-13.md](official/openai-prompt-engineering.2026-08-13.md) |
| GPT-5.6 family prompting (conditional) | [official/openai-gpt-5.6-sol-prompting.2026-08-13.md](official/openai-gpt-5.6-sol-prompting.2026-08-13.md), then [models/gpt-5.6.en.md](models/gpt-5.6.en.md) |
| GPT-5.6 model/API facts (conditional) | [official/openai-gpt-5.6-model.2026-08-13.md](official/openai-gpt-5.6-model.2026-08-13.md) |
| Another listed provider/model or translation | [models/index.md](models/index.md), then the catalog-matched guide |

Model guides are authored route layers over their listed source URLs. A
`provider_identifier` is the exact string accepted by the named provider;
`normalized_slug` is only a lowercase local route key, not an API alias. A
`source-gap` or `UNVERIFIED` status means the source does not support a
dedicated prompt/profile claim; do not turn the gap into behavior by inference.
