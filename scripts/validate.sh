#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="${ROOT_DIR}/skills/design-craft"
LEGACY_SKILL_DIR="${ROOT_DIR}/skills/frontend-craft"
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

if [[ "${PORTABLE}" == "0" ]]; then
  if [[ ! -f "${VALIDATOR}" ]]; then
    echo "Missing skill validator: ${VALIDATOR}" >&2
    echo "Set SKILL_CREATOR_QUICK_VALIDATE to a compatible quick_validate.py path." >&2
    exit 1
  fi

  python3 "${VALIDATOR}" "${SKILL_DIR}"
  python3 "${VALIDATOR}" "${LEGACY_SKILL_DIR}"
fi

required_files=(
  "README.md"
  "CHANGELOG.md"
  "VERSION"
  "package.json"
  "Makefile"
  ".gitmodules"
  "docs/maintenance.md"
  "THIRD_PARTY_NOTICES.md"
  "upstreams.lock.json"
  "skills/design-craft/SKILL.md"
  "skills/design-craft/agents/openai.yaml"
  "skills/design-craft/references/source-map.md"
  "skills/design-craft/references/foundational-visual-principles.md"
  "skills/design-craft/references/design-move-library.md"
  "skills/design-craft/references/design-system-contract.md"
  "skills/design-craft/references/visual-judgment.md"
  "skills/design-craft/references/product-ui-taste-review.md"
  "skills/design-craft/references/taste-score-calibration.md"
  "skills/design-craft/references/impeccable-workflow.md"
  "skills/design-craft/references/intent-map.md"
  "skills/design-craft/references/motion-quality.md"
  "skills/design-craft/references/motion-vocabulary.md"
  "skills/design-craft/references/engineering-quality.md"
  "skills/design-craft/references/performance-quality.md"
  "skills/design-craft/references/architecture-quality.md"
  "skills/design-craft/references/project-structure.md"
  "skills/design-craft/references/report-quality.md"
  "skills/design-craft/references/surface-playbooks.md"
  "skills/design-craft/references/validation-contract.md"
  "skills/design-craft/templates/vercel-geist/README.md"
  "skills/design-craft/templates/vercel-geist/design.md"
  "skills/design-craft/templates/vercel-geist/design.dark.md"
  "skills/frontend-craft/SKILL.md"
  "skills/frontend-craft/agents/openai.yaml"
  "evals/landing-page.md"
  "evals/dashboard-quality.md"
  "evals/frontend-architecture.md"
  "evals/forward-test-log.md"
  "evals/live-task-log.md"
  "evals/golden-tasks/generic-review-workbench.md"
  "evals/product-ui-taste/material-ops-home/input.md"
  "evals/product-ui-taste/material-ops-home/review.expected.md"
  "evals/product-ui-taste/material-ops-home/score.json"
  "evals/product-ui-taste/live-browser-samples/input.md"
  "evals/product-ui-taste/live-browser-samples/review.expected.md"
  "evals/product-ui-taste/live-browser-samples/score.json"
  "evals/product-ui-taste/before-after/README.md"
  "evals/product-ui-taste/before-after/_template/input.md"
  "evals/product-ui-taste/before-after/_template/score.before.json"
  "evals/product-ui-taste/before-after/_template/score.after.json"
  "evals/product-ui-taste/before-after/_template/diff-summary.md"
  "evals/product-ui-taste/before-after/_template/validation.md"
  "evals/product-ui-taste/before-after/_template/screenshots.json"
  "evals/product-ui-taste/before-after/generic-review-workbench-local-l4/input.md"
  "evals/product-ui-taste/before-after/generic-review-workbench-local-l4/score.before.json"
  "evals/product-ui-taste/before-after/generic-review-workbench-local-l4/score.after.json"
  "evals/product-ui-taste/before-after/generic-review-workbench-local-l4/diff-summary.md"
  "evals/product-ui-taste/before-after/generic-review-workbench-local-l4/validation.md"
  "evals/product-ui-taste/before-after/generic-review-workbench-local-l4/screenshots.json"
  "evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/input.md"
  "evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/score.before.json"
  "evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/score.after.json"
  "evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/diff-summary.md"
  "evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/validation.md"
  "evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/screenshots.json"
  "evals/cross-agent/README.md"
  "evals/cross-agent/_template/prompt.md"
  "evals/cross-agent/_template/expected-findings.md"
  "evals/cross-agent/_template/scorecard.md"
  "evals/cross-agent/same-prompt-dashboard-review/prompt.md"
  "evals/cross-agent/same-prompt-dashboard-review/expected-findings.md"
  "evals/cross-agent/same-prompt-dashboard-review/scorecard.md"
  "evals/cross-agent/same-prompt-landing-polish/prompt.md"
  "evals/cross-agent/same-prompt-landing-polish/expected-findings.md"
  "evals/cross-agent/same-prompt-landing-polish/scorecard.md"
  "evals/cross-agent/same-prompt-motion-review/prompt.md"
  "evals/cross-agent/same-prompt-motion-review/expected-findings.md"
  "evals/cross-agent/same-prompt-motion-review/scorecard.md"
  "evals/fixtures/css-smells/card-soup.css"
  "evals/fixtures/focus-smells/Button.tsx"
  "evals/fixtures/l4-pages/generic-review-workbench/index.html"
  "evals/fixtures/l4-pages/ops-dashboard-decision-surface/index.html"
  "evals/fixtures/l4-cases/generic-invalid/diff-summary.md"
  "evals/fixtures/l4-cases/generic-invalid/input.md"
  "evals/fixtures/l4-cases/generic-invalid/score.after.json"
  "evals/fixtures/l4-cases/generic-invalid/score.before.json"
  "evals/fixtures/l4-cases/generic-invalid/screenshots.json"
  "evals/fixtures/l4-cases/generic-invalid/validation.md"
  "evals/fixtures/l4-cases/generic-valid/diff-summary.md"
  "evals/fixtures/l4-cases/generic-valid/input.md"
  "evals/fixtures/l4-cases/generic-valid/score.after.json"
  "evals/fixtures/l4-cases/generic-valid/score.before.json"
  "evals/fixtures/l4-cases/generic-valid/screenshots.json"
  "evals/fixtures/l4-cases/generic-valid/validation.md"
  "evals/fixtures/l4-screenshot-manifests/generic-invalid.json"
  "evals/fixtures/l4-screenshot-manifests/generic-valid.json"
  "evals/fixtures/token-smells/panel.css"
  "adapters/codex/README.md"
  "adapters/codex/route-pack/README.md"
  "adapters/cursor/README.md"
  "adapters/cursor/.cursor/rules/design-craft.mdc"
  "adapters/claude/README.md"
  "adapters/pi/README.md"
  "adapters/generic/README.md"
  "scripts/design_craft_audit.sh"
  "scripts/design_craft_active_scope_validate.py"
  "scripts/design_craft_detect.sh"
  "scripts/design_craft_doctor.sh"
  "scripts/design_craft_init_agent.sh"
  "scripts/design_craft_l4_capture.py"
  "scripts/design_craft_l4_case_validate.py"
  "scripts/design_craft_l4_eval_case.sh"
  "scripts/design_craft_l4_evidence_manifest.py"
  "scripts/design_craft_browser_evidence.py"
  "scripts/design_craft_codex_route_pack.py"
  "scripts/design_craft_cross_agent_validate.py"
  "scripts/design_craft_css_smell_scan.py"
  "scripts/design_craft_focus_audit.py"
  "scripts/design_craft_static_review.py"
  "scripts/design_craft_token_audit.py"
  "scripts/design_craft_pass.sh"
  "scripts/design_craft_route.sh"
  "scripts/design_craft_seed_design.sh"
  "scripts/design_craft_taste_review.sh"
  "scripts/design_craft_score.py"
  "scripts/frontend_craft_audit.sh"
  "scripts/frontend_craft_detect.sh"
  "scripts/frontend_craft_browser_evidence.py"
  "scripts/frontend_craft_pass.sh"
  "scripts/frontend_craft_route.sh"
  "scripts/frontend_craft_seed_design.sh"
  "scripts/frontend_craft_taste_review.sh"
  "scripts/frontend_craft_score.py"
  "scripts/upstream_absorption_report.py"
)

