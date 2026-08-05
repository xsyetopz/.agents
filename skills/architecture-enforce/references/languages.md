# Language architecture catalog

## Use this reference

Load this reference when languages affects the repository boundary under review. Verify its rules against source, build, test, and runtime evidence; every unresolved warning or error remains blocking.

Use this catalog after identifying the repository's language, framework, and
toolchain. Years approximate first public appearance or standard lineage. They
order the catalog only; they do not rank quality. For build and package
ownership, read `toolchains.md`. For filename case, separators, reserved names,
and suffixes, read `naming.md`; its contract applies to every row below.

## Contents

1. Selection and enforcement
2. 1950s-1970s: foundational and systems ecosystems
3. 1980s: modular, object-oriented, and concurrent ecosystems
4. 1990s: scripting, managed, web, and functional ecosystems
5. 2000s: managed-platform expansion
6. Late 2000s-2010s: modern systems, application, and data ecosystems
7. Mixed-language repositories

## 1. Selection and enforcement

Apply rules in this order:

1. Obey compiler, language, runtime, platform, and toolchain requirements.
2. Preserve externally committed public paths and package/schema/deployment contracts.
3. Obey framework loader, generator, and test-discovery requirements.
4. Apply published language guidance and dominant ecosystem convention.
5. Select one coherent repository convention only where no authority decides.
6. Apply this skill's defaults only where the first five do not decide.

A repository convention should not justify long separator-delimited names,
repeated owner prefixes, or a filename taxonomy. Apply the review normalization
and extraction signals in `naming.md` after satisfying higher authorities; make
them hard gates only through an explicit repository policy.

Treat a package, crate, target, assembly, component, or module as a boundary only
when it controls visibility, dependencies, compilation, deployment, reuse, or
ownership. Reject decorative layer trees and generic
`common`, `shared`, `helpers`, or `utils` packages without a named capability and
at least two stable consumers.

Table headings have these meanings:

- **Owner / boundary** identifies where dependencies and public API are controlled.
- **Source / tests** identifies the usual topology; framework conventions may
  override it.
- **Reject** lists recurring architecture failures, not every invalid layout.

## 2. 1950s-1970s: foundational and systems ecosystems

