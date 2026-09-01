# Eclipse plug-in packaging and release

## Current Tycho baseline

On 2026-09-01, Tycho 5.0.4 was the current stable version found, requiring Maven 3.9.9 and JDK 21. Tycho main documentation also exposed 6.0.0-SNAPSHOT pages. Pin a released Tycho version in production builds and verify its system requirements.

Tycho builds plug-ins/OSGi bundles, tests, features, products, target definitions, and p2 repositories. Current packaging types include `eclipse-plugin`, `eclipse-test-plugin`, `eclipse-feature`, `eclipse-repository`, `eclipse-target-definition`, and `p2-installable-unit`.

## Reproducible build

- Use Maven Wrapper or a documented Maven floor and pin Tycho/build extensions.
- Define a reproducible target platform through `.target`, p2 repositories, or established BND/Tycho configuration.
- Avoid dependency resolution from the developer's running IDE.
- Keep qualifier generation deterministic where the release process requires reproducible outputs.
- Use Tycho's current `tycho-build` extension for supported pomless/structured builds; older `tycho-pomless` is deprecated.
- Build from a clean checkout and retain resolved-target diagnostics.

## Features, products, and p2

- Features group installable bundles and source features; keep included/plugin versions and licensing correct.
- Products define application, features/IUs, launchers, branding, start levels, and target environments.
- Use `eclipse-repository` and current category definitions for p2 repositories/update sites.
- Test repository metadata and artifacts with p2 installation, not only file existence.
- Preserve IU IDs and update paths. Renames/removals can strand installed users.
- Include a JRE in RCP products only through the project's deliberate JustJ/manual strategy and target matrix.

## Signing, SBOM, and supply chain

- Sign JARs/products according to organization and target-platform policy.
- Keep signing keys, keystores, passwords, timestamp credentials, and repository credentials in approved secret stores.
- Verify signatures after final packaging.
- Generate SBOMs where project or distribution policy requires them and reconcile bundled/transitive content.
- Record checksums, build environment, target repositories, source revision, and signing identity.

## Release gate

1. Validate manifests, extension schemas, features, products, and target platform.
2. Run unit, plug-in, integration/UI, and API baseline tests.
3. Build features/products/p2 repositories from clean state.
4. Install/update/uninstall from the generated p2 repository in a clean runtime.
5. Verify platform filters, source bundles, licenses, signatures, checksums, and SBOM.
6. Review semantic versions, qualifiers, release notes, and rollback repository.

## Publication boundary

Uploading p2 repositories, changing composite repositories, Marketplace submissions, signing with production keys, and promoting release channels are external writes requiring explicit authorization. Prepare artifacts and a publication plan locally when authorization is absent.

## Official sources

- https://tycho.eclipseprojects.io/doc/main/index.html
- https://tycho.eclipseprojects.io/doc/main/PackagingTypes.html
- https://tycho.eclipseprojects.io/doc/main/TychoBuildExtension.html
- https://tycho.eclipseprojects.io/doc/main/TestingBundles.html
- https://tycho.eclipseprojects.io/doc/main/Products.html
- https://tycho.eclipseprojects.io/doc/main/BuildingSites.html
- https://tycho.eclipseprojects.io/doc/main/IncludeJRE.html
- https://tycho.eclipseprojects.io/doc/main/SBOM.html
