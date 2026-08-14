---
name: apple-design-hig
description: Apple HIG, native platform UX, accessibility, and cross-device interface decisions; excludes SDK and generic web UX.
---

# Apple Design HIG

Use current Apple Human Interface Guidelines to make an Apple-platform interface decision and record its source.

## Use this skill

- Design or review an iOS, iPadOS, macOS, watchOS, tvOS, or visionOS interface.
- Choose native navigation, presentation, input, feedback, typography, color, motion, or system experiences.
- Check adaptation across devices, input modes, appearances, Dynamic Type, VoiceOver, and other accessibility needs.
- Do not use for Swift, SwiftUI, UIKit, or SDK/API correctness without a design question; App Store policy, entitlements, provisioning, privacy manifests, legal advice; or generic web and cross-platform UX.

## Rules

- Treat the live Apple Human Interface Guidelines as authority; bundled references are an offline index.
- Resolve platform, device class, input method, and accessibility context before recommending a pattern.
- Prefer system components. Justify deviations with a concrete product constraint.
- Separate HIG recommendations, implementation requirements, and inferred design judgment. Do not invent Apple rules or API guarantees.

## Steps

1. State the interface decision, platform context, constraints, and affected users.
2. Inspect the existing interface when one exists.
3. Open the matching platform, foundation, pattern, component, and accessibility references.
4. Verify material guidance against the live HIG and cite exact pages.
5. Recommend a pattern, rejected alternatives, accessibility effects, and implementation implications.
6. If files change, verify relevant sizes, input modes, appearances, and accessibility settings.

## Resources

- Start with the [HIG reference index](references/index.md).
- Foundations: [foundations](references/foundations.md), [design principles](references/design-principles.md), [typography](references/typography.md), [color](references/color.md), and [accessibility](references/accessibility.md).
- Platform adaptation: [iOS](references/designing-for-ios.md), [iPadOS](references/designing-for-ipados.md), [macOS](references/designing-for-macos.md), [watchOS](references/designing-for-watchos.md), [tvOS](references/designing-for-tvos.md), and [visionOS](references/designing-for-visionos.md).
- Patterns and components: [pattern catalog](references/pattern-catalog.md), [layout](references/layout.md), [motion](references/motion.md), [components](references/components.md), [controls](references/controls.md), and [inputs](references/inputs.md).
- Presentation and inclusion: [navigation and search](references/navigation-and-search.md), [presentation](references/presentation.md), [inclusion](references/inclusion.md), and [VoiceOver](references/voiceover.md).
- Repeatable audit sequence: [audit workflow](references/audit-workflow.md).

## Verify

- Name the platform context and cite current HIG pages for material recommendations.
- Separate design advice from implementation contracts and state accessibility effects.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Confirm mapped references resolve. Static checks do not prove live-source freshness or behavioral quality.
- For SwiftUI implementation review, use `$swiftui-pro`; for broad interface refinement, use `$impeccable`; for screenshot acceptance, use `$design-proof-gate`.
