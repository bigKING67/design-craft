#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_SRC="${ROOT_DIR}/skills/frontend-craft"
INSTALL_ROOT="${FRONTEND_CRAFT_SKILL_ROOT:-${HOME}/.agents/skills}"
TARGET="${INSTALL_ROOT}/frontend-craft"
BACKUP_ROOT="${HOME}/.agents/backups/frontend-craft"
DRY_RUN=0

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

if [[ ! -f "${SKILL_SRC}/SKILL.md" ]]; then
  echo "Missing skill source: ${SKILL_SRC}/SKILL.md" >&2
  exit 1
fi

echo "Source: ${SKILL_SRC}"
echo "Target: ${TARGET}"

if [[ "${DRY_RUN}" == "1" ]]; then
  if [[ -e "${TARGET}" ]]; then
    echo "Would backup existing target under: ${BACKUP_ROOT}"
  fi
  echo "Would install frontend-craft skill."
  exit 0
fi

mkdir -p "${INSTALL_ROOT}"

if [[ -e "${TARGET}" ]]; then
  stamp="$(date -u +%Y%m%dT%H%M%SZ)"
  backup="${BACKUP_ROOT}/${stamp}"
  mkdir -p "${BACKUP_ROOT}"
  mv "${TARGET}" "${backup}"
  echo "Backed up existing skill to: ${backup}"
fi

cp -R "${SKILL_SRC}" "${TARGET}"
echo "Installed frontend-craft skill to: ${TARGET}"
