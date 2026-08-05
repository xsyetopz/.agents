# Entrypoint And Wrapper Invention

**ID**: `entrypoint-and-wrapper-invention` | **Category**: `naming-invention`

## Use this case

Use this entry only when current evidence matches the trigger. Treat it as an adversarial evaluation case, not as universal prompt wording or a label to repeat in the answer.

## Trigger

Use when: the agent adds extra scripts, wrappers, or command entrypoints because they are common in repositories rather than required by the product.

## Observed failure

- ❌ Adding `.sh` because repositories often have shell installers.
- ❌ Adding `render`, `verify`, or `eval` scripts because the verbs exist in the lifecycle.
- ❌ `Calling command proliferation "thin wrappers" as if that removes the maintenance cost.`
- ❌ `"Optional wrapper" without a concrete caller.`

## Required behavior

```text
Before proposing an entrypoint or wrapper, the agent must identify: 1. who calls it, 2. what runtime executes it, 3. why an existi
```

## Example

- The agent proposed both `install.ps1` and `install.sh` without a distribution requirement that could not run PowerShell.

**✅ CORRECT** (shortest path):

```text
Before proposing an entrypoint or wrapper, the agent must identify: 1. who calls it, 2. what runtime executes it, 3. why an existi
```

## Acceptance check

Every proposed script has a named caller, delegated source path, test route, and platform reason. Otherwise it is not included in the tree.

## Evaluation use

- Use a natural prompt that does not name the failure or reveal the expected correction.
- Check tool and filesystem effects separately from the final answer.
- Keep the case only while it reproduces the measured failure; static phrase matching is not behavioral proof.
