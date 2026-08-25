# Test ownership and placement

> Locally authored enforcement guidance, not a primary source or generated snapshot; source gap: live verification of current language, provider, and tool claims against authority sources (see `enforcement-sources.md`) is required.

Test placement is part of production architecture. Put a test at the smallest
boundary whose contract it proves. Its location and build target should make
that ownership visible.

## Contents

- General ownership; Deno; Node/Bun; Go; Rust; Python; Swift
- Java/Kotlin; C/C++; C#/F#; declaration/platform companions; Zig; D; Nim; Odin/C3
- Ruby; PHP; architecture fitness tests; test-support boundaries

## General rule

Place tests where ownership is traceable from test placement and package
ownership, and where the ecosystem's normal tooling discovers them without
custom configuration. Test code and benchmark
code must be separate source units: do not embed test blocks, test functions,
annotations, macros, or runner DSL calls in authored production modules. A test
file remains a separate source unit even when it shares a package, namespace, or
target.

The bundled architecture audit rejects native inline forms and framework forms
for which the file carries explicit runner evidence. Actual test files and
exact test/benchmark roots are exempt. A custom source set is exempt only when an existing repository-owned build or test configuration defines it and repository evidence confirms its runner, owner, and scope. Do not add a custom schema file for the exemption. A directory whose name merely contains `test` is not a test location. If a runner uses an unrecognized form, improve the repository-native check rather than weakening or
bypassing the bundled audit.

Treat a runner-recognized test prefix/suffix as a technical marker for the
filename rules in `enforcement-naming.md`: `test_parser.py`, `parser_test.go`,
`parser.test.ts`, `parser.spec.ts`, and `ParserTest.java` each represent the
`parser` logical unit. Strip only the marker recognized by the active runner.
Semantic words before it still count, so `run-status-codec.test.ts` remains a
three-token violation. A source file and its test, declaration/header, generated
companion, or platform variant form one logical family for prefix-colony counts.

A test tree should either sit beside source or mirror it exactly. It should not
invent a competing architecture.

Benchmarks follow the same separation rule. Use a runner-recognized benchmark
source set or an exact `bench`/`benches` root; source-adjacent files may use
`*_bench.*`, `*_benchmarks.*`, `*.bench.*`, or `*.benchmark.*` when the runner
supports them. Do not place benchmark blocks or benchmark annotations in a
production module.

Do not infer test ownership or test type from a directory label alone. The
bundled scanner uses exact runner conventions only to avoid false inline-test
alarms; classify the test itself by the boundary crossed:

- **unit:** one cohesive source unit or package-internal behavior;
- **contract:** a stable API, ABI, protocol, plugin, or consumer/provider agreement;
- **integration:** two or more real infrastructure/package/process boundaries;
- **end-to-end:** the shipped entrypoint and user/device-visible workflow;
- **architecture:** dependency direction, cycle freedom, visibility, public
  surface, package contents, or workspace constraints.

Each separate test source set, project, target, suite, or process needs distinct
dependencies or a distinct lifecycle. Reject a `unit/` or `integration/` tree
that duplicates the source taxonomy without adding enforcement.

## Deno

Prefer Deno's underscore convention:

```text
src/
  mod.ts
  parser.ts
  parser_test.ts
  main.ts
  main_test.ts
```

For a larger package:

```text
src/
  parser/
    mod.ts
    lexer.ts
    lexer_test.ts
    parser.ts
    parser_test.ts
```

Do not use `*.test.ts` as the house pattern for Deno unless an existing
framework requires it.

## Node.js, Bun, pnpm, npm, Yarn, Vitest, Jest

Prefer source-adjacent conventional suffixes:

```text
src/
  parser.ts
  parser.test.ts
```

or language-specific extensions such as `.test.tsx`, `.spec.ts`, or `.spec.tsx`
when already established. Choose one convention per repository.

Use `__tests__/` only when the framework or existing repository convention
clearly favors it. Keep each `__tests__/` directory beside its owner rather
than building one global detached test taxonomy.

## Go

Keep tests in the same package directory:

```text
parser/
  parser.go
  parser_test.go
```

Use external test packages (`package parser_test`) for public-contract tests
and same-package tests for internal behavior when justified. Do not create a
global unit-test root.

## Rust

Keep Rust unit tests in separate, source-owned files. This skill rejects
production modules that contain inline tests or benchmarks; there is no
inline-test exception. The companion file remains part of the same source owner
and is connected through an external module declaration.

```text
src/
  parser.rs
  parser_tests.rs
```

Connect the companion from `parser.rs`:

```rust
#[cfg(test)]
#[path = "parser_tests.rs"]
mod tests;
```

For a module with an owned directory, use `parser/tests.rs` and connect it with
`mod tests;` or an explicit `#[path]`. Keep the companion discoverable and
owned by the same package/module; do not create a global detached unit-test
taxonomy.

Also valid and often useful for a unit that already owns an inner directory:

```text
src/
  parser.rs
  parser/
    tests.rs
```

Connect it with:

```rust
#[cfg(test)]
#[path = "parser/tests.rs"]
mod tests;
```

