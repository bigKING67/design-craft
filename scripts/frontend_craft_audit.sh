#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

TARGET="."
MODE="audit"
SURFACE="auto"
INTENT="auto"
SCOPE="auto"
STYLE="auto"
SKIP_ROUTE=0
SKIP_DETECTOR=0
SKIP_SCORE=0
STRICT=0

usage() {
  cat <<'EOF'
Usage:
  scripts/frontend_craft_audit.sh [options]

Options:
  --target <path>     Project, folder, or file to audit.
  --mode <mode>       critique|audit|polish|harden|optimize|structure|architecture.
  --surface <value>   Route planner surface, default auto.
  --intent <value>    Route planner intent, default auto.
  --scope <value>     Route planner scope, default auto.
  --style <value>     Route planner style, default auto.
  --skip-route        Do not call frontend_craft_route.sh.
  --skip-detector     Do not call frontend_craft_detect.sh.
  --skip-score        Do not call frontend_craft_score.py.
  --strict            Exit non-zero if a sub-check exits non-zero.
EOF
}

abspath() {
  python3 - "$1" <<'PY'
import sys
from pathlib import Path
print(Path(sys.argv[1]).expanduser().resolve())
PY
}

section() {
  printf '\n== %s ==\n' "$1"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:?Missing value for --target}"
      shift 2
      ;;
    --mode)
      MODE="${2:?Missing value for --mode}"
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
    --skip-route)
      SKIP_ROUTE=1
      shift
      ;;
    --skip-detector)
      SKIP_DETECTOR=1
      shift
      ;;
    --skip-score)
      SKIP_SCORE=1
      shift
      ;;
    --strict)
      STRICT=1
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

case "${MODE}" in
  critique|audit|polish|harden|optimize|structure|architecture) ;;
  *)
    echo "Unknown mode: ${MODE}" >&2
    usage >&2
    exit 2
    ;;
esac

TARGET="$(abspath "${TARGET}")"
overall_status=0

section "frontend-craft ${MODE}"
echo "target: ${TARGET}"
echo "surface: ${SURFACE}"
echo "intent: ${INTENT}"
echo "scope: ${SCOPE}"
echo "style: ${STYLE}"

if [[ "${SKIP_ROUTE}" != "1" ]]; then
  section "route"
  set +e
  "${ROOT_DIR}/scripts/frontend_craft_route.sh" \
    --target "${TARGET}" \
    --surface "${SURFACE}" \
    --intent "${INTENT}" \
    --scope "${SCOPE}" \
    --style "${STYLE}"
  status=$?
  set -e
  if [[ "${status}" != "0" ]]; then
    overall_status="${status}"
    echo "route_status: ${status}"
    echo "route_note: inspect preflight output before implementation."
  fi
else
  section "route"
  echo "skipped"
fi

if [[ "${SKIP_DETECTOR}" != "1" ]]; then
  section "detector"
  set +e
  "${ROOT_DIR}/scripts/frontend_craft_detect.sh" --target "${TARGET}"
  status=$?
  set -e
  if [[ "${status}" != "0" ]]; then
    overall_status="${status}"
    echo "detector_status: ${status}"
  fi
else
  section "detector"
  echo "skipped"
fi

if [[ "${SKIP_SCORE}" != "1" ]]; then
  section "frontend-craft source score"
  if [[ "${TARGET}" == "${ROOT_DIR}" || "${TARGET}" == "${ROOT_DIR}/"* ]]; then
    set +e
    "${ROOT_DIR}/scripts/frontend_craft_score.py" --self
    status=$?
    set -e
    if [[ "${status}" != "0" ]]; then
      overall_status="${status}"
      echo "score_status: ${status}"
    fi
  else
    echo "skipped: target is not the frontend-craft source repo."
  fi
else
  section "frontend-craft source score"
  echo "skipped"
fi

section "mode checklist"
case "${MODE}" in
  critique)
    cat <<'EOF'
- Start with one design read: surface, audience, vibe, and primary job.
- Judge product-job fit before decoration: what decision or action becomes clearer?
- Check hierarchy, density, typography rhythm, color intent, motion restraint, and responsive risk.
- Call out generic AI tells: nested-card soup, vague labels, fake gradients, ornamental noise, and weak empty states.
- If the user asks for a score or why the UI is not 100, use product-ui-taste-review.md plus taste-score-calibration.md; label evidence level and product UI taste score.
- Report method provenance for full critiques: dual-agent only if it actually ran; otherwise say single-context/degraded with the reason.
- Classify issues as P0/P1/P2/P3 and recommend the next pass: shape, polish, harden, optimize, or implement.
- Keep this read-only unless the user asks for changes.
EOF
    ;;
  audit)
    cat <<'EOF'
- Confirm authority order: live runtime > scoped AGENTS/README > DESIGN.md > route > frontend-craft references.
- Classify findings as P0/P1/P2/P3.
- Separate candidate_skills from selected_skills.
- Require browser validation for visible UI changes.
- Require screenshot artifact evidence when route output requires browser screenshots.
EOF
    ;;
  polish)
    cat <<'EOF'
- Polish only after function works.
- Check alignment, spacing, hierarchy, line length, tokens, focus, hover, disabled, loading, error, and reduced motion.
- Do not turn polish into redesign without approval.
EOF
    ;;
  harden)
    cat <<'EOF'
- Test hostile data: empty, long labels, missing fields, 4xx/5xx, slow network, permissions, large numbers, and narrow viewport.
- Bound lists and tables; avoid hidden fallback paths.
- Keep recovery actions visible.
EOF
    ;;
  optimize)
    cat <<'EOF'
- Establish a baseline first.
- Target LCP, INP, CLS, bundle cost, render hot paths, chart/table scale, and animation cost.
- Roll back changes that do not improve the target or simplify code.
EOF
    ;;
  structure)
    cat <<'EOF'
- Add files only where existing conventions support them.
- Shared abstractions require repeated real callers and the same intent.
- Avoid parallel source trees and vague utility folders.
EOF
    ;;
  architecture)
    cat <<'EOF'
- Identify runtime entrypoint, route ownership, state ownership, data sources, trust boundaries, interfaces, migration, and rollback.
- Preserve current architecture unless there is a concrete failure.
EOF
    ;;
esac

section "status"
if [[ "${overall_status}" == "0" ]]; then
  echo "frontend-craft audit wrapper completed."
else
  echo "frontend-craft audit wrapper completed with sub-check status ${overall_status}."
fi

if [[ "${STRICT}" == "1" ]]; then
  exit "${overall_status}"
fi

exit 0
