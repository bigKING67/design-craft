#!/usr/bin/env python3
"""Validate the five-skill emilkowalski/skills absorption contract."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SCHEMA = "design-craft.emil-absorption.v1"
ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "upstreams.lock.json"
MATRIX_PATH = ROOT / "docs/emilkowalski-absorption.md"
COMPATIBILITY_PATH = ROOT / "skills/design-craft/COMPATIBILITY.json"


COVERAGE = {
    "emil-design-eng": {
        "status": "absorbed",
        "paths": [
            "skills/design-craft/references/motion-quality.md",
            "skills/design-craft/references/motion-patterns.md",
            "skills/design-craft/references/engineering-quality.md",
            "skills/design-craft/references/design-system-contract.md",
        ],
        "terms": [
            "@starting-style",
            "skip the remaining delay and entrance motion",
            "visibilitychange",
            "font-optical-sizing",
            "scale(0.97)",
        ],
    },
    "apple-design": {
        "status": "absorbed",
        "paths": [
            "skills/design-craft/references/interaction-physics.md",
            "skills/design-craft/references/product-design-principles.md",
            "skills/design-craft/references/design-system-contract.md",
        ],
        "terms": [
            "presentation value",
            "projected endpoint",
            "rubber-band",
            "font-optical-sizing",
            "causal state change",
        ],
    },
    "review-animations": {
        "status": "absorbed",
        "paths": [
            "skills/design-craft/references/motion-quality.md",
            "skills/design-craft/references/motion-audit-planning.md",
            "skills/design-craft/scripts/design_craft_detect.sh",
        ],
        "terms": [
            "| Before | After | Why |",
            "transition: all",
            "Static source",
            "Block",
        ],
    },
    "improve-animations": {
        "status": "absorbed",
        "paths": [
            "skills/design-craft/references/motion-audit-planning.md",
            "skills/design-craft/templates/motion-plan/plan.md",
            "skills/design-craft/scripts/design_craft_motion_plan.py",
        ],
        "terms": [
            "Phase 1: motion recon",
            "user impact x frequency x confidence / implementation cost",
            "reconcile",
            "design-craft.motion-plan-scaffold.v1",
        ],
    },
    "animation-vocabulary": {
        "status": "absorbed",
        "paths": ["skills/design-craft/references/motion-vocabulary.md"],
        "terms": [
            "Perceptual duration",
            "Idle animation",
            "Anticipation",
            "Follow-through",
            "Squash and stretch",
        ],
    },
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_head(path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def validate() -> dict:
    errors: list[str] = []
    lock = read_json(LOCK_PATH)
    meta = lock.get("upstreams", {}).get("emilkowalski-skills", {})
    inventory = meta.get("skill_inventory", {})
    upstream = ROOT / meta.get("path", "upstreams/emilkowalski-skills")

    expected_skills = inventory.get("skills", [])
    expected_auxiliary = inventory.get("auxiliary_markdown", [])
    observed_skills = sorted(
        path.parent.name
        for path in (upstream / "skills").glob("*/SKILL.md")
        if path.is_file()
    )
    observed_auxiliary = sorted(
        path.relative_to(upstream).as_posix()
        for path in (upstream / "skills").rglob("*.md")
        if path.name != "SKILL.md"
    )
    observed_non_markdown = sorted(
        path.relative_to(upstream).as_posix()
        for path in (upstream / "skills").rglob("*")
        if path.is_file() and path.suffix.lower() != ".md"
    )

    if observed_skills != sorted(expected_skills):
        errors.append(
            "upstream Skill inventory drift: "
            f"expected {sorted(expected_skills)}, observed {observed_skills}"
        )
    if observed_auxiliary != sorted(expected_auxiliary):
        errors.append(
            "upstream auxiliary Markdown inventory drift: "
            f"expected {sorted(expected_auxiliary)}, observed {observed_auxiliary}"
        )
    if observed_non_markdown != sorted(inventory.get("non_markdown_files", [])):
        errors.append(
            "upstream non-Markdown inventory drift: "
            f"observed {observed_non_markdown}"
        )

    observed_commit = git_head(upstream)
    if observed_commit != meta.get("commit"):
        errors.append(
            f"upstream checkout {observed_commit or 'unavailable'} does not match lock {meta.get('commit')}"
        )
    if meta.get("reviewed_commit") != meta.get("commit"):
        errors.append("reviewed_commit must match the checked compatibility commit")
    if meta.get("coverage_contract") != SCHEMA:
        errors.append(f"coverage_contract must be {SCHEMA}")
    if meta.get("coverage_matrix") != str(MATRIX_PATH.relative_to(ROOT)):
        errors.append(
            f"coverage_matrix must be {MATRIX_PATH.relative_to(ROOT)}"
        )

    compatibility = read_json(COMPATIBILITY_PATH)
    contract = compatibility.get("maintenance_contracts", {}).get("emil_absorption")
    if contract != SCHEMA:
        errors.append(f"COMPATIBILITY.json must declare {SCHEMA}")

    matrix_text = MATRIX_PATH.read_text(encoding="utf-8") if MATRIX_PATH.is_file() else ""
    for label in (
        "absorbed",
        "partial",
        "missing-high-value",
        "intentionally-rejected",
        "provenance-only",
    ):
        if f"`{label}`" not in matrix_text:
            errors.append(f"absorption matrix is missing status vocabulary: {label}")

    coverage_payload = {}
    for skill, spec in COVERAGE.items():
        if skill not in expected_skills:
            errors.append(f"coverage map contains unexpected Skill: {skill}")
        if f"`{skill}`" not in matrix_text:
            errors.append(f"absorption matrix is missing Skill section: {skill}")
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
            errors.append(f"{skill}: missing local coverage paths: {missing_paths}")
        if missing_terms:
            errors.append(f"{skill}: missing local coverage terms: {missing_terms}")
        coverage_payload[skill] = {
            "status": spec["status"],
            "paths": spec["paths"],
            "missing_paths": missing_paths,
            "missing_terms": missing_terms,
        }

    if set(COVERAGE) != set(expected_skills):
        errors.append(
            "coverage map must match the five locked Skill entrypoints exactly"
        )

    return {
        "schema": SCHEMA,
        "ok": not errors,
        "upstream": {
            "commit": observed_commit,
            "locked_commit": meta.get("commit"),
            "skill_count": len(observed_skills),
            "skills": observed_skills,
            "auxiliary_markdown_count": len(observed_auxiliary),
            "auxiliary_markdown": observed_auxiliary,
            "non_markdown_file_count": len(observed_non_markdown),
            "non_markdown_files": observed_non_markdown,
        },
        "coverage": coverage_payload,
        "matrix": str(MATRIX_PATH.relative_to(ROOT)),
        "errors": errors,
    }


def self_check() -> None:
    if set(COVERAGE) != {
        "emil-design-eng",
        "apple-design",
        "review-animations",
        "improve-animations",
        "animation-vocabulary",
    }:
        raise RuntimeError("internal five-Skill coverage map drifted")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Run internal contract checks.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on validation errors.")
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
            "Emil absorption verified: "
            f"skills={upstream['skill_count']} "
            f"auxiliary_markdown={upstream['auxiliary_markdown_count']} "
            f"non_markdown={upstream['non_markdown_file_count']}"
        )
    else:
        print("\n".join(payload["errors"]), file=sys.stderr)
    return 0 if payload["ok"] or not args.strict else 2


if __name__ == "__main__":
    raise SystemExit(main())
