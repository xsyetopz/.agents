# Commit Signing

## Use this reference

Load this reference when signing guide is part of the requested local Git state transition. Inspect current status and history first, preserve unrelated work, identify recovery, and verify the resulting state.

## Why sign

Signing verifies that a commit was made by the claimed author. Required for some
orgs and open-source projects. GitHub shows a "Verified" badge on signed
commits.

## GPG signing

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
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global gpg.format ssh
git config --global gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
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
# ~/.gnupg/gpg-agent.conf
pinentry-program /opt/homebrew/bin/pinentry-mac  # macOS
# or: /usr/bin/pinentry-tty
```

**"No secret key"**: Your `signingkey` doesn't match a secret key on the
machine. Check: `gpg --list-secret-keys --keyid-format LONG`

**"gpg.ssh.allowedSignersFile" error**: Create the file:

```bash
echo "$(git config --get user.email) $(cat ~/.ssh/id_ed25519.pub)" > ~/.ssh/allowed_signers
```
