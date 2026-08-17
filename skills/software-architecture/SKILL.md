---
name: software-architecture
description: Software architecture decisions, boundary audits, topology enforcement, dependency direction, ownership, and structural migrations.
---

# Software Architecture

Design, audit, and enforce software boundaries from repository evidence while preserving behavior and established contracts unless a migration is authorized.

## Use this skill

- Decide or audit package, module, service, storage, protocol, deployment, ownership, public-contract, or multi-file structure.
- Enforce a selected topology, dependency direction, cohesive ownership boundary, generated-source boundary, or structural migration.
- Use it for architecture drift, cycles, fragmented sibling files, helper or manager colonies, public-surface changes, and architecture-check failures.
- Do not use for isolated formatting, comments, local naming, or other behavior-preserving edits with no structural effect.
- Redirect repository policy and documentation to `/skill:repo-docs`, pipeline gates to `/skill:git-ci-cd`, and prompt/tool-routing design to `/skill:prompt-engineering`.

## Rules

- Inspect repository instructions, callers, contracts, tests, build and deployment graphs, generators, and public surfaces before deciding or editing.
- State scope, owners, boundaries, dependency direction, quality scenarios, preserved contracts, migration order, and rollback boundary.
- Compare materially different candidates and a do-less baseline before selecting a nontrivial topology.
- Assign every changed path one durable owner, responsibility, visibility, lifecycle, dependency direction, and reason it remains separate.
- Never weaken warnings or failures with exclusions, ignores, advisory modes, threshold changes, allow-failure paths, or reduced tests.
- Do not invent custom schema files or custom generated files as outputs. Do not add custom policy files, manifests, registries, provenance files, or generated audit reports; use repository-native checks and report evidence directly.
- Change canonical generator inputs instead of generated output. Preserve public entrypoints and contracts unless the authorized migration records the change.

## Steps

1. Frame the decision or finding, scope, owners, constraints, quality scenarios, preserved contracts, and completion evidence.
2. Inventory Git state, authored and generated source, callers, dependencies, build targets, tests, generators, deployables, and public surfaces. Run the bundled Python capability preflight and read-only audit when they apply.
3. Map current and candidate topology. Compare alternatives, including do-less, against migration cost, reversibility, operational risk, and measurable quality attributes.
4. Select the smallest cohesive structure and record ownership, dependency direction, migration order, rollback boundary, and rejected alternatives in the response or an existing authorized repository format.
5. Implement the authorized slice through canonical source and repository-native configuration. Do not create a custom architecture schema or generated evidence file.
6. Run focused tests, production or integration entrypoints, repository-native architecture checks, and final diff inspection. Resolve each diagnostic at its owning cause.

## Resources

- Start with the package [reference router](references/index.md).
- Load only the routed design or enforcement reference needed for the current decision or finding.

## Verify

- Done means every changed path has a durable owner, contracts are preserved or explicitly migrated, repository-native checks have no unresolved warnings or errors, and no suppression or custom output artifact was added.
- Run `python3 scripts/check.py`, `python3 scripts/providers.py capabilities --root <repo> --format json`, `python3 scripts/audit_architecture.py <repo> --format json`, and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Run the package audit tests plus the target repository's focused tests, production or integration entrypoint, architecture checks, and final diff inspection.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark unavailable provider data, hosted settings, integration runs, or runtime evidence `UNVERIFIED`.
