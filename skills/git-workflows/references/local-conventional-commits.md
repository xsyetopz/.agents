# Conventional Commits fallback

Use this fallback only when the repository has no contribution or commit-message guidance.

Conventional Commit subjects complement, but do not replace, the required commit-slicing contract in [SKILL.md](../SKILL.md). A valid subject is not sufficient: before staging each commit, define its one coherent purpose, explicit paths or hunks, dependency/order, validation, and revert consequence. Mixed worktrees use explicit file or hunk staging, and a commit is accepted only when its staged diff matches that slice.

## Detect existing authority

Inspect before adding policy or hooks:

- Repository instructions and contribution files such as `AGENTS.md`, `CONTRIBUTING*`, `COMMIT*`, `.github/`, `docs/`, and relevant `README*` sections.
- Commit templates, `commitlint`, gitlint, Lefthook, pre-commit, Husky, tracked hook directories, package scripts, and the effective `core.hooksPath`.
- Recent accepted commit subjects as evidence of established practice, not authority by themselves.

If any repository-owned contribution or commit guidance exists, follow it. Keep the repository-owned policy and hook unless the user explicitly requests a policy change.

## Install the fallback

When no guidance exists and the task authorizes repository commit-workflow changes:

1. Adopt Conventional Commits for new commit subjects: `type(scope): description`. The scope is optional; `!` may mark a breaking change.
2. Stage only the planned paths or hunks for each slice. Use file-based staging for separable files and `git add -p` for separable hunks; do not use giant staging patterns.
3. If the repository already owns a hook manager or tracked hook path, add an equivalent `commit-msg` hook through that mechanism. Extend the existing hook manager rather than creating a parallel system.
4. Otherwise copy the package [commit-msg hook](../assets/commit-msg) to `.githooks/commit-msg`.
5. Run:

   ```bash
   chmod +x .githooks/commit-msg
   git config --local core.hooksPath .githooks
   ```

6. Verify one accepted and one rejected message by invoking the hook with temporary message files. Before each commit, inspect `git diff --cached --check`, `git diff --cached`, the staged path inventory, and the proposed subject. Then create the requested commit and inspect its subject. The hook validates the subject only; it does not establish that the staged diff is a coherent, revertable slice.

The tracked hook is an established Git repository mechanism. The local `core.hooksPath` setting is per clone; do not claim that cloning the hook file activates it for other contributors.

## Hook behavior

The fallback accepts any lowercase Conventional Commit type, an optional scope, an optional breaking-change marker, and a non-empty description. It also allows Git merge and revert subjects plus temporary `fixup!` and `squash!` commits. It does not impose a project-specific type list or subject-length limit.

Local hooks can be bypassed with `--no-verify`; hosted enforcement requires separately authorized server or CI configuration.
