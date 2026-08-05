# GitHub GraphQL API

## Use this reference

Load this reference when github graphql is part of the GitHub or GitLab API task. Resolve platform, host, repository, target, read/write intent, permissions, and response evidence before applying commands.

Endpoint: `POST https://api.github.com/graphql`

## When to use

GraphQL is more efficient than REST when you need multiple related data points
in a single request. Use it for complex queries that would require 3+ REST
calls.

## Auth

```bash
gh api graphql -f query='
  query {
    viewer { login }
  }
'
```

## Common queries

### Latest release with assets

```graphql
query {
  repository(owner: "owner", name: "repo") {
    latestRelease {
      tagName
      name
      publishedAt
      releaseAssets(first: 10) {
        nodes {
          name
          downloadUrl
          size
        }
      }
    }
  }
}
```

### Repository info with recent releases

```graphql
query {
  repository(owner: "owner", name: "repo") {
    nameWithOwner
    stargazerCount
    defaultBranchRef { name }
    releases(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        tagName
        name
        publishedAt
      }
    }
  }
}
```

### Search repositories

```graphql
query {
  search(query: "topic:cli language:rust stars:>1000", type: REPOSITORY, first: 10) {
    repositoryCount
    edges {
      node {
        ... on Repository {
          nameWithOwner
          stargazerCount
          description
        }
      }
    }
  }
}
```

### Check PR CI status

```graphql
query {
  repository(owner: "owner", name: "repo") {
    pullRequest(number: 42) {
      title
      state
      commits(last: 1) {
        nodes {
          commit {
            statusCheckRollup {
              state
            }
          }
        }
      }
    }
  }
}
```

## Using with `gh`

```bash
# Inline query
gh api graphql -f query='query { viewer { login } }'

# From file
gh api graphql --input query.graphql

# With variables
gh api graphql -F owner=vercel -F name=next.js -f query='
  query($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
      stargazerCount
    }
  }
'

# Extract with jq
gh api graphql -f query='...' --jq '.data.repository.stargazerCount'
```

## Pagination

GraphQL uses cursor-based pagination:

```graphql
releases(first: 10, after: $cursor, orderBy: ...) {
  nodes { ... }
  pageInfo { endCursor hasNextPage }
}
```
