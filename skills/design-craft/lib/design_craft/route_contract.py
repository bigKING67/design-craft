"""Pure route policy and rendering for the portable design-craft runtime."""

from __future__ import annotations

import json
from pathlib import Path


VISUAL_INTENTS = frozenset(
    {
        "visual-refine",
        "redesign",
        "new-page",
        "high-motion",
        "brand",
        "mobile-flow",
        "reference-only",
    }
)
LARGE_SCOPE_INTENTS = frozenset(
    {"redesign", "new-page", "brand", "mobile-flow", "high-motion"}
)
DEVELOPER_PRODUCT_SURFACES = frozenset(
    {"auto", "dashboard", "app", "admin", "data-app"}
)
NON_SEED_INTENTS = frozenset(
    {"brand", "high-motion", "mobile-flow", "reference-only"}
)


def load_route_payload(path: Path) -> dict[str, object]:
    try:
        return parse_route_payload(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}


def parse_route_payload(raw: str) -> dict[str, object]:
    payload = json.loads(raw)
    return payload if isinstance(payload, dict) else {}


def fallback_tier(
    *,
    intent: str,
    scope: str,
    style: str,
    design_authority_mode: str,
    has_reference: bool,
    needs_reference: bool,
) -> str:
    visual = intent in VISUAL_INTENTS or has_reference or needs_reference
    large_scope = scope in {"page", "multi-page"} or intent in LARGE_SCOPE_INTENTS
    micro_visual_safe = (
        scope == "micro"
        and intent in {"auto", "functional", "visual-refine"}
        and not has_reference
        and not needs_reference
        and style in {"auto", "none"}
        and design_authority_mode != "evolve"
    )
    if micro_visual_safe:
        return "L0"
    if not visual and intent in {"auto", "functional"}:
        return "L1-F"
    if large_scope:
        return "L2"
    return "L1-V"


def portable_fallback_payload(
    *,
    tier: str,
    platform: str,
    surface: str,
    intent: str,
    scope: str,
    style: str,
    style_authority_path: str,
    design_authority_mode: str,
    existing_project: bool,
    has_reference: bool,
    needs_reference: bool,
) -> dict[str, object]:
    implementation_expected = intent != "reference-only"
    authority_required = tier != "L0"
    authority_ok = bool(style_authority_path) or not authority_required
    visual = intent in VISUAL_INTENTS or has_reference or needs_reference
    browser_required = platform == "web" and tier != "L0" and implementation_expected
    screenshot_required = (
        platform == "web"
        and implementation_expected
        and (
            tier == "L2"
            or has_reference
            or needs_reference
            or intent in LARGE_SCOPE_INTENTS
            or (visual and scope in {"section", "page", "multi-page"})
        )
    )
    return {
        "ok": authority_ok,
        "frontend_tier": tier,
        "design_tier": tier,
        "candidate_skills": ["design-craft"],
        "skills": ["design-craft"],
        "execution_mode": "main_serial",
        "subagent_required": False,
        "subagent_recommended": False,
        "style_authority_path": style_authority_path,
        "style_authority_source": (
            "explicit_or_discovered" if style_authority_path else "none"
        ),
        "style_authority_mode": (
            "evolve" if design_authority_mode == "evolve" else "enforce"
        ),
        "preflight_status": "pass" if authority_ok else "fail",
        "preflight_code": "OK" if authority_ok else "STYLE_AUTHORITY_MISSING",
        "gate_decision": "allow" if authority_ok else "deny",
        "browser_validation_required": browser_required,
        "preferred_browser_tool": "tmwd_browser",
        "browser_screenshot_required": screenshot_required,
        "screenshot_evidence_level": "required" if screenshot_required else "none",
        "screenshot_required_reason": (
            "portable fallback visual-risk policy"
            if screenshot_required
            else "not required by portable fallback"
        ),
        "preferred_screenshot_tool": "tmwd_browser.browser_screenshot_ops",
        "directory_governance_required": tier != "L0",
        "performance_review_required": tier in {"L1-V", "L2"},
        "quality_tradeoff": (
            "Global Codex route planner unavailable; conservative portable fallback used."
        ),
        "inputs": {
            "surface": surface,
            "intent": intent,
            "scope": scope,
            "style": style,
            "existing_project": existing_project,
        },
    }


