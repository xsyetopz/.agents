#!/usr/bin/env bash
# Exercise one project-scoped skill install/list/remove cycle in a disposable
# fixture. The Vercel CLI is intentionally pinned; changing the pin requires
# a new help probe and a new review of removal semantics.

set -Eeuo pipefail

readonly CLI_VERSION="1.5.22"
readonly SKILL_NAME="skill-creator"
readonly TARGET_AGENT="codex"

die() {
  local code="$1"
  shift
  printf 'skills-cli-smoke: %s\n' "$*" >&2
  exit "$code"
}

usage() {
  cat >&2 <<'EOF'
Usage: RUNNER=npx|bunx SOURCE=/path/to/my-agent-skills-btw scripts/skills_cli_smoke.sh

Runs a network-backed, project-scoped add/list/remove probe with the pinned
Vercel skills CLI. The fixture installs skill-creator alongside one unrelated
local skill, then proves targeted removal preserves that unrelated skill.
SOURCE defaults to the repository containing this script. The fixture, HOME,
and CODEX_HOME are temporary and are removed on exit.

Exit codes:
  0  install, list, removal, and lock assertions passed
  2  usage or required dependency error
  3  source or fixture precondition failed
  4  pinned CLI contract or assertion failed
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi
if [[ $# -ne 0 ]]; then
  usage
  die 2 "unexpected argument: $1"
fi

RUNNER="${RUNNER:-npx}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
SOURCE="${SOURCE:-$REPO_ROOT}"

case "$RUNNER" in
  npx)
    CLI=(npx -y "skills@${CLI_VERSION}")
    ;;
  bunx)
    # --bun is the verified Bun launcher shape for skills@1.5.22.
    CLI=(bunx --bun "skills@${CLI_VERSION}")
    ;;
  *)
    usage
    die 2 "RUNNER must be npx or bunx (got: $RUNNER)"
    ;;
esac

command -v python3 >/dev/null 2>&1 || die 2 "python3 is required to assert JSON and lock state"
command -v git >/dev/null 2>&1 || die 2 "git is required for the disposable project fixture"
command -v "$RUNNER" >/dev/null 2>&1 || die 2 "$RUNNER is not available"

