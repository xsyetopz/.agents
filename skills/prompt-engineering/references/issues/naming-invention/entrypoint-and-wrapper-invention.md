# Entrypoint And Wrapper Invention

**ID**: `entrypoint-and-wrapper-invention` | **Category**: `naming-invention`

## Trigger

Use when: the agent adds extra scripts, wrappers, or command entrypoints because they are common in repositories rather than required by the product.

## Bad forms — what this looks like

- ❌ Adding `.sh` because repositories often have shell installers.
- ❌ Adding `render`, `verify`, or `eval` scripts because the verbs exist in the lifecycle.
- ❌ `Calling command proliferation "thin wrappers" as if that removes the maintenance cost.`
- ❌ `"Optional wrapper" without a concrete caller.`

## Required behavior

```text
Before proposing an entrypoint or wrapper, the agent must identify: 1. who calls it, 2. what runtime executes it, 3. why an existi
```

## Concrete example

- The agent proposed both `install.ps1` and `install.sh` without a distribution requirement that could not run PowerShell.

**✅ CORRECT** (shortest path):

```text
Before proposing an entrypoint or wrapper, the agent must identify: 1. who calls it, 2. what runtime executes it, 3. why an existi
```

## Acceptance check

Every proposed script has a named caller, delegated source path, test route, and platform reason. Otherwise it is not included in the tree.

## Efficiency note

- **Evidence path**: Inspect enough current evidence to prove the role, reach, and requested outcome; expand when findings conflict or risk requires it.
- **No overthinking**: Pattern obvious? State it and move on.
- **Cut to the chase**: Skip narration, self-analysis, process logging.
