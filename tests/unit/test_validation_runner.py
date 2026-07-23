from __future__ import annotations

import sys
import unittest

from tools.design_craft.validation.model import GateSpec
from tools.design_craft.validation.runner import run_gates


def gate(gate_id: str, code: str, *, execution: str = "parallel", depends_on: tuple[str, ...] = ()) -> GateSpec:
    return GateSpec(
        gate_id=gate_id,
        command=(sys.executable, "-c", code),
        profiles=frozenset({"portable"}),
        timeout_seconds=5,
        execution=execution,
        depends_on=depends_on,
    )


class ValidationRunnerTests(unittest.TestCase):
    def test_nonzero_exit_is_observable(self) -> None:
        result = run_gates((gate("failure", "raise SystemExit(7)"),))[0]
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.exit_code, 7)
        self.assertEqual(result.error_code, "NONZERO_EXIT")

    def test_serial_dependency_failure_skips_gate(self) -> None:
        results = run_gates(
            (
                gate("failure", "raise SystemExit(1)"),
                gate(
                    "dependent",
                    "raise SystemExit('must not execute')",
                    execution="serial",
                    depends_on=("failure",),
                ),
            )
        )
        self.assertEqual(results[1].status, "skipped")
        self.assertEqual(results[1].error_code, "DEPENDENCY_FAILED")


if __name__ == "__main__":
    unittest.main()
