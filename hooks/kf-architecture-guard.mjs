import { existsSync } from "node:fs";
import { join } from "node:path";

let input = "";
process.stdin.on("data", (chunk) => {
  input += chunk;
});
process.stdin.on("end", () => {
  try {
    const skillsDir = join(process.env.HOME, ".agents", "skills");
    const hasDesign = existsSync(join(skillsDir, "architecture-design"));
    const hasEnforce = existsSync(join(skillsDir, "architecture-enforce"));

    if (!hasDesign && !hasEnforce) {
      process.exit(0);
      return;
    }

    const parts = [];
    if (hasDesign) {
      parts.push(
        `\`architecture-design\` is installed - use for architecture selection, system decomposition, ADRs, flow diagrams, and quality-attribute tradeoffs. 11-phase gate workflow, evidence-based.`,
      );
    }
    if (hasEnforce) {
      parts.push(
        `\`architecture-enforce\` is installed - use to enforce dependency rules, module boundaries, public API contracts, and cross-language ownership.`,
      );
    }

    process.stdout.write(`[agent-skill] ${parts.join(" ")}\n`);
  } catch {
    // fail open
  }
  process.exit(0);
});
