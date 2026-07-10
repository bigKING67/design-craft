#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export DESIGN_CRAFT_SOURCE_ROOT="${DESIGN_CRAFT_SOURCE_ROOT:-${ROOT_DIR}}"
exec "${ROOT_DIR}/skills/design-craft/scripts/design_craft_taste_review.sh" "$@"
