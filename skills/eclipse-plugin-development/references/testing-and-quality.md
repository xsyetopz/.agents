# Eclipse plug-in testing and quality

## Test layers

1. Plain JUnit tests for OSGi/Eclipse-independent logic.
2. JUnit Plug-in tests inside an Equinox/Eclipse runtime.
3. Tycho Surefire tests in reproducible CI target platforms.
4. SWTBot or repository-standard UI automation for user flows requiring widgets.
5. Product/update-site installation and startup smoke tests.
6. API Tools baseline and versioning analysis.

Do not replace runtime tests with mocks when extension registry, OSGi services, adapters, resources, preferences, or workbench behavior is the contract.

## PDE and runtime tests

- Use the JUnit Plug-in Test launcher for local development and preserve launch configurations only when repository policy tracks them.
- Select the minimum bundle set needed by the test launch; avoid silently using the entire development IDE.
- Use clean runtime workspaces and configuration areas.
- Test UI and non-UI thread modes correctly.
- Restore preferences, extension registrations, services, workspace resources, jobs, and system properties.
- Wait for Jobs through job families/rules and observable state rather than sleeps.
- Close workbench windows/editors and dispose SWT resources created by tests.

## Tycho tests

- Preserve `eclipse-test-plugin` packaging in existing projects, but for new designs prefer `eclipse-plugin` with a configured `tycho-surefire-plugin:plugin-test` execution as current Tycho guidance recommends.
- Configure `tycho-surefire-plugin` with explicit application/product, dependencies, UI harness, JVM arguments, and test includes.
- Keep target-platform resolution deterministic and fail on missing IUs rather than falling back to the local installation.
- Separate unit, plug-in, integration, and UI test phases when they have different runtime requirements.
- Capture test runtime logs and `.metadata/.log` on failure.

## API and version checks

- Maintain an API baseline for exported packages and extension points when the project publishes API.
- Run PDE API Tools or Tycho API Tools integration to detect binary/source compatibility and version errors.
- Review leaks of internal packages into public signatures.
- Update bundle/package versions according to actual compatibility changes, not merely because a file changed.
- Validate extension-point schemas and examples when consumers exist.

## Behavior cases

- Bundle/DS activation and deactivation, missing optional service, dynamic service arrival/removal.
- Extension registry metadata and lazy class creation.
- Commands/handlers: selection, active part, enablement expressions, keybindings, cancellation.
- Workspace: deltas, scheduling rules, linked/derived resources, refresh, read-only resources, project close/delete.
- UI: display-thread access, disposal during async callback, theme/DPI, accessibility, workbench restart.
- Jobs: cancellation, priority, family joining, conflicting scheduling rules, error status.
- Preferences/secure storage: scopes, defaults, migration, corrupt values, unavailable secure storage.
- p2/product: install, update, rollback/uninstall, missing dependency, platform filters.

## Matrix and performance

- Test the minimum supported target platform and newest declared target.
- Test relevant operating systems/window systems when native SWT behavior or fragments differ.
- Keep current release testing separate from future milestone/RC early-warning jobs.
- Measure bundle activation, UI responsiveness, job contention, workspace scanning, and memory/resource leaks.
- Avoid early startup, full workspace traversal, synchronous UI I/O, excessive resource listeners, and leaked OSGi trackers.

## Official sources

- https://help.eclipse.org/latest/topic/org.eclipse.pde.doc.user/guide/tools/launchers/junit_launcher.htm
- https://help.eclipse.org/latest/topic/org.eclipse.pde.doc.user/guide/tools/launchers/eclipse_application_launcher.htm
- https://help.eclipse.org/latest/topic/org.eclipse.pde.doc.user/guide/tools/launchers/plugins.htm
- https://tycho.eclipseprojects.io/doc/main/TestingBundles.html
- https://tycho.eclipseprojects.io/doc/main/tycho-surefire-plugin/plugin-info.html
- https://help.eclipse.org/latest/topic/org.eclipse.pde.doc.user/tasks/api_tooling_setup.htm
