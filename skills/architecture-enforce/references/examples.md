# Structural examples

> Illustrative examples, not evidence or a generated snapshot; source gap: live verification of each example against repository facts and current primary sources is required before relying on a claim.

Apply the language and toolchain references before adopting a tree. These
examples show how boundary decisions affect a repository tree.

## Contents

- Flat TypeScript prefix colony; cross-language filename extraction; prefix
  colony extraction
- Deno library; Rust source-owned tests; Go package boundary
- Oversized orchestrator; microfile confetti; test exile
- C/C++ target architecture; modular monolith before service extraction;
  polyglot generated boundary; ceremonial enterprise layering

## Flat TypeScript (Deno) prefix colony

Before:

```text
src/
  auth-session-handler.ts
  auth-session-store.ts
  auth-session-types.ts
  auth-token-handler.ts
  auth-token-validator.ts
  auth-utils.ts
  billing-invoice-handler.ts
  billing-invoice-types.ts
  main.ts
```

After:

```text
src/
  auth/
    mod.ts
    session.ts
    session_test.ts
    token.ts
    token_test.ts
  billing/
    mod.ts
    invoice.ts
    invoice_test.ts
  main.ts
```

The directory supplies ownership, so filenames no longer repeat category chains.

## Cross-language filename extraction

The semantic review signal is cross-language; the resulting case and companions
remain native to each ecosystem.

```text
# Python: official short lowercase module style
src/security/security_token_runtime.py
  -> src/security/token/runtime.py
tests/security/test_security_token_runtime.py
  -> tests/security/token/test_runtime.py

# Java: retain public-type/file matching instead of splitting PascalCase words
src/main/java/com/acme/security/SecurityTokenRuntime.java
  -> src/main/java/com/acme/security/token/TokenRuntime.java
src/test/java/com/acme/security/SecurityTokenRuntimeTest.java
  -> src/test/java/com/acme/security/token/TokenRuntimeTest.java

# C++: repository-selected lowercase stems, aligned header/source/test family
include/acme/security/security_token_runtime.hpp
  -> include/acme/security/token/runtime.hpp
src/security/security_token_runtime.cpp
  -> src/security/token/runtime.cpp
tests/security/security_token_runtime_test.cpp
  -> tests/security/token/runtime_test.cpp

# Go: preserve required test marker and package ownership
internal/security/security_token_runtime.go
  -> internal/security/token/runtime.go
internal/security/security_token_runtime_test.go
  -> internal/security/token/runtime_test.go
```

Update package/module declarations, imports/includes, exports, build lists,
generator inputs, tests, CI path filters, and documentation atomically. Remove
obsolete paths and empty directories. A public-path constraint requires an exact
provenance entry in `.architecture-enforcement.json`; this records context and
does not waive a finding or justify an undocumented alias.

## Prefix colony extraction

Before:

```text
src/
  destination-http.ts
  destination-file.ts
  destination-memory.ts
  destination-contract.ts
```

After:

```text
src/
  destination/
    http.ts
    file.ts
    memory.ts
    contract.ts
```

Three sibling logical units sharing `destination` require extraction even
though every original leaf has only two semantic tokens. A corresponding
`destination-http.test.ts` is part of the `destination-http` logical family; it
does not count as a fourth unit.

## Deno library

```text
deno.jsonc
src/
  mod.ts
  parser.ts
  parser_test.ts
  diagnostics.ts
  diagnostics_test.ts
  main.ts
  main_test.ts
```

`mod.ts` exports supported library APIs. `main.ts` owns CLI composition. Tests
use Deno's `_test.ts` convention.

## Rust source-owned tests

```text
src/
  lib.rs
  parser.rs
  parser_tests.rs
  parser/
    lexer.rs
    diagnostics.rs
```

`parser.rs` connects the separate unit file with
`#[cfg(test)] #[path = "parser_tests.rs"] mod tests;`. For a cohesive nested
module, use `parser/tests.rs` instead. Reserve top-level `tests/` for public
integration tests.

## Go package boundary

Bad:

```text
internal/
  auth_session.go
  auth_token.go
  billing_invoice.go
  common_utils.go
```

Better:

```text
internal/
  auth/
    session.go
    session_test.go
    token.go
    token_test.go
  billing/
    invoice.go
    invoice_test.go
```

Do not add another directory beneath `auth/` merely to place each file in its
own folder.

For a Go service with these owners, apply the official module/package guidance
and select only the directories the service actually owns:

```text
go.mod
go.sum
cmd/
  api/
    main.go                    # thin composition root
internal/
  auth/
    session.go
    session_test.go
  billing/
    invoice.go
    invoice_test.go
  platform/
    postgres/
      invoice_store.go
api/
  openapi.yaml
deployments/
  helm/
scripts/
  verify.sh
```

