---
name: apple-design-hig
description: Use this skill when designing or auditing Apple-platform UI, UX, interaction, accessibility, typography, layout, color, motion, components, inputs, system experiences, or Apple technology decisions across iOS, iPadOS, macOS, tvOS, visionOS, watchOS, and games. Check the live HIG and cite exact guidance; distinguish HIG recommendations from SDK, API, entitlement, and accessibility implementation contracts.
---

# Apple Design HIG

Use this skill to navigate Apple's living Human Interface Guidelines (HIG).
Apple's live documentation is the source of truth; the bundled Markdown corpus
is a reproducible reading copy for offline discovery and analysis.

## Non-negotiables

- Identify the target platform(s), OS release, device and input context,
  framework, and user goals before selecting guidance. If unknown, state the
  assumption and choose the broadest safe rule.
- Start discovery in `references/index.md` for the HIG home, then open the
  page matching the URL slug at `references/<slug>.md`. Use
  `references/whats-new.md` for the complete What's New listing.
- Treat each reference as ordinary Markdown with standard YAML front matter
  (title, source URL, and retrieval metadata), headings, paragraphs, lists,
  tables, and preserved links.
- Read **Platform considerations**, **Specifications**, and **Change log** when
  present. A platform-specific page or consideration narrows a generic rule.
- Summarize guidance in your own words and link the exact Apple page. Do not
  reproduce long passages, screenshots, or proprietary media.
- Separate HIG guidance from implementation contracts. For APIs, availability,
  entitlements, metrics, or accessibility behavior, follow the linked Apple
  Developer documentation and verify the target SDK.
- Call out conflicts, legacy terminology, unavailable pages, redirects, and
  uncertainty. Memory or an older snapshot is not current evidence.

## Workflow

1. **Frame the decision.** Record platform, minimum OS, device posture,
   screen/input constraints, content type, localization, accessibility needs,
   and whether this is a new design, audit, redesign, or implementation.
2. **Find the page.** Read `references/index.md`, search the reference directory
   by title or slug, and follow links from the matching page. Use
   `references/whats-new.md` to discover recent topics; never assume a fixed
   topic list is exhaustive.
3. **Check current evidence.** For a current or version-sensitive claim, open
   the canonical Apple URL and compare it with the local reference. Record the
   live retrieval date and any change-log date used as evidence.
4. **Resolve cross-cutting constraints.** Check accessibility and inclusion,
   Dynamic Type and legibility, localization and right-to-left layout, dark
   mode and contrast, privacy, reduced motion, haptics/audio, safe areas,
   multitasking/windowing, and the platform's input model.
5. **Map to implementation.** Prefer system components, semantic controls,
   platform conventions, SF Symbols, system typography, and adaptive layout.
   Link relevant API documentation, note SDK availability, and do not invent
   behavior that the HIG does not specify.
6. **Deliver and verify.** State the decision, rationale, platform differences,
   alternatives rejected, and a verification checklist. Inspect supported
   appearances, sizes, input methods, orientations/window sizes, localization
   directions, assistive technologies, reduced-motion settings, and
   empty/loading/error states. Report what was tested and what still requires
   an Apple-device or SDK check.

## Refresh and validation

Run commands from `skills/apple-design-hig/`:

```sh
python3 scripts/harvest_hig.py harvest
python3 scripts/harvest_hig.py validate
python3 scripts/harvest_hig.py table-smoke
python3 scripts/hig_catalog.py --all --deep
```

`harvest` replaces the generated `references/` directory from Apple's DocC JSON
and the What's New page, writing one file per current HIG URL (`index.md` for
the root) and `whats-new.md`. Binary
images, videos, and audio are intentionally omitted; their alt text, captions,
and external references remain. `validate` checks front matter, URL/slugs,
links, and What's New coverage. `table-smoke` exercises table-bearing pages.
The catalog helper is for live discovery, not a citation substitute.

Apple currently exposes HIG articles through
`https://developer.apple.com/tutorials/data/design/human-interface-guidelines/`
and the human-facing site at
`https://developer.apple.com/design/human-interface-guidelines/`. Historical
What's New rows can point to unavailable pages (`messages-for-business`,
`touch-bar`) or redirects (`navigation-bars` → `toolbars`); report these as
historical exceptions rather than creating duplicate or fabricated pages.

If network access is unavailable, label conclusions as snapshot-based and
include the reference retrieval date. Recheck the live page whenever a change
log, OS release, API, or review requirement may have changed.

When citing guidance, use:

> **Apple HIG — _Page title_** (retrieved YYYY-MM-DD): _paraphrased rule_.
> <https://developer.apple.com/design/human-interface-guidelines/<slug>>
