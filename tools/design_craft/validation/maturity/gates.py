from __future__ import annotations

import json
import hashlib
import os
import re
import sys
import tempfile
import time
from pathlib import Path

from ...benchmark.runner import compare_results, run_suite
from ...release.metadata import validate_release_metadata
from .model import GateRunner, MaturityContext, MaturityGateResult
from .process_runner import bounded, json_payload, run_command


RUNTIME_SCRIPTS = {
    "design_craft_audit.sh",
    "design_craft_pass.sh",
    "design_craft_detect.sh",
    "design_craft_route.sh",
    "design_craft_seed_design.sh",
    "design_craft_taste_review.sh",
    "design_craft_browser_evidence.py",
    "design_craft_css_smell_scan.py",
    "design_craft_focus_audit.py",
    "design_craft_token_audit.py",
    "design_craft_static_review.py",
    "design_craft_l4_capture.py",
    "design_craft_l4_evidence_manifest.py",
    "design_craft_l4_eval_case.sh",
    "design_craft_l4_case_validate.py",
    "design_craft_platform_scan.py",
}
TASKS = (
    "same-prompt-dashboard-review",
    "same-prompt-motion-review",
    "same-prompt-native-adaptive-review",
)


def _result(
    gate_id: str,
    passed: bool,
    duration_ms: float,
    evidence: object,
    error: str = "",
) -> MaturityGateResult:
    return MaturityGateResult(
        gate_id=gate_id,
        status="passed" if passed else "failed",
        duration_ms=round(duration_ms, 3),
        evidence=evidence,
        error="" if passed else bounded(error or "gate failed"),
    )


def _command_gate(
    gate_id: str,
    command: list[str],
    *,
    timeout: int = 180,
    evidence: object | None = None,
) -> GateRunner:
    def evaluate(context: MaturityContext) -> MaturityGateResult:
        result = run_command(command, root=context.root, timeout=timeout)
        return _result(
            gate_id,
            result.returncode == 0,
            result.duration_ms,
            evidence if evidence is not None else {"command": command},
            result.stderr or result.stdout or result.error_code or "command failed",
        )

    return evaluate


def contract_completeness(context: MaturityContext) -> MaturityGateResult:
    result = run_command(
        [sys.executable, "scripts/design_craft_score.py", "--self", "--no-smoke", "--json"],
        root=context.root,
    )
    payload = json_payload(result)
    passed = (
        result.returncode == 0
        and payload.get("schema") == "design-craft.source-completeness.v1"
        and payload.get("score") == 100
    )
    return _result(
        "contract_completeness",
        passed,
        result.duration_ms,
        {"metric": "source_completeness", "score": payload.get("score")},
        result.stderr or "source completeness must be exactly 100",
    )


def release_metadata(phase: str) -> GateRunner:
    gate_id = f"release_metadata_{phase}"

    def evaluate(context: MaturityContext) -> MaturityGateResult:
        started = time.perf_counter()
        payload = validate_release_metadata(phase=phase, root=context.root)
        return _result(
            gate_id,
            payload.get("ok") is True,
            (time.perf_counter() - started) * 1_000,
            {
                "schema": payload.get("schema"),
                "version": payload.get("version"),
                "tag": payload.get("tag"),
                "changelog_state": payload.get("changelog_state"),
            },
            "; ".join(str(item) for item in payload.get("errors", [])),
        )

    return evaluate


def portable_runtime_payload(context: MaturityContext) -> MaturityGateResult:
    started = time.perf_counter()
    root = context.root / "skills/design-craft/scripts"
    missing = sorted(name for name in RUNTIME_SCRIPTS if not (root / name).is_file())
    non_executable = sorted(
        name for name in RUNTIME_SCRIPTS if (root / name).is_file() and not os.access(root / name, os.X_OK)
    )
    return _result(
        "portable_runtime_payload",
        not missing and not non_executable,
        (time.perf_counter() - started) * 1_000,
        {"script_count": len(RUNTIME_SCRIPTS)},
        f"missing={missing}, non_executable={non_executable}",
    )


