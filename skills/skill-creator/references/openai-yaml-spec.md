# openai.yaml Specification

## Use this reference

Load this reference when openai yaml spec is part of the skill-authoring task. Keep the discovery description precise, the entry instructions lean, details progressively disclosed, and behavior independently verifiable.

`agents/openai.yaml` is a product-specific config read by OpenAI-compatible
runtimes. It is read by the machine/harness, not the agent.

## Required fields

```yaml
interface:
  display_name: "Human-Facing Title"
  short_description: "25-64 char blurb for UI lists"
  default_prompt: "Use $skill-name to do X."
```

### interface.display_name

Human-facing title shown in UI skill lists and chips. Title case, 2-6 words.

### interface.short_description

Human-facing short UI blurb for quick scanning. 25-64 characters.

### interface.default_prompt

Default prompt snippet inserted when invoking the skill. Typically one sentence.
Must mention the skill as `$skill-name` (e.g. `"Use $git-ci-cd to ..."`).

## Optional fields

### interface.icon_small

Path to a small icon asset relative to the skill directory. Default to
`./assets/` and place the icon in the skill's `assets/` folder.

```yaml
  icon_small: "./assets/icon-400px.png"
```

### interface.icon_large

Path to a larger logo asset relative to the skill directory.

```yaml
  icon_large: "./assets/logo.svg"
```

### interface.brand_color

Hex color used for UI accents such as badges.

```yaml
  brand_color: "#3B82F6"
```

### dependencies.tools

List of tool dependencies, currently only `mcp` type is supported.

```yaml
dependencies:
  tools:
    - type: "mcp"
      value: "github"
      description: "GitHub MCP server for repository operations"
      transport: "streamable_http"
      url: "https://api.githubcopilot.com/mcp/"
```

## Full example

```yaml
interface:
  display_name: "Git CI/CD Pipeline Designer"
  short_description: "Author and debug CI/CD across platforms"
  icon_small: "./assets/icon-400px.png"
  icon_large: "./assets/logo.svg"
  brand_color: "#F05032"
  default_prompt: "Use $git-ci-cd to design, debug, or modify CI/CD pipelines."

dependencies:
  tools:
    - type: "mcp"
      value: "github"
      description: "GitHub MCP server"
      transport: "streamable_http"
      url: "https://api.githubcopilot.com/mcp/"
```

## Quoting

- Quote all string values
- Keep keys unquoted
- YAML 1.2 compatible
