from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from design_craft_github_governance import (  # noqa: E402
    ACTIONS_PERMISSIONS,
    SELECTED_ACTIONS,
    _api_failure,
    desired_rulesets,
    validate_actions_permissions,
    validate_ruleset,
)


class GitHubGovernanceContractTests(unittest.TestCase):
    def test_administration_denial_has_machine_readable_classification(self) -> None:
        result = subprocess.CompletedProcess(
            ["gh", "api"],
            1,
            stdout="",
            stderr="HTTP 403: Resource not accessible by integration",
        )
        error = _api_failure(result, "repos/example/design-craft/actions/permissions")
        self.assertEqual(error.code, "insufficient_permissions")
        self.assertIn("actions/permissions", error.endpoint)

    def test_desired_rulesets_validate_without_bypass(self) -> None:
        for payload in desired_rulesets().values():
            self.assertEqual(validate_ruleset(payload, payload), [])

    def test_ruleset_bypass_is_rejected(self) -> None:
        expected = desired_rulesets()["design-craft-main"]
        observed = {**expected, "bypass_actors": [{"actor_type": "RepositoryRole"}]}
        errors = validate_ruleset(observed, expected)
        self.assertTrue(any("bypass_actors" in error for error in errors))

    def test_actions_permission_drift_is_rejected(self) -> None:
        observed = {**ACTIONS_PERMISSIONS, "sha_pinning_required": False}
        errors = validate_actions_permissions(observed, SELECTED_ACTIONS)
        self.assertTrue(any("sha_pinning_required" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