Add `pkg/` only for packages intentionally supported as imports by external Go
modules. Do not add empty `configs/`, `build/`, `web/`, `website/`, `assets/`, or
`third_party/` directories merely because the template lists them. Do not put
Go application source under a project-level `src/`.

## Oversized orchestrator

Before:

```text
src/deploy.ts  # 1,240 lines
```

The file handles:

- configuration parsing;
- deployment planning;
- provider API calls;
- progress rendering;
- rollback policy.

After:

```text
src/deploy/
  __tests__/
    execute.test.ts
    rollback.test.ts
  mod.ts
  config.ts
  plan.ts
  execute.ts
  rollback.ts
  progress.ts
```

Do not split into `types.ts`, `interfaces.ts`, `constants.ts`, `helpers.ts`,
`validation.ts`, or one file for each operation/phase. Those names classify
syntax or procedure, not durable responsibilities. Keep each role with its
nearest owner unless the source-topology map proves an independent lifecycle,
contract, visibility/dependency boundary, or failure policy.

## Microfile confetti

Before:

```text
src/parser/
  parser.ts
  parser-options.ts
  parser-state.ts
  parser-result.ts
  parser-context.ts
  parser-helper.ts
```

When each secondary file contains only a tiny declaration used exclusively by
`parser.ts`, consolidate:

```text
src/parser/
  parser.ts
  diagnostics.ts
  parser.test.ts
```

Keep options, state, result, and internal context with the parser unless they
have independent ownership, lifecycle, visibility, dependency contract, or
reuse. `Validation`, `Helpers`, `Open`, `Reduce`, and `Commit` remain
procedural roles by default; names alone do not justify one-file-per-role
decomposition.

## Test exile

Before:

```text
src/checkout/pricing.ts
src/checkout/discounts.ts
tests/unit/services/pricing-service.test.ts
tests/unit/helpers/discount-helper.test.ts
```

After for Node/Bun/Vitest:

```text
src/checkout/
  pricing.ts
  pricing.test.ts
  discounts.ts
  discounts.test.ts
```

After for Java/Kotlin, retain mirrored source sets instead of literal colocation.

## C/C++ target architecture with CMake, Ninja, and Conan

Rejected:

```text
include/
  common.h
src/
  managers.cpp
  services.cpp
  utils.cpp
CMakeLists.txt              # one target containing everything
conanfile.py                # dependencies leaked globally
```

Accepted for one deployable with enforced components:

```text
CMakeLists.txt
CMakePresets.json
conanfile.py
cmake/
  dependencies.cmake
src/
  checkout/
    CMakeLists.txt
    include/acme/checkout/pricing.hpp
    pricing.cpp
    discount_policy.cpp
    pricing_test.cpp
  payments/
    CMakeLists.txt
    include/acme/payments/gateway.hpp
    payment_service.cpp
    stripe_adapter.cpp
  app/
    CMakeLists.txt
    main.cpp
```

`checkout` owns pricing policy. `payments` owns an inward-defined gateway and
the vendor adapter. `app` is the composition root. CMake declares target edges,
Conan resolves external dependencies, and Ninja may execute the generated build;
none substitutes for another.

## Modular monolith before service extraction

Rejected premature services:

```text
services/
  users-service/
  user-preferences-service/
  user-notifications-service/
```

When all three deploy together, share one database transaction boundary, and
have no independent scaling or failure requirement, prefer enforced modules:

```text
src/
  identity/
    public/
    internal/
  preferences/
    public/
    internal/
  notifications/
    public/
    adapters/
  app/
    composition_root.*
```

Extract a network service only after operational independence justifies timeout,
versioning, observability, and data-ownership costs.

## Polyglot repository with generated boundary

```text
proto/
  checkout/v1/checkout.proto
services/
  checkout-go/
    go.mod
    internal/
  pricing-rust/
    Cargo.toml
    src/
clients/
  web-typescript/
    package.json
generated/
  go/
  rust/
  typescript/
tools/
  codegen/
```

The schema is the authoritative cross-language contract. Generated types remain
outside domain policy, each language package owns an adapter, and CI regenerates
then fails on a diff. Do not share source directories or reach across package
manifests with relative imports.

## Ceremonial enterprise layering

Rejected:

```text
controllers/checkout_controller.*
services/checkout_service.*       # forwards one call
managers/checkout_manager.*       # forwards one call
repositories/checkout_repository.*
models/checkout_model.*
```

Accepted when checkout is one capability:

```text
checkout/
  pricing.*
  place_order.*
  order_store_port.*
  adapters/sql_order_store.*
  tests/...
```

Create layers only where dependency direction or lifecycle differs. Do not call
pass-through files "corporate architecture."

## Sources

- [Architecture source map](sources.md); verify the linked source record before relying on current or external claims.
