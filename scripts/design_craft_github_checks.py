#!/usr/bin/env python3
"""Require successful GitHub validation and native-runtime runs for HEAD."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from design_craft_native_release_bundle import (
    asset_names as native_asset_names,
    validate as validate_native_release_bundle,
    validate_run_observation,
)
from design_craft_release_assets import asset_names, validate as validate_release_assets


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


def latest_matching_run(
    runs: list[dict],
    *,
    head: str,
    required_event: str | None = None,
    required_branch: str | None = None,
) -> tuple[list[dict], dict | None]:
    matching = [
        item
        for item in runs
        if item.get("headSha") == head
        and (required_event is None or item.get("event") == required_event)
        and (required_branch is None or item.get("headBranch") == required_branch)
    ]
    matching.sort(key=lambda item: str(item.get("createdAt", "")), reverse=True)
    return matching, matching[0] if matching else None


def validate_latest_run(
    workflow: str,
    runs: list[dict],
    *,
    head: str,
    required_event: str | None = None,
    required_branch: str | None = None,
) -> tuple[list[dict], dict | None, list[str]]:
    matching, latest = latest_matching_run(
        runs,
        head=head,
        required_event=required_event,
        required_branch=required_branch,
    )
    qualifiers = []
    if required_event:
        qualifiers.append(f"event={required_event}")
    if required_branch:
        qualifiers.append(f"headBranch={required_branch}")
    suffix = f" ({', '.join(qualifiers)})" if qualifiers else ""
    if latest is None:
        return matching, latest, [f"{workflow} has no run for {head}{suffix}"]
    if latest.get("status") != "completed":
        return matching, latest, [
            f"latest {workflow} run for {head}{suffix} is not completed: "
            f"{latest.get('url', 'unknown run')}"
        ]
    if latest.get("conclusion") != "success":
        return matching, latest, [
            f"latest {workflow} run for {head}{suffix} did not succeed: "
            f"{latest.get('conclusion', 'unknown')} {latest.get('url', '')}".strip()
        ]
    return matching, latest, []


def run_self_check() -> None:
    head = "a" * 40
    manual_success = {
        "databaseId": 1,
        "status": "completed",
        "conclusion": "success",
        "headSha": head,
        "headBranch": "main",
        "event": "workflow_dispatch",
        "createdAt": "2026-01-01T00:00:00Z",
        "url": "https://example.invalid/manual",
    }
    tag_failure = {
        **manual_success,
        "databaseId": 2,
        "conclusion": "failure",
        "headBranch": "v0.5.0",
        "event": "push",
        "createdAt": "2026-01-02T00:00:00Z",
        "url": "https://example.invalid/tag-failure",
    }
    _, latest, errors = validate_latest_run(
        "native-runtime.yml",
        [manual_success, tag_failure],
        head=head,
        required_event="push",
        required_branch="v0.5.0",
    )
    if latest != tag_failure or not errors:
        raise RuntimeError("tag-run validation accepted an older manual success")

    tag_success = {
        **tag_failure,
        "databaseId": 3,
        "conclusion": "success",
        "createdAt": "2026-01-03T00:00:00Z",
        "url": "https://example.invalid/tag-success",
    }
    _, latest, errors = validate_latest_run(
        "native-runtime.yml",
        [manual_success, tag_failure, tag_success],
        head=head,
        required_event="push",
        required_branch="v0.5.0",
    )
    if latest != tag_success or errors:
        raise RuntimeError("latest successful tag run did not validate")

    package_assets = set(asset_names("0.5.0"))
    native_assets = set(native_asset_names("0.5.0"))
    if len(package_assets | native_assets) != 6 or package_assets & native_assets:
        raise RuntimeError("GitHub Release contract must require six distinct assets")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--require-tag-run",
        action="store_true",
        help="Require the latest v<VERSION> tag-push run for every workflow.",
    )
    parser.add_argument(
        "--require-release-assets",
        action="store_true",
        help="Require a published GitHub Release and validated package plus native-runtime bundle assets.",
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        run_self_check()
        print("github_checks_self_check=ok")
        return 0

    errors: list[str] = []
    results: dict[str, object] = {}
    selected_runs: dict[str, object] = {}
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

    required_event: str | None = None
    required_branch: str | None = None
    if args.require_tag_run:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        required_branch = f"v{version}"
        required_event = "push"
        tag_result = run(["git", "rev-list", "-n", "1", required_branch])
        if tag_result.returncode != 0 or tag_result.stdout.strip() != head:
            errors.append(f"tag {required_branch} must exist and point to current HEAD")

    release_payload: dict[str, object] | None = None
    release_assets_validation: dict[str, object] | None = None
    if args.require_release_assets:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        release_tag = f"v{version}"
        if not repo:
            errors.append("cannot verify GitHub Release without a repository")
        else:
            release_result = run(
                ["gh", "api", f"repos/{repo}/releases/tags/{release_tag}"]
            )
            if release_result.returncode != 0:
                errors.append(
                    release_result.stderr.strip()
                    or f"GitHub Release {release_tag} does not exist"
                )
            else:
                try:
                    release_payload = json.loads(release_result.stdout)
                except json.JSONDecodeError as exc:
                    errors.append(f"invalid GitHub Release payload: {exc}")
                else:
                    if release_payload.get("draft") is True:
                        errors.append(f"GitHub Release {release_tag} must not be a draft")
                    if release_payload.get("prerelease") is True:
                        errors.append(f"GitHub Release {release_tag} must not be a prerelease")
                    if release_payload.get("tag_name") != release_tag:
                        errors.append(f"GitHub Release tag must be {release_tag}")
                    package_names = asset_names(version)
                    native_names = native_asset_names(version)
                    expected_assets = {*package_names, *native_names}
                    observed_assets = {
                        item.get("name")
                        for item in release_payload.get("assets", [])
                        if isinstance(item, dict)
                    }
                    missing_assets = sorted(expected_assets - observed_assets)
                    if missing_assets:
                        errors.append(
                            "GitHub Release is missing required assets: "
                            + ", ".join(missing_assets)
                        )
                    else:
                        with tempfile.TemporaryDirectory(
                            prefix="design-craft-release-download-"
                        ) as tmp_value:
                            download = run(
                                [
                                    "gh",
                                    "release",
                                    "download",
                                    release_tag,
                                    "--repo",
                                    repo,
                                    "--dir",
                                    tmp_value,
                                    *[
                                        argument
                                        for name in (*package_names, *native_names)
                                        for argument in ("--pattern", name)
                                    ],
                                ]
                            )
                            if download.returncode != 0:
                                errors.append(
                                    download.stderr.strip()
                                    or "cannot download GitHub Release assets"
                                )
                            else:
                                package_validation = validate_release_assets(Path(tmp_value))
                                native_validation = validate_native_release_bundle(
                                    Path(tmp_value),
                                    verify_remote_run=False,
                                    require_current_source=True,
                                )
                                release_assets_validation = {
                                    "package": package_validation,
                                    "native": native_validation,
                                }
                                errors.extend(package_validation.get("errors", []))
                                errors.extend(native_validation.get("errors", []))

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
                    "attempt,databaseId,status,conclusion,headSha,headBranch,url,event,createdAt,workflowName",
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
            matching, latest, run_errors = validate_latest_run(
                workflow,
                runs,
                head=head,
                required_event=required_event,
                required_branch=required_branch,
            )
            results[workflow] = matching
            selected_runs[workflow] = latest
            errors.extend(run_errors)

    if args.require_release_assets:
        native_validation = (
            release_assets_validation.get("native")
            if isinstance(release_assets_validation, dict)
            else None
        )
        selected_native = selected_runs.get("native-runtime.yml")
        if not isinstance(native_validation, dict):
            errors.append("native release asset validation is unavailable")
        elif not isinstance(selected_native, dict):
            errors.append("cannot bind native release assets to the selected tag run")
        else:
            manifest_run = native_validation.get("github_run")
            if not isinstance(manifest_run, dict):
                errors.append("native release manifest does not contain github_run")
            else:
                errors.extend(
                    validate_run_observation(manifest_run, expected_run=selected_native)
                )

    payload = {
        "schema": SCHEMA,
        "root": str(ROOT),
        "repository": repo,
        "head": head,
        "required_event": required_event,
        "required_branch": required_branch,
        "workflows": results,
        "selected_runs": selected_runs,
        "release": release_payload,
        "release_assets_validation": release_assets_validation,
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
