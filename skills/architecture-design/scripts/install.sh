#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  install.sh --codex-global [--force]
  install.sh --codex-repo [REPO] [--force]
  install.sh --claude-global [--force]
  install.sh --claude-repo [REPO] [--force]
  install.sh --path DESTINATION_PARENT [--force]

The skill directory is copied under the selected parent as
"architecture-design". Existing installs are not overwritten unless
--force is provided.
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_ROOT")"
MODE=""
BASE=""
FORCE=0

while (($#)); do
  case "$1" in
    --codex-global)
      MODE="codex-global"; shift ;;
    --codex-repo)
      MODE="codex-repo"
      if (($# > 1)) && [[ "$2" != --* ]]; then BASE="$2"; shift 2; else BASE="$PWD"; shift; fi ;;
    --claude-global)
      MODE="claude-global"; shift ;;
    --claude-repo)
      MODE="claude-repo"
      if (($# > 1)) && [[ "$2" != --* ]]; then BASE="$2"; shift 2; else BASE="$PWD"; shift; fi ;;
    --path)
      (($# > 1)) || { echo "--path requires a destination parent" >&2; exit 2; }
      MODE="path"; BASE="$2"; shift 2 ;;
    --force)
      FORCE=1; shift ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$MODE" in
  codex-global) DEST_PARENT="$HOME/.agents/skills" ;;
  codex-repo) DEST_PARENT="$(cd "$BASE" && pwd)/.agents/skills" ;;
  claude-global) DEST_PARENT="$HOME/.claude/skills" ;;
  claude-repo) DEST_PARENT="$(cd "$BASE" && pwd)/.claude/skills" ;;
  path) mkdir -p "$BASE"; DEST_PARENT="$(cd "$BASE" && pwd)" ;;
  *) usage >&2; exit 2 ;;
esac

DEST="$DEST_PARENT/$SKILL_NAME"
mkdir -p "$DEST_PARENT"
if [[ -e "$DEST" ]]; then
  if ((FORCE)); then
    rm -rf "$DEST"
  else
    echo "Refusing to overwrite existing install: $DEST" >&2
    echo "Re-run with --force after reviewing local modifications." >&2
    exit 1
  fi
fi

# Avoid copying VCS metadata or accidental local caches.
mkdir -p "$DEST"
(
  cd "$SKILL_ROOT"
  tar --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' -cf - .
) | (
  cd "$DEST"
  tar -xf -
)

python3 "$DEST/scripts/validate_skill.py" "$DEST"
echo "Installed $SKILL_NAME at $DEST"
