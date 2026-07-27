---
name: fourth-wall
description: Coordinate work through a bounded native Codex MultiAgentV2 task graph. Read before the first subagent spawn or orchestration action in a task. Use for complexity-aware model dispatch, behavioral roles, task messaging, worker-to-worker ownership delegation, dependency fan-out, review loops, goal checkpoints, warm handoffs, synchronization, and recovery. Do not use for routine single-agent work or communication across unrelated top-level Desktop tasks.
---

# Fourth Wall

Use this skill before a root agent spawns its first child, and whenever an existing native Codex MultiAgentV2 task tree needs routing, synchronization, review, recovery, or handoff. Depth-1 Terra/Sol Workers must also follow it before using their single bounded delegation allowance.

The skill solves one coordination problem: divide work without losing the full outcome, overlapping ownership, wasting root context on delegated loops, or accepting prose as proof. Complexity and horizon select a capability pair; a behavioral role selects the duty and task-name prefix. When the Skizzles profile is installed, generated capability-bearing `agent_type` values persist that pair through reactivation. The root owns the graph, integration, and final acceptance.

## Audience and scope

- Operate within the current root task tree. Native task paths and messaging do not cross unrelated top-level Desktop tasks.
- Keep the root focused on the overall outcome, decisions, dispatch, integration acceptance, and evidence evaluation.
- Delegate complete ownership slices with a clear owner, boundary, implementation, validation, and evidence contract. Do not retain the expensive execution loop at the root merely because delegation is active.
- Stay single-agent when coordination overhead would exceed the value of delegation.
- Children are peers beneath the root. Non-Workers return further decomposition to the root. A depth-1 Terra/Sol Worker may dispatch one active bounded Worker only when it can transfer a small, disjoint, end-to-end ownership slice while continuing independent implementation.

## Dispatch contract

Name every child `<role>__<objective>`. Double underscores separate the behavioral role from the objective; use single underscores inside the objective. Examples: `worker__implement_filters`, `triage__map_sync_flow`, and `review__audit_auth_change`. Capability belongs in the selected native `agent_type` or explicit fallback fields, not in the task name.

Choose the cheapest route likely to succeed. Complexity selects the model class; horizon selects reasoning effort and how much recent context to fork:

| Route | Complexity / horizon | Preferred model | Effort | Availability fallback |
|---|---|---|---|---|
| Mechanical | Tiny, repetitive, short | `gpt-5.6-luna` | low | `gpt-5.6-terra` low |
| Scoped | Conventional, bounded, short | `gpt-5.6-luna` | medium | `gpt-5.6-terra` low |
| Broad | Straightforward reasoning, long context | `gpt-5.6-terra` | low | None |
| Standard | Normal debugging or implementation | `gpt-5.6-terra` | medium | None |
| Complex | Ambiguous but bounded cross-boundary reasoning | `gpt-5.6-sol` | low | None |
| Specialized | Architecture, security, migrations, or long horizon | `gpt-5.6-sol` | medium | None |
| Critical | Adversarial acceptance, irreversible work, or repeated failure | `gpt-5.6-sol` | high | None |

This table is a capability baseline and fallback. It is not a normative winner ranking. Do not derive routing policy from AAII scores, prices, or the table alone. Comparable assignments must record an explicit candidate set, propensity or seed, workflow shape, and verified workflow measurements. See [references/routing-learning.md](references/routing-learning.md).

Use Luna only when the active `spawn_agent` schema offers it and the assignment is short-lived, self-contained, cheaply verifiable, and comfortably below long-context territory. If Luna is unavailable, use the listed Terra fallback. Prefer Terra as context insurance when broad repository history must remain coherent even if reasoning is conventional. Use Sol when ambiguity, specialization, runtime-only behavior, cross-boundary architecture, platform lifecycle, or defect-escape cost dominates. A small difficult task may need Sol, while a large straightforward mapping task may fit Terra.

