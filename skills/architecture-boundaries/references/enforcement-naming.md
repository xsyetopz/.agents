# Filename contract

> Locally authored enforcement guidance, not a primary source or generated snapshot; source gap: live verification of current language, provider, and tool claims against authority sources (see `enforcement-sources.md`) is required.

Use this reference after detecting languages, toolchains, frameworks, generators,
and test runners. It applies to authored source, tests, configuration, IDL,
schemas, extensionless shebang scripts, and architecture-bearing documentation.
It supplements `enforcement-languages.md`; it does not replace compiler or loader
requirements.

## Contents

1. Authority and classification
2. Review defaults for authored files
3. Markers, families, and reserved names
4. Language and ecosystem catalog
5. Migration and output
6. Migration and output
7. Primary naming authorities

## 1. Authority and classification

Resolve names in this order:

1. compiler, language, runtime, platform, and toolchain requirements;
2. externally committed public paths and package/schema/deployment contracts;
3. framework loaders, generators, and test discovery;
4. published language guidance and dominant ecosystem convention;
5. one documented repository convention where no authority decides;
6. the short-name review default below when no higher authority decides.

Do not call a convention "official" unless a language, compiler, standard
library, or owning tool specifies it. A framework convention is authoritative
only inside that framework. Dominant practice is a default, not a compiler rule.
Repository convention can select among undecided case or separator styles; it
cannot legalize a taxonomy, prefix colony, repeated owner, or semantically long
leaf.

Classify every candidate before enforcement:

- **Authored:** apply the complete contract.
- **Generated/vendor/schema-derived:** retain generator/upstream names; isolate
  them, record provenance, and change the source or generator rather than output.
- **Ordered migration:** retain the migration tool's sequence/timestamp and
  descriptive stem; do not normalize away ordering metadata.
- **Snapshot/fixture:** retain exact runner or data-contract names when discovery
  or golden-file mapping requires them. A `schemas/` or `fixtures/` directory
  alone is not proof; source schemas and hand-authored fixtures receive normal
  filename checks.
- **Reserved:** retain an exact compiler/tool/framework name.

These classifications are visible exemptions. A directory name alone does not
prove them. The bundled audit recognizes only deterministic built-in evidence,
such as a reserved framework filename, generated companion pattern, or canonical
generated header. Exemptions do not make equivalent authored names acceptable
and do not count excluded paths as full-repository proof.

## 2. Review defaults for authored files

Use the shortest leaf that identifies one durable responsibility inside its
owner path. Prefer one semantic token; allow two when one token would be vague
or misleading.

For a separator-delimited leaf:

1. Strip the extension.
2. Remove only recognized discovery or representation markers listed below.
3. Count remaining semantic tokens separated by `-`, `_`, or repeated dots.
4. Flag three or more semantic tokens for owner review. Make the finding a hard
   gate only when the active toolchain or repository policy explicitly does so.

`runtime`, `codec`, `service`, `support`, `context`, `contract`, `manifest`,
`pins`, `boundary`, `regular`, `official`, `endpoint`, `package`, `workspace`,
`catalog`, `rollout`, `destination`, and version labels such as `v1` are
semantic. General words do not become suffixes merely because a repository uses
them repeatedly.

Do not split CamelCase or PascalCase declaration names to apply the token limit.
Where a compiler, language guide, loader, or dominant type-per-file convention
maps a declaration to its file, match the declaration and review whether that
declaration itself is cohesive. Do not shorten a public type into an opaque
filename.

Flag the following for review unless a higher authority or a recorded decision
requires the name:

- three or more sibling logical units with the same semantic leading token;
- a multi-token leaf that repeats an ancestor owner token;
- technical-taxonomy leaves such as `checkout-service`, `parser-helper`, or
  `order-types` when the suffix substitutes for responsibility;
- serial or temporal names such as `new_parser`, `handler2`, or `final-api`;
- abbreviations that require repository folklore to decode.