def portable_route_fallback(context: MaturityContext) -> MaturityGateResult:
    with tempfile.TemporaryDirectory(prefix="design-craft-maturity-route-") as raw:
        target = Path(raw)
        (target / "DESIGN.md").write_text(
            "# Design\n\n## Typography System\nSystem type.\n\n## Color Palette\nSemantic roles.\n\n"
            "## Motion Language\nReduced motion.\n\n## Component Grammar\nNative states.\n",
            encoding="utf-8",
        )
        (target / "PRODUCT.md").write_text(
            "# Product\n\n## Platform\nadaptive\n", encoding="utf-8"
        )
        result = run_command(
            [
                "bash",
                "skills/design-craft/scripts/design_craft_route.sh",
                "--target",
                str(target),
                "--surface",
                "mobile",
                "--intent",
                "visual-refine",
                "--scope",
                "component",
                "--json-only",
            ],
            root=context.root,
            environment={"DESIGN_CRAFT_ROUTE_PLAN": str(target / "missing-route-plan.sh")},
        )
    payload = json_payload(result)
    passed = (
        result.returncode == 0
        and payload.get("route_source") == "portable_fallback"
        and payload.get("degraded") is True
        and payload.get("platform") == "adaptive"
        and payload.get("native_validation_required") is True
    )
    return _result(
        "portable_route_fallback",
        passed,
        result.duration_ms,
        {"route_source": payload.get("route_source"), "platform": payload.get("platform")},
        result.stderr or "portable fallback route contract failed",
    )


def detector_degraded_contract(context: MaturityContext) -> MaturityGateResult:
    with tempfile.TemporaryDirectory(prefix="design-craft-maturity-detector-") as raw:
        result = run_command(
            [
                "bash",
                "skills/design-craft/scripts/design_craft_detect.sh",
                "--target",
                "evals/fixtures/css-smells",
                "--full-json",
            ],
            root=context.root,
            environment={
                "HOME": raw,
                "DESIGN_CRAFT_SOURCE_ROOT": str(Path(raw) / "missing-source"),
                "DESIGN_CRAFT_IMPECCABLE_DETECTOR": str(Path(raw) / "missing-detect.mjs"),
            },
        )
    payload = json_payload(result)
    detector = payload.get("upstream_detector")
    passed = (
        result.returncode == 0
        and payload.get("degraded") is True
        and isinstance(detector, dict)
        and detector.get("status") == "unavailable"
    )
    return _result(
        "detector_degraded_contract",
        passed,
        result.duration_ms,
        {"degraded": payload.get("degraded")},
        result.stderr or "unavailable detector did not fail open with explicit degraded status",
    )


def platform_fixtures(context: MaturityContext) -> MaturityGateResult:
    started = time.perf_counter()
    failures: list[str] = []
    scanner = "skills/design-craft/scripts/design_craft_platform_scan.py"
    for platform in ("ios", "android", "adaptive"):
        valid = run_command(
            [sys.executable, scanner, "--target", f"evals/fixtures/platforms/{platform}/valid", "--json", "--strict"],
            root=context.root,
        )
        invalid = run_command(
            [sys.executable, scanner, "--target", f"evals/fixtures/platforms/{platform}/invalid", "--json", "--strict"],
            root=context.root,
        )
        if valid.returncode != 0:
            failures.append(f"{platform}: valid fixture failed")
        if invalid.returncode == 0:
            failures.append(f"{platform}: invalid fixture passed")
    return _result(
        "platform_fixtures",
        not failures,
        (time.perf_counter() - started) * 1_000,
        {"platforms": ["ios", "android", "adaptive"]},
        "; ".join(failures),
    )


