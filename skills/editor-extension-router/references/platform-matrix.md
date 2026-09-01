# Editor extension platform matrix

Version-sensitive baseline verified on 2026-09-01. Re-check official documentation before relying on a specific API or release.

| Platform | Verified current baseline | Main runtime/model | Declarative assets | Procedural reach | Distribution |
|---|---|---|---|---|---|
| JetBrains IntelliJ Platform | 2026.2 docs; Gradle plugin 2.x | JVM, Kotlin/Java, IntelliJ services/extensions | `plugin.xml`, module descriptors, icons/resources | Deep IDE/PSI/index/UI/project integration | JetBrains Marketplace plugin ZIP |
| VS Code | Stable 1.135 | Node extension host and browser web worker | `package.json` contribution points, grammars, themes, snippets | Broad editor/workspace APIs, webviews, LSP/DAP, remote/web | VSIX, Visual Studio Marketplace, optionally Open VSX |
| Zed | Rust API crate 0.7.0 | Declarative assets plus Rust compiled to WASM | `extension.toml`, languages, queries, themes, icons, snippets | Focused LSP/DAP/tool-resolution capability; sandboxed | PR/submodule to Zed extensions registry |
| Neovim | Stable 0.12.5 | In-process Lua/Vimscript, RPC providers | Runtimepath files, queries, syntax, help | Highly programmable editor core, LSP client, processes/UI | Git/runtimepath/packages; decentralized managers |
| Eclipse | 2026-06 / Platform 4.40; Tycho 5.0.4 stable | JVM, OSGi bundles, PDE/e4/SWT/JFace | OSGi manifests, `plugin.xml`, DS descriptors, features/products | Deep workspace/workbench/RCP integration | Bundles/features/products and p2 repositories |
| Sublime Text | Sublime Text 4 build 4200 stable | Embedded Python 3.8 API environment | Resource files for syntax, settings, menus, themes, completions | Commands/listeners, views, minihtml, processes through Python | `.sublime-package`, Package Control/channel |

These are research snapshots, not automatic project upgrade targets.

## Capability fit

### Full IDE semantic/project integration

- JetBrains: strongest fit for PSI, inspections, intentions, refactoring, indexes, project models, and IntelliJ-native UI.
- Eclipse: strongest fit for Eclipse workspace/resources, JDT/PDE/e4/RCP, OSGi services, and deep workbench integration.
- VS Code: good fit through extension APIs and LSP, but avoids private workbench/DOM internals.
- Neovim: strong programmable client behavior; project semantics usually come from LSP or plugin-owned analysis.
- Zed: intentionally narrower extension API; language, LSP, debugger, theme/icon/snippet capabilities are primary.
- Sublime: strong editing/package customization and Python APIs; deep semantic analysis is usually external or package-owned.

### Reusable language support

- LSP server: portable across all six when each client adapter supports needed methods and launch/configuration.
- TextMate grammar: natural for VS Code and Sublime; can inform other platforms but is not a universal artifact.
- Tree-sitter grammar/queries: natural for Zed and Neovim; host query conventions differ.
- JetBrains custom language support: PSI/parser/lexer/stubs/indexes are platform-native and generally not portable.
- Eclipse language tooling: LSP4E can reuse LSP, while native JDT/Xtext/model tooling is platform-specific.

### Debugging

- DAP is reusable across VS Code, Zed, Neovim clients/plugins, and Eclipse integrations when available.
- JetBrains debugger integrations commonly use platform-specific execution/debugger APIs, though adapters/protocol bridges can be shared.
- Sublime debugging generally depends on a package such as an LSP/DAP client; core package APIs do not imply a standardized debugger contribution.

### Remote and web

- VS Code explicitly supports local, remote, and browser extension hosts; design placement and Node/web differences.
- JetBrains remote-development behavior depends on platform/frontend/backend APIs and target product; verify per feature.
- Zed supports remote-development product behavior, but extension execution remains constrained by its current API/WASM model.
- Neovim typically runs where the editor process runs; remote usage is terminal/RPC/environment architecture rather than a separate marketplace host model.
- Eclipse remote tooling is feature-specific, not a universal split extension-host contract.
- Sublime packages run in the local editor process.

### Native processes and binaries

- JetBrains/Eclipse/VS Code desktop/Neovim/Sublime can launch processes subject to platform and security design.
- VS Code web extensions cannot use ordinary Node process APIs.
- Zed Rust extensions use supported APIs to locate/download/run tools; they are not unrestricted native Rust.
- Every platform needs OS/architecture mapping, quoting, timeout/cancellation, update, integrity, and trust policy.

## Selection questions

1. Which editors do target users already use?
2. Is the feature language intelligence, editor UI, project model, debugger, theme, or workflow automation?
3. Can the core be an LSP/DAP/CLI/library, or does it need host-private models?
4. Must it run in browsers, remote workspaces, air-gapped environments, or restricted workspaces?
5. Does it execute workspace-controlled code or download binaries?
6. Are native UI, refactoring, index, or RCP capabilities required?
7. Which registries/licenses/publisher identities can the project maintain?
8. What minimum editor versions and operating systems are supportable in CI?
9. Is preserving an existing public extension ID/settings/state mandatory?

## Primary official sources

- https://plugins.jetbrains.com/docs/intellij/welcome.html
- https://code.visualstudio.com/api
- https://zed.dev/docs/extensions
- https://neovim.io/doc/user/lua-plugin/
- https://help.eclipse.org/latest/topic/org.eclipse.pde.doc.user/concepts/plugin.htm
- https://www.sublimetext.com/docs/
