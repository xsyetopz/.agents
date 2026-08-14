# Submodules and Git LFS

Scope: local Git submodules and Git Large File Storage (LFS). A submodule records a commit in another repository; an LFS pointer records content stored by an LFS server. Both require network access and matching credentials for full content, so unavailable objects are `UNVERIFIED`.

## Submodules

Adding, updating, or removing a submodule changes tracked repository state and may fetch code from a remote. Confirm the URL and commit, inspect the diff, and authorize the commit before applying these examples.

### Add a submodule

```bash
git submodule add https://github.com/owner/repo.git path/to/sub
git commit -m "Add submodule: repo at path/to/sub"
```

### Clone with submodules

```bash
git clone --recurse-submodules https://github.com/owner/repo.git

# Or after a regular clone
git submodule update --init --recursive
```

### Update submodules

```bash
# Fetch latest for all submodules
git submodule update --remote

# Pull latest for each (and merge into the tracked branch)
git submodule foreach 'git pull origin $(git rev-parse --abbrev-ref HEAD)'
```

### Submodule status

```bash
git submodule status           # check tracked commits
git submodule foreach git status  # check for local changes in submodules
```

### Remove a submodule

```bash
git submodule deinit -f path/to/sub
git rm path/to/sub
rm -rf .git/modules/path/to/sub
git commit -m "Remove submodule"
```

### Update tracked commit

```bash
cd path/to/sub
git checkout main
git pull
cd ../..
git add path/to/sub
git commit -m "Update submodule to latest main"
```

### When to use subtrees instead

Submodules track a specific commit. Subtrees copy the code into the repo. Use
subtrees when you want to modify the dependency's code inline. Use submodules
when the dependency is external and versioned independently.

## Git LFS

### Setup

```bash
git lfs install
git lfs track "*.psd" "*.zip" "*.mp4"
git add .gitattributes
git commit -m "Configure LFS tracking"
```

### Verify tracking

```bash
git lfs track          # list tracked patterns
git lfs ls-files       # list LFS-tracked files in HEAD
```

### Migrate existing files to LFS

```bash
# Migrate all .zip files in history to LFS
git lfs migrate import --include="*.zip" --everything

# Migrate files in a specific branch
git lfs migrate import --include="*.png" --include-ref=main
```

`--everything` rewrites all branches and tags - use with caution on shared
repos.

### Fetch LFS objects

```bash
git lfs fetch            # fetch all
git lfs fetch --all      # fetch for all branches
git lfs pull             # fetch + checkout
```

### Common issues

**Clone is slow or hangs**: LFS objects are fetched during clone. Use
`GIT_LFS_SKIP_SMUDGE=1 git clone ...` to skip, then `git lfs pull` selectively.

**File has pointer instead of content**: LFS didn't download the object. Run
`git lfs pull`.

**Can't push LFS objects**: The LFS server may reject large files. Check your
quota.

```bash
# Debug LFS operations
GIT_TRACE=1 GIT_TRANSFER_TRACE=1 GIT_CURL_VERBOSE=1 git lfs push origin main
```

## Sources

- [Git Toolkit source map](sources.md) — Git, LFS, and hosted-boundary references.
- [Git submodule documentation](https://git-scm.com/docs/git-submodule) and [Git LFS](https://git-lfs.com/) — command and storage semantics (LFS page unverified in this pass).