Do not spend model turns merely polling commands or children. The owner of a long-running command uses the native bounded wait/session primitive, stores verbose output outside model context, and reports only completion state, relevant deltas, error signatures, and artifact paths. Delegate an engineering outcome only when the child can interpret and act on the result.

When the generated Skizzles roles are installed and advertised, select the matching capability-bearing `agent_type` and do not duplicate its model or effort with independent overrides. Otherwise pass `model` and `reasoning_effort` explicitly on every spawn, using only models advertised by the active tool schema; do not invent an `agent_type` that the schema does not expose.

Choose `fork_turns` deliberately:

- Use `"none"` for self-contained packets, isolated implementation, sensitive stale context, and Worker grandchildren.
- Prefer a small positive integer string such as `"1"` or `"2"` when recent owner intent or an established plan would prevent rediscovery.
- Use `"all"` only when the complete conversation is genuinely required and bounded enough to justify its context cost.

Codex 0.145.0-alpha.18 supports explicit model/reasoning overrides with positive and full-history forks. Full-history forks still inherit the parent `agent_type`, so do not combine `fork_turns="all"` with an `agent_type` override. Do not claim an effective model or effort merely from a successful call; use host-visible task settings or rollout evidence when verification matters.

Choose the independent behavioral role that best matches the duty. Canonical templates live in `assets/agent-role-templates/`; packaging generates the ignored `assets/agents/` output and its manifest.

| Role | Use | Resource |
|---|---|---|
| Triage | Focused codebase research and current-shape mapping | [agent-role-templates/triage.toml](../../assets/agent-role-templates/triage.toml) |
| Worker | Well-defined implementation with explicit ownership | [agent-role-templates/worker.toml](../../assets/agent-role-templates/worker.toml) |
| Designer | Frontend and product UI implementation | [agent-role-templates/designer.toml](../../assets/agent-role-templates/designer.toml) |
| QA | Runtime piloting and evidence-rich product verification | [agent-role-templates/qa.toml](../../assets/agent-role-templates/qa.toml) |
| Review | Independent adversarial review and final validation | [agent-role-templates/review.toml](../../assets/agent-role-templates/review.toml) |
| Deployment | Careful procedural deployment and production operations | [agent-role-templates/deployment.toml](../../assets/agent-role-templates/deployment.toml) |

The generated manifest is the source of truth for installed capability names. The current defaults are `default` = Terra-medium, `triage` = Terra-low, `worker` = Luna-medium, `designer` = Sol-medium, `qa` = Luna-medium, `review` = Sol-medium, and `deployment` = Sol-medium. Worker has the complete Luna, Terra, and Sol ladder; other roles expose only the variants declared in `assets/agent-role-spec.json`.

In every spawn message:

1. Name the selected route and role.
2. Tell the child to read this skill and the linked role resource.
3. Provide the complete objective, ownership, constraints, established decisions, relevant skill obligations, and expected proof.
4. Choose the smallest useful `fork_turns` value so the handoff remains explicit without forcing the child to rediscover recent decisions.

For a long or replacement-heavy root task, keep one durable task packet under `/tmp` and give children its path plus their slice-specific instructions. Keep the packet concise and operational; do not automate reconstruction or rewriting of encrypted spawn messages. Record the overall objective, established decisions, constraints, live ownership, evidence, open gates, and routing state. Update it only at meaningful handoffs or acceptance points, not as a transcript.

Example:

```text
You are dispatched as a Scoped Worker. Select the advertised generated
`worker` capability (or the explicit Terra-low fallback when roles are absent).
Read $fourth-wall and the canonical Worker role. You are a bounded leaf and
must not spawn subagents.

Assignment: ...
Ownership: ...
Constraints: ...
Expected proof: ...
```

## Execution discipline

Role templates describe duties; generated capability-bearing roles carry the model and effort decision. Explicit spawn fields carry that decision only when the generated profile is unavailable.

