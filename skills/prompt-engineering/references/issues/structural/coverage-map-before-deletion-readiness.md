# Coverage Map Before Deletion Readiness

**ID**: `coverage-map-before-deletion-readiness` | **Category**: `structural`

## Trigger

Use when: the agent is asked to make example/source repositories deletable, portable, fully covered, or absorbed into another repo, but starts implementation before proving source-to-current coverage.

## Bad forms — what this looks like

- ❌ `Starting generator edits before a coverage map.`
- ❌ `Copying only familiar config files from example repos.`
- ❌ `Saying coverage is full because the obvious files were moved.`
- ❌ `Treating source repo deletion as safe without mapping generated output and validation.`

## Required behavior

```text
For deletion-readiness work, first build a coverage map that names: source artifact, current local owner, generator or source-of-t
```

## Concrete example

- A user says three template/config repos should become deletable, and the agent edits a generator before listing every artifact from those repos.

**✅ CORRECT** (shortest path):

```text
For deletion-readiness work, first build a coverage map that names: source artifact, current local owner, generator or source-of-t
```

## Acceptance check

Before editing or reporting deletion readiness, the agent can show a source-to-current coverage matrix with no unexamined source artifacts and with validation or an explicit gap for each row.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
