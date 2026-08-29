from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from tools.design_craft.routing.semantic_audit import _semantic_validation
from tools.design_craft.routing.semantic_contract import REQUIRED_FRAGMENTS, semantic_paths
from tools.design_craft.routing.semantic_runtime import (
    RuntimeValidation,
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


if __name__ == "__main__":
    unittest.main()
