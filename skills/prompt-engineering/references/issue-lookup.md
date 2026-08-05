# Issue Lookup

## Use this reference

Use this table to select one failure category from observed behavior. Then open
the exact case through references/issue-corpus-index.md. Do not load all issue
files or route solely from complaint wording.

| Observed behavior | Category |
|---|---|
| invents layers, categories, models, or namespaces after correction | abstract-reframing |
| edits or dismisses an artifact before tracing callers and effects | artifact-role-confusion |
| echoes a complaint or treats its label as established fact | complaint-mirroring |
| promises deletion or cleanup before ownership/behavior accounting | deletion-cleanup |
| works on docs, snapshots, or harnesses instead of the product outcome | docs-orbit |
| confuses memory, current context, account state, or source state | memory-state |
| invents files, roles, entrypoints, or compatibility surfaces | naming-invention |
| says something is universally needed or useless without evaluation | need-claims |
| bypasses the named prompt, source, or native workflow | prompt-boundary |
| leaks prompt scaffolding or stated traits into output | prompt-psychology |
| turns style or tone commentary into the purpose of technical work | prose-policing |
| converts diagnosis, criticism, or context into mutation authority | scope-consent |
| deletes, bypasses, or reframes tooling before tracing its contract | script-tool-evasion |
| lets stale examples or invented artifacts override canonical evidence | source-truth |
| decomposes by category or fills placeholders before ownership is proved | structural |
| replaces the answer with apology, agreement, or self-narration | tone-meta |

## Selection rules

1. Select from observable effects and final-answer content, not assumed internal
   reasoning.
2. Prefer one narrow case; add a second only when it tests a distinct effect.
3. Preserve the original task and authority boundary in the evaluation.
4. Use natural prompts that do not name the category or expected correction.
5. Inspect tool/filesystem effects separately from the final answer.
6. Retire redundant or non-reproducing cases instead of accumulating aliases.
