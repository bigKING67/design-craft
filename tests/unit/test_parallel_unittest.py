from __future__ import annotations

import unittest
from unittest import mock

from scripts import design_craft_parallel_unittest as parallel_unittest


class ParallelUnittestTests(unittest.TestCase):
    def test_collect_test_ids_is_complete_and_sorted(self) -> None:
        test_ids = parallel_unittest.collect_test_ids(
            ["tests.contract.test_installer.InstallerContractTests"]
        )

        self.assertEqual(len(test_ids), 5)
        self.assertEqual(test_ids, sorted(test_ids))
        self.assertTrue(
            all(test_id.startswith("tests.contract.test_installer.") for test_id in test_ids)
        )

    def test_run_tests_preserves_input_order(self) -> None:
        def fake_run(test_id: str) -> parallel_unittest.TestResult:
            return parallel_unittest.TestResult(test_id, 0, "", "")

        with mock.patch.object(parallel_unittest, "run_test", side_effect=fake_run):
            results = parallel_unittest.run_tests(["test.z", "test.a"], jobs=2)

        self.assertEqual([result.test_id for result in results], ["test.z", "test.a"])

    def test_failure_result_remains_observable(self) -> None:
        expected = parallel_unittest.TestResult("test.failure", 1, "", "trace")
        with mock.patch.object(parallel_unittest, "run_test", return_value=expected):
            results = parallel_unittest.run_tests(["test.failure"], jobs=4)

        self.assertEqual(results, [expected])
