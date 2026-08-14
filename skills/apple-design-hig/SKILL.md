---
name: apple-design-hig
description: Apple HIG, iOS/macOS UX, native components, accessibility; excludes SDK and generic web UX.
---

# Apple Design HIG

Apply current Apple design guidance to a concrete interface decision and keep the source-to-decision trace visible.

## When to use

- Review or design an iOS, iPadOS, macOS, watchOS, tvOS, or visionOS screen, flow, or component.
- Choose native navigation, presentation, input, feedback, typography, color, motion, or system experiences.
- Audit adaptation across devices, input modes, appearances, Dynamic Type, VoiceOver, or other accessibility needs.

## When NOT to use

- Swift, SwiftUI, UIKit, or SDK/API correctness without a design question.
- App Store policy, entitlements, provisioning, privacy manifests, or legal advice.
- Generic web or cross-platform UX with no Apple-platform decision.

## Guardrails

- Treat the live Apple Human Interface Guidelines as authority; bundled references are an offline index.
- Resolve platform, device class, input method, and accessibility context before recommending a pattern.
- Prefer system components; justify deviations with a concrete product constraint.
- Separate HIG recommendations, implementation requirements, and inferred design judgment. Never invent an Apple rule or API guarantee.

## Workflow

1. State the interface decision, platform contexts, constraints, and affected users.
2. Inspect the existing interface when one exists.
3. Load only the matching platform, foundation, pattern, component, and accessibility references.
4. Verify material guidance against the live HIG and cite the exact pages.
5. Recommend a pattern, rejected alternatives, accessibility effects, and implementation implications.
6. If files change, verify relevant sizes, input modes, appearances, and accessibility settings.

## Quick start

Read [design principles](references/design-principles.md), the target platform reference, the relevant component or pattern reference, and [accessibility](references/accessibility.md). Use [audit workflow](references/audit-workflow.md) for the audit sequence.

## Reference map

- Canonical ordered router: [index](references/index.md).
- Foundations and rationale: [foundations](references/foundations.md), [design principles](references/design-principles.md).
- Platform adaptation: [iOS](references/designing-for-ios.md), [iPadOS](references/designing-for-ipados.md), [macOS](references/designing-for-macos.md), [watchOS](references/designing-for-watchos.md), [visionOS](references/designing-for-visionos.md), or the matching platform file.
- Common tasks and flows: [pattern catalog](references/pattern-catalog.md).
- Layout and presentation: [layout](references/layout.md), [typography](references/typography.md), [color](references/color.md), [motion](references/motion.md), [navigation and search](references/navigation-and-search.md), [presentation](references/presentation.md).
- Components and access: [components](references/components.md), [controls](references/controls.md), [inputs](references/inputs.md), [accessibility](references/accessibility.md), [VoiceOver](references/voiceover.md), [inclusion](references/inclusion.md).
- Audit procedure: [audit workflow](references/audit-workflow.md).

## Completion

A result is complete when it names the platform context, cites current HIG pages for material recommendations, separates design advice from implementation contracts, addresses accessibility, and verifies any changed interface.

## Validation

Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package. Confirm every mapped reference resolves; static PASS does not claim live-source freshness or behavioral quality.

## Related skills

- `$swiftui-pro` for SwiftUI implementation review.
- `$impeccable` for broader product-interface refinement.
- `$design-proof-gate` for screenshot-backed visual acceptance.
