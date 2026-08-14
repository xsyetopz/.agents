# Skill creator reference router

Select the smallest package-local reference that answers the current authoring,
validation, or distribution question. Read one route first; follow another
reference only when that route explicitly requires it.

## When you need | Read

### Authoring

| When you need | Read |
| --- | --- |
| reference names, package layout, semantic consolidation, or shallow disclosure | [conventions](conventions.md) |
| source records, claim boundaries, citation gaps, or GitHub Mermaid fences and edge labels | [reference provenance](reference-provenance.md) |
| routing graphs and behavioral examples | [graphs and examples](graph-and-examples.md) |

### Metadata and routing

| When you need | Read |
| --- | --- |
| `SKILL.md` name and keyword description fields | [frontmatter specification](frontmatter-spec.md) |
| `agents/openai.yaml` client metadata | [OpenAI YAML specification](openai-yaml-spec.md) |

### Validation and safety

| When you need | Read |
| --- | --- |
| required files, links, headings, portability, or static checks | [validation guide](validation-guide.md) |
| missing paths, stale links, or validator failures | [troubleshooting](troubleshooting.md) |
| expected outcomes, activation, untrusted content, or supply-chain review | [evaluation and security](evaluation-and-security.md) |

### Distribution

| When you need | Read |
| --- | --- |
| pinned CLI copy, list, remove, and lock evidence | [package distribution](package-distribution.md) |

All routes are relative to this package. Update this router, the entrypoint,
contract paths, and eval cases together when a reference is renamed or added.
