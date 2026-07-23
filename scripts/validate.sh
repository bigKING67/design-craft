#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="${ROOT_DIR}/skills/design-craft"
VALIDATOR="${SKILL_CREATOR_QUICK_VALIDATE:-${HOME}/.codex/skills/.system/skill-creator/scripts/quick_validate.py}"
PORTABLE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --portable)
      PORTABLE=1
      ;;
    *)
      echo "Unknown argument: $1" >&2
      echo "Usage: $0 [--portable]" >&2
      exit 2
      ;;
  esac
  shift
done

cd "${ROOT_DIR}"
export PYTHONDONTWRITEBYTECODE=1

if [[ -z "${DESIGN_CRAFT_BASH:-}" ]]; then
  if command -v cygpath >/dev/null 2>&1; then
    DESIGN_CRAFT_BASH="$(cygpath -w "${BASH}")"
  else
    DESIGN_CRAFT_BASH="${BASH}"
  fi
fi
export DESIGN_CRAFT_BASH

if [[ "${PORTABLE}" == "0" ]]; then
  if [[ ! -f "${VALIDATOR}" ]]; then
    echo "Missing skill validator: ${VALIDATOR}" >&2
    echo "Set SKILL_CREATOR_QUICK_VALIDATE to a compatible quick_validate.py path." >&2
    exit 1
  fi
  python3 "${VALIDATOR}" "${SKILL_DIR}"
fi

python3 -m tools.design_craft.validation.repository_contracts --check
python3 -m tools.design_craft.validation.tooling_contracts --check
python3 scripts/design_craft_lint.py --check
python3 scripts/design_craft_package_validate.py --check --validate
python3 scripts/design_craft_public_repo_validate.py --check --validate
python3 scripts/design_craft_workflow_validate.py --check --validate

node tests/contract/test_upstream_review_issue.cjs
python3 scripts/upstream_absorption_report.py --check
python3 scripts/design_craft_taste_absorption.py --check --strict
python3 scripts/design_craft_impeccable_absorption.py --check --strict
python3 scripts/design_craft_emil_absorption.py --check --strict
python3 scripts/design_craft_cross_agent_run.py --check
python3 scripts/design_craft_cross_agent_validate.py --check
python3 scripts/design_craft_comparative_run.py --check
python3 scripts/design_craft_comparative_judge.py --check
python3 scripts/design_craft_comparative_validate.py --check
python3 scripts/design_craft_native_runtime_validate.py --check
python3 scripts/design_craft_github_checks.py --check
python3 scripts/design_craft_github_governance.py --check
python3 scripts/design_craft_install_verify.py --check
python3 scripts/design_craft_codex_route_pack.py --check
python3 scripts/design_craft_maturity.py --check

python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/design_craft_maturity.py --profile development

echo "design-craft validation passed."
