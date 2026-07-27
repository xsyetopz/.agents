# Delegation contract

Use this reference when a root, or an eligible depth-1 Worker, prepares consequential delegated work. It converts an orchestration decision into a bounded assignment that the recipient can execute without reconstructing the parent's reasoning.

The handoff must preserve the top-level outcome while naming one complete ownership slice and its acceptance evidence.

## Before spawning

Define:

1. **Outcome:** the observable state this task must produce.
2. **Ownership:** files, modules, services, or product surface this task owns.
3. **Dependencies:** inputs that must already exist and downstream tasks waiting on this result.
4. **Constraints:** user decisions, architecture boundaries, relevant skills, and forbidden scope changes.
5. **Evidence:** exact checks, artifacts, screenshots, or source inspection expected at completion.
6. **Return shape:** changed areas, validation performed, unresolved risks, and the next recommended action.

## Complete-slice test

Prefer a handoff that gives one child the complete causal loop: inspect the owned surface, implement the change, run focused validation, correct in-scope failures, and collect relevant runtime proof. A code-only handoff is too narrow when it predictably leaves the root with the longer test, integration, or proof campaign.

Keep shared Git mutations and final acceptance at the root. When parallel edits prevent lock-heavy checks, defer those checks until the tree stabilizes, then dispatch one integration Worker, Review, or QA leaf with the complete serial command or piloting contract.

## Spawn shape

Encode the role and objective in the task name; carry capability explicitly:

```json
{
  "task_name": "worker__backend_contract",
  "fork_turns": "1",
  "agent_type": "worker",
  "model": "gpt-5.6-luna",
  "reasoning_effort": "high",
  "message": "You are dispatched as a Scoped Worker. Own the bounded backend contract through implementation, focused validation, in-scope fixes, and compact evidence..."
}
```

Complexity and horizon select model, effort, and fork depth; the role selects behavior. Under the Skizzles profile, set the matching native `agent_type`; under native instructions, set it only when the active schema advertises that role. Name the route and role in the message and pass explicit model and reasoning overrides from the active tool schema. The installed role config already supplies the shared subagent base plus role-specific developer instructions, so repeat only assignment-specific constraints.

## Worker grandchildren

A depth-1 Terra/Sol Worker may dispatch at most one active bounded Worker when all of these hold:

- The child is named `worker__...` and uses Luna high when available or Terra medium as the bounded fallback.
- The slice is small, disjoint from the parent's continuing edits, and comfortably short-context.
- The child owns inspection, implementation, focused validation, in-scope fixes, and completion evidence together.
- The parent has genuinely independent implementation to continue while the child works.
- The child uses `fork_turns = "none"`, remains a leaf, and may be reactivated only for coherent follow-on work within the same ownership boundary.

Do not create a command runner by another name. If the parent must interpret every result or modify the same surface before validation is meaningful, keep that loop with the parent. Non-Worker roles return delegation proposals to the root.

Include directly relevant skill names and obligations in the message. Skills available to the parent are not a substitute for telling the recipient which domain contract governs its work.

## Fan-out test

Spawn tasks in parallel only when all are true:

- Each owns a coherent responsibility boundary.
- Their write sets are disjoint or explicitly sequenced.
- Each can make meaningful progress without waiting for another spawned task.
- The root can continue useful cross-slice decisions, integration inspection, or planning without duplicating delegated execution.
- The expected speed or quality gain exceeds coordination cost.

Prefer dependency order over maximum concurrency. Contracts, schemas, and shared interfaces usually stabilize before broad implementation fan-out.

## Blockers

A valid blocker identifies one of:

- An unavailable external dependency or environment.
- Contradictory requirements.
- A safety boundary that forbids the required action.
- A product or architecture decision only the owner can make.

Task size, difficult code, uncertainty, failing tests, or the need for more investigation are not blockers by themselves.

## Completion claim

Require the task to report:

- What changed and where.
- What behavior is now true.
- What validation ran and its result.
- What did not run and why.
- Remaining risks, decisions, or downstream work.

The root verifies this claim before integration or completion.

Completion releases active ownership but does not destroy the child. Use `followup_task` for reviewer-directed corrections or coherent next work by the same owner at its current capability. Classify review findings before treating them as routing evidence: an explicit-contract miss is attributable rework, an adjacent existing defect is healing rather than failure, and a newly discovered invariant requires clarification rather than blame. Use a fresh task with a compact handoff when independent judgment, context reset, changed ownership, or a recorded higher route is required.

When a durable `/tmp` task packet exists, pass its path rather than repeating stable cross-task context. The spawn message must still contain the child's selected route, role, concrete objective, ownership, constraints, and expected proof so the packet supplements rather than hides the assignment. Do not put secrets, raw transcripts, or unbounded build logs in the packet.
