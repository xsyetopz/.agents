---
name: apple-design-hig
description: >
  Use when designing, implementing, or auditing Apple-platform UI and UX against the current Human Interface Guidelines. Covers iOS, iPadOS, macOS, tvOS, visionOS, watchOS, games, accessibility, VoiceOver, Dynamic Type, layout, navigation, windows, menus, controls, forms, sheets, popovers, typography, color, materials, motion, haptics, SF Symbols, widgets, notifications, onboarding, privacy, and platform conventions. Trigger phrases include Apple HIG, Human Interface Guidelines, iPhone design, iPad layout, Mac app, spatial UI, watch interaction, tvOS focus, Apple accessibility, system component, and native Apple experience. Distinguish design guidance from SDK, API, entitlement, and implementation contracts.
---

# Apple Design HIG

Apply current Apple design guidance to a concrete interface decision and show the
source-to-decision trace. The live HIG is authoritative; bundled references are
an offline discovery index, not proof that guidance is current.

## When to use

- Designing or reviewing an Apple-platform screen, flow, component, or system experience
- Choosing native navigation, presentation, input, menu, window, or feedback patterns
- Auditing accessibility, adaptation, layout, typography, color, motion, or interaction
- Comparing conventions across Apple platforms and device classes

## When NOT to use

- Swift or SwiftUI API correctness without a design question
- App Store policy, entitlement, provisioning, privacy-manifest, or legal advice
- Generic web or cross-platform UI with no Apple-specific decision

## Source authority

1. Check the live Apple Human Interface Guidelines.
2. Use references/index.md and topic files to locate relevant concepts.
3. Verify material guidance live before presenting it as current.
4. Label SDK behavior, accessibility implementation requirements, and inferred design judgment separately from HIG recommendations.

## Non-negotiables

- Cite the exact live HIG page supporting each material recommendation.
- Resolve platform, device class, input method, and accessibility context first.
- Prefer system components unless a documented product need justifies deviation.
- Treat accessibility as part of the interaction contract.
- Do not invent Apple rules or convert advice into an API requirement.

## Workflow

1. State the interface decision and platform contexts.
2. Inspect the existing UI and constraints when present.
3. Load only relevant platform, foundation, pattern, and component references.
4. Verify current live HIG guidance.
5. Produce the recommendation, rejected alternatives, accessibility effects, and implementation implications.
6. If files change, validate the real interface at relevant sizes, input modes, appearances, and accessibility settings.

## Quick start

Load references/design-principles.md, the target platform file, the relevant
pattern/component file, and accessibility references when interaction or content
changes.

## Reference map

| Need | Load |
|---|---|
| Complete topic index | references/index.md |
| Foundations | references/foundations.md, references/design-principles.md |
| Platform adaptation | references/designing-for-ios.md and the matching platform file |
| Layout, type, color, motion | references/layout.md, references/typography.md, references/color.md, references/motion.md |
| Navigation and presentation | references/navigation-and-search.md, references/presentation.md, references/modality.md |
| Accessibility | references/accessibility.md, references/voiceover.md, references/inclusion.md |
| Components and inputs | references/components.md, references/controls.md, references/inputs.md |
| Audit procedure | references/workflow.md |

## Completion

A complete result names platform context, cites current HIG guidance, separates
recommendation from implementation contract, covers accessibility, and verifies
any changed interface rather than stopping at prose.

## Related skills

- swiftui-pro for SwiftUI implementation review
- impeccable for broader product-interface refinement
- design-proof-gate for screenshot-backed visual acceptance