Count a source/header/test/declaration/platform family as one logical unit. When
a colony or long leaf appears, create a durable owner directory/module/package
and keep one- or two-token leaves under it. Do not merely rename every sibling
to a different synonym. The extracted owner may initially contain one file when
the directory itself carries module/package identity, visibility, routing,
public path, or an established extraction boundary. A wrapper directory with no
such semantics remains ceremonial.

This single-file owner distinction applies only to a real boundary produced or
preserved by extraction; it is not permission to wrap arbitrary leaves.

Examples:

```text
# repeated owner and three semantic tokens
security/security-tool-runtime.ts  -> security/tool/runtime.ts
security-tool-contract.ts          -> security/tool/contract.ts

# colony
destination-http.ts                -> destination/http.ts
destination-file.ts                -> destination/file.ts
destination-memory.ts              -> destination/memory.ts

# technical markers do not add semantic tokens
parser.test.ts                     # parser
parser.browser.test.ts             # parser + recognized platform marker
parser.d.ts                        # parser + declaration marker
parser_test.go                     # parser + required Go test marker
```

## 3. Semantic naming surfaces

Apply the same authority process to names beyond files:

- name packages, modules, namespaces, targets, and directories after the
  capability or bounded context they own;
- name types, functions, methods, values, constants, predicates, and errors
  after behavior, state, units, and failure semantics;
- use stable ubiquitous language for APIs, schemas, events, commands, queries,
  database objects, metrics, configuration keys, environment variables, and
  feature flags;
- make boolean polarity explicit (`is`, `has`, `can`, or a domain predicate),
  include units in measurements, and avoid unexplained abbreviations;
- permit pattern vocabulary such as `Repository`, `Factory`, or `Adapter` only
  when the selected boundary and forces make the role real; reject suffixes
  that hide an unowned capability.

Treat names as compatibility surfaces when serialized, reflected, exported,
published, persisted, or consumed by another team. Rename them with a contract
and migration plan, not a mechanical formatter.

## 4. Markers, families, and reserved names

Normalize a marker only when the active tool recognizes it:

- tests: `test_`, `_test`, `.test`, `.spec`, conventional `Test`/`Tests`, and a
  runner-required test directory or main file;
- declarations/interfaces: `.d.ts`, `.d.mts`, `.d.cts`, `.mli`, `.fsi`, header
  counterparts, or another tool-defined declaration representation;
- platforms/variants: Kotlin source-set suffixes such as `.jvm`/`.js`, Apple or
  Android platform markers, Go build-constraint filenames, and other
  toolchain-defined target markers;
- generated companions: `.g.dart`, `.freezed.dart`, designer resources,
  bindings, or another generator-owned marker.

A marker is not permission to chain semantic words: `run-status-codec.test.ts`
still has three semantic tokens.

Preserve exact reserved names. Common examples include `package.json`,
`tsconfig.json`, `deno.json`, `Cargo.toml`, `go.mod`, `go.sum`, `build.zig`,
`CMakeLists.txt`, `Makefile`, `Dockerfile`, `Gemfile`, `Rakefile`, `NAMESPACE`,
`DESCRIPTION`, `mix.exs`, `pubspec.yaml`, `Package.swift`,
`module-info.java`, `package-info.java`, `lib.rs`, `main.rs`, `mod.rs`,
`root.zig`, `__init__.py`, `conftest.py`, `runtests.jl`, and `AGENTS.md`.
This list is illustrative; verify the active tool version and framework.

## 5. Language and ecosystem catalog

The **Authority** column distinguishes requirements, official guidance,
framework/tool rules, dominant conventions, and repository-selected conventions.
"Repository-selected" means no broader filename case rule is claimed; all
universal semantic rules still apply.

