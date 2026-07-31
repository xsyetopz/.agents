---
name: apple-design-hig
description: Use when designing or auditing Apple-platform UI, UX, interaction, accessibility, typography, layout, color, motion, components, inputs, or system experiences across iOS, iPadOS, macOS, tvOS, visionOS, watchOS, and games. Check the live HIG and cite exact guidance; distinguish HIG recommendations from SDK, API, entitlement, and accessibility implementation contracts.
---

# Apple Design HIG

Navigate Apple's living Human Interface Guidelines (HIG). The live documentation
at `developer.apple.com/design/human-interface-guidelines/` is the source of
truth; the bundled Markdown corpus in `references/` is a reproducible reading
copy for offline discovery and analysis.

## When to use

- Designing new Apple-platform UI or UX
- Auditing existing UI against HIG
- Choosing between system components (sheets, popovers, toolbars, etc.)
- Resolving platform-specific design questions (iOS vs. macOS vs. visionOS)
- Checking accessibility, Dynamic Type, dark mode, localization, or layout requirements

## When NOT to use

- Implementing APIs or checking SDK availability — link to Apple Developer docs instead
- Choosing third-party libraries or frameworks
- General UI design not targeting Apple platforms

## Non-negotiables

- Identify target platform(s), OS release, device context, and input model before selecting guidance.
- Start discovery in `references/index.md`. Read **Platform considerations**, **Specifications**, and **Change log** when present.
- Separate HIG guidance from implementation contracts. For APIs, entitlements, or accessibility behavior, follow the linked Apple Developer docs.
- When citing: **Apple HIG — _Page title_** (retrieved YYYY-MM-DD): _paraphrased rule_. Link the canonical URL.
- Call out conflicts, legacy terminology, redirects, and unavailable pages. Memory or an old snapshot is not current evidence.

## Quick start

1. **Frame**: platform, OS version, device, input, content type, accessibility needs.
2. **Find**: read `references/index.md`, search by title, check `references/whats-new.md`.
3. **Check**: compare local reference against the live Apple URL for version-sensitive claims.
4. **Resolve**: check accessibility, Dynamic Type, localization, dark mode, safe areas, multitasking.
5. **Map**: prefer system components, SF Symbols, system typography, adaptive layout.
6. **Deliver**: state decision, rationale, platform differences, verification checklist.

Full workflow detail: [references/workflow.md](references/workflow.md).

## Reference map

| If you need to... | Load |
|---|---|
| Start discovery | `references/index.md` |
| Find a specific component/pattern | `references/<slug>.md` (match URL slug) |
| See recent HIG changes | `references/whats-new.md` |
| Full workflow detail | `references/workflow.md` |

## Related skills

None — this skill is self-contained.

## Maintenance

```sh
python3 scripts/harvest_hig.py harvest   # refresh reference corpus
python3 scripts/harvest_hig.py validate  # check integrity
```
