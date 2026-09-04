from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from tools.design_craft.routing.semantic_audit import _semantic_validation
from tools.design_craft.routing.semantic_contract import REQUIRED_FRAGMENTS, semantic_paths
from tools.design_craft.routing.semantic_runtime import (
    RuntimeValidation,
    _validate_route_probes,
    route_probe_requests,
)


class SemanticAuditTests(unittest.TestCase):
    def test_static_work_runs_before_waiting_for_runtime_results(self) -> None:
        events: list[str] = []
        batch = object()

        def submit(*_args: object, **_kwargs: object) -> object:
            events.append("submit")
            return batch

        def static(*_args: object, **_kwargs: object) -> list[str]:
            events.append("static")
            return ["static issue"]

        def schema(observed: object) -> list[str]:
            self.assertIs(observed, batch)
            events.append("schema")
            return ["schema issue"]

        def runtime(*_args: object, **_kwargs: object) -> RuntimeValidation:
            events.append("runtime")
            return RuntimeValidation(
                issues=["runtime issue"],
                warnings=[],
                probes=[],
                profiles=[],
                model_catalog_source="not-run",
            )

        with (
            patch(
                "tools.design_craft.routing.semantic_audit.submit_runtime_probe_batch",
                side_effect=submit,
            ),
            patch(
                "tools.design_craft.routing.semantic_audit.static_validation",
                side_effect=static,
            ),
            patch(
                "tools.design_craft.routing.semantic_audit.validate_schema_probe",
                side_effect=schema,
            ),
            patch(
                "tools.design_craft.routing.semantic_audit.runtime_validation",
                side_effect=runtime,
            ),
        ):
            result = _semantic_validation(Path("/route-pack"), object())

        self.assertEqual(events, ["submit", "static", "schema", "runtime"])
        self.assertEqual(
            result["issues"],
            ["schema issue", "static issue", "runtime issue"],
        )
        self.assertEqual(result["status"], "error")

    def test_route_module_inventory_preserves_stable_order(self) -> None:
        names = [path.name for path in semantic_paths(Path("/pack")).route_files]

        self.assertEqual(names[0], "frontend_route_plan.sh")
        self.assertEqual(names[-1], "frontend_worker_payload_core.py")
        self.assertIn("frontend_route_evidence.py", names)
        self.assertIn("frontend_route_visual_review.py", names)
        self.assertEqual(len(names), 19)
        self.assertEqual(len(names), len(set(names)))

    def test_browser_lifecycle_static_contract_requires_v2_schemas(self) -> None:
        fragments = REQUIRED_FRAGMENTS["frontend_route_browser_contract.py"]

        self.assertIn(
            'RECEIPT_SCHEMA = "frontend-route.browser-lifecycle-receipt.v2"',
            fragments,
        )
        self.assertIn(
            'OBSERVATIONS_SCHEMA = "frontend-route.browser-lifecycle-observations.v2"',
            fragments,
        )
        self.assertFalse(
            any("browser-lifecycle-receipt.v1" in item for item in fragments)
        )
        self.assertFalse(
            any("browser-lifecycle-observations.v1" in item for item in fragments)
        )

    def test_runtime_probe_contract_keeps_six_bounded_routes(self) -> None:
        requests = route_probe_requests()

        self.assertEqual(len(requests), 6)
        self.assertEqual(requests[0][0][-1], "external")
        self.assertEqual(requests[3][0][-2:], ["--browser-context", "local"])
        self.assertEqual(requests[4][2], "ultra")
        self.assertIn("comp-fidelity", requests[5][0])

    def test_local_and_compact_route_probes_require_browser67_lifecycle(self) -> None:
        browser_lifecycle = {"applicable": True, "managed_runtime": "browser67"}

        def browser_payload() -> dict:
            return {
                "preferred_browser_tool": "tmwd_browser",
                "preferred_runtime_tool": "tmwd_browser",
                "planned_browser_lifecycle": browser_lifecycle,
                "browser_lifecycle": browser_lifecycle,
                "actual_browser_lifecycle_state": {
                    "state": "not_started",
                    "finalize_result": "not_started",
                    "delivery_summary_observed": False,
                },
                "style_authority_applicability": "not_applicable",
                "visual_contract_required": False,
            }

        compact = {
            "schema": "frontend-route.compact.v1",
            "route": {"frontend_tier": "L1-F"},
            "runtime_profile": {"verified": True},
            "validation": {"preflight_code": "OK"},
            "planned_browser_lifecycle": browser_lifecycle,
            "browser_lifecycle": browser_lifecycle,
            "actual_browser_lifecycle_state": {
                "state": "not_started",
                "finalize_result": "not_started",
            },
        }
        results = [
            (0, browser_payload(), ""),
            (0, browser_payload(), ""),
            (
                0,
                {
                    "runtime_profile_source": "environment",
                    "runtime_profile_verified": True,
                    "effective_model": "gpt-5.6-sol",
                    "effective_reasoning": "max",
                    "reasoning_application_status": "runtime_verified",
                    "runtime_profile_evidence": {
                        "kind": "explicit_environment",
                        "contains_prompt_data": False,
                    },
                },
                "",
            ),
            (0, compact, ""),
            (
                2,
                {
                    "route_status": "error",
                    "route_error_code": "RUNTIME_PROFILE_CONFLICT",
                    "gate_decision": "deny",
                    "runtime_profile_verified": True,
                    "runtime_remediation_policy": (
                        "downgrade_to_max_or_authorize_delegation"
                    ),
                },
                "",
            ),
            (
                0,
                {
                    "evidence_mode": "comp-fidelity",
                    "runtime_validation_required": False,
                    "browser_validation_required": False,
                    "browser_screenshot_required": False,
                    "visual_contract_required": False,
                    "visual_review_required": False,
                    "candidate_skills": ["design-craft"],
                    "evidence_contract": {
                        "delivery_state": "measurement_only",
                        "measurement_is_visual_acceptance": False,
                        "global_pixel_pass_threshold": None,
                    },
                },
                "",
            ),
        ]

        probes, issues = _validate_route_probes(results)

        self.assertEqual(issues, [])
        self.assertTrue(all(probe["ok"] for probe in probes))

        legacy_local = browser_payload()
        legacy_local["preferred_browser_tool"] = "in_app_browser"
        legacy_local["preferred_runtime_tool"] = "in_app_browser"
        legacy_local["actual_browser_lifecycle_state"] = {
            "state": "not_applicable",
            "finalize_result": "not_applicable",
            "delivery_summary_observed": False,
        }
        results[1] = (0, legacy_local, "")

        probes, issues = _validate_route_probes(results)

        local_probe = next(
            probe for probe in probes if probe["name"] == "browser_context_local"
        )
        self.assertFalse(local_probe["ok"])
        self.assertTrue(
            any("expected browser/runtime tool tmwd_browser" in issue for issue in issues)
        )


if __name__ == "__main__":
    unittest.main()
