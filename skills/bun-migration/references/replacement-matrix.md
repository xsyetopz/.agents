# Bun 1.4 replacement matrix

Use this table after inventorying active consumers. **Required** applies when the repository adopts Bun as its package manager. **Conditional** requires focused compatibility evidence before removal.

| Existing surface | Bun target | Decision | Prove before removal |
| --- | --- | --- | --- |
| Bun below 1.4 | Bun 1.4+ | Required | All active development, CI, image, and deployment pins changed |
| npm, pnpm, or Yarn installs | `bun install`, `bun ci`, `bun add`, `bun remove` | Required | Lockfile migration, lifecycle scripts, workspaces, catalogs, patches, and linker behavior |
| `npm run`, `pnpm run`, or Yarn scripts | `bun run` | Required | Script arguments and exit behavior |
| `npx`, `pnpx`, or `yarn dlx` | `bunx` | Required | CLI runs correctly under Bun |
| `concurrently` or `npm-run-all` | `bun run --parallel` or `--sequential` | Conditional | Selection, output, failure, and process termination semantics |
| `tsx` or `ts-node` | Direct `bun file.ts` | Conditional | Loader hooks and runtime behavior |
| Node.js | Bun runtime | Conditional | Native addons, loaders, workers, inspector, V8, and Node-version semantics |
| Deno | Bun runtime and scripts | Conditional | `Deno.*`, permissions, import maps, URL/JSR imports, tasks, KV, and Deploy APIs |
| Jest or Vitest | `bun test` | Conditional | Mocks, timers, snapshots, environments, browser mode, plugins, and reporters |
| Vite | Bun HTML server and `bun build` | Conditional | Framework adapters, plugins, SSR, proxy, environment, Rollup, and library output |
| webpack or esbuild | `bun build` | Conditional | Loaders, plugins, transforms, output, and metadata consumers |
| `dotenv` | Bun environment loading | Conditional | Parse, precedence, override, and load-order behavior |
| `node-fetch` or standard `undici` use | Global `fetch` | Conditional | Proxy, agent, stream, and error behavior |
| `ws` | Bun WebSocket APIs | Conditional | Client/server architecture and protocol behavior |
| SQLite, SQL, Redis, image, Markdown, cron, or PTY libraries | Relevant Bun API | Conditional | Full API, platform, operational, and data compatibility |
| TypeScript typechecking or declarations | Existing TypeScript tool | Keep | Bun transpilation does not replace these checks |
| New Bun project without Biome | `@biomejs/biome@2.5.10` plus the package `biome.json` template | Recommended | Generate only when neither `biome.json` nor `biome.jsonc` exists; omit the `react` domain |
| Existing Biome configuration | Biome 2.5.10 | Version-only | Preserve the file; update only the package version and an existing schema URL |
| Existing ESLint or Prettier | Biome 2.5.10 | Conditional | Verify rules, plugins, ignores, scripts, editor integration, and formatting before removal |

When a conditional replacement fails, keep the tool and run it under Bun where supported. Describe that as the existing tool running under Bun rather than a native replacement.

## Primary sources

- [Bun 1.4 release notes](https://bun.com/blog/bun-v1.4)
- [Package manager](https://bun.com/docs/pm)
- [Lockfile](https://bun.com/docs/pm/lockfile)
- [Workspaces](https://bun.com/docs/pm/workspaces)
- [Test runner](https://bun.com/docs/test)
- [Bundler](https://bun.com/docs/bundler)
- [Vite guidance](https://bun.com/docs/guides/ecosystem/vite)
- [CI guidance](https://bun.com/docs/guides/runtime/cicd)
