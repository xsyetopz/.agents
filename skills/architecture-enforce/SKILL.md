---
name: architecture-enforce
description: Use when designing, reviewing, refactoring, migrating, or decomposing repository architecture - packages, modules, deployables, APIs, schemas, build graphs, or cross-language boundaries. This also triggers when a change creates, splits, merges, moves, or renames three or more sibling source files, or changes package/directory topology. Enforce ownership, dependency direction, public contracts, quality attributes, security and reliability, naming, toolchain topology, separation of tests and benchmarks, and executable verification without inventing layers or suppressing findings.
---

# Architecture Enforce

Enforce architecture as an accountable system of boundaries, decisions, and
proof. Be strict about ownership, dependency direction, public contracts,
quality attributes, and operational behavior. Reject cargo-cult layering,
pattern name-dropping, and arbitrary refactors presented as architecture.

This skill owns architectural enforcement. For architecture *decisions*
(ADRs, pattern selection, decomposition), use `architecture-design` first.

## When to use

- Auditing an existing codebase for architecture violations
- Enforcing import/dependency rules, module boundaries, or naming conventions
- Reviewing a PR for architectural compliance
- Refactoring or migrating code while preserving architectural contracts
- Setting up CI architecture checks
- Creating, splitting, merging, moving, or renaming **three or more sibling
  source files** in one change
- Changing package, module, export, target, or directory topology, even when
  the source edits look mechanical

## When NOT to use

- Making architecture *decisions* (patterns, ADRs, decomposition) - use `architecture-design`
- A single-line fix or rename with no structural impact
- Inventing layers or interfaces solely to match a diagram

## Non-negotiable contract

Every changed architectural unit must have:

1. One accountable owner and one durable capability or reason to change
2. An explicit public surface, or an intentional private status
3. Allowed dependency directions enforced by the language, build graph, or policy
4. Owned data, lifecycle, failure, observability, and compatibility behavior
5. Tests at the boundary they claim to prove
6. A reproducible build/package/deployment declaration
7. A focused verification path through the real entrypoint

Do not accept compilation, green unit tests, a diagram, or a familiar pattern
name as architecture proof by itself.

### Topology and decomposition gate

Files are implementation units, not architectural boundaries by default. A
type, operation, phase, helper, validation rule, or procedural step does not
earn a file merely because it has a name. Reject one-type-per-file,
one-operation-per-file, one-phase-per-file, one-helper-per-file, and
one-validation-per-file decomposition when the units share an owner, change
reason, visibility, lifecycle, dependency set, or test contract. Consolidate
such units into the nearest cohesive owner.

`Validation`, `Helpers`, `Open`, `Reduce`, and `Commit` are procedural roles,
not durable architectural owners. They may remain separate only when evidence
proves an independent lifecycle, public contract, deployment/visibility
boundary, dependency direction, or independently verifiable failure policy.
Names and a desire for a tidy tree are not evidence.

This skill is mandatory for any topology trigger listed above. Build a
source-topology map for the candidate working tree (tracked **and untracked**
files), with one row per changed or newly created source unit:

| Path | Owner | Change reason | Visibility | Lifecycle | Dependencies | Consolidation rationale |
| --- | --- | --- | --- | --- | --- | --- |

Every row must name the nearest durable owner and explain why the unit cannot
be consolidated. A missing row, shared owner with no independent contract, or
unexplained categorical file is a structural finding.

### Fail-closed acceptance

Acceptance is a technical gate, not a conversational approval. Do not replace
evidence with urgency, reassurance, praise, a user preference, or a verbal
exception. A passing acceptance requires the unmodified full-repository gate,
the source-topology map, and zero unresolved warning or error findings.
Existing findings block acceptance; they are not a baseline that can be
carried forward. The command exposes no exclusion, disabled/inventory-only,
advisory, threshold-override, or exception-waiver mode. If the gate cannot
establish the required result, stop and report the blocker.

### Check integrity and failure ownership (non-negotiable)

Lint, test, policy, provider, build, and architecture checks are part of the
contract and must remain active. Never add or expand ignore directives (such
as `.gitignore`, tool ignore files, or lint/check excludes), disable a rule,
provider, or CI job, lower severity, add `allow-failure` or
`continue-on-error`, exclude a failing path, alter a baseline, or weaken or
delete a test/check to obtain a green result. A suppression is not a fix and
cannot turn a failed gate into acceptance.

Repair failures at the owning cause and rerun the affected check. If the tool
itself is wrong, preserve the failing gate and record a minimal reproducer
(tool/version, exact command and configuration, input, output, and exit code)
before requesting explicit authorization for a policy change. The architecture
gate remains blocked while a check is disabled, downgraded, excluded, made
advisory, or otherwise weakened; no agent may grant that authorization by
conversation alone.

## Quick start - mandatory audit protocol

From this skill directory, first enumerate the complete candidate working tree;
the audit must cover source files that are not yet tracked:

```bash
git status --short
git ls-files --others --exclude-standard
```

Run both commands before and after every repository change:

```bash
python3 scripts/providers.py capabilities --root <repo> --format json
python3 scripts/audit_architecture.py <repo> --format json
```

Record the exact scope, gate, provider status, findings, and exit codes. A
source read or model-produced claim is not evidence that the commands ran.
The acceptance command has one fixed policy: full filesystem scope, tracked and
untracked candidates, fixed thresholds, and failure on every warning or error.
There is no acceptance downgrade flag or waiver file. Confirm that the
candidate map includes every changed and untracked source path before claiming
completion.

## Enforcement profiles

Choose the smallest profile that explains the real deployment boundaries:

| Profile | When |
|---|---|
| Modular monolith | One deployable with capability-owned modules |
| Library / SDK | Narrow stable API/ABI, versioned compatibility |
| Client / UI / edge runtime | Platform lifecycle, state ownership, rendering/input boundaries |
| Pipeline / data-oriented | Explicit stages, data ownership, backpressure |
| Plugin / extension host | Discovery, lifecycle, failure isolation |
| Service / distributed | Independent deployability, network contracts, idempotency |
| Embedded / real-time | Timing, resource, determinism, hazard budgets |
| Polyglot workspace | Language-native modules + explicit FFI/schema/process contracts |

Do not select microservices, CQRS, event sourcing, or a service layer without a
stated force the simpler profile cannot satisfy.

## Reference map

| If you need to... | Load |
|---|---|
| Understand ownership, coupling, dependency, and migration rules | `references/principles.md` |
| See pattern selection gates and ADR template | `references/patterns.md` |
| Define quality-attribute scenarios and production gates | `references/quality-attributes.md` |
| Run fitness functions and evidence reporting | `references/verification.md` |
| Configure syntax rules, providers, and tool-backed checks | `references/tooling.md` |
| Apply naming authorities across all semantic surfaces | `references/naming.md` |
| Understand language-family and ecosystem boundaries | `references/languages.md` |
| Navigate build systems (CMake, Make, Ninja, Xmake, Conan) | `references/toolchains.md` |
| See accepted and rejected structural examples | `references/examples.md` |
| Place tests in runner-recognized sources | `references/testing.md` |
| Verify primary architecture and ecosystem authority links | `references/sources.md` |

## Related skills

- `architecture-design` - Before enforcing boundaries, use this to make the
  architecture decisions (ADRs, pattern selection, decomposition). Enforcement
  without design has no target to enforce against.

## Maintenance

```sh
# From the repository root:
python3 skills/architecture-enforce/scripts/audit_architecture.py <repo> --format json
```
