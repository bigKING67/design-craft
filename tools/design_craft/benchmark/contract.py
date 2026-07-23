from __future__ import annotations

import math
import re


SCHEMA = "design-craft.benchmark-result.v1"
COMPARISON_SCHEMA = "design-craft.benchmark-comparison.v1"
RELATIVE_REGRESSION_LIMIT = 0.15
ABSOLUTE_REGRESSION_LIMIT_MS = 50.0
MIN_FULL_SAMPLES = 20
INCREMENTAL_FILE_COUNTS = (1, 10, 100)
CACHE_CAPACITY = 32
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}")

SMOKE_METRIC_NAMES = frozenset(
    {
        "route_selection",
        "route_pack",
        "tree_scan_1000",
        "tree_scan_10000",
        "validation_registry",
        "lint_full",
        "evidence_validation",
        "package_validation",
        "incremental_validation_1",
        "incremental_validation_10",
        "incremental_validation_100",
        "validation_cache_cold",
        "validation_cache_warm",
        "validation_cache_overflow",
        "install_atomic",
        "install_rollback",
        "installer_lock_contention",
        "release_bundle_build",
    }
)
FULL_METRIC_NAMES = SMOKE_METRIC_NAMES | {"tree_scan_100000"}


def _is_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def metric_errors(name: str, metric: object) -> list[str]:
    if not isinstance(metric, dict):
        return [f"metric {name} must be an object"]
    errors: list[str] = []
    if metric.get("unit") != "ms":
        errors.append(f"metric {name} unit must be ms")
    iterations = metric.get("iterations")
    samples = metric.get("samples")
    if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations <= 0:
        errors.append(f"metric {name} iterations must be a positive integer")
    if not isinstance(samples, list) or not samples:
        errors.append(f"metric {name} samples must be a non-empty array")
        numeric_samples: list[float] = []
    else:
        numeric_samples = [
            float(value)
            for value in samples
            if _is_number(value) and float(value) >= 0
        ]
        if len(numeric_samples) != len(samples):
            errors.append(f"metric {name} samples must be finite non-negative numbers")
        if (
            isinstance(iterations, int)
            and not isinstance(iterations, bool)
            and len(samples) != iterations
        ):
            errors.append(f"metric {name} sample count must match iterations")
    timing_values: dict[str, float] = {}
    for field in ("p50", "p95", "max"):
        value = metric.get(field)
        if not _is_number(value) or float(value) < 0:
            errors.append(f"metric {name} {field} must be a finite non-negative number")
        else:
            timing_values[field] = float(value)
    if set(timing_values) == {"p50", "p95", "max"} and not (
        timing_values["p50"] <= timing_values["p95"] <= timing_values["max"]
    ):
        errors.append(f"metric {name} must satisfy p50 <= p95 <= max")
    if (
        numeric_samples
        and "max" in timing_values
        and abs(max(numeric_samples) - timing_values["max"]) > 0.001
    ):
        errors.append(f"metric {name} max must match its samples")
    return errors


def specialized_metric_errors(name: str, metric: object) -> list[str]:
    if not isinstance(metric, dict):
        return []
    errors: list[str] = []
    if name.startswith("incremental_validation_"):
        try:
            expected = int(name.rsplit("_", 1)[1])
        except ValueError:
            return [f"metric {name} has an invalid incremental file count"]
        if metric.get("changed_files") != expected:
            errors.append(f"metric {name} changed_files must be {expected}")
        if metric.get("validation_scope") != "explicit_changed_files":
            errors.append(f"metric {name} must declare explicit_changed_files scope")
        if metric.get("fixture_root") != "temporary_directory":
            errors.append(f"metric {name} must use a temporary fixture root")
    if name.startswith("validation_cache_"):
        integer_fields = (
            "cache_capacity",
            "working_set",
            "cache_hits",
            "cache_misses",
            "cache_evictions",
            "max_entries_observed",
        )
        for field in integer_fields:
            value = metric.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                errors.append(f"metric {name} {field} must be a non-negative integer")
        capacity = metric.get("cache_capacity")
        max_entries = metric.get("max_entries_observed")
        if (
            isinstance(capacity, int)
            and isinstance(max_entries, int)
            and max_entries > capacity
        ):
            errors.append(f"metric {name} exceeded its declared cache capacity")
        if name == "validation_cache_cold" and (
            metric.get("warm") is not False
            or metric.get("cache_hits") != 0
            or not isinstance(metric.get("cache_misses"), int)
            or metric["cache_misses"] <= 0
        ):
            errors.append("metric validation_cache_cold must record only cache misses")
        if name == "validation_cache_warm" and (
            metric.get("warm") is not True
            or not isinstance(metric.get("cache_hits"), int)
            or metric["cache_hits"] <= 0
            or metric.get("cache_misses") != 0
        ):
            errors.append("metric validation_cache_warm must record only cache hits")
        if name == "validation_cache_overflow" and (
            not isinstance(metric.get("cache_evictions"), int)
            or metric["cache_evictions"] <= 0
        ):
            errors.append("metric validation_cache_overflow must record bounded evictions")
    if name == "install_rollback" and (
        metric.get("failure_point") != "after_switch"
        or metric.get("expected_exit_code") != 1
        or metric.get("rollback_verified") is not True
        or metric.get("install_root") != "temporary_directory"
    ):
        errors.append("metric install_rollback must prove temporary after-switch restoration")
    if name == "installer_lock_contention" and (
        metric.get("lock_timeout_seconds") != 0
        or metric.get("contention_observed") is not True
        or metric.get("real_install_touched") is not False
        or metric.get("install_root") != "temporary_directory"
    ):
        errors.append("metric installer_lock_contention must fail closed in a temporary root")
    if name == "release_bundle_build" and (
        metric.get("bundle_kind") != "operational_npm_package"
        or not isinstance(metric.get("artifact_bytes"), int)
        or metric["artifact_bytes"] <= 0
        or metric.get("deterministic") is not True
        or metric.get("output_root") != "temporary_directory"
    ):
        errors.append("metric release_bundle_build must prove deterministic temporary output")
    return errors