- Act decisively when the path is clear and evidence is sufficient.
- Keep mechanical and reversible work direct.
- Investigate uncertainty that materially affects correctness, ownership, or costly rework.
- Stop and report a real owner decision when competing valid outcomes cannot be resolved from code, evidence, or instructions.
- Prefer one child owning investigation-through-proof for a coherent slice over splitting implementation and its focused validation between child and root.
- Complete causal ownership includes the smallest executable proof of the real boundary or production entrypoint changed. Source inspection, helper-only tests, and successful builds are not sufficient when a local runtime smoke can exercise the behavior directly.
- For runtime, platform, cross-process, or live-state boundaries, sequence proof by increasing cost: focused source/unit checks, then the cheapest causal smoke through the production entrypoint, then full product QA. Skip the smoke only when full QA is itself the cheapest executable proof.
- A test-green/runtime-red result raises the next owner one route. A second failure on the same causal surface requires fresh Triage of the production path and proof boundary before another implementation attempt.
- Use the root's capability for decomposition, cross-slice decisions, and acceptance. Route repetitive implementation, integration stabilization, build/test loops, and runtime proof to an appropriately capable leaf whenever the ownership can be made coherent.
- Delegate engineering loops, not command errands. A Worker grandchild owns inspection, implementation, focused checks, in-scope fixes, and its compact completion evidence together.

## Escalation and cooldown

Treat the dispatch table as the baseline and maintain a task-family floor when execution evidence shows the baseline is insufficient. Escalation is fast and de-escalation is deliberately slow.

Raise the affected task family's floor immediately when a lower-route result fails acceptance, root or reviewer must substantially repair it, ownership crosses an unexpected boundary, reproduction becomes runtime-only or platform-specific, a proposed fix violates an architectural invariant, or the same causal surface fails again. A test-green/runtime-red result raises the next owner one route. A second failure requires fresh Triage of the production path and proof boundary before another implementation attempt. Attach the floor to a concrete risk signature or ownership family, not permanently to the whole repository.

Within an active systemic incident, keep diagnostic and acceptance work at the proven elevated floor. Once uncertainty is removed, bounded implementation descendants may use a lower route when the invariant, ownership, and proof are explicit; the elevated reviewer still owns acceptance. Never infer that a lower route would have succeeded merely because a higher-route task completed in one shot.

Consider a one-route cooldown only after three consecutive independently accepted assignments in the same task family. Count a success only when the first implementation passes focused checks and runtime proof, independent review finds no material issue, and neither root repair nor replacement is required. Use only the documented routes: `critical` -> `specialized` -> `complex` -> `standard`. This preserves the model while reducing reasoning wherever the table supports it, then crosses model class once. `broad` is selected by long context rather than elevated difficulty, so move it to `scoped` only when a new assignment is genuinely short-context; likewise move `standard` to `scoped` only after the work becomes independently Luna-eligible. `mechanical` and `scoped` are already baseline routes. Keep the reduced route on probation for three more clean assignments before adopting it as the new baseline. Any material rejection, root rescue, architecture correction, or attributable regression resets the clean-success count and immediately restores the last proven floor. Do not invent model/effort hybrids outside the routing table.

Do not automatically cool down crash investigation, security or authentication, data corruption, migrations, irreversible operations, native window or engine lifecycle, accessibility-engine faults, or final adversarial acceptance. Their sparse samples and high defect cost do not justify downward experiments. Record the task family, current floor, evidence trigger, clean-success count, probation state, and last accepted route in the durable task packet.

## Native primitives

- `spawn_agent`: dispatch a bounded task with a behavioral role and clear handoff; only eligible Workers may use it below the root.
- `list_agents`: inspect live task paths, statuses, and latest assignments.
- `send_message`: queue context or corrections to running work without starting a new turn.
- `followup_task`: reactivate an idle or completed child for another turn while preserving its task identity, model, reasoning effort, and accumulated context.
- `wait_agent`: wait for mailbox activity, user steering, or a bounded timeout.
- `interrupt_agent`: stop obsolete or unsafe work without destroying task identity.

