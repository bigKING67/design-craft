from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.design_craft.benchmark.contract import (
    ABSOLUTE_REGRESSION_LIMIT_MS,
    CACHE_CAPACITY,
    MIN_FULL_SAMPLES,
    RELATIVE_REGRESSION_LIMIT,
    SCHEMA,
    SMOKE_METRIC_NAMES,
    compare_results,
    result_errors,
)
from tools.design_craft.benchmark.fixtures import (
    _BoundedDigestCache,
    _validate_changed_files,
)
from tools.design_craft.benchmark.runner import _measure_cache, _percentile


def metric(p95: float) -> dict[str, object]:
    return {
        "unit": "ms",
        "iterations": 1,
        "p50": p95,
        "p95": p95,
        "max": p95,
        "samples": [p95],
    }


def metrics(p95: float) -> dict[str, dict[str, object]]:
    values = {name: metric(p95) for name in SMOKE_METRIC_NAMES}
    for count in (1, 10, 100):
        values[f"incremental_validation_{count}"].update(
            {
                "changed_files": count,
                "validation_scope": "explicit_changed_files",
                "fixture_root": "temporary_directory",
            }
        )
    values["validation_cache_cold"].update(
        {
            "cache_capacity": CACHE_CAPACITY,
            "working_set": CACHE_CAPACITY,
            "cache_hits": 0,
            "cache_misses": CACHE_CAPACITY,
            "cache_evictions": 0,
            "max_entries_observed": CACHE_CAPACITY,
            "warm": False,
        }
    )
    values["validation_cache_warm"].update(
        {
            "cache_capacity": CACHE_CAPACITY,
            "working_set": CACHE_CAPACITY,
            "cache_hits": CACHE_CAPACITY,
            "cache_misses": 0,
            "cache_evictions": 0,
            "max_entries_observed": CACHE_CAPACITY,
            "warm": True,
        }
    )
    values["validation_cache_overflow"].update(
        {
            "cache_capacity": CACHE_CAPACITY,
            "working_set": CACHE_CAPACITY * 2,
            "cache_hits": 0,
            "cache_misses": CACHE_CAPACITY * 2,
            "cache_evictions": CACHE_CAPACITY,
            "max_entries_observed": CACHE_CAPACITY,
            "warm": False,
        }
    )
    values["install_rollback"].update(
        {
            "failure_point": "after_switch",
            "expected_exit_code": 1,
            "rollback_verified": True,
            "install_root": "temporary_directory",
        }
    )
    values["installer_lock_contention"].update(
        {
            "lock_timeout_seconds": 0,
            "contention_observed": True,
            "real_install_touched": False,
            "install_root": "temporary_directory",
        }
    )
    values["release_bundle_build"].update(
        {
            "bundle_kind": "operational_npm_package",
            "artifact_bytes": 1024,
            "deterministic": True,
            "output_root": "temporary_directory",
        }
    )
    return values


def result(
    p95: float,
    *,
    runner: str = "fixture",
    scale: str = "smoke",
) -> dict[str, object]:
    return {
        "schema": SCHEMA,
        "scale": scale,
        "runner_id": runner,
        "source_commit": "a" * 40,
        "source_dirty": False,
        "python": "3.13.5",
        "platform": "fixture-platform",
        "policy": {
            "relative_regression_limit": RELATIVE_REGRESSION_LIMIT,
            "absolute_regression_limit_ms": ABSOLUTE_REGRESSION_LIMIT_MS,
        },
        "metrics": metrics(p95),
    }


def full_result(p95: float) -> dict[str, object]:
    payload = result(p95, scale="full")
    payload["metrics"]["tree_scan_100000"] = metric(p95)
    for value in payload["metrics"].values():
        value["iterations"] = MIN_FULL_SAMPLES
        value["samples"] = [p95] * MIN_FULL_SAMPLES
    return payload


