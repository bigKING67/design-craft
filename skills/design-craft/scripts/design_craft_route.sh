#!/usr/bin/env bash
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROUTE_PLAN="${DESIGN_CRAFT_ROUTE_PLAN:-${HOME}/.codex/tools/frontend_route_plan.sh}"
PLATFORM_SCAN="${SKILL_ROOT}/scripts/design_craft_platform_scan.py"

TARGET="${PWD}"
SURFACE="auto"
INTENT="auto"
SCOPE="auto"
STYLE="auto"
PLATFORM="auto"
PRODUCT_CONTEXT_PATH=""
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
  design_craft_route.sh [options]

Options:
  --target <path>                   Workspace root or file.
  --surface <value>                 auto|dashboard|app|admin|data-app|landing|promo|homepage|marketing|mobile|brand
  --intent <value>                  auto|functional|visual-refine|redesign|new-page|high-motion|brand|mobile-flow|reference-only
  --scope <value>                   auto|micro|component|section|page|multi-page
  --style <value>                   auto|high-end|minimalist|industrial|gpt-taste|none
  --platform <value>                auto|web|ios|android|adaptive
  --product-context-path <path>     Explicit PRODUCT.md.
  --design-authority-mode <value>   auto|enforce|evolve
  --style-authority-path <path>     Explicit DESIGN.md or equivalent visual authority.
  --has-reference-image <0|1>
  --needs-generated-reference <0|1>
  --existing-project <0|1>
  --json-only                       Emit JSON only.
  --dry-run                         Print the resolved planner command.

When the global Codex planner is unavailable, this script emits a conservative
portable fallback with route_source=portable_fallback and degraded=true.
EOF
}

abspath() {
  python3 - "$1" <<'PY'
import sys
from pathlib import Path
print(Path(sys.argv[1]).expanduser().resolve())
PY
}

find_upward() {
  python3 - "$1" "$2" <<'PY'
import sys
from pathlib import Path

start = Path(sys.argv[1]).expanduser().resolve()
name = sys.argv[2]
if start.is_file():
    start = start.parent
for directory in (start, *start.parents):
    candidate = directory / name
    if candidate.is_file():
        print(candidate)
        break
PY
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="${2:?Missing value for --target}"; shift 2 ;;
    --surface) SURFACE="${2:?Missing value for --surface}"; shift 2 ;;
    --intent) INTENT="${2:?Missing value for --intent}"; shift 2 ;;
    --scope) SCOPE="${2:?Missing value for --scope}"; shift 2 ;;
    --style) STYLE="${2:?Missing value for --style}"; shift 2 ;;
    --platform) PLATFORM="${2:?Missing value for --platform}"; shift 2 ;;
    --product-context-path) PRODUCT_CONTEXT_PATH="$(abspath "${2:?Missing value for --product-context-path}")"; shift 2 ;;
    --design-authority-mode) DESIGN_AUTHORITY_MODE="${2:?Missing value for --design-authority-mode}"; shift 2 ;;
    --style-authority-path) STYLE_AUTHORITY_PATH="$(abspath "${2:?Missing value for --style-authority-path}")"; shift 2 ;;
    --has-reference-image) HAS_REFERENCE_IMAGE="${2:?Missing value for --has-reference-image}"; shift 2 ;;
    --needs-generated-reference) NEEDS_GENERATED_REFERENCE="${2:?Missing value for --needs-generated-reference}"; shift 2 ;;
    --existing-project) EXISTING_PROJECT="${2:?Missing value for --existing-project}"; shift 2 ;;
    --json-only) JSON_ONLY=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "${PLATFORM}" in
  auto|web|ios|android|adaptive) ;;
  *) echo "Invalid platform: ${PLATFORM}" >&2; exit 2 ;;
esac

