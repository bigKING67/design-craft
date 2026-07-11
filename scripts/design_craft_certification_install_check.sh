#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

TEMP_ROOT="$(mktemp -d -t design-craft-cert-install.XXXXXX)"
cleanup() {
  rm -rf "${TEMP_ROOT}"
}
trap cleanup EXIT INT TERM

export DESIGN_CRAFT_SKILL_ROOT="${TEMP_ROOT}/skills"
export DESIGN_CRAFT_BACKUP_KEEP=0

mkdir -p "${DESIGN_CRAFT_SKILL_ROOT}"
bash scripts/install_local.sh --keep-backups 0
make install-verify
python3 scripts/design_craft_maturity.py --profile local --min-score 100

echo "certification install verified in temporary root: ${DESIGN_CRAFT_SKILL_ROOT}"
