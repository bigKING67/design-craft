#!/usr/bin/env python3
"""Validate GitHub workflow pinning and native evidence runner contracts."""

from __future__ import annotations

import argparse
import json
import plistlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SCHEMA = "design-craft.workflow-verification.v1"
ROOT = Path(__file__).resolve().parents[1]
ACTION_PATTERN = re.compile(r"\buses:\s*[^@\s]+@([^\s#]+)")


def require_tokens(text: str, tokens: tuple[str, ...], label: str) -> list[str]:
    return [f"{label} missing {token}" for token in tokens if token not in text]


def action_pin_errors(workflow: Path, text: str) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = ACTION_PATTERN.search(line)
        if match and not re.fullmatch(r"[0-9a-f]{40}", match.group(1)):
            errors.append(f"{workflow.relative_to(ROOT)}:{line_number}: action must use a full SHA")
    return errors


def workflow_job_block(text: str, job_name: str) -> str:
    start_match = re.search(rf"(?m)^  {re.escape(job_name)}:\s*$", text)
    if start_match is None:
        return ""
    next_match = re.search(
        r"(?m)^  [A-Za-z0-9_-]+:\s*$",
        text[start_match.end() :],
    )
    if next_match is None:
        return text[start_match.start() :]
    end = start_match.end() + next_match.start()
    return text[start_match.start() : end]


def validate() -> dict:
    errors: list[str] = []
    native_workflow_path = ROOT / ".github/workflows/native-runtime.yml"
    validate_workflow_path = ROOT / ".github/workflows/validate.yml"
    dependabot_path = ROOT / ".github/dependabot.yml"
    ios_runner_path = ROOT / "scripts/native_runtime_ci_ios.sh"
    android_runner_path = ROOT / "scripts/native_runtime_ci_android.sh"
    android_common_path = ROOT / "scripts/native_runtime_android_common.sh"
    portable_validator_path = ROOT / "scripts/validate.sh"
    ios_fixture_path = ROOT / "evals/native-runtime/fixtures/ios/App.swift"

    required_paths = (
        native_workflow_path,
        validate_workflow_path,
        dependabot_path,
        ios_runner_path,
        android_runner_path,
        android_common_path,
        portable_validator_path,
        ios_fixture_path,
    )
    for path in required_paths:
        if not path.is_file():
            errors.append(f"missing workflow contract file: {path.relative_to(ROOT)}")
    if errors:
        return {"schema": SCHEMA, "root": str(ROOT), "ok": False, "errors": errors}

    native_workflow = native_workflow_path.read_text(encoding="utf-8")
    validate_workflow = validate_workflow_path.read_text(encoding="utf-8")
    dependabot = dependabot_path.read_text(encoding="utf-8")
    ios_runner = ios_runner_path.read_text(encoding="utf-8")
    android_runner = android_runner_path.read_text(encoding="utf-8")
    android_common = android_common_path.read_text(encoding="utf-8")
    portable_validator = portable_validator_path.read_text(encoding="utf-8")
    ios_fixture = ios_fixture_path.read_text(encoding="utf-8")

    errors.extend(
        require_tokens(
            native_workflow,
            (
                "native_runtime_ci_ios.sh",
                "reactivecircus/android-emulator-runner@",
                "native_runtime_ci_android.sh",
                "Enable KVM access",
                "-no-metrics",
                "concurrency:",
                "cancel-in-progress: false",
            ),
            ".github/workflows/native-runtime.yml",
        )
    )
    errors.extend(
        require_tokens(
            validate_workflow,
            (
                "DESIGN_CRAFT_NATIVE_BUILD_ONLY",
                "android-fixture-build",
                'tags: ["v*"]',
                "concurrency:",
                "cancel-in-progress: true",
                "name: lint",
                "name: contract-tests",
                "make lint",
                "make contract-tests",
            ),
            ".github/workflows/validate.yml",
        )
    )
    if validate_workflow.count("timeout-minutes:") != 5:
        errors.append(".github/workflows/validate.yml must set a timeout on all five jobs")
    for job_name in ("portable", "windows-portable"):
        block = workflow_job_block(validate_workflow, job_name)
        if "submodules: recursive" not in block or "fetch-depth: 0" not in block:
            errors.append(
                f".github/workflows/validate.yml {job_name} must fetch recursive submodules and full history"
            )
    if native_workflow.count("timeout-minutes:") != 2:
        errors.append(
            ".github/workflows/native-runtime.yml must set a timeout on both jobs"
        )
    errors.extend(
        require_tokens(
            ios_runner,
            (
                "xcrun simctl",
                "-parse-as-library",
                "-module-name DesignCraftEvidence",
                "simctl openurl",
                "live/cold deep-link interaction",
                "before_screenshot=",
                "interaction_marker=",
                "launch_log=",
                "simulator-selection.txt",
                "runtime-events.txt",
                "open-confirmation.png",
                'tap --label "Open"',
                "26a64009c09a3ae980b1f1b4b377bd2a2dd96cbbde24821935e47352cb71cc69",
            ),
            "scripts/native_runtime_ci_ios.sh",
        )
    )
    if "--confirm-runtime" in ios_runner or "--confirm-runtime" in ios_fixture:
        errors.append("iOS certification must not use a test-only --confirm-runtime path")
    if "DESIGN_CRAFT_RUNTIME_URL_RECEIVED" not in ios_fixture:
        errors.append("iOS fixture must log receipt of the real runtime URL")
    if "createDirectory" not in ios_fixture or "runtime-events.txt" not in ios_fixture:
        errors.append("iOS fixture must preserve observable URL and marker-write diagnostics")

    errors.extend(
        require_tokens(
            portable_validator,
            (
                "command -v rg",
                "grep -R -n -E",
                '"${BASH}" -n',
            ),
            "scripts/validate.sh",
        )
    )

    errors.extend(
        require_tokens(
            android_runner,
            (
                "design_craft_native_runtime_record.py",
                "native_runtime_android_common.sh",
                "before_accessibility_tree=",
                "after_accessibility_tree=",
                "after_screenshot=",
                "launch_log=",
            ),
            "scripts/native_runtime_ci_android.sh",
        )
    )
    errors.extend(
        require_tokens(
            android_common,
            ("uiautomator", "adb exec-out cat", "android:id/aerr_close"),
            "scripts/native_runtime_android_common.sh",
        )
    )
    errors.extend(
        require_tokens(
            dependabot,
            ("package-ecosystem: github-actions", "package-ecosystem: npm"),
            ".github/dependabot.yml",
        )
    )

    for workflow_path in (ROOT / ".github/workflows").glob("*.yml"):
        errors.extend(action_pin_errors(workflow_path, workflow_path.read_text(encoding="utf-8")))

    try:
        probe = json.loads(
            (ROOT / "evals/native-runtime/environment-probe.json").read_text(encoding="utf-8")
        )
        if probe.get("schema") != "design-craft.native-runtime-probe.v1":
            errors.append("native runtime environment probe schema is invalid")
        if not isinstance(probe.get("ios", {}).get("ready"), bool):
            errors.append("native runtime iOS readiness must be boolean")
        if not isinstance(probe.get("android", {}).get("ready"), bool):
            errors.append("native runtime Android readiness must be boolean")
    except Exception as exc:
        errors.append(f"native runtime environment probe is invalid: {exc}")

    try:
        plist = plistlib.loads((ROOT / "evals/native-runtime/fixtures/ios/Info.plist").read_bytes())
        if plist.get("CFBundleIdentifier") != "dev.designcraft.runtime-evidence":
            errors.append("iOS fixture bundle identifier is invalid")
        url_types = plist.get("CFBundleURLTypes", [])
        if not url_types or url_types[0].get("CFBundleTypeRole") != "Viewer":
            errors.append("iOS fixture URL type must declare the Viewer role")
        scene_manifest = plist.get("UIApplicationSceneManifest", {})
        scene_configs = scene_manifest.get("UISceneConfigurations", {})
        if scene_manifest.get("UIApplicationSupportsMultipleScenes") is not False:
            errors.append("iOS fixture must disable multiple scenes")
        if not scene_configs.get("UIWindowSceneSessionRoleApplication"):
            errors.append("iOS fixture must register the UIWindowScene application role")
    except Exception as exc:
        errors.append(f"iOS Info.plist is invalid: {exc}")

    try:
        ET.parse(ROOT / "evals/native-runtime/fixtures/android/app/src/main/AndroidManifest.xml")
    except Exception as exc:
        errors.append(f"Android fixture manifest is invalid: {exc}")

    return {
        "schema": SCHEMA,
        "root": str(ROOT),
        "workflow_count": len(list((ROOT / ".github/workflows").glob("*.yml"))),
        "ok": not errors,
        "errors": errors,
    }