for path in "${required_files[@]}"; do
  if [[ ! -f "${path}" ]]; then
    echo "Missing required file: ${path}" >&2
    exit 1
  fi
done

python3 scripts/design_craft_active_scope_validate.py --check >/dev/null
python3 scripts/design_craft_active_scope_validate.py --root . >/dev/null


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

if ! grep -q "emilkowalski/skills" THIRD_PARTY_NOTICES.md; then
  echo "THIRD_PARTY_NOTICES.md is missing emilkowalski/skills notice" >&2
  exit 1
fi

if ! grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' VERSION; then
  echo "VERSION must contain a semantic version such as 0.1.0" >&2
  exit 1
fi

node <<'NODE'
const fs = require("fs");
const pkg = JSON.parse(fs.readFileSync("package.json", "utf8"));
const version = fs.readFileSync("VERSION", "utf8").trim();
if (pkg.version !== version) {
  throw new Error(`package.json version (${pkg.version}) must match VERSION (${version})`);
}
if (!Array.isArray(pkg.keywords) || !pkg.keywords.includes("pi-package")) {
  throw new Error("package.json keywords must include pi-package");
}
const expectedSkills = ["skills/design-craft"];
const actualSkills = pkg.pi && Array.isArray(pkg.pi.skills) ? pkg.pi.skills : [];
for (const skill of expectedSkills) {
  if (!actualSkills.includes(skill)) {
    throw new Error(`package.json pi.skills must include ${skill}`);
  }
  if (!fs.existsSync(`${skill}/SKILL.md`)) {
    throw new Error(`missing package skill entrypoint: ${skill}/SKILL.md`);
  }
}
if (actualSkills.includes("skills/frontend-craft")) {
  throw new Error("package.json pi.skills must not expose the legacy frontend-craft alias by default");
}
NODE

