from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from tools.design_craft.repo import REPO_ROOT


SCRIPT_PATH = (
    REPO_ROOT / "skills/design-craft/scripts/design_craft_route_runtime.py"
)
SPEC = importlib.util.spec_from_file_location("design_craft_route_runtime", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
route_runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(route_runtime)


def platform_payload(platform: str = "web") -> dict[str, object]:
    native = platform != "web"
    return {
        "platform": platform,
        "platform_source": "explicit",
        "platform_confidence": 1.0,
        "signals": [],
        "contradictions": [],
        "product_context_path": "",
        "runtime_validation_kind": "browser" if not native else "native",
        "native_validation_required": native,
        "preferred_runtime_tool": "tmwd_browser" if not native else "native-tool",
    }


class RouteRuntimeTests(unittest.TestCase):
    def test_fallback_tiers_cover_runtime_risk_levels(self) -> None:
        common = {
            "style": "auto",
            "design_authority_mode": "auto",
            "has_reference": False,
            "needs_reference": False,
        }
        self.assertEqual(
            route_runtime.fallback_tier(
                intent="functional", scope="micro", **common
            ),
            "L0",
        )
        self.assertEqual(
            route_runtime.fallback_tier(
                intent="functional", scope="component", **common
            ),
            "L1-F",
        )
        self.assertEqual(
            route_runtime.fallback_tier(
                intent="visual-refine", scope="component", **common
            ),
            "L1-V",
        )
        self.assertEqual(
            route_runtime.fallback_tier(
                intent="redesign", scope="page", **common
            ),
            "L2",
        )

    def test_portable_fallback_denies_missing_authority(self) -> None:
        payload = route_runtime.build_route_payload(
            route_payload={},
            platform_payload=platform_payload(),
            route_source="portable_fallback",
            surface="dashboard",
            intent="redesign",
            scope="page",
            style="auto",
            style_authority_path="",
            design_authority_mode="auto",
            existing_project=True,
            has_reference=False,
            needs_reference=False,
        )

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["frontend_tier"], "L2")
        self.assertEqual(payload["preflight_code"], "STYLE_AUTHORITY_MISSING")
        self.assertTrue(payload["browser_screenshot_required"])

    def test_global_payload_keeps_planner_decisions_and_normalizes_inputs(self) -> None:
        payload = route_runtime.build_route_payload(
            route_payload={
                "ok": True,
                "frontend_tier": "L1-V",
                "candidate_skills": ["design-craft"],
                "inputs": "invalid",
            },
            platform_payload=platform_payload(),
            route_source="codex_global",
            surface="dashboard",
            intent="visual-refine",
            scope="component",
            style="auto",
            style_authority_path="",
            design_authority_mode="auto",
            existing_project=True,
            has_reference=False,
            needs_reference=False,
        )

        self.assertEqual(payload["frontend_tier"], "L1-V")
        self.assertEqual(payload["route_source"], "codex_global")
        self.assertFalse(payload["degraded"])
        self.assertEqual(payload["inputs"]["platform"], "web")

    def test_native_route_recommends_platform_references(self) -> None:
        references = route_runtime.recommended_references(
            platform="adaptive",
            intent="visual-refine",
            developer_product_seed_applicable=False,
        )

        self.assertIn("references/ios-quality.md", references)
        self.assertIn("references/android-quality.md", references)
        self.assertIn("references/adaptive-quality.md", references)
        self.assertIn("references/interaction-physics.md", references)

    def test_route_loader_rejects_non_object_json(self) -> None:
        with tempfile.TemporaryDirectory(prefix="design-craft-route-runtime-") as raw:
            path = Path(raw) / "route.json"
            path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")

            self.assertEqual(route_runtime.load_route_payload(path), {})


if __name__ == "__main__":
    unittest.main()
