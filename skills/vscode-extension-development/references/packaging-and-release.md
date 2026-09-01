# VS Code packaging and release

## Prepackage contract

Confirm publisher/name identity, version, engine floor, license, README, changelog, support/repository links, icons, categories, pricing, preview state, extension packs/dependencies, registry targets, telemetry/privacy disclosure, and platform-specific assets.

## Bundling

- Preserve an existing repository's established bundler unless migration is requested. For new scaffolds from this skill, use the pinned Bun 1.4.0 `Bun.build` pipeline modeled on `xsyetopz/versionlens-redux`.
- Externalize the `vscode` module and preserve source maps according to release policy.
- Build separate Node and browser outputs when both entrypoints exist.
- Give the build script a non-publishing `--check` mode that builds into a temporary directory and cleans it up. This catches bundling failures without replacing reviewed release output.
- Check dynamic imports, native modules, worker assets, localization files, grammars, schemas, binaries, and license notices.
- Keep production bundles free of tests, source, secrets, local configuration, caches, and unnecessary dependencies.

## VSIX inspection

Use `@vscode/vsce` through a pinned project dependency. In the Bun baseline, invoke it as `bunx vsce ... --no-dependencies`; the production bundle, not a runtime `node_modules` tree, is the package input.

1. Run production build and tests.
2. Run `vsce ls` or inspect the package file list.
3. Run `vsce package`.
4. Unzip/inspect the VSIX for entrypoints, manifest, assets, licenses, unexpected files, symlinks, and secrets.
5. Install it into a clean profile and exercise core activation and upgrade behavior.

`.vscodeignore` and the `files`/bundler strategy must agree. Never exclude runtime assets or include source trees merely because local development still resolves them.

## Marketplace and Open VSX

- Visual Studio Marketplace publishing uses `vsce` and a publisher identity/token.
- Open VSX is a separate registry with separate namespace, token, policy, and compatibility expectations.
- Publishing to one registry does not authorize or prove compatibility with the other.
- Extension names and publisher identifiers are long-lived public contracts. Treat deletion, transfer, and rename as migrations.
- Do not remove an extension/version or unpublish without explicit authorization and impact review.

## Versioning and compatibility

- Release a new immutable semantic version; never overwrite an existing version.
- Keep `engines.vscode` at the true API floor.
- Use platform-specific packages only when native assets require them and test each package.
- Separate preview/stable channels or pre-release versions according to existing product policy.
- Document breaking setting/command/state migrations and preserve user state when possible.

## CI and credentials

- Separate PR validation from protected release jobs.
- Pin actions and tool versions, use minimal token scopes, and store tokens only in secret providers.
- Build and test before packaging; where possible publish the exact inspected artifact.
- Avoid echoing PATs, package manifests containing substituted secrets, or telemetry keys.
- Retain VSIX checksums, file lists, test matrix, registry response, and release commit.
- Publisher creation, verification, first publish, production publish, unpublish, and removal require explicit authorization.
- Pin Bun 1.4.0, Biome 2.5.10, the VSCE dependency, and CI setup versions. Fail frozen installs rather than silently rewriting `bun.lock` during release jobs.

## Official sources

- <https://code.visualstudio.com/api/working-with-extensions/bundling-extension>
- <https://code.visualstudio.com/api/working-with-extensions/publishing-extension>
- <https://code.visualstudio.com/api/working-with-extensions/continuous-integration>
- <https://github.com/microsoft/vscode-vsce>
- <https://github.com/eclipse/openvsx/wiki/Publishing-Extensions>
- <https://bun.sh/docs/bundler>