if ! grep -q "make release-gate" README.md; then
  echo "README.md must document make release-gate" >&2
  exit 1
fi

if ! grep -q "make release-gate" docs/maintenance.md; then
  echo "docs/maintenance.md must document make release-gate" >&2
  exit 1
fi

if ! grep -Fq 'renamed to `design-craft`' skills/frontend-craft/SKILL.md; then
  echo "legacy frontend-craft alias must point users to design-craft" >&2
  exit 1
fi

legacy_extra_files="$(
  find skills/frontend-craft -type f \
    ! -path "skills/frontend-craft/SKILL.md" \
    ! -path "skills/frontend-craft/agents/openai.yaml" \
    -print
)"
if [[ -n "${legacy_extra_files}" ]]; then
  echo "legacy frontend-craft alias must stay minimal; unexpected files:" >&2
  echo "${legacy_extra_files}" >&2
  exit 1
fi

if rg -n "\\[TODO|TODO:" "skills/design-craft"; then
  echo "Canonical skill still contains TODO markers" >&2
  exit 1
fi

for path in \
  "scripts/install_local.sh" \
  "scripts/sync_upstreams.sh" \
  "scripts/validate.sh" \
  "scripts/design_craft_audit.sh" \
  "scripts/design_craft_active_scope_validate.py" \
  "scripts/design_craft_detect.sh" \
  "scripts/design_craft_doctor.sh" \
  "scripts/design_craft_init_agent.sh" \
  "scripts/design_craft_l4_capture.py" \
  "scripts/design_craft_l4_case_validate.py" \
  "scripts/design_craft_l4_eval_case.sh" \
  "scripts/design_craft_l4_evidence_manifest.py" \
  "scripts/design_craft_browser_evidence.py" \
  "scripts/design_craft_codex_route_pack.py" \
  "scripts/design_craft_cross_agent_validate.py" \
  "scripts/design_craft_css_smell_scan.py" \
  "scripts/design_craft_focus_audit.py" \
  "scripts/design_craft_static_review.py" \
  "scripts/design_craft_token_audit.py" \
  "scripts/design_craft_pass.sh" \
  "scripts/design_craft_route.sh" \
  "scripts/design_craft_seed_design.sh" \
  "scripts/design_craft_taste_review.sh" \
  "scripts/design_craft_score.py" \
  "scripts/frontend_craft_audit.sh" \
  "scripts/frontend_craft_detect.sh" \
  "scripts/frontend_craft_browser_evidence.py" \
  "scripts/frontend_craft_pass.sh" \
  "scripts/frontend_craft_route.sh" \
  "scripts/frontend_craft_seed_design.sh" \
  "scripts/frontend_craft_taste_review.sh" \
  "scripts/frontend_craft_score.py" \
  "scripts/upstream_absorption_report.py"; do
  if [[ ! -x "${path}" ]]; then
    echo "Script is not executable: ${path}" >&2
    exit 1
  fi
done

