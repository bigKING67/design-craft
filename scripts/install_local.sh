#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_ROOT="${DESIGN_CRAFT_SKILL_ROOT:-${FRONTEND_CRAFT_SKILL_ROOT:-${HOME}/.agents/skills}}"
BACKUP_BASE="${HOME}/.agents/backups"
DRY_RUN=0
INCLUDE_LEGACY_ALIAS=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      ;;
    --include-legacy-alias)
      INCLUDE_LEGACY_ALIAS=1
      ;;
    *)
      echo "Unknown argument: $1" >&2
      echo "Usage: $0 [--dry-run] [--include-legacy-alias]" >&2
      exit 2
      ;;
  esac
  shift
done

install_one() {
  local name="$1"
  local source="${ROOT_DIR}/skills/${name}"
  local target="${INSTALL_ROOT}/${name}"
  local backup_root="${BACKUP_BASE}/${name}"

  if [[ ! -f "${source}/SKILL.md" ]]; then
    echo "Missing skill source: ${source}/SKILL.md" >&2
    exit 1
  fi

  echo "Source: ${source}"
  echo "Target: ${target}"

  if [[ "${DRY_RUN}" == "1" ]]; then
    if [[ -e "${target}" ]]; then
      echo "Would backup existing ${name} target under: ${backup_root}"
    fi
    echo "Would install ${name} skill."
    return
  fi

  mkdir -p "${INSTALL_ROOT}"

  if [[ -e "${target}" ]]; then
    local stamp
    local backup
    stamp="$(date -u +%Y%m%dT%H%M%SZ)"
    backup="${backup_root}/${stamp}"
    mkdir -p "${backup_root}"
    mv "${target}" "${backup}"
    echo "Backed up existing ${name} skill to: ${backup}"
  fi

  cp -R "${source}" "${target}"
  echo "Installed ${name} skill to: ${target}"
}

install_one "design-craft"
if [[ "${INCLUDE_LEGACY_ALIAS}" == "1" ]]; then
  install_one "frontend-craft"
else
  echo "Skipped legacy frontend-craft alias. Pass --include-legacy-alias to install it."
fi

if [[ "${DRY_RUN}" == "1" ]]; then
  echo "dry_run: no files changed"
fi
