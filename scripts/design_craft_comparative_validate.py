#!/usr/bin/env python3
"""Validate comparative ablation definitions, isolated runs, blind judge, and result."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from design_craft_comparative_common import (
    BLIND_LABELS,
    BLIND_MAP_SCHEMA,
    JUDGE_RUN_SCHEMA,
    RESULT_SCHEMA,
    RUN_SCHEMA,
    SOURCE_BRAND_PATTERN,
    VARIANTS_SCHEMA,
    contract_sha256,
    load_scorecard,
    sha256_file,
    validate_judgment,
    validate_judgment_schema,
    variant_ids,
)
from design_craft_evidence_common import tree_sha256


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DEFINITION_FILES = (
    "prompt.md",
    "variants.json",
    "scorecard.md",
    "scorecard.json",
    "expected-findings.md",
    "judgment.schema.json",
)
REQUIRED_OBSERVED_FILES = (
    "blind-packet.md",
    "blind-map.json",
    "judge-output.raw.txt",
    "blind-judgment.json",
    "run.judge.json",
    "comparison.json",
)


def markdown_weight_total(path: Path) -> int:
    total = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) >= 2 and cells[1].isdigit():
            total += int(cells[1])
    return total


def load_variants(case_dir: Path) -> tuple[dict, list[str]]:
    path = case_dir / "variants.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"{path}: invalid variants JSON: {exc}"]
    errors: list[str] = []
    if payload.get("schema") != VARIANTS_SCHEMA:
        errors.append(f"{path}: schema must be {VARIANTS_SCHEMA}")
    if payload.get("host") != "pi":
        errors.append(f"{path}: comparative host must be pi")
    items = payload.get("variants")
    try:
        required = variant_ids(payload)
    except ValueError as exc:
        errors.append(f"{path}: {exc}")
        required = ("baseline", "invalid-focused", "design-craft")
    ids = [item.get("id") for item in items if isinstance(item, dict)] if isinstance(items, list) else []
    if sorted(ids) != sorted(required) or len(ids) != len(required):
        errors.append(f"{path}: variants must be {list(required)} exactly once")
    for item in items if isinstance(items, list) else []:
        paths = item.get("skill_paths")
        if not isinstance(paths, list) or not all(isinstance(value, str) for value in paths):
            errors.append(f"{path}: variant {item.get('id')} skill_paths must be an array")
            continue
        if item.get("id") == "baseline" and paths:
            errors.append(f"{path}: baseline must not load skills")
        if item.get("id") != "baseline" and not paths:
            errors.append(f"{path}: variant {item.get('id')} must load at least one skill")
        for relative in paths:
            if Path(relative).is_absolute() or ".." in Path(relative).parts:
                errors.append(f"{path}: variant skill path must stay repository-relative: {relative}")
            elif not ROOT.joinpath(relative, "SKILL.md").is_file():
                errors.append(f"{path}: missing variant skill {relative}")
    return payload, errors


def validate_definition(case_dir: Path) -> tuple[dict, dict[str, int], list[str]]:
    errors: list[str] = []
    for name in REQUIRED_DEFINITION_FILES:
        if not case_dir.joinpath(name).is_file():
            errors.append(f"{case_dir}: missing {name}")
    if errors:
        return {}, {}, errors
    variants, variant_errors = load_variants(case_dir)
    errors.extend(variant_errors)
    weights, scorecard_errors = load_scorecard(case_dir)
    errors.extend(scorecard_errors)
    if markdown_weight_total(case_dir / "scorecard.md") != 100:
        errors.append(f"{case_dir}/scorecard.md: visible criterion weights must total 100")
    if weights:
        errors.extend(validate_judgment_schema(case_dir, weights))
    prompt = (case_dir / "prompt.md").read_text(encoding="utf-8").lower()
    if "do not name" not in prompt or "skill" not in prompt:
        errors.append(f"{case_dir}/prompt.md: must prohibit skill/source brand disclosure")
    return variants, weights, errors


def validate_run(
    case_dir: Path,
    variant_id: str,
    variant: dict,
    *,
    prompt_hash: str,
) -> tuple[dict, list[str]]:
    output = case_dir / f"output.{variant_id}.md"
    manifest = case_dir / f"run.{variant_id}.json"
    errors: list[str] = []
    if not output.is_file() or not manifest.is_file():
        return {}, [f"{case_dir}: incomplete observed variant {variant_id}"]
    output_text = output.read_text(encoding="utf-8")
    if len(output_text.strip()) < 200:
        errors.append(f"{output}: observed output is too sparse")
    match = SOURCE_BRAND_PATTERN.search(output_text)
    if match:
        errors.append(f"{output}: reveals a skill/source brand near {match.group(0)!r}")
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, [*errors, f"{manifest}: {exc}"]
    if payload.get("schema") != RUN_SCHEMA:
        errors.append(f"{manifest}: schema must be {RUN_SCHEMA}")
    if payload.get("variant") != variant_id or payload.get("host") != "pi":
        errors.append(f"{manifest}: variant/host mismatch")
    if payload.get("prompt_sha256") != prompt_hash:
        errors.append(f"{manifest}: prompt hash mismatch")
    if payload.get("output_path") != output.name or payload.get("output_sha256") != sha256_file(output):
        errors.append(f"{manifest}: output path/hash mismatch")
    for key in (
        "host_version",
        "model",
        "model_observation",
        "thinking",
        "thinking_observation",
        "runner_os",
        "command",
        "cwd",
    ):
        if not isinstance(payload.get(key), str) or not payload[key].strip():
            errors.append(f"{manifest}: {key} must be non-empty")
    if payload.get("model_observation") != "requested_by_cli":
        errors.append(f"{manifest}: model_observation must be requested_by_cli")
    if payload.get("thinking_observation") != "requested_by_cli":
        errors.append(f"{manifest}: thinking_observation must be requested_by_cli")
    if payload.get("contract_sha256") != contract_sha256():
        errors.append(f"{manifest}: comparative contract hash is stale")
    if payload.get("skill_install_mode") != "isolated_project_copy":
        errors.append(f"{manifest}: skill_install_mode must be isolated_project_copy")
    if payload.get("workspace_kind") != "repo_external_isolated_project":
        errors.append(f"{manifest}: workspace_kind must be repo_external_isolated_project")
    if payload.get("returncode") != 0 or payload.get("worktree_unchanged") is not True:
        errors.append(f"{manifest}: run must be successful and non-mutating")
    before_hash = payload.get("worktree_before_sha256")
    if not re.fullmatch(r"[0-9a-f]{64}", str(before_hash or "")):
        errors.append(f"{manifest}: worktree_before_sha256 is invalid")
    if before_hash != payload.get("worktree_after_sha256"):
        errors.append(f"{manifest}: worktree fingerprints must match")
    for key in ("command", "cwd"):
        if re.search(r"(?:/Users/|/home/|[A-Za-z]:[\\/]Users[\\/])", str(payload.get(key, ""))):
            errors.append(f"{manifest}: {key} leaks a local user path")
    expected_trees = {
        str(relative): tree_sha256(ROOT / str(relative))
        for relative in variant.get("skill_paths", [])
    }
    if payload.get("skill_trees") != expected_trees:
        errors.append(f"{manifest}: skill_trees must match current variant sources")
    installed_paths = payload.get("installed_skill_paths")
    if not isinstance(installed_paths, dict) or set(installed_paths) != set(expected_trees):
        errors.append(f"{manifest}: installed_skill_paths must cover every variant skill")
    elif any(not str(value).startswith("$VARIANT_WORKSPACE/") for value in installed_paths.values()):
        errors.append(f"{manifest}: installed skill paths must be redacted workspace paths")
    return payload, errors


def validate_judge_evidence(
    case_dir: Path, weights: dict[str, int]
) -> tuple[dict, dict, list[str]]:
    manifest_path = case_dir / "run.judge.json"
    judgment_path = case_dir / "blind-judgment.json"
    raw_path = case_dir / "judge-output.raw.txt"
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        judgment = json.loads(judgment_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, {}, [f"{case_dir}: invalid judge evidence: {exc}"]
    if manifest.get("schema") != JUDGE_RUN_SCHEMA:
        errors.append(f"{manifest_path}: schema must be {JUDGE_RUN_SCHEMA}")
    if manifest.get("host") == "pi":
        errors.append(f"{manifest_path}: judge must be independent from Pi")
    if manifest.get("packet_sha256") != sha256_file(case_dir / "blind-packet.md"):
        errors.append(f"{manifest_path}: packet hash mismatch")
    if manifest.get("judgment_schema_sha256") != sha256_file(case_dir / "judgment.schema.json"):
        errors.append(f"{manifest_path}: judgment schema hash mismatch")
    if manifest.get("judgment_path") != judgment_path.name or manifest.get("judgment_sha256") != sha256_file(judgment_path):
        errors.append(f"{manifest_path}: judgment path/hash mismatch")
    if not raw_path.is_file() or manifest.get("raw_output_path") != raw_path.name or manifest.get("raw_output_sha256") != sha256_file(raw_path):
        errors.append(f"{manifest_path}: raw judge output path/hash mismatch")
    if manifest.get("workspace_kind") != "repo_external_empty_project":
        errors.append(f"{manifest_path}: judge workspace must be repo-external and empty")
    if manifest.get("returncode") != 0 or manifest.get("worktree_unchanged") is not True:
        errors.append(f"{manifest_path}: judge run must be successful and non-mutating")
    if manifest.get("worktree_before_sha256") != manifest.get("worktree_after_sha256"):
        errors.append(f"{manifest_path}: judge worktree fingerprints must match")
    for key in (
        "host_version",
        "model",
        "model_observation",
        "reasoning_profile",
        "reasoning_observation",
        "runner_os",
        "command",
        "cwd",
    ):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            errors.append(f"{manifest_path}: {key} must be non-empty")
    errors.extend(f"{judgment_path}: {item}" for item in validate_judgment(judgment, weights))
    return manifest, judgment, errors


def validate_blind_map(
    case_dir: Path, required_variants: tuple[str, str, str]
) -> tuple[dict, list[str]]:
    path = case_dir / "blind-map.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"{path}: {exc}"]
    errors: list[str] = []
    if payload.get("schema") != BLIND_MAP_SCHEMA:
        errors.append(f"{path}: schema must be {BLIND_MAP_SCHEMA}")
    if payload.get("case_id") != case_dir.name:
        errors.append(f"{path}: case_id mismatch")
    if payload.get("focused_variant") != required_variants[1]:
        errors.append(f"{path}: focused_variant mismatch")
    hashes = {
        "prompt_sha256": "prompt.md",
        "scorecard_sha256": "scorecard.md",
        "scorecard_json_sha256": "scorecard.json",
        "judgment_schema_sha256": "judgment.schema.json",
        "packet_sha256": "blind-packet.md",
    }
    for field, name in hashes.items():
        target = case_dir / name
        if not target.is_file() or payload.get(field) != sha256_file(target):
            errors.append(f"{path}: {field} mismatch")
    outputs = payload.get("outputs")
    if not isinstance(outputs, dict) or set(outputs) != set(BLIND_LABELS):
        errors.append(f"{path}: outputs must contain A, B, and C")
    else:
        variants = set()
        for label, item in outputs.items():
            if not isinstance(item, dict):
                errors.append(f"{path}: output {label} must be an object")
                continue
            variant = item.get("variant")
            variants.add(variant)
            for field, file_field in (("sha256", "path"), ("run_sha256", "run_path")):
                target = case_dir / str(item.get(file_field, ""))
                if not target.is_file() or item.get(field) != sha256_file(target):
                    errors.append(f"{path}: output {label} {field} mismatch")
        if variants != set(required_variants):
            errors.append(f"{path}: blind labels must map every variant exactly once")
    return payload, errors


def validate_result(
    case_dir: Path,
    *,
    blind_map: dict,
    judge_manifest: dict,
    judgment: dict,
    runs: dict[str, dict],
    required_variants: tuple[str, str, str],
) -> list[str]:
    path = case_dir / "comparison.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: {exc}"]
    errors: list[str] = []
    if payload.get("schema") != RESULT_SCHEMA or payload.get("case_id") != case_dir.name:
        errors.append(f"{path}: schema/case_id mismatch")
    if payload.get("focused_variant") != required_variants[1]:
        errors.append(f"{path}: focused_variant mismatch")
    hashes = {
        "prompt_sha256": "prompt.md",
        "scorecard_sha256": "scorecard.md",
        "scorecard_json_sha256": "scorecard.json",
        "judgment_schema_sha256": "judgment.schema.json",
        "blind_map_sha256": "blind-map.json",
        "blind_packet_sha256": "blind-packet.md",
        "judgment_sha256": "blind-judgment.json",
    }
    for field, name in hashes.items():
        if payload.get(field) != sha256_file(case_dir / name):
            errors.append(f"{path}: {field} mismatch")
    judge = payload.get("judge")
    if not isinstance(judge, dict):
        errors.append(f"{path}: judge must be an object")
    else:
        expected_judge = {
            "host": judge_manifest.get("host"),
            "version": judge_manifest.get("host_version"),
            "model": judge_manifest.get("model"),
            "model_observation": judge_manifest.get("model_observation"),
            "reasoning": judge_manifest.get("reasoning_profile"),
            "reasoning_observation": judge_manifest.get("reasoning_observation"),
            "runner_os": judge_manifest.get("runner_os"),
            "run_path": "run.judge.json",
            "run_sha256": sha256_file(case_dir / "run.judge.json"),
            "raw_output_path": "judge-output.raw.txt",
            "raw_output_sha256": sha256_file(case_dir / "judge-output.raw.txt"),
        }
        if judge != expected_judge:
            errors.append(f"{path}: judge metadata must derive from run.judge.json")
    results = payload.get("results")
    if not isinstance(results, dict) or set(results) != set(required_variants):
        errors.append(f"{path}: results must cover every variant")
    else:
        scores = {
            variant: item.get("score") if isinstance(item, dict) else None
            for variant, item in results.items()
        }
        if not all(isinstance(value, int) and not isinstance(value, bool) for value in scores.values()):
            errors.append(f"{path}: every variant score must be an integer")
        elif not (
            all(
                scores["design-craft"] > scores[variant]
                for variant in required_variants
                if variant != "design-craft"
            )
            and payload.get("winner") == "design-craft"
        ):
            errors.append(f"{path}: certification requires design-craft to win the blind ablation")
    if payload.get("rationale") != judgment.get("rationale"):
        errors.append(f"{path}: rationale must match the admitted judgment")
    variant_runs = payload.get("variant_runs")
    if not isinstance(variant_runs, dict) or set(variant_runs) != set(required_variants):
        errors.append(f"{path}: variant_runs must cover every variant")
    else:
        for variant, run_payload in runs.items():
            expected = {
                "run_path": f"run.{variant}.json",
                "run_sha256": sha256_file(case_dir / f"run.{variant}.json"),
                "output_path": f"output.{variant}.md",
                "output_sha256": sha256_file(case_dir / f"output.{variant}.md"),
                "host": run_payload.get("host"),
                "host_version": run_payload.get("host_version"),
                "model": run_payload.get("model"),
                "thinking": run_payload.get("thinking"),
                "skill_trees": run_payload.get("skill_trees"),
                "contract_sha256": run_payload.get("contract_sha256"),
            }
            if variant_runs.get(variant) != expected:
                errors.append(f"{path}: variant_runs.{variant} is not bound to current evidence")
    label_map = {
        label: item.get("variant")
        for label, item in blind_map.get("outputs", {}).items()
        if isinstance(item, dict)
    }
    if label_map.get(judgment.get("winner")) != payload.get("winner"):
        errors.append(f"{path}: unblinded winner does not match the judgment")
    return errors


def validate_case(case_dir: Path, *, require_observed: bool) -> list[str]:
    variants, weights, errors = validate_definition(case_dir)
    if errors:
        return errors
    try:
        required_variants = variant_ids(variants)
    except ValueError as exc:
        return [f"{case_dir}/variants.json: {exc}"]
    observed_any = any(case_dir.glob("output.*.md")) or any(
        case_dir.glob("run.*.json")
    ) or any(case_dir.joinpath(name).exists() for name in REQUIRED_OBSERVED_FILES)
    if not require_observed and not observed_any:
        return []
    prompt_hash = sha256_file(case_dir / "prompt.md")
    variant_map = {
        item.get("id"): item
        for item in variants.get("variants", [])
        if isinstance(item, dict)
    }
    runs: dict[str, dict] = {}
    for variant_id in required_variants:
        payload, run_errors = validate_run(
            case_dir,
            variant_id,
            variant_map.get(variant_id, {}),
            prompt_hash=prompt_hash,
        )
        if payload:
            runs[variant_id] = payload
        errors.extend(run_errors)
    for name in REQUIRED_OBSERVED_FILES:
        if not case_dir.joinpath(name).is_file():
            errors.append(f"{case_dir}: missing observed comparative artifact {name}")
    if errors:
        return errors
    blind_map, map_errors = validate_blind_map(case_dir, required_variants)
    errors.extend(map_errors)
    judge_manifest, judgment, judge_errors = validate_judge_evidence(case_dir, weights)
    errors.extend(judge_errors)
    if not errors:
        errors.extend(
            validate_result(
                case_dir,
                blind_map=blind_map,
                judge_manifest=judge_manifest,
                judgment=judgment,
                runs=runs,
                required_variants=required_variants,
            )
        )
    return errors


def active_cases(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and not path.name.startswith("_")
    ) if root.is_dir() else []


def copy_definition_fixture(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True)
    for name in REQUIRED_DEFINITION_FILES:
        shutil.copy2(source / name, destination / name)


def run_self_check() -> list[str]:
    errors: list[str] = []
    source = ROOT / "evals/comparative/emil-motion-ablation"
    if validate_definition(source)[2]:
        errors.append("comparative self-check source definition is invalid")
    with tempfile.TemporaryDirectory(prefix="design-craft-comparative-validate-") as raw:
        case = Path(raw) / "invalid-case"
        copy_definition_fixture(source, case)
        variants = json.loads((case / "variants.json").read_text(encoding="utf-8"))
        variants["variants"] = []
        (case / "variants.json").write_text(json.dumps(variants), encoding="utf-8")
        if not validate_definition(case)[2]:
            errors.append("comparative self-check accepted an empty variant set")
        shutil.copy2(source / "variants.json", case / "variants.json")
        scorecard = json.loads((case / "scorecard.json").read_text(encoding="utf-8"))
        scorecard["criteria"][0]["weight"] -= 1
        (case / "scorecard.json").write_text(json.dumps(scorecard), encoding="utf-8")
        if not validate_definition(case)[2]:
            errors.append("comparative self-check accepted a non-100 scorecard")

    with tempfile.TemporaryDirectory(prefix="design-craft-comparative-e2e-") as raw:
        case = Path(raw) / source.name
        copy_definition_fixture(source, case)
        variants, definition_errors = load_variants(case)
        weights, scorecard_errors = load_scorecard(case)
        if definition_errors or scorecard_errors:
            errors.append("comparative e2e self-check could not load its fixture")
            return errors
        prompt_hash = sha256_file(case / "prompt.md")
        for item in variants["variants"]:
            variant = item["id"]
            output = case / f"output.{variant}.md"
            output.write_text(
                "Static evidence only. Runtime behavior remains unverified. "
                "The response provides prioritized motion findings, concrete plans, "
                "Reduced Motion checks, and bounded verification steps. " * 3,
                encoding="utf-8",
            )
            skill_trees = {
                str(relative): tree_sha256(ROOT / str(relative))
                for relative in item.get("skill_paths", [])
            }
            installed_paths = {
                relative: f"$VARIANT_WORKSPACE/.pi/skills/{index:02d}-skill"
                for index, relative in enumerate(skill_trees, start=1)
            }
            (case / f"run.{variant}.json").write_text(
                json.dumps(
                    {
                        "schema": RUN_SCHEMA,
                        "variant": variant,
                        "host": "pi",
                        "host_version": "self-check",
                        "model": "fixture-model",
                        "model_observation": "requested_by_cli",
                        "thinking": "high",
                        "thinking_observation": "requested_by_cli",
                        "runner_os": "fixture",
                        "prompt_sha256": prompt_hash,
                        "output_path": output.name,
                        "output_sha256": sha256_file(output),
                        "skill_trees": skill_trees,
                        "installed_skill_paths": installed_paths,
                        "skill_install_mode": "isolated_project_copy",
                        "workspace_kind": "repo_external_isolated_project",
                        "cwd": "$VARIANT_WORKSPACE",
                        "command": "pi --print --no-skills",
                        "contract_sha256": contract_sha256(),
                        "returncode": 0,
                        "worktree_before_sha256": "a" * 64,
                        "worktree_after_sha256": "a" * 64,
                        "worktree_unchanged": True,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        blind = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/design_craft_comparative_blind.py"),
                "--case-dir",
                str(case),
                "--seed",
                "self-check-seed",
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if blind.returncode != 0:
            errors.append(
                "comparative e2e self-check blind step failed: "
                + (blind.stderr.strip() or blind.stdout.strip())
            )
            return errors
        blind_map = json.loads((case / "blind-map.json").read_text(encoding="utf-8"))
        focused_variant = variants["focused_variant"]
        points_by_variant = {
            "baseline": {key: max(0, value - 5) for key, value in weights.items()},
            focused_variant: {
                key: max(0, value - 2) for key, value in weights.items()
            },
            "design-craft": dict(weights),
        }
        results = []
        winner_label = ""
        for label, item in blind_map["outputs"].items():
            variant = item["variant"]
            criteria = points_by_variant[variant]
            if variant == "design-craft":
                winner_label = label
            results.append(
                {
                    "label": label,
                    "criteria": criteria,
                    "total": sum(criteria.values()),
                    "summary": "A sufficiently detailed self-check comparative judgment summary.",
                }
            )
        judgment = {
            "results": results,
            "winner": winner_label,
            "rationale": "The self-check winner has the highest recomputed score under the exact scorecard.",
        }
        judgment_bytes = (
            json.dumps(judgment, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        judgment_path = case / "blind-judgment.json"
        raw_output_path = case / "judge-output.raw.txt"
        judgment_path.write_bytes(judgment_bytes)
        raw_output_path.write_bytes(judgment_bytes)
        (case / "run.judge.json").write_text(
            json.dumps(
                {
                    "schema": JUDGE_RUN_SCHEMA,
                    "host": "codex",
                    "host_version": "self-check",
                    "model": "fixture-model",
                    "model_observation": "requested_by_cli",
                    "reasoning_profile": "high",
                    "reasoning_observation": "requested_by_cli",
                    "runner_os": "fixture",
                    "packet_path": "blind-packet.md",
                    "packet_sha256": sha256_file(case / "blind-packet.md"),
                    "judgment_schema_sha256": sha256_file(case / "judgment.schema.json"),
                    "raw_output_path": raw_output_path.name,
                    "raw_output_sha256": sha256_file(raw_output_path),
                    "judgment_path": judgment_path.name,
                    "judgment_sha256": sha256_file(judgment_path),
                    "workspace_kind": "repo_external_empty_project",
                    "cwd": "$JUDGE_WORKSPACE",
                    "command": "codex exec --sandbox read-only",
                    "returncode": 0,
                    "worktree_before_sha256": "b" * 64,
                    "worktree_after_sha256": "b" * 64,
                    "worktree_unchanged": True,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        record = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/design_craft_comparative_record.py"),
                "--case-dir",
                str(case),
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if record.returncode != 0:
            errors.append(
                "comparative e2e self-check record step failed: "
                + (record.stderr.strip() or record.stdout.strip())
            )
            return errors
        observed_errors = validate_case(case, require_observed=True)
        if observed_errors:
            errors.append(
                "comparative e2e self-check rejected valid observed evidence: "
                + "; ".join(observed_errors)
            )
        comparison = json.loads((case / "comparison.json").read_text(encoding="utf-8"))
        comparison["results"]["design-craft"]["score"] = 0
        (case / "comparison.json").write_text(json.dumps(comparison), encoding="utf-8")
        if not validate_case(case, require_observed=True):
            errors.append("comparative e2e self-check accepted a tampered winner score")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="evals/comparative")
    parser.add_argument("--case-dir")
    parser.add_argument("--require-observed", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors = run_self_check() if args.check else []
    if args.case_dir:
        cases = [Path(args.case_dir).expanduser().resolve()]
    else:
        cases = active_cases(Path(args.root).expanduser().resolve())
    if not cases:
        errors.append("at least one active comparative case is required")
    for case in cases:
        errors.extend(validate_case(case, require_observed=args.require_observed))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 2
    if args.check:
        print("comparative_validator_self_check=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
