# Bun, ES2025, and TypeScript contract

Keep these independent contracts visible in the repository's existing configuration:

- Bun executes/transpiles the application; it does not replace the repository's TypeScript checker.
- TypeScript 7's native Go/shared-memory compiler improves type-checking, editor, and build-tool latency; it does not make emitted application code faster at runtime. Measure runtime changes in Bun/JavaScriptCore separately from compiler/build changes.
- `target` and `lib` describe emitted JavaScript and ambient APIs. Use `ES2025` only where the application's runtime support policy permits it; preserve a stricter existing target unless the user authorizes a runtime baseline change.
- `module`, `moduleResolution`, `types`, JSX, decorators, declaration emit, and project references are compatibility decisions, not runtime-speed toggles.
- If `compilerOptions.types` is present, treat it as the project’s explicit global type allow-list; list each required Bun/test/environment type intentionally.

For TypeScript compiler performance, use `tsc --extendedDiagnostics` and `tsc --generateTrace <directory>` only to diagnose a measured slow type-check or build. Do not disable checking (`noCheck`) merely to claim a product runtime improvement; split type-check and transpile stages only when the repository can preserve diagnostics and declaration correctness.

## Source locations

- TypeScript compiler command/reference: `https://www.typescriptlang.org/docs/handbook/compiler-options.html`
- TSConfig `types` semantics: `https://www.typescriptlang.org/tsconfig/types.html`
