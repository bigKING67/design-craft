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
export PYTHONDONTWRITEBYTECODE=1

python_syntax_check() {
  python3 - "$1" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
compile(path.read_text(encoding="utf-8"), str(path), "exec")
PY
}

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
  "package-lock.json"
  "Makefile"
  ".github/workflows/validate.yml"
  ".github/workflows/upstream-audit.yml"
  ".github/workflows/native-runtime.yml"
  ".github/scripts/upstream_review_issue.cjs"
  ".gitmodules"
  "docs/maintenance.md"
  "THIRD_PARTY_NOTICES.md"
  "upstreams.lock.json"
  "skills/design-craft/SKILL.md"
  "skills/design-craft/VERSION"
  "skills/design-craft/COMPATIBILITY.json"
  "skills/design-craft/agents/openai.yaml"
  "skills/design-craft/references/source-map.md"
  "skills/design-craft/references/product-context.md"
  "skills/design-craft/references/product-design-principles.md"
  "skills/design-craft/references/interaction-physics.md"
  "skills/design-craft/references/ios-quality.md"
  "skills/design-craft/references/android-quality.md"
  "skills/design-craft/references/adaptive-quality.md"
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
  "skills/design-craft/templates/l4-eval-case/input.md"
  "skills/design-craft/templates/l4-eval-case/score.before.json"
  "skills/design-craft/templates/l4-eval-case/score.after.json"
  "skills/design-craft/templates/l4-eval-case/diff-summary.md"
  "skills/design-craft/templates/l4-eval-case/validation.md"
  "skills/design-craft/templates/l4-eval-case/screenshots.json"
  "skills/design-craft/scripts/design_craft_audit.sh"
  "skills/design-craft/scripts/design_craft_browser_evidence.py"
  "skills/design-craft/scripts/design_craft_css_smell_scan.py"
  "skills/design-craft/scripts/design_craft_detect.sh"
  "skills/design-craft/scripts/design_craft_focus_audit.py"
  "skills/design-craft/scripts/design_craft_l4_capture.py"
  "skills/design-craft/scripts/design_craft_l4_case_validate.py"
  "skills/design-craft/scripts/design_craft_l4_eval_case.sh"
  "skills/design-craft/scripts/design_craft_l4_evidence_manifest.py"
  "skills/design-craft/scripts/design_craft_pass.sh"
  "skills/design-craft/scripts/design_craft_platform_scan.py"
  "skills/design-craft/scripts/design_craft_route.sh"
  "skills/design-craft/scripts/design_craft_seed_design.sh"
  "skills/design-craft/scripts/design_craft_static_review.py"
  "skills/design-craft/scripts/design_craft_taste_review.sh"
  "skills/design-craft/scripts/design_craft_token_audit.py"
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
  "evals/cross-agent/_template/criteria.json"
  "evals/cross-agent/same-prompt-dashboard-review/prompt.md"
  "evals/cross-agent/same-prompt-dashboard-review/expected-findings.md"
  "evals/cross-agent/same-prompt-dashboard-review/scorecard.md"
  "evals/cross-agent/same-prompt-landing-polish/prompt.md"
  "evals/cross-agent/same-prompt-landing-polish/expected-findings.md"
  "evals/cross-agent/same-prompt-landing-polish/scorecard.md"
  "evals/cross-agent/same-prompt-motion-review/prompt.md"
  "evals/cross-agent/same-prompt-motion-review/expected-findings.md"
  "evals/cross-agent/same-prompt-motion-review/scorecard.md"
  "evals/cross-agent/same-prompt-motion-review/codex-output.md"
  "evals/cross-agent/same-prompt-motion-review/pi-output.md"
  "evals/cross-agent/same-prompt-motion-review/score.codex.json"
  "evals/cross-agent/same-prompt-motion-review/score.pi.json"
  "evals/cross-agent/same-prompt-motion-review/comparison.md"
  "evals/cross-agent/same-prompt-motion-review/cursor-unverified.md"
  "evals/cross-agent/same-prompt-motion-review/claude-unverified.md"
  "evals/cross-agent/same-prompt-native-adaptive-review/prompt.md"
  "evals/cross-agent/same-prompt-native-adaptive-review/expected-findings.md"
  "evals/cross-agent/same-prompt-native-adaptive-review/scorecard.md"
  "evals/cross-agent/same-prompt-native-adaptive-review/codex-output.md"
  "evals/cross-agent/same-prompt-native-adaptive-review/pi-output.md"
  "evals/cross-agent/same-prompt-native-adaptive-review/score.codex.json"
  "evals/cross-agent/same-prompt-native-adaptive-review/score.pi.json"
  "evals/cross-agent/same-prompt-native-adaptive-review/comparison.md"
  "evals/cross-agent/same-prompt-native-adaptive-review/cursor-unverified.md"
  "evals/cross-agent/same-prompt-native-adaptive-review/claude-unverified.md"
  "evals/native-runtime/README.md"
  "evals/native-runtime/environment-probe.json"
  "evals/native-runtime/fixtures/ios/App.swift"
  "evals/native-runtime/fixtures/ios/Info.plist"
  "evals/native-runtime/fixtures/android/settings.gradle.kts"
  "evals/native-runtime/fixtures/android/build.gradle.kts"
  "evals/native-runtime/fixtures/android/app/build.gradle.kts"
  "evals/native-runtime/fixtures/android/app/src/main/AndroidManifest.xml"
  "evals/native-runtime/fixtures/android/app/src/main/java/dev/designcraft/runtimeevidence/MainActivity.java"
  "evals/fixtures/css-smells/card-soup.css"
  "evals/fixtures/focus-smells/Button.tsx"
  "evals/fixtures/l4-pages/generic-review-workbench/index.html"
  "evals/fixtures/l4-pages/ops-dashboard-decision-surface/index.html"
  "evals/fixtures/l4-pages/gesture-sheet-interaction/index.html"
  "evals/fixtures/l4-pages/gesture-sheet-interaction/validation.json"
  "evals/fixtures/platforms/ios/valid/PRODUCT.md"
  "evals/fixtures/platforms/ios/valid/App.swift"
  "evals/fixtures/platforms/ios/invalid/PRODUCT.md"
  "evals/fixtures/platforms/ios/invalid/App.swift"
  "evals/fixtures/platforms/android/valid/PRODUCT.md"
  "evals/fixtures/platforms/android/valid/Review.kt"
  "evals/fixtures/platforms/android/invalid/PRODUCT.md"
  "evals/fixtures/platforms/android/invalid/Review.kt"
  "evals/fixtures/platforms/adaptive/valid/PRODUCT.md"
  "evals/fixtures/platforms/adaptive/valid/package.json"
  "evals/fixtures/platforms/adaptive/valid/Review.tsx"
  "evals/fixtures/platforms/adaptive/invalid/PRODUCT.md"
  "evals/fixtures/platforms/adaptive/invalid/package.json"
  "evals/fixtures/platforms/adaptive/invalid/Review.tsx"
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
  "scripts/design_craft_maturity.py"
  "scripts/design_craft_native_runtime_validate.py"
  "scripts/design_craft_native_runtime_record.py"
  "scripts/design_craft_platform_scan.py"
  "scripts/design_craft_browser_evidence.py"
  "scripts/design_craft_codex_route_pack.py"
  "scripts/design_craft_cross_agent_validate.py"
  "scripts/design_craft_cross_agent_record.py"
  "scripts/design_craft_evidence_common.py"
  "scripts/design_craft_css_smell_scan.py"
  "scripts/design_craft_focus_audit.py"
  "scripts/design_craft_github_checks.py"
  "scripts/design_craft_static_review.py"
  "scripts/design_craft_token_audit.py"
  "scripts/design_craft_pass.sh"
  "scripts/design_craft_route.sh"
  "scripts/design_craft_seed_design.sh"
  "scripts/design_craft_taste_review.sh"
  "scripts/design_craft_score.py"
  "scripts/design_craft_install_verify.py"
  "scripts/design_craft_release_verify.py"
  "scripts/design_craft_sync_status.py"
  "scripts/native_runtime_ci_ios.sh"
  "scripts/native_runtime_ci_android.sh"
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

