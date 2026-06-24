#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage:
  scripts/frontend_craft_pass.sh [frontend_craft_audit.sh options]

Preferred neutral wrapper for frontend-craft quality passes.

Examples:
  scripts/frontend_craft_pass.sh --target /path/to/project --mode critique
  scripts/frontend_craft_pass.sh --target /path/to/project --mode harden

Supported modes are delegated to frontend_craft_audit.sh:
  critique|audit|polish|harden|optimize|structure|architecture
EOF
  exit 0
fi

exec "${ROOT_DIR}/scripts/frontend_craft_audit.sh" "$@"
