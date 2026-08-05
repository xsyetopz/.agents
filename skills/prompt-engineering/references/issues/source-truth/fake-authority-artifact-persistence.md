# Fake Authority Artifact Persistence

**ID**: `fake-authority-artifact-persistence` | **Category**: `source-truth`

## Trigger

Fake Authority Artifact Persistence

## Required behavior

```text
Stop after the first correction when the artifact class is unclear.
Inspect existing `_stored` material and real external sources before creating authority artifacts.
Do not create a spec, schema, standard, matrix, benchmark, ADR, migration guide, or API contract unless its source basis is an act
If no real source exists, record that absence in docs or plans, not in the authority directory.
Prefer "missing source" or "not yet specified" over filling the gap with plausible structure.
```

## Concrete example

Fake Authority Artifact Persistence

**✅ CORRECT** (shortest path):

```text
Stop after the first correction when the artifact class is unclear.
Inspect existing `_stored` material and real external sources before creating authority artifacts.
Do not create a spec, schema, standard, matrix, benchmark, ADR, migration guide, or API contract unless its source basis is an act
```

## Acceptance check

- Fake authority artifacts are removed. - Remaining authority artifacts either come from real existing sources or are explicitly requested local definitions. - Any new authority artifact cites its concrete source path, external URL, runtime command, or explicit user approval.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