TARGET="$(abspath "${TARGET}")"
if [[ -z "${STYLE_AUTHORITY_PATH}" ]]; then
  STYLE_AUTHORITY_PATH="$(find_upward "${TARGET}" "DESIGN.md")"
fi
if [[ -z "${PRODUCT_CONTEXT_PATH}" ]]; then
  PRODUCT_CONTEXT_PATH="$(find_upward "${TARGET}" "PRODUCT.md")"
fi

platform_cmd=(python3 "${PLATFORM_SCAN}" --target "${TARGET}" --platform "${PLATFORM}" --mode detect --json)
if [[ -n "${PRODUCT_CONTEXT_PATH}" ]]; then
  platform_cmd+=(--product-context-path "${PRODUCT_CONTEXT_PATH}")
fi
PLATFORM_JSON="$("${platform_cmd[@]}")"

planner_cmd=(
  bash "${ROUTE_PLAN}"
  --surface "${SURFACE}"
  --intent "${INTENT}"
  --scope "${SCOPE}"
  --style "${STYLE}"
  --platform "${PLATFORM}"
  --design-authority-mode "${DESIGN_AUTHORITY_MODE}"
  --has-reference-image "${HAS_REFERENCE_IMAGE}"
  --needs-generated-reference "${NEEDS_GENERATED_REFERENCE}"
  --existing-project "${EXISTING_PROJECT}"
  --output json
)
if [[ -n "${PRODUCT_CONTEXT_PATH}" ]]; then
  planner_cmd+=(--product-context-path "${PRODUCT_CONTEXT_PATH}")
fi
if [[ -n "${STYLE_AUTHORITY_PATH}" ]]; then
  planner_cmd+=(--style-authority-path "${STYLE_AUTHORITY_PATH}")
fi

if [[ "${DRY_RUN}" == "1" ]]; then
  if [[ -x "${ROUTE_PLAN}" ]]; then
    printf 'FRONTEND_WORKSPACE_ROOT=%q ' "${TARGET}"
    printf '%q ' "${planner_cmd[@]}"
    printf '\n'
  else
    printf 'portable_fallback target=%q platform=%q product_context=%q style_authority=%q\n' \
      "${TARGET}" "${PLATFORM}" "${PRODUCT_CONTEXT_PATH}" "${STYLE_AUTHORITY_PATH}"
  fi
  exit 0
fi

TMP_JSON="$(mktemp -t design-craft-route.XXXXXX)"
trap 'rm -f "${TMP_JSON}"' EXIT

planner_status=0
if [[ -x "${ROUTE_PLAN}" ]]; then
  set +e
  FRONTEND_WORKSPACE_ROOT="${TARGET}" "${planner_cmd[@]}" >"${TMP_JSON}"
  planner_status=$?
  set -e
  route_source="codex_global"
else
  route_source="portable_fallback"
  printf '{}\n' >"${TMP_JSON}"
fi

set +e
python3 - \
  "${TMP_JSON}" \
  "${PLATFORM_JSON}" \
  "${route_source}" \
  "${planner_status}" \
  "${SURFACE}" \
  "${INTENT}" \
  "${SCOPE}" \
  "${STYLE}" \
  "${STYLE_AUTHORITY_PATH}" \
  "${DESIGN_AUTHORITY_MODE}" \
  "${EXISTING_PROJECT}" \
  "${HAS_REFERENCE_IMAGE}" \
  "${NEEDS_GENERATED_REFERENCE}" \
  "${JSON_ONLY}" <<'PY'
import json
import sys
from pathlib import Path

(
    route_path,
    platform_raw,
    route_source,
    planner_status_raw,
    surface,
    intent,
    scope,
    style,
    style_authority_path,
    design_authority_mode,
    existing_project_raw,
    has_reference_raw,
    needs_reference_raw,
    json_only_raw,
) = sys.argv[1:]

planner_status = int(planner_status_raw)
existing_project = existing_project_raw == "1"
has_reference = has_reference_raw == "1"
needs_reference = needs_reference_raw == "1"
json_only = json_only_raw == "1"
platform_payload = json.loads(platform_raw)

