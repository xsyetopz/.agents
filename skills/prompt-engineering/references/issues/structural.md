# Structural Cases

**Category:** `structural`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="coverage-map-before-deletion-readiness"></a>

## coverage-map-before-deletion-readiness

**ID**: `coverage-map-before-deletion-readiness` | **Category**: `structural`

### Trigger

Use when: the agent is asked to make example/source repositories deletable, portable, fully covered, or absorbed into another repo, but starts implementation before proving source-to-current coverage.

### Observed failure

- ❌ `Starting generator edits before a coverage map.`
- ❌ `Copying only familiar config files from example repos.`
- ❌ `Saying coverage is full because the obvious files were moved.`
- ❌ `Treating source repo deletion as safe without mapping generated output and validation.`

### Required behavior

```text
For deletion-readiness work, first build a coverage map that names: source artifact, current local owner, generator or source-of-t
```

### Example

- A user says three template/config repos should become deletable, and the agent edits a generator before listing every artifact from those repos.

**✅ CORRECT** (shortest path):

```text
For deletion-readiness work, first build a coverage map that names: source artifact, current local owner, generator or source-of-t
```

### Acceptance check

Before editing or reporting deletion readiness, the agent can show a source-to-current coverage matrix with no unexamined source artifacts and with validation or an explicit gap for each row.

<a id="meta-placeholders"></a>

## meta-placeholders

**ID**: `meta-placeholders`

**Merged from**: `authorization-scope-and-control-failures`, `code-completeness-and-lazy-execution`, `conclusion-smuggling-and-decision-framing`, `engineering-rigor-and-root-cause-analysis`, `project-lifecycle-scope-and-architecture`, `proposal-churn-user-policing-burden`, `referent-scope-and-ownership-smuggling`, `scope-execution-and-artifact-role-confusion`, `srp-dry-and-scope-collapse`
**Category**: `structural`

### Trigger

- Use when: extracting a specific assistant-behavior failure mode, guardrail, or acceptance criterion.
- Use when: the agent repeatedly emits proposals with unsupported details that require additional correction.

### Observed failure

- ❌ `Incremental "fixed" trees that repeat the same unsupported naming behavior.`
- ❌ `Asking the user to discover each invented artifact one by one.`
- ❌ `Replacing one generic taxonomy with another generic taxonomy.`
- ❌ `Confidently naming artifacts before doing the authority pass.`

### Required behavior

```text
Before proposing architecture after corrections, the agent must: 1. collect the accepted constraints, 2. collect rejected patterns
```

### Example

#### Duplicate Artifact Creation Before Fit Check ```diff - The assistant creates a new issue, section, route, or artifact before checking whether an existing one already owns the concept

**✅ CORRECT** (shortest path, minimal tool calls):

```text
Before proposing architecture after corrections, the agent must: 1. collect the accepted constraints, 2. collect rejected patterns
```

### Acceptance check

- The user can review the proposal for product tradeoffs rather than first correcting preventable invented files, wrappers, and categories.

<a id="responsibility-split-before-scale"></a>

## responsibility-split-before-scale

**ID**: `responsibility-split-before-scale` | **Category**: `structural`

### Trigger

Use when: the agent keeps adding behavior to already-large modules, CLIs, renderers, generators, or config files during a broad expansion instead of first separating responsibilities.

### Observed failure

- ❌ `Adding more renderer logic to an already oversized CLI file.`
- ❌ `Combining comparison, design, migration, and validation in one edit loop.`
- ❌ `Using one core module for parsing, rendering, file IO, validation, and reporting.`
- ❌ `Deferring the split until after another broad feature pass.`

### Required behavior

```text
Before broadening an already-large artifact, identify its current responsibilities, callers, inputs, outputs, and validation reach
```

### Example

- A template generator CLI already contains parsing and rendering, and the agent adds multiple language presets there instead of splitting renderer ownership.

**✅ CORRECT** (shortest path):

```text
Before broadening an already-large artifact, identify its current responsibilities, callers, inputs, outputs, and validation reach
```

### Acceptance check

New broad-scope behavior lands in a file whose responsibility is named and bounded, or the agent reports that a split is needed before more implementation. Large multipurpose files are not expanded further without explicit authorization and a stated reason.

## References

- [Issue corpus index](../issue-corpus-index.md)
- [Official source records](../official-sources.md)
