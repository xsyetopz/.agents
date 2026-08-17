# Prompt workflow

Use this reference to revise an existing prompt after a behavior failure has been observed or a prompt change has been explicitly requested.

## Find the owning surface

Read the full prompt that owns the behavior. Then inspect the layers that can override or consume it: higher-priority instructions, repository policy, tool descriptions, examples, runtime injection, and output formatting. Record conflicts instead of copying the same rule into every layer.

A prompt path is not automatically source authority. Establish who produces it, whether it is generated, where it is loaded, and which agent or product surface consumes it.

## Ground the diagnosis

Use the smallest relevant exchange or rollout. Identify:

- what the user asked;
- what effects were authorized;
- what the agent observed before acting;
- what unsupported inference it made;
- what it did or failed to do;
- what response or effect would have satisfied the request.

Keep quoted user judgments separate from technical findings. Do not create a new issue type, registry row, or schema for every wording variant of the same behavior.

## Rewrite the owner

Prefer concrete instructions with an observable trigger and action:

- “If the user asks why an artifact exists, inspect and answer without editing.”
- “If the requested file is absent, report it; do not choose a substitute.”
- “Before removing a script, trace callers, inputs, outputs, side effects, and uncovered behavior.”
- “After a correction, use the corrected term and remove the rejected assumption.”

State each rule once. Remove conflicts, vague moral language, duplicated warnings, and examples that do not address a measured gap. Do not request private chain-of-thought. Require visible evidence, decisions, and results instead.

Preserve the requested artifact category. Prompt work must not turn a code request into documentation, a test request into a checklist, or runtime proof into a prose scan.

## Route tools and models

For each tool that the agent can use, define when it applies, what input it needs, what evidence it returns, what effect it may cause, when approval is required, and when to stop. Do not expose irrelevant tools merely because they are available.

When a request names a model or provider, use a current first-party source for exact identifiers, controls, and limits. Treat stored snapshots as dated evidence. Do not infer one model's behavior from another member of a family, and do not silently replace an unavailable selector or effort level.

## Keep implementation and verification honest

Prompt prose cannot repair a runtime defect. If the tool contract, event path, parser, or product state causes the failure, report the runtime owner and route the fix there.

Do not add a script whose main purpose is checking agent wording, headings, labels, or document presence. Use behavioral evaluation for agent behavior and the repository's existing structural checker for package structure.
