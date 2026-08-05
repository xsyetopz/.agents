# Official OpenAI GPT-5.6 Prompting Guidance

## Use this reference

Load this reference when openai gpt 5.6 is material to a measured prompt or agent-behavior failure. Apply current provider guidance first, state each instruction once, and verify observable effects separately from the final answer.

Retrieved 2026-08-05 from current official OpenAI documentation:

- https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6
- https://developers.openai.com/api/docs/guides/prompt-engineering#coding

The live OpenAI pages are canonical. Re-fetch them before a new model-specific
change; this file is an auditable local snapshot of the clauses applied by this
skill.

## Clause matrix

| ID | Official guidance | Required skill behavior | Audit |
|---|---|---|---|
| OAI-LEAN-1 | Favor leaner prompts. | Remove repetition and irrelevant tools/examples. | Prompt-size and duplicate-policy audit. |
| OAI-LEAN-2 | Remove one instruction/example/tool group at a time and rerun the same evals. | Use paired baseline/candidate ablations. | Live rollout audit records identical cases. |
| OAI-LEAN-3 | State each instruction once. | Keep autonomy and approval in one section. | Structural section audit. |
| OAI-TOOLS-1 | Expose only relevant tools with concise, precise descriptions. | Tool inventory and schemas are task-specific. | Tool-surface review. |
| OAI-EXAMPLE-1 | Keep examples/style for product requirements or measured gaps. | Examples are conditional, not a default. | Every example maps to evidence. |
| OAI-CONTEXT-1 | Track context as sessions grow. | Measure prompt/tool growth and repeated content. | Context-size audit. |
| OAI-AUTH-1 | Read-only requests inspect and report; implementation requires a change request. | One compact read/change boundary. | No-write live cases. |
| OAI-AUTH-2 | Change/build/fix requests make in-scope local changes and validate without asking. | Preserve safe local autonomy. | Required-write live control. |
| OAI-AUTH-3 | Confirm external, destructive, costly, or scope-expanding actions. | One consequential-action boundary. | Static and adversarial cases. |
| OAI-STYLE-1 | Broad brevity instructions may over-shorten. | Specify required facts and omissions. | Final-answer rubric. |
| OAI-STYLE-2 | Use `text.verbosity` for API default detail. | Keep API control separate from task content. | API configuration review. |
| OAI-TONE-1 | Describe writing choices, not broad tone labels. | Direct answer, specific acknowledgement, relevant reassurance only. | Answer-quality rubric. |
| OAI-PRO-1 | Keep standard/pro prompts outcome-focused; do not say “think harder.” | Same requirements across modes. | Forbidden-claim audit. |
| OAI-PRO-2 | Compare quality, tokens, latency, and cost on the same tasks. | Quality gates resource gains. | Paired evaluation report. |
| OAI-PTC-1 | Use PTC for bounded predictable reductions, not merely multiple calls. | Task-specific routing and handoff. | Tool-route audit. |
| OAI-PTC-2 | Specify tools, schema, evidence, concurrency, retries, stops, and direct work. | Complete orchestration contract. | Contract audit. |
| OAI-PTC-3 | Test program output and final assistant message separately. | Separate effect and answer oracles. | Behavioral test harness. |
| OAI-CODE-1 | Define the software-agent role and structured tool use. | Role and workflow are explicit. | Prompt structure audit. |
| OAI-CODE-2 | Require thorough correctness tests and verify patches. | Inspect resulting files/diffs after edit tools. | Required-write live control. |
| OAI-CODE-3 | Use clean semantic Markdown. | Output requirements name needed structure. | Final-answer inspection. |
| OAI-AGENT-1 | Resolve the full task, with notable tool preambles and progress tracking when useful. | Completion and planning scale to task size. | Long-task cases; no universal TODO requirement. |

## Compact autonomy policy

OpenAI recommends a compact policy equivalent to:

```text
For requests to answer, explain, review, diagnose, or plan, inspect relevant
materials and report. Do not implement unless the request also asks.

For requests to change, build, or fix, make the requested in-scope local changes
and run relevant non-destructive validation without asking.

Require confirmation for external writes, destructive actions, purchases, or
material scope expansion.
```

Keep this policy in one place. Repetition can cause unnecessary approvals.

## Evaluation rule

Static wording checks detect drift; they do not prove model behavior. The live
audit must execute the installed Codex binary in disposable fixtures using
natural prompts, independently inspect tool/filesystem effects, and inspect the
final answer. Missing Codex, authentication failure, timeout, or malformed
output is a failed audit, not a skip.
