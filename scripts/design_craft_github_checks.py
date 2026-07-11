#!/usr/bin/env python3
"""Require successful GitHub validation and native-runtime runs for HEAD."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


SCHEMA = "design-craft.github-checks.v1"
ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ("validate.yml", "native-runtime.yml")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    results: dict[str, object] = {}
    if not shutil.which("gh"):
        errors.append("gh CLI is required to verify remote workflow runs")
        repo = ""
        head = ""
    else:
        head_result = run(["git", "rev-parse", "HEAD"])
        head = head_result.stdout.strip()
        repo_result = run(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"])
        repo = repo_result.stdout.strip()
        if head_result.returncode != 0 or not head:
            errors.append("cannot resolve current HEAD")
        if repo_result.returncode != 0 or not repo:
            errors.append(repo_result.stderr.strip() or "cannot resolve GitHub repository")

    if repo and head:
        for workflow in WORKFLOWS:
            result = run(
                [
                    "gh",
                    "run",
                    "list",
                    "--repo",
                    repo,
                    "--workflow",
                    workflow,
                    "--commit",
                    head,
                    "--limit",
                    "20",
                    "--json",
                    "databaseId,status,conclusion,headSha,url,event,createdAt",
                ]
            )
            if result.returncode != 0:
                errors.append(result.stderr.strip() or f"cannot query {workflow}")
                results[workflow] = []
                continue
            try:
                runs = json.loads(result.stdout)
            except json.JSONDecodeError as exc:
                errors.append(f"invalid gh output for {workflow}: {exc}")
                results[workflow] = []
                continue
            matching = [item for item in runs if item.get("headSha") == head]
            successful = [
                item
                for item in matching
                if item.get("status") == "completed" and item.get("conclusion") == "success"
            ]
            results[workflow] = matching
            if not successful:
                errors.append(f"{workflow} has no successful completed run for {head}")

    payload = {
        "schema": SCHEMA,
        "root": str(ROOT),
        "repository": repo,
        "head": head,
        "workflows": results,
        "ok": not errors,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif payload["ok"]:
        print("GitHub release checks verified")
    else:
        print("\n".join(errors), file=sys.stderr)
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
