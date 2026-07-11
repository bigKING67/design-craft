#!/usr/bin/env python3
"""Record a cryptographically bound cross-agent score artifact."""

from __future__ import annotations

import argparse
import json
import platform
from datetime import date
from pathlib import Path

from design_craft_cross_agent_validate import (
    OBSERVED_REQUIRED_CRITERIA,
    OBSERVED_SCHEMA_V2,
    read_text,
    scorecard_weights,
    sha256_text,
    validate_output,
    validate_observed_score,
)
from design_craft_evidence_common import sha256_file, skill_provenance


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-dir", required=True)
    parser.add_argument("--agent", required=True, choices=("codex", "pi", "cursor", "claude"))
    parser.add_argument("--agent-version", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--reasoning-profile", required=True)
    parser.add_argument("--runner-os", default=platform.platform())
    parser.add_argument("--skill-root", required=True)
    parser.add_argument(
        "--canonical-skill-root",
        default=str(ROOT / "skills/design-craft"),
        help="Current canonical source tree used to validate an installed skill copy.",
    )
    parser.add_argument("--command-summary", required=True)
    parser.add_argument("--criteria-json", required=True)
    parser.add_argument("--output")
    parser.add_argument("--score-output")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument(
        "--allow-dirty-source",
        action="store_true",
        help="Allow a development-only record with skill_source_dirty=true.",
    )
    args = parser.parse_args()

    task_dir = Path(args.task_dir).expanduser().resolve()
    skill_root = Path(args.skill_root).expanduser().resolve()
    canonical_skill_root = Path(args.canonical_skill_root).expanduser().resolve()
    output = Path(args.output).expanduser().resolve() if args.output else task_dir / f"{args.agent}-output.md"
    score_output = (
        Path(args.score_output).expanduser().resolve()
        if args.score_output
        else task_dir / f"score.{args.agent}.json"
    )
    criteria_path = Path(args.criteria_json).expanduser().resolve()

    for path, label in (
        (task_dir / "prompt.md", "prompt"),
        (task_dir / "scorecard.md", "scorecard"),
        (output, "agent output"),
        (criteria_path, "criteria JSON"),
    ):
        if not path.is_file():
            parser.error(f"{label} does not exist: {path}")

    provenance = skill_provenance(skill_root)
    if provenance.get("skill_source_dirty") is not False and not args.allow_dirty_source:
        parser.error("refusing to record certified evidence from a dirty skill source")

    try:
        criteria = json.loads(criteria_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        parser.error(f"invalid criteria JSON: {exc}")
    if not isinstance(criteria, dict):
        parser.error("criteria JSON must contain an object")

    weights = scorecard_weights(task_dir / "scorecard.md")
    if set(weights) != set(OBSERVED_REQUIRED_CRITERIA):
        parser.error("scorecard does not expose the canonical seven criteria")

    normalized: dict[str, dict[str, object]] = {}
    score = 0
    for criterion in OBSERVED_REQUIRED_CRITERIA:
        raw = criteria.get(criterion)
        if not isinstance(raw, dict):
            parser.error(f"criteria JSON is missing object {criterion!r}")
        earned = raw.get("earned")
        passed = raw.get("passed")
        note = raw.get("note")
        weight = weights[criterion]
        if not isinstance(earned, int) or isinstance(earned, bool) or not 0 <= earned <= weight:
            parser.error(f"{criterion}.earned must be an integer from 0 to {weight}")
        if not isinstance(passed, bool):
            parser.error(f"{criterion}.passed must be boolean")
        if not isinstance(note, str) or len(note.strip()) < 8:
            parser.error(f"{criterion}.note must explain the score")
        normalized[criterion] = {
            "passed": passed,
            "earned": earned,
            "note": note.strip(),
        }
        score += earned

    try:
        output_relative = output.relative_to(task_dir).as_posix()
    except ValueError:
        parser.error("agent output must be stored inside the task directory")

    payload = {
        "schema": OBSERVED_SCHEMA_V2,
        "task_id": task_dir.name,
        "agent": args.agent,
        "verified": True,
        "agent_version": args.agent_version,
        "model": args.model,
        "reasoning_profile": args.reasoning_profile,
        "runner_os": args.runner_os,
        "date": args.date,
        "prompt_sha256": sha256_text(read_text(task_dir / "prompt.md")),
        "scorecard_sha256": sha256_file(task_dir / "scorecard.md"),
        **provenance,
        "command_summary": args.command_summary,
        "output_path": output_relative,
        "output_sha256": sha256_file(output),
        "score": score,
        "criteria": normalized,
    }
    score_output.parent.mkdir(parents=True, exist_ok=True)
    score_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    errors = validate_output(task_dir, args.agent)
    errors.extend(validate_observed_score(
        task_dir,
        args.agent,
        payload["prompt_sha256"],
        skill_root=canonical_skill_root,
        require_schema_v2=True,
        require_current_source=not args.allow_dirty_source,
    ))
    if errors:
        score_output.unlink(missing_ok=True)
        parser.error("generated evidence did not validate: " + "; ".join(errors))

    print(score_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