| Approx. year | Ecosystem | Authority | Filename guidance and common markers |
| --- | --- | --- | --- |
| 1957 | **Fortran** | Tool/compiler mapping plus repository-selected case | Align a file with its primary module where tooling benefits; select one short case style. Keep preprocessor and fixed/free-form extensions required by the build. |
| 1958 | **Lisp family / Common Lisp** | ASDF load mapping; dominant lowercase/hyphen practice | Name files by the subsystem loaded by the `.asd`; keep the system definition reserved and avoid package-prefix colonies. |
| 1959 | **COBOL** | Compiler, dataset, copybook, and build-product rules | Preserve required program/copybook identifiers, dataset constraints, and generated members. Apply short semantic stems only where the platform permits. |
| 1964 | **BASIC / Visual Basic lineage** | IDE/project/designer rules; dominant type alignment in VB.NET | Preserve form/designer/resource companions. Match a primary public type when the project does so; otherwise select short PascalCase names. |
| 1970 | **Pascal / Delphi / Object Pascal** | Unit/compiler and IDE form rules | Match unit names and preserve paired form/resource files. Do not rename generated designer companions independently. |
| 1971 | **Shell (`sh`, Bash, Zsh, PowerShell)** | Entrypoint/platform rules; dominant lowercase practice | Prefer short lowercase executable or capability names; use the repository's established `-`/`_` only after checking invocation contracts. PowerShell commonly uses approved verb-noun command naming, which does not justify long module leaves. |
| 1972 | **C** | Build/include contracts; repository-selected case | No universal official filename case rule is asserted. Select short lowercase stems; keep `.h`/`.c` logical families and platform suffixes recognized by the build. |
| 1974 | **SQL and database procedural languages** | Migration/schema tool rules | Preserve ordered timestamps/versions and repeatable-migration prefixes. Use a short descriptive remainder; schema-derived output stays generator-owned. |
| 1978 | **MATLAB / numerical workspace languages** | MATLAB class/package/function mapping | Preserve `+package`, `@class`, and primary function/class mapping rules. Tests and Simulink/codegen companions follow the selected tool. |
| 1980 | **Smalltalk** | Image/export tool rules | Names may be image metadata rather than filesystem contracts. Preserve dialect export/package conventions; apply this contract to authored export files when names are selectable. |
| 1983 | **Ada** | Compiler naming convention and project configuration | Match package hierarchy to compiler/project filename mapping, including body/spec forms. Never substitute a foreign case style for configured GNAT or other compiler rules. |
| 1984 | **Objective-C** | Xcode/framework/resource rules; dominant type alignment | Commonly match `.h`/`.m`/`.mm` to the primary class and keep test/resource companions. Prefixes required for public collision avoidance are contractual, not architecture. No universal official case claim is made. |
| 1985 | **C++** | Module/build/include contracts; repository-selected case | No universal official filename case rule is asserted. Keep header/source/template counterparts discoverably aligned and select short lowercase stems unless public type/module mapping decides otherwise. |
| 1986 | **Erlang** | Compiler module mapping | Match the module atom to the `.erl` filename; preserve OTP application and test-suite conventions such as Common Test `_SUITE`. |
| 1987 | **Perl** | Package-to-path and harness rules | Match module namespaces under `lib/`; retain `.pm`, executable, and `t/` discovery forms. Numbered tests remain tool/repository conventions, not semantic tokens when they are discovery metadata. |
| 1988 | **Tcl** | Package index and application rules | Select short capability stems where the package loader does not dictate names; keep `pkgIndex.tcl` and harness-reserved names exact. |
| 1990 | **Haskell** | Compiler module-to-path mapping | Match hierarchical module names and capitalization. Preserve `Main.hs` for executable entry modules where used; tests follow the selected framework. |
| 1991 | **Python** | Official language guidance plus import/test rules | PEP 8 specifies short, all-lowercase module names, with underscores only when readability improves. Preserve `__init__.py`, `__main__.py`, `conftest.py`, and runner prefixes/suffixes such as `test_`. |
| 1993 | **Lua** | `require`/host loader mapping; dominant lowercase practice | Match module paths expected by `require`; preserve host/plugin entry names such as selected `init.lua`. Choose short lowercase stems where the host does not decide. |
| 1993 | **R** | R package/tool rules; repository-selected source case | Preserve `DESCRIPTION`, `NAMESPACE`, `R/`, `tests/testthat/`, and testthat discovery. No universal official source filename case rule is asserted; choose a coherent short style. |
| 1995 | **Ruby** | Constant autoload/framework mapping; dominant snake_case | Use snake_case file paths matching constants where Zeitwerk/Rails or local autoloaders require it. Preserve gem and test/spec discovery names. |
| 1995 | **Java** | Language/tool convention | Conventionally match a source file to its simple public top-level type; preserve `module-info.java` and `package-info.java`. Use conventional `Test`/`Tests` companions under configured source sets. |
| 1995 | **JavaScript** | Framework/tool rules; repository-selected source case | JavaScript has no universal official source filename case rule. Follow loader/framework-required entry names and the selected short case style; normalize `.test`/`.spec` only when the runner recognizes them. |
| 1995 | **PHP** | Composer/PSR-4 and framework mapping | Match namespace/class paths required by autoloading; use primary-class filenames where adopted. Preserve framework commands, migrations, and test suffixes. |
| 1996 | **OCaml** | Compiler/Dune module mapping | File stems determine module names; keep `.ml`/`.mli` counterparts aligned and preserve Dune-reserved files. Use short module names rather than taxonomic suffix chains. |
| 2000 | **C# / .NET** | SDK/project/designer rules; dominant type alignment | Commonly match the primary type and PascalCase, but do not claim a language-wide compiler rule. Preserve generated `.Designer`, XAML/code-behind, project, and conventional `Tests` companions. |
| 2001 | **D** | Compiler module-to-path mapping | Match module declarations to paths; preserve `package.d`. Use short module stems and runner/build-recognized test forms. |
| 2004 | **Scala** | JVM/build conventions; repository-selected grouping | Match a principal public type/object where it aids discovery, but cohesive multi-declaration files are valid. Use short PascalCase declaration-owned files or a documented local style. |
| 2005 | **F#** | Project compile-order and module/signature mapping | Keep `.fs`/`.fsi` counterparts and project order aligned. Common PascalCase/type alignment is a convention; preserve conventional test-project `Tests` markers. |
| 2007 | **Clojure** | Namespace-to-resource mapping | Match namespace segments to paths using Clojure's hyphen-to-underscore resource mapping. Preserve conventional `core.clj` only as an intentional namespace entry, not a dumping ground. |
| 2009 | **Go** | Toolchain requirements plus Go package practice | `_test.go` is required for `go test` discovery. Preserve build-constraint OS/architecture suffixes and `doc.go`; use short lowercase/underscore stems without type-per-file ceremony. Follow the official module-layout guidance in `enforcement-languages.md`. |
| 2010 | **Rust** | Compiler module mapping and Cargo-reserved roots | Module declarations map to `foo.rs`, `foo/mod.rs`, and submodules. Preserve `lib.rs`, `main.rs`, `mod.rs`, Cargo manifests, and selected source-adjacent/integration test structure; use short snake_case module stems. |
| 2011 | **Kotlin** | Official language guidance and platform tooling | Official guidance uses a filename matching the sole class, or descriptive UpperCamelCase for multiple declarations, and supports platform suffixes. Preserve source-set and test conventions; do not force Java one-type-per-file ceremony. |
| 2011 | **Dart / Flutter** | Official Dart/library and generator/framework rules | Use lower_snake_case authored library files; preserve package facade, test discovery, and generated companions such as `.g.dart` and `.freezed.dart`. |
| 2011 | **Elixir** | Mix/compiler mapping and dominant snake_case | Match module paths in snake_case under `lib/`/`test/`; preserve `mix.exs`, `config.exs`, and conventional `_test.exs`. |
| 2012 | **TypeScript** | Tool/framework rules; repository-selected source case | TypeScript standardizes declaration forms such as `.d.ts`, `.d.mts`, and `.d.cts`, not a universal source filename case. Select one short case style and preserve Node/Bun `.test`/`.spec` or Deno `_test` only for the active runner. |
| 2012 | **Julia** | Package/module conventions and tool rules | Preserve `src/Package.jl` and `test/runtests.jl`; use declaration-aligned module capitalization and short capability suite names where tools do not decide. |
| 2014 | **Swift** | SwiftPM/Xcode/resource rules; dominant type/capability alignment | No universal official filename case rule is asserted. Commonly use UpperCamelCase matching the primary type/capability; preserve generated resources and test-target conventions. Avoid `Extensions.swift` and taxonomy suffixes. |
| 2016 | **Zig** | Compiler/build import paths and reserved roots | Preserve `build.zig`, `root.zig`, and `main.zig`; use short lowercase stems selected by the repository where imports do not impose a path. Keep target variants explicit only when the build recognizes them. |
| 2016 | **Odin** | Package/tool rules; repository-selected case | Select short names consistent with verified package/tool conventions; do not repeat the package in every leaf. Platform suffixes count as markers only when the active build recognizes them. |
| 2019 | **C3** | Compiler/build module rules; repository-selected case | Follow the detected C3 toolchain's module and test mapping. Select short semantic stems where undecided; do not import C prefix taxonomies into module-qualified code. |