| Approx. year | Ecosystem | Owner / boundary | Source / tests | Reject |
| --- | --- | --- | --- | --- |
| 1947 | **Assembly families** | Treat object files, calling conventions, ABI surfaces, linker sections, interrupt/vector tables, and platform-specific modules as explicit boundaries. Keep handwritten assembly behind a stable C/Rust/Fortran or platform ABI when possible. | Follow the authoritative assembler/linker/build graph; keep architecture variants isolated and test through the consuming binary or emulator. Document register, stack, alignment, clobber, and ownership contracts. | Unowned inline assembly, duplicated ABI assumptions, global symbols that bypass module ownership, or mixing generated stubs with handwritten routines. |
| 1957 | **Fortran** | Use modules and libraries as public boundaries; isolate numerical kernels from file, MPI, accelerator, and application orchestration adapters. | Follow the selected build tool's `src/` convention; keep module names and files discoverably aligned. Put unit tests beside a test target or in a mirrored `test/`; keep reference datasets and tolerances explicit. | Global state spread across unrelated program units, unowned include fragments, or mixing generated interface code into authored kernels. |
| 1958 | **Lisp family / Common Lisp** | Use ASDF systems and packages intentionally. Systems own load/build composition; packages own symbol visibility. Keep implementation packages internal and export only supported symbols. | Group files by subsystem in `.asd` load order. Tests live in a separate test system that depends on public or explicitly internal test surfaces. | One universal package, implicit load-order coupling, or interned-symbol access that bypasses package contracts. |
| 1959 | **COBOL** | Treat programs, copybooks, data definitions, batch jobs, and transaction adapters as separately owned assets. Preserve stable record and external-call contracts. | Follow mainframe/build-product dataset conventions; mirror business capability rather than inventing a Unix tree during a partial migration. Keep test drivers and golden datasets outside production copybooks. | Casual edits to shared copybooks, business rules embedded in transport/JCL glue, or generated source edited directly. |
| 1964 | **BASIC / Visual Basic lineage** | In maintained VB.NET, use projects, namespaces, and assemblies as boundaries. In classic or embedded variants, preserve platform project structure and isolate forms/UI from domain behavior where the runtime permits. | Keep tests in dedicated test projects for .NET; for legacy variants, use the established harness and characterize behavior before reorganizing modules. | Mechanical conversion to a foreign folder pattern, giant form/code-behind modules, or shared mutable globals used as integration architecture. |
| 1970 | **Pascal / Delphi / Object Pascal** | Use units and packages as visibility/build boundaries. Keep forms and generated designer resources paired with their owners; place domain logic in non-visual units. | Follow project/package structure; use test projects or suites grouped by unit/capability. | Hand-editing designer-managed files, cyclic `uses` graphs, or a monolithic data module acting as service locator. |
| 1971 | **Shell (`sh`, Bash, Zsh, PowerShell)** | Treat a script as an executable adapter, not application architecture. Move durable logic into sourced capability modules or a testable implementation language. Keep entrypoints thin. | Put operator commands under `scripts/`, `bin/`, or the repository convention; name sourced modules by capability. Use Bats/ShellSpec/Pester or repository-native tests. Test destructive paths with fakes or sandboxes. | A generic `scripts/utils.*`, hidden working-directory assumptions, source-on-import side effects, or production logic encoded only in CI YAML. |
| 1972 | **C** | Use libraries/components and headers as contracts. Public headers belong under `include/<product>/`; private headers remain with implementation. Enforce dependency direction at link targets, not include-path convention alone. | Prefer `src/<capability>/*.c`, intentional translation units, and tests under the owning target or `tests/<capability>/`. Keep generated headers/sources isolated. | A global include directory exposing internals, one function per translation unit, umbrella headers exporting everything, or unchecked cross-component relative includes. |
| 1974 | **SQL and database procedural languages** | Treat schemas as owned modules or bounded contexts. Expose views, routines, or service APIs instead of allowing cross-domain table access. Migrations are an ordered deployment ledger, not a source-module taxonomy. | Keep repeatable definitions, versioned migrations, seeds, and tests distinct. Test constraints, compatibility views, rollback/forward behavior, and material query plans. | Editing an applied migration, a universal `public` schema with cross-domain writes, application-specific reporting queries in shared migrations, or generated ORM migrations hand-tuned without updating their source model. |
| 1978 | **MATLAB / numerical workspace languages** | Use packages (`+name`), classes, projects, and toolboxes as ownership units; isolate scripts and live notebooks from reusable functions. | Put reusable code in named packages and tests in `tests/` mirroring capability; keep generated code and Simulink artifacts under explicit ownership. | Base-workspace state as an API, path mutation as dependency management, or production algorithms living only in notebooks. |

### C and native-library default

```text
include/acme/parser.h       # supported consumer surface
src/parser/parser.c         # owned implementation
src/parser/parser_internal.h
tests/parser/parser_test.c
```

Keep ABI-facing declarations narrow. Do not expose allocation strategy, private
struct layout, platform headers, or third-party types unless they are an
intentional compatibility contract.

## 3. 1980s: modular, object-oriented, and concurrent ecosystems

