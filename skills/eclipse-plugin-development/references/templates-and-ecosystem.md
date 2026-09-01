# Eclipse templates and ecosystem examples

Verified 2026-09-01. Eclipse repositories often span bundles, tests, features, targets, products, and p2 repositories. Extract the smallest relevant pattern and preserve EPL/license obligations.

## Primary build/platform sources

- `eclipse-tycho/tycho`: build implementation, integration tests, documentation examples, packaging types, and current Maven/Tycho practices.
- `eclipse-pde/eclipse.pde`: PDE manifests, tooling, launchers, API Tools, feature/product support, and examples.
- `eclipse-platform/eclipse.platform`: current workspace/runtime APIs and versioning conventions.
- `eclipse-platform/eclipse.platform.ui`: workbench, commands/handlers, SWT/JFace/e4 UI, and UI tests.

## Production projects

- `eclipse-lsp4e/lsp4e`: LSP and DAP integration, target platform, mock servers, plug-in tests, and p2 repository module.
- `eclipse-tm4e/tm4e`: TextMate grammar integration commonly paired with LSP4E.
- `eclipse-egit/egit`: core/UI bundle separation, target platform, unit/UI tests, features, source features, documentation, and repository packaging.
- `eclipse-m2e/m2e-core`: workspace builders, project configuration, jobs, Maven integration, and large multi-bundle lifecycle.
- `eclipse-wildwebdeveloper/wildwebdeveloper`: language servers, TextMate grammars, debug integration, and web-language tooling.
- `eclipse-jdt/eclipse.jdt.ui`: large-scale Java UI, refactoring, views/editors, actions/handlers, API baselines, and tests.

## What to extract

- Bundle/core/UI/test/feature/repository separation only where responsibilities require it.
- Target-platform and Tycho reactor structure.
- DS services and lazy extension declarations.
- PDE JUnit/Tycho test runtime configuration.
- API baseline and semantic bundle/package version updates.
- p2 install/update smoke testing.

## Avoid copying

- Eclipse project governance/release infrastructure into a small third-party plugin.
- `.internal` API use visible in platform implementation.
- Incubating/snapshot Tycho syntax without pinning the matching release.
- EPL source without satisfying license and derivative-work requirements.

## Repositories

- https://github.com/eclipse-tycho/tycho
- https://github.com/eclipse-pde/eclipse.pde
- https://github.com/eclipse-platform/eclipse.platform
- https://github.com/eclipse-platform/eclipse.platform.ui
- https://github.com/eclipse-lsp4e/lsp4e
- https://github.com/eclipse-tm4e/tm4e
- https://github.com/eclipse-egit/egit
- https://github.com/eclipse-m2e/m2e-core
- https://github.com/eclipse-wildwebdeveloper/wildwebdeveloper
- https://github.com/eclipse-jdt/eclipse.jdt.ui