Read [references/coordination-loop.md](references/coordination-loop.md) for exact delivery and lifecycle semantics.

## Workflow

1. Preserve the full owner-requested outcome and acceptance evidence. Keep an active goal's complete breadth.
2. Build the smallest useful bounded graph. Prefer one Worker with complete slice ownership before broad fan-out.
3. Assign disjoint ownership, a behavioral role, a self-contained handoff, implementation and validation responsibility, and expected proof.
4. Continue only high-value root work such as shared-contract decisions, integration inspection, and downstream routing. Do not fill child runtime with duplicate implementation, routine test loops, or repeated status polling.
5. Treat completion messages as claims. Inspect changes and evidence, then dispatch Review or QA when risk warrants independent proof.
6. When an integrated ownership slice has focused proof and no known breakage, commit it as a forward-progress checkpoint before changing causal surfaces, beginning risky work, handing off substantial ownership, or starting independent QA/Review. `/goal` state is not required. The root owns the checkpoint and excludes unrelated shared-worktree changes.
7. Send corrections to a running owner with `send_message`. After it completes, use `followup_task` when the same owner and context remain useful; spawn a fresh sibling when independence, a context reset, or a different route is the point. Prefer corrective commits over rewriting already reviewed checkpoints.
8. Finish with a coherent integrated outcome, validating the aggregate commit series and working tree rather than only the latest checkpoint.

Read [references/delegation-contract.md](references/delegation-contract.md) before splitting consequential implementation work.

## Evidence contract

Every delegated owner returns an inspectable completion claim:

- owned files, modules, services, or product surface
- behavior now true at that boundary
- focused checks and their results
- the cheapest causal runtime proof when the production entrypoint is locally runnable
- artifacts such as screenshots, logs, or report paths
- checks not run, with the reason
- remaining risks, decisions, and dependent work

The root inspects the change and its evidence before integration. Review judges correctness, architecture, security, and evidence sufficiency. QA supplies runnable product proof. Source inspection, helper-only tests, successful builds, child completion prose, and guardian allow decisions do not substitute for the required causal evidence.

## Common task shapes

- A big-picture root retains product intent and decisions while specialists own bounded execution.
- Dependency fan-out dispatches independent preparation in parallel, then releases downstream work after contracts stabilize.
- Worker offload lets a Terra/Sol Worker continue its implementation while one bounded Worker owns a small disjoint slice through focused proof.
- A persistent specialist is reactivated for coherent follow-on work when retained context and ownership reduce rediscovery.
- An adversarial loop has Review evaluate implementation and evidence, then sends findings to a fresh owning Worker when more work is needed.
- Integration stabilization gives one Worker the serial build, test, and fix loop after parallel edits settle. The root retains Git authority and acceptance.
- Implementation proof gives one QA leaf ownership of application startup, piloting, logs, screenshots, and runtime evidence before any independent downstream QA task.
- A warm handoff collects a compact state packet, dispatches a fresh sibling with the same role, then retires obsolete ownership.
- Drift recovery inspects the tree, resolves stale or overlapping ownership, and interrupts only obsolete or unsafe work.

Read [references/handoff-packet.md](references/handoff-packet.md) for context renewal and its limits.

## Measurement and learning

Every experiment records the complete workflow, not just the selected model:
task stratum, model and effort per stage, topology, decomposition, role plan,
context inheritance and duplication, tokens, retries, failed loops, escalation,
replacement, latency, and independently verified success. Join the observation
to the runtime assignment and receipt by digest. Compare candidates only inside
a comparable stratum after minimum-sample and reliability gates; minimize
expected total workflow tokens per verified success, with money and latency
secondary. A missing join, model completion claim, or guardian allow is not
success evidence. The host owns assignment and persistence; Fourth Wall records
evidence and curates policy revisions after independent review.

