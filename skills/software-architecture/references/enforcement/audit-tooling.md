# Executable architecture tooling

> Locally authored enforcement guidance, not a primary source or generated snapshot; source gap: live verification of current language, provider, and tool claims against [authority sources](sources.md) is required.

Use the bundled adapter for tool discovery and syntax evidence. It never
installs software, executes repository-provided shell commands, rewrites files,
or treats a missing provider as a clean result.

## Capability preflight

```bash
python3 scripts/providers.py capabilities --root <repo> --format json
```

The report distinguishes `ready` from `unavailable` and records the resolved
binary and version. Providers include ast-grep, Semgrep, Tree-sitter, clangd,
Cargo, Go, CMake, Ninja, Xmake, and Conan. Availability is not proof that a
provider has the project grammar, compilation database, build directory, or
manifest it needs.

## Read-only AST query

```bash
python3 scripts/providers.py ast-query \
  --root <repo> --tool ast-grep --language rust \
  --pattern 'unsafe { $$$BODY }' --rule-id unsafe-block \
  --severity warning --message 'review unsafe boundary' src
```

The adapter invokes `ast-grep run --json=stream --color never` with direct
arguments and validates every returned range and path against `<repo>`. It
returns a versioned envelope with provider version, argv, exit status, timing,
SHA-256 digests, normalized findings, and diagnostics. Exit codes are `0` for
clean, `1` for matches, `3` for unavailable, `4` for provider failure, `5` for
timeout/resource failure, and `6` for malformed output.

## Full read-only audit

```bash
python3 scripts/audit_architecture.py <repo> --format json
```

The bundled scanner is supplemental evidence. It reads repository files and
prints findings to standard output. It has no policy-file input and applies only
its built-in inventory, naming, topology, suppression, and inline-test rules. It
must not create a policy, provenance, schema, manifest, or report file in the
target repository. Keep repository-native architecture, build, lint, and test
commands as the acceptance authority.

## Package graph

Use the native resolver without configuring or generating a build:

```bash
python3 scripts/providers.py graph --root <repo> --tool auto --format json
```

`cargo-metadata` consumes `cargo metadata --format-version=1 --no-deps`; `go-list`
consumes `go list -json ./...`. The adapter accepts only structured JSON, keeps
provider diagnostics and digests, and reports resolver failures as
`tool-failed` rather than inventing a dependency graph.

## Sources

- [Architecture source map](sources.md); verify the linked source record before relying on current or external claims.
