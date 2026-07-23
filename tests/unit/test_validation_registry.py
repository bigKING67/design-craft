from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.design_craft.validation.registry import load_registry, select_gates


class ValidationRegistryTests(unittest.TestCase):
    def test_repository_registry_selects_portable_gates(self) -> None:
        gates = select_gates(load_registry(), "portable")
        self.assertEqual(
            [gate.gate_id for gate in gates],
            [
                "repository-contracts",
                "lint",
                "contract-tests",
                "development-maturity",
            ],
        )

    def test_duplicate_gate_ids_fail(self) -> None:
        payload = {
            "schema": "design-craft.validation-gates.v1",
            "gates": [
                {
                    "id": "duplicate",
                    "command": ["python3", "--version"],
                    "profiles": ["portable"],
                    "timeout_seconds": 10,
                    "execution": "parallel",
                },
                {
                    "id": "duplicate",
                    "command": ["python3", "--version"],
                    "profiles": ["portable"],
                    "timeout_seconds": 10,
                    "execution": "parallel",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "gates.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate validation gate id"):
                load_registry(path)

    def test_profile_cannot_omit_dependency(self) -> None:
        payload = {
            "schema": "design-craft.validation-gates.v1",
            "gates": [
                {
                    "id": "base",
                    "command": ["python3", "--version"],
                    "profiles": ["local"],
                    "timeout_seconds": 10,
                    "execution": "parallel",
                },
                {
                    "id": "dependent",
                    "command": ["python3", "--version"],
                    "profiles": ["portable", "local"],
                    "timeout_seconds": 10,
                    "execution": "serial",
                    "depends_on": ["base"],
                },
            ],
        }
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "gates.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "without dependencies"):
                select_gates(load_registry(path), "portable")


if __name__ == "__main__":
    unittest.main()
