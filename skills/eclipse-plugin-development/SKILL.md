---
name: eclipse-plugin-development
description: Build, migrate, test, package, and publish Eclipse IDE, Equinox OSGi, PDE, RCP, feature, and p2 plug-ins with current target-platform and Tycho practices. Use for MANIFEST.MF, plugin.xml, Declarative Services, extension points, SWT/JFace/e4 UI, PDE tests, API Tools, features, products, and update sites.
---

# Eclipse Plugin Development

Develop against an explicit target platform and OSGi contract. Keep bundle metadata, Java packages, extension declarations, build configuration, features/products, and p2 repository metadata synchronized. Prefer public Eclipse APIs, Declarative Services, Jobs, and lifecycle-safe UI/resource handling.

## Start with evidence

1. Inspect `META-INF/MANIFEST.MF`, `plugin.xml`, `fragment.xml`, `build.properties`, `OSGI-INF/`, `.target`, feature/product/category files, Maven/Tycho configuration, API baselines, tests, CI, and signing/publication workflows.
2. Identify target Eclipse release/platform, Java level, Tycho/Maven floor, bundle symbolic names and versions, singleton/fragment status, exported/imported packages, required bundles, extension points, features/products, and p2 repositories.
3. Preserve PDE/BND/pomless layout and existing target-platform strategy unless migration is requested.
4. Load relevant references:
   - [Platform and architecture](references/platform-and-architecture.md) for OSGi metadata, APIs, services, extension registry, Jobs, SWT/JFace/e4, resources, and compatibility.
   - [Testing and quality](references/testing-and-quality.md) for PDE JUnit, Tycho Surefire, UI/integration tests, API Tools, target matrices, and performance.
   - [Packaging and release](references/packaging-and-release.md) for Tycho, features, products, p2 repositories, signing, SBOMs, and release gates.
   - [Templates and ecosystem examples](references/templates-and-ecosystem.md) before choosing bundle, test, feature, repository, LSP4E, or RCP patterns.

## Implementation contract

- Resolve every build through the declared target platform; do not compile against random workspace/install contents.
- Keep OSGi imports/exports, `Require-Bundle`, execution environment, services, and extension declarations minimal and accurate.
- Prefer package imports and Declarative Services where established; use bundle activators only for lifecycle work that cannot be declarative.
- Never use `org.eclipse.*.internal` or APIs marked restricted/not intended for clients unless unsupported coupling is explicitly accepted.
- Keep SWT access on the display thread. Use Jobs for background work, scheduling rules for workspace mutations, progress monitors for cancellation, and async UI handoff for presentation.
- Dispose SWT colors, fonts, images, controls, listeners, services, trackers, jobs, and OSGi registrations at the owning lifecycle.
- Avoid blocking bundle activation and early-startup extensions. Use lazy activation and extension registry metadata.
- Maintain semantic OSGi versions, package versioning, and API baseline compatibility. Do not widen version ranges or re-export dependencies casually.
- Keep NLS strings, icons, accessibility, high-DPI behavior, and platform conventions consistent.

## Validation boundary

Run manifest/PDE validation, focused unit tests, JUnit Plug-in tests, Tycho build and test phases, API Tools/baseline checks, product/update-site assembly when affected, and clean target/runtime smoke tests. Test minimum and current declared target platforms.

Report target platform, bundle/feature/product metadata changes, API/version impacts, tests, p2 artifacts, signing state, and external release actions not performed.

## Templates

Use [the Tycho plug-in/feature/repository starter](assets/tycho-plugin-template/) as an adaptation source. Replace coordinates, target repository, Java/Tycho versions, IDs, and package names before import; remove feature/repository modules when only a bundle is requested.

## Boundaries

- Publishing update sites, signing with production keys, Marketplace changes, and release promotion require explicit authorization.
- Do not convert a plug-in task into a full RCP product or BND migration without scope authorization.
- Route cross-editor platform selection or shared language-server design to `$editor-extension-router`.