for path in \
  scripts/design_craft_audit.sh \
  scripts/design_craft_detect.sh \
  scripts/design_craft_doctor.sh \
  scripts/design_craft_init_agent.sh \
  scripts/design_craft_l4_eval_case.sh \
  scripts/design_craft_pass.sh \
  scripts/design_craft_route.sh \
  scripts/design_craft_seed_design.sh \
  scripts/design_craft_taste_review.sh \
  scripts/frontend_craft_audit.sh \
  scripts/frontend_craft_detect.sh \
  scripts/frontend_craft_pass.sh \
  scripts/frontend_craft_route.sh \
  scripts/frontend_craft_seed_design.sh \
  scripts/frontend_craft_taste_review.sh; do
  bash -n "${path}"
done

make -n validate >/dev/null
make -n release-gate >/dev/null

for path in \
  scripts/design_craft_score.py \
  scripts/design_craft_active_scope_validate.py \
  scripts/design_craft_browser_evidence.py \
  scripts/design_craft_codex_route_pack.py \
  scripts/design_craft_cross_agent_validate.py \
  scripts/design_craft_l4_capture.py \
  scripts/design_craft_l4_case_validate.py \
  scripts/design_craft_l4_evidence_manifest.py \
  scripts/design_craft_css_smell_scan.py \
  scripts/design_craft_focus_audit.py \
  scripts/design_craft_static_review.py \
  scripts/design_craft_token_audit.py \
  scripts/frontend_craft_score.py \
  scripts/frontend_craft_browser_evidence.py \
  scripts/upstream_absorption_report.py; do
  python3 -m py_compile "${path}"
done

python3 scripts/design_craft_score.py --self --no-smoke --json >/dev/null
python3 scripts/design_craft_browser_evidence.py --check --print-js >/dev/null
if [[ "${PORTABLE}" == "0" ]]; then
  python3 scripts/design_craft_codex_route_pack.py --check >/dev/null
  python3 scripts/design_craft_codex_route_pack.py --strict >/dev/null
fi
python3 scripts/design_craft_cross_agent_validate.py --check >/dev/null
python3 scripts/design_craft_cross_agent_validate.py --root evals/cross-agent >/dev/null
python3 scripts/design_craft_l4_capture.py --check >/dev/null
python3 scripts/design_craft_l4_evidence_manifest.py --check >/dev/null
python3 scripts/design_craft_l4_evidence_manifest.py \
  --validate-screenshots-json evals/product-ui-taste/before-after/_template/screenshots.json >/dev/null
python3 scripts/design_craft_l4_evidence_manifest.py \
  --validate-screenshots-json evals/fixtures/l4-screenshot-manifests/generic-valid.json \
  --strict >/dev/null
python3 scripts/design_craft_l4_evidence_manifest.py \
  --validate-screenshots-json evals/product-ui-taste/before-after/generic-review-workbench-local-l4/screenshots.json \
  --strict >/dev/null
python3 scripts/design_craft_l4_evidence_manifest.py \
  --validate-screenshots-json evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/screenshots.json \
  --strict >/dev/null
if python3 scripts/design_craft_l4_evidence_manifest.py \
  --validate-screenshots-json evals/fixtures/l4-screenshot-manifests/generic-invalid.json \
  --strict >/dev/null 2>&1; then
  echo "Invalid L4 screenshot manifest unexpectedly passed strict validation" >&2
  exit 1
fi
python3 scripts/design_craft_l4_case_validate.py --check >/dev/null
python3 scripts/design_craft_l4_case_validate.py \
  --case-dir evals/fixtures/l4-cases/generic-valid \
  --strict >/dev/null
python3 scripts/design_craft_l4_case_validate.py \
  --case-dir evals/product-ui-taste/before-after/generic-review-workbench-local-l4 \
  --strict >/dev/null
python3 scripts/design_craft_l4_case_validate.py \
  --case-dir evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4 \
  --strict >/dev/null
if python3 scripts/design_craft_l4_case_validate.py \
  --case-dir evals/fixtures/l4-cases/generic-invalid \
  --strict >/dev/null 2>&1; then
  echo "Invalid L4 case directory unexpectedly passed strict validation" >&2
  exit 1
