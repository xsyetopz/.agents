# Architecture verification and evidence

Use fitness functions to keep an architectural decision true as the repository
changes. Prefer deterministic checks at the owning boundary and report what
each check can and cannot prove.

For every skill-triggered repository change, run the capability preflight and
the full bundled audit before editing and again after editing. Treat command
output and exit codes as evidence. A scoped or inventory-only command is not an
acceptance proof; use it only with explicit user approval and retain the full
audit result. Never suppress a finding by excluding paths, lowering the gate,
editing an exception, moving code under an ignored directory, or changing the
checker without the user's explicit decision.

## Proof ladder

Run checks in this order unless the changed boundary makes a later check the
cheapest causal proof:

1. formatter, manifest, schema, package-content, generated-freshness, and
   configuration validation;
2. compiler/type checker plus focused unit, property, and contract tests;
3. forbidden-import, module-visibility, dependency-cycle, API/ABI baseline,
   schema compatibility, architecture, security, and supply-chain checks;
4. package/workspace build, integration tests, migrations, load/failure tests,
   and deployment assembly;
5. runtime smoke through the actual production entrypoint, then full QA and
   operational rehearsal where risk warrants it.

Stop at the first causal failure, repair the owning boundary, and rerun the
smallest affected proof before expanding scope. A helper test or successful
build cannot substitute for an entrypoint smoke when composition changed.

## Fitness-function classes

- **Dependency:** reject forbidden imports/includes, private paths, cycles,
  undeclared project references, and wrong visibility.
- **Public surface:** compare exports, headers, symbols, routes, schemas,
  events, package contents, and generated clients with an intentional baseline.
- **Ownership:** map source/test/fixture/generated paths to a capability and
  detect unowned data, duplicate contracts, or cross-boundary mutations.
- **Naming:** apply toolchain and public-contract rules first; use semantic
  filename, namespace, API, event, error, and configuration checks as policy
  gates only when explicitly configured.
- **Quality:** run contract, fault, security, load, capacity, compatibility,
  observability, recovery, and rollout tests that correspond to recorded
  scenarios.
- **Delivery:** validate lockfile scope, deterministic generation, artifact
  provenance, reproducible packaging, and environment-specific configuration.

## Syntax-aware evidence

For source-structure rules, prefer an AST or compiler-backed query over text
matching. Use `ast-grep` or Tree-sitter for language-structural patterns,
language-native analyzers or compiler APIs for symbols, types, visibility, and
references, and the authoritative build/package graph for resolved dependency
edges. A regular-expression or filename scan may inventory candidates, but it
cannot prove syntax, ownership, dependency direction, or semantic cohesion.
The bundled inline detector is a conservative lexical gate for registered
native and framework forms: it masks comments and strings but does not claim
complete parser coverage. Add AST/compiler-backed rules for forms outside its
registry; never weaken the bundled gate to accommodate a missed form.

## Bundled scanner

Run:

```bash
python3 scripts/audit_architecture.py <repo>
```

The scanner emits deterministic structural signals plus a mandatory
inline-test/benchmark policy gate. It also reports authored line-size bands,
naming heuristics, generic/flat buckets, artifact classification, JavaScript
lockfile conflicts, and machine-readable exception quality. It does not infer
semantic ownership, dependency direction, quality attributes, API compatibility,
or runtime correctness. Use `--fail-on warning` for a policy gate only when the
repository has reviewed its thresholds. `--fail-on never` is inventory-only and
requires explicit acknowledgement; it cannot establish acceptance. Likewise,
`--exclude` requires explicit scoped-audit acknowledgement. Excluded and exempt
paths remain visible and cannot establish full-repository acceptance.
The inline detector masks comments and strings, recognizes exact test/benchmark
source conventions, accepts only visible reviewed `test_source_roots` contracts
for custom runner layouts, and fails closed when authored source cannot be read.

The command wrapper stays in `scripts/audit_architecture.py`. Its implementation
lives in the focused `scripts/architecture_audit/` modules: `discovery.py` for
file and artifact discovery, `findings.py` for structural rules,
`inline_tests.py` for the bundled test/benchmark gate, `exceptions.py` for
machine-readable exceptions, `audit.py` for orchestration, and `cli.py` for
arguments and rendering. Keep future changes in the owning module; do not grow
the wrapper or merge unrelated responsibilities back into one script.

Run `python3 scripts/architecture_tools.py capabilities --root <repo> --format json`
before using a configured provider, then run the full audit command. The
architecture audit exposes each configured provider status in its text/JSON
report. A required provider that is absent,
times out, fails, or emits malformed structured output is blocked and fails the
gate; it is never converted into a heuristic pass. The bundled filename and
directory checks are inventory evidence only.

## Evidence report

For every check, record the command or tool, scope, outcome, relevant artifact
or log, and what remains unproven. Distinguish passed, failed, skipped,
blocked, flaky, and environment-failed checks. Include baseline failures and
known limitations. A claim that a pattern or quality attribute is enforced
without a named check is an unresolved design risk.
