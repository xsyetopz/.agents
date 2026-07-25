# Authority sources

Use current, version-appropriate primary sources when a repository contract or
language rule is unclear. Record retrieval date and pinned tool versions in an
ADR or review note; these links are starting points, not a substitute for local
documentation.

- [AWS Well-Architected Framework pillars](https://docs.aws.amazon.com/wellarchitected/latest/migration-lens/well-architected-framework-pillars.html)
  — operational excellence, security, reliability, performance, cost, and
  sustainability questions.
- [Microsoft Architecture styles](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles)
  — selecting styles from workload constraints and trade-offs.
- [Microsoft Anti-Corruption Layer](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer)
  and [Strangler Fig](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig)
  — explicit integration and migration boundaries.
- [C4 model](https://c4model.com/) — hierarchical context, container, component,
  code, dynamic, and deployment views; use diagrams as communication, not
  proof of implementation.
- [Go module layout guidance](https://go.dev/doc/modules/layout), [PEP 8](https://peps.python.org/pep-0008/),
  [Rust module reference](https://doc.rust-lang.org/reference/items/modules.html),
  and [Kotlin source-file conventions](https://kotlinlang.org/docs/coding-conventions.html#source-file-names)
  — examples of ecosystem-specific naming and module authority.
- [ast-grep `run` command](https://ast-grep.github.io/reference/cli/run.html) and
  [JSON mode](https://ast-grep.github.io/guide/tools/json.html) — the pinned
  command shape and structured match coordinates used by the bundled adapter.

Prefer language specifications, compiler documentation, framework loader rules,
standards, and repository-pinned versions over blog summaries or copied
community templates. Mark an industry practice as a judgment when no primary
authority defines it.
