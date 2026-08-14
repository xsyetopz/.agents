# Conventions

Scope: package boundaries, semantic reference design, naming, and progressive
disclosure. Keep each resource portable after a project-scoped CLI copy.

## Package boundary

The open format requires a root `SKILL.md` with valid `name` and `description`
frontmatter. This repository's package contract additionally requires client
metadata, a validator configuration, references, assets, evals, a checker, and
an included license. Treat those additions as this catalog's distribution
contract, not as universal Agent Skills requirements.

## Entrypoint and headings

Keep one root `SKILL.md`; do not add wrappers, aliases, nested entrypoints, or
compatibility paths. Preserve this exact H2 order:

1. `Use this skill`
2. `Rules`
3. `Steps`
4. `Resources`
5. `Verify`

Use one placement rule: `Use this skill` contains triggers, exclusions, and
sibling redirects; `Rules` contains constraints; `Steps` contains one executable
path; `Resources` contains only package-local resource routing, starting with
`references/index.md`; `Verify` contains done state, commands, evidence, and an
explicit unavailable or `UNVERIFIED` classification. All five sections contain
content. The shared validator also requires `Verify` to name
`python3 scripts/check.py`. This five-part sequence is this repository's
contract, not an upstream Agent Skills requirement. Detail belongs one hop away
in `references/`.

## Reference names and routes

- Use lowercase-kebab, topic-specific names such as `package-distribution.md` and `model-routing.md`.
- Avoid generic root names such as `workflow.md`, `patterns.md`, or `tooling.md`.
- Reserve `references/index.md` for the package's root router. Use a directory only for a real taxonomy; add its own `index.md` when it has more than five leaves.
- Keep ordered procedures in a dedicated directory when numeric prefixes add meaning; do not impose numbers on unrelated topics.
- Link every contract `reference_paths` entry from the entrypoint or `references/index.md`, and keep links package-relative.

## Semantic consolidation

Consolidate by meaning, not by filename or line count. Before merging:

1. Trace inbound links, contract paths, eval cases, scripts, and source provenance.
2. Classify each section as canonical rule, unique example/case, duplicate boilerplate, or source snapshot.
3. Keep one canonical rule, preserve unique executable details and dated sources, and update routes atomically.
4. Remove stale paths rather than retaining aliases or shadow copies.

Use a consistent authored reference schema when useful: scope, rules, procedure,
checks, and sources. Split a reference above roughly 200 lines when one topic
has independent routes; retain a reason for any larger source snapshot.
For source records and Mermaid syntax, use the package
[reference provenance guide](reference-provenance.md); keep the record in a
normal `## Sources` or `## References` section rather than inventing frontmatter.

## Tone and portability

Describe artifact state, evidence, effect, and next check. Replace subjective
labels or inferred intent with observable conditions. Keep links, scripts,
assets, and symlinks under the package root; reject host paths, global checkouts,
and escaping links. Static checks, behavioral evaluation, and CLI evidence are
separate claims.

## Distribution

Select one skill explicitly, use the pinned CLI, project scope, and `--copy`,
then inspect the copied tree and lock entries. See
[package distribution](package-distribution.md) for command and removal evidence.

## Sources

- [Reference provenance guide](reference-provenance.md) for source records, scope boundaries, and freshness labels.