| Approx. year | Ecosystem | Owner / boundary | Source / tests | Reject |
| --- | --- | --- | --- | --- |
| 1980 | **Smalltalk** | Use packages and class categories supported by the image/tooling as ownership metadata; keep domain objects separate from UI and persistence adapters. | Place SUnit tests in paired test packages/categories. Preserve image/export conventions required by the selected dialect. | God objects, behavior hidden in workspace scripts, or category names used as substitutes for dependency boundaries. |
| 1983 | **Ada** | Use package specifications as public contracts and bodies/child packages as implementation boundaries. Use project files to enforce library and subsystem dependencies. | Match package hierarchy and filenames to compiler conventions; keep AUnit or harness tests in dedicated test projects with explicit access policy. | Leaking private child packages, circular `with` dependencies, or generated bindings mixed with authored specifications. |
| 1984 | **Objective-C** | Use framework/module targets as boundaries and `.h` files as intentional API. Keep class extensions and private headers implementation-local; preserve Xcode resource ownership. | Group implementation by feature within targets; keep XCTest targets parallel to product targets. | Prefix-based naming treated as architecture, massive umbrella headers, public headers importing private implementation, or logic concentrated in view controllers. |
| 1985 | **C++** | Use build targets, libraries, namespaces, and module/header surfaces together. Public headers or module interfaces define contracts. Private headers and templates remain with their owner. | Prefer `include/<product>/<capability>.hpp`, `src/<capability>/`, and target-aligned tests. Keep template implementation adjacent (`.tpp`/`.ipp`) when needed. | Header-only by default, one class per library, transitive includes as API, target-wide `PUBLIC` dependencies that should be `PRIVATE`, or an all-exporting umbrella header. |
| 1986 | **Erlang** | Use OTP applications and supervision trees as operational boundaries. Modules own behavior, processes own state, and behaviours define contracts. | Keep `src/`, `include/`, `priv/`, and `test/` within each application. Put EUnit/Common Test modules in the application test source set rather than embedding test generators or assertions in `src/`. | A flat module namespace across unrelated OTP apps, process dictionaries as shared state, cross-app calls to private modules, supervisors containing business logic, or inline EUnit/Common Test code in production modules. |
| 1987 | **Perl** | Use distributions and namespaces as package boundaries; keep command wrappers thin over modules under `lib/`. | Follow `lib/Acme/...`, `bin/` or `script/`, and `t/` numbering/naming already established; group tests by capability, not chronology alone. | Runtime `@INC` manipulation, giant procedural entrypoints, exported-everything modules, or unowned `Util.pm`. |
| 1988 | **Tcl** | Use packages and namespaces as boundaries; isolate interpreter/UI glue from reusable commands and state. | Follow package index and application conventions; keep `tcltest` suites beside or mirrored from their package owner. | Global variables as inter-package contracts, source-order coupling, or a single script mixing UI, transport, and domain behavior. |

### C++ public/private default

```text
include/acme/parser/parser.hpp
src/parser/parser.cpp
src/parser/lexer.hpp         # private to the target
src/parser/lexer.cpp
tests/parser/parser_test.cpp
```

Do not infer that a physical header is public. Confirm install/export rules and
target include visibility in the authoritative build model.

## 4. 1990s: scripting, managed, web, and functional ecosystems

| Approx. year | Ecosystem | Owner / boundary | Source / tests | Reject |
| --- | --- | --- | --- | --- |
| 1990 | **Haskell** | Use Cabal packages/components and modules as boundaries; keep exposed modules minimal and internal modules unexposed. | Follow `src/`, `app/`, and `test/` component roots; structure tests by public module or capability. | An all-exporting Prelude replacement, cyclic module pressure solved with boot files by default, or typeclass abstraction without multiple credible consumers. |
| 1991 | **Python** | Use distributions and import packages as boundaries. Prefer a `src/` layout for distributable libraries. Organize large framework applications by domain while preserving discovery rules. | Use `src/acme/<capability>/` and mirrored `tests/` or framework-native tests. Keep `__init__.py` as a deliberate facade, not a recursive export dump. | Import-path mutation, top-level `utils.py`, business logic in framework entrypoints, tests importing private filesystem paths, or namespace-package changes without packaging evidence. |
| 1993 | **Lua** | Use modules, rocks, or host-application plugin units as boundaries; return explicit module tables and isolate host globals at adapters. | Mirror module paths under `spec/` or `test/` according to the selected harness; keep embedded-runtime fixtures owned by their host adapter. | Ambient globals, mutation during `require`, one `init.lua` exporting the whole tree, or assuming standalone Lua conventions inside an engine/plugin host. |
| 1993 | **R** | Use packages and namespaces as production boundaries; scripts and notebooks consume package code rather than becoming its source of truth. | Follow `R/`, `tests/testthat/`, `inst/`, and `vignettes/`; use `NAMESPACE`/roxygen ownership consistently and isolate generated documentation. | `source()` chains as architecture, `.GlobalEnv` state, analysis notebooks containing unrecoverable production logic, or hand-editing generated `NAMESPACE` under roxygen ownership. |
| 1995 | **Ruby** | Use gems, Bundler groups, namespaces, and framework engines/components as boundaries. Keep `lib/<gem>.rb` as a deliberate entrypoint. | Mirror `lib/acme/...` under `spec/` or `test/`. In Rails, preserve autoload paths while organizing large systems by bounded feature. | Catch-all `concerns`, `services`, or `helpers`, monkey patches without explicit ownership, callback webs as cross-domain integration, or autoload-name/path mismatches. |
| 1995 | **Java** | Use JPMS modules where adopted, build modules, packages, and visibility as boundaries. Organize first by domain/capability, then by real internal layer. | Follow build source sets such as `src/main/java` and `src/test/java`; one public top-level class per file remains the default. | Repository-wide `controllers/services/repositories/models` buckets, public classes used to bypass package ownership, split packages, or reflection-based access to internals without an explicit adapter. |
| 1995 | **JavaScript** | Use packages, export maps, and runtime module mode as boundaries. For Node/Bun, use intentional `index.*` facades only. For browser frameworks, colocate feature-owned components, styles, stories, and tests. | Follow the selected runner's `*.test.*` or `*.spec.*`; separate contract/e2e suites only at real boundaries. | Deep imports around package exports, mixed ESM/CJS without an interop boundary, global `components/hooks/utils` dumping grounds, or framework CLI output reorganized against its loader. |
| 1995 | **PHP** | Use Composer packages, PSR-4 namespaces, and framework modules/bundles as boundaries. Keep namespace paths aligned with autoload configuration. | Follow `src/<Capability>/...` and mirrored `tests/`; one primary class per file is the normal default. | Global syntax-category folders across domains, service-locator access everywhere, traits as unowned code sharing, or path/namespace drift. |
| 1996 | **OCaml** | Use Dune libraries/executables and modules as boundaries; `.mli` files define intentional public contracts where abstraction matters. | Keep library-owned tests in Dune test stanzas or test libraries; structure modules by capability and control wrapping explicitly. | Exposing every module, cyclic dependencies hidden through global opens, or signatures duplicated without serving abstraction. |

