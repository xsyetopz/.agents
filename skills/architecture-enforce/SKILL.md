---
name: architecture-enforce
description: Use when designing, reviewing, refactoring, migrating, or decomposing repository architecture — packages, modules, deployables, APIs, schemas, build graphs, or cross-language boundaries. Enforce ownership, dependency direction, public contracts, quality attributes, security and reliability, naming, toolchain topology, separation of tests and benchmarks, and executable verification without inventing layers or suppressing findings.
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

## When NOT to use

- Making architecture *decisions* (patterns, ADRs, decomposition) — use `architecture-design`
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

## Quick start — mandatory audit protocol

From this skill directory, run both commands before and after every repository change:

```bash
python3 scripts/architecture_tools.py capabilities --root <repo> --format json
python3 scripts/audit_architecture.py <repo> --format json
```

Record the exact scope, gate, provider status, findings, and exit codes. A
source read or model-produced claim is not evidence that the commands ran.

Do not use `--exclude`, `--fail-on never`, or an edited exception entry to
suppress findings without explicit user approval for that exact scope and reason.

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

- `architecture-design` — Before enforcing boundaries, use this to make the
  architecture decisions (ADRs, pattern selection, decomposition). Enforcement
  without design has no target to enforce against.

## Maintenance

```sh
python3 scripts/audit_architecture.py <repo> --format json
```
