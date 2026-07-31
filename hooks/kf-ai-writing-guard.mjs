import { existsSync } from "node:fs";
import { join } from "node:path";

let input = "";
process.stdin.on("data", (chunk) => {
  input += chunk;
});
process.stdin.on("end", () => {
  try {
    const skillDir = join(
      process.env.HOME,
      ".agents",
      "skills",
      "avoid-ai-writing",
    );
    if (!existsSync(skillDir)) {
      process.exit(0);
      return;
    }

    process.stdout.write(`
[agent-skill] The \`avoid-ai-writing\` skill is installed and available. Use it to audit, detect, or rewrite text that may contain AI writing patterns. Modes: rewrite (default), detect (flag only), edit (file in-place). Voice profiles: casual, professional, technical, warm, blunt. Trigger: mention "remove AI-isms", "clean up AI writing", "audit writing for AI tells", or similar.
`);
  } catch {
    // fail open
  }
  process.exit(0);
});