### Managed/web package default

```text
src/<domain>/<capability>/       # authored implementation
tests/<domain>/<capability>/     # mirrored only where ecosystem expects it
<manifest>                       # package-level dependency contract
<lockfile>                       # reproducible resolution contract
```

Do not apply this literal tree to Rails, Django, Maven, or another framework that
requires a different loader/source-set structure. Preserve the semantic owner,
not the drawing.

## 5. 2000s: managed-platform expansion

| Approx. year | Ecosystem | Owner / boundary | Source / tests | Reject |
| --- | --- | --- | --- | --- |
| 2000 | **C# / .NET** | Use solutions only as coordination views; projects, assemblies, namespaces, and access modifiers are boundaries. Keep deployment hosts thin over application/domain projects. | Prefer `src/Acme.Capability/` and `tests/Acme.Capability.Tests/`, feature folders inside each project, and target-aligned test projects. | A project per trivial type, giant `Services`/`Managers` folders, circular project references, partial classes used to hide poor cohesion, or domain code depending on ASP.NET/UI hosts. |
| 2001 | **D** | Use Dub packages/configurations and D modules as boundaries; match module declarations to source paths and use `package.d` only as an intentional facade. | Follow `source/` and `tests/` or `_test.d` source units; keep all `unittest` blocks outside production modules. | One-type-per-file ceremony, an automatic re-exporting `package.d`, C-style global prefixes where module qualification provides ownership, or inline `unittest` blocks. |
| 2004 | **Scala** | Use sbt/Mill modules, JVM packages, and visibility as boundaries. Keep functional core, effects, transports, and persistence dependencies directed. | Follow `src/main/scala` and `src/test/scala` per module. Group tightly related algebra/data definitions when cohesive rather than forcing Java file rules. | Implicit/given scope as an unbounded dependency registry, package objects as dumping grounds, or one cross-repository technical-layer tree. |
| 2005 | **F#** | Use projects/assemblies and modules as boundaries; treat compile order in project files as an explicit dependency graph. | Keep feature modules in dependency order and tests in paired test projects. Use signatures only when they provide a meaningful abstraction surface. | Arbitrary file reordering, cyclic design disguised through mutable state, or one `Types.fs` containing unrelated domain models. |
| 2007 | **Clojure** | Use artifacts/modules and namespaces as boundaries; keep side effects at system edges and domain transformations in owned namespaces. | Mirror `src/acme/...` under `test/acme/...`; put REPL/dev-only code in explicit dev paths or aliases. | A universal `core` namespace, runtime var resolution to bypass dependency direction, production reliance on REPL state, or multimethod/global registry sprawl without ownership. |

## 6. Late 2000s-2010s: modern systems, application, and data ecosystems

