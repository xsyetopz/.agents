# Prose Policing Tooling

**Merged from**: `prose-policing-tooling`, `prose-script-manufacturing`, `executable-prose-governance`
**Category**: `prose-policing`

## Trigger patterns

- Prose Policing Tooling
- Use when: the agent creates a script, command, or installer action whose main purpose is to check wording, document shape, issue labels, or policy phrasing rather than product behavior.
- Use when: the agent creates or preserves scripts, commands, CI jobs, installer actions, generators, or task runners whose main output is policing wording, headings, labels, doc presence, or assistant-authored process rules.

## Bad forms — what this looks like

- ❌ `"I added a script to ensure the docs stay clean."`
- ❌ `"The check passes" when the check only scans prose.`
- ❌ `Wiring a prose checker into install, update, remove, release, or smoke paths.`
- ❌ `Creating a command because it makes the final report look tested.`
- ❌ `Replacing one prose checker with another name after criticism.`
- ❌ `Treating internal issue files as a reason to add executable policy gates.`

## Required behavior

```text
Before adding or keeping executable automation, answer:
What real input does it consume?
What product output or state does it change or validate?
Who calls it?
Does any user-facing install/update/remove path depend on it?
Would a human reading the files catch the same thing without a command?
```

## Concrete example

**User says**: "why is verifiy.mjs even here? nobody needs a prose SCRIPT!"

**❌ Agent (WRONG)**: "I'll remove the verifier script and its references. A script that just polices doc prose is not needed here."

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Before adding or keeping executable automation, answer:
What real input does it consume?
What product output or state does it change or validate?
```

## Acceptance checks

- - Prose-only verifier scripts are removed. - Installer actions perform install lifecycle behavior, not documentation linting. - Release or smoke evidence comes from commands that exercise runtime behavior.
- - New scripts state a concrete behavioral input and output in the owning artifact or tests. - Documentation cleanup does not add commands, gates, generated reports, or installer actions. - Release evidence comes from product behavior checks, not prose-shape checks. - When a prose-only script is found, references are audited before removal.
- Every script, command, CI job, installer action, and generated report has a behavior role that can be stated without mentioning wording, headings, labels, assistant process, or documentation ceremony. If prose review is needed, it stays as review.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
