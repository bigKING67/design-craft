from __future__ import annotations

import unittest

from tools.design_craft.validation.maturity.profiles import (
    check_profile_invariants,
    load_profile,
)


class MaturityProfileTests(unittest.TestCase):
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
