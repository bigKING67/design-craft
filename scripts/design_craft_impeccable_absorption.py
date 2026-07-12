#!/usr/bin/env python3
"""Validate the pbakaus/impeccable fusion and runtime boundary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from design_craft_absorption_common import (
    MATRIX_STATUS_LABELS,
    validate_matrix_vocabulary,
    validate_review_state,
)


SCHEMA = "design-craft.impeccable-absorption.v1"
ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "upstreams.lock.json"
MATRIX_PATH = ROOT / "docs/impeccable-absorption.md"
COMPATIBILITY_PATH = ROOT / "skills/design-craft/COMPATIBILITY.json"
DECISION_STATUSES = {
    "absorbed",
    "partial",
    "missing_high_value",
    "intentionally_rejected",
    "provenance_only",
}


COVERAGE = {
    "workflow_modes": {
        "paths": ["skills/design-craft/references/impeccable-workflow.md"],
        "terms": [
            "`shape`",
            "`craft`",
            "`critique`",
            "`audit`",
            "`polish`",
            "`harden`",
            "`adapt`",
            "`optimize`",
            "`extract`",
            "`document`",
            "`live`",
        ],
    },
    "hardening_and_performance": {
        "paths": [
            "skills/design-craft/references/impeccable-workflow.md",
            "skills/design-craft/references/engineering-quality.md",
            "skills/design-craft/references/performance-quality.md",
        ],
        "terms": [
            "Use realistic hostile data",
            "4xx/5xx/network timeout",
            "Measure or establish a baseline first",
            "Loading, empty, error",
        ],
    },
    "detector_and_evidence": {
        "paths": [
            "skills/design-craft/references/impeccable-workflow.md",
            "skills/design-craft/scripts/design_craft_detect.sh",
        ],
        "terms": [
            "upstreams/impeccable/skill/scripts/detect.mjs",
            "signals, not law",
            "DEGRADED: single-context",
            "Do not claim dual-agent",
        ],
    },
    "platform_quality": {
        "paths": [
            "skills/design-craft/references/ios-quality.md",
            "skills/design-craft/references/android-quality.md",
            "skills/design-craft/references/adaptive-quality.md",
            "skills/design-craft/scripts/design_craft_platform_scan.py",
        ],
        "terms": [
            "size classes",
            "predictive Back",
            "Shared versus platform-specific",
            "WebView/Capacitor/Cordova shells remain `web`",
        ],
    },
    "design_system_corrections": {
        "paths": [
            "skills/design-craft/references/design-system-contract.md",
            "skills/design-craft/references/foundational-visual-principles.md",
        ],
        "terms": [
            "component state matrix",
            "focus-visible",
            "Proximity",
            "Alignment",
        ],
    },
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> dict:
    errors: list[str] = []
    matrix_relative = MATRIX_PATH.relative_to(ROOT).as_posix()
    lock = read_json(LOCK_PATH)
    meta = lock.get("upstreams", {}).get("impeccable", {})
    upstream = ROOT / meta.get("path", "upstreams/impeccable")
    inventory = meta.get("skill_inventory", {})
    state, state_errors = validate_review_state("impeccable", meta, upstream)
    errors.extend(state_errors)

    main_skill = str(inventory.get("main_skill", ""))
    expected_commands = inventory.get("commands", [])
    detector_path = str(inventory.get("detector", ""))
    platform_references = inventory.get("platform_references", [])
    rejected_paths = inventory.get("intentionally_rejected_paths", [])
    command_decisions = inventory.get("command_decisions", {})

    if not main_skill or not (upstream / main_skill).is_file():
        errors.append(f"impeccable main Skill is missing: {main_skill or 'unavailable'}")
    observed_commands = sorted(
        path.stem
        for path in (upstream / "site/content/skills").glob("*.md")
        if path.is_file()
    )
    if observed_commands != sorted(expected_commands):
        errors.append(
            "impeccable command inventory drift: "
            f"expected {sorted(expected_commands)}, observed {observed_commands}"
        )
    if set(command_decisions) != set(expected_commands):
        errors.append("command_decisions must cover every impeccable command exactly once")
    for command, decision in command_decisions.items():
        if decision not in DECISION_STATUSES:
            errors.append(f"/{command}: invalid absorption decision {decision!r}")
        if decision == "missing_high_value":
            errors.append(f"/{command}: missing_high_value blocks absorption completeness")

    for label, relative in (
        ("detector", detector_path),
        *(("platform reference", str(path)) for path in platform_references),
        *(("rejected runtime/package boundary", str(path)) for path in rejected_paths),
    ):
        if not relative or not (upstream / relative).is_file():
            errors.append(f"impeccable {label} path is missing: {relative or 'unavailable'}")

    if meta.get("coverage_contract") != SCHEMA:
        errors.append(f"coverage_contract must be {SCHEMA}")
    if meta.get("coverage_matrix") != matrix_relative:
        errors.append(f"coverage_matrix must be {matrix_relative}")
    compatibility = read_json(COMPATIBILITY_PATH)
    contract = compatibility.get("maintenance_contracts", {}).get(
        "impeccable_absorption"
    )
    if contract != SCHEMA:
        errors.append(f"COMPATIBILITY.json must declare {SCHEMA}")

    matrix_text = MATRIX_PATH.read_text(encoding="utf-8") if MATRIX_PATH.is_file() else ""
    errors.extend(validate_matrix_vocabulary(matrix_text))
    for command in expected_commands:
        if f"`/{command}`" not in matrix_text:
            errors.append(f"absorption matrix is missing command: /{command}")
    for term in (
        "live-server",
        "manual-edit",
        "provider",
        "package",
        "GitHub sheriff",
        "browser67",
    ):
        if term.casefold() not in matrix_text.casefold():
            errors.append(f"absorption matrix is missing runtime boundary term: {term}")

    coverage_payload = {}
    for capability, spec in COVERAGE.items():
        combined = ""
        missing_paths = []
        for relative in spec["paths"]:
            path = ROOT / relative
            if not path.is_file():
                missing_paths.append(relative)
                continue
            combined += "\n" + path.read_text(encoding="utf-8")
        normalized = combined.casefold()
        missing_terms = [
            term for term in spec["terms"] if term.casefold() not in normalized
        ]
        if missing_paths:
            errors.append(f"{capability}: missing local coverage paths: {missing_paths}")
        if missing_terms:
            errors.append(f"{capability}: missing local coverage terms: {missing_terms}")
        coverage_payload[capability] = {
            "paths": spec["paths"],
            "missing_paths": missing_paths,
            "missing_terms": missing_terms,
        }

    detector_wrapper = ROOT / "skills/design-craft/scripts/design_craft_detect.sh"
    detector_text = detector_wrapper.read_text(encoding="utf-8") if detector_wrapper.is_file() else ""
    if detector_path not in detector_text:
        errors.append("design_craft_detect.sh must retain the locked upstream detector path")

    return {
        "schema": SCHEMA,
        "ok": not errors,
        "upstream": {
            **state,
            "main_skill": main_skill,
            "command_count": len(observed_commands),
            "commands": observed_commands,
            "detector": detector_path,
            "platform_references": platform_references,
            "intentionally_rejected_paths": rejected_paths,
        },
        "coverage": coverage_payload,
        "matrix": matrix_relative,
        "status_vocabulary": list(MATRIX_STATUS_LABELS),
        "errors": errors,
    }


def self_check() -> None:
    if set(COVERAGE) != {
        "workflow_modes",
        "hardening_and_performance",
        "detector_and_evidence",
        "platform_quality",
        "design_system_corrections",
    }:
        raise RuntimeError("internal impeccable coverage map drifted")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.check:
        self_check()
    payload = validate()
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif payload["ok"]:
        upstream = payload["upstream"]
        print(
            "impeccable absorption verified: "
            f"commands={upstream['command_count']} "
            f"cumulative={upstream['cumulative_status']} "
            f"latest={upstream['latest_range_status']}"
        )
    else:
        print("\n".join(payload["errors"]), file=sys.stderr)
    return 0 if payload["ok"] or not args.strict else 2


if __name__ == "__main__":
    raise SystemExit(main())