Reserve top-level `tests/` for integration tests compiled as external crates
against public APIs. Do not use it as the default home for all tests.

## Python

Respect the selected test runner. For pytest, common valid patterns are:

```text
src/acme/parser.py
tests/parser/test_parser.py
```

or a repository-level exact mirror:

```text
src/acme/parser/tokenizer.py
tests/acme/parser/test_tokenizer.py
```

For small packages, colocated `test_parser.py` may be acceptable, but avoid
shipping test-only dependencies in runtime artifacts when packaging constraints
matter.

## Swift

Swift Package Manager normally uses mirrored test targets:

```text
Sources/Parser/Parser.swift
Tests/ParserTests/ParserTests.swift
```

Within larger targets, mirror source ownership beneath the test target. Use
Swift Testing (default) or XCTest (for Xcode users) naming already
adopted by the repository.

## Java and Kotlin

Follow build-tool source sets:

```text
src/main/java/com/acme/parser/Parser.java
src/test/java/com/acme/parser/ParserTest.java
```

```text
src/main/kotlin/com/acme/parser/Parser.kt
src/test/kotlin/com/acme/parser/ParserTest.kt
```

The test package must mirror the production package. Keep integration tests in
a separate configured source set only when they have distinct lifecycle or dependencies.

## C and C++

Mirror components in the test tree when build tooling expects separation:

```text
src/parser/parser.c
include/acme/parser.h
tests/parser/parser_test.c
```

Small libraries may colocate test translation units beside source if the build
system clearly excludes them from production targets.

## CSharp/FSharp

Use sibling test projects and mirror namespaces/directories:

```text
src/Acme.Parser/Parser.{cs,fs}
tests/Acme.Parser.Tests/ParserTests.{cs,fs}
```

Do not mix production and test dependencies in one project merely for proximity.

## Declaration and platform companions

Keep test names aligned with the production logical unit after removing
tool-recognized representation markers. Examples include TypeScript `.d.ts`,
OCaml `.mli`, F# `.fsi`, C/C++ headers, Kotlin platform suffixes, Go
OS/architecture filename constraints, Dart generated companions, and Apple or
Android variants selected by the build. Do not treat arbitrary words such as
`support`, `runtime`, `service`, `context`, or `v1` as markers.

When renaming a production unit, update every companion and discovery/config
reference in the same change. Verify test enumeration, not only compilation, so
a syntactically valid rename cannot silently remove tests from the suite.

## Zig

Zig `test` blocks are still test code and must not remain in authored production
modules. Put them in a dedicated test root or source-owned test file and compose
that file through the build graph. Preserve package ownership and keep the
production module free of `test { ... }` declarations.

## D

Use the repository's unit-test model, but keep D `unittest { ... }` blocks out
of authored implementation modules. Use source-adjacent `_test.d` modules or a
mirrored test package accepted by the selected Dub configuration.

## Nim, Odin, and C3

Follow the package and test-runner conventions available in the repository, but
keep Nim `unittest`, `suite`, and `test` blocks out of authored implementation
modules. Prefer source-adjacent test files named consistently by the toolchain,
and preserve package ownership. Do not invent a global tests hierarchy unless
required by the build system.

## Ruby

Mirror library paths:

```text
lib/acme/parser.rb
spec/acme/parser_spec.rb
```

or `test/acme/parser_test.rb` for Minitest. Do not mix RSpec and Minitest
naming conventions without a migration plan.

## PHP

Mirror PSR-4 namespaces:

```text
src/Parser/Parser.php
tests/Parser/ParserTest.php
```

Keep unit and integration suites separate only when configuration,
dependencies, or runtime boundaries differ.

## Architecture fitness tests

Start with the strongest native enforcement available. Add a focused checker
only for gaps. Examples include:

- compiler/module visibility and forbidden project references;
- Bazel/Buck visibility, dependency queries, and layering rules;
- Java/Kotlin package/module rules with ArchUnit or equivalent;
- .NET project-reference and namespace rules with architecture tests;
- JavaScript/TypeScript import-boundary lint rules and package export maps;
- Python import-linter rules and distribution-content checks;
- Rust crate visibility plus dependency graph/cycle/license policies;
- Go `internal/` enforcement, package graph checks, and import-policy analyzers;
- C/C++ target dependency checks, public-header installation checks, and include
  graph analysis;
- Swift target dependencies and package/product API checks.

Architecture tests must assert allowed direction or a narrowly defined forbidden
edge. Avoid brittle snapshots of the entire tree when a semantic rule can be
expressed instead.

## Test-support boundaries

Reusable test support belongs to the narrowest owning test target/package. A
cross-repository `test-utils` package requires the same admission test as shared
production code: multiple real consumers, stable semantics, a named owner, and
no production dependency. Builders should create valid domain objects by
default; infrastructure fixtures must expose cleanup and isolation behavior.

Do not let mocks reproduce vendor/framework APIs across the product. Prefer a
port-owned fake for domain/application tests and a contract/integration test for
the real adapter.

## Sources

- Architecture source map (see `enforcement-sources.md`); verify the linked source record before relying on current or external claims.