if [[ "$SOURCE" != /* ]]; then
  SOURCE="$(cd -- "$SOURCE" 2>/dev/null && pwd -P)" || die 3 "SOURCE does not resolve: $SOURCE"
fi
[[ -d "$SOURCE/skills/$SKILL_NAME" ]] || die 3 "SOURCE is missing skills/$SKILL_NAME: $SOURCE"
[[ -f "$SOURCE/skills/$SKILL_NAME/SKILL.md" ]] || die 3 "SOURCE is missing skills/$SKILL_NAME/SKILL.md"

TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/my-agent-skills-smoke.XXXXXX")" || die 3 "could not create a temporary directory"
TMP_ROOT="$(cd -- "$TMP_ROOT" && pwd -P)" || die 3 "could not resolve the temporary directory"
cleanup() {
  if [[ "${KEEP_TMP:-0}" == "1" ]]; then
    printf 'skills-cli-smoke: KEEP_TMP=1; fixture retained at %s\n' "$TMP_ROOT" >&2
    return
  fi
  rm -rf -- "$TMP_ROOT"
}
trap cleanup EXIT

PROJECT="$TMP_ROOT/project"
mkdir -p -- "$PROJECT" "$TMP_ROOT/home" "$TMP_ROOT/codex-home"
printf '%s\n' '{"private":true}' > "$PROJECT/package.json"
git -C "$PROJECT" init -q || die 3 "could not initialize disposable Git project"

# Keep npm/Bun and Codex discovery inside the fixture. The CLI still receives
# a project-scoped destination; no global install/list/remove operation is run.
export HOME="$TMP_ROOT/home"
export CODEX_HOME="$TMP_ROOT/codex-home"
cd -- "$PROJECT"

log_command() {
  printf 'skills-cli-smoke: ' >&2
  printf '%q ' "$@" >&2
  printf '\n' >&2
}

run_cli() {
  log_command "$@"
  "$@" >&2 || die 4 "CLI command failed"
}

capture_cli() {
  local output="$1"
  shift
  log_command "$@"
  "$@" > "$output" || die 4 "CLI command failed (JSON output: $output)"
}

LOCK="$PROJECT/skills-lock.json"
SKILL_PATH="$PROJECT/.agents/skills/$SKILL_NAME"
OTHER_SKILL_NAME="smoke-unrelated"
OTHER_SOURCE="$TMP_ROOT/unrelated-source"
OTHER_PATH="$PROJECT/.agents/skills/$OTHER_SKILL_NAME"

mkdir -p -- "$OTHER_SOURCE/skills/$OTHER_SKILL_NAME"
cat > "$OTHER_SOURCE/skills/$OTHER_SKILL_NAME/SKILL.md" <<'EOF'
---
name: smoke-unrelated
description: Disposable unrelated skill used to prove targeted removal preserves neighbors.
---

This fixture skill must remain installed while skill-creator is removed.
EOF

tree_digest() {
  python3 - "$1" <<'PY'
import hashlib
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
digest = hashlib.sha256()
for path in sorted(root.rglob("*")):
    if path.is_symlink() or not path.is_file():
        continue
    digest.update(str(path.relative_to(root)).encode("utf-8"))
    digest.update(b"\0")
    digest.update(path.read_bytes())
print(digest.hexdigest())
PY
}

run_cli "${CLI[@]}" add "$OTHER_SOURCE" --skill "$OTHER_SKILL_NAME" --agent "$TARGET_AGENT" --copy -y
[[ -d "$OTHER_PATH" ]] || die 4 "unrelated install did not create $OTHER_PATH"
[[ ! -L "$OTHER_PATH" ]] || die 4 "unrelated install created a symlink"
[[ -f "$OTHER_PATH/SKILL.md" ]] || die 4 "unrelated copied skill is missing SKILL.md"
OTHER_DIGEST_BEFORE="$(tree_digest "$OTHER_PATH")" || die 4 "could not hash unrelated skill"

[[ -f "$LOCK" ]] || die 4 "unrelated install did not create skills-lock.json"
cp -- "$LOCK" "$TMP_ROOT/lock-after-unrelated.json"
capture_cli "$TMP_ROOT/list-after-unrelated.json" "${CLI[@]}" list --agent "$TARGET_AGENT" --json
python3 - "$TMP_ROOT/list-after-unrelated.json" "$OTHER_PATH" <<'PY' || die 4 "unrelated baseline list was not exactly one skill"
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    rows = json.load(handle)
if not isinstance(rows, list) or len(rows) != 1:
    raise SystemExit(f"expected one unrelated row, got {rows!r}")
row = rows[0]
if row.get("name") != "smoke-unrelated" or row.get("scope") != "project":
    raise SystemExit(f"unexpected unrelated row: {row!r}")
if row.get("path") != sys.argv[2] or row.get("sourceType") != "local":
    raise SystemExit(f"unexpected unrelated path/source: {row!r}")
if row.get("agents") != ["Codex"]:
    raise SystemExit(f"unexpected unrelated agents: {row!r}")
PY
capture_cli "$TMP_ROOT/list-all-after-unrelated.json" "${CLI[@]}" list --json
python3 - "$TMP_ROOT/list-all-after-unrelated.json" "$OTHER_PATH" <<'PY' || die 4 "unrelated unfiltered baseline was not exactly one skill"
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    rows = json.load(handle)
if not isinstance(rows, list) or len(rows) != 1:
    raise SystemExit(f"expected one unfiltered unrelated row, got {rows!r}")
row = rows[0]
if row.get("name") != "smoke-unrelated" or row.get("path") != sys.argv[2]:
    raise SystemExit(f"unexpected unfiltered unrelated row: {row!r}")
if row.get("scope") != "project" or row.get("sourceType") != "local":
    raise SystemExit(f"unexpected unfiltered unrelated scope/source: {row!r}")
PY
python3 - "$TMP_ROOT/lock-after-unrelated.json" <<'PY' || die 4 "unrelated baseline lock was not exactly one skill"
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)
if data.get("version") != 1 or set(data.get("skills", {})) != {"smoke-unrelated"}:
    raise SystemExit(f"unexpected unrelated baseline lock: {data!r}")
entry = data["skills"]["smoke-unrelated"]
if entry.get("sourceType") != "local" or not entry.get("computedHash"):
    raise SystemExit(f"unexpected unrelated lock entry: {entry!r}")
PY

run_cli "${CLI[@]}" add "$SOURCE" --skill "$SKILL_NAME" --agent "$TARGET_AGENT" --copy -y
[[ -d "$SKILL_PATH" ]] || die 4 "install did not create $SKILL_PATH"
[[ ! -L "$SKILL_PATH" ]] || die 4 "install created a symlink; --copy must produce regular files"
[[ -f "$SKILL_PATH/SKILL.md" ]] || die 4 "copied skill is missing SKILL.md"

capture_cli "$TMP_ROOT/list-after-add.json" "${CLI[@]}" list --agent "$TARGET_AGENT" --json
python3 - "$TMP_ROOT/list-after-add.json" "$TMP_ROOT/list-after-unrelated.json" "$SKILL_PATH" "$OTHER_PATH" <<'PY' || die 4 "project list did not contain both expected skills"
import json
import sys

with open(sys.argv[2], encoding="utf-8") as handle:
    baseline = json.load(handle)
with open(sys.argv[1], encoding="utf-8") as handle:
    rows = json.load(handle)
if not isinstance(rows, list) or len(rows) != 2:
    raise SystemExit(f"expected two project rows, got {rows!r}")
by_name = {row.get("name"): row for row in rows}
if set(by_name) != {"smoke-unrelated", "skill-creator"}:
    raise SystemExit(f"unexpected project names: {by_name!r}")
if by_name["smoke-unrelated"] != baseline[0]:
    raise SystemExit("unrelated list row changed during selected install")
selected = by_name["skill-creator"]
if selected.get("scope") != "project" or selected.get("path") != sys.argv[3]:
    raise SystemExit(f"unexpected selected row: {selected!r}")
if selected.get("sourceType") != "local" or selected.get("agents") != ["Codex"]:
    raise SystemExit(f"unexpected selected source/agents: {selected!r}")
if by_name["smoke-unrelated"].get("path") != sys.argv[4]:
    raise SystemExit(f"unexpected unrelated path: {by_name['smoke-unrelated']!r}")
PY

[[ -f "$LOCK" ]] || die 4 "install did not create skills-lock.json"
python3 - "$LOCK" "$TMP_ROOT/lock-after-unrelated.json" <<'PY' || die 4 "install lock state was not exactly the two expected skills"
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)
with open(sys.argv[2], encoding="utf-8") as handle:
    baseline = json.load(handle)
if data.get("version") != 1:
    raise SystemExit(f"unexpected lock version: {data!r}")
skills = data.get("skills")
if not isinstance(skills, dict) or set(skills) != {"smoke-unrelated", "skill-creator"}:
    raise SystemExit(f"expected exactly two selected skills in lock: {skills!r}")
if skills["smoke-unrelated"] != baseline["skills"]["smoke-unrelated"]:
    raise SystemExit("unrelated lock entry changed during selected install")
entry = skills["skill-creator"]
if entry.get("sourceType") != "local" or not entry.get("computedHash"):
    raise SystemExit(f"unexpected selected lock entry: {entry!r}")
PY

# list --json (without --agent) exposes the display names sharing the target
# directory. The removal command must enumerate those agents explicitly:
# skills@1.5.22 accepts --agent '*' in help, but rejects the literal wildcard.
capture_cli "$TMP_ROOT/list-shared-after-add.json" "${CLI[@]}" list --json
agent_names="$(python3 - "$TMP_ROOT/list-shared-after-add.json" "$SKILL_PATH" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    rows = json.load(handle)
matches = [row for row in rows if row.get("name") == "skill-creator" and row.get("path") == sys.argv[2]]
if len(matches) != 1:
    raise SystemExit(f"expected one shared-target row, got {matches!r}")
agents = matches[0].get("agents")
if not isinstance(agents, list) or not agents:
    raise SystemExit(f"missing shared agents: {matches[0]!r}")
for agent in agents:
    if not isinstance(agent, str) or not agent:
        raise SystemExit(f"invalid agent display name: {agent!r}")
    print(agent)
PY
)" || die 4 "could not enumerate agents sharing the project target"

agent_ids=()
has_codex=0
while IFS= read -r display_name; do
  [[ -n "$display_name" ]] || continue
  case "$display_name" in
    Codex)
      agent_ids+=(codex)
      has_codex=1
      ;;
    Cursor)
      agent_ids+=(cursor)
      ;;
    "GitHub Copilot")
      agent_ids+=(github-copilot)
      ;;
    "Kimi Code CLI")
      agent_ids+=(kimi-code-cli)
      ;;
    Zed)
      agent_ids+=(zed)
      ;;
    *)
      die 4 "unknown shared agent from pinned CLI: $display_name; stop rather than remove broadly"
      ;;
  esac
done <<< "$agent_names"
(( has_codex == 1 )) || die 4 "shared-agent list did not include Codex"
(( ${#agent_ids[@]} > 0 )) || die 4 "shared-agent list was empty"

run_cli "${CLI[@]}" remove --skill "$SKILL_NAME" --agent "${agent_ids[@]}" -y
[[ ! -e "$SKILL_PATH" ]] || die 4 "remove reported success but left $SKILL_PATH"

capture_cli "$TMP_ROOT/list-after-remove.json" "${CLI[@]}" list --agent "$TARGET_AGENT" --json
python3 - "$TMP_ROOT/list-after-remove.json" "$TMP_ROOT/list-after-unrelated.json" "$OTHER_PATH" <<'PY' || die 4 "Codex list did not preserve exactly the unrelated skill"
import json
import sys

with open(sys.argv[2], encoding="utf-8") as handle:
    baseline = json.load(handle)
with open(sys.argv[1], encoding="utf-8") as handle:
    rows = json.load(handle)
if rows != baseline:
    raise SystemExit(f"expected unchanged unrelated row {baseline!r}, got {rows!r}")
if len(rows) != 1 or rows[0].get("name") != "smoke-unrelated":
    raise SystemExit(f"selected removal changed unrelated inventory: {rows!r}")
if rows[0].get("path") != sys.argv[3]:
    raise SystemExit(f"unrelated path changed: {rows!r}")
PY

capture_cli "$TMP_ROOT/list-all-after-remove.json" "${CLI[@]}" list --json
python3 - "$TMP_ROOT/list-all-after-remove.json" "$TMP_ROOT/list-all-after-unrelated.json" "$OTHER_PATH" <<'PY' || die 4 "project list did not preserve exactly the unrelated skill"
import json
import sys

with open(sys.argv[2], encoding="utf-8") as handle:
    baseline = json.load(handle)
with open(sys.argv[1], encoding="utf-8") as handle:
    rows = json.load(handle)
if rows != baseline:
    raise SystemExit(f"expected unchanged unrelated row {baseline!r}, got {rows!r}")
if len(rows) != 1 or rows[0].get("name") != "smoke-unrelated":
    raise SystemExit(f"selected removal changed unrelated inventory: {rows!r}")
if rows[0].get("path") != sys.argv[3]:
    raise SystemExit(f"unrelated path changed: {rows!r}")
PY

[[ -d "$OTHER_PATH" ]] || die 4 "targeted removal deleted unrelated skill $OTHER_PATH"
[[ ! -L "$OTHER_PATH" ]] || die 4 "targeted removal changed unrelated skill into a symlink"
OTHER_DIGEST_AFTER="$(tree_digest "$OTHER_PATH")" || die 4 "could not hash unrelated skill after removal"
[[ "$OTHER_DIGEST_AFTER" == "$OTHER_DIGEST_BEFORE" ]] || die 4 "unrelated skill files changed during selected removal"

# A verified 1.5.22 probe reported stale selected metadata after a narrow
# Codex-only removal. The matching-agent removal used here must leave the
# unrelated entry and zero selected lock entries; fail closed if the selected
# key survives, if the unrelated entry changes, or if the lock disappears.
[[ -f "$LOCK" ]] || die 4 "targeted removal deleted lock metadata for unrelated skill"
lock_state="$(python3 - "$LOCK" "$TMP_ROOT/lock-after-unrelated.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)
with open(sys.argv[2], encoding="utf-8") as handle:
    baseline = json.load(handle)
if data.get("version") != 1 or not isinstance(data.get("skills"), dict):
    raise SystemExit(f"malformed post-remove lock: {data!r}")
skills = data["skills"]
if set(skills) != {"smoke-unrelated"}:
    raise SystemExit(f"selected or unexpected lock entries remain: {skills!r}")
if skills["smoke-unrelated"] != baseline["skills"]["smoke-unrelated"]:
    raise SystemExit("unrelated lock entry changed during selected removal")
print("preserved-unrelated")
PY
)" || die 4 "post-remove lock state was invalid"

printf 'skills-cli-smoke: PASS runner=%s cli=skills@%s lock_after_remove=%s\n' "$RUNNER" "$CLI_VERSION" "$lock_state" >&2
