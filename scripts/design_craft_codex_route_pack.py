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
from pathlib import Path


SCHEMA = "design-craft.codex-route-pack.v2"


@dataclass(frozen=True)
class PackFile:
    path: str
    required: bool
    kind: str


ROUTE_PACK_FILES = [
    PackFile("AGENTS.md", True, "global-rule"),
    PackFile("rules/frontend.md", True, "frontend-rule"),
    PackFile("agents/worker.toml", True, "frontend-agent"),
    PackFile("tools/frontend_route_plan.sh", True, "route-planner"),
    PackFile("tools/frontend_platform_detect.py", True, "platform-detector"),
    PackFile("tools/frontend_agent_routing.json", True, "route-config"),
    PackFile("tools/frontend_worker_entry.sh", True, "worker-gate"),
    PackFile("tools/frontend_preflight_spec.json", True, "preflight-config"),
    PackFile("tools/frontend_preflight.py", True, "preflight-runner"),
    PackFile("tools/frontend_preflight_run.sh", True, "preflight-entry"),
    PackFile("tools/frontend_preflight_verify.sh", True, "preflight-validator"),
    PackFile("tools/agents_quality_verify.sh", True, "global-validator"),
    PackFile("tools/tests/test_frontend_route_plan.sh", True, "route-test"),
    PackFile("tools/tests/test_frontend_route_contract.sh", True, "route-test"),
    PackFile("tools/tests/test_frontend_delivery_contract.sh", True, "route-test"),
    PackFile("tools/tests/test_frontend_preflight.sh", True, "preflight-test"),
    PackFile("tools/tests/test_frontend_preflight_spec_sync.sh", True, "preflight-test"),
    PackFile("tools/frontend_authority_init.sh", False, "style-authority-helper"),
    PackFile("tools/frontend_preflight_policy.json", False, "preflight-policy"),
    PackFile("tools/frontend_preflight_policy_run.sh", False, "preflight-policy"),
    PackFile("tools/frontend_preflight_report.sh", False, "preflight-report"),
    PackFile("tools/frontend_preflight_log_summary.sh", False, "preflight-logs"),
    PackFile("tools/frontend_preflight_log_rotate.sh", False, "preflight-logs"),
    PackFile("tools/frontend_preflight_log_maintenance.sh", False, "preflight-logs"),
]


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


def semantic_validation(source_root: Path) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    routing_path = source_root / "tools/frontend_agent_routing.json"
    route_plan_path = source_root / "tools/frontend_route_plan.sh"
    platform_detect_path = source_root / "tools/frontend_platform_detect.py"
    worker_entry_path = source_root / "tools/frontend_worker_entry.sh"
    worker_agent_path = source_root / "agents/worker.toml"
    config_path = source_root / "config.toml"
    profiles: list[dict[str, str]] = []
    model_catalog_source = "not-run"

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

    for path, forbidden in [
        (route_plan_path, ["gpt-5.5", "default_high", "worker_xhigh", "route_defaults ="]),
        (worker_entry_path, ["gpt-5.5", "default_high", "worker_xhigh"]),
    ]:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            issues.append(f"failed to read {path.name}: {exc}")
            continue
        for fragment in forbidden:
            if fragment in text:
                issues.append(f"{path.name} contains stale routing fragment: {fragment}")
        explicit_reasoning_vocabulary = "auto|inherit|low|medium|high|xhigh|max"
        if explicit_reasoning_vocabulary not in text:
            issues.append(f"{path.name} missing explicit reasoning vocabulary: {explicit_reasoning_vocabulary}")
        if explicit_reasoning_vocabulary + "|ultra" in text:
            issues.append(f"{path.name} incorrectly exposes ultra as an explicit frontend override")
        required_fragments = {
            "frontend_route_plan.sh": [
                "quality_governance",
                "delegation_contract",
                "--orchestration",
                "--platform",
                "--product-context-path",
                '"design_tier": tier',
                '"runtime_validation_kind"',
                '"native_validation_required"',
            ],
            "frontend_worker_entry.sh": [
                "reasoning_targets",
                "delegation_policies",
                "runtime_remediation_policies",
                "--platform",
                "runtime_validation_kinds",
                '"design_tier": frontend_tier',
            ],
        }.get(path.name, [])
        for fragment in required_fragments:
            if fragment not in text:
                issues.append(f"{path.name} missing V2 routing fragment: {fragment}")

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
        "runtime_profiles": profiles,
        "model_catalog_source": model_catalog_source,
    }


def build_manifest(source_root: Path, *, include_semantic: bool = True) -> dict:
    files = [file_entry(source_root, spec) for spec in ROUTE_PACK_FILES]
    missing_required = [
        item["path"] for item in files if item["required"] and not item["exists"]
    ]
    existing_files = [item for item in files if item["exists"]]
    if include_semantic and not missing_required:
        semantic = semantic_validation(source_root)
    else:
        reason = (
            "semantic validation skipped because required route-pack files are missing"
            if missing_required
            else "semantic validation disabled for structural self-check"
        )
        semantic = {
            "status": "skipped",
            "issues": [],
            "warnings": [reason],
            "runtime_profiles": [],
            "model_catalog_source": "unavailable",
        }
    if missing_required:
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


def copy_pack(source_root: Path, export_dir: Path, dry_run: bool) -> list[str]:
    copied: list[str] = []
    for spec in ROUTE_PACK_FILES:
        source = source_root / spec.path
        if not source.is_file():
            continue
        destination = export_dir / spec.path
        copied.append(spec.path)
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
        for spec in ROUTE_PACK_FILES:
            if not spec.required:
                continue
            path = root / spec.path
            path.parent.mkdir(parents=True, exist_ok=True)
            if spec.path.endswith(".json"):
                path.write_text("{}\n", encoding="utf-8")
            else:
                path.write_text("# fixture\n", encoding="utf-8")
            if spec.path.endswith(".sh"):
                path.chmod(0o755)

        payload = build_manifest(root, include_semantic=False)
        if payload["status"] != "ok":
            print("self-check fixture unexpectedly failed", file=sys.stderr)
            print(json.dumps(payload, indent=2), file=sys.stderr)
            return 1

        export_dir = Path(tmp) / "export"
        copied = copy_pack(root, export_dir, dry_run=False)
        if len(copied) != len([item for item in ROUTE_PACK_FILES if item.required]):
            print("self-check copied an unexpected file count", file=sys.stderr)
            return 1
        manifest_path = export_dir / "codex-route-pack.manifest.json"
        write_manifest(payload, manifest_path, dry_run=False)
        if not manifest_path.is_file():
            print("self-check did not write manifest", file=sys.stderr)
            return 1

        missing = root / "tools/frontend_route_plan.sh"
        missing.unlink()
        failed = build_manifest(root, include_semantic=False)
        if failed["status"] != "missing-required":
            print("self-check missing-required fixture unexpectedly passed", file=sys.stderr)
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
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when required files are missing.")
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
        copied = copy_pack(source_root, export_dir, dry_run=args.dry_run)
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
