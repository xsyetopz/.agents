# Apple HIG Workflow

Scope: local-policy. This authored workflow explains how to apply the bundled
Apple HIG snapshot. Bundled topic files remain source material and may need a
live-page check when guidance is version-sensitive.

Source status: use the HIG source index (see `hig-source-index.md`) to locate the
canonical Apple pages, then record the page consulted and its retrieval date.

## Full workflow

### 1. Frame the decision

Record platform, minimum OS, device posture, screen/input constraints, content
type, localization, accessibility needs, and whether this is a new design,
audit, redesign, or implementation.

### 2. Find the page

Use the direct reference routes in `../SKILL.md`, search the reference directory by
title or slug, and open the smallest matching page. Use
`references/whats-new.md` to discover recent topics; use the current topic list
list is exhaustive.

### 3. Check current evidence

For a current or version-sensitive claim, open the canonical Apple URL and
compare it with the local reference. Record the live retrieval date and any
change-log date used as evidence.

### 4. Resolve cross-cutting constraints

Check accessibility and inclusion, Dynamic Type and legibility, localization
and right-to-left layout, dark mode and contrast, privacy, reduced motion,
haptics/audio, safe areas, multitasking/windowing, and the platform's input
model.

### 5. Map to implementation

Prefer system components, semantic controls, platform conventions, SF Symbols,
system typography, and adaptive layout. Link relevant API documentation, note
SDK availability, and describe only behavior that the HIG specifies.

### 6. Deliver and verify

State the decision, rationale, platform differences, alternatives rejected, and
a verification checklist. Inspect supported appearances, sizes, input methods,
orientations/window sizes, localization directions, assistive technologies,
reduced-motion settings, and empty/loading/error states. Report what was tested
and what still requires an Apple-device or SDK check.

## Snapshot audit and validation

Run commands from the skill directory:

```sh
python3 scripts/hig_catalog.py --help
python3 scripts/hig_catalog.py --all --deep
python3 scripts/hig_catalog.py --topic foundations
```

The catalog helper reads Apple's live DocC JSON and prints the current catalog
or one topic summary to standard output. These commands are read-only and leave the
bundled references. Compare the printed source URLs and retrieval date with the
local snapshot, then report stale or missing coverage instead of creating a
custom generated file. The catalog helper is for live discovery, not a citation
substitute.

Apple currently exposes HIG articles through
`https://developer.apple.com/tutorials/data/design/human-interface-guidelines/`
and the human-facing site at
`https://developer.apple.com/design/human-interface-guidelines/`. Historical
What's New rows can point to unavailable pages (`messages-for-business`,
`touch-bar`) or redirects (`navigation-bars` -> `toolbars`); report these as
historical exceptions rather than creating duplicate or fabricated pages.

If network access is unavailable, label conclusions as snapshot-based and
include the reference retrieval date. Recheck the live page whenever a change
log, OS release, API, or review requirement may have changed.

## Sources

- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Apple Design — What’s New](https://developer.apple.com/design/whats-new/)
- Bundled HIG source index (see `hig-source-index.md`)
