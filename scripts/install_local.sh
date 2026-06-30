#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_ROOT="${DESIGN_CRAFT_SKILL_ROOT:-${FRONTEND_CRAFT_SKILL_ROOT:-${HOME}/.agents/skills}}"
BACKUP_BASE="${HOME}/.agents/backups"
DRY_RUN=0

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

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
install_one "frontend-craft"

if [[ "${DRY_RUN}" == "1" ]]; then
  echo "dry_run: no files changed"
fi
