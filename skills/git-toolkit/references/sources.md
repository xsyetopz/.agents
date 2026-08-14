# Git Toolkit source map

This map distinguishes Git's local command semantics from hosted-provider
boundary documentation. A `Checked` date means the linked page was opened
while this package was revised on 2026-08-14; an unmarked or `UNVERIFIED`
entry must be checked before relying on a current claim. The operational
examples remain local guidance and never prove a remote effect.

| Scope | Authoritative source | Status |
| --- | --- | --- |
| Git commands, configuration, hooks, refs, and recovery semantics | [Git reference](https://git-scm.com/docs) | Checked 2026-08-14 |
| Conceptual Git workflows and history model | [Pro Git book](https://git-scm.com/book/en/v2) | Checked 2026-08-14 |
| Git Large File Storage (LFS) behavior | [Git LFS](https://git-lfs.com/) | UNVERIFIED in this pass |
| GitHub large-file and signature verification boundary | [About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage) | Checked 2026-08-14 |
| GitHub hosted branch and commit settings (not local execution) | [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches) | Checked 2026-08-14 |
| GitLab hosted branch settings (not local execution) | [GitLab protected branches](https://docs.gitlab.com/ee/user/project/protected_branches.html) | UNVERIFIED in this pass |
| Bitbucket hosted branch permissions (not local execution) | [Bitbucket branch permissions](https://support.atlassian.com/bitbucket-cloud/docs/use-branch-permissions/) | Checked 2026-08-14 |
| Semantic Versioning (SemVer) precedence | [Semantic Versioning 2.0.0](https://semver.org/) | Checked 2026-08-14 |
| Secret scanning and history-rewrite safety | [GitHub secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning) | Checked 2026-08-14 |

Local status, history, staging, recovery, and worktree state must be inspected
in the target checkout. Hosted settings, signatures, hooks installed outside
the checkout, and network-backed LFS objects remain `UNVERIFIED` until directly
observed. Destructive commands require exact authorization and a recovery plan.
