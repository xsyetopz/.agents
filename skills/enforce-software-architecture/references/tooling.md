# Executable architecture tooling

Use the bundled adapter for tool discovery and syntax evidence. It never
installs software, executes repository-provided shell commands, rewrites files,
or treats a missing provider as a clean result.

## Capability preflight

```bash
python3 scripts/architecture_tools.py capabilities --root <repo> --format json
```

The report distinguishes `ready` from `unavailable` and records the resolved
binary and version. Providers include ast-grep, Semgrep, Tree-sitter, clangd,
Cargo, Go, CMake, Ninja, Xmake, and Conan. Availability is not proof that a
provider has the project grammar, compilation database, build directory, or
manifest it needs.

## Read-only AST query

```bash
python3 scripts/architecture_tools.py ast-query \
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

## Repository rules

Add repeatable syntax gates to `.architecture-enforcement.json` without putting
commands in repository configuration:

```json
{
  "syntax_rules": [
    {
      "id": "forbidden-python-import",
      "tool": "ast-grep",
      "language": "python",
      "pattern": "import $MODULE",
      "severity": "error",
      "message": "this module crosses the protected boundary",
      "mode": "required",
      "paths": ["src"]
    }
  ]
}
```

`required` rules fail closed on `blocked`, `timeout`, `tool-failed`, or
`invalid-output`. `advisory` rules report the same condition as a warning but
never claim proof. The filename and regex checks remain `inventory` evidence;
they cannot satisfy a syntax, symbol, package-graph, or build-graph gate.

## Package graph

Use the native resolver without configuring or generating a build:

```bash
python3 scripts/architecture_tools.py graph --root <repo> --tool auto --format json
```

`cargo-metadata` consumes `cargo metadata --format-version=1 --no-deps`; `go-list`
consumes `go list -json ./...`. The adapter accepts only structured JSON, keeps
provider diagnostics and digests, and reports resolver failures as
`tool-failed` rather than inventing a dependency graph.
