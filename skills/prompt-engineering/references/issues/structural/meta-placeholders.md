# Structural Meta-Issues

**Merged from**: `authorization-scope-and-control-failures`, `code-completeness-and-lazy-execution`, `conclusion-smuggling-and-decision-framing`, `engineering-rigor-and-root-cause-analysis`, `project-lifecycle-scope-and-architecture`, `proposal-churn-user-policing-burden`, `referent-scope-and-ownership-smuggling`, `scope-execution-and-artifact-role-confusion`, `srp-dry-and-scope-collapse`
**Category**: `structural`

## Trigger patterns

- Use when: extracting a specific assistant-behavior failure mode, guardrail, or acceptance criterion.
- Use when: the agent repeatedly emits shallow or partially grounded proposals that force the user to identify each obvious flaw.

## Bad forms — what this looks like

- ❌ `Incremental "fixed" trees that repeat the same unsupported naming behavior.`
- ❌ `Asking the user to discover each invented artifact one by one.`
- ❌ `Replacing one generic taxonomy with another generic taxonomy.`
- ❌ `Confidently naming artifacts before doing the authority pass.`

## Required behavior

```text
Before proposing architecture after corrections, the agent must: 1. collect the accepted constraints, 2. collect rejected patterns
```

## Concrete example

### Duplicate Artifact Creation Before Fit Check ```diff - The assistant creates a new issue, section, route, or artifact before checking whether an existing one already owns the concept

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Before proposing architecture after corrections, the agent must: 1. collect the accepted constraints, 2. collect rejected patterns
```

## Acceptance checks

- The user can review the proposal for product tradeoffs rather than first correcting preventable invented files, wrappers, and categories.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