| Approx. year | Ecosystem | Owner / boundary | Source / tests | Reject |
| --- | --- | --- | --- | --- |
| 2009 | **Go** | Use modules, packages, compiler-enforced `internal/`, and the official [module organization guidance](https://go.dev/doc/modules/layout) as the authority. Select `cmd/<binary>`, `internal/`, or another layout from the project kind; `pkg/` is an external API commitment, not a default. | Keep cohesive package files flat, adjacent `*_test.go`, and package-owned `testdata/`. Add `api/`, `configs/`, `deployments/`, or `scripts/` only when the repository owns those artifact classes. | A project-level `src/` copied without evidence, Java-style one-type-per-file, `util/common/models` packages, import cycles, or business behavior in `cmd`/`main`. |
| 2010 | **Rust** | Crates are build/reuse boundaries; modules and visibility enforce internal ownership. Keep `lib.rs`/`main.rs` as composition surfaces and use `pub(crate)` before widening API. | Use `foo.rs` plus `foo/` submodules or established `foo/mod.rs`; keep unit tests and benches in `*_tests.rs`, `foo/tests.rs`, `tests/`, or `benches/` source units. Connect source-owned tests with an external module declaration. | Crate-per-file fragmentation, indiscriminate `pub use`, giant prelude modules, circular feature flags, splitting solely to evade borrow/visibility design, or inline `#[test]`, `#[bench]`, or body-bearing test modules. |
| 2011 | **Kotlin** | Use Gradle/Maven modules, packages, and Kotlin visibility as boundaries; for Android, keep platform/UI adapters outside domain/application modules. | Follow `src/main/kotlin`, `src/test/kotlin`, and platform source sets; group tightly related declarations when cohesive. | Java ceremony imposed mechanically, global extension-function dumps, Android framework types leaking into domain modules, or Gradle module proliferation without dependency/build value. |
| 2011 | **Dart / Flutter** | Use packages and Dart libraries as boundaries; feature packages own UI, state, and adapters while domain code avoids Flutter imports. Use `part` only for generated or tightly coupled library implementation. | Follow `lib/src/`, a small `lib/<package>.dart` facade, adjacent/mirrored `test/`, and `integration_test/` for app boundaries. | `screens/widgets/services/models` as repository-wide buckets, public `src/` deep imports, giant barrels, or hand-edited generated `.g.dart`/`.freezed.dart`. |
| 2011 | **Elixir** | Use Mix projects/umbrella applications, OTP applications, contexts, and behaviours as boundaries. Contexts expose capability APIs; processes are not default domain containers. | Follow `lib/` and mirrored `test/`; keep supervision/config adapters separate from pure domain modules. | One umbrella app per technical layer, cross-context schema/repo access, process-per-module design, or `use` macros that silently inject broad dependencies. |
| 2012 | **TypeScript** | Use packages, export maps, project references where justified, and runtime-compatible module mode as boundaries. Keep types with their owner; create type-only packages only for true shared contracts. | Node/Bun use the selected `*.test.*`/`*.spec.*` convention. Deno uses `deno.json(c)`, deliberate `mod.ts` facades, and normally `*_test.ts`. | Recursive barrels, `types.ts` for unrelated declarations, path aliases that bypass package exports, or compiling one source tree under incompatible server/browser assumptions. |
| 2008 | **Nim** | Use Nim modules, packages, and build targets as visibility and dependency boundaries; isolate C/Objective-C interop and generated bindings at adapters. | Follow the detected Nimble/project layout and module import mapping; keep tests in dedicated suites or source-adjacent test files. | Global compile-time state used as architecture, broad `include` chains that bypass imports, speculative OO layers, generated C output treated as authored policy, or inline `unittest`/`suite`/`test` blocks. |
| 2012 | **Julia** | Use packages/modules as production boundaries and environments as dependency boundaries; keep notebooks/scripts as consumers of package code. | Follow `src/Package.jl` with owned submodules and `test/runtests.jl` delegating to capability suites. | Mutation of the global environment, giant `include` chains without module ownership, or performance-sensitive kernels mixed with I/O/orchestration. |
| 2014 | **Swift** | Use SwiftPM/Xcode targets and modules as boundaries; keep app composition thin and organize target internals by feature/domain. Protocols must represent real substitution or boundary needs. | SwiftPM uses `Sources/<Target>/` and `Tests/<Target>Tests/`; Xcode test targets parallel product targets. Keep extensions near the owned type/capability. | Universal `Models/Views/Managers`, target-per-folder fragmentation, enormous `Extensions.swift`, generated Xcode resources hand-edited, or UI frameworks imported into domain targets. |
| 2014 | **Crystal** | Use shards, modules, and compile targets as boundaries; keep macro-heavy metaprogramming local to the owner and foreign-library bindings behind adapters. | Follow `shard.yml`, `src/`, and `spec/` conventions with module/path alignment; verify generated C or platform bindings through the actual compiler target. | Ruby-style runtime loading assumptions, global macro side effects, unowned `lib` bindings, or packages split only to mimic another ecosystem. |
| 2016 | **Zig** | Use build modules/artifacts and explicit imports as boundaries. Keep `root.zig`/`main.zig` as composition surfaces and capability submodules explicit. | Put `test` blocks in dedicated test roots or source-owned test files and wire them through the build graph; isolate generated bindings. | Generic `util.zig`, public declarations by accident, inline `test` blocks in production modules, one build step owning unrelated products, or C ABI details spread through domain modules. |
| 2016 | **Odin** | Use packages as ownership/visibility boundaries. Several flat `.odin` files per cohesive package are idiomatic. Isolate foreign interfaces and platform variants. | Keep tests according to repository/tool conventions and name platform-specific files explicitly. Practices vary, so preserve verified local structure. | Repeating the package name in every filename, speculative OO layers, a global utility package, or unmarked generated bindings. |
| 2019 | **C3** | Use modules, packages, and build targets to express ownership; keep C interop at adapters and exploit module qualification instead of global prefixes. | Group cohesive `.c3` files under capability directories; follow the detected toolchain's test conventions because they may evolve. | C-style prefix taxonomies, speculative class-style layering, or assumptions about niche tool behavior not evidenced by the repository/tool version. |

### Go application baseline and adjacent ecosystems

```text
# Go application
go.mod
go.sum
cmd/server/main.go               # composition only
internal/checkout/*.go           # private capability packages
internal/platform/postgres/*.go  # technical adapters
pkg/client/*.go                  # only if external consumers are supported
api/openapi.yaml                 # only when this contract exists
deployments/                     # only when deployment assets are owned here

# Rust
crates/protocol/src/lib.rs
crates/protocol/tests/contract.rs

# SwiftPM
Sources/Checkout/{Domain,API}/
Tests/CheckoutTests/
```

For a substantial Go application, use `cmd/` plus `internal/` and reject a
project-level `src/`. Do not copy every directory from the community layout.
Each directory must own real artifacts, and `pkg/` commits the project to an
externally consumable package surface. A single-purpose library or small command
may remain flat. Do not turn a Rust workspace into a crate-per-directory layout
or create a Swift target merely to reduce file count.

## 7. Mixed-language repositories

Choose boundaries by deployable or product ownership first. Then preserve each
language's native layout inside its boundary:

```text
apps/
  desktop/                 # Swift/Xcode owner
  web/                     # TypeScript workspace package
services/
  billing/                 # JVM or .NET service owner
  gateway/                 # Go module owner
packages/
  protocol/                # schema source of truth
  native-parser/           # C/C++/Rust library owner
generated/
  protocol/{java,swift,ts}/
```

Enforce all of the following:

1. Give every subtree one authoritative build/package owner; a root orchestrator
   may invoke it but must not duplicate its dependency graph.
2. Put schemas, IDLs, and code generators in a named contract owner. Generate
   language bindings into isolated paths; never patch generated output directly.
3. Cross boundaries through versioned APIs, schemas, FFI headers, or package
   exports. Forbid private-path imports and source-level reach-through.
4. Keep one lockfile per declared resolution domain. Multiple lockfiles are valid
   only when release cadence or tooling isolation is intentional and documented.
5. Assign integration tests to the boundary they prove: consumer contract tests
   with the consumer, provider compatibility tests with the provider, and end-to-
   end workflows with the deployable system owner.
6. Keep vendored third-party code, generated bindings, build output, and authored
   source visibly separate. Apply format/lint only where the generator or vendor
   workflow permits it.
7. Do not force every language into `src/domain/layer`. Standardize dependency
   policy, ownership metadata, and verification entrypoints instead.

Before moving a cross-language boundary, inspect FFI memory ownership, ABI and
calling convention, serialization compatibility, error mapping, concurrency or
runtime affinity, generated-file provenance, and release/version coupling.
