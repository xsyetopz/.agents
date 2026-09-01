# Eclipse platform and architecture

Verified against Eclipse Platform/PDE and Tycho documentation on 2026-09-01. Eclipse 2026-06 (Platform 4.40) was the current released train. Tycho 5.0.4 was the current stable documentation found; Tycho `main` also contained 6.0.0-SNAPSHOT material. Use the repository's pinned release, not snapshot documentation, unless snapshot adoption is requested.

## Bundle metadata

PDE coordinates several files:

- `META-INF/MANIFEST.MF`: OSGi identity, version, execution environment, imports/requirements, exports, activation, localization, and classpath.
- `plugin.xml`: Eclipse extensions and extension points.
- `fragment.xml`: fragment contributions.
- `build.properties`: source/output and packaged resources.
- `OSGI-INF/*.xml`: Declarative Services components when XML descriptors are used.
- `.target`: reproducible target platform.
- `feature.xml`, `.product`, `category.xml`: distribution composition.

Use the PDE manifest editor/organize-manifest tooling where useful, but review resulting source changes. Keep generated and hand-authored ownership clear.

## Identity and versions

- Bundle symbolic names are stable public IDs.
- OSGi versions have `major.minor.micro.qualifier`; package export versions and bundle versions serve different compatibility purposes.
- Increment major for breaking API, minor for compatible API additions, and micro for implementation fixes according to project policy.
- Use version ranges deliberately. Overly broad ranges can resolve incompatible APIs; overly narrow ranges prevent valid updates.
- Use `Bundle-RequiredExecutionEnvironment`/current execution-environment metadata consistent with target platform and compiler.
- Mark a bundle singleton only when extension-registry or singleton semantics require it.

## Dependencies

- Prefer `Import-Package` for service/package coupling when project conventions support it; `Require-Bundle` couples to a bundle's identity and exports.
- Export only supported API packages. Keep implementation packages unexported.
- Re-export dependencies only when they are intentionally part of the consumer API.
- Avoid split packages and buddy-policy/classloader workarounds.
- Use optional/dynamic imports only when code remains correct without the dependency and lifecycle changes are handled.
- Resolve against the target platform, not the development IDE installation.

## Extensions and services

- Extension points provide declarative, lazily instantiated contributions. Put enough metadata in `plugin.xml` to avoid loading classes for labels, icons, and enablement.
- Use stable IDs and schema validation. Treat extension-point schema as public API when other bundles contribute.
- Prefer Declarative Services for OSGi services, dependencies, activation, configuration, and lifecycle.
- Keep component activation cheap and avoid using service lookup during static initialization.
- Use activators only for genuine bundle start/stop ownership. Never perform long I/O, UI creation, or workspace scans in `start()`.
- Unregister services/listeners and cancel work during deactivation.

## API boundaries

- Use public packages documented for clients.
- Avoid `.internal` packages and API elements marked restricted, not intended to be implemented/subclassed/instantiated, or deprecated for removal.
- Check Eclipse API Tools and the current deprecated list before migration.
- Use adapters, extension points, services, commands/handlers, and dependency injection rather than reaching into workbench internals.
- Preserve binary compatibility for exported API and extension-point contracts.

## Concurrency and resources

- SWT widgets are display-thread confined. Use `Display.asyncExec`, `syncExec`, `UIJob`, or e4 `UISynchronize` only for bounded UI work.
- Use Eclipse Jobs for background operations, `IProgressMonitor` cancellation, job families, and workspace scheduling rules.
- Workspace writes should use workspace runnables/operations with correct resource scheduling rules.
- Avoid holding locks while calling UI synchronization or external code.
- Check widget/resource disposal before asynchronous UI updates.
- Dispose created SWT `Color`, `Font`, `Image`, and controls unless shared through a platform registry that owns them.

## Workspace and UI

- Use `IResource`/workspace APIs for workspace content and refresh/markers/deltas; raw filesystem edits require synchronization.
- Use commands/handlers and expressions for menu/toolbar enablement rather than legacy action delegates in new code.
- Keep views/editors responsive and support workbench save/restore lifecycle.
- Use JFace viewers, data binding, preferences, secure storage, and e4 injection according to existing architecture.
- Externalize visible strings, support mnemonics and keyboard navigation, use shared images/themes, and verify high DPI/dark theme.

## Official sources

- https://help.eclipse.org/latest/topic/org.eclipse.pde.doc.user/concepts/plugin.htm
- https://help.eclipse.org/latest/topic/org.eclipse.pde.doc.user/guide/tools/editors/manifest_editor/editor.htm
- https://help.eclipse.org/latest/topic/org.eclipse.platform.doc.isv/guide/runtime.htm
- https://help.eclipse.org/latest/topic/org.eclipse.platform.doc.isv/reference/api/overview-summary.html
- https://help.eclipse.org/latest/topic/org.eclipse.platform.doc.isv/reference/api/deprecated-list.html
- https://help.eclipse.org/latest/topic/org.eclipse.platform.doc.isv/guide/runtime_jobs.htm
- https://help.eclipse.org/latest/topic/org.eclipse.platform.doc.isv/guide/swt.htm
- https://help.eclipse.org/latest/topic/org.eclipse.platform.doc.isv/guide/workbench.htm
- https://www.eclipse.org/downloads/packages/release/2026-06/r
