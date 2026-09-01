---
name: apple-design-hig
description: Make Apple-platform HIG, native UX, accessibility, or cross-device interface decisions. Use for Apple interaction and presentation guidance; not for implementation API lookup or non-Apple web design.
---

# Apple Design HIG

Resolve an Apple-platform interface decision from current Human Interface Guidelines, product context, and accessibility evidence.

State the decision, platform, device class, input modes, appearances, accessibility needs, constraints, affected users, and acceptance check. Keep product requirements, HIG guidance, SDK facts, and design judgment distinct. Safe local inspection and validation may proceed; live or external checks and product changes follow the user's authorization.

## Start with evidence

1. Inspect the existing interface and separate product constraints from assumed platform rules.

## Workflow

1. Load only the matching package references from the direct routes below; use `hig-source-index.md` for source coverage and `audit-workflow.md` for a full review.
   - [GOOD/RED implementation examples](references/examples.md) (read before choosing a native component or accessibility implementation; RED marks a contrast, while GOOD is the implementation pattern)
   - [Accessibility](references/accessibility.md) · [Action button](references/action-button.md) · [Action sheets](references/action-sheets.md) · [Activity rings](references/activity-rings.md)
   - [Activity views](references/activity-views.md) · [AirPlay](references/airplay.md) · [Alerts](references/alerts.md) · [Always On](references/always-on.md)
   - [App Clips](references/app-clips.md) · [App icons](references/app-icons.md) · [App Shortcuts](references/app-shortcuts.md) · [Apple Pay](references/apple-pay.md)
   - [Apple Pencil and Scribble](references/apple-pencil-and-scribble.md) · [Apple HIG Workflow](references/audit-workflow.md) · [Augmented reality](references/augmented-reality.md) · [Boxes](references/boxes.md)
   - [Branding](references/branding.md) · [Buttons](references/buttons.md) · [Camera Control](references/camera-control.md) · [CareKit](references/carekit.md)
   - [CarPlay](references/carplay.md) · [Charting data](references/charting-data.md) · [Charts](references/charts.md) · [Collaboration and sharing](references/collaboration-and-sharing.md)
   - [Collections](references/collections.md) · [Color wells](references/color-wells.md) · [Color](references/color.md) · [Column views](references/column-views.md)
   - [Combo boxes](references/combo-boxes.md) · [Complications](references/complications.md) · [Components](references/components.md) · [Content](references/content.md)
   - [Context menus](references/context-menus.md) · [Controls](references/controls.md) · [Dark Mode](references/dark-mode.md) · [Design principles](references/design-principles.md)
   - [Designing for games](references/designing-for-games.md) · [Designing for iOS](references/designing-for-ios.md) · [Designing for iPadOS](references/designing-for-ipados.md) · [Designing for macOS](references/designing-for-macos.md)
   - [Designing for tvOS](references/designing-for-tvos.md) · [Designing for visionOS](references/designing-for-visionos.md) · [Designing for watchOS](references/designing-for-watchos.md) · [Digit entry views](references/digit-entry-views.md)
   - [Digital Crown](references/digital-crown.md) · [Disclosure controls](references/disclosure-controls.md) · [Dock menus](references/dock-menus.md) · [Drag and drop](references/drag-and-drop.md)
   - [Edit menus](references/edit-menus.md) · [Entering data](references/entering-data.md) · [Eyes](references/eyes.md) · [Feedback](references/feedback.md)
   - [File management](references/file-management.md) · [Focus and selection](references/focus-and-selection.md) · [Foundations](references/foundations.md) · [Game Center](references/game-center.md)
   - [Game controls](references/game-controls.md) · [Gauges](references/gauges.md) · [Generative AI](references/generative-ai.md) · [Gestures](references/gestures.md)
   - [Getting started](references/getting-started.md) · [Going full screen](references/going-full-screen.md) · [Gyroscope and accelerometer](references/gyro-and-accelerometer.md) · [HealthKit](references/healthkit.md)
   - [Human Interface Guidelines](references/hig-source-index.md) · [Home Screen quick actions](references/home-screen-quick-actions.md) · [HomeKit](references/homekit.md) · [iCloud](references/icloud.md)
   - [Icons](references/icons.md) · [ID Verifier](references/id-verifier.md) · [Image views](references/image-views.md) · [Image wells](references/image-wells.md)
   - [Images](references/images.md) · [iMessage apps and stickers](references/imessage-apps-and-stickers.md) · [Immersive experiences](references/immersive-experiences.md) · [In-app purchase](references/in-app-purchase.md)
   - [Inclusion](references/inclusion.md) · [Inputs](references/inputs.md) · [Keyboards](references/keyboards.md) · [Labels](references/labels.md)
   - [Launching](references/launching.md) · [Layout and organization](references/layout-and-organization.md) · [Layout](references/layout.md) · [Lists and tables](references/lists-and-tables.md)
   - [Live Activities](references/live-activities.md) · [Live Photos](references/live-photos.md) · [Live-viewing apps](references/live-viewing-apps.md) · [Loading](references/loading.md)
   - [Lockups](references/lockups.md) · [Mac Catalyst](references/mac-catalyst.md) · [Machine learning](references/machine-learning.md) · [Managing accounts](references/managing-accounts.md)
   - [Managing notifications](references/managing-notifications.md) · [Maps](references/maps.md) · [Materials](references/materials.md) · [Menus and actions](references/menus-and-actions.md)
   - [Menus](references/menus.md) · [Modality](references/modality.md) · [Motion](references/motion.md) · [Multitasking](references/multitasking.md)
   - [Navigation and search](references/navigation-and-search.md) · [Nearby interactions](references/nearby-interactions.md) · [NFC](references/nfc.md) · [Notifications](references/notifications.md)
   - [Offering help](references/offering-help.md) · [Onboarding](references/onboarding.md) · [Ornaments](references/ornaments.md) · [Outline views](references/outline-views.md)
   - [Page controls](references/page-controls.md) · [Panels](references/panels.md) · [Path controls](references/path-controls.md) · [Patterns](references/pattern-catalog.md)
   - [Photo editing](references/photo-editing.md) · [Pickers](references/pickers.md) · [Playing audio](references/playing-audio.md) · [Playing haptics](references/playing-haptics.md)
   - [Playing video](references/playing-video.md) · [Pointing devices](references/pointing-devices.md) · [Pop-up buttons](references/pop-up-buttons.md) · [Popovers](references/popovers.md)
   - [Presentation](references/presentation.md) · [Printing](references/printing.md) · [Privacy](references/privacy.md) · [Progress indicators](references/progress-indicators.md)
   - [Pull-down buttons](references/pull-down-buttons.md) · [Rating indicators](references/rating-indicators.md) · [Ratings and reviews](references/ratings-and-reviews.md) · [Remotes](references/remotes.md)
   - [ResearchKit](references/researchkit.md) · [Right to left](references/right-to-left.md) · [Scroll views](references/scroll-views.md) · [Search fields](references/search-fields.md)
   - [Searching](references/searching.md) · [Segmented controls](references/segmented-controls.md) · [Selection and input](references/selection-and-input.md) · [Settings](references/settings.md)
   - [SF Symbols](references/sf-symbols.md) · [SharePlay](references/shareplay.md) · [ShazamKit](references/shazamkit.md) · [Sheets](references/sheets.md)
   - [Sidebars](references/sidebars.md) · [Sign in with Apple](references/sign-in-with-apple.md) · [Siri](references/siri.md) · [Sliders](references/sliders.md)
   - [Snippets](references/snippets.md) · [Spatial layout](references/spatial-layout.md) · [Split views](references/split-views.md) · [Status bars](references/status-bars.md)
   - [Status](references/status.md) · [Steppers](references/steppers.md) · [System experiences](references/system-experiences.md) · [Tab bars](references/tab-bars.md)
   - [Tab views](references/tab-views.md) · [Tap to Pay on iPhone](references/tap-to-pay-on-iphone.md) · [Technologies](references/technologies.md) · [Text fields](references/text-fields.md)
   - [Text views](references/text-views.md) · [The menu bar](references/the-menu-bar.md) · [Toggles](references/toggles.md) · [Token fields](references/token-fields.md)
   - [Toolbars](references/toolbars.md) · [Top Shelf](references/top-shelf.md) · [Typography](references/typography.md) · [Undo and redo](references/undo-and-redo.md)
   - [Virtual keyboards](references/virtual-keyboards.md) · [VoiceOver](references/voiceover.md) · [Wallet](references/wallet.md) · [Watch faces](references/watch-faces.md)
   - [Web views](references/web-views.md) · [What’s New in Apple Design](references/whats-new.md) · [Widgets](references/widgets.md) · [Windows](references/windows.md)
   - [Workouts](references/workouts.md) · [Writing](references/writing.md)
2. Verify material guidance against the live Apple HIG and cite the exact pages used.
3. Recommend the smallest native pattern, state rejected alternatives, and describe accessibility and implementation implications.

## Validation

1. When live discovery is needed, run `python3 scripts/hig_catalog.py --help` before the relevant catalog query; run the target project's interface and accessibility checks after edits.
2. Return the decision, platform differences, evidence, commands, changed paths, and any live HIG, device, SDK, hosted, or behavioral evidence that remains `UNVERIFIED`.

## Boundaries

- Bundled references are an offline snapshot; the live Apple HIG provides version-sensitive guidance.
- Prefer system components unless a concrete product constraint justifies a deviation.
- Keep HIG recommendations, SDK requirements, and inferred design judgment distinct.
- Route Swift, SwiftUI, UIKit, and other API correctness to implementation documentation; route generic web UX, App Store policy, provisioning, privacy manifests, and legal questions elsewhere.
- Use established repository formats and canonical inputs; keep new output in the repository's existing formats.
