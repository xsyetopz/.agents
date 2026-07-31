# Named README Workflow Bypass

**ID**: `named-readme-workflow-bypass` | **Category**: `prompt-boundary`

## Trigger

Use when: the user names a README, template, generator workflow, or external guide as the authority, but the agent inspects unrelated files, copies or hand-rolls scaffold, runs unrelated checks, or substitutes its own workflow instead of following the named source literally.

## Bad forms — what this looks like

- ❌ `Reading template internals after being told to read only README.md.`
- ❌ `Manually creating a scaffold when the README documents a generator command.`
- ❌ `Running checks in the template repo when the user asked to use the workflow on a different repo.`
- ❌ `Treating 'use this README' as permission to copy files.`
- ❌ `Treating a correction as permission to start writing files.`

## Required behavior

```text
When the user names a README or guide, read that source before inspecting adjacent files unless the source itself directs further
Respect explicit bounds such as "read only the README", "do not copy files", or "use the generator workflow".
Identify the authoritative workflow described by the source before acting.
Preserve the requested artifact category: generator workflow means run the generator, not hand-roll equivalent files; read means r
Do not run extra checks, create files, or inspect generated output unless the user asked or the documented workflow requires it fo
```

## Concrete example

- User points to a Rust template README for workspace setup; the agent inspects template Cargo files instead of reading the README.

**✅ CORRECT** (shortest path):

```text
When the user names a README or guide, read that source before inspecting adjacent files unless the source itself directs further
Respect explicit bounds such as "read only the README", "do not copy files", or "use the generator workflow".
Identify the authoritative workflow described by the source before acting.
```

## Acceptance check

The action trace starts with the named source, not adjacent artifacts. Every command or edit is either directly requested by the user or required by the named workflow for the target repo. No copied template files, manual scaffold, unrelated validation, or internal-template inspection appears when the user constrained the source to the README.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