python3 - <<'PY'
import json
import re
from pathlib import Path

path = Path("evals/fixtures/l4-pages/gesture-sheet-interaction/validation.json")
payload = json.loads(path.read_text(encoding="utf-8"))
assert payload.get("schema") == "design-craft.gesture-fixture-validation.v1"
assert payload.get("scenario", {}).get("schema") == "design-craft.gesture-fixture-trace.v1"
assert payload.get("scenario", {}).get("trace_length", 0) >= 10
assert all(payload.get("scenario", {}).get("assertions", {}).values())
screenshot = payload.get("screenshot", {})
assert screenshot.get("target") == "viewport"
assert screenshot.get("repo_external") is True
assert re.fullmatch(r"[0-9a-f]{64}", screenshot.get("sha256", ""))
assert len(screenshot.get("dimensions", [])) == 2
assert all(isinstance(value, int) and value > 0 for value in screenshot["dimensions"])
assert payload.get("cleanup", {}).get("remaining_unkept_count") == 0
PY


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

if ! cmp -s VERSION skills/design-craft/VERSION; then
  echo "skills/design-craft/VERSION must match root VERSION" >&2
  exit 1
fi

node <<'NODE'
const fs = require("fs");
const pkg = JSON.parse(fs.readFileSync("package.json", "utf8"));
const lock = JSON.parse(fs.readFileSync("package-lock.json", "utf8"));
const version = fs.readFileSync("VERSION", "utf8").trim();
if (pkg.version !== version) {
  throw new Error(`package.json version (${pkg.version}) must match VERSION (${version})`);
}
if (lock.name !== pkg.name || lock.version !== version) {
  throw new Error("package-lock.json root name/version must match package.json and VERSION");
}
if (!lock.packages || !lock.packages[""] || lock.packages[""].version !== version) {
  throw new Error("package-lock.json packages root version must match VERSION");
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
const compatibility = JSON.parse(fs.readFileSync("skills/design-craft/COMPATIBILITY.json", "utf8"));
if (
  compatibility.schema !== "design-craft.compatibility.v1" ||
  !compatibility.codex_route_pack ||
  compatibility.codex_route_pack.schema !== "design-craft.codex-route-pack.v2" ||
  compatibility.codex_route_pack.manifest_schema !== "codex.frontend-route-pack.manifest.v1" ||
  compatibility.codex_route_pack.snapshot_schema !== "codex.global_agents.snapshot.v2" ||
  compatibility.codex_route_pack.routing_version !== 2 ||
  !compatibility.evidence_contracts ||
  compatibility.evidence_contracts.cross_agent !== "design-craft.cross-agent-score.v2" ||
  compatibility.evidence_contracts.native_runtime !== "design-craft.native-runtime-evidence.v2" ||
  compatibility.evidence_contracts.release_verification !== "design-craft.release-verification.v1" ||
  compatibility.evidence_contracts.github_checks !== "design-craft.github-checks.v1"
) {
  throw new Error("skills/design-craft/COMPATIBILITY.json must pin route-pack and evidence contracts");
}
NODE
node --check .github/scripts/upstream_review_issue.cjs
node <<'NODE'
const assert = require("assert");
const maintainIssue = require("./.github/scripts/upstream_review_issue.cjs");

function mockGithub(issues) {
  const calls = [];
  return {
    calls,
    rest: {
      issues: {
        listForRepo: async () => ({ data: issues }),
        create: async (args) => calls.push(["create", args]),
        update: async (args) => calls.push(["update", args]),
        createComment: async (args) => calls.push(["comment", args]),
      },
    },
  };
}

(async () => {
  process.env.GITHUB_SERVER_URL = "https://github.com";
  process.env.GITHUB_REPOSITORY = "example/design-craft";
  process.env.GITHUB_RUN_ID = "1";
  const context = { repo: { owner: "example", repo: "design-craft" } };

  const createGithub = mockGithub([]);
  await maintainIssue({ github: createGithub, context, mode: "drift", reportPath: "README.md" });
  assert.equal(createGithub.calls[0][0], "create");

  const issue = { number: 7, title: "[design-craft] Upstream review required" };
  const updateGithub = mockGithub([issue]);
  await maintainIssue({ github: updateGithub, context, mode: "drift", reportPath: "README.md" });
  assert.equal(updateGithub.calls[0][0], "update");

  const resolveGithub = mockGithub([issue]);
  await maintainIssue({ github: resolveGithub, context, mode: "resolved" });
  assert.deepEqual(resolveGithub.calls.map((call) => call[0]), ["comment", "update"]);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
NODE

if ! grep -q "make release-gate" README.md; then
  echo "README.md must document make release-gate" >&2
  exit 1
fi

if ! grep -q "make release-gate" docs/maintenance.md; then
  echo "docs/maintenance.md must document make release-gate" >&2
  exit 1
fi

if ! grep -q "make release-readiness" README.md || ! grep -q "make release-readiness" docs/maintenance.md; then
  echo "README.md and docs/maintenance.md must document make release-readiness" >&2
  exit 1
fi

python3 - <<'PY'
from pathlib import Path

makefile = Path("Makefile").read_text(encoding="utf-8")
source_line = next(line for line in makefile.splitlines() if line.startswith("release-gate-source:"))
if "upstream-freshness" in source_line or "upstream-remote" in source_line:
    raise SystemExit("release-gate-source must not depend on mutable upstream freshness")
if "release-readiness: release-gate" not in makefile or "--remote-details --fail-on-unreviewed" not in makefile:
    raise SystemExit("release-readiness must add the actionable remote freshness audit")

workflow = Path(".github/workflows/upstream-audit.yml").read_text(encoding="utf-8")
for needle in ("17 3 * * *", "--remote-details", "issues: write", "Open or update review issue"):
    if needle not in workflow:
        raise SystemExit(f"upstream audit workflow missing {needle!r}")
PY

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
	"scripts/design_craft_maturity.py" \
	"scripts/design_craft_native_runtime_validate.py" \
	"scripts/design_craft_native_runtime_record.py" \
  "scripts/design_craft_platform_scan.py" \
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
	"scripts/design_craft_install_verify.py" \
	"scripts/design_craft_release_verify.py" \
	"scripts/design_craft_sync_status.py" \
	"scripts/design_craft_cross_agent_record.py" \
	"scripts/design_craft_evidence_common.py" \
	"scripts/design_craft_github_checks.py" \
	"scripts/native_runtime_ci_ios.sh" \
	"scripts/native_runtime_ci_android.sh" \
  "skills/design-craft/scripts/design_craft_audit.sh" \
  "skills/design-craft/scripts/design_craft_browser_evidence.py" \
  "skills/design-craft/scripts/design_craft_css_smell_scan.py" \
  "skills/design-craft/scripts/design_craft_detect.sh" \
  "skills/design-craft/scripts/design_craft_focus_audit.py" \
  "skills/design-craft/scripts/design_craft_l4_capture.py" \
  "skills/design-craft/scripts/design_craft_l4_case_validate.py" \
  "skills/design-craft/scripts/design_craft_l4_eval_case.sh" \
  "skills/design-craft/scripts/design_craft_l4_evidence_manifest.py" \
  "skills/design-craft/scripts/design_craft_pass.sh" \
  "skills/design-craft/scripts/design_craft_platform_scan.py" \
  "skills/design-craft/scripts/design_craft_route.sh" \
  "skills/design-craft/scripts/design_craft_seed_design.sh" \
  "skills/design-craft/scripts/design_craft_static_review.py" \
  "skills/design-craft/scripts/design_craft_taste_review.sh" \
  "skills/design-craft/scripts/design_craft_token_audit.py" \
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

if find "${SKILL_DIR}" -type d -name __pycache__ -print -quit | grep -q .; then
  echo "Canonical skill must not contain __pycache__ directories" >&2
  exit 1
fi

for path in \
  scripts/install_local.sh \
  scripts/sync_upstreams.sh \
  scripts/validate.sh \
  scripts/design_craft_audit.sh \
  scripts/design_craft_detect.sh \
  scripts/design_craft_doctor.sh \
  scripts/design_craft_init_agent.sh \
  scripts/design_craft_l4_eval_case.sh \
  scripts/design_craft_pass.sh \
  scripts/design_craft_route.sh \
  scripts/design_craft_seed_design.sh \
  scripts/design_craft_taste_review.sh \
  scripts/native_runtime_ci_ios.sh \
  scripts/native_runtime_ci_android.sh \
  skills/design-craft/scripts/design_craft_audit.sh \
  skills/design-craft/scripts/design_craft_detect.sh \
  skills/design-craft/scripts/design_craft_l4_eval_case.sh \
  skills/design-craft/scripts/design_craft_pass.sh \
  skills/design-craft/scripts/design_craft_route.sh \
  skills/design-craft/scripts/design_craft_seed_design.sh \
  skills/design-craft/scripts/design_craft_taste_review.sh \
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
make -n release-readiness >/dev/null
make -n release-certify >/dev/null
make -n release-tag-verify >/dev/null
make -n sync-status >/dev/null

python3 - <<'PY'
from pathlib import Path

makefile = Path("Makefile").read_text(encoding="utf-8")
four_host_recipe = makefile.split("cross-agent-four-host-check:", 1)[1].split("\n\n", 1)[0]
for needle in ("set -e", "--require-schema-v2", "--require-current-source"):
    if needle not in four_host_recipe:
        raise SystemExit(f"cross-agent-four-host-check missing {needle!r}")
certify_recipe = makefile.split("release-certify:", 1)[1].split("\n\n", 1)[0]
for needle in ("cross-agent-four-host-check", "native-runtime-check", "--min-score 100"):
    if needle not in certify_recipe:
        raise SystemExit(f"release-certify missing {needle!r}")
PY

for path in \
  scripts/design_craft_score.py \
  scripts/design_craft_active_scope_validate.py \
  scripts/design_craft_browser_evidence.py \
  scripts/design_craft_codex_route_pack.py \
  scripts/design_craft_cross_agent_validate.py \
  scripts/design_craft_cross_agent_record.py \
	scripts/design_craft_evidence_common.py \
	scripts/design_craft_github_checks.py \
  scripts/design_craft_l4_capture.py \
  scripts/design_craft_l4_case_validate.py \
  scripts/design_craft_l4_evidence_manifest.py \
	scripts/design_craft_maturity.py \
	scripts/design_craft_native_runtime_validate.py \
	scripts/design_craft_native_runtime_record.py \
  scripts/design_craft_platform_scan.py \
  scripts/design_craft_css_smell_scan.py \
  scripts/design_craft_focus_audit.py \
  scripts/design_craft_static_review.py \
	scripts/design_craft_token_audit.py \
	scripts/design_craft_install_verify.py \
	scripts/design_craft_release_verify.py \
	scripts/design_craft_sync_status.py \
  scripts/frontend_craft_score.py \
  scripts/frontend_craft_browser_evidence.py \
  scripts/upstream_absorption_report.py \
  skills/design-craft/scripts/design_craft_browser_evidence.py \
  skills/design-craft/scripts/design_craft_css_smell_scan.py \
  skills/design-craft/scripts/design_craft_focus_audit.py \
  skills/design-craft/scripts/design_craft_l4_capture.py \
  skills/design-craft/scripts/design_craft_l4_case_validate.py \
  skills/design-craft/scripts/design_craft_l4_evidence_manifest.py \
  skills/design-craft/scripts/design_craft_platform_scan.py \
  skills/design-craft/scripts/design_craft_static_review.py \
  skills/design-craft/scripts/design_craft_token_audit.py; do
  python_syntax_check "${path}"
done

python3 scripts/upstream_absorption_report.py --check
python3 scripts/design_craft_maturity.py --check
python3 scripts/design_craft_native_runtime_validate.py --check
python3 - <<'PY'
import json
import plistlib
import xml.etree.ElementTree as ET
from pathlib import Path

payload = json.loads(Path("evals/native-runtime/environment-probe.json").read_text(encoding="utf-8"))
assert payload.get("schema") == "design-craft.native-runtime-probe.v1"
assert isinstance(payload.get("ios", {}).get("ready"), bool)
assert isinstance(payload.get("android", {}).get("ready"), bool)
plist = plistlib.loads(Path("evals/native-runtime/fixtures/ios/Info.plist").read_bytes())
assert plist.get("CFBundleIdentifier") == "dev.designcraft.runtime-evidence"
ET.parse("evals/native-runtime/fixtures/android/app/src/main/AndroidManifest.xml")

workflow = Path(".github/workflows/native-runtime.yml").read_text(encoding="utf-8")
for needle in ("native_runtime_ci_ios.sh", "reactivecircus/android-emulator-runner@", "native_runtime_ci_android.sh"):
    assert needle in workflow
ios_runner = Path("scripts/native_runtime_ci_ios.sh").read_text(encoding="utf-8")
android_runner = Path("scripts/native_runtime_ci_android.sh").read_text(encoding="utf-8")
assert "xcrun simctl" in ios_runner and "design_craft_native_runtime_record.py" in ios_runner
assert "simctl openurl" in ios_runner and "runtime-interaction.txt" in ios_runner
assert "uiautomator" in android_runner and "design_craft_native_runtime_record.py" in android_runner
PY

python3 - <<'PY'
import re
from pathlib import Path

for workflow in Path(".github/workflows").glob("*.yml"):
    for line_number, line in enumerate(workflow.read_text(encoding="utf-8").splitlines(), start=1):
        match = re.search(r"\buses:\s*[^@\s]+@([^\s#]+)", line)
        if match and not re.fullmatch(r"[0-9a-f]{40}", match.group(1)):
            raise SystemExit(f"{workflow}:{line_number}: action must be pinned to a full SHA")
PY

(
  tmp_native_dir="$(mktemp -d -t design-craft-native-record.XXXXXX)"
  trap 'rm -rf "${tmp_native_dir}"' EXIT
  printf '%s\n' runtime > "${tmp_native_dir}/artifact.txt"
  python3 scripts/design_craft_native_runtime_record.py \
    --platform ios \
    --runtime-kind ios_simulator \
    --runtime-id fixture-simulator \
    --tool fixture \
    --command "fixture build" \
    --assertion build=true \
    --assertion launch=true \
    --assertion screenshot=true \
    --artifact "${tmp_native_dir}/artifact.txt" \
    --fixture-root evals/native-runtime/fixtures/ios \
    --output "${tmp_native_dir}/ios-observed.json" >/dev/null
  python3 scripts/design_craft_native_runtime_validate.py \
    --validate \
    --root "${tmp_native_dir}" \
    --require ios >/dev/null
)

(
  tmp_install_dir="$(mktemp -d -t design-craft-install-validation.XXXXXX)"
  trap 'rm -rf "${tmp_install_dir}"' EXIT
  export DESIGN_CRAFT_SKILL_ROOT="${tmp_install_dir}/skills"
  export DESIGN_CRAFT_BACKUP_ROOT="${tmp_install_dir}/backups"
  bash scripts/install_local.sh --keep-backups 2 >/dev/null
  test ! -e "${DESIGN_CRAFT_SKILL_ROOT}/frontend-craft"
  python3 scripts/design_craft_install_verify.py \
    --source skills/design-craft \
    --installed "${DESIGN_CRAFT_SKILL_ROOT}/design-craft" \
    --expected-name design-craft \
    --expected-version "$(cat VERSION)" \
    --require-metadata >/dev/null
  python3 - "${DESIGN_CRAFT_SKILL_ROOT}/design-craft/.design-craft-install.json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
payload["source_commit"] = "0" * 40
path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY
  if python3 scripts/design_craft_install_verify.py \
    --source skills/design-craft \
    --installed "${DESIGN_CRAFT_SKILL_ROOT}/design-craft" \
    --expected-name design-craft \
    --expected-version "$(cat VERSION)" \
    --require-metadata >/dev/null 2>&1; then
    echo "Stale install source_commit unexpectedly passed provenance validation" >&2
    exit 1
  fi
  bash scripts/install_local.sh --keep-backups 2 >/dev/null
  if DESIGN_CRAFT_INSTALL_TEST_FAIL_AFTER_BACKUP=1 bash scripts/install_local.sh --keep-backups 2 >/dev/null 2>&1; then
    echo "Installer after-backup failpoint unexpectedly passed" >&2
    exit 1
  fi
  python3 scripts/design_craft_install_verify.py \
    --source skills/design-craft \
    --installed "${DESIGN_CRAFT_SKILL_ROOT}/design-craft" \
    --expected-name design-craft \
    --expected-version "$(cat VERSION)" \
    --require-metadata >/dev/null
  if DESIGN_CRAFT_INSTALL_TEST_FAIL_AFTER_SWITCH=1 bash scripts/install_local.sh --keep-backups 2 >/dev/null 2>&1; then
    echo "Installer after-switch failpoint unexpectedly passed" >&2
    exit 1
  fi
  python3 scripts/design_craft_install_verify.py \
    --source skills/design-craft \
    --installed "${DESIGN_CRAFT_SKILL_ROOT}/design-craft" \
    --expected-name design-craft \
    --expected-version "$(cat VERSION)" \
    --require-metadata >/dev/null
  mkdir -p "${DESIGN_CRAFT_SKILL_ROOT}/frontend-craft"
  printf '%s\n' stale > "${DESIGN_CRAFT_SKILL_ROOT}/frontend-craft/stale.txt"
  for _ in 1 2 3; do
    bash scripts/install_local.sh --keep-backups 2 >/dev/null
  done
  python3 scripts/design_craft_install_verify.py \
    --source skills/frontend-craft \
    --installed "${DESIGN_CRAFT_SKILL_ROOT}/frontend-craft" \
    --expected-name frontend-craft \
    --expected-version "$(cat VERSION)" \
    --require-metadata >/dev/null
  backup_count="$(find "${DESIGN_CRAFT_BACKUP_ROOT}/design-craft" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d '[:space:]')"
  if (( backup_count > 2 )); then
    echo "Installer backup retention failed: ${backup_count} backups remain" >&2
    exit 1
  fi
)

python3 - <<'PY'
import json
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "scripts/design_craft_score.py", "--self", "--no-smoke", "--json"],
    check=False,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
payload = json.loads(result.stdout)
if (
    result.returncode != 0
    or payload.get("schema") != "design-craft.source-completeness.v1"
    or payload.get("score") != 100
):
    raise SystemExit(
        "source completeness must be 100/100: "
        f"rc={result.returncode} schema={payload.get('schema')} score={payload.get('score')}"
    )
PY
python3 scripts/design_craft_browser_evidence.py --check --print-js >/dev/null
if [[ "${PORTABLE}" == "0" ]]; then
  python3 scripts/design_craft_codex_route_pack.py --check >/dev/null
  python3 scripts/design_craft_codex_route_pack.py --strict >/dev/null
fi
python3 scripts/design_craft_cross_agent_validate.py --check >/dev/null
python3 scripts/design_craft_cross_agent_validate.py --root evals/cross-agent >/dev/null
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-dashboard-review >/dev/null
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-motion-review >/dev/null
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-native-adaptive-review >/dev/null
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
python3 - <<'PY'
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path.cwd()


def run(command, *, env=None):
    result = subprocess.run(
        [str(part) for part in command],
        cwd=root,
        env=env,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result


for platform in ("ios", "android", "adaptive"):
    valid = run(
        [
            sys.executable,
            "scripts/design_craft_platform_scan.py",
            "--target",
            f"evals/fixtures/platforms/{platform}/valid",
            "--json",
            "--strict",
        ]
    )
    invalid = run(
        [
            sys.executable,
            "scripts/design_craft_platform_scan.py",
            "--target",
            f"evals/fixtures/platforms/{platform}/invalid",
            "--json",
            "--strict",
        ]
    )
    if valid.returncode != 0 or invalid.returncode == 0:
        raise SystemExit(
            f"{platform} platform fixtures failed: valid_rc={valid.returncode} invalid_rc={invalid.returncode}"
        )

with tempfile.TemporaryDirectory(prefix="design-craft-portable-") as raw:
    temp = Path(raw)
    target = temp / "target"
    target.mkdir()
    (target / "DESIGN.md").write_text(
        "# Design\n\n"
        "## Typography System\nSystem type.\n\n"
        "## Color Palette\nSemantic roles.\n\n"
        "## Motion Language\nReduced motion.\n\n"
        "## Component Grammar\nNative states.\n",
        encoding="utf-8",
    )
    (target / "PRODUCT.md").write_text(
        "# Product Context\n\n## Platform\nadaptive\n",
        encoding="utf-8",
    )
    route_env = dict(os.environ)
    route_env["DESIGN_CRAFT_ROUTE_PLAN"] = str(temp / "missing-route-plan.sh")
    route = run(
        [
            "bash",
            "skills/design-craft/scripts/design_craft_route.sh",
            "--target",
            target,
            "--surface",
            "mobile",
            "--intent",
            "visual-refine",
            "--scope",
            "component",
            "--json-only",
        ],
        env=route_env,
    )
    route_payload = json.loads(route.stdout)
    if not (
        route.returncode == 0
        and route_payload.get("route_source") == "portable_fallback"
        and route_payload.get("degraded") is True
        and route_payload.get("platform") == "adaptive"
        and route_payload.get("native_validation_required") is True
    ):
        raise SystemExit("portable route fallback contract failed")

    detector_env = dict(os.environ)
    detector_env["HOME"] = str(temp / "home")
    detector_env["DESIGN_CRAFT_SOURCE_ROOT"] = str(temp / "missing-source")
    detector_env["DESIGN_CRAFT_IMPECCABLE_DETECTOR"] = str(temp / "missing-detector.mjs")
    detector = run(
        [
            "bash",
            "skills/design-craft/scripts/design_craft_detect.sh",
            "--target",
            root / "evals/fixtures/css-smells",
            "--full-json",
        ],
        env=detector_env,
    )
    detector_payload = json.loads(detector.stdout)
    upstream_detector = detector_payload.get("upstream_detector", {})
    if not (
        detector.returncode == 0
        and detector_payload.get("degraded") is True
        and upstream_detector.get("status") == "unavailable"
    ):
        raise SystemExit("portable detector degraded contract failed")

    installed = temp / "installed/design-craft"
    shutil.copytree(root / "skills/design-craft", installed)
    cases = temp / "installed-cases"
    scaffold = run(
        [
            "bash",
            installed / "scripts/design_craft_l4_eval_case.sh",
            "--case-id",
            "portable-installed-runtime",
            "--surface",
            "validation",
            "--output-root",
            cases,
        ]
    )
    if scaffold.returncode != 0:
        raise SystemExit("installed-skill L4 scaffold failed: " + scaffold.stderr.strip())
    manifest = cases / "portable-installed-runtime/screenshots.json"
    manifest_check = run(
        [
            sys.executable,
            installed / "scripts/design_craft_l4_evidence_manifest.py",
            "--validate-screenshots-json",
            manifest,
        ]
    )
    if manifest_check.returncode != 0:
        raise SystemExit("installed-skill L4 manifest validation failed")
PY
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
source_audit_output="$(bash scripts/design_craft_audit.sh --target . --mode audit --skip-route --skip-detector)"
if [[ "${source_audit_output}" != *"design-craft source completeness: 100/100"* ]]; then
  echo "Root audit wrapper did not run the source-completeness scorer" >&2
  exit 1
fi
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
  "product-context.md" \
  "product-design-principles.md" \
  "design-system-contract.md" \
  "foundational-visual-principles.md" \
  "design-move-library.md" \
  "visual-judgment.md" \
  "product-ui-taste-review.md" \
  "taste-score-calibration.md" \
  "impeccable-workflow.md" \
  "intent-map.md" \
  "motion-quality.md" \
  "interaction-physics.md" \
  "motion-vocabulary.md" \
  "ios-quality.md" \
  "android-quality.md" \
  "adaptive-quality.md" \
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
import re
import subprocess
import sys
from pathlib import Path

payload = json.loads(Path("upstreams.lock.json").read_text(encoding="utf-8"))
errors = []
upstreams = payload.get("upstreams", {})
expected = {"taste-skill", "impeccable", "emilkowalski-skills"}
if set(upstreams) != expected:
    errors.append(f"upstream set must be {sorted(expected)}")
for name, meta in upstreams.items():
    path = meta["path"]
    want = meta["commit"]
    for field in ("commit", "reviewed_commit", "absorbed_commit"):
        value = meta.get(field, "")
        if not re.fullmatch(r"[0-9a-f]{40}", value):
            errors.append(f"{name}: {field} must be a full lowercase Git SHA")
    if meta.get("reviewed_commit") != want:
        errors.append(f"{name}: reviewed_commit must match compatibility commit")
    if meta.get("decision") not in {"absorbed", "partial", "provenance_only", "deferred"}:
        errors.append(f"{name}: invalid review decision")
    if not meta.get("reviewed_at") or not meta.get("notes"):
        errors.append(f"{name}: reviewed_at and notes are required")
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

python3 scripts/design_craft_maturity.py --profile portable --min-score 95 --json >/dev/null

echo "design-craft validation passed."
