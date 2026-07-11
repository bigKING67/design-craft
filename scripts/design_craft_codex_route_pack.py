#!/usr/bin/env python3
"""Audit or export the local Codex frontend route toolkit.

The route planner and global frontend rules live under ``~/.codex`` on this
machine, which is intentionally outside this repository. This helper makes that
local state portable by producing a whitelisted manifest, and optionally a
copyable bundle, without putting arbitrary Codex home contents under source
control.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


SCHEMA = "design-craft.codex-route-pack.v2"
ROUTE_PACK_MANIFEST_SCHEMA = "codex.frontend-route-pack.manifest.v1"
ROUTE_PACK_MANIFEST_PATH = "tools/frontend_route_pack_manifest.json"


@dataclass(frozen=True)
class PackFile:
    path: str
    required: bool
    kind: str


SUGGESTED_VALIDATION_COMMANDS = [
    "bash ~/.codex/tools/tests/test_frontend_route_plan.sh",
    "bash ~/.codex/tools/tests/test_frontend_delivery_contract.sh",
    "bash ~/.codex/tools/tests/test_frontend_route_contract.sh",
    "bash ~/.codex/tools/tests/test_frontend_preflight_spec_sync.sh",
    "bash ~/.codex/tools/tests/test_frontend_preflight.sh",
    "bash ~/.codex/tools/frontend_preflight_verify.sh",
    "bash ~/.codex/tools/agents_quality_verify.sh --fast",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def default_source_root() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_entry(source_root: Path, spec: PackFile) -> dict:
    path = source_root / spec.path
    entry = {
        "path": spec.path,
        "required": spec.required,
        "kind": spec.kind,
        "exists": path.is_file(),
    }
    if path.is_file():
        mode = path.stat().st_mode
        entry.update(
            {
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "executable": bool(mode & stat.S_IXUSR),
            }
        )
    return entry


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def normalize_manifest_path(raw_path: object) -> str:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ValueError("route-pack manifest file path must be a non-empty string")
    path = raw_path.strip()
    posix_path = PurePosixPath(path)
    if posix_path.is_absolute() or "\\" in path or any(part in {"", ".", ".."} for part in posix_path.parts):
        raise ValueError(f"route-pack manifest file path must be a safe relative POSIX path: {path!r}")
    return posix_path.as_posix()


def load_route_pack_files(source_root: Path) -> tuple[list[PackFile], dict]:
    manifest_path = source_root / ROUTE_PACK_MANIFEST_PATH
    manifest = load_json(manifest_path)
    errors: list[str] = []

    if manifest.get("schema") != ROUTE_PACK_MANIFEST_SCHEMA:
        errors.append(
            "route-pack manifest schema must be "
            f"{ROUTE_PACK_MANIFEST_SCHEMA}, got {manifest.get('schema')!r}"
        )
    if manifest.get("version") != 1:
        errors.append("route-pack manifest version must be 1")

    raw_files = manifest.get("files")
    if not isinstance(raw_files, list) or not raw_files:
        errors.append("route-pack manifest files must be a non-empty array")
        raw_files = []

    seen: set[str] = set()
    route_pack_files: list[PackFile] = []
    snapshot_paths: set[str] = set()
    route_pack_metadata: dict[str, dict] = {}
    for index, raw in enumerate(raw_files):
        prefix = f"route-pack manifest files[{index}]"
        if not isinstance(raw, dict):
            errors.append(f"{prefix} must be an object")
            continue
        try:
            rel_path = normalize_manifest_path(raw.get("path"))
        except ValueError as exc:
            errors.append(f"{prefix}: {exc}")
            continue
        if rel_path in seen:
            errors.append(f"route-pack manifest contains duplicate path: {rel_path}")
            continue
        seen.add(rel_path)

        required = raw.get("required")
        route_pack = raw.get("route_pack")
        snapshot = raw.get("snapshot")
        kind = raw.get("kind")
        if not isinstance(required, bool):
            errors.append(f"{prefix}.required must be boolean")
        if not isinstance(route_pack, bool):
            errors.append(f"{prefix}.route_pack must be boolean")
        if not isinstance(snapshot, bool):
            errors.append(f"{prefix}.snapshot must be boolean")
        if not isinstance(kind, str) or not kind.strip():
            errors.append(f"{prefix}.kind must be a non-empty string")
        if not all(
            [
                isinstance(required, bool),
                isinstance(route_pack, bool),
                isinstance(snapshot, bool),
                isinstance(kind, str) and bool(kind.strip()),
            ]
        ):
            continue

        if snapshot:
            snapshot_paths.add(rel_path)
        if route_pack:
            route_pack_files.append(PackFile(rel_path, required, kind.strip()))
            route_pack_metadata[rel_path] = raw

    manifest_entry = route_pack_metadata.get(ROUTE_PACK_MANIFEST_PATH)
    if not manifest_entry or manifest_entry.get("required") is not True:
        errors.append(
            f"{ROUTE_PACK_MANIFEST_PATH} must include itself as required route_pack=true"
        )
    required_without_snapshot = sorted(
        spec.path
        for spec in route_pack_files
        if spec.required and spec.path not in snapshot_paths
    )
    if required_without_snapshot:
        errors.append(
            "required route-pack files must also be snapshot=true: "
            + ", ".join(required_without_snapshot)
        )
    if not route_pack_files:
        errors.append("route-pack manifest selects no route_pack=true files")
    if errors:
        raise ValueError("; ".join(errors))

    return route_pack_files, {
        "schema": manifest["schema"],
        "version": manifest["version"],
        "path": ROUTE_PACK_MANIFEST_PATH,
        "sha256": sha256_file(manifest_path),
        "declared_files": len(raw_files),
        "selected_files": len(route_pack_files),
        "required_files": sum(1 for spec in route_pack_files if spec.required),
        "snapshot_files": len(snapshot_paths),
        "required_snapshot_covered": not required_without_snapshot,
    }


def load_toml(path: Path) -> dict:
    payload = tomllib.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected TOML table: {path}")
    return payload


def bundled_model_catalog() -> tuple[dict[str, dict], str | None]:
    codex = shutil.which("codex")
    if not codex:
        return {}, "codex executable is unavailable; runtime model compatibility was not checked"
    try:
        completed = subprocess.run(
            [codex, "debug", "models", "--bundled"],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {}, f"failed to load bundled model catalog: {exc}"
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        return {}, f"codex debug models --bundled failed: {detail[:240]}"
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {}, f"bundled model catalog is not valid JSON: {exc}"
    models = payload.get("models") if isinstance(payload, dict) else None
    if not isinstance(models, list):
        return {}, "bundled model catalog does not contain a models list"
    catalog = {
        str(item.get("slug")): item
        for item in models
        if isinstance(item, dict) and str(item.get("slug", "")).strip()
    }
    return catalog, None


def runtime_profiles(config: dict) -> list[dict[str, str]]:
    profiles: list[dict[str, str]] = []

    def add(role: str, model: object, reasoning: object = "") -> None:
        model_name = str(model or "").strip()
        if not model_name:
            return
        profiles.append(
            {
                "role": role,
                "model": model_name,
                "reasoning": str(reasoning or "").strip(),
            }
        )

    add("main", config.get("model"), config.get("model_reasoning_effort"))
    add("review_model", config.get("review_model"))
    agents = config.get("agents")
    if isinstance(agents, dict):
        for role, raw in agents.items():
            if isinstance(raw, dict):
                add(f"agent:{role}", raw.get("model"), raw.get("model_reasoning_effort"))
    return profiles


def run_route_probe(
    source_root: Path,
    arguments: list[str],
    *,
    runtime_model: str | None = None,
    runtime_reasoning: str | None = None,
) -> tuple[int, dict, str]:
    route_plan = source_root / "tools/frontend_route_plan.sh"
    env = os.environ.copy()
    env.update(
        {
            "CODEX_HOME": str(source_root),
            "FRONTEND_WORKSPACE_ROOT": str(source_root),
            "FRONTEND_PREFLIGHT_LOG_ENABLED": "0",
        }
    )
    env.pop("CODEX_EFFECTIVE_MODEL", None)
    env.pop("CODEX_EFFECTIVE_REASONING", None)
    if runtime_model is not None:
        env["CODEX_EFFECTIVE_MODEL"] = runtime_model
    if runtime_reasoning is not None:
        env["CODEX_EFFECTIVE_REASONING"] = runtime_reasoning
    try:
        completed = subprocess.run(
            ["bash", str(route_plan), *arguments],
            cwd=source_root,
            env=env,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, {}, str(exc)
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        detail = (completed.stderr or completed.stdout).strip()
        return completed.returncode, {}, f"invalid route JSON: {exc}; {detail[:240]}"
    return completed.returncode, payload, (completed.stderr or "").strip()


def semantic_validation(source_root: Path) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    runtime_probes: list[dict] = []
    routing_path = source_root / "tools/frontend_agent_routing.json"
    routing_schema_path = source_root / "tools/frontend_agent_routing.schema.json"
    routing_schema_validator_path = source_root / "tools/frontend_route_schema_validate.py"
    route_plan_path = source_root / "tools/frontend_route_plan.sh"
    route_core_path = source_root / "tools/frontend_route_core.py"
    platform_detect_path = source_root / "tools/frontend_platform_detect.py"
    worker_entry_path = source_root / "tools/frontend_worker_entry.sh"
    worker_route_core_path = source_root / "tools/frontend_worker_route_core.py"
    worker_payload_core_path = source_root / "tools/frontend_worker_payload_core.py"
    worker_agent_path = source_root / "agents/worker.toml"
    config_path = source_root / "config.toml"
    profiles: list[dict[str, str]] = []
    model_catalog_source = "not-run"

    try:
        schema_completed = subprocess.run(
            [
                sys.executable,
                str(routing_schema_validator_path),
                "--schema",
                str(routing_schema_path),
                "--instance",
                str(routing_path),
                "--json",
            ],
            cwd=source_root,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
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
        ],
        "frontend_route_core.py": [
            "quality_governance",
            "delegation_contract",
            "runtime_profile_verified",
            "delegation_authorization_missing",
            '"design_tier": tier',
            '"preferred_browser_tool": preferred_browser_tool',
            '"runtime_validation_kind": runtime_validation_kind',
            '"native_validation_required": native_validation_required',
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
    for browser_context, expected_tool in [
        ("external", "tmwd_browser"),
        ("local", "in_app_browser"),
    ]:
        returncode, payload, detail = run_route_probe(
            source_root,
            [*probe_base, "--browser-context", browser_context],
        )
        probe_ok = (
            returncode == 0
            and payload.get("preferred_browser_tool") == expected_tool
            and payload.get("preferred_runtime_tool") == expected_tool
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
            }
        )
        if not probe_ok:
            issues.append(
                f"browser context {browser_context} route probe failed: "
                f"expected browser/runtime tool {expected_tool}; {detail[:240]}"
            )

    returncode, payload, detail = run_route_probe(
        source_root,
        [*probe_base, "--browser-context", "local"],
        runtime_model="gpt-5.6-sol",
        runtime_reasoning="ultra",
    )
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
            catalog, catalog_warning = bundled_model_catalog()
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
        "runtime_profiles": profiles,
        "model_catalog_source": model_catalog_source,
    }


def build_manifest(source_root: Path, *, include_semantic: bool = True) -> dict:
    manifest_error = ""
    try:
        route_pack_files, route_pack_manifest = load_route_pack_files(source_root)
        route_pack_manifest["status"] = "ok"
        route_pack_manifest["errors"] = []
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        manifest_error = str(exc)
        route_pack_files = [
            PackFile(ROUTE_PACK_MANIFEST_PATH, True, "route-manifest")
        ]
        manifest_path = source_root / ROUTE_PACK_MANIFEST_PATH
        route_pack_manifest = {
            "schema": "unknown",
            "version": None,
            "path": ROUTE_PACK_MANIFEST_PATH,
            "sha256": sha256_file(manifest_path) if manifest_path.is_file() else "",
            "declared_files": 0,
            "selected_files": 0,
            "required_files": 1,
            "snapshot_files": 0,
            "required_snapshot_covered": False,
            "status": "error",
            "errors": [manifest_error],
        }

    files = [file_entry(source_root, spec) for spec in route_pack_files]
    missing_required = [
        item["path"] for item in files if item["required"] and not item["exists"]
    ]
    existing_files = [item for item in files if item["exists"]]
    if include_semantic and not missing_required and not manifest_error:
        semantic = semantic_validation(source_root)
    else:
        reason = (
            "semantic validation skipped because the route-pack manifest is invalid"
            if manifest_error
            else "semantic validation skipped because required route-pack files are missing"
            if missing_required
            else "semantic validation disabled for structural self-check"
        )
        semantic = {
            "status": "skipped",
            "issues": [],
            "warnings": [reason],
            "runtime_probes": [],
            "runtime_profiles": [],
            "model_catalog_source": "unavailable",
        }
    if manifest_error:
        status = "manifest-error"
    elif missing_required:
        status = "missing-required"
    elif semantic["status"] == "error":
        status = "semantic-error"
    else:
        status = "ok"
    return {
        "schema": SCHEMA,
        "generated_at": utc_now(),
        "source_root": str(source_root),
        "status": status,
        "route_pack_manifest": route_pack_manifest,
        "summary": {
            "tracked_files": len(files),
            "existing_files": len(existing_files),
            "required_files": sum(1 for item in files if item["required"]),
            "missing_required": missing_required,
        },
        "files": files,
        "semantic_validation": semantic,
        "validation": {
            "suggested_commands": SUGGESTED_VALIDATION_COMMANDS,
            "screenshot_policy": "Route planner decides screenshot_evidence_level=none|optional|required.",
        },
    }


def copy_pack(source_root: Path, export_dir: Path, files: list[dict], dry_run: bool) -> list[str]:
    copied: list[str] = []
    for item in files:
        source = source_root / item["path"]
        if not source.is_file():
            continue
        destination = export_dir / item["path"]
        copied.append(item["path"])
        if dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return copied


def write_manifest(payload: dict, manifest_path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def emit_human(payload: dict, copied: list[str], manifest_path: Path | None, dry_run: bool) -> None:
    summary = payload["summary"]
    print(f"schema: {payload['schema']}")
    print(f"source_root: {payload['source_root']}")
    print(f"status: {payload['status']}")
    route_pack_manifest = payload.get("route_pack_manifest", {})
    print(
        "route_pack_manifest: "
        f"{route_pack_manifest.get('status', 'unknown')} "
        f"({route_pack_manifest.get('path', ROUTE_PACK_MANIFEST_PATH)})"
    )
    for error in route_pack_manifest.get("errors", []):
        print(f"- manifest_error: {error}")
    print(
        "files: "
        f"{summary['existing_files']}/{summary['tracked_files']} existing, "
        f"{len(summary['missing_required'])} missing required"
    )
    if summary["missing_required"]:
        print("missing_required:")
        for rel_path in summary["missing_required"]:
            print(f"- {rel_path}")
    semantic = payload.get("semantic_validation", {})
    if semantic:
        print(f"semantic_validation: {semantic.get('status', 'unknown')}")
        for issue in semantic.get("issues", []):
            print(f"- semantic_error: {issue}")
        for warning in semantic.get("warnings", []):
            print(f"- semantic_warning: {warning}")
    if copied:
        action = "would_copy" if dry_run else "copied"
        print(f"{action}: {len(copied)} files")
    if manifest_path is not None:
        action = "would_write_manifest" if dry_run else "manifest"
        print(f"{action}: {manifest_path}")


def self_check() -> int:
    with tempfile.TemporaryDirectory(prefix="design-craft-route-pack.") as tmp:
        root = Path(tmp) / "codex-home"
        fixture_files = [
            {
                "path": ROUTE_PACK_MANIFEST_PATH,
                "required": True,
                "kind": "route-manifest",
                "route_pack": True,
                "snapshot": True,
            },
            {
                "path": "tools/frontend_route_plan.sh",
                "required": True,
                "kind": "route-planner",
                "route_pack": True,
                "snapshot": True,
            },
            {
                "path": "tools/frontend_authority_init.sh",
                "required": False,
                "kind": "style-authority-helper",
                "route_pack": True,
                "snapshot": True,
            },
        ]
        manifest_path = root / ROUTE_PACK_MANIFEST_PATH
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(
                {
                    "schema": ROUTE_PACK_MANIFEST_SCHEMA,
                    "version": 1,
                    "files": fixture_files,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        for raw in fixture_files:
            if not raw["required"] or raw["path"] == ROUTE_PACK_MANIFEST_PATH:
                continue
            path = root / raw["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# fixture\n", encoding="utf-8")
            if raw["path"].endswith(".sh"):
                path.chmod(0o755)

        payload = build_manifest(root, include_semantic=False)
        if payload["status"] != "ok":
            print("self-check fixture unexpectedly failed", file=sys.stderr)
            print(json.dumps(payload, indent=2), file=sys.stderr)
            return 1

        export_dir = Path(tmp) / "export"
        copied = copy_pack(root, export_dir, payload["files"], dry_run=False)
        if copied != [ROUTE_PACK_MANIFEST_PATH, "tools/frontend_route_plan.sh"]:
            print("self-check copied an unexpected file count", file=sys.stderr)
            return 1
        export_manifest_path = export_dir / "codex-route-pack.manifest.json"
        write_manifest(payload, export_manifest_path, dry_run=False)
        if not export_manifest_path.is_file():
            print("self-check did not write manifest", file=sys.stderr)
            return 1

        missing = root / "tools/frontend_route_plan.sh"
        missing.unlink()
        failed = build_manifest(root, include_semantic=False)
        if failed["status"] != "missing-required":
            print("self-check missing-required fixture unexpectedly passed", file=sys.stderr)
            return 1

        fixture_files[1]["snapshot"] = False
        manifest_path.write_text(
            json.dumps(
                {
                    "schema": ROUTE_PACK_MANIFEST_SCHEMA,
                    "version": 1,
                    "files": fixture_files,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        invalid_manifest = build_manifest(root, include_semantic=False)
        if invalid_manifest["status"] != "manifest-error":
            print("self-check invalid manifest unexpectedly passed", file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit or export the local Codex frontend route toolkit."
    )
    parser.add_argument("--source-root", default=None, help="Codex home root; default: $CODEX_HOME or ~/.codex.")
    parser.add_argument("--export-dir", default=None, help="Optional directory to receive a whitelisted copy.")
    parser.add_argument("--manifest", default=None, help="Optional manifest output path.")
    parser.add_argument("--json", action="store_true", help="Print the manifest JSON to stdout.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero for manifest, required-file, or semantic validation failures.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be written without copying files.")
    parser.add_argument("--check", action="store_true", help="Run built-in self-check fixtures.")
    args = parser.parse_args()

    if args.check:
        return self_check()

    source_root = (
        Path(args.source_root).expanduser().resolve()
        if args.source_root
        else default_source_root().resolve()
    )
    payload = build_manifest(source_root)

    export_dir = Path(args.export_dir).expanduser().resolve() if args.export_dir else None
    manifest_path = Path(args.manifest).expanduser().resolve() if args.manifest else None
    copied: list[str] = []

    if export_dir is not None:
        if export_dir == source_root or source_root in export_dir.parents:
            print("Refusing to export the route pack inside the source Codex home.", file=sys.stderr)
            return 2
        if payload.get("route_pack_manifest", {}).get("status") != "ok":
            print("Refusing to export from an invalid route-pack manifest.", file=sys.stderr)
            return 2
        copied = copy_pack(source_root, export_dir, payload["files"], dry_run=args.dry_run)
        if manifest_path is None:
            manifest_path = export_dir / "codex-route-pack.manifest.json"

    if manifest_path is not None:
        write_manifest(payload, manifest_path, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        emit_human(payload, copied, manifest_path, dry_run=args.dry_run)

    if args.strict and payload["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
