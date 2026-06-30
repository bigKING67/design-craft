#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROUTE_PLAN="${DESIGN_CRAFT_ROUTE_PLAN:-${HOME}/.codex/tools/frontend_route_plan.sh}"

TARGET="${PWD}"
SURFACE="auto"
INTENT="auto"
SCOPE="auto"
STYLE="auto"
DESIGN_AUTHORITY_MODE="auto"
STYLE_AUTHORITY_PATH=""
HAS_REFERENCE_IMAGE="0"
NEEDS_GENERATED_REFERENCE="0"
EXISTING_PROJECT="1"
JSON_ONLY=0
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage:
  scripts/design_craft_route.sh [options]

Options:
  --target <path>                   Workspace root or file to use for DESIGN.md discovery.
  --surface <value>                 auto|dashboard|app|admin|data-app|landing|promo|homepage|marketing|mobile|brand
  --intent <value>                  auto|functional|visual-refine|redesign|new-page|high-motion|brand|mobile-flow|reference-only
  --scope <value>                   auto|micro|component|section|page|multi-page
  --style <value>                   auto|high-end|minimalist|industrial|gpt-taste|none
  --design-authority-mode <value>   auto|enforce|evolve
  --style-authority-path <path>     Explicit DESIGN.md or equivalent style authority.
  --has-reference-image <0|1>
  --needs-generated-reference <0|1>
  --existing-project <0|1>
  --json-only                       Emit route planner JSON only.
  --dry-run                         Print the resolved command without executing it.
EOF
}

abspath() {
  python3 - "$1" <<'PY'
import sys
from pathlib import Path
print(Path(sys.argv[1]).expanduser().resolve())
PY
}

find_design_md() {
  local start="$1"
  local dir
  start="$(abspath "${start}")"
  if [[ -f "${start}" ]]; then
    dir="$(dirname "${start}")"
  else
    dir="${start}"
  fi
  while [[ "${dir}" != "/" ]]; do
    if [[ -f "${dir}/DESIGN.md" ]]; then
      printf '%s\n' "${dir}/DESIGN.md"
      return 0
    fi
    dir="$(dirname "${dir}")"
  done
  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:?Missing value for --target}"
      shift 2
      ;;
    --surface)
      SURFACE="${2:?Missing value for --surface}"
      shift 2
      ;;
    --intent)
      INTENT="${2:?Missing value for --intent}"
      shift 2
      ;;
    --scope)
      SCOPE="${2:?Missing value for --scope}"
      shift 2
      ;;
    --style)
      STYLE="${2:?Missing value for --style}"
      shift 2
      ;;
    --design-authority-mode)
      DESIGN_AUTHORITY_MODE="${2:?Missing value for --design-authority-mode}"
      shift 2
      ;;
    --style-authority-path)
      STYLE_AUTHORITY_PATH="$(abspath "${2:?Missing value for --style-authority-path}")"
      shift 2
      ;;
    --has-reference-image)
      HAS_REFERENCE_IMAGE="${2:?Missing value for --has-reference-image}"
      shift 2
      ;;
    --needs-generated-reference)
      NEEDS_GENERATED_REFERENCE="${2:?Missing value for --needs-generated-reference}"
      shift 2
      ;;
    --existing-project)
      EXISTING_PROJECT="${2:?Missing value for --existing-project}"
      shift 2
      ;;
    --json-only)
      JSON_ONLY=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

TARGET="$(abspath "${TARGET}")"

if [[ -z "${STYLE_AUTHORITY_PATH}" ]]; then
  STYLE_AUTHORITY_PATH="$(find_design_md "${TARGET}" || true)"
fi

if [[ ! -f "${ROUTE_PLAN}" ]]; then
  echo "Missing route planner: ${ROUTE_PLAN}" >&2
  exit 1
fi

cmd=(
  bash "${ROUTE_PLAN}"
  --surface "${SURFACE}"
  --intent "${INTENT}"
  --scope "${SCOPE}"
  --style "${STYLE}"
  --design-authority-mode "${DESIGN_AUTHORITY_MODE}"
  --has-reference-image "${HAS_REFERENCE_IMAGE}"
  --needs-generated-reference "${NEEDS_GENERATED_REFERENCE}"
  --existing-project "${EXISTING_PROJECT}"
  --output json
)