try:
    route_payload = json.loads(Path(route_path).read_text(encoding="utf-8"))
except Exception:
    route_payload = {}

visual_intents = {
    "visual-refine",
    "redesign",
    "new-page",
    "high-motion",
    "brand",
    "mobile-flow",
    "reference-only",
}
visual = intent in visual_intents or has_reference or needs_reference
large_scope = scope in {"page", "multi-page"} or intent in {
    "redesign",
    "new-page",
    "brand",
    "mobile-flow",
    "high-motion",
}
micro_visual_safe = (
    scope == "micro"
    and intent in {"auto", "functional", "visual-refine"}
    and not has_reference
    and not needs_reference
    and style in {"auto", "none"}
    and design_authority_mode != "evolve"
)
if micro_visual_safe:
    fallback_tier = "L0"
elif not visual and intent in {"auto", "functional"}:
    fallback_tier = "L1-F"
elif large_scope:
    fallback_tier = "L2"
else:
    fallback_tier = "L1-V"

platform = platform_payload["platform"]
native = bool(platform_payload["native_validation_required"])

if route_source == "portable_fallback":
    tier = fallback_tier
    implementation_expected = intent != "reference-only"
    authority_required = tier != "L0"
    authority_ok = bool(style_authority_path) or not authority_required
    browser_required = platform == "web" and tier != "L0" and implementation_expected
    runtime_required = tier != "L0" and implementation_expected
    screenshot_required = (
        platform == "web"
        and implementation_expected
        and (
            tier == "L2"
            or has_reference
            or needs_reference
            or intent in {"redesign", "new-page", "brand", "mobile-flow", "high-motion"}
            or (visual and scope in {"section", "page", "multi-page"})
        )
    )
    route_payload = {
        "ok": authority_ok,
        "frontend_tier": tier,
        "design_tier": tier,
        "candidate_skills": ["design-craft"],
        "skills": ["design-craft"],
        "execution_mode": "main_serial",
        "subagent_required": False,
        "subagent_recommended": False,
        "style_authority_path": style_authority_path,
        "style_authority_source": "explicit_or_discovered" if style_authority_path else "none",
        "style_authority_mode": "evolve" if design_authority_mode == "evolve" else "enforce",
        "preflight_status": "pass" if authority_ok else "fail",
        "preflight_code": "OK" if authority_ok else "STYLE_AUTHORITY_MISSING",
        "gate_decision": "allow" if authority_ok else "deny",
        "browser_validation_required": browser_required,
        "preferred_browser_tool": "tmwd_browser",
        "browser_screenshot_required": screenshot_required,
        "screenshot_evidence_level": "required" if screenshot_required else "none",
        "screenshot_required_reason": (
            "portable fallback visual-risk policy" if screenshot_required else "not required by portable fallback"
        ),
        "preferred_screenshot_tool": "tmwd_browser.browser_screenshot_ops",
        "directory_governance_required": tier != "L0",
        "performance_review_required": tier in {"L1-V", "L2"},
        "quality_tradeoff": "Global Codex route planner unavailable; conservative portable fallback used.",
        "inputs": {
            "surface": surface,
            "intent": intent,
            "scope": scope,
            "style": style,
            "existing_project": existing_project,
        },
    }