def upstream_lock_parity(context: MaturityContext) -> MaturityGateResult:
    started = time.perf_counter()
    errors: list[str] = []
    try:
        payload = json.loads((context.root / "upstreams.lock.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return _result("upstream_lock_parity", False, 0, {}, str(exc))
    if payload.get("schema") != "design-craft.upstreams-lock.v3":
        errors.append("upstream lock schema is invalid")
    upstreams = payload.get("upstreams")
    if not isinstance(upstreams, dict):
        errors.append("upstreams must be an object")
        upstreams = {}
    for name, metadata in upstreams.items():
        if not isinstance(metadata, dict):
            errors.append(f"{name}: metadata is invalid")
            continue
        commit = metadata.get("commit")
        reviewed = metadata.get("reviewed_through_commit")
        if metadata.get("reviewed_commit") != reviewed:
            errors.append(f"{name}: reviewed commit alias is stale")
        if metadata.get("latest_range_head_commit") != reviewed:
            errors.append(f"{name}: latest reviewed range head is stale")
        if metadata.get("absorbed_commit") != metadata.get(
            "behavior_absorbed_through_commit"
        ):
            errors.append(f"{name}: absorbed commit alias is stale")
        if not metadata.get("notes") or not metadata.get("coverage_contract"):
            errors.append(f"{name}: review metadata is incomplete")
        result = run_command(
            ["git", "-C", str(metadata.get("path", "")), "rev-parse", "HEAD"],
            root=context.root,
            timeout=30,
        )
        if result.returncode != 0 or result.stdout.strip() != commit:
            errors.append(f"{name}: submodule HEAD does not match lock")
    return _result(
        "upstream_lock_parity",
        not errors,
        (time.perf_counter() - started) * 1_000,
        {"upstream_count": len(upstreams)},
        "; ".join(errors),
    )


def route_pack(context: MaturityContext) -> MaturityGateResult:
    result = run_command(
        [sys.executable, "scripts/design_craft_codex_route_pack.py", "--strict", "--json"],
        root=context.root,
        timeout=120,
    )
    payload = json_payload(result)
    passed = result.returncode == 0 and payload.get("status") == "ok"
    return _result(
        "route_pack",
        passed,
        result.duration_ms,
        {"status": payload.get("status"), "summary": payload.get("summary")},
        result.stderr or "strict route-pack validation failed",
    )


def cross_agent_contracts(context: MaturityContext) -> MaturityGateResult:
    started = time.perf_counter()
    result = run_command(
        [sys.executable, "scripts/design_craft_cross_agent_validate.py", "--root", "evals/cross-agent"],
        root=context.root,
        timeout=120,
    )
    failures = [result.stderr or result.stdout] if result.returncode != 0 else []
    return _result(
        "cross_agent_contracts",
        not failures,
        (time.perf_counter() - started) * 1_000,
        {"active": "definitions", "history": "separate_history_audit"},
        "; ".join(failures),
    )


def comparative_contracts(context: MaturityContext) -> MaturityGateResult:
    started = time.perf_counter()
    result = run_command(
        [sys.executable, "scripts/design_craft_comparative_validate.py"],
        root=context.root,
        timeout=120,
    )
    failures = [result.stderr or result.stdout] if result.returncode != 0 else []
    return _result(
        "comparative_contracts",
        not failures,
        (time.perf_counter() - started) * 1_000,
        {"active": "definitions", "history": "separate_history_audit"},
        "; ".join(failures),
    )


def l4_evidence_contract(context: MaturityContext) -> MaturityGateResult:
    started = time.perf_counter()
    failures: list[str] = []
    for case in (
        "evals/product-ui-taste/before-after/generic-review-workbench-local-l4",
        "evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4",
    ):
        result = run_command(
            [
                sys.executable,
                "skills/design-craft/scripts/design_craft_l4_case_validate.py",
                "--case-dir",
                case,
                "--strict",
            ],
            root=context.root,
        )
        if result.returncode != 0:
            failures.append(result.stderr or result.stdout)
    return _result(
        "l4_evidence_contract",
        not failures,
        (time.perf_counter() - started) * 1_000,
        {"case_count": 2, "claim": "manifest_contract_only"},
        "; ".join(failures),
    )


def performance_regression(context: MaturityContext) -> MaturityGateResult:
    started = time.perf_counter()
    path = context.baseline_path
    if path is None or not path.is_file():
        return _result(
            "performance_regression",
            False,
            (time.perf_counter() - started) * 1_000,
            {"baseline": str(path) if path else None},
            "benchmark baseline is required and must exist",
        )
    try:
        baseline = json.loads(path.read_text(encoding="utf-8"))
        current = run_suite(str(baseline.get("scale", "smoke")))
        comparison = compare_results(baseline, current)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return _result("performance_regression", False, 0, {"baseline": str(path)}, str(exc))
    evidence = {
        "baseline": str(path),
        "runner_id": current.get("runner_id"),
        "scale": current.get("scale"),
        "comparisons": comparison.get("comparisons", []),
    }
    return _result(
        "performance_regression",
        comparison.get("ok") is True,
        (time.perf_counter() - started) * 1_000,
        evidence,
        "; ".join(str(item) for item in comparison.get("errors", [])) or "benchmark regression detected",
    )


def host_current_source(host: str) -> GateRunner:
    gate_id = f"host_{host}_current_source"

    def evaluate(context: MaturityContext) -> MaturityGateResult:
        started = time.perf_counter()
        failures: list[str] = []
        for task in TASKS:
            result = run_command(
                [
                    sys.executable,
                    "scripts/design_craft_cross_agent_validate.py",
                    "--observed-task",
                    f"evals/cross-agent/{task}",
                    "--require-host",
                    host,
                ],
                root=context.root,
                timeout=120,
            )
            if result.returncode != 0:
                failures.append(f"{task}: {result.stderr or result.stdout}")
        return _result(
            gate_id,
            not failures,
            (time.perf_counter() - started) * 1_000,
            {"host": host, "tasks": list(TASKS), "schema": "score-v4"},
            "; ".join(failures),
        )

    return evaluate


def native_current_source(native: str) -> GateRunner:
    gate_id = f"native_{native}_current_source"

    def evaluate(context: MaturityContext) -> MaturityGateResult:
        evidence_root = Path(
            os.environ.get(
                "DESIGN_CRAFT_NATIVE_EVIDENCE_ROOT",
                context.root / "evals/native-runtime",
            )
        ).expanduser().resolve()
        command = [
            sys.executable,
            "scripts/design_craft_native_runtime_validate.py",
            "--validate",
            "--root",
            str(evidence_root),
            "--require-current-source",
            "--json",
        ]
        if native == "ios_simulator":
            command.extend(("--require", "ios"))
        elif native == "android_emulator":
            command.extend(("--require", "android"))
        elif native == "physical_device":
            command.append("--require-real-device")
        else:
            return _result(gate_id, False, 0, {"native": native}, "unknown native target")
        result = run_command(command, root=context.root, timeout=180)
        payload = json_payload(result)
        evidence_key = {
            "ios_simulator": "ios",
            "android_emulator": "android",
            "physical_device": "real_device",
        }[native]
        evidence_payload = payload.get("evidence")
        record = (
            evidence_payload.get(evidence_key)
            if isinstance(evidence_payload, dict)
            else None
        )
        evidence_path = evidence_root / (
            "real-device-observed.json"
            if native == "physical_device"
            else f"{'ios' if native == 'ios_simulator' else 'android'}-observed.json"
        )
        try:
            display_path = str(evidence_path.relative_to(context.root))
        except ValueError:
            display_path = evidence_path.name
        record_binding = {
            "native": native,
            "schema": record.get("schema") if isinstance(record, dict) else None,
            "evidence_path": display_path,
            "evidence_source_path": str(evidence_path),
            "evidence_sha256": (
                hashlib.sha256(evidence_path.read_bytes()).hexdigest()
                if evidence_path.is_file()
                else None
            ),
            "source_commit": record.get("source_commit") if isinstance(record, dict) else None,
            "platform": record.get("platform") if isinstance(record, dict) else None,
            "runtime_kind": record.get("runtime_kind") if isinstance(record, dict) else None,
            "contract_sha256": (
                record.get("contract_sha256") if isinstance(record, dict) else None
            ),
            "observed_at": record.get("observed_at") if isinstance(record, dict) else None,
            "workflow": record.get("workflow") if isinstance(record, dict) else None,
            "artifacts": record.get("artifacts") if isinstance(record, dict) else None,
        }
        return _result(
            gate_id,
            result.returncode == 0 and payload.get("ok") is True,
            result.duration_ms,
            record_binding,
            result.stderr or "; ".join(str(item) for item in payload.get("errors", [])),
        )

    return evaluate


def comparative_evaluation(context: MaturityContext) -> MaturityGateResult:
    return _command_gate(
        "comparative_evaluation",
        [sys.executable, "scripts/design_craft_comparative_validate.py", "--require-observed"],
        timeout=240,
        evidence={"status": "current_source_required"},
    )(context)


def clean_worktree(context: MaturityContext) -> MaturityGateResult:
    result = run_command(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        root=context.root,
        timeout=30,
    )
    dirty_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return _result(
        "clean_worktree",
        result.returncode == 0 and dirty_count == 0,
        result.duration_ms,
        {"dirty_path_count": dirty_count},
        result.stderr or "release worktree must be clean",
    )


def install_provenance(context: MaturityContext) -> MaturityGateResult:
    install_root = Path(
        os.environ.get("DESIGN_CRAFT_SKILL_ROOT", Path.home() / ".agents/skills")
    ).expanduser()
    result = run_command(
        [
            sys.executable,
            "scripts/design_craft_install_verify.py",
            "--source",
            "skills/design-craft",
            "--installed",
            str(install_root / "design-craft"),
            "--expected-name",
            "design-craft",
            "--expected-version",
            (context.root / "VERSION").read_text(encoding="utf-8").strip(),
            "--require-metadata",
            "--json",
        ],
        root=context.root,
    )
    payload = json_payload(result)
    return _result(
        "install_provenance",
        result.returncode == 0 and payload.get("ok") is True,
        result.duration_ms,
        {"installed": str(install_root / "design-craft"), "schema": payload.get("schema")},
        result.stderr or "; ".join(str(item) for item in payload.get("errors", [])),
    )


def upstream_remote_review(context: MaturityContext) -> MaturityGateResult:
    return _command_gate(
        "upstream_remote_review",
        [sys.executable, "scripts/upstream_absorption_report.py", "--remote-details", "--fail-on-unreviewed"],
        timeout=240,
        evidence={"mode": "live_remote_read"},
    )(context)


def main_branch(context: MaturityContext) -> MaturityGateResult:
    result = run_command(
        ["git", "symbolic-ref", "--quiet", "--short", "HEAD"],
        root=context.root,
        timeout=30,
    )
    branch = result.stdout.strip()
    return _result(
        "main_branch",
        result.returncode == 0 and branch == "main",
        result.duration_ms,
        {"branch": branch or None},
        result.stderr or "final release verification must run from main",
    )


def main_ruleset(context: MaturityContext) -> MaturityGateResult:
    return _command_gate(
        "main_ruleset",
        [sys.executable, "scripts/design_craft_github_governance.py"],
        timeout=240,
        evidence={"scope": "live_github_governance_read"},
    )(context)


STATIC_GATES: dict[str, GateRunner] = {
    "contract_completeness": contract_completeness,
    "release_metadata_candidate": release_metadata("candidate"),
    "release_metadata_final": release_metadata("final"),
    "portable_runtime_payload": portable_runtime_payload,
    "portable_route_fallback": portable_route_fallback,
    "detector_degraded_contract": detector_degraded_contract,
    "platform_fixtures": platform_fixtures,
    "upstream_lock_parity": upstream_lock_parity,
    "workflow_contract": _command_gate(
        "workflow_contract",
        [sys.executable, "scripts/design_craft_workflow_validate.py", "--check", "--validate"],
    ),
    "package_boundary": _command_gate(
        "package_boundary",
        [sys.executable, "scripts/design_craft_package_validate.py", "--check", "--validate"],
        timeout=240,
    ),
    "active_scope": _command_gate(
        "active_scope",
        [sys.executable, "scripts/design_craft_active_scope_validate.py", "--root", "."],
    ),
    "route_pack": route_pack,
    "cross_agent_contracts": cross_agent_contracts,
    "comparative_contracts": comparative_contracts,
    "installer_contract": _command_gate(
        "installer_contract",
        [sys.executable, "-m", "unittest", "tests.integration.test_installer"],
        timeout=180,
    ),
    "l4_evidence_contract": l4_evidence_contract,
    "performance_regression": performance_regression,
    "comparative_evaluation": comparative_evaluation,
    "clean_worktree": clean_worktree,
    "install_provenance": install_provenance,
    "upstream_remote_review": upstream_remote_review,
    "main_branch": main_branch,
    "main_ruleset": main_ruleset,
}


def gate_runner(gate_id: str) -> GateRunner:
    if gate_id in STATIC_GATES:
        return STATIC_GATES[gate_id]
    host_match = re.fullmatch(r"host_(codex|pi|cursor|claude)_current_source", gate_id)
    if host_match:
        return host_current_source(host_match.group(1))
    native_match = re.fullmatch(
        r"native_(ios_simulator|android_emulator|physical_device)_current_source",
        gate_id,
    )
    if native_match:
        return native_current_source(native_match.group(1))
    raise ValueError(f"no maturity gate runner registered for {gate_id}")