def self_check() -> list[str]:
    errors: list[str] = []
    fake = ROOT / ".github/workflows/fixture.yml"
    if action_pin_errors(fake, "- uses: actions/checkout@v4") == []:
        errors.append("workflow validator did not reject an unpinned action")
    if action_pin_errors(fake, "- uses: actions/checkout@" + "a" * 40):
        errors.append("workflow validator rejected a full-SHA action pin")
    fixture = (
        "jobs:\n"
        "  portable:\n"
        "    steps:\n"
        "      - with:\n"
        "          fetch-depth: 0\n"
        "  windows-portable:\n"
        "    steps: []\n"
    )
    portable = workflow_job_block(fixture, "portable")
    windows = workflow_job_block(fixture, "windows-portable")
    if "fetch-depth: 0" not in portable or "windows-portable" in portable:
        errors.append("workflow job-block parser did not isolate the portable job")
    if "steps: []" not in windows:
        errors.append("workflow job-block parser did not isolate the final job")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.check and not args.validate:
        args.validate = True

    errors = self_check() if args.check else []
    payload = validate() if args.validate else {
        "schema": SCHEMA,
        "root": str(ROOT),
        "workflow_count": 0,
        "ok": True,
        "errors": [],
    }
    errors.extend(payload["errors"])
    payload["errors"] = errors
    payload["ok"] = not errors

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif payload["ok"]:
        print(f"workflow contracts verified: {payload['workflow_count']} workflows")
    else:
        print("\n".join(errors), file=sys.stderr)
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
