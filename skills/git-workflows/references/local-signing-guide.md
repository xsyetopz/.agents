# Commit Signing

Scope: local commit and tag signing with GNU Privacy Guard (GPG) or Secure Shell (SSH) keys. A locally valid signature is not hosted verification until the provider has the matching public key and displays the verification result.

## Why sign

Signing verifies that a commit was made by the claimed author. Required for some
orgs and open-source projects. GitHub shows a "Verified" badge on signed
commits.

## GPG signing

The configuration examples below change user-level signing defaults and export public-key material. Confirm the key identity and destination before running them; do not disclose private keys, and treat hosted verification as `UNVERIFIED` until the provider confirms it.

### GPG setup

```bash
# Generate a GPG key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format LONG

# Export public key
gpg --armor --export YOUR_KEY_ID
```

### Configure git

```bash
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true     # sign all commits
git config --global tag.gpgsign true        # sign all tags
```

### Sign a single commit

```bash
git commit -S -m "Signed commit"
```

### Verify signatures

```bash
git log --show-signature
git verify-commit HEAD
git verify-tag v1.0.0
```

### Add GPG key to GitHub/GitLab

1. Export: `gpg --armor --export YOUR_KEY_ID`
2. Copy the output (including `-----BEGIN PGP PUBLIC KEY BLOCK-----`)
3. GitHub: Settings -> SSH and GPG keys -> New GPG key
4. GitLab: Preferences -> GPG Keys

## SSH signing

Git 2.34+ supports signing with SSH keys.

### SSH setup

```bash
# Use existing SSH key or generate a new one
ssh-keygen -t ed25519 -C "email@example.com"

# Configure git
git config --global user.signingkey path/to/id_ed25519.pub
git config --global gpg.format ssh
git config --global gpg.ssh.allowedSignersFile path/to/allowed_signers
git config --global commit.gpgsign true
```

### Verify

```bash
git log --show-signature
```

### Add SSH key to GitHub/GitLab

Use the same key you use for SSH authentication. GitHub: Settings -> SSH and GPG
keys -> New SSH key -> choose "Signing Key" type. GitLab: Preferences -> SSH
Keys.

## Troubleshooting

**"error: gpg failed to sign the data"**: GPG agent isn't running.

```bash
export GPG_TTY=$(tty)
gpgconf --kill gpg-agent
```

**No passphrase prompt in GUI/IDE**: Set `pinentry` mode:

```bash
# User-level GnuPG config file (for example, path/to/gpg-agent.conf)
pinentry-program path/to/pinentry-mac  # macOS
# or: path/to/pinentry-tty
```

**"No secret key"**: Your `signingkey` doesn't match a secret key on the
machine. Check: `gpg --list-secret-keys --keyid-format LONG`

**"gpg.ssh.allowedSignersFile" error**: Create the file:

```bash
echo "$(git config --get user.email) $(cat path/to/id_ed25519.pub)" > path/to/allowed_signers
```

## Sources

- Git Workflows source map (see `local-sources.md`) — Git signing and hosted-boundary references.
- [Git commit documentation](https://git-scm.com/docs/git-commit) and [GitHub authentication documentation](https://docs.github.com/en/authentication) — local signing and provider verification boundaries.
