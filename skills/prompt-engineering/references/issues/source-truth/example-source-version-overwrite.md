# Example Source Version Overwrite

**ID**: `example-source-version-overwrite` | **Category**: `source-truth`

## Trigger

Use when: the agent treats a version, dependency ref, standard, config value, or generated setting from an example repository as authority to overwrite current local state.

## Bad forms — what this looks like

- ❌ `Changing 1.26.4 to 1.26.3 because an example repo has 1.26.3.`
- ❌ `Treating a sample go.mod, package lock, action ref, model name, or compiler standard as the current desired value.`
- ❌ `Editing generated output without checking the generator owner.`
- ❌ `Downgrading a local value while investigating coverage.`

## Required behavior

```text
Before changing a version-like value, identify whether the source is authoritative, illustrative, stale, generated, user-authored,
```

## Concrete example

- A template repo uses an older language version and the agent copies it over a newer generated value.

**✅ CORRECT** (shortest path):

```text
Before changing a version-like value, identify whether the source is authoritative, illustrative, stale, generated, user-authored,
```

## Acceptance check

Every version/config change is backed by a stated authority trace: source value, current local value, owner, consumer, reach, and reason the change is authorized. Conflicts are reported rather than edited.

## Efficiency note

- **Shortest path**: Verify once, act once.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
