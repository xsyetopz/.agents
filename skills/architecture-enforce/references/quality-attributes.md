# Quality-attribute scenarios and gates

Architecture is a response to measurable forces, not a collection of nouns.
Write scenarios before selecting a pattern or boundary. Use this form:

```text
Stimulus: <request, fault, deploy, load, threat, or change>
Context: <normal/peak/failure state, trust zone, data class, version>
Response: <observable behavior and owner>
Target: <latency, throughput, availability, RTO/RPO, error budget, or deadline>
Proof: <test, load run, threat check, telemetry, rehearsal, or review>
```

## Reliability and resilience

Require explicit failure domains, deadlines, cancellation, retry and
idempotency policy, backpressure, overload behavior, recovery, and data
consistency. Define RTO/RPO or availability targets when the system is
operationally significant. Test dependency loss, partial writes, duplicate
delivery, stale reads, restart, deploy rollback, and exhausted capacity.

Do not add retries without a bounded deadline, jitter/backoff, duplicate
semantics, and a decision about which layer owns retry. Do not call a system
resilient because it has a circuit breaker; prove recovery and user-visible
behavior.

## Security and privacy

Map trust boundaries, principals, assets, data classifications, and threat
assumptions. Assign ownership for authentication, authorization, validation,
secrets, key rotation, audit trails, dependency provenance, and incident
response. Minimize data movement and retention. Keep identity and policy types
out of adapters that should not own access decisions.

Verify least privilege, fail-closed behavior, input/output validation, secure
defaults, dependency and artifact scanning, secret absence, and relevant abuse
cases. Treat public APIs, plugins, FFI, generated clients, and message brokers
as attack surfaces.

## Performance and capacity

State workload shape, latency percentiles, throughput, concurrency, memory,
storage, network, startup, and cost budgets that influence architecture. Model
capacity and contention before introducing caches, queues, batching, pools,
lock-free structures, or a new service.

Measure the production-shaped path with representative data and failure states.
Document cache invalidation, freshness, eviction, hot keys, queue limits, and
degradation. A faster microbenchmark does not prove a faster system boundary.

## Operability

Every deployable and consequential async boundary needs an operating owner,
structured logs, metrics, traces/correlation, health/readiness semantics,
alerts, dashboards, rollout/rollback, and a runbook. Define SLOs, error-budget
policy, and what happens when telemetry is unavailable. Keep diagnostic context
at translation and process boundaries without leaking secrets or payloads.

## Compatibility and evolution

For every API, ABI, schema, event, database, generated client, or configuration
contract, define producer/consumer ownership, compatibility direction,
versioning, deprecation, migration, and rollback. Test old/new combinations
when rolling upgrades or mixed versions are possible. Treat serialized names,
error codes, metrics, and environment variables as public contracts when
external consumers depend on them.

## Delivery and supply chain

Require a reproducible dependency resolution policy, authoritative manifests,
lockfile scope, build inputs, generated-output provenance, artifact identity,
and environment parity. Verify that committed generated output is fresh and
that deployment artifacts can be traced to source and tool versions. Keep build
and package boundaries consistent with source visibility.

## Cost and sustainability

Assess compute, storage, network, licensing, energy, and operator time when
they materially constrain the design. Assign an owner and a measurement method;
avoid speculative optimization or sustainability claims without a workload
model. Prefer deletion, bounded retention, right-sized capacity, and simpler
operations when they satisfy the scenario.

## Safety, compliance, and accessibility

For regulated, safety-relevant, or user-facing systems, identify applicable
hazards, controls, evidence retention, auditability, data residency, recovery,
and human-impact constraints. Assign review ownership and preserve traceability
from requirement to implementation and test. For UI and client architecture,
include input modality, assistive technology, localization, privacy, and reduced
motion or resource constraints in the scenarios; defer component-level rules to
the platform design system when one exists.

## Acceptance rule

An attribute is architecturally addressed only when the scenario has an owner,
a target, a design invariant, and executable or independently reviewable proof.
Record unknown targets as risks; do not silently substitute a pattern or a
folder structure for missing requirements.
