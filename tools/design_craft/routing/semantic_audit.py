from __future__ import annotations

import json
import subprocess
import tomllib
from concurrent.futures import Executor, ThreadPoolExecutor
from pathlib import Path

from .manifest import load_json
from .probes import runtime_profiles
from .runtime_batch import RUNTIME_PROBE_WORKERS, submit_runtime_probe_batch


def load_toml(path: Path) -> dict:
    payload = tomllib.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected TOML table: {path}")
    return payload


def semantic_validation(source_root: Path) -> dict:
    with ThreadPoolExecutor(max_workers=RUNTIME_PROBE_WORKERS) as executor:
        return _semantic_validation(source_root, executor)


def _semantic_validation(source_root: Path, executor: Executor) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    runtime_probes: list[dict] = []
    routing_path = source_root / "tools/frontend_agent_routing.json"
    route_plan_path = source_root / "tools/frontend_route_plan.sh"
    route_core_path = source_root / "tools/frontend_route_core.py"
    route_authority_path = source_root / "tools/frontend_route_authority.py"
    route_browser_path = source_root / "tools/frontend_route_browser.py"
    route_browser_capture_path = source_root / "tools/frontend_route_browser_capture.py"
    route_browser_capture_sanitize_path = source_root / "tools/frontend_route_browser_capture_sanitize.py"
    route_browser_capture_store_path = source_root / "tools/frontend_route_browser_capture_store.py"
    route_browser_contract_path = source_root / "tools/frontend_route_browser_contract.py"
    route_browser_receipt_path = source_root / "tools/frontend_route_browser_receipt.py"
    route_browser_receipt_core_path = source_root / "tools/frontend_route_browser_receipt_core.py"
    route_browser_receipt_reducer_path = source_root / "tools/frontend_route_browser_receipt_reducer.py"
    route_delivery_path = source_root / "tools/frontend_route_delivery.py"
    route_runtime_path = source_root / "tools/frontend_route_runtime.py"
    route_telemetry_path = source_root / "tools/frontend_route_telemetry.py"
    platform_detect_path = source_root / "tools/frontend_platform_detect.py"
    worker_entry_path = source_root / "tools/frontend_worker_entry.sh"
    worker_route_core_path = source_root / "tools/frontend_worker_route_core.py"
    worker_payload_core_path = source_root / "tools/frontend_worker_payload_core.py"
    worker_agent_path = source_root / "agents/worker.toml"
    config_path = source_root / "config.toml"
    profiles: list[dict[str, str]] = []
    model_catalog_source = "not-run"

    probe_base = [
        "--surface",
        "dashboard",
        "--intent",
        "functional",
        "--scope",
        "component",
        "--visual-contract",
        "not-applicable",
        "--output",
        "json",
    ]
    compact_arguments = [
        *probe_base[:-1],
        "compact-json",
        "--browser-context",
        "local",
    ]
    probe_requests = [
        ([*probe_base, "--browser-context", "external"], None, None),
        ([*probe_base, "--browser-context", "local"], None, None),
        ([*probe_base, "--browser-context", "local"], "gpt-5.6-sol", "max"),
        (compact_arguments, "gpt-5.6-sol", "max"),
        ([*probe_base, "--browser-context", "local"], "gpt-5.6-sol", "ultra"),
    ]

    # The runtime probes are independent, read-only certification checks. Run
    # them together while the static manifest checks use the current process.
    probe_batch = submit_runtime_probe_batch(executor, source_root, probe_requests)
    schema_future = probe_batch.schema
    telemetry_future = probe_batch.telemetry
    capture_future = probe_batch.browser_capture
    receipt_future = probe_batch.browser_receipt
    route_futures = probe_batch.routes
    catalog_future = probe_batch.model_catalog

    try:
        schema_completed = schema_future.result()
        schema_payload = json.loads(schema_completed.stdout)
        if schema_completed.returncode != 0 or schema_payload.get("ok") is not True:
            schema_errors = schema_payload.get("errors")
            detail = "; ".join(schema_errors) if isinstance(schema_errors, list) else schema_completed.stderr.strip()
            issues.append(f"frontend routing JSON Schema validation failed: {detail[:500]}")
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        issues.append(f"failed to run frontend routing JSON Schema validation: {exc}")

    try:
        routing = load_json(routing_path)
        if routing.get("version") != 2:
            issues.append("frontend_agent_routing.json must use version 2")
        if routing.get("policy_name") != "frontend-route-v2":
            issues.append("frontend_agent_routing.json missing frontend-route-v2 policy name")
        tier_defaults = routing.get("tier_defaults")
        if not isinstance(tier_defaults, dict):
            issues.append("frontend_agent_routing.json missing tier_defaults")
        else:
            for tier in ["L0", "L1-F", "L1-V", "L2"]:
                route = tier_defaults.get(tier)
                if not isinstance(route, dict):
                    issues.append(f"missing tier route: {tier}")
                    continue
                if route.get("agent_route") != "main_inherit":
                    issues.append(f"{tier} must use agent_route=main_inherit")
                if route.get("agent_model") != "inherit":
                    issues.append(f"{tier} must inherit the runtime model")
                if route.get("execution_mode") != "main_serial":
                    issues.append(f"{tier} default execution_mode must be main_serial")
                if route.get("subagent_required") is not False:
                    issues.append(f"{tier} must not require a subagent by tier")
        delegation = routing.get("delegation_contract")
        if not isinstance(delegation, dict):
            issues.append("frontend_agent_routing.json missing delegation_contract")
        else:
            if delegation.get("minimum_independent_subtasks") != 2:
                issues.append("delegation requires exactly the documented minimum of two independent subtasks")
            if delegation.get("fallback_when_unavailable") != "continue_main_and_report":
                issues.append("delegation fallback must continue with the main agent")
        platform_validation = routing.get("quality_governance", {}).get("platform_validation")
        if not isinstance(platform_validation, dict):
            issues.append("frontend_agent_routing.json missing quality_governance.platform_validation")
        else:
            if platform_validation.get("surface_mobile_is_native_signal") is not False:
                issues.append("surface=mobile must not be a native platform signal")
            if platform_validation.get("static_scan_is_runtime_proof") is not False:
                issues.append("static native scans must not be runtime proof")
        quality_governance = routing.get("quality_governance", {})
        risk_governance = quality_governance.get("risk_governance", {})
        if risk_governance.get("architecture_review_required_intents") != ["redesign", "new-page"]:
            issues.append("architecture review intent triggers must be declared in routing config")
        if quality_governance.get("performance_review_required_for_surfaces") != ["dashboard", "app"]:
            issues.append("performance review surface triggers must be declared in routing config")
        reasoning = routing.get("reasoning_overrides")
        required_reasoning = {"inherit", "low", "medium", "high", "xhigh", "max", "ultra"}
        if not isinstance(reasoning, dict) or not required_reasoning.issubset(reasoning):
            issues.append("routing reasoning vocabulary must cover inherit/low/medium/high/xhigh/max/ultra")
        elif not isinstance(reasoning.get("ultra"), dict):
            issues.append("routing ultra reasoning policy must be an object")
        else:
            ultra = reasoning["ultra"]
            if ultra.get("explicit_override_allowed") is not False:
                issues.append("ultra must remain runtime-profile-only for controlled frontend delegation")
            if ultra.get("runtime_auto_delegation") is not True:
                issues.append("ultra must disclose GPT-5.6 runtime automatic delegation")
            if ultra.get("fallback_reasoning_target") != "max":
                issues.append("ultra must identify max as the explicit main-owned fallback")
        orchestration = routing.get("orchestration_overrides")
        if not isinstance(orchestration, dict) or not {"main", "parallel", "review"}.issubset(orchestration):
            issues.append("routing orchestration overrides must cover main/parallel/review")
        if "gpt-5.5" in json.dumps(routing, ensure_ascii=False):
            issues.append("routing config still pins gpt-5.5")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        issues.append(f"failed to validate routing config: {exc}")

    route_files = [
        route_plan_path,
        route_core_path,
        route_authority_path,
        route_browser_path,
        route_browser_capture_path,
        route_browser_capture_sanitize_path,
        route_browser_capture_store_path,
        route_browser_contract_path,
        route_browser_receipt_path,
        route_browser_receipt_core_path,
        route_browser_receipt_reducer_path,
        route_delivery_path,
        route_runtime_path,
        route_telemetry_path,
        worker_entry_path,
        worker_route_core_path,
        worker_payload_core_path,
    ]
    required_fragments = {
        "frontend_route_plan.sh": [
            "frontend_route_core.py",
            "--orchestration",
            "--platform",
            "--product-context-path",
            "--browser-context",
            "--delegation-authorization",
            "--visual-contract",
            "compact-json",
            "human",
        ],
        "frontend_route_core.py": [
            "from frontend_route_authority import",
            "from frontend_route_browser import resolve_browser_route",
            "from frontend_route_delivery import",
            "from frontend_route_runtime import resolve_runtime_profile",
            "from frontend_route_telemetry import ROUTE_TELEMETRY_SCHEMA, append_route_event",
            "quality_governance",
            "delegation_contract",
            "runtime_profile_verified",
            "delegation_authorization_missing",
            "architecture_review_required_intents",
            "performance_review_required_for_surfaces",
            '"frontend-route.compact.v1"',
            '"design_tier": tier',
            '"preferred_browser_tool": preferred_browser_tool',
            '"planned_browser_lifecycle": planned_browser_lifecycle',
            '"actual_browser_lifecycle_state": actual_browser_lifecycle_state',
            '"runtime_validation_kind": runtime_validation_kind',
            '"native_validation_required": native_validation_required',
        ],
        "frontend_route_authority.py": [
            "discover_design_md",
            "authority_digest",
            "build_authority_constraints",
        ],
        "frontend_route_browser.py": [
            "resolve_browser_route",
            '"preferred_browser_tool"',
            '"native_validation_required"',
            '"planned_browser_lifecycle"',
            '"actual_browser_lifecycle_state"',
        ],
        "frontend_route_browser_capture.py": [
            "from frontend_route_browser_capture_sanitize import",
            "from frontend_route_browser_capture_store import",
            '"--ingest-hook"',
            '"--strict"',
            "MAX_HOOK_BYTES",
        ],
        "frontend_route_browser_capture_sanitize.py": [
            "def sanitize_route",
            "def sanitize_hook_event",
            "def _aliased_token",
            '"workspaceKey"',
            '"preferred_browser_tool": SOURCE_SERVER',
            "SUPPORTED_ACTIONS",
        ],
        "frontend_route_browser_capture_store.py": [
            'CAPTURE_STATE_FILE = "capture-state.json"',
            'CAPTURE_HEALTH_FILE = "capture-health.json"',
            'CAPTURE_STATUS_SCHEMA = "frontend-route.browser-capture-status.v2"',
            '"last_error_code"',
            '"error_count"',
            '"health_persisted"',
            '"health_status"',
            "MAX_INCOMPLETE_STATES = 1000",
            "MAX_COMPLETE_RECEIPTS = 100",
            "def save_route_binding",
            "def ingest_observation",
            "def prune_capture_state",
        ],
        "frontend_route_browser_contract.py": [
            'RECEIPT_SCHEMA = "frontend-route.browser-lifecycle-receipt.v1"',
            'OBSERVATIONS_SCHEMA = "frontend-route.browser-lifecycle-observations.v1"',
            'OUTCOME_SCHEMA = "browser67.tool-outcome.v3"',
            "MAX_ROUTE_BYTES",
            "MAX_OBSERVATIONS",
            "planner_actual_browser_lifecycle_state",
        ],
        "frontend_route_browser_receipt.py": [
            "from frontend_route_browser_receipt_core import",
            '"--require-complete"',
            "return 3",
        ],
        "frontend_route_browser_receipt_core.py": [
            "def read_json_file",
            "def normalize_receipt",
            '"receipt_valid"',
            '"runtime_complete"',
            '"host_observation_binding"',
        ],
        "frontend_route_browser_receipt_reducer.py": [
            "class LifecycleReducer",
            "def expected_scope",
            '"workspaceKey"',
            "def _apply_entry",
            "def _apply_inspection",
            "def _apply_adoption",
            "def _apply_finalize",
            "def format_delivery_summary",
        ],
        "frontend_route_delivery.py": [
            "build_skill_selection_contract",
            "build_delivery_contract",
            "current Codex turn_context",
            "planned_browser_lifecycle",
            "actual_browser_lifecycle_state",
        ],
        "frontend_route_runtime.py": [
            "FRONTEND_RUNTIME_SESSION_DISCOVERY",
            "codex_session_turn_context",
            "contains_prompt_data",
            "_safe_evidence_path",
            "resolve_runtime_profile",
        ],
        "frontend_route_telemetry.py": [
            "FRONTEND_ROUTE_TELEMETRY_LOG_ENABLED",
            "FRONTEND_ROUTE_TELEMETRY_CONTEXT",
            "append_route_event",
            "summarize",
            'EVENT_SCHEMA = "frontend-route.telemetry-event.v2"',
            'SUMMARY_SCHEMA = "frontend-route.telemetry-summary.v2"',
            '"p50"',
            '"p95"',
            '"contains_sensitive_data"',
        ],
        "frontend_worker_entry.sh": [
            "frontend_worker_route_core.py",
            "frontend_worker_payload_core.py",
            "--platform",
            "--runtime-validation-kind",
            "--preferred-runtime-tool",
        ],
        "frontend_worker_route_core.py": [
            "reasoning_targets",
            "delegation_policies",
            "runtime_remediation_policies",
            "validate_document",
        ],
        "frontend_worker_payload_core.py": [
            "runtime_validation_kinds",
            '"design_tier": frontend_tier',
            '"preferred_runtime_tool": preferred_runtime_tool',
        ],
    }
    for path in route_files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            issues.append(f"failed to read {path.name}: {exc}")
            continue
        for fragment in ["gpt-5.5", "default_high", "worker_xhigh", "route_defaults ="]:
            if fragment in text:
                issues.append(f"{path.name} contains stale routing fragment: {fragment}")
        for fragment in required_fragments.get(path.name, []):
            if fragment not in text:
                issues.append(f"{path.name} missing V2 routing fragment: {fragment}")

    explicit_reasoning_vocabulary = "auto|inherit|low|medium|high|xhigh|max"
    for path in [route_plan_path, worker_entry_path]:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if explicit_reasoning_vocabulary not in text:
            issues.append(f"{path.name} missing explicit reasoning vocabulary: {explicit_reasoning_vocabulary}")
        if explicit_reasoning_vocabulary + "|ultra" in text:
            issues.append(f"{path.name} incorrectly exposes ultra as an explicit frontend override")

    try:
        platform_text = platform_detect_path.read_text(encoding="utf-8")
        for fragment in (
            "design-craft.platform-scan.v1",
            "React Native/Expo dependency",
            "Capacitor/Cordova/WebView shell",
            "product_context",
        ):
            if fragment not in platform_text:
                issues.append(f"frontend_platform_detect.py missing platform fragment: {fragment}")
    except OSError as exc:
        issues.append(f"failed to read frontend_platform_detect.py: {exc}")

    try:
        worker = load_toml(worker_agent_path)
        for required in ["name", "description", "developer_instructions"]:
            if not str(worker.get(required, "")).strip():
                issues.append(f"worker.toml missing required field: {required}")
        if "model" in worker or "model_reasoning_effort" in worker:
            issues.append("worker.toml must inherit model and reasoning from the parent/runtime profile")
    except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        issues.append(f"failed to validate worker.toml: {exc}")

    try:
        telemetry_completed = telemetry_future.result()
        telemetry_probe_ok = telemetry_completed.returncode == 0
        telemetry_detail = (telemetry_completed.stderr or telemetry_completed.stdout).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        telemetry_probe_ok = False
        telemetry_detail = str(exc)
    runtime_probes.append(
        {
            "name": "route_telemetry_self_check",
            "ok": telemetry_probe_ok,
        }
    )
    if not telemetry_probe_ok:
        issues.append(f"frontend route telemetry self-check failed: {telemetry_detail[:240]}")

    try:
        capture_completed = capture_future.result()
        capture_probe_ok = capture_completed.returncode == 0
        capture_detail = (capture_completed.stderr or capture_completed.stdout).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        capture_probe_ok = False
        capture_detail = str(exc)
    runtime_probes.append(
        {
            "name": "browser_lifecycle_capture_contract_tests",
            "ok": capture_probe_ok,
        }
    )
    if not capture_probe_ok:
        issues.append(f"frontend browser lifecycle capture tests failed: {capture_detail[:240]}")

    try:
        receipt_completed = receipt_future.result()
        receipt_probe_ok = receipt_completed.returncode == 0
        receipt_detail = (receipt_completed.stderr or receipt_completed.stdout).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        receipt_probe_ok = False
        receipt_detail = str(exc)
    runtime_probes.append(
        {
            "name": "browser_lifecycle_receipt_contract_tests",
            "ok": receipt_probe_ok,
        }
    )
    if not receipt_probe_ok:
        issues.append(f"frontend browser lifecycle receipt contract tests failed: {receipt_detail[:240]}")

    probe_results = [future.result() for future in route_futures]

    for (browser_context, expected_tool), (returncode, payload, detail) in zip([
        ("external", "tmwd_browser"),
        ("local", "in_app_browser"),
    ], probe_results[:2]):
        expected_lifecycle_state = (
            "not_started" if expected_tool == "tmwd_browser" else "not_applicable"
        )
        actual_lifecycle = payload.get("actual_browser_lifecycle_state")
        probe_ok = (
            returncode == 0
            and payload.get("preferred_browser_tool") == expected_tool
            and payload.get("preferred_runtime_tool") == expected_tool
            and payload.get("planned_browser_lifecycle") == payload.get("browser_lifecycle")
            and isinstance(actual_lifecycle, dict)
            and actual_lifecycle.get("state") == expected_lifecycle_state
            and actual_lifecycle.get("finalize_result") == expected_lifecycle_state
            and actual_lifecycle.get("delivery_summary_observed") is False
            and payload.get("style_authority_applicability") == "not_applicable"
            and payload.get("visual_contract_required") is False
        )
        runtime_probes.append(
            {
                "name": f"browser_context_{browser_context}",
                "ok": probe_ok,
                "returncode": returncode,
                "preferred_browser_tool": payload.get("preferred_browser_tool"),
                "preferred_runtime_tool": payload.get("preferred_runtime_tool"),
                "actual_browser_lifecycle_state": (
                    actual_lifecycle.get("state")
                    if isinstance(actual_lifecycle, dict)
                    else None
                ),
            }
        )
        if not probe_ok:
            issues.append(
                f"browser context {browser_context} route probe failed: "
                f"expected browser/runtime tool {expected_tool}; {detail[:240]}"
            )

    returncode, payload, detail = probe_results[2]
    runtime_evidence = payload.get("runtime_profile_evidence")
    runtime_truth_probe_ok = (
        returncode == 0
        and payload.get("runtime_profile_source") == "environment"
        and payload.get("runtime_profile_verified") is True
        and payload.get("effective_model") == "gpt-5.6-sol"
        and payload.get("effective_reasoning") == "max"
        and payload.get("reasoning_application_status") == "runtime_verified"
        and isinstance(runtime_evidence, dict)
        and runtime_evidence.get("kind") == "explicit_environment"
        and runtime_evidence.get("contains_prompt_data") is False
    )
    runtime_probes.append(
        {
            "name": "verified_environment_runtime_profile",
            "ok": runtime_truth_probe_ok,
            "returncode": returncode,
            "runtime_profile_source": payload.get("runtime_profile_source"),
            "runtime_profile_verified": payload.get("runtime_profile_verified"),
            "effective_model": payload.get("effective_model"),
            "effective_reasoning": payload.get("effective_reasoning"),
        }
    )
    if not runtime_truth_probe_ok:
        issues.append(f"verified environment runtime-profile probe failed: {detail[:240]}")

    returncode, payload, detail = probe_results[3]
    compact_probe_ok = (
        returncode == 0
        and payload.get("schema") == "frontend-route.compact.v1"
        and "delivery_contract" not in payload
        and payload.get("route", {}).get("frontend_tier") == "L1-F"
        and payload.get("runtime_profile", {}).get("verified") is True
        and payload.get("validation", {}).get("preflight_code") == "OK"
        and payload.get("planned_browser_lifecycle") == payload.get("browser_lifecycle")
        and payload.get("actual_browser_lifecycle_state", {}).get("state")
        == "not_applicable"
        and payload.get("actual_browser_lifecycle_state", {}).get("finalize_result")
        == "not_applicable"
    )
    runtime_probes.append(
        {
            "name": "compact_route_output",
            "ok": compact_probe_ok,
            "returncode": returncode,
            "schema": payload.get("schema"),
        }
    )
    if not compact_probe_ok:
        issues.append(f"compact route output probe failed: {detail[:240]}")

    returncode, payload, detail = probe_results[4]
    ultra_probe_ok = (
        returncode == 2
        and payload.get("route_status") == "error"
        and payload.get("route_error_code") == "RUNTIME_PROFILE_CONFLICT"
        and payload.get("gate_decision") == "deny"
        and payload.get("runtime_profile_verified") is True
        and payload.get("runtime_remediation_policy")
        == "downgrade_to_max_or_authorize_delegation"
    )
    runtime_probes.append(
        {
            "name": "unauthorized_ultra_runtime_conflict",
            "ok": ultra_probe_ok,
            "returncode": returncode,
            "route_error_code": payload.get("route_error_code"),
            "gate_decision": payload.get("gate_decision"),
        }
    )
    if not ultra_probe_ok:
        issues.append(f"unauthorized ultra runtime route probe failed: {detail[:240]}")

    if config_path.is_file():
        try:
            config = load_toml(config_path)
            profiles = runtime_profiles(config)
            catalog, catalog_warning = catalog_future.result()
            if catalog_warning:
                warnings.append(catalog_warning)
            if catalog:
                model_catalog_source = "codex debug models --bundled"
                for profile in profiles:
                    model = catalog.get(profile["model"])
                    if not model:
                        issues.append(f"runtime profile {profile['role']} references unknown model {profile['model']}")
                        continue
                    reasoning = profile["reasoning"]
                    if reasoning:
                        supported = {
                            str(item.get("effort", ""))
                            for item in model.get("supported_reasoning_levels", [])
                            if isinstance(item, dict)
                        }
                        if reasoning not in supported:
                            issues.append(
                                f"runtime profile {profile['role']} uses unsupported reasoning {reasoning} for {profile['model']}"
                            )
        except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
            issues.append(f"failed to validate config.toml model profiles: {exc}")
    else:
        warnings.append("config.toml not present in route pack source; runtime profiles were not checked")

    return {
        "status": "error" if issues else "warning" if warnings else "ok",
        "issues": issues,
        "warnings": warnings,
        "runtime_probes": runtime_probes,
        "route_modules": [path.name for path in route_files],
        "runtime_profiles": profiles,
        "model_catalog_source": model_catalog_source,
    }
