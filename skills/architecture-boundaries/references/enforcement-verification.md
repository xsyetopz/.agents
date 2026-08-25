# Architecture verification and evidence

> Locally authored enforcement guidance, not a primary source or generated snapshot; source gap: live verification of current language, provider, and tool claims against authority sources (see `enforcement-sources.md`) is required.

Use fitness functions to keep an architectural decision true as the repository
changes. Prefer deterministic checks at the owning boundary and report what
each check can and cannot prove.

For every skill-triggered repository change, enumerate the candidate working
tree first and include tracked plus non-ignored untracked files:

```bash
git status --short
git ls-files --others --exclude-standard
```

Run the capability preflight and full bundled audit before editing and again
after editing. Treat command output and exit codes as evidence. The command has
one acceptance policy: full Git-visible scope (tracked plus non-ignored
untracked files), fixed thresholds, and failure on every warning or error. It
exposes no scope, severity, threshold, or exception waiver. Tracked files
remain visible even when an ignore pattern matches them; never suppress a
finding by moving tracked code under an ignored directory or changing the
checker.

For a topology trigger, require a source-topology table before editing and
after editing. Each changed or new source path must map to owner, change reason,
visibility, lifecycle, dependencies, and a rationale for not consolidating it
with the nearest owner. A missing row or a categorical one-file split is an
unresolved structural finding. Acceptance requires zero unresolved warning or error
findings; pre-change output is context for comparison, not a waiver
baseline, and existing findings must remain visible with a disposition.

## Proof ladder

Run checks in this order unless the changed boundary makes a later check the
cheapest causal proof:

1. formatter, manifest, schema, package-content, generated-freshness, and
   configuration validation;
2. compiler/type checker plus focused unit, property, and contract tests;
3. forbidden-import, module-visibility, dependency-cycle, API/ABI comparison,
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
  events, package contents, and generated clients with intentional compatibility
  evidence. A baseline comparison identifies change; it never waives a finding.
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

## Repository-native audit evidence

Use the target repository's existing dependency, architecture, test, build, and
lint commands. Keep their configuration unchanged while diagnosing a finding.
Capture exact commands and exit codes in the response. Do not add a custom
schema, provenance file, suppression baseline, or generated audit report.

## Check integrity and failure ownership

Lint, test, policy, provider, build, and architecture checks are part of the
acceptance contract. Audit the check configuration and CI changes along with
the source tree. The following are prohibited as a way to obtain a green
result:

- adding or expanding ignore directives, tool ignore files, or lint/check
  exclusions;
- disabling rules, providers, or jobs, or marking them advisory;
- lowering severity or thresholds, altering baselines, or adding exceptions;
- adding `allow-failure` or `continue-on-error`;
- excluding a failing path; and
- weakening or deleting a test or check.

Fix each failure at its owning cause and rerun the affected proof. If a tool is
wrong, leave the gate enabled and failing, then record a minimal reproducer
(tool/version, exact command and configuration, input, output, and exit code)
and request explicit policy-change authorization. The architecture gate cannot
pass while a check is disabled, downgraded, excluded, advisory, or otherwise
weakened. The evidence report must include one row per check with its owner,
exact command, scope, active rules/providers/jobs, fixed severity/failure
behavior, result, and artifact path.

## Evidence report

For every check, record the command or tool, scope, outcome, relevant artifact
or log, and what remains unproven. Distinguish passed, failed, skipped,
blocked, flaky, and environment-failed checks. Include pre-change diagnostic
results and known limitations without treating them as a baseline waiver. A
claim that a pattern or quality attribute is enforced without a named check is
an unresolved design risk.

## Sources

- Architecture source map (see `enforcement-sources.md`); verify the linked source record before relying on current or external claims.
