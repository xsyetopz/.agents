# Biome 2.5.10 baseline

Use this policy when initializing a new Bun project or when the repository already uses Biome.

## New project without Biome

1. Confirm that neither `biome.json` nor `biome.jsonc` exists.
2. Install the exact development dependency:

   ```bash
   bun add --dev --exact @biomejs/biome@2.5.10
   ```

3. Copy the package [Biome template](../assets/biome.json) to the project root as `biome.json`.
4. Keep the template unchanged unless the repository has an explicit configuration requirement. Do not add the `react` domain.
5. Run `bunx biome check .` and the repository's applicable checks.

`biome.json` is an established Biome configuration format, not a custom schema or generated output.

## Existing Biome configuration

- Preserve the existing filename, rules, domains, includes, formatter settings, and other behavior.
- Change only the Biome version: pin `@biomejs/biome` to `2.5.10` and update an existing Biome schema URL to `https://biomejs.dev/schemas/2.5.10/schema.json`.
- Do not replace an existing file with the template. Do not add missing template fields or remove any existing fields if the repository already owns it.
- Run `bun install`, `bunx biome check .`, and the repository's applicable lint and format checks.

## Existing ESLint or Prettier

Biome 2.5.10 is a candidate replacement, not a Bun runtime feature. Migrate existing ESLint or Prettier.
