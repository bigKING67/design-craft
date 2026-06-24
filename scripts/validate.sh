#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="${ROOT_DIR}/skills/frontend-craft"
VALIDATOR="/Users/gaoqian/.codex/skills/.system/skill-creator/scripts/quick_validate.py"

cd "${ROOT_DIR}"

python3 "${VALIDATOR}" "${SKILL_DIR}"

required_files=(
  "README.md"
  "CHANGELOG.md"
  "VERSION"
  "Makefile"
  "docs/maintenance.md"
  "THIRD_PARTY_NOTICES.md"
  "upstreams.lock.json"
  "skills/frontend-craft/SKILL.md"
  "skills/frontend-craft/agents/openai.yaml"
  "skills/frontend-craft/references/source-map.md"
  "skills/frontend-craft/references/design-system-contract.md"
  "skills/frontend-craft/references/visual-judgment.md"
  "skills/frontend-craft/references/impeccable-workflow.md"
  "skills/frontend-craft/references/intent-map.md"
  "skills/frontend-craft/references/engineering-quality.md"
  "skills/frontend-craft/references/performance-quality.md"
  "skills/frontend-craft/references/architecture-quality.md"
  "skills/frontend-craft/references/project-structure.md"
  "skills/frontend-craft/references/report-quality.md"
  "skills/frontend-craft/references/surface-playbooks.md"
  "skills/frontend-craft/references/validation-contract.md"
  "skills/frontend-craft/templates/vercel-geist/README.md"
  "skills/frontend-craft/templates/vercel-geist/design.md"
  "skills/frontend-craft/templates/vercel-geist/design.dark.md"
  "evals/landing-page.md"
  "evals/dashboard-quality.md"
  "evals/datahub-special-report.md"
  "evals/frontend-architecture.md"
  "evals/forward-test-log.md"
  "evals/live-task-log.md"
  "evals/golden-tasks/datahub-industry-news.md"
  "scripts/frontend_craft_audit.sh"
  "scripts/frontend_craft_detect.sh"
  "scripts/frontend_craft_pass.sh"
  "scripts/frontend_craft_route.sh"
  "scripts/frontend_craft_seed_design.sh"
  "scripts/frontend_craft_score.py"
  "scripts/upstream_absorption_report.py"
)

for path in "${required_files[@]}"; do
  if [[ ! -f "${path}" ]]; then
    echo "Missing required file: ${path}" >&2
    exit 1
  fi
done

if ! grep -q "MIT" THIRD_PARTY_NOTICES.md; then
  echo "THIRD_PARTY_NOTICES.md is missing MIT notice" >&2
  exit 1
fi

if ! grep -q "Apache-2.0" THIRD_PARTY_NOTICES.md; then
  echo "THIRD_PARTY_NOTICES.md is missing Apache-2.0 notice" >&2
  exit 1
fi

if ! grep -q "Vercel Geist" THIRD_PARTY_NOTICES.md; then
  echo "THIRD_PARTY_NOTICES.md is missing Vercel Geist notice" >&2
  exit 1
fi

if ! grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' VERSION; then
  echo "VERSION must contain a semantic version such as 0.1.0" >&2
  exit 1
fi

if ! grep -q "make release-gate" README.md; then
  echo "README.md must document make release-gate" >&2
  exit 1
fi

if ! grep -q "make release-gate" docs/maintenance.md; then
  echo "docs/maintenance.md must document make release-gate" >&2
  exit 1
fi

if rg -n "\\[TODO|TODO:" "skills/frontend-craft"; then
  echo "Skill still contains TODO markers" >&2
  exit 1
fi

for path in \
  "scripts/install_local.sh" \
  "scripts/sync_upstreams.sh" \
  "scripts/validate.sh" \
  "scripts/frontend_craft_audit.sh" \
  "scripts/frontend_craft_detect.sh" \
  "scripts/frontend_craft_pass.sh" \
  "scripts/frontend_craft_route.sh" \
  "scripts/frontend_craft_seed_design.sh" \
  "scripts/frontend_craft_score.py" \
  "scripts/upstream_absorption_report.py"; do
  if [[ ! -x "${path}" ]]; then
    echo "Script is not executable: ${path}" >&2
    exit 1
  fi
done

bash -n scripts/frontend_craft_audit.sh
bash -n scripts/frontend_craft_detect.sh
bash -n scripts/frontend_craft_pass.sh
bash -n scripts/frontend_craft_route.sh
bash -n scripts/frontend_craft_seed_design.sh
make -n validate >/dev/null
make -n release-gate >/dev/null
python3 -m py_compile scripts/frontend_craft_score.py
python3 -m py_compile scripts/upstream_absorption_report.py
python3 scripts/frontend_craft_score.py --self --no-smoke --json >/dev/null
python3 scripts/upstream_absorption_report.py --json >/dev/null
bash scripts/frontend_craft_detect.sh --target skills/frontend-craft --json-only >/dev/null
bash scripts/frontend_craft_detect.sh --target skills/frontend-craft --full-json >/dev/null
bash scripts/frontend_craft_pass.sh --target skills/frontend-craft --mode audit --skip-route --skip-score >/dev/null
bash scripts/frontend_craft_audit.sh --target skills/frontend-craft --mode audit --skip-route --skip-score >/dev/null
bash scripts/frontend_craft_audit.sh --target skills/frontend-craft --mode critique --skip-route --skip-score >/dev/null
bash scripts/frontend_craft_seed_design.sh --target skills/frontend-craft --dry-run >/dev/null

tmp_design_seed_dir="$(mktemp -d -t frontend-craft-seed.XXXXXX)"
trap 'rm -rf "${tmp_design_seed_dir}"' EXIT
bash scripts/frontend_craft_seed_design.sh --target "${tmp_design_seed_dir}" >/dev/null
cmp skills/frontend-craft/templates/vercel-geist/design.md "${tmp_design_seed_dir}/DESIGN.md" >/dev/null
cmp skills/frontend-craft/templates/vercel-geist/design.dark.md "${tmp_design_seed_dir}/DESIGN.dark.md" >/dev/null

for ref in \
  "design-system-contract.md" \
  "visual-judgment.md" \
  "impeccable-workflow.md" \
  "intent-map.md" \
  "engineering-quality.md" \
  "performance-quality.md" \
  "architecture-quality.md" \
  "project-structure.md" \
  "report-quality.md" \
  "surface-playbooks.md" \
  "validation-contract.md" \
  "source-map.md"; do
  if ! grep -q "${ref}" skills/frontend-craft/SKILL.md; then
    echo "SKILL.md does not route reference: ${ref}" >&2
    exit 1
  fi
done

for template in \
  "templates/vercel-geist/design.md" \
  "templates/vercel-geist/design.dark.md"; do
  if ! grep -q "${template}" skills/frontend-craft/SKILL.md; then
    echo "SKILL.md does not route template: ${template}" >&2
    exit 1
  fi
done

python3 - <<'PY'
import json
import subprocess
import sys
from pathlib import Path

payload = json.loads(Path("upstreams.lock.json").read_text(encoding="utf-8"))
errors = []
for name, meta in payload["upstreams"].items():
    path = meta["path"]
    want = meta["commit"]
    got = subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"], text=True).strip()
    if got != want:
        errors.append(f"{name}: lock commit {want} != working commit {got}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
PY

echo "frontend-craft validation passed."
