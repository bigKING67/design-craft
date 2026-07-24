from __future__ import annotations

import os
import platform
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable

from ..repo import REPO_ROOT
from ..validation.registry import load_registry, select_gates
from .contract import (
    ABSOLUTE_REGRESSION_LIMIT_MS,
    CACHE_CAPACITY,
    INCREMENTAL_FILE_COUNTS,
    MIN_FULL_SAMPLES,
    POLICY_VERSION,
    RELATIVE_REGRESSION_LIMIT,
    SCHEMA,
    compare_results,
)
from .fixtures import (
    _BoundedDigestCache,
    _completed,
    _copy_install_fixture,
    _create_tree,
    _create_validation_fixture,
    _install_command,
    _release_bundle_once,
    _run,
    _tree_digest,
    _validate_changed_files,
)


def _percentile(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    index = max(0, min(len(ordered) - 1, round((len(ordered) - 1) * percentile)))
    return ordered[index]


def _measure(function: Callable[[], object], iterations: int) -> dict[str, object]:
    if iterations <= 0:
        raise ValueError("benchmark iterations must be positive")
    samples: list[float] = []
    for _ in range(iterations):
        started = time.perf_counter()
        function()
        samples.append((time.perf_counter() - started) * 1_000)
    return {
        "unit": "ms",
        "iterations": iterations,
        "p50": round(statistics.median(samples), 3),
        "p95": round(_percentile(samples, 0.95), 3),
        "max": round(max(samples), 3),
        "samples": [round(value, 3) for value in samples],
    }



def _measure_cache(
    root: Path,
    paths: list[Path],
    *,
    capacity: int,
    iterations: int,
    warm: bool,
) -> dict[str, object]:
    observed = {"hits": 0, "misses": 0, "evictions": 0, "max_entries": 0}
    warm_cache = _BoundedDigestCache(root, capacity) if warm else None
    if warm_cache is not None:
        for path in paths:
            warm_cache.digest(path)
        warm_cache.reset_counters()

    def exercise() -> None:
        cache = warm_cache or _BoundedDigestCache(root, capacity)
        before = (cache.hits, cache.misses, cache.evictions)
        for path in paths:
            cache.digest(path)
        observed["hits"] += cache.hits - before[0]
        observed["misses"] += cache.misses - before[1]
        observed["evictions"] += cache.evictions - before[2]
        observed["max_entries"] = max(
            observed["max_entries"], cache.max_entries_observed
        )
        if cache.entries > capacity:
            raise RuntimeError("bounded validation cache exceeded its capacity")

    metric = _measure(exercise, iterations)
    metric.update(
        {
            "cache_capacity": capacity,
            "working_set": len(paths),
            "cache_hits": observed["hits"],
            "cache_misses": observed["misses"],
            "cache_evictions": observed["evictions"],
            "max_entries_observed": observed["max_entries"],
            "warm": warm,
        }
    )
    return metric



def _git_value(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def _normalized_arch() -> str:
    value = platform.machine().lower()
    return {"amd64": "x86_64", "arm64": "aarch64"}.get(value, value)


def _runner_image() -> str:
    value = os.environ.get("ImageOS", "").strip().lower()
    known = {
        "ubuntu24": "ubuntu-24.04",
        "ubuntu22": "ubuntu-22.04",
        "macos15": "macos-15",
        "macos14": "macos-14",
    }
    return known.get(value, value or platform.system().lower())


def _node_version() -> str:
    result = subprocess.run(
        ["node", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    value = result.stdout.strip().removeprefix("v")
    return value or "unavailable"


def run_suite(scale: str = "smoke") -> dict[str, object]:
    if scale not in {"smoke", "full"}:
        raise ValueError("benchmark scale must be smoke or full")
    metrics: dict[str, dict[str, object]] = {}
    with tempfile.TemporaryDirectory(prefix="design-craft-bench-") as raw:
        temporary = Path(raw)
        route_target = temporary / "route-target"
        route_target.mkdir()
        (route_target / "DESIGN.md").write_text(
            "# Design\n\n## Typography System\nReadable.\n\n"
            "## Color Palette\nSemantic.\n\n## Motion Language\nCalm.\n\n"
            "## Component Grammar\nNative states.\n",
            encoding="utf-8",
        )
        route_command = [
            "bash",
            "skills/design-craft/scripts/design_craft_route.sh",
            "--target",
            str(route_target),
            "--surface",
            "dashboard",
            "--intent",
            "visual-refine",
            "--scope",
            "page",
            "--json-only",
        ]
        route_env = {
            "FRONTEND_ROUTE_TELEMETRY_LOG_ENABLED": "0",
            "FRONTEND_RUNTIME_SESSION_DISCOVERY": "0",
            "DESIGN_CRAFT_ROUTE_PLAN": str(temporary / "missing-route-plan.sh"),
        }
        metrics["route_selection"] = _measure(
            lambda: _run(route_command, env=route_env),
            5 if scale == "smoke" else MIN_FULL_SAMPLES,
        )
        route_pack_metric = _measure(
            lambda: _run(
                [sys.executable, "scripts/design_craft_codex_route_pack.py", "--check"]
            ),
            2 if scale == "smoke" else MIN_FULL_SAMPLES,
        )
        route_pack_metric["fixture_scope"] = "portable_self_check"
        metrics["route_pack"] = route_pack_metric

        for count, iterations in ((1_000, 5), (10_000, 3)):
            fixture = temporary / f"tree-{count}"
            fixture.mkdir()
            _create_tree(fixture, count)
            metrics[f"tree_scan_{count}"] = _measure(
                lambda fixture=fixture: _tree_digest(fixture),
                iterations if scale == "smoke" else MIN_FULL_SAMPLES,
            )
        if scale == "full":
            fixture = temporary / "tree-100000"
            fixture.mkdir()
            _create_tree(fixture, 100_000)
            metrics["tree_scan_100000"] = _measure(
                lambda: _tree_digest(fixture), MIN_FULL_SAMPLES
            )

        metrics["validation_registry"] = _measure(
            lambda: select_gates(load_registry(), "portable"), 20 if scale == "smoke" else 100
        )
        metrics["lint_full"] = _measure(
            lambda: _run([sys.executable, "scripts/design_craft_lint.py"]),
            2 if scale == "smoke" else MIN_FULL_SAMPLES,
        )
        metrics["evidence_validation"] = _measure(
            lambda: _run(
                [
                    sys.executable,
                    "skills/design-craft/scripts/design_craft_browser_evidence.py",
                    "--check",
                    "--print-js",
                ]
            ),
            3 if scale == "smoke" else MIN_FULL_SAMPLES,
        )
        metrics["package_validation"] = _measure(
            lambda: _run(
                [sys.executable, "scripts/design_craft_package_validate.py", "--validate"]
            ),
            2 if scale == "smoke" else MIN_FULL_SAMPLES,
        )

        incremental_root = temporary / "incremental-validation"
        incremental_root.mkdir()
        incremental_paths = _create_validation_fixture(incremental_root)
        for count in INCREMENTAL_FILE_COUNTS:
            metric = _measure(
                lambda count=count: _validate_changed_files(
                    incremental_root, incremental_paths[:count]
                ),
                5 if scale == "smoke" else MIN_FULL_SAMPLES,
            )
            metric.update(
                {
                    "changed_files": count,
                    "validation_scope": "explicit_changed_files",
                    "fixture_root": "temporary_directory",
                }
            )
            metrics[f"incremental_validation_{count}"] = metric

        cache_paths = incremental_paths[:CACHE_CAPACITY]
        metrics["validation_cache_cold"] = _measure_cache(
            incremental_root,
            cache_paths,
            capacity=CACHE_CAPACITY,
            iterations=3 if scale == "smoke" else MIN_FULL_SAMPLES,
            warm=False,
        )
        metrics["validation_cache_warm"] = _measure_cache(
            incremental_root,
            cache_paths,
            capacity=CACHE_CAPACITY,
            iterations=3 if scale == "smoke" else MIN_FULL_SAMPLES,
            warm=True,
        )
        metrics["validation_cache_overflow"] = _measure_cache(
            incremental_root,
            incremental_paths[: CACHE_CAPACITY * 2],
            capacity=CACHE_CAPACITY,
            iterations=2 if scale == "smoke" else MIN_FULL_SAMPLES,
            warm=False,
        )

        install_fixture = temporary / "install-source"
        _copy_install_fixture(install_fixture)
        install_root = temporary / "installed"
        backup_root = temporary / "backups"
        install_env = {
            "DESIGN_CRAFT_SKILL_ROOT": str(install_root),
            "DESIGN_CRAFT_BACKUP_ROOT": str(backup_root),
            "DESIGN_CRAFT_BACKUP_KEEP": "2",
        }
        install_command = _install_command(install_fixture)
        metrics["install_atomic"] = _measure(
            lambda: _run(install_command, env=install_env),
            1 if scale == "smoke" else MIN_FULL_SAMPLES,
        )

        installed_skill = install_root / "design-craft"
        installed_digest = _tree_digest(installed_skill)

        def rollback_install() -> None:
            result = _completed(
                install_command,
                env={**install_env, "DESIGN_CRAFT_INSTALL_TEST_FAIL_AFTER_SWITCH": "1"},
            )
            if result.returncode != 1 or "previous design-craft target was restored" not in result.stderr:
                raise RuntimeError(
                    "installer rollback benchmark did not fail at the expected failpoint: "
                    + (result.stderr.strip() or f"exit={result.returncode}")
                )
            if not installed_skill.is_dir() or _tree_digest(installed_skill) != installed_digest:
                raise RuntimeError("installer rollback benchmark did not restore the original tree")

        rollback_metric = _measure(
            rollback_install, 1 if scale == "smoke" else MIN_FULL_SAMPLES
        )
        rollback_metric.update(
            {
                "failure_point": "after_switch",
                "expected_exit_code": 1,
                "rollback_verified": True,
                "install_root": "temporary_directory",
            }
        )
        metrics["install_rollback"] = rollback_metric

        contended_root = temporary / "contended-install"
        contended_backup = temporary / "contended-backups"
        lock_dir = contended_root / ".design-craft-install.lock"
        lock_dir.mkdir(parents=True)
        (lock_dir / "pid").write_text(f"{os.getpid()}\n", encoding="utf-8")
        contention_env = {
            "DESIGN_CRAFT_SKILL_ROOT": str(contended_root),
            "DESIGN_CRAFT_BACKUP_ROOT": str(contended_backup),
            "DESIGN_CRAFT_INSTALL_LOCK_TIMEOUT": "0",
        }

        def contend_install() -> None:
            result = _completed(
                [*install_command, "--lock-timeout", "0"], env=contention_env
            )
            if result.returncode != 1 or "Timed out waiting for install lock" not in result.stderr:
                raise RuntimeError(
                    "installer contention benchmark did not fail closed: "
                    + (result.stderr.strip() or f"exit={result.returncode}")
                )
            if (contended_root / "design-craft").exists():
                raise RuntimeError("installer contention benchmark modified the install target")

        contention_metric = _measure(
            contend_install, 1 if scale == "smoke" else MIN_FULL_SAMPLES
        )
        contention_metric.update(
            {
                "lock_timeout_seconds": 0,
                "contention_observed": True,
                "real_install_touched": False,
                "install_root": "temporary_directory",
            }
        )
        metrics["installer_lock_contention"] = contention_metric

        release_observations: list[tuple[int, str]] = []
        release_index = 0

        def build_release_bundle() -> None:
            nonlocal release_index
            output = temporary / f"release-bundle-{release_index:02d}"
            release_index += 1
            release_observations.append(_release_bundle_once(output))

        release_metric = _measure(
            build_release_bundle, 2 if scale == "smoke" else MIN_FULL_SAMPLES
        )
        bundle_sizes = {item[0] for item in release_observations}
        bundle_digests = {item[1] for item in release_observations}
        deterministic = len(bundle_sizes) == 1 and len(bundle_digests) == 1
        if not deterministic:
            raise RuntimeError("release bundle benchmark produced non-deterministic package bytes")
        release_metric.update(
            {
                "bundle_kind": "operational_npm_package",
                "artifact_bytes": release_observations[0][0],
                "deterministic": True,
                "output_root": "temporary_directory",
            }
        )
        metrics["release_bundle_build"] = release_metric

    return {
        "schema": SCHEMA,
        "scale": scale,
        "runner": {
            "os": platform.system().lower(),
            "arch": _normalized_arch(),
            "image": _runner_image(),
            "image_version": os.environ.get("ImageVersion", "unavailable"),
            "python": platform.python_version(),
            "node": _node_version(),
        },
        "diagnostics": {
            "platform": platform.platform(),
            "kernel": platform.release(),
        },
        "source_commit": _git_value("rev-parse", "HEAD"),
        "source_dirty": bool(_git_value("status", "--porcelain=v1", "--untracked-files=all")),
        "policy": {
            "version": POLICY_VERSION,
            "relative_regression_limit": RELATIVE_REGRESSION_LIMIT,
            "absolute_regression_limit_ms": ABSOLUTE_REGRESSION_LIMIT_MS,
        },
        "metrics": metrics,
    }
