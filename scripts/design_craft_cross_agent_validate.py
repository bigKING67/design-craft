#!/usr/bin/env python3
"""Validate cross-agent benchmark task definitions."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from design_craft_evidence_common import (
    git_is_ancestor,
    git_root,
    git_tree_sha256,
    read_version,
    sha256_file,
    skill_provenance,
    tree_sha256,
)
from tools.design_craft.evaluation.cross_agent.contract import (
    CURRENT_SCORE_KEYS,
    CURRENT_RUN_KEYS,
    HOSTS,
    OBSERVED_REQUIRED_CRITERIA,
    OBSERVED_SCHEMA_V2,
    OBSERVED_SCHEMA_V3,
    OBSERVED_SCHEMA_V4,
    RUN_SCHEMA_V2,
    STATUS_SCHEMA,
    cross_agent_contract_sha256,
    load_evidence_status,
    read_text,
    render_current_comparison,
    scorecard_weights,
    sha256_text,
    validate_definition_root as validate_root,
    validate_task_definition as validate_task_dir,
)
from tools.design_craft.evaluation.cross_agent.history import (
    historical_scorecard_weights as historical_markdown_scorecard_weights,
    validate_historical_task_definition as validate_historical_task_dir,
)


def validate_observed_score(
    task_dir: Path,
    host: str,
    prompt_hash: str,
    *,
    skill_root: Path,
    score_path: Path | None = None,
    require_current_schema: bool = False,
    require_current_source: bool = False,
) -> list[str]:
    errors: list[str] = []
    path = score_path or task_dir / f"score.{host}.json"
    if not path.is_file():
        return [f"{path}: missing observed score file"]
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return [f"{path}: invalid JSON: {exc}"]

    schema = payload.get("schema")
    if schema not in {OBSERVED_SCHEMA_V2, OBSERVED_SCHEMA_V3, OBSERVED_SCHEMA_V4}:
        errors.append(
            f"{path}: schema must be historical v2/v3 or current {OBSERVED_SCHEMA_V4}"
        )
    if require_current_schema and schema != OBSERVED_SCHEMA_V4:
        errors.append(f"{path}: current evidence must use {OBSERVED_SCHEMA_V4}")
    if schema == OBSERVED_SCHEMA_V4 and set(payload) != CURRENT_SCORE_KEYS:
        errors.append(
            f"{path}: current score fields mismatch "
            f"missing={sorted(CURRENT_SCORE_KEYS - set(payload))} "
            f"extra={sorted(set(payload) - CURRENT_SCORE_KEYS)}"
        )
    if payload.get("task_id") != task_dir.name:
        errors.append(f"{path}: task_id must be {task_dir.name}")
    if payload.get("agent") != host:
        errors.append(f"{path}: agent must be {host}")
    if payload.get("verified") is not True:
        errors.append(f"{path}: observed host must set verified=true")
    if payload.get("prompt_sha256") != prompt_hash:
        errors.append(f"{path}: prompt_sha256 must match prompt.md")
    for key in ("agent_version", "date", "skill_path", "command_summary"):
        if not isinstance(payload.get(key), str) or not payload[key].strip():
            errors.append(f"{path}: {key} must be a non-empty string")
    skill_path_value = str(payload.get("skill_path", ""))
    if re.match(r"^(?:/Users/|/home/|[A-Za-z]:[\\/]Users[\\/])", skill_path_value):
        errors.append(f"{path}: skill_path must redact the host home directory")
    score = payload.get("score")
    if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 100:
        errors.append(f"{path}: score must be an integer from 0 to 100")

    if schema in {OBSERVED_SCHEMA_V2, OBSERVED_SCHEMA_V3, OBSERVED_SCHEMA_V4}:
        for key in ("model", "reasoning_profile", "runner_os", "skill_version"):
            if not isinstance(payload.get(key), str) or not payload[key].strip():
                errors.append(f"{path}: {key} must be a non-empty string")
        if schema in {OBSERVED_SCHEMA_V3, OBSERVED_SCHEMA_V4}:
            for key in (
                "model_observation",
                "reasoning_observation",
                "provenance_skill_path",
            ):
                if not isinstance(payload.get(key), str) or not payload[key].strip():
                    errors.append(f"{path}: {key} must be a non-empty string")

        source_commit = str(payload.get("skill_source_commit", ""))
        if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
            errors.append(f"{path}: skill_source_commit must be a full lowercase Git SHA")
        source_dirty = payload.get("skill_source_dirty")
        if not isinstance(source_dirty, bool):
            errors.append(f"{path}: skill_source_dirty must be boolean")
        if "repo_dirty" in payload and not isinstance(payload.get("repo_dirty"), bool):
            errors.append(f"{path}: repo_dirty must be boolean when present")
        digest_keys = ["skill_tree_sha256", "output_sha256"]
        digest_keys.append("scorecard_json_sha256" if schema == OBSERVED_SCHEMA_V4 else "scorecard_sha256")
        if schema in {OBSERVED_SCHEMA_V3, OBSERVED_SCHEMA_V4}:
            digest_keys.extend(("contract_sha256", "run_manifest_sha256"))
        for key in digest_keys:
            if not re.fullmatch(r"[0-9a-f]{64}", str(payload.get(key, ""))):
                errors.append(f"{path}: {key} must be 64 lowercase hex characters")

        output_path_value = payload.get("output_path")
        if not isinstance(output_path_value, str) or not output_path_value.strip():
            errors.append(f"{path}: output_path must be a non-empty relative path")
        else:
            output_relative = Path(output_path_value)
            if output_relative.is_absolute() or ".." in output_relative.parts:
                errors.append(f"{path}: output_path must stay inside the task directory")
            else:
                output_path = task_dir / output_relative
                if output_path.name != f"{host}-output.md":
                    errors.append(f"{path}: output_path must point to {host}-output.md")
                elif not output_path.is_file():
                    errors.append(f"{path}: output_path does not exist: {output_path}")
                elif payload.get("output_sha256") != sha256_file(output_path):
                    errors.append(f"{path}: output_sha256 must match {output_path.name}")

        scorecard_path = task_dir / ("scorecard.json" if schema == OBSERVED_SCHEMA_V4 else "scorecard.md")
        scorecard_digest_key = "scorecard_json_sha256" if schema == OBSERVED_SCHEMA_V4 else "scorecard_sha256"
        if scorecard_path.is_file() and payload.get(scorecard_digest_key) != sha256_file(scorecard_path):
            errors.append(f"{path}: {scorecard_digest_key} must match {scorecard_path.name}")

        if schema in {OBSERVED_SCHEMA_V3, OBSERVED_SCHEMA_V4}:
            run_manifest_value = payload.get("run_manifest_path")
            if not isinstance(run_manifest_value, str) or not run_manifest_value.strip():
                errors.append(f"{path}: run_manifest_path must be a non-empty relative path")
            else:
                run_relative = Path(run_manifest_value)
                run_path = task_dir / run_relative
                if run_relative.is_absolute() or ".." in run_relative.parts:
                    errors.append(f"{path}: run_manifest_path must stay inside the task directory")
                elif run_path.name != f"run.{host}.json" or not run_path.is_file():
                    errors.append(f"{path}: run_manifest_path must point to run.{host}.json")
                else:
                    if payload.get("run_manifest_sha256") != sha256_file(run_path):
                        errors.append(f"{path}: run_manifest_sha256 must match {run_path.name}")
                    try:
                        run_payload = json.loads(run_path.read_text(encoding="utf-8"))
                    except json.JSONDecodeError as exc:
                        errors.append(f"{run_path}: invalid run manifest: {exc}")
                    else:
                        if schema == OBSERVED_SCHEMA_V4 and set(run_payload) != CURRENT_RUN_KEYS:
                            errors.append(
                                f"{run_path}: current run fields mismatch "
                                f"missing={sorted(CURRENT_RUN_KEYS - set(run_payload))} "
                                f"extra={sorted(set(run_payload) - CURRENT_RUN_KEYS)}"
                            )
                        if run_payload.get("schema") != RUN_SCHEMA_V2:
                            errors.append(
                                f"{run_path}: run manifest schema must be {RUN_SCHEMA_V2}"
                            )
                        if run_payload.get("host") != host:
                            errors.append(f"{run_path}: host must be {host}")
                        if run_payload.get("prompt_sha256") != prompt_hash:
                            errors.append(f"{run_path}: prompt_sha256 must match prompt.md")
                        if run_payload.get("output_sha256") != payload.get("output_sha256"):
                            errors.append(f"{run_path}: output_sha256 must match the score artifact")
                        if run_payload.get("worktree_unchanged") is not True:
                            errors.append(f"{run_path}: worktree_unchanged must be true")
                        if schema in {OBSERVED_SCHEMA_V3, OBSERVED_SCHEMA_V4}:
                            run_score_pairs = {
                                "host_version": "agent_version",
                                "model": "model",
                                "model_observation": "model_observation",
                                "reasoning_profile": "reasoning_profile",
                                "reasoning_observation": "reasoning_observation",
                                "runner_os": "runner_os",
                                "skill_path": "skill_path",
                                "skill_tree_sha256": "skill_tree_sha256",
                                "command": "command_summary",
                            }
                            for run_key, score_key in run_score_pairs.items():
                                if run_payload.get(run_key) != payload.get(score_key):
                                    errors.append(
                                        f"{run_path}: {run_key} must match score field {score_key}"
                                    )
                            if run_payload.get("skill_install_mode") != "isolated_project_copy":
                                errors.append(
                                    f"{run_path}: skill_install_mode must be isolated_project_copy"
                                )
                            if run_payload.get("workspace_kind") != "repo_external_isolated_project":
                                errors.append(
                                    f"{run_path}: workspace_kind must be repo_external_isolated_project"
                                )
                            if run_payload.get("returncode") != 0:
                                errors.append(f"{run_path}: returncode must be zero")
                            before_hash = run_payload.get("worktree_before_sha256")
                            after_hash = run_payload.get("worktree_after_sha256")
                            if not re.fullmatch(r"[0-9a-f]{64}", str(before_hash or "")):
                                errors.append(
                                    f"{run_path}: worktree_before_sha256 must be 64 lowercase hex characters"
                                )
                            if before_hash != after_hash:
                                errors.append(
                                    f"{run_path}: worktree fingerprints must match"
                                )
                            for key in ("skill_path", "command", "cwd"):
                                value = str(run_payload.get(key, ""))
                                if not value:
                                    errors.append(f"{run_path}: {key} must be non-empty")
                                elif re.search(
                                    r"(?:/Users/|/home/|[A-Za-z]:[\\/]Users[\\/])",
                                    value,
                                ):
                                    errors.append(f"{run_path}: {key} must redact local user paths")

        if require_current_source:
            current_version = read_version(skill_root)
            current_tree = tree_sha256(skill_root)
            if payload.get("skill_version") != current_version:
                errors.append(
                    f"{path}: skill_version must match current skill version {current_version}"
                )
            if payload.get("skill_tree_sha256") != current_tree:
                errors.append(f"{path}: skill_tree_sha256 must match the current skill tree")
            if schema in {OBSERVED_SCHEMA_V3, OBSERVED_SCHEMA_V4} and payload.get("contract_sha256") != cross_agent_contract_sha256():
                errors.append(
                    f"{path}: contract_sha256 must match the current cross-agent contract"
                )
            if source_dirty is not False:
                errors.append(f"{path}: certified evidence must record skill_source_dirty=false")
            if re.fullmatch(r"[0-9a-f]{40}", source_commit):
                try:
                    repository = git_root(skill_root)
                except (OSError, ValueError, RuntimeError):
                    errors.append(f"{path}: current skill source is not in a Git repository")
                else:
                    if not git_is_ancestor(repository, source_commit):
                        errors.append(
                            f"{path}: skill_source_commit must be an ancestor of current HEAD"
                        )
                    else:
                        try:
                            committed_tree = git_tree_sha256(
                                repository,
                                skill_root,
                                source_commit,
                            )
                        except (OSError, ValueError, subprocess.CalledProcessError) as exc:
                            errors.append(
                                f"{path}: cannot inspect skill tree at skill_source_commit: {exc}"
                            )
                        else:
                            if payload.get("skill_tree_sha256") != committed_tree:
                                errors.append(
                                    f"{path}: skill_source_commit tree must match skill_tree_sha256"
                                )

    criteria = payload.get("criteria")
    if not isinstance(criteria, dict):
        errors.append(f"{path}: criteria must be an object")
        return errors
    if set(criteria) != set(OBSERVED_REQUIRED_CRITERIA):
        errors.append(
            f"{path}: criteria must contain exactly {list(OBSERVED_REQUIRED_CRITERIA)}"
        )
    if schema == OBSERVED_SCHEMA_V4:
        weights = scorecard_weights(task_dir / "scorecard.json")
    elif schema in {OBSERVED_SCHEMA_V2, OBSERVED_SCHEMA_V3}:
        weights = historical_markdown_scorecard_weights(task_dir / "scorecard.md")
    else:
        weights = {}
    earned_total = 0
    for criterion in OBSERVED_REQUIRED_CRITERIA:
        result = criteria.get(criterion)
        if not isinstance(result, dict):
            errors.append(f"{path}: criteria.{criterion} must be an object")
            continue
        expected_result_keys = (
            {"passed", "earned", "note"}
            if schema in {OBSERVED_SCHEMA_V2, OBSERVED_SCHEMA_V3, OBSERVED_SCHEMA_V4}
            else {"passed", "note"}
        )
        if set(result) != expected_result_keys:
            errors.append(
                f"{path}: criteria.{criterion} fields must be "
                f"{sorted(expected_result_keys)}"
            )
        if not isinstance(result.get("passed"), bool):
            errors.append(f"{path}: criteria.{criterion}.passed must be boolean")
        note = result.get("note")
        if not isinstance(note, str) or len(note.strip()) < 8:
            errors.append(f"{path}: criteria.{criterion}.note must explain the result")
        if schema in {OBSERVED_SCHEMA_V2, OBSERVED_SCHEMA_V3, OBSERVED_SCHEMA_V4}:
            weight = weights.get(criterion)
            earned = result.get("earned")
            if weight is None:
                errors.append(f"{path}: scorecard weight is unavailable for {criterion}")
            elif not isinstance(earned, int) or isinstance(earned, bool) or not 0 <= earned <= weight:
                errors.append(
                    f"{path}: criteria.{criterion}.earned must be an integer from 0 to {weight}"
                )
            else:
                earned_total += earned
                if result.get("passed") is True and earned == 0:
                    errors.append(
                        f"{path}: criteria.{criterion} cannot pass with zero earned points"
                    )
                if result.get("passed") is False and earned == weight:
                    errors.append(
                        f"{path}: criteria.{criterion} cannot fail with full earned points"
                    )
    if schema in {OBSERVED_SCHEMA_V2, OBSERVED_SCHEMA_V3, OBSERVED_SCHEMA_V4} and isinstance(score, int) and score != earned_total:
        errors.append(
            f"{path}: score must equal the sum of criteria earned points "
            f"({earned_total}, observed {score})"
        )
    return errors


def validate_output(task_dir: Path, host: str) -> list[str]:
    errors: list[str] = []
    output = task_dir / f"{host}-output.md"
    if not output.is_file():
        return [f"{output}: missing observed output"]
    text = read_text(output)
    if len(text.strip()) < 400:
        errors.append(f"{output}: observed output is too sparse")
    lowered = text.lower()
    required_concepts = {
        "evidence": ("evidence", "证据"),
        "unverified": ("unverified", "未验证"),
        "design move": (
            "design move",
            "设计动作",
            "设计建议",
            "设计移动",
            "设计修正",
            "设计改进",
        ),
    }
    for label, variants in required_concepts.items():
        if not any(variant in lowered for variant in variants):
            errors.append(f"{output}: output should cover the {label!r} concept")
    return errors


def observed_hosts(task_dir: Path) -> set[str]:
    return {
        host
        for host in HOSTS
        if (task_dir / f"{host}-output.md").is_file() and (task_dir / f"score.{host}.json").is_file()
    }


def validate_observed_task(
    task_dir: Path,
    required_hosts: tuple[str, ...] = (),
    *,
    skill_root: Path = ROOT / "skills/design-craft",
    require_current_schema: bool = False,
    require_current_source: bool = False,
    historical: bool = False,
    require_any_observed: bool = False,
) -> list[str]:
    errors = (
        validate_historical_task_dir(task_dir)
        if historical
        else validate_task_dir(task_dir)
    )
    if errors:
        return errors

    prompt_path = task_dir / "prompt.md"
    prompt_hash = sha256_text(read_text(prompt_path))

    observed = observed_hosts(task_dir)
    if require_any_observed and not observed:
        errors.append(f"{task_dir}: at least one observed host is required")
    states: dict[str, str] = {}
    if not historical:
        states, status_errors = load_evidence_status(task_dir / "evidence-status.json")
        errors.extend(status_errors)
    for host in HOSTS:
        output_path = task_dir / f"{host}-output.md"
        score_path = task_dir / f"score.{host}.json"
        unverified_path = task_dir / f"{host}-unverified.md"
        has_any_observed = output_path.exists() or score_path.exists()
        if has_any_observed:
            errors.extend(validate_output(task_dir, host))
            errors.extend(
                validate_observed_score(
                    task_dir,
                    host,
                    prompt_hash,
                    skill_root=skill_root,
                    require_current_schema=require_current_schema,
                    require_current_source=require_current_source,
                )
            )
            if historical:
                if unverified_path.exists():
                    errors.append(f"{unverified_path}: remove stale unverified note after recording an observed run")
            elif states.get(host) != "observed":
                errors.append(
                    f"{task_dir / 'evidence-status.json'}: hosts.{host}.status must be observed"
                )
        else:
            if historical:
                if not unverified_path.is_file():
                    errors.append(f"{unverified_path}: missing explicit {host} unverified note")
                else:
                    text = read_text(unverified_path).lower()
                    if "unverified" not in text or "reason" not in text:
                        errors.append(f"{unverified_path}: must record {host} as unverified with a reason")
            else:
                state = states.get(host)
                if state not in {"pending", "unverified"}:
                    errors.append(
                        f"{task_dir / 'evidence-status.json'}: hosts.{host}.status must be pending or unverified without observed artifacts"
                    )

    for host in required_hosts:
        if host not in observed:
            errors.append(f"{task_dir}: required observed host is missing: {host}")

    if historical:
        comparison_path = task_dir / "comparison.md"
        if not comparison_path.is_file():
            errors.append(f"{comparison_path}: missing comparison summary")
            return errors
        comparison = read_text(comparison_path).lower()
        if len(comparison.strip()) < 80:
            errors.append(f"{comparison_path}: comparison summary is too sparse")
        for term in HOSTS:
            if term not in comparison:
                errors.append(f"{comparison_path}: comparison must mention {term}")
    return errors


def write_valid_task(root: Path) -> None:
    task = root / "same-prompt-generic"
    task.mkdir(parents=True)
    (task / "prompt.md").write_text(
        "# Same prompt: generic\n\nUse design-craft to critique a generic product surface with evidence labels.\n",
        encoding="utf-8",
    )
    (task / "expected-findings.md").write_text(
        "# Expected findings\n\n"
        "- Respect style authority.\n"
        "- Label missing browser evidence.\n"
        "- Recommend concrete design moves.\n",
        encoding="utf-8",
    )
    criteria = [
        ("style_authority", "Style authority and product context", 15),
        ("reference_selection", "Reference selection", 15),
        ("anti_generic_redesign", "Anti-generic redesign", 15),
        ("evidence_level", "Evidence level labeling", 15),
        ("verified_boundary", "Verified/unverified boundary", 15),
        ("design_moves", "Concrete design moves", 15),
        ("scope_control", "Scope control and unrelated changes", 10),
    ]
    (task / "scorecard.json").write_text(
        json.dumps(
            {
                "schema": "design-craft.cross-agent-scorecard.v1",
                "task_id": task.name,
                "criteria": [
                    {
                        "id": criterion_id,
                        "label": label,
                        "weight": weight,
                        "pass_evidence": "Self-check provides concrete pass evidence.",
                        "deduction_trigger": "Self-check provides a concrete deduction trigger.",
                    }
                    for criterion_id, label, weight in criteria
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (task / "evidence-status.json").write_text(
        json.dumps(
            {
                "schema": STATUS_SCHEMA,
                "task_id": task.name,
                "hosts": {
                    host: {
                        "status": "pending",
                        "reason": "Self-check has not admitted current observed evidence.",
                    }
                    for host in HOSTS
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (task / "comparison.md").write_text(
        render_current_comparison(task), encoding="utf-8"
    )


def run_self_check() -> list[str]:
    temp_root = Path(tempfile.mkdtemp(prefix="design-craft-cross-agent-"))
    try:
        write_valid_task(temp_root)
        errors = validate_root(temp_root)
        invalid = temp_root / "same-prompt-invalid"
        shutil.copytree(temp_root / "same-prompt-generic", invalid)
        invalid_scorecard = json.loads((invalid / "scorecard.json").read_text(encoding="utf-8"))
        invalid_scorecard["criteria"][0]["weight"] = "15"
        (invalid / "scorecard.json").write_text(
            json.dumps(invalid_scorecard, indent=2) + "\n", encoding="utf-8"
        )
        invalid_errors = validate_task_dir(invalid)
        if not any("weight must be a positive integer" in error for error in invalid_errors):
            errors.append("self-check failed to reject an invalid JSON scorecard")

        task = temp_root / "same-prompt-generic"
        errors.extend(validate_observed_task(task))
        (task / "cursor-output.md").write_text("Evidence and unverified design moves. " * 20, encoding="utf-8")
        partial_errors = validate_observed_task(task)
        if not any("score.cursor.json" in error for error in partial_errors):
            errors.append("self-check failed to reject a partial observed-host artifact pair")
        (task / "cursor-output.md").unlink()

        output = task / "codex-output.md"
        output.write_text("Evidence, unverified boundaries, and design moves. " * 20, encoding="utf-8")
        run_manifest = task / "run.codex.json"
        run_manifest.write_text(
            json.dumps(
                {
                    "schema": RUN_SCHEMA_V2,
                    "host": "codex",
                    "host_version": "self-check",
                    "model": "fixture-model",
                    "model_observation": "requested_by_cli",
                    "reasoning_profile": "fixture",
                    "reasoning_observation": "requested_by_cli",
                    "runner_os": "fixture",
                    "started_at": "2026-01-01T00:00:00Z",
                    "duration_seconds": 1.0,
                    "timeout_seconds": 60,
                    "prompt_path": "prompt.md",
                    "prompt_sha256": sha256_text(read_text(task / "prompt.md")),
                    "prompt_transport": "stdin",
                    "output_path": output.name,
                    "output_sha256": sha256_file(output),
                    "skill_path": "$BENCHMARK_WORKSPACE/.agents/skills/design-craft",
                    "skill_tree_sha256": tree_sha256(ROOT / "skills/design-craft"),
                    "skill_install_mode": "isolated_project_copy",
                    "workspace_kind": "repo_external_isolated_project",
                    "cwd": "$BENCHMARK_WORKSPACE",
                    "command": "codex exec --sandbox read-only $BENCHMARK_WORKSPACE",
                    "returncode": 0,
                    "stderr_bytes": 0,
                    "stderr_sha256": sha256_text(""),
                    "worktree_before_sha256": "a" * 64,
                    "worktree_after_sha256": "a" * 64,
                    "worktree_unchanged": True,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        provenance = skill_provenance(ROOT / "skills/design-craft")
        weights = scorecard_weights(task / "scorecard.json")
        score_payload = {
            "schema": OBSERVED_SCHEMA_V4,
            "task_id": task.name,
            "agent": "codex",
            "verified": True,
            "agent_version": "self-check",
            "model": "fixture-model",
            "model_observation": "requested_by_cli",
            "reasoning_profile": "fixture",
            "reasoning_observation": "requested_by_cli",
            "runner_os": "fixture",
            "date": "2026-01-01",
            "prompt_sha256": sha256_text(read_text(task / "prompt.md")),
            "scorecard_json_sha256": sha256_file(task / "scorecard.json"),
            "contract_sha256": cross_agent_contract_sha256(),
            "run_manifest_path": run_manifest.name,
            "run_manifest_sha256": sha256_file(run_manifest),
            "skill_path": "$BENCHMARK_WORKSPACE/.agents/skills/design-craft",
            "provenance_skill_path": provenance["skill_path"],
            "skill_version": provenance["skill_version"],
            "skill_source_commit": provenance["skill_source_commit"],
            "skill_source_dirty": provenance["skill_source_dirty"],
            "repo_dirty": provenance["repo_dirty"],
            "release_state": provenance["release_state"],
            "skill_tree_sha256": provenance["skill_tree_sha256"],
            "command_summary": "codex exec --sandbox read-only $BENCHMARK_WORKSPACE",
            "output_path": output.name,
            "output_sha256": sha256_file(output),
            "score": 100,
            "criteria": {
                criterion: {
                    "passed": True,
                    "earned": weight,
                    "note": "Self-check earned points match the scorecard contract.",
                }
                for criterion, weight in weights.items()
            },
        }
        score_path = task / "score.codex.json"
        score_path.write_text(json.dumps(score_payload, indent=2) + "\n", encoding="utf-8")
        status_payload = json.loads((task / "evidence-status.json").read_text(encoding="utf-8"))
        status_payload["hosts"]["codex"] = {
            "status": "observed",
            "reason": "Self-check admitted a complete current observed artifact pair.",
        }
        (task / "evidence-status.json").write_text(
            json.dumps(status_payload, indent=2) + "\n", encoding="utf-8"
        )
        (task / "comparison.md").write_text(
            render_current_comparison(task), encoding="utf-8"
        )
        errors.extend(validate_observed_task(task))
        score_payload["score"] = 99
        score_path.write_text(json.dumps(score_payload, indent=2) + "\n", encoding="utf-8")
        score_errors = validate_observed_task(task)
        if not any("sum of criteria earned points" in error for error in score_errors):
            errors.append("self-check failed to reject a non-computed cross-agent score")
        return errors
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate design-craft cross-agent benchmark tasks.")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="Run built-in self-checks.")
    modes.add_argument("--root", help="Cross-agent benchmark root.")
    modes.add_argument("--observed-task", help="Validate one task with recorded outputs.")
    modes.add_argument(
        "--history-root",
        help="Validate immutable historical observed tasks without treating them as current source.",
    )
    parser.add_argument(
        "--require-host",
        action="append",
        choices=HOSTS,
        default=[],
        help="Require this host to have a real output and score in --observed-task",
    )
    parser.add_argument(
        "--skill-root",
        help="Canonical skill root used only by --observed-task.",
    )
    args = parser.parse_args()
    if not args.observed_task and (args.require_host or args.skill_root):
        parser.error("--require-host and --skill-root require --observed-task")

    errors: list[str] = []
    if args.check:
        errors.extend(run_self_check())
    elif args.history_root:
        history_root = Path(args.history_root).expanduser().resolve()
        historical_tasks = sorted(
            path for path in history_root.rglob("same-prompt-*") if path.is_dir()
        )
        if not historical_tasks:
            errors.append(f"{history_root}: no historical observed tasks found")
        for task in historical_tasks:
            errors.extend(validate_observed_task(task, historical=True))
    elif args.observed_task:
        errors.extend(
            validate_observed_task(
                Path(args.observed_task),
                tuple(args.require_host),
                skill_root=(
                    Path(args.skill_root).expanduser().resolve()
                    if args.skill_root
                    else ROOT / "skills/design-craft"
                ),
                require_current_schema=True,
                require_current_source=True,
                require_any_observed=True,
            )
        )
    else:
        errors.extend(validate_root(Path(args.root or "evals/cross-agent")))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
