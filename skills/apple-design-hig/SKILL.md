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
- Do not activate for Swift, SwiftUI, UIKit, or other SDK/API correctness work; use the implementation-specific documentation or skill for the target project.
- Do not activate for generic web or cross-platform UX, App Store policy, entitlements, provisioning, privacy manifests, or legal advice.

## Rules

- Treat the live Apple Human Interface Guidelines as authority; bundled references are an offline index.
- Resolve platform, device class, input method, appearance, and accessibility context before recommending a pattern.
- Prefer system components. Justify deviations with a concrete product constraint.
- Separate HIG recommendations, implementation requirements, and inferred design judgment. Do not invent Apple rules or API guarantees.

## Steps

1. State the interface decision, platform context, constraints, and affected users.
2. Inspect the existing interface when one exists.
3. Use the reference router to select platform, foundation, pattern, component, and accessibility material.
4. Verify material guidance against the live HIG and cite exact pages.
5. Recommend a pattern, rejected alternatives, accessibility effects, and implementation implications.
6. If files change, verify relevant sizes, input modes, appearances, and accessibility settings.

## Resources

- Start with the package [reference router](references/index.md).
- The router links the local HIG snapshot and the authored audit workflow; use those routes before searching individual topics.

## Verify

- Done means the platform context is named, current HIG pages support material recommendations, and accessibility effects are stated.
- Run `python3 scripts/check.py` and `python3 -m json.tool evals/evals.json >/dev/null` from this package.
- Confirm mapped references resolve. Static checks do not prove live-source freshness or behavioral quality.
- Report commands, exit codes, changed paths, evidence, and remaining limits.
- Mark live HIG, hosted, or behavioral evidence `UNVERIFIED` when it was not available or not run.