fi
python3 scripts/design_craft_css_smell_scan.py --target evals/fixtures/css-smells --json >/dev/null
python3 scripts/design_craft_focus_audit.py --target evals/fixtures/focus-smells --json >/dev/null
python3 scripts/design_craft_token_audit.py --target evals/fixtures/token-smells --json >/dev/null
python3 scripts/design_craft_static_review.py --target evals/fixtures --json >/dev/null
python3 scripts/upstream_absorption_report.py --json >/dev/null
if [[ "${PORTABLE}" == "0" ]]; then
  python3 scripts/upstream_absorption_report.py --json --remote >/dev/null
fi

bash scripts/design_craft_detect.sh --target skills/design-craft --json-only >/dev/null
bash scripts/design_craft_detect.sh --target skills/design-craft --full-json >/dev/null
bash scripts/design_craft_detect.sh --target evals/fixtures/css-smells --full-json >/dev/null
bash scripts/design_craft_doctor.sh --target . --json >/dev/null
tmp_init_dir="$(mktemp -d -t design-craft-init.XXXXXX)"
trap 'rm -rf "${tmp_design_seed_dir:-}" "${tmp_init_dir:-}"' EXIT
bash scripts/design_craft_init_agent.sh --agent codex --target "${tmp_init_dir}" --scope project --dry-run >/dev/null
bash scripts/design_craft_init_agent.sh --agent cursor --target "${tmp_init_dir}" --scope project --with-rule --dry-run >/dev/null
bash scripts/design_craft_init_agent.sh --agent claude --target "${tmp_init_dir}" --scope project --dry-run >/dev/null
bash scripts/design_craft_init_agent.sh --agent pi --target "${tmp_init_dir}" --scope project --dry-run >/dev/null
bash scripts/design_craft_init_agent.sh --agent generic --target "${tmp_init_dir}" --scope project --dry-run >/dev/null
bash scripts/design_craft_l4_eval_case.sh --case-id validation-l4-case --surface validation --output-root "${tmp_init_dir}/l4" >/dev/null
test -f "${tmp_init_dir}/l4/validation-l4-case/screenshots.json"
python3 scripts/design_craft_l4_evidence_manifest.py \
  --validate-screenshots-json "${tmp_init_dir}/l4/validation-l4-case/screenshots.json" >/dev/null
bash scripts/design_craft_pass.sh --target skills/design-craft --mode audit --skip-route --skip-score >/dev/null
bash scripts/design_craft_pass.sh --target skills/design-craft --mode critique --skip-route --skip-score >/dev/null
bash scripts/design_craft_pass.sh --target skills/design-craft --mode motion --skip-route --skip-score >/dev/null
bash scripts/design_craft_audit.sh --target skills/design-craft --mode audit --skip-route --skip-score >/dev/null
bash scripts/design_craft_audit.sh --target skills/design-craft --mode critique --skip-route --skip-score >/dev/null
bash scripts/design_craft_seed_design.sh --target skills/design-craft --dry-run >/dev/null
bash scripts/design_craft_taste_review.sh --target skills/design-craft --context "validation smoke" --evidence-level L0 >/dev/null

bash scripts/frontend_craft_pass.sh --target skills/design-craft --mode motion --skip-route --skip-score >/dev/null
python3 scripts/frontend_craft_score.py --self --no-smoke --json >/dev/null

tmp_design_seed_dir="$(mktemp -d -t design-craft-seed.XXXXXX)"
trap 'rm -rf "${tmp_design_seed_dir:-}" "${tmp_init_dir:-}"' EXIT
bash scripts/design_craft_seed_design.sh --target "${tmp_design_seed_dir}" >/dev/null
cmp skills/design-craft/templates/vercel-geist/design.md "${tmp_design_seed_dir}/DESIGN.md" >/dev/null
cmp skills/design-craft/templates/vercel-geist/design.dark.md "${tmp_design_seed_dir}/DESIGN.dark.md" >/dev/null

for ref in \
  "design-system-contract.md" \
  "foundational-visual-principles.md" \
  "design-move-library.md" \
  "visual-judgment.md" \
  "product-ui-taste-review.md" \
  "taste-score-calibration.md" \
  "impeccable-workflow.md" \
  "intent-map.md" \
  "motion-quality.md" \
  "motion-vocabulary.md" \
  "engineering-quality.md" \
  "performance-quality.md" \
  "architecture-quality.md" \
  "project-structure.md" \
  "report-quality.md" \
  "surface-playbooks.md" \
  "validation-contract.md" \
  "source-map.md"; do
  if ! grep -q "${ref}" skills/design-craft/SKILL.md; then
    echo "SKILL.md does not route reference: ${ref}" >&2
    exit 1
  fi