class BenchmarkPolicyTests(unittest.TestCase):
    def test_full_results_require_enough_samples_for_p95(self) -> None:
        payload = full_result(100.0)
        self.assertEqual(result_errors(payload, label="current"), [])

        payload["metrics"]["route_pack"]["iterations"] = MIN_FULL_SAMPLES - 1
        payload["metrics"]["route_pack"]["samples"] = [100.0] * (
            MIN_FULL_SAMPLES - 1
        )
        errors = result_errors(payload, label="current")
        self.assertTrue(any("at least 20 samples" in error for error in errors))

    def test_full_sample_p95_is_not_a_single_maximum(self) -> None:
        samples = [100.0] * (MIN_FULL_SAMPLES - 1) + [1000.0]
        self.assertEqual(_percentile(samples, 0.95), 100.0)

    def test_small_absolute_variance_does_not_fail(self) -> None:
        comparison = compare_results(result(10.0), result(20.0))
        self.assertTrue(comparison["ok"])

    def test_relative_and_absolute_regression_fails(self) -> None:
        comparison = compare_results(result(100.0), result(170.0))
        self.assertFalse(comparison["ok"])
        self.assertTrue(any(item["regressed"] for item in comparison["comparisons"]))

    def test_different_runner_fails_closed(self) -> None:
        comparison = compare_results(result(100.0), result(100.0, runner="other"))
        self.assertFalse(comparison["ok"])

    def test_missing_schema_fails_closed(self) -> None:
        baseline = result(100.0)
        del baseline["schema"]
        comparison = compare_results(baseline, result(100.0))
        self.assertFalse(comparison["ok"])
        self.assertTrue(any("schema" in error for error in comparison["errors"]))

    def test_metric_set_drift_fails_closed(self) -> None:
        baseline = result(100.0)
        del baseline["metrics"]["incremental_validation_100"]
        comparison = compare_results(baseline, result(100.0))
        self.assertFalse(comparison["ok"])
        self.assertTrue(any("metric set" in error for error in comparison["errors"]))

    def test_non_finite_metric_fails_closed(self) -> None:
        baseline = result(100.0)
        baseline["metrics"]["route_selection"]["p95"] = float("nan")
        comparison = compare_results(baseline, result(100.0))
        self.assertFalse(comparison["ok"])
        self.assertTrue(any("finite" in error for error in comparison["errors"]))

    def test_sample_count_mismatch_fails_closed(self) -> None:
        baseline = result(100.0)
        baseline["metrics"]["route_selection"]["iterations"] = 2
        comparison = compare_results(baseline, result(100.0))
        self.assertFalse(comparison["ok"])
        self.assertTrue(any("sample count" in error for error in comparison["errors"]))

    def test_baseline_and_current_sample_counts_must_match(self) -> None:
        current = result(100.0)
        current["metrics"]["route_selection"]["iterations"] = 2
        current["metrics"]["route_selection"]["samples"] = [100.0, 100.0]
        comparison = compare_results(result(100.0), current)
        self.assertFalse(comparison["ok"])
        self.assertTrue(any("between baseline and current" in error for error in comparison["errors"]))

    def test_cache_capacity_violation_fails_closed(self) -> None:
        baseline = result(100.0)
        baseline["metrics"]["validation_cache_warm"]["max_entries_observed"] = (
            CACHE_CAPACITY + 1
        )
        comparison = compare_results(baseline, result(100.0))
        self.assertFalse(comparison["ok"])
        self.assertTrue(any("cache capacity" in error for error in comparison["errors"]))

    def test_release_bundle_contract_fails_closed(self) -> None:
        baseline = result(100.0)
        baseline["metrics"]["release_bundle_build"]["deterministic"] = False
        comparison = compare_results(baseline, result(100.0))
        self.assertFalse(comparison["ok"])
        self.assertTrue(any("release_bundle_build" in error for error in comparison["errors"]))


class IncrementalAndCacheTests(unittest.TestCase):
    def test_incremental_validation_rejects_invalid_python(self) -> None:
        with tempfile.TemporaryDirectory(prefix="design-craft-benchmark-test-") as raw:
            root = Path(raw)
            invalid = root / "invalid.py"
            invalid.write_text("def broken(:\n", encoding="utf-8")
            with self.assertRaises(SyntaxError):
                _validate_changed_files(root, [invalid])

    def test_incremental_validation_rejects_duplicate_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="design-craft-benchmark-test-") as raw:
            root = Path(raw)
            path = root / "valid.json"
            path.write_text('{"ok": true}\n', encoding="utf-8")
            with self.assertRaises(ValueError):
                _validate_changed_files(root, [path, path])

    def test_bounded_cache_records_hits_misses_and_invalidation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="design-craft-benchmark-test-") as raw:
            root = Path(raw)
            paths = []
            for index in range(3):
                path = root / f"fixture-{index}.txt"
                path.write_text(f"value {index}\n", encoding="utf-8")
                paths.append(path)
            cache = _BoundedDigestCache(root, capacity=2)
            first = cache.digest(paths[0])
            self.assertEqual(cache.misses, 1)
            self.assertEqual(cache.digest(paths[0]), first)
            self.assertEqual(cache.hits, 1)
            paths[0].write_text("changed value with a different size\n", encoding="utf-8")
            self.assertNotEqual(cache.digest(paths[0]), first)
            self.assertEqual(cache.misses, 2)
            cache.digest(paths[1])
            cache.digest(paths[2])
            self.assertEqual(cache.entries, 2)
            self.assertLessEqual(cache.max_entries_observed, cache.capacity)
            self.assertGreater(cache.evictions, 0)

    def test_warm_metric_excludes_cache_population_from_counters(self) -> None:
        with tempfile.TemporaryDirectory(prefix="design-craft-benchmark-test-") as raw:
            root = Path(raw)
            paths = []
            for index in range(3):
                path = root / f"fixture-{index}.txt"
                path.write_text(f"value {index}\n", encoding="utf-8")
                paths.append(path)

            cold = _measure_cache(root, paths, capacity=3, iterations=2, warm=False)
            warm = _measure_cache(root, paths, capacity=3, iterations=2, warm=True)

            self.assertEqual(cold["cache_hits"], 0)
            self.assertEqual(cold["cache_misses"], 6)
            self.assertEqual(warm["cache_hits"], 6)
            self.assertEqual(warm["cache_misses"], 0)


if __name__ == "__main__":
    unittest.main()