tier = route_payload.get("frontend_tier") or fallback_tier
runtime_required = intent != "reference-only" and tier != "L0"
route_payload.update(
    {
        "design_tier": tier,
        "frontend_tier": tier,
        "route_source": route_source,
        "degraded": route_source == "portable_fallback" or bool(route_payload.get("degraded", False)),
        "platform": platform,
        "platform_source": platform_payload["platform_source"],
        "platform_confidence": platform_payload["platform_confidence"],
        "platform_signals": platform_payload.get("signals", []),
        "platform_contradictions": platform_payload.get("contradictions", []),
        "product_context_path": platform_payload.get("product_context_path", ""),
        "runtime_validation_required": runtime_required,
        "runtime_validation_kind": platform_payload["runtime_validation_kind"],
        "native_validation_required": native and runtime_required,
        "preferred_runtime_tool": platform_payload["preferred_runtime_tool"],
    }
)
route_payload.setdefault("inputs", {})
route_payload["inputs"].update(
    {
        "platform": platform,
        "requested_platform": platform_payload.get("platform") if platform_payload.get("platform_source") == "explicit" else "auto",
        "product_context_path": platform_payload.get("product_context_path", ""),
    }
)

developer_product_surfaces = {"auto", "dashboard", "app", "admin", "data-app"}
non_seed_intents = {"brand", "high-motion", "mobile-flow", "reference-only"}
has_style_authority = bool(route_payload.get("style_authority_path"))
vercel_geist_seed_applicable = (
    platform == "web"
    and not has_style_authority
    and surface in developer_product_surfaces
    and intent not in non_seed_intents
)
if vercel_geist_seed_applicable:
    vercel_geist_seed_reason = (
        "existing developer-product surface has no resolved style authority; "
        "use the Geist seed only if runtime/project style is weak"
        if existing_project
        else "new developer-product surface has no resolved style authority"
    )
elif platform != "web":
    vercel_geist_seed_reason = "native/adaptive platforms require platform-specific design authority"
elif has_style_authority:
    vercel_geist_seed_reason = "stronger style authority was resolved"
elif surface not in developer_product_surfaces:
    vercel_geist_seed_reason = "surface is not a default developer-product seed case"
else:
    vercel_geist_seed_reason = "intent calls for another style authority path"
route_payload.update(
    {
        "vercel_geist_seed_applicable": vercel_geist_seed_applicable,
        "vercel_geist_seed_reason": vercel_geist_seed_reason,
    }
)

if json_only:
    print(json.dumps(route_payload, ensure_ascii=False, indent=2, sort_keys=True))
else:
    print("design-craft route summary:")
    for key in [
        "ok",
        "frontend_tier",
        "design_tier",
        "platform",
        "platform_source",
        "platform_confidence",
        "product_context_path",
        "route_source",
        "degraded",
        "candidate_skills",
        "execution_mode",
        "subagent_required",
        "style_authority_path",
        "preflight_status",
        "preflight_code",
        "runtime_validation_required",
        "runtime_validation_kind",
        "native_validation_required",
        "preferred_runtime_tool",
        "browser_validation_required",
        "browser_screenshot_required",
        "vercel_geist_seed_applicable",
        "vercel_geist_seed_reason",
    ]:
        print(f"- {key}: {route_payload.get(key)}")

    refs = {"references/validation-contract.md", "references/product-context.md"}
    if platform == "ios":
        refs.add("references/ios-quality.md")
    elif platform == "android":
        refs.add("references/android-quality.md")
    elif platform == "adaptive":
        refs.update(
            {
                "references/ios-quality.md",
                "references/android-quality.md",
                "references/adaptive-quality.md",
            }
        )
    if intent == "high-motion" or platform != "web":
        refs.add("references/interaction-physics.md")
    if vercel_geist_seed_applicable:
        refs.update(
            {
                "templates/vercel-geist/design.md",
                "templates/vercel-geist/design.dark.md",
            }
        )
    print("- recommended_design_craft_references:")
    for ref in sorted(refs):
        print(f"  - {ref}")
    print("\nraw_json:")
    print(json.dumps(route_payload, ensure_ascii=False, indent=2, sort_keys=True))

if route_source == "portable_fallback":
    raise SystemExit(0 if route_payload.get("ok") else 2)
raise SystemExit(0 if planner_status == 0 else 2)
PY
status=$?
set -e
exit "${status}"