## 6. Migration and output

Before renaming, inventory imports/includes, module declarations, manifests,
exports, package contents, reflection strings, route/config references,
code-generation inputs and outputs, test discovery, CI path filters,
documentation links, case-insensitive filesystem hazards, and published paths.

Move one logical owner at a time. Use symbol-aware moves where available. Update
source/header/test/declaration/platform companions, build metadata, generated
lists, imports/exports, and consumers in the same change. Do not leave aliases,
barrels, forwarding wrappers, duplicate files, or empty directories unless a
public compatibility contract requires a time-bounded transition.

Report:

- detected naming authorities and the selected fallback convention;
- every added, renamed, moved, consolidated, or intentionally retained path;
- updated declarations, imports/includes, exports, manifests, generator inputs,
  tests, CI filters, and docs;
- visible generated/vendor/schema/migration/snapshot/reserved exemptions;
- case-only rename handling and public-path compatibility impact;
- exact checks and outcomes, including negative naming audit results before and
  clean results after;
- remaining uncertainty about ecosystem convention.

## 7. Primary naming authorities

Use the active compiler, tool, or framework documentation when it conflicts
with this catalog. These primary references support the most common normalized
forms:

- [PEP 8 package and module names](https://peps.python.org/pep-0008/#package-and-module-names)
- [Go test file discovery](https://pkg.go.dev/testing#hdr-Overview)
- [Rust module files](https://doc.rust-lang.org/reference/items/modules.html)
and [Cargo target layout](https://doc.rust-lang.org/cargo/guide/project-layout.html)
- [Java source and class file convention](https://docs.oracle.com/javase/tutorial/java/package/managingfiles.html)
- [Kotlin source-file conventions](https://kotlinlang.org/docs/coding-conventions.html#source-file-names)
- [Deno test discovery](https://docs.deno.com/runtime/test/) and [Bun test discovery](https://bun.sh/docs/test/discovery)
- [TypeScript declaration-file forms](https://www.typescriptlang.org/docs/handbook/2/type-declarations.html)

Absence from this list does not downgrade a language's own specification,
compiler mapping, or package-manager rules. Verify those rules from the pinned
tool version before renaming.

## Sources

- Architecture source map (see `enforcement-sources.md`); verify the linked source record before relying on current or external claims.
