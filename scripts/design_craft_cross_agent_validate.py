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


REQUIRED_FILES = ("prompt.md", "expected-findings.md", "scorecard.md")
PLACEHOLDER_PATTERN = re.compile(
    r"\bTODO\b|Use `evals/cross-agent/_template/scorecard\.md`|after real agent runs",
    re.I,
)
REQUIRED_CRITERIA = {
    "style authority": ("style authority", "product context"),
    "reference selection": ("reference",),
    "anti-generic redesign": ("generic", "redesign"),
    "evidence level": ("evidence level",),
    "verified boundary": ("verified", "unverified"),
    "design moves": ("design moves",),
    "scope control": ("unrelated", "scope"),
}
OBSERVED_SCHEMA = "design-craft.cross-agent-score.v1"
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
    return errors


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


def validate_observed_score(task_dir: Path, host: str, prompt_hash: str) -> list[str]:
    errors: list[str] = []
    path = task_dir / f"score.{host}.json"
    if not path.is_file():
        return [f"{path}: missing observed score file"]
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return [f"{path}: invalid JSON: {exc}"]

    if payload.get("schema") != OBSERVED_SCHEMA:
        errors.append(f"{path}: schema must be {OBSERVED_SCHEMA}")
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
    if not isinstance(score, int) or not 0 <= score <= 100:
        errors.append(f"{path}: score must be an integer from 0 to 100")

    criteria = payload.get("criteria")
    if not isinstance(criteria, dict):
        errors.append(f"{path}: criteria must be an object")
        return errors
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
    for term in ("evidence", "unverified", "design move"):
        if term not in lowered:
            errors.append(f"{output}: output should mention {term!r}")
    return errors


def observed_hosts(task_dir: Path) -> set[str]:
    return {
        host
        for host in HOSTS
        if (task_dir / f"{host}-output.md").is_file() and (task_dir / f"score.{host}.json").is_file()
    }


def validate_observed_task(task_dir: Path, required_hosts: tuple[str, ...] = ()) -> list[str]:
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
            errors.extend(validate_observed_score(task_dir, host, prompt_hash))
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
    args = parser.parse_args()

    errors: list[str] = []
    if args.check:
        errors.extend(run_self_check())
    elif args.observed_task:
        errors.extend(validate_observed_task(Path(args.observed_task), tuple(args.require_host)))
    else:
        errors.extend(validate_root(Path(args.root)))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
