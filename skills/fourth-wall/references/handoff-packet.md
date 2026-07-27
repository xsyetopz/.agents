# Context renewal and warm handoff

Use this reference when accumulated context is harming speed or clarity, ownership changes, or an agent can no longer continue reliably. It is for roots coordinating a sibling replacement and for outgoing owners preparing operational state. Do not hand off merely to avoid summarizing ordinary progress.

The packet must let a successor resume the same outcome without inheriting a transcript or guessing about ownership, routing, and acceptance state.

## Compact packet

Include only operational state:

```md
## Objective
The full outcome still being pursued.

## Ownership
Current task paths, roles, and file or system boundaries.

## Established State
Completed changes, decisions, commits or artifacts, and validation evidence.

## Constraints
User decisions, architecture boundaries, relevant skills, and known hazards.

## Open Work
Unfinished items, valid blockers, dependencies, and remaining gates.

## Next Action
The first concrete action the successor should take.

## Routing State
The active owner and route, any bounded capability adjustment reason, and the
path to `routing-decisions.jsonl` beside this packet.
```

Do not include motivational framing, a chronological transcript, stable base instructions, or facts the successor can cheaply inspect.

For a long root task, store this packet under `/tmp` and pass its path to children together with a compact slice-specific assignment or follow-up. Update it at ownership transfers, material routing changes, and acceptance checkpoints. Do not automate encrypted spawn-message rewriting or continuously append command output.

## Worker or specialist handoff

Use a parent-mediated sibling replacement so the root preserves the task graph and role boundary:

1. The outgoing task sends the packet to the root with `send_message` and stops taking new ownership.
2. The root inspects the packet and current tree.
3. The root spawns a fresh sibling named `<role>__<objective>`, passes explicit model/reasoning controls, sets the matching native `agent_type` and names the behavioral role in its handoff, and chooses the smallest useful bounded history fork.
4. The root confirms the successor exists and has the right ownership boundary.
5. The predecessor returns or is interrupted only after the successor is established.

Prefer no-history forks. Quote the relevant completed decisions in the handoff packet or point to a durable artifact instead of relying on inherited execution history.

## Reactivation or replacement

Use `followup_task` when a completed child remains the right owner and its accumulated context reduces rediscovery; current native MultiAgentV2 preserves its original model and reasoning settings but cannot change them. Spawn a fresh sibling when the next action benefits from independent judgment, a clean context, changed ownership, or a recorded capability increase. Use the smallest useful positive fork plus the packet so the successor retains relevant knowledge without inheriting an unbounded transcript.

## Root handoff limitation

MultiAgentV2 cannot promote a child into the top-level root or archive and replace the root atomically. If the root itself needs renewal:

1. Produce an orchestrator packet containing the overall objective, live task tree, ownership, decisions, evidence, gates, and next action.
2. Start a new top-level Desktop task through a user- or app-level thread operation.
3. Give the replacement the packet and the relevant workspace.
4. Confirm continuity before retiring the old root.

Native task messaging applies only inside one root tree. Crossing between unrelated top-level tasks requires app-level thread coordination, not MultiAgentV2 task tools.