def seed_applicability(
    *,
    route_payload: dict[str, object],
    platform: str,
    surface: str,
    intent: str,
    existing_project: bool,
) -> tuple[bool, str]:
    has_style_authority = bool(route_payload.get("style_authority_path"))
    applicable = (
        platform == "web"
        and not has_style_authority
        and surface in DEVELOPER_PRODUCT_SURFACES
        and intent not in NON_SEED_INTENTS
    )
    if applicable:
        reason = (
            "existing developer-product surface has no resolved style authority; "
            "use the original developer-product seed only if runtime/project style is weak"
            if existing_project
            else "new developer-product surface has no resolved style authority"
        )
    elif platform != "web":
        reason = "native/adaptive platforms require platform-specific design authority"
    elif has_style_authority:
        reason = "stronger style authority was resolved"
    elif surface not in DEVELOPER_PRODUCT_SURFACES:
        reason = "surface is not a default developer-product seed case"
    else:
        reason = "intent calls for another style authority path"
    return applicable, reason


def build_route_payload(
    *,
    route_payload: dict[str, object],
    platform_payload: dict[str, object],
    route_source: str,
    surface: str,
    intent: str,
    scope: str,
    style: str,
    style_authority_path: str,
    design_authority_mode: str,
    existing_project: bool,
    has_reference: bool,
    needs_reference: bool,
) -> dict[str, object]:
    resolved_fallback_tier = fallback_tier(
        intent=intent,
        scope=scope,
        style=style,
        design_authority_mode=design_authority_mode,
        has_reference=has_reference,
        needs_reference=needs_reference,
    )
    platform = str(platform_payload["platform"])
    native = bool(platform_payload["native_validation_required"])

    if route_source == "portable_fallback":
        route_payload = portable_fallback_payload(
            tier=resolved_fallback_tier,
            platform=platform,
            surface=surface,
            intent=intent,
            scope=scope,
            style=style,
            style_authority_path=style_authority_path,
            design_authority_mode=design_authority_mode,
            existing_project=existing_project,
            has_reference=has_reference,
            needs_reference=needs_reference,
        )

    tier = route_payload.get("frontend_tier") or resolved_fallback_tier
    runtime_required = intent != "reference-only" and tier != "L0"
    route_payload.update(
        {
            "design_tier": tier,
            "frontend_tier": tier,
            "route_source": route_source,
            "degraded": route_source == "portable_fallback"
            or bool(route_payload.get("degraded", False)),
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
    inputs = route_payload.setdefault("inputs", {})
    if not isinstance(inputs, dict):
        inputs = {}
        route_payload["inputs"] = inputs
    inputs.update(
        {
            "platform": platform,
            "requested_platform": (
                platform_payload.get("platform")
                if platform_payload.get("platform_source") == "explicit"
                else "auto"
            ),
            "product_context_path": platform_payload.get("product_context_path", ""),
        }
    )

    seed_applicable, seed_reason = seed_applicability(
        route_payload=route_payload,
        platform=platform,
        surface=surface,
        intent=intent,
        existing_project=existing_project,
    )
    route_payload.update(
        {
            "developer_product_seed_applicable": seed_applicable,
            "developer_product_seed_reason": seed_reason,
            # Compatibility fields for existing route consumers.
            "vercel_geist_seed_applicable": seed_applicable,
            "vercel_geist_seed_reason": seed_reason,
        }
    )
    return route_payload


def recommended_references(
    *, platform: str, intent: str, developer_product_seed_applicable: bool
) -> list[str]:
    references = {"references/validation-contract.md", "references/product-context.md"}
    if platform == "ios":
        references.add("references/ios-quality.md")
    elif platform == "android":
        references.add("references/android-quality.md")
    elif platform == "adaptive":
        references.update(
            {
                "references/ios-quality.md",
                "references/android-quality.md",
                "references/adaptive-quality.md",
            }
        )
    if intent == "high-motion" or platform != "web":
        references.add("references/interaction-physics.md")
    if developer_product_seed_applicable:
        references.update(
            {
                "templates/developer-product/design.md",
                "templates/developer-product/design.dark.md",
            }
        )
    return sorted(references)


def print_route_payload(
    route_payload: dict[str, object], *, intent: str, json_only: bool
) -> None:
    if json_only:
        print(json.dumps(route_payload, ensure_ascii=False, indent=2, sort_keys=True))
        return

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
        "developer_product_seed_applicable",
        "developer_product_seed_reason",
    ]:
        print(f"- {key}: {route_payload.get(key)}")
    print("- recommended_design_craft_references:")
    for reference in recommended_references(
        platform=str(route_payload["platform"]),
        intent=intent,
        developer_product_seed_applicable=bool(
            route_payload["developer_product_seed_applicable"]
        ),
    ):
        print(f"  - {reference}")
    print("\nraw_json:")
    print(json.dumps(route_payload, ensure_ascii=False, indent=2, sort_keys=True))
