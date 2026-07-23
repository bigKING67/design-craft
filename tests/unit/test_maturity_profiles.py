from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.design_craft.repo import REPO_ROOT
from tools.design_craft.validation.maturity.gates import performance_regression, route_pack
from tools.design_craft.validation.maturity.model import MaturityContext
from tools.design_craft.validation.maturity.profiles import (
    check_profile_invariants,
    load_profile,
)


class MaturityProfileTests(unittest.TestCase):
    def test_development_route_pack_is_portable(self) -> None:
        with tempfile.TemporaryDirectory(prefix="design-craft-missing-codex-") as raw:
            missing_codex_home = Path(raw) / "missing"
            with mock.patch.dict(
                os.environ,
                {"CODEX_HOME": str(missing_codex_home)},
                clear=False,
            ):
                result = route_pack(
                    MaturityContext(
                        root=REPO_ROOT,
                        profile="development",
                        phase="candidate",
                        baseline_path=None,
                    )
                )
        self.assertTrue(result.passed, result.error)
        self.assertEqual(result.evidence["fixture_scope"], "portable_self_check")

    def test_release_performance_rejects_smoke_baseline(self) -> None:
        with tempfile.TemporaryDirectory(prefix="design-craft-maturity-test-") as raw:
            baseline = Path(raw) / "baseline.json"
            baseline.write_text(json.dumps({"scale": "smoke"}), encoding="utf-8")
            result = performance_regression(
                MaturityContext(
                    root=Path(raw),
                    profile="operational_95",
                    phase="candidate",
                    baseline_path=baseline,
                )
            )
        self.assertFalse(result.passed)
        self.assertIn("full suite", result.error)

    def test_profile_invariants(self) -> None:
        self.assertEqual(check_profile_invariants(), [])

    def test_operational_is_not_a_missing_evidence_cap(self) -> None:
        profile = load_profile("operational_95", "candidate")
        self.assertIn("host_codex_current_source", profile.required_gate_ids)
        self.assertIn("host_pi_current_source", profile.required_gate_ids)
        self.assertIn("native_ios_simulator_current_source", profile.required_gate_ids)
        self.assertIn("native_android_emulator_current_source", profile.required_gate_ids)
        self.assertIn("performance_regression", profile.required_gate_ids)

    def test_final_phase_adds_live_main_governance(self) -> None:
        candidate = load_profile("operational_95", "candidate")
        final = load_profile("operational_95", "final")
        self.assertNotIn("main_ruleset", candidate.required_gate_ids)
        self.assertIn("main_branch", final.required_gate_ids)
        self.assertIn("main_ruleset", final.required_gate_ids)


if __name__ == "__main__":
    unittest.main()
