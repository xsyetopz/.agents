# Coverage Map Before Deletion Readiness

**ID**: `coverage-map-before-deletion-readiness` | **Category**: `structural`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent is asked to make example/source repositories deletable, portable, fully covered, or absorbed into another repo, but starts implementation before proving source-to-current coverage.

## Observed failure

- ❌ `Starting generator edits before a coverage map.`
- ❌ `Copying only familiar config files from example repos.`
- ❌ `Saying coverage is full because the obvious files were moved.`
- ❌ `Treating source repo deletion as safe without mapping generated output and validation.`

## Required behavior

```text
For deletion-readiness work, first build a coverage map that names: source artifact, current local owner, generator or source-of-t
```

## Example

- A user says three template/config repos should become deletable, and the agent edits a generator before listing every artifact from those repos.

**✅ CORRECT** (shortest path):

```text
For deletion-readiness work, first build a coverage map that names: source artifact, current local owner, generator or source-of-t
```

## Acceptance check

Before editing or reporting deletion readiness, the agent can show a source-to-current coverage matrix with no unexamined source artifacts and with validation or an explicit gap for each row.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
