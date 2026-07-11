#!/usr/bin/env python3
"""Validate cross-agent benchmark task definitions."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

from design_craft_evidence_common import (
    git_is_ancestor,
    git_root,
    read_version,
    sha256_file,
    skill_provenance,
    tree_sha256,
)


REQUIRED_FILES = ("prompt.md", "expected-findings.md", "scorecard.md")
PLACEHOLDER_PATTERN = re.compile(
    r"\bTODO\b|Use `evals/cross-agent/_template/scorecard\.md`|after real agent runs",
    re.I,
)
REQUIRED_CRITERIA = {
    "style_authority": ("style authority", "product context"),
    "reference_selection": ("reference",),
    "anti_generic_redesign": ("generic", "redesign"),
    "evidence_level": ("evidence level",),
    "verified_boundary": ("verified", "unverified"),
    "design_moves": ("design moves",),
    "scope_control": ("unrelated", "scope"),
}
ROOT = Path(__file__).resolve().parents[1]
OBSERVED_SCHEMA_V1 = "design-craft.cross-agent-score.v1"
OBSERVED_SCHEMA_V2 = "design-craft.cross-agent-score.v2"
HOSTS = ("codex", "pi", "cursor", "claude")
OBSERVED_REQUIRED_CRITERIA = (
    "style_authority",
    "reference_selection",
    "anti_generic_redesign",
    "evidence_level",
    "verified_boundary",
    "design_moves",
    "scope_control",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells):
            continue
        rows.append(cells)
    return rows


def bullet_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if re.match(r"^\s*[-*]\s+\S", line))


def validate_scorecard(path: Path) -> list[str]:
    text = read_text(path)
    errors: list[str] = []
    rows = markdown_rows(text)
    if len(rows) < 2:
        return [f"{path}: scorecard must include a markdown criteria table"]

    header = [cell.lower() for cell in rows[0]]
    for required in ("criterion", "weight", "pass evidence", "deduction trigger"):
        if required not in header:
            errors.append(f"{path}: scorecard table missing column {required!r}")
    if errors:
        return errors

    criterion_index = header.index("criterion")
    weight_index = header.index("weight")
    criteria_text = " ".join(
        row[criterion_index].lower()
        for row in rows[1:]
        if len(row) > criterion_index
    )
    for label, terms in REQUIRED_CRITERIA.items():
        if not all(term in criteria_text for term in terms):
            errors.append(f"{path}: scorecard missing criterion coverage for {label}")

    weights: list[int] = []
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) <= max(criterion_index, weight_index):
            errors.append(f"{path}: table row {row_number} has too few columns")
            continue
        match = re.fullmatch(r"([0-9]+)(?:\s*%)?", row[weight_index])
        if not match:
            errors.append(f"{path}: table row {row_number} weight must be an integer")
            continue
        weight = int(match.group(1))
        if weight <= 0:
            errors.append(f"{path}: table row {row_number} weight must be positive")
        weights.append(weight)
    if weights and sum(weights) != 100:
        errors.append(f"{path}: scorecard weights must sum to 100, got {sum(weights)}")
    if weights and len(weights) != len(OBSERVED_REQUIRED_CRITERIA):
        errors.append(
            f"{path}: scorecard must define exactly {len(OBSERVED_REQUIRED_CRITERIA)} criteria"
        )
    return errors


def scorecard_weights(path: Path) -> dict[str, int]:
    rows = markdown_rows(read_text(path))
    if len(rows) < 2:
        return {}
    header = [cell.lower() for cell in rows[0]]
    if "criterion" not in header or "weight" not in header:
        return {}
    criterion_index = header.index("criterion")
    weight_index = header.index("weight")
    values: dict[str, int] = {}
    for row in rows[1:]:
        if len(row) <= max(criterion_index, weight_index):
            return {}
        match = re.fullmatch(r"([0-9]+)(?:\s*%)?", row[weight_index])
        if not match:
            return {}
        criterion_text = row[criterion_index].lower()
        matches = [
            criterion
            for criterion, terms in REQUIRED_CRITERIA.items()
            if all(term in criterion_text for term in terms)
        ]
        if len(matches) != 1 or matches[0] in values:
            return {}
        values[matches[0]] = int(match.group(1))
    if set(values) != set(OBSERVED_REQUIRED_CRITERIA):
        return {}
    return values


def validate_task_dir(path: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        file_path = path / name
        if not file_path.is_file():
            errors.append(f"{path}: missing required file {name}")
            continue
        text = read_text(file_path)
        if PLACEHOLDER_PATTERN.search(text):
            errors.append(f"{file_path}: contains template placeholder text")
        if len(text.strip()) < 80:
            errors.append(f"{file_path}: file is too sparse for an active benchmark task")

    prompt_path = path / "prompt.md"
    if prompt_path.is_file():
        prompt = read_text(prompt_path)
        if "design-craft" not in prompt.lower():
            errors.append(f"{prompt_path}: prompt must explicitly route through design-craft")

    findings_path = path / "expected-findings.md"
    if findings_path.is_file() and bullet_count(read_text(findings_path)) < 3:
        errors.append(f"{findings_path}: expected findings must include at least three bullets")

    scorecard_path = path / "scorecard.md"
    if scorecard_path.is_file():
        errors.extend(validate_scorecard(scorecard_path))
    return errors


def validate_root(root: Path) -> list[str]:
    if not root.is_dir():
        return [f"{root}: cross-agent benchmark root does not exist"]
    errors: list[str] = []
    task_dirs = sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and not path.name.startswith("_")
    )
    if not task_dirs:
        return [f"{root}: at least one active benchmark task directory is required"]
    for task_dir in task_dirs:
        errors.extend(validate_task_dir(task_dir))
    return errors


def sha256_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_observed_score(
    task_dir: Path,
    host: str,
    prompt_hash: str,
    *,
    skill_root: Path,
    score_path: Path | None = None,
    require_schema_v2: bool = False,
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
    if schema not in {OBSERVED_SCHEMA_V1, OBSERVED_SCHEMA_V2}:
        errors.append(
            f"{path}: schema must be {OBSERVED_SCHEMA_V1} or {OBSERVED_SCHEMA_V2}"
        )
    if require_schema_v2 and schema != OBSERVED_SCHEMA_V2:
        errors.append(f"{path}: certified evidence must use {OBSERVED_SCHEMA_V2}")
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
    score = payload.get("score")
    if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 100:
        errors.append(f"{path}: score must be an integer from 0 to 100")

    if schema == OBSERVED_SCHEMA_V2:
        for key in ("model", "reasoning_profile", "runner_os", "skill_version"):
            if not isinstance(payload.get(key), str) or not payload[key].strip():
                errors.append(f"{path}: {key} must be a non-empty string")

        source_commit = str(payload.get("skill_source_commit", ""))
        if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
            errors.append(f"{path}: skill_source_commit must be a full lowercase Git SHA")
        source_dirty = payload.get("skill_source_dirty")
        if not isinstance(source_dirty, bool):
            errors.append(f"{path}: skill_source_dirty must be boolean")
        for key in ("skill_tree_sha256", "output_sha256", "scorecard_sha256"):
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

        scorecard_path = task_dir / "scorecard.md"
        if scorecard_path.is_file() and payload.get("scorecard_sha256") != sha256_file(scorecard_path):
            errors.append(f"{path}: scorecard_sha256 must match scorecard.md")

        if require_current_source:
            current_version = read_version(skill_root)
            current_tree = tree_sha256(skill_root)
            if payload.get("skill_version") != current_version:
                errors.append(
                    f"{path}: skill_version must match current skill version {current_version}"
                )
            if payload.get("skill_tree_sha256") != current_tree:
                errors.append(f"{path}: skill_tree_sha256 must match the current skill tree")
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

    criteria = payload.get("criteria")
    if not isinstance(criteria, dict):
        errors.append(f"{path}: criteria must be an object")
        return errors
    weights = scorecard_weights(task_dir / "scorecard.md") if schema == OBSERVED_SCHEMA_V2 else {}
    earned_total = 0
    for criterion in OBSERVED_REQUIRED_CRITERIA:
        result = criteria.get(criterion)
        if not isinstance(result, dict):
            errors.append(f"{path}: criteria.{criterion} must be an object")
            continue
        if not isinstance(result.get("passed"), bool):
            errors.append(f"{path}: criteria.{criterion}.passed must be boolean")
        note = result.get("note")
        if not isinstance(note, str) or len(note.strip()) < 8:
            errors.append(f"{path}: criteria.{criterion}.note must explain the result")
        if schema == OBSERVED_SCHEMA_V2:
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
    if schema == OBSERVED_SCHEMA_V2 and isinstance(score, int) and score != earned_total:
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
        "design move": ("design move", "设计动作", "设计建议"),
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
    require_schema_v2: bool = False,
    require_current_source: bool = False,
) -> list[str]:
    errors = validate_task_dir(task_dir)
    if errors:
        return errors

    prompt_path = task_dir / "prompt.md"
    prompt_hash = sha256_text(read_text(prompt_path))

    observed = observed_hosts(task_dir)
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
                    require_schema_v2=require_schema_v2,
                    require_current_source=require_current_source,
                )
            )
            if unverified_path.exists():
                errors.append(f"{unverified_path}: remove stale unverified note after recording an observed run")
        else:
            if not unverified_path.is_file():
                errors.append(f"{unverified_path}: missing explicit {host} unverified note")
            else:
                text = read_text(unverified_path).lower()
                if "unverified" not in text or "reason" not in text:
                    errors.append(f"{unverified_path}: must record {host} as unverified with a reason")

    for host in required_hosts:
        if host not in observed:
            errors.append(f"{task_dir}: required observed host is missing: {host}")

    comparison_path = task_dir / "comparison.md"
    if not comparison_path.is_file():
        errors.append(f"{comparison_path}: missing comparison summary")
    else:
        comparison = read_text(comparison_path).lower()
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
    (task / "scorecard.md").write_text(
        "# Scorecard\n\n"
        "| Criterion | Weight | Pass evidence | Deduction trigger |\n"
        "|---|---:|---|---|\n"
        "| Style authority and product context | 15 | Reads local authority. | Overrides product context. |\n"
        "| Reference selection | 15 | Chooses focused references. | Loads unrelated references. |\n"
        "| Anti-generic redesign | 15 | Avoids generic redesign. | Applies generic redesign. |\n"
        "| Evidence level labeling | 15 | Labels evidence level. | Overclaims evidence. |\n"
        "| Verified/unverified boundary | 15 | Separates verified and unverified. | Blurs verification. |\n"
        "| Concrete design moves | 15 | Gives design moves. | Gives vague advice. |\n"
        "| Scope control and unrelated changes | 10 | Avoids unrelated changes. | Expands scope. |\n",
        encoding="utf-8",
    )


def run_self_check() -> list[str]:
    temp_root = Path(tempfile.mkdtemp(prefix="design-craft-cross-agent-"))
    try:
        write_valid_task(temp_root)
        errors = validate_root(temp_root)
        invalid = temp_root / "same-prompt-invalid"
        shutil.copytree(temp_root / "same-prompt-generic", invalid)
        (invalid / "scorecard.md").write_text("# Scorecard\n\n- TODO\n", encoding="utf-8")
        invalid_errors = validate_task_dir(invalid)
        if not any("placeholder" in error or "table" in error for error in invalid_errors):
            errors.append("self-check failed to reject placeholder scorecard")

        task = temp_root / "same-prompt-generic"
        for host in HOSTS:
            (task / f"{host}-unverified.md").write_text(
                f"# {host} unverified\n\nStatus: unverified.\n\nReason: fixture host did not run.\n",
                encoding="utf-8",
            )
        (task / "comparison.md").write_text(
            "# Comparison\n\nCodex, Pi, Cursor, and Claude remain unverified in this fixture.\n",
            encoding="utf-8",
        )
        errors.extend(validate_observed_task(task))
        (task / "cursor-output.md").write_text("Evidence and unverified design moves. " * 20, encoding="utf-8")
        partial_errors = validate_observed_task(task)
        if not any("score.cursor.json" in error for error in partial_errors):
            errors.append("self-check failed to reject a partial observed-host artifact pair")
        (task / "cursor-output.md").unlink()

        (task / "codex-unverified.md").unlink()
        output = task / "codex-output.md"
        output.write_text("Evidence, unverified boundaries, and design moves. " * 20, encoding="utf-8")
        provenance = skill_provenance(ROOT / "skills/design-craft")
        weights = scorecard_weights(task / "scorecard.md")
        score_payload = {
            "schema": OBSERVED_SCHEMA_V2,
            "task_id": task.name,
            "agent": "codex",
            "verified": True,
            "agent_version": "self-check",
            "model": "fixture-model",
            "reasoning_profile": "fixture",
            "runner_os": "fixture",
            "date": "2026-01-01",
            "prompt_sha256": sha256_text(read_text(task / "prompt.md")),
            "scorecard_sha256": sha256_file(task / "scorecard.md"),
            "skill_path": provenance["skill_path"],
            "skill_version": provenance["skill_version"],
            "skill_source_commit": provenance["skill_source_commit"],
            "skill_source_dirty": provenance["skill_source_dirty"],
            "skill_tree_sha256": provenance["skill_tree_sha256"],
            "command_summary": "self-check fixture",
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
    parser.add_argument("--check", action="store_true", help="Run built-in self-checks.")
    parser.add_argument("--root", default="evals/cross-agent", help="Cross-agent benchmark root.")
    parser.add_argument("--observed-task", help="Validate one task directory with recorded agent outputs.")
    parser.add_argument(
        "--require-host",
        action="append",
        choices=HOSTS,
        default=[],
        help="Require this host to have a real output and score in --observed-task",
    )
    parser.add_argument(
        "--require-schema-v2",
        action="store_true",
        help="Require cryptographically bound v2 score artifacts.",
    )
    parser.add_argument(
        "--require-current-source",
        action="store_true",
        help="Require v2 evidence bound to the current skill version and tree.",
    )
    parser.add_argument(
        "--skill-root",
        default=str(ROOT / "skills/design-craft"),
        help="Current canonical skill root used by --require-current-source.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    if args.check:
        errors.extend(run_self_check())
    elif args.observed_task:
        errors.extend(
            validate_observed_task(
                Path(args.observed_task),
                tuple(args.require_host),
                skill_root=Path(args.skill_root).expanduser().resolve(),
                require_schema_v2=args.require_schema_v2 or args.require_current_source,
                require_current_source=args.require_current_source,
            )
        )
    else:
        errors.extend(validate_root(Path(args.root)))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