if [[ -n "${STYLE_AUTHORITY_PATH}" ]]; then
  cmd+=(--style-authority-path "${STYLE_AUTHORITY_PATH}")
fi

if [[ "${DRY_RUN}" == "1" ]]; then
  printf 'FRONTEND_WORKSPACE_ROOT=%q ' "${TARGET}"
  printf '%q ' "${cmd[@]}"
  printf '\n'
  exit 0
fi

TMP_JSON="$(mktemp -t design-craft-route.XXXXXX)"
trap 'rm -f "${TMP_JSON}"' EXIT

set +e
FRONTEND_WORKSPACE_ROOT="${TARGET}" "${cmd[@]}" >"${TMP_JSON}"
status=$?
set -e

if [[ "${JSON_ONLY}" == "1" ]]; then
  cat "${TMP_JSON}"
  exit "${status}"
fi

python3 - "${TMP_JSON}" "${status}" <<'PY'
import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
status = int(sys.argv[2])

surface = payload.get("inputs", {}).get("surface") or "auto"
intent = payload.get("inputs", {}).get("intent") or "auto"
refs = {"references/validation-contract.md"}
if surface in {"landing", "promo", "homepage", "marketing", "brand"}:
    refs.add("references/visual-judgment.md")
if surface in {"dashboard", "admin", "app", "data-app"}:
    refs.add("references/surface-playbooks.md")
if surface in {"dashboard", "data-app"}:
    refs.add("references/report-quality.md")
if payload.get("performance_review_required"):
    refs.add("references/performance-quality.md")
if payload.get("directory_governance_required"):
    refs.add("references/project-structure.md")
if payload.get("frontend_tier") in {"L2", "L3"}:
    refs.add("references/engineering-quality.md")

developer_product_surfaces = {"auto", "dashboard", "app", "admin", "data-app"}
non_seed_intents = {"brand", "high-motion", "mobile-flow", "reference-only"}
has_style_authority = bool(payload.get("style_authority_path"))
existing_project = bool(payload.get("inputs", {}).get("existing_project"))
vercel_geist_seed_applicable = (
    not has_style_authority
    and surface in developer_product_surfaces
    and intent not in non_seed_intents
)
if vercel_geist_seed_applicable:
    refs.add("templates/vercel-geist/design.md")
    refs.add("templates/vercel-geist/design.dark.md")
    if existing_project:
        vercel_geist_seed_reason = (
            "existing developer-product surface has no resolved style authority; "
            "use the Geist seed only if runtime/project style is weak"
        )
    else:
        vercel_geist_seed_reason = (
            "new developer-product surface has no resolved style authority"
        )
elif has_style_authority:
    vercel_geist_seed_reason = "stronger style authority was resolved"
elif surface not in developer_product_surfaces:
    vercel_geist_seed_reason = "surface is not a default developer-product seed case"
else:
    vercel_geist_seed_reason = "intent calls for another style authority path"

print("design-craft route summary:")
for key in [
    "ok",
    "frontend_tier",
    "candidate_skills",
    "execution_mode",
    "subagent_required",
    "style_authority_path",
    "style_authority_mode",
    "preflight_status",
    "preflight_code",
    "browser_validation_required",
    "browser_screenshot_required",
    "preferred_screenshot_tool",
    "directory_governance_required",
    "performance_review_required",
]:
    print(f"- {key}: {payload.get(key)}")
print(f"- vercel_geist_seed_applicable: {vercel_geist_seed_applicable}")
print(f"- vercel_geist_seed_reason: {vercel_geist_seed_reason}")

print("- recommended_design_craft_references:")
for ref in sorted(refs):
    print(f"  - {ref}")

if status != 0:
    print(f"- route_planner_exit_status: {status}")
    print("- note: non-zero status usually means preflight failed; inspect JSON before implementing.")

print("\nraw_json:")
PY

cat "${TMP_JSON}"
exit "${status}"
