# Version Fetching

## Use this reference

Load this reference when version fetching is part of the GitHub or GitLab API task. Resolve platform, host, repository, target, read/write intent, permissions, and response evidence before applying commands.

Patterns for fetching release versions across platforms.

## GitHub - latest release

```bash
# gh CLI - one-liner
gh release view --repo owner/repo --json tagName -q '.tagName'

# Raw API
curl -sS https://api.github.com/repos/owner/repo/releases/latest | jq -r '.tag_name'

# Handle prereleases - get latest non-prerelease
gh api /repos/owner/repo/releases --jq '
  [.[] | select(.prerelease == false)] | .[0].tag_name
'
```

## GitLab - latest release

```bash
# glab CLI
glab release view --repo owner/repo latest

# Raw API - first result sorted by date
curl -sS -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/$PROJECT_ID/releases?per_page=1" \
  | jq -r '.[0].tag_name'
```

## Comparing versions

### Semver comparison

```bash
# Using sort -V (version sort)
printf "v1.2.3\nv1.10.0\nv1.2.10" | sort -V | tail -1
# -> v1.10.0

# Is a version newer than another?
[ "$(printf '%s\n%s' 'v1.2.3' 'v1.3.0' | sort -V | tail -1)" = "v1.3.0" ] && echo newer
```

### Find latest across repos

```bash
# Multiple repos, find latest version
for repo in owner/repo1 owner/repo2 owner/repo3; do
  tag=$(gh release view --repo "$repo" --json tagName -q '.tagName' 2>/dev/null)
  printf '%s\t%s\n' "$tag" "$repo"
done | sort -V
```

### Check if a newer version exists

```bash
# GitHub
current="v1.2.3"
latest=$(gh release view --repo owner/repo --json tagName -q '.tagName')
if [ "$(printf '%s\n%s' "$current" "$latest" | sort -V | tail -1)" != "$current" ]; then
  echo "Update available: $current -> $latest"
fi
```

## Release assets

```bash
# GitHub - download a release asset by name pattern
gh release download --repo owner/repo --pattern '*.tar.gz' --dir /tmp

# GitHub - get download URL for a specific asset
gh release view --repo owner/repo --json assets -q '
  .assets[] | select(.name | endswith(".tar.gz")) | .url
'

# GitHub - download via API (requires redirect follow)
asset_url=$(gh api /repos/owner/repo/releases/latest \
  --jq '.assets[] | select(.name == "binary-linux-amd64").url')
curl -sSL -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/octet-stream" \
  -o binary "$asset_url"
```

## Git tags vs releases

Not all tags are releases. On GitHub, a release wraps a tag with metadata. Use
releases endpoints when you need release notes, assets, or publish dates. Use
tags endpoints when you only need the tag names.

```bash
# All tags (lightweight + annotated)
git ls-remote --tags --sort=version:refname https://github.com/owner/repo.git

# Releases only (with metadata)
gh release list --repo owner/repo --limit 10
```
