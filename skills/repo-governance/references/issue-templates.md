# Issue Templates

## Use this reference

Load this reference when issue templates is part of the governance task. Give each rule one audience, scope, owner, precedence, enforcement mechanism, and validation path.

Configuring `.github/ISSUE_TEMPLATE/` with YAML forms. Source:
[GitHub issue template docs](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository).

## File structure

```text
.github/
├── ISSUE_TEMPLATE/
│   ├── config.yml          # Template chooser configuration
│   ├── 1-bug.yml           # Bug report form
│   ├── 2-feature.yml       # Feature request form
│   └── 3-epic.yml          # Epic/tracking issue form
└── pull_request_template.md
```

Ordering: files are listed alphanumerically grouped by filetype (YAML before
Markdown). Prefix with numbers for explicit ordering. For 10+ templates,
use zero-padded prefixes (`01-`, `02-`, ..., `11-`).

## Template chooser (config.yml)

```yaml
blank_issues_enabled: false  # Force template use for external contributors
contact_links:
  - name: Community Discussions
    url: https://github.com/owner/repo/discussions
    about: Ask questions and share ideas here.
  - name: Security Vulnerability
    url: https://github.com/owner/repo/security/advisories/new
    about: Report security vulnerabilities privately.
```

When `blank_issues_enabled: false`, users with Read/Triage roles only see
configured templates. Write+ roles still see a "Blank issue" option labeled
"Maintainers only."

## Bug report form (1-bug.yml)

```yaml
name: Bug Report
description: File a bug report.
title: "[Bug]: "
labels: ["bug", "triage"]
type: bug
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report.

  - type: input
    id: version
    attributes:
      label: Version
      description: What version are you running?
      placeholder: "2.1.0"
    validations:
      required: true

  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Steps to reproduce, expected vs actual behavior.
      placeholder: |
        1. Run `tool --flag`
        2. Open file X
        3. See error Y
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: Operating System
      options:
        - macOS
        - Linux
        - Windows
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant log output
      description: Paste any relevant logs. Automatically code-formatted.
      render: shell

  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      options:
        - label: I agree to follow this project's Code of Conduct
          required: true
```

## Feature request form (2-feature.yml)

```yaml
name: Feature Request
description: Suggest a new feature.
title: "[Feature]: "
labels: ["enhancement"]
type: feature
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem does this feature solve? Be specific.
    validations:
      required: true

  - type: textarea
    id: proposal
    attributes:
      label: Proposed solution
      description: Describe the feature. Include API design, CLI interface, or UI mockups.
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      description: What workarounds exist today? Why aren't they sufficient?

  - type: checkboxes
    id: scope
    attributes:
      label: Scope
      options:
        - label: I'm willing to contribute this feature
```

## Field types reference

| Type | Use case |
| --- | --- |
| `markdown` | Free-text section (instructions, links) |
| `input` | Single-line text (version, email, URL) |
| `textarea` | Multi-line text (description, logs, steps) |
| `dropdown` | Single or multi-select from predefined options |
| `checkboxes` | Multiple boolean options (agreements, scope) |
| `upload` | File attachment (screenshots, logs) |

## Anti-patterns

1. **Too many required fields.** Every required field increases the chance the
   user will close the tab. Only require what's strictly necessary for triage.

2. **Generic templates.** A single "Issue" template with no structure collects
   noise. At minimum, separate bug from feature.

3. **No `config.yml`.** Without it, the "Blank issue" option appears alongside
   templates and external contributors bypass them.

4. **Template-only for external, blank for internal.** If internal contributors
   use blank issues and external use templates, your internal tracking rots.
   Use the same templates for everyone.

## PR templates

The companion to issue templates. Lives at `.github/pull_request_template.md`:

```markdown
## Description
<!-- What does this PR do? -->

## Related issues
<!-- Closes #123 -->

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Checklist
- [ ] Tests pass locally
- [ ] New tests added for new code
- [ ] Documentation updated
- [ ] CHANGELOG.md entry added
```
