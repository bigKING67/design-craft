#!/usr/bin/env python3
"""Shared schemas and validation helpers for comparative benchmark evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from design_craft_evidence_common import files_sha256


ROOT = Path(__file__).resolve().parents[1]
VARIANTS_SCHEMA = "design-craft.comparative-variants.v1"
SCORECARD_SCHEMA = "design-craft.comparative-scorecard.v1"
RUN_SCHEMA = "design-craft.comparative-run.v2"
BLIND_MAP_SCHEMA = "design-craft.comparative-blind-map.v2"
JUDGE_RUN_SCHEMA = "design-craft.comparative-judge-run.v1"
RESULT_SCHEMA = "design-craft.comparative-result.v2"
REQUIRED_VARIANTS = ("baseline", "emil", "design-craft")
BLIND_LABELS = ("A", "B", "C")
CONTRACT_FILES = (
    "scripts/design_craft_comparative_common.py",
    "scripts/design_craft_comparative_run.py",
    "scripts/design_craft_comparative_blind.py",
    "scripts/design_craft_comparative_judge.py",
    "scripts/design_craft_comparative_record.py",
    "scripts/design_craft_comparative_validate.py",
    "scripts/design_craft_cross_agent_run.py",
    "scripts/design_craft_evidence_common.py",
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def contract_sha256() -> str:
    return files_sha256(ROOT, CONTRACT_FILES)


def load_scorecard(case_dir: Path) -> tuple[dict[str, int], list[str]]:
    path = case_dir / "scorecard.json"
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"{path}: invalid scorecard JSON: {exc}"]
    if payload.get("schema") != SCORECARD_SCHEMA:
        errors.append(f"{path}: schema must be {SCORECARD_SCHEMA}")
    criteria = payload.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        return {}, [*errors, f"{path}: criteria must be a non-empty array"]
    weights: dict[str, int] = {}
    for index, item in enumerate(criteria):
        if not isinstance(item, dict):
            errors.append(f"{path}: criterion {index} must be an object")
            continue
        criterion_id = item.get("id")
        weight = item.get("weight")
        if not isinstance(criterion_id, str) or not criterion_id.replace("_", "").isalnum():
            errors.append(f"{path}: criterion {index} has an invalid id")
            continue
        if criterion_id in weights:
            errors.append(f"{path}: duplicate criterion id {criterion_id}")
            continue
        if not isinstance(weight, int) or isinstance(weight, bool) or weight <= 0:
            errors.append(f"{path}: criterion {criterion_id} weight must be positive")
            continue
        if not isinstance(item.get("label"), str) or not item["label"].strip():
            errors.append(f"{path}: criterion {criterion_id} label is required")
        if not isinstance(item.get("full_credit"), str) or len(item["full_credit"].strip()) < 12:
            errors.append(f"{path}: criterion {criterion_id} full_credit is too sparse")
        weights[criterion_id] = weight
    if sum(weights.values()) != 100:
        errors.append(f"{path}: criterion weights must total 100")
    if payload.get("total") != 100:
        errors.append(f"{path}: total must be 100")
    return weights, errors


def validate_judgment_schema(case_dir: Path, weights: dict[str, int]) -> list[str]:
    path = case_dir / "judgment.schema.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: invalid judgment schema: {exc}"]
    try:
        criteria = payload["properties"]["results"]["items"]["properties"]["criteria"]
        properties = criteria["properties"]
        required = set(criteria["required"])
    except (KeyError, TypeError) as exc:
        return [f"{path}: missing criteria schema structure: {exc}"]
    errors: list[str] = []
    if required != set(weights) or set(properties) != set(weights):
        errors.append(f"{path}: criteria properties must match scorecard.json")
    for criterion, maximum in weights.items():
        definition = properties.get(criterion, {})
        if definition.get("type") != "integer" or definition.get("minimum") != 0:
            errors.append(f"{path}: {criterion} must be an integer with minimum 0")
        if definition.get("maximum") != maximum:
            errors.append(f"{path}: {criterion} maximum must be {maximum}")
    return errors


def parse_json_output(raw: str) -> dict:
    stripped = raw.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        if start < 0:
            raise
        payload, end = json.JSONDecoder().raw_decode(stripped[start:])
        if stripped[start + end :].strip():
            raise ValueError("judge output contains trailing non-JSON content")
    if not isinstance(payload, dict):
        raise ValueError("judge output must be a JSON object")
    return payload


def validate_judgment(payload: dict, weights: dict[str, int]) -> list[str]:
    errors: list[str] = []
    if set(payload) != {"results", "winner", "rationale"}:
        errors.append("judgment must contain only results, winner, and rationale")
    results = payload.get("results")
    if not isinstance(results, list) or len(results) != 3:
        return [*errors, "judgment results must contain exactly three entries"]
    labels: list[str] = []
    totals: dict[str, int] = {}
    for index, item in enumerate(results):
        if not isinstance(item, dict):
            errors.append(f"judgment result {index} must be an object")
            continue
        if set(item) != {"label", "criteria", "total", "summary"}:
            errors.append(f"judgment result {index} has unsupported fields")
        label = item.get("label")
        if label not in BLIND_LABELS:
            errors.append(f"judgment result {index} label must be A, B, or C")
            continue
        labels.append(label)
        criteria = item.get("criteria")
        if not isinstance(criteria, dict) or set(criteria) != set(weights):
            errors.append(f"judgment {label} criteria must match scorecard.json")
            continue
        computed = 0
        for criterion, maximum in weights.items():
            value = criteria.get(criterion)
            if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= maximum:
                errors.append(f"judgment {label}.{criterion} must be 0..{maximum}")
            else:
                computed += value
        if item.get("total") != computed:
            errors.append(f"judgment {label} total must equal criterion points")
        totals[label] = computed
        summary = item.get("summary")
        if not isinstance(summary, str) or len(summary.strip()) < 20:
            errors.append(f"judgment {label} summary must contain at least 20 characters")
    if sorted(labels) != list(BLIND_LABELS):
        errors.append("judgment labels must contain A, B, and C exactly once")
    winner = payload.get("winner")
    if winner not in BLIND_LABELS:
        errors.append("judgment winner must be A, B, or C")
    elif totals and winner in totals and totals[winner] != max(totals.values()):
        errors.append("judgment winner must have the highest computed score")
    rationale = payload.get("rationale")
    if not isinstance(rationale, str) or len(rationale.strip()) < 40:
        errors.append("judgment rationale must contain at least 40 characters")
    return errors