When observed behavior reveals a reusable routing or lifecycle caveat, follow [references/learning-loop.md](references/learning-loop.md). Record evidence-backed candidates without silently changing global policy during active work.

## Hard boundaries

- Triage, Designer, QA, Review, Deployment, and bounded Luna/Terra Workers are leaves. A depth-1 Terra/Sol Worker may have at most one active bounded Worker grandchild; all other delegation proposals return to the root.
- Worker grandchildren must be named `worker__...`, select the generated `worker` or `worker_terra_medium` capability when advertised (otherwise explicit Luna-medium or Terra-low fallback), set `fork_turns = "none"`, own a disjoint complete implementation loop, and never spawn again. The parent and root enforce the one-active-grandchild limit through lifecycle discipline.
- Reactivate a completed child only when its prior role, route, context, and ownership still fit the next action. Spawn a fresh sibling when independent review, clean context, changed ownership, or escalation is valuable.
- Do not let two implementation tasks own overlapping files without explicit coordination.
- The root owns Git integration, decides when parallel edits are stable, and accepts the final result. Once stable, delegate serialized project-wide verification, integration repair loops, and live proof when a leaf can own them coherently; run them at the root only when delegation overhead would exceed the work.
- The root commits stable forward progress after inspecting a coherent slice and its evidence. Do not commit every child result mechanically, known-broken intermediate states, overlapping ownership, or unrelated user/agent changes. Commit boundaries are independent of `/goal` boundaries.
- Do not turn size, difficulty, or uncertainty into a blocker. A blocker identifies an external dependency, contradiction, safety issue, or owner decision.
- Do not accept completion prose as proof.
- Do not attempt to promote a child into the root. Root renewal requires a new top-level task and an explicit handoff.

## Versioned trust contracts

The published [context-envelope schema](contracts/context-envelope.schema.json)
defines the portable v3 JSON shape. Each property records origin/time, trust,
canonical SHA-256 coverage, scope/objective/policy identity, retention/expiry,
sensitivity/redaction, transformations and producers, and property-specific
validation evidence. The published
[handoff/review schema](contracts/handoff-review.schema.json) defines the
portable objective, input, artifact, acceptance, policy/model, actor, and
evidence-reference shape.

JSON Schema validates document structure; it does not compare actor identities,
recompute digests, consult current policy/model versions, or compare timestamps
with a trusted clock. The repository's plugin composition checker pins the
exact published schema bytes and runs strict typed evaluators with explicit
clock and expected-version options. Context validation timestamps must follow
retrieval and every recorded transformation, and canonical calendar timestamps
are checked without date normalization. Those evaluators reject duplicate
context properties, incomplete integrity coverage, stale data, unredacted
secrets, self-review, reference mismatches, and model-transformed data presented
as validated without property-matched deterministic evidence. Property names
must match their containing property in every validation state, including
untrusted, invalid, and unvalidated records. Contract publication reads bind
the opened file identity and compare every ancestor identity before and after
the read. Descriptor metadata is compared around two bounded positioned reads,
so transient hardlinks and in-place rewrites fail even if the final pathname is
restored. Device, inode, link, size, and nanosecond timestamps remain bigint
throughout; supported runtimes must expose exact bigint stats or validation
fails closed. Handoff acceptance references must equal the exact repository-local
reference supplied by trusted evaluator options; this is a local composition
identity, not a global registry. The canonical
public [trust-boundary incident-regression corpus](fixtures/trust-boundary-incidents.json)
contains valid controls plus executable mutations and stable rejection codes.
It is implementation-visible regression input, not independent or private
acceptance material.

Published contract assets are bounded to 1 MiB. Composition rejects duplicate
JSON object keys by decoded identity before `JSON.parse`, including collisions
between literal and Unicode-escaped key spellings.

Neither the published schemas nor the repository evaluator intercept native
Codex handoffs, attest that a host supplied truthful facts, or enforce the host
lifecycle. Native integration must collect trusted facts and invoke a
deterministic consumer explicitly.
