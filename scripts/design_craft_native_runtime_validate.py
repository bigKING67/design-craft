#!/usr/bin/env python3
"""Probe native SDK availability and validate observed native runtime evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PROBE_SCHEMA = "design-craft.native-runtime-probe.v1"
EVIDENCE_SCHEMA = "design-craft.native-runtime-evidence.v1"
VALIDATION_SCHEMA = "design-craft.native-runtime-validation.v1"
PLATFORM_FILES = {
    "ios": "ios-observed.json",
    "android": "android-observed.json",
}
PLATFORM_RUNTIME_KIND = {
    "ios": "ios_simulator",
    "android": "android_emulator",
}
RUNTIME_KINDS = {
    "ios": {"ios_simulator", "ios_device"},
    "android": {"android_emulator", "android_device"},
}


def run(command: list[str], timeout: int = 15) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(command, 1, "", str(exc))


def command_path(name: str) -> str | None:
    return shutil.which(name)


def probe_environment() -> dict:
    xcode_select = run(["xcode-select", "-p"]) if command_path("xcode-select") else None
    simctl = run(["xcrun", "--find", "simctl"]) if command_path("xcrun") else None
    ios_devices: list[str] = []
    if simctl and simctl.returncode == 0:
        listed = run(["xcrun", "simctl", "list", "devices", "available", "-j"], timeout=30)
        if listed.returncode == 0:
            try:
                payload = json.loads(listed.stdout)
                for devices in payload.get("devices", {}).values():
                    for device in devices:
                        if device.get("isAvailable"):
                            ios_devices.append(f"{device.get('name')} ({device.get('udid')})")
            except json.JSONDecodeError:
                pass

    adb_path = command_path("adb")
    adb_devices: list[str] = []
    if adb_path:
        listed = run([adb_path, "devices", "-l"])
        if listed.returncode == 0:
            adb_devices = [
                line.strip()
                for line in listed.stdout.splitlines()[1:]
                if line.strip() and "\tdevice" in line
            ]

    emulator_path = command_path("emulator")
    android_avds: list[str] = []
    if emulator_path:
        listed = run([emulator_path, "-list-avds"])
        if listed.returncode == 0:
            android_avds = [line.strip() for line in listed.stdout.splitlines() if line.strip()]

    return {
        "schema": PROBE_SCHEMA,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "ios": {
            "xcode_select_path": xcode_select.stdout.strip() if xcode_select and xcode_select.returncode == 0 else None,
            "xcodebuild_path": command_path("xcodebuild"),
            "simctl_path": simctl.stdout.strip() if simctl and simctl.returncode == 0 else None,
            "available_simulators": ios_devices,
            "ready": bool(simctl and simctl.returncode == 0 and ios_devices),
            "detail": "simctl unavailable" if not simctl or simctl.returncode != 0 else "no available Simulator runtime" if not ios_devices else "ready",
        },
        "android": {
            "adb_path": adb_path,
            "emulator_path": emulator_path,
            "available_avds": android_avds,
            "connected_devices": adb_devices,
            "ready": bool(adb_path and emulator_path and android_avds),
            "detail": "adb unavailable" if not adb_path else "emulator unavailable" if not emulator_path else "no AVD configured" if not android_avds else "ready",
        },
    }


def validate_evidence(
    path: Path,
    expected_platform: str,
    expected_runtime_kind: str | None = None,
) -> tuple[dict, list[str]]:
    if not path.is_file():
        return {}, [f"missing observed evidence: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"invalid evidence JSON {path}: {exc}"]

    errors: list[str] = []
    if payload.get("schema") != EVIDENCE_SCHEMA:
        errors.append(f"{path}: schema must be {EVIDENCE_SCHEMA}")
    if payload.get("platform") != expected_platform:
        errors.append(f"{path}: platform must be {expected_platform}")
    if payload.get("verified") is not True:
        errors.append(f"{path}: verified must be true")
    if payload.get("runtime_kind") not in RUNTIME_KINDS[expected_platform]:
        errors.append(f"{path}: invalid runtime_kind for {expected_platform}")
    if expected_runtime_kind and payload.get("runtime_kind") != expected_runtime_kind:
        errors.append(f"{path}: runtime_kind must be {expected_runtime_kind}")
    if payload.get("evidence_level") != "runtime_observed":
        errors.append(f"{path}: evidence_level must be runtime_observed")
    observed_at = payload.get("observed_at")
    if not isinstance(observed_at, str) or not observed_at.endswith("Z"):
        errors.append(f"{path}: observed_at must be a UTC timestamp ending in Z")
    runtime_id = payload.get("runtime_id")
    if not isinstance(runtime_id, str) or len(runtime_id.strip()) < 3:
        errors.append(f"{path}: runtime_id is required")
    if not isinstance(payload.get("tool"), str) or not payload["tool"].strip():
        errors.append(f"{path}: tool is required")
    if not re.fullmatch(r"[0-9a-f]{40}", str(payload.get("source_commit", ""))):
        errors.append(f"{path}: source_commit must be a full lowercase Git SHA")
    if not isinstance(payload.get("source_dirty"), bool):
        errors.append(f"{path}: source_dirty must be boolean")
    if not isinstance(payload.get("capture_context"), str) or not payload["capture_context"].strip():
        errors.append(f"{path}: capture_context is required")
    commands = payload.get("commands")
    if not isinstance(commands, list) or not commands or not all(isinstance(item, str) and item.strip() for item in commands):
        errors.append(f"{path}: commands must be a non-empty string array")
    assertions = payload.get("assertions")
    if not isinstance(assertions, dict) or len(assertions) < 3:
        errors.append(f"{path}: assertions must contain at least three runtime checks")
    elif not all(value is True for value in assertions.values()):
        errors.append(f"{path}: every recorded runtime assertion must pass")
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(f"{path}: at least one runtime artifact is required")
    else:
        evidence_dir = path.parent.resolve()
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                errors.append(f"{path}: artifact {index} must be an object")
                continue
            raw_artifact_path = artifact.get("path")
            if not isinstance(raw_artifact_path, str) or not raw_artifact_path.strip():
                errors.append(f"{path}: artifact {index} path is required")
                continue
            sha = str(artifact.get("sha256", ""))
            if not re.fullmatch(r"[0-9a-f]{64}", sha):
                errors.append(f"{path}: artifact {index} sha256 must be 64 lowercase hex characters")
            expected_bytes = artifact.get("bytes")
            if not isinstance(expected_bytes, int) or isinstance(expected_bytes, bool) or expected_bytes <= 0:
                errors.append(f"{path}: artifact {index} bytes must be a positive integer")

            relative_path = Path(raw_artifact_path)
            if relative_path.is_absolute() or ".." in relative_path.parts:
                errors.append(f"{path}: artifact {index} path must stay relative to the evidence directory")
                continue
            artifact_path = (evidence_dir / relative_path).resolve()
            if artifact_path != evidence_dir and evidence_dir not in artifact_path.parents:
                errors.append(f"{path}: artifact {index} path escapes the evidence directory")
                continue
            if not artifact_path.is_file():
                errors.append(f"{path}: artifact {index} file is missing: {artifact_path}")
                continue
            observed_bytes = artifact_path.stat().st_size
            if isinstance(expected_bytes, int) and observed_bytes != expected_bytes:
                errors.append(
                    f"{path}: artifact {index} byte count does not match {artifact_path}"
                )
            observed_sha = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
            if observed_sha != sha:
                errors.append(f"{path}: artifact {index} hash does not match {artifact_path}")
    return payload, errors


def validate_root(root: Path, required: list[str], require_real_device: bool = False) -> dict:
    evidence: dict[str, dict] = {}
    errors: list[str] = []
    for name in required:
        payload, platform_errors = validate_evidence(
            root / PLATFORM_FILES[name],
            name,
            PLATFORM_RUNTIME_KIND[name],
        )
        if payload:
            evidence[name] = payload
        errors.extend(platform_errors)
    if require_real_device:
        device_path = root / "real-device-observed.json"
        try:
            device_payload = json.loads(device_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"missing or invalid real-device evidence: {device_path}: {exc}")
        else:
            device_platform = device_payload.get("platform")
            if device_platform not in PLATFORM_FILES:
                errors.append(f"{device_path}: platform must be ios or android")
            else:
                payload, device_errors = validate_evidence(
                    device_path,
                    device_platform,
                    f"{device_platform}_device",
                )
                if payload:
                    evidence["real_device"] = payload
                errors.extend(device_errors)
    return {
        "schema": VALIDATION_SCHEMA,
        "root": str(root),
        "required_platforms": required,
        "require_real_device": require_real_device,
        "ok": not errors,
        "evidence": evidence,
        "errors": errors,
    }


def run_self_check() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="design-craft-native-runtime-") as raw:
        root = Path(raw)
        artifact_path = root / "fixture.png"
        artifact_path.write_bytes(b"runtime-evidence")
        valid = {
            "schema": EVIDENCE_SCHEMA,
            "platform": "ios",
            "verified": True,
            "runtime_kind": "ios_simulator",
            "evidence_level": "runtime_observed",
            "observed_at": "2026-01-01T00:00:00Z",
            "runtime_id": "fixture-simulator",
            "tool": "fixture",
            "source_commit": "a" * 40,
            "source_dirty": False,
            "capture_context": "fixture",
            "commands": ["xcrun simctl boot fixture"],
            "assertions": {"build": True, "launch": True, "interaction": True},
            "artifacts": [
                {
                    "path": artifact_path.name,
                    "sha256": hashlib.sha256(artifact_path.read_bytes()).hexdigest(),
                    "bytes": artifact_path.stat().st_size,
                }
            ],
        }
        path = root / "ios-observed.json"
        path.write_text(json.dumps(valid), encoding="utf-8")
        _, valid_errors = validate_evidence(path, "ios")
        errors.extend(valid_errors)
        valid["evidence_level"] = "static_source"
        path.write_text(json.dumps(valid), encoding="utf-8")
        _, invalid_errors = validate_evidence(path, "ios")
        if not any("runtime_observed" in item for item in invalid_errors):
            errors.append("self-check failed to reject static evidence")
        valid["evidence_level"] = "runtime_observed"
        valid["artifacts"][0]["path"] = "missing.png"
        path.write_text(json.dumps(valid), encoding="utf-8")
        _, missing_artifact_errors = validate_evidence(path, "ios")
        if not any("file is missing" in item for item in missing_artifact_errors):
            errors.append("self-check failed to reject missing runtime artifacts")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", action="store_true", help="Probe native SDK and runtime availability")
    parser.add_argument("--write-probe", help="Write the probe JSON to this path")
    parser.add_argument("--validate", action="store_true", help="Validate observed runtime evidence")
    parser.add_argument("--root", default="evals/native-runtime")
    parser.add_argument("--require", action="append", choices=sorted(PLATFORM_FILES), default=[])
    parser.add_argument("--require-real-device", action="store_true")
    parser.add_argument("--check", action="store_true", help="Run offline validation self-checks")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.check:
        errors = run_self_check()
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        return 0

    if args.probe or args.write_probe:
        payload = probe_environment()
        if args.write_probe:
            path = Path(args.write_probe).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if args.json or not args.write_probe:
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.validate:
        required = args.require or sorted(PLATFORM_FILES)
        payload = validate_root(
            Path(args.root).expanduser().resolve(),
            required,
            require_real_device=args.require_real_device,
        )
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        elif payload["ok"]:
            print("native runtime evidence verified")
        else:
            print("\n".join(payload["errors"]), file=sys.stderr)
        return 0 if payload["ok"] else 2

    parser.error("choose --probe, --write-probe, --validate, or --check")


if __name__ == "__main__":
    raise SystemExit(main())
