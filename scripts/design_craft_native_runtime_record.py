#!/usr/bin/env python3
"""Record one native runtime observation with hashed artifacts."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from design_craft_evidence_common import sha256_file, skill_provenance, tree_sha256


SCHEMA = "design-craft.native-runtime-evidence.v2"


def parse_assertion(raw: str) -> tuple[str, bool]:
    if "=" not in raw:
        raise argparse.ArgumentTypeError("assertion must use name=true|false")
    name, value = raw.split("=", 1)
    normalized = value.strip().lower()
    if not name.strip() or normalized not in {"true", "false"}:
        raise argparse.ArgumentTypeError("assertion must use name=true|false")
    return name.strip(), normalized == "true"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", required=True, choices=("ios", "android"))
    parser.add_argument(
        "--runtime-kind",
        required=True,
        choices=("ios_simulator", "ios_device", "android_emulator", "android_device"),
    )
    parser.add_argument("--runtime-id", required=True)
    parser.add_argument("--tool", required=True)
    parser.add_argument("--command", action="append", required=True)
    parser.add_argument("--assertion", action="append", type=parse_assertion, required=True)
    parser.add_argument("--artifact", action="append", required=True)
    parser.add_argument("--skill-root", default="skills/design-craft")
    parser.add_argument("--fixture-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    expected_prefix = "ios_" if args.platform == "ios" else "android_"
    if not args.runtime_kind.startswith(expected_prefix):
        parser.error("runtime kind does not match platform")
    assertions = dict(args.assertion)
    if len(assertions) < 3:
        parser.error("at least three distinct assertions are required")

    output = Path(args.output).expanduser()
    skill_root = Path(args.skill_root).expanduser().resolve()
    fixture_root = Path(args.fixture_root).expanduser().resolve()
    if not fixture_root.is_dir():
        parser.error(f"fixture root does not exist: {fixture_root}")
    try:
        provenance = skill_provenance(skill_root)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        parser.error(f"cannot resolve skill provenance: {exc}")
    source_commit = str(provenance.get("skill_source_commit", ""))
    if len(source_commit) != 40:
        parser.error("skill provenance must contain a full source commit")
    artifacts = []
    for raw in args.artifact:
        path = Path(raw).expanduser()
        if not path.is_file():
            parser.error(f"artifact does not exist: {path}")
        try:
            stored_path = str(path.resolve().relative_to(output.parent.resolve()))
        except ValueError:
            stored_path = raw
        artifacts.append(
            {
                "path": stored_path,
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )

    payload = {
        "schema": SCHEMA,
        "platform": args.platform,
        "verified": True,
        "runtime_kind": args.runtime_kind,
        "evidence_level": "runtime_observed",
        "observed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "runtime_id": args.runtime_id,
        "tool": args.tool,
        "source_commit": source_commit,
        "source_dirty": provenance.get("skill_source_dirty"),
        "skill_source_dirty": provenance.get("skill_source_dirty"),
        "repo_dirty": provenance.get("repo_dirty"),
        "skill_version": provenance.get("skill_version"),
        "skill_tree_sha256": provenance.get("skill_tree_sha256"),
        "fixture_tree_sha256": tree_sha256(
            fixture_root,
            ignored_dirs={"build", ".gradle"},
        ),
        "capture_context": (
            f"{os.environ.get('GITHUB_SERVER_URL')}/{os.environ.get('GITHUB_REPOSITORY')}/actions/runs/{os.environ.get('GITHUB_RUN_ID')}"
            if os.environ.get("GITHUB_ACTIONS") == "true"
            else "local"
        ),
        "commands": args.command,
        "assertions": assertions,
        "artifacts": artifacts,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
