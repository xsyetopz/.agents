export function greeting(name: string): string {
  const trimmed = name.trim();
  return `Hello, ${trimmed || "workspace"}.`;
}
