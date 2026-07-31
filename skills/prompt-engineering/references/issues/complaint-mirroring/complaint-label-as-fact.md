# Complaint Label as Fact

**Merged from**: `complaint-label-as-evidence`, `complaint-term-to-product-claim`
**Category**: `complaint-mirroring`

## Trigger patterns

- Use when: the agent adopts a user's critical wording as a factual artifact classification before inspecting the artifact.
- Use when: the agent converts a user's complaint term into an asserted product fact, then proposes edits from that asserted fact.

## Required behavior

```text
Quote or paraphrase the complaint only as user input, not as artifact fact.
Inspect the artifact before naming its role.
Trace callers, commands, tests, docs, generated output, filesystem writes, install reach, and ownership.
State observed behavior before proposing edits.
Separate artifact role, defect, and patch.
If the artifact should be removed, remove stale references and replacement copies in the same change.
```

## Concrete example

The assistant treated a charged complaint label as the artifact's observed role

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Quote or paraphrase the complaint only as user input, not as artifact fact.
Inspect the artifact before naming its role.
Trace callers, commands, tests, docs, generated output, filesystem writes, install reach, and ownership.
```

## Acceptance checks

- - Artifact-role answers cite observed inputs, outputs, callers, writes, ownership, and install reach. - User complaint labels are not reused as factual classifications unless inspection confirms them. - Removal commits do not leave stale references. - The same rejected behavior is not recreated under a new name. - Final reports separate what was observed from what changed.
- - User wording is not copied into product claims without evidence. - Universal need claims do not appear before caller and reach accounting. - Removal proposals include behavior accounting and reference cleanup. - Final reports separate user criticism, observed artifact behavior, changed files, command evidence, and remaining unverified claims.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
