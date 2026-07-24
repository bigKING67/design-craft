from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from design_craft_github_governance import (  # noqa: E402
    RELEASE_CREDENTIAL_ENV,
    GovernanceApiError,
    _api_failure,
    governance_environment,
    preflight,
)


class GitHubGovernanceCredentialTests(unittest.TestCase):
    def test_release_preflight_fails_closed_without_credential(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(GovernanceApiError) as raised:
                governance_environment(required=True)
        self.assertEqual(raised.exception.code, "credential_missing")
        self.assertEqual(raised.exception.endpoint, RELEASE_CREDENTIAL_ENV)

    def test_release_credential_is_forwarded_only_as_gh_token(self) -> None:
        with patch.dict(os.environ, {RELEASE_CREDENTIAL_ENV: "fixture-secret"}, clear=True):
            environment = governance_environment(required=True)
        assert environment is not None
        self.assertEqual(environment["GH_TOKEN"], "fixture-secret")
        self.assertNotIn(RELEASE_CREDENTIAL_ENV, environment)

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

    def test_preflight_reads_all_administration_endpoints(self) -> None:
        with patch(
            "design_craft_github_governance.fetch_rulesets",
            return_value=[],
        ) as rulesets, patch(
            "design_craft_github_governance.api_object",
            side_effect=(
                {"allowed_actions": "selected"},
                {"patterns_allowed": []},
            ),
        ) as api:
            payload = preflight("example/design-craft", environment={"GH_TOKEN": "x"})
        self.assertTrue(payload["ok"])
        rulesets.assert_called_once()
        self.assertEqual(api.call_count, 2)


if __name__ == "__main__":
    unittest.main()
