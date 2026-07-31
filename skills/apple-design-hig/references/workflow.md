# Apple HIG Workflow

## Full workflow

### 1. Frame the decision

Record platform, minimum OS, device posture, screen/input constraints, content
type, localization, accessibility needs, and whether this is a new design,
audit, redesign, or implementation.

### 2. Find the page

Read `references/index.md`, search the reference directory by title or slug, and
follow links from the matching page. Use `references/whats-new.md` to discover
recent topics; never assume a fixed topic list is exhaustive.

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
SDK availability, and do not invent behavior that the HIG does not specify.

### 6. Deliver and verify

State the decision, rationale, platform differences, alternatives rejected, and
a verification checklist. Inspect supported appearances, sizes, input methods,
orientations/window sizes, localization directions, assistive technologies,
reduced-motion settings, and empty/loading/error states. Report what was tested
and what still requires an Apple-device or SDK check.

## Refresh and validation

Run commands from the skill directory:

```sh
python3 scripts/harvest_hig.py harvest
python3 scripts/harvest_hig.py validate
python3 scripts/harvest_hig.py table-smoke
python3 scripts/hig_catalog.py --all --deep
```

`harvest` replaces the generated `references/` directory from Apple's DocC JSON
and the What's New page, writing one file per current HIG URL (`index.md` for
the root) and `whats-new.md`. Binary images, videos, and audio are intentionally
omitted; their alt text, captions, and external references remain. `validate`
checks front matter, URL/slugs, links, and What's New coverage. `table-smoke`
exercises table-bearing pages. The catalog helper is for live discovery, not a
citation substitute.

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