def result_errors(payload: object, *, label: str) -> list[str]:
    if not isinstance(payload, dict):
        return [f"{label} benchmark result must be an object"]
    errors: list[str] = []
    if payload.get("schema") != SCHEMA:
        errors.append(f"{label} benchmark schema must be {SCHEMA}")
    scale = payload.get("scale")
    if scale not in {"smoke", "full"}:
        errors.append(f"{label} benchmark scale must be smoke or full")
    runner_id = payload.get("runner_id")
    if not isinstance(runner_id, str) or not runner_id.strip():
        errors.append(f"{label} runner_id must be a non-empty string")
    source_commit = payload.get("source_commit")
    if not isinstance(source_commit, str) or COMMIT_PATTERN.fullmatch(source_commit) is None:
        errors.append(f"{label} source_commit must be a full lowercase Git SHA")
    if not isinstance(payload.get("source_dirty"), bool):
        errors.append(f"{label} source_dirty must be boolean")
    for field in ("python", "platform"):
        if not isinstance(payload.get(field), str) or not str(payload[field]).strip():
            errors.append(f"{label} {field} must be a non-empty string")
    expected_policy = {
        "relative_regression_limit": RELATIVE_REGRESSION_LIMIT,
        "absolute_regression_limit_ms": ABSOLUTE_REGRESSION_LIMIT_MS,
    }
    if payload.get("policy") != expected_policy:
        errors.append(f"{label} benchmark policy does not match the comparison contract")
    metrics = payload.get("metrics")
    if not isinstance(metrics, dict):
        errors.append(f"{label} benchmark result must contain a metrics object")
        return errors
    expected_names = FULL_METRIC_NAMES if scale == "full" else SMOKE_METRIC_NAMES
    if set(metrics) != set(expected_names):
        errors.append(
            f"{label} metric set mismatch expected={sorted(expected_names)} "
            f"actual={sorted(metrics)}"
        )
    for name, metric in metrics.items():
        errors.extend(f"{label}: {error}" for error in metric_errors(str(name), metric))
        errors.extend(
            f"{label}: {error}"
            for error in specialized_metric_errors(str(name), metric)
        )
        if scale == "full" and isinstance(metric, dict):
            iterations = metric.get("iterations")
            if (
                isinstance(iterations, int)
                and not isinstance(iterations, bool)
                and iterations < MIN_FULL_SAMPLES
            ):
                errors.append(
                    f"{label}: full metric {name} must use at least "
                    f"{MIN_FULL_SAMPLES} samples"
                )
    return errors


def compare_results(
    baseline: dict[str, object], current: dict[str, object]
) -> dict[str, object]:
    errors = [
        *result_errors(baseline, label="baseline"),
        *result_errors(current, label="current"),
    ]
    comparisons: list[dict[str, object]] = []
    if not isinstance(baseline, dict) or not isinstance(current, dict):
        return {
            "schema": COMPARISON_SCHEMA,
            "ok": False,
            "errors": errors,
            "comparisons": comparisons,
        }
    for field in ("runner_id", "scale", "python", "platform", "policy"):
        if baseline.get(field) != current.get(field):
            errors.append(f"baseline {field} must match the current benchmark")
    baseline_metrics = baseline.get("metrics")
    current_metrics = current.get("metrics")
    if not isinstance(baseline_metrics, dict) or not isinstance(current_metrics, dict):
        return {
            "schema": COMPARISON_SCHEMA,
            "ok": False,
            "errors": errors,
            "comparisons": comparisons,
        }
    if set(baseline_metrics) != set(current_metrics):
        errors.append("baseline and current metric sets must match exactly")
    for name in sorted(set(baseline_metrics) & set(current_metrics)):
        baseline_metric = baseline_metrics[name]
        current_metric = current_metrics[name]
        if metric_errors(name, baseline_metric) or metric_errors(name, current_metric):
            continue
        assert isinstance(baseline_metric, dict)
        assert isinstance(current_metric, dict)
        baseline_p95 = float(baseline_metric["p95"])
        current_p95 = float(current_metric["p95"])
        absolute_delta = current_p95 - baseline_p95
        relative_delta = absolute_delta / max(baseline_p95, 0.001)
        regressed = (
            absolute_delta > ABSOLUTE_REGRESSION_LIMIT_MS
            and relative_delta > RELATIVE_REGRESSION_LIMIT
        )
        if regressed:
            errors.append(
                f"{name} regressed by {relative_delta:.1%} and {absolute_delta:.3f} ms"
            )
        comparisons.append(
            {
                "name": name,
                "baseline_p95_ms": baseline_p95,
                "current_p95_ms": current_p95,
                "absolute_delta_ms": round(absolute_delta, 3),
                "relative_delta": round(relative_delta, 6),
                "regressed": regressed,
            }
        )
    return {
        "schema": COMPARISON_SCHEMA,
        "baseline_commit": baseline.get("source_commit"),
        "current_commit": current.get("source_commit"),
        "runner_id": current.get("runner_id"),
        "ok": not errors,
        "errors": errors,
        "comparisons": comparisons,
    }
