# GOOD/RED CI/CD trust-boundary examples

Keep untrusted change execution separate from secrets and write-capable deployment jobs. **RED** is a contrast for review; use GOOD as the implementation pattern.

## Pull request code and deployment credentials

### GOOD

```diff
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@
+on:
+  pull_request:
+  push:
+    branches: [main]
+permissions:
+  contents: read
+jobs:
+  test:
+    steps:
+      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
+      - run: ./ci/test.sh
+  deploy:
+    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
+    permissions:
+      contents: read
+      deployments: write
```

### RED

```diff
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@
+on: pull_request_target
+jobs:
+  test:
+    steps:
+      - uses: actions/checkout@v4
+        with: {ref: ${{ github.event.pull_request.head.sha }}}
+      - run: ./ci/test.sh
+        env: {DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}}
```
