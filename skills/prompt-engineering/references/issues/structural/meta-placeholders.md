# Structural Meta-Issues

**Merged from**: `authorization-scope-and-control-failures`, `code-completeness-and-lazy-execution`, `conclusion-smuggling-and-decision-framing`, `engineering-rigor-and-root-cause-analysis`, `project-lifecycle-scope-and-architecture`, `proposal-churn-user-policing-burden`, `referent-scope-and-ownership-smuggling`, `scope-execution-and-artifact-role-confusion`, `srp-dry-and-scope-collapse`
**Category**: `structural`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

- Use when: extracting a specific assistant-behavior failure mode, guardrail, or acceptance criterion.
- Use when: the agent repeatedly emits shallow or partially grounded proposals that force the user to identify each obvious flaw.

## Observed failure

- ❌ `Incremental "fixed" trees that repeat the same unsupported naming behavior.`
- ❌ `Asking the user to discover each invented artifact one by one.`
- ❌ `Replacing one generic taxonomy with another generic taxonomy.`
- ❌ `Confidently naming artifacts before doing the authority pass.`

## Required behavior

```text
Before proposing architecture after corrections, the agent must: 1. collect the accepted constraints, 2. collect rejected patterns
```

## Example

### Duplicate Artifact Creation Before Fit Check ```diff - The assistant creates a new issue, section, route, or artifact before checking whether an existing one already owns the concept

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Before proposing architecture after corrections, the agent must: 1. collect the accepted constraints, 2. collect rejected patterns
```

## Acceptance check

- The user can review the proposal for product tradeoffs rather than first correcting preventable invented files, wrappers, and categories.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