done

for template in \
  "templates/vercel-geist/design.md" \
  "templates/vercel-geist/design.dark.md"; do
  if ! grep -q "${template}" skills/design-craft/SKILL.md; then
    echo "SKILL.md does not route template: ${template}" >&2
    exit 1
  fi
done

for upstream_name in taste-skill impeccable emilkowalski-skills; do
  if ! grep -q "\"${upstream_name}\"" upstreams.lock.json; then
    echo "upstreams.lock.json is missing ${upstream_name}" >&2
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

python3 - <<'PY'
import json
import sys
from pathlib import Path

errors = []
score_paths = [
    Path("evals/product-ui-taste/material-ops-home/score.json"),
    Path("evals/product-ui-taste/before-after/generic-review-workbench-local-l4/score.before.json"),
    Path("evals/product-ui-taste/before-after/generic-review-workbench-local-l4/score.after.json"),
    Path("evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/score.before.json"),
    Path("evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/score.after.json"),
]
score_paths = [path for path in score_paths if path.is_file()]
if not score_paths:
    errors.append("product-ui-taste must include at least one score JSON file")

levels = {"L0", "L1", "L2", "L3", "L4"}
has_l2_plus = False

for score_path in score_paths:
    payload = json.loads(score_path.read_text(encoding="utf-8"))
    root_case_id = payload.get("case_id") or score_path.parent.name
    entries = payload.get("cases")
    if entries is None:
        entries = [payload]
    if not isinstance(entries, list) or not entries:
        errors.append(f"{score_path}: cases must be a non-empty list or omitted for a singleton case")
        continue

    for index, entry in enumerate(entries):
        case_id = entry.get("case_id") or f"{root_case_id}[{index}]"
        level = entry.get("evidence_level") or payload.get("evidence_level")
        if level not in levels:
            errors.append(f"{score_path}: {case_id} evidence_level must be one of {sorted(levels)}")
        if level in {"L2", "L3", "L4"}:
            has_l2_plus = True
            if not entry.get("screenshot_sha256"):
                errors.append(f"{score_path}: {case_id} L2+ case must record screenshot_sha256")
            dims = entry.get("screenshot_dimensions")
            if (
                not isinstance(dims, list)
                or len(dims) != 2
                or not all(isinstance(value, int) and value > 0 for value in dims)
            ):
                errors.append(f"{score_path}: {case_id} L2+ case must record screenshot_dimensions")

        expected = entry.get("expected_score")
        acceptable = entry.get("acceptable_range")
        if (
            not isinstance(expected, int)
            or not isinstance(acceptable, list)
            or len(acceptable) != 2
            or not all(isinstance(value, int) for value in acceptable)
        ):
            errors.append(f"{score_path}: {case_id} score fields must be integers")
        else:
            low, high = acceptable
            if not low <= expected <= high:
                errors.append(f"{score_path}: {case_id} expected_score must fit acceptable_range")

        if not isinstance(entry.get("maturity_band"), str) or not entry["maturity_band"]:
            errors.append(f"{score_path}: {case_id} maturity_band is required")

        required = entry.get("required_findings", [])
        guards = entry.get("false_positive_guards", [])
        if len(required) < 3 or len(guards) < 3:
            errors.append(f"{score_path}: {case_id} must keep required findings and false-positive guards")

material_payload = json.loads(Path("evals/product-ui-taste/material-ops-home/score.json").read_text(encoding="utf-8"))
if material_payload.get("evidence_level") != "L0":
    errors.append("material-ops-home evidence_level must stay L0 as the static screenshot calibration case")
if not has_l2_plus:
    errors.append("product-ui-taste must include at least one L2+ browser evidence case")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
PY

score_json_paths=(
  evals/product-ui-taste/material-ops-home/score.json
  evals/product-ui-taste/before-after/generic-review-workbench-local-l4/score.before.json
  evals/product-ui-taste/before-after/generic-review-workbench-local-l4/score.after.json
  evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/score.before.json
  evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4/score.after.json
)
for score_json in "${score_json_paths[@]}"; do
  if [[ -e "${score_json}" ]]; then
    python3 scripts/design_craft_browser_evidence.py --validate-score-json "${score_json}" >/dev/null
  fi
done

echo "design-craft validation passed."
