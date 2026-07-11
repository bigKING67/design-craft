#!/usr/bin/env python3
"""Validate design-craft version, release metadata, and repository state."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


SCHEMA = "design-craft.release-verification.v1"
ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def release_section(changelog: str, version: str) -> str:
    match = re.search(
        rf"^## {re.escape(version)} - (?P<label>[^\n]+)\n(?P<body>.*?)(?=^## |\Z)",
        changelog,
        flags=re.M | re.S,
    )
    return match.group(0) if match else ""


def validate(*, certify: bool, require_tag: bool, require_remote: bool) -> dict:
    errors: list[str] = []
    version = read(ROOT / "VERSION")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        errors.append("VERSION must be a stable semantic version")

    try:
        package = json.loads(read(ROOT / "package.json"))
        lock = json.loads(read(ROOT / "package-lock.json"))
        compatibility = json.loads(read(ROOT / "skills/design-craft/COMPATIBILITY.json"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"release JSON metadata is invalid: {exc}")
        package = {}
        lock = {}
        compatibility = {}

    if package.get("version") != version:
        errors.append("package.json version must match VERSION")
    if lock.get("version") != version or lock.get("packages", {}).get("", {}).get("version") != version:
        errors.append("package-lock.json versions must match VERSION")
    if read(ROOT / "skills/design-craft/VERSION") != version:
        errors.append("skills/design-craft/VERSION must match VERSION")

    evidence_contracts = compatibility.get("evidence_contracts", {})
    expected_contracts = {
        "cross_agent": "design-craft.cross-agent-score.v2",
        "native_runtime": "design-craft.native-runtime-evidence.v2",
        "release_verification": SCHEMA,
        "github_checks": "design-craft.github-checks.v1",
    }
    for key, expected in expected_contracts.items():
        if evidence_contracts.get(key) != expected:
            errors.append(f"COMPATIBILITY.json evidence_contracts.{key} must be {expected}")

    changelog = read(ROOT / "CHANGELOG.md")
    section = release_section(changelog, version)
    if not section:
        errors.append(f"CHANGELOG.md must contain a {version} release section")
    else:
        for token in ("web", "iOS", "Android", "adaptive", "95", "100"):
            if token not in section:
                errors.append(f"{version} changelog section must mention {token}")
        if certify:
            header = section.splitlines()[0]
            if not re.fullmatch(rf"## {re.escape(version)} - [0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}", header):
                errors.append("certification requires a dated, non-Unreleased changelog section")

    status = run_git("status", "--porcelain=v1", "--untracked-files=all")
    if status.returncode != 0:
        errors.append("cannot inspect Git worktree state")
    elif certify and status.stdout.strip():
        errors.append("certification requires a clean Git worktree")

    head = run_git("rev-parse", "HEAD").stdout.strip()
    tag = f"v{version}"
    if require_tag:
        tag_result = run_git("rev-list", "-n", "1", tag)
        if tag_result.returncode != 0 or tag_result.stdout.strip() != head:
            errors.append(f"tag {tag} must exist and point to current HEAD")

    upstream_ahead = None
    upstream_behind = None
    if require_remote:
        counts = run_git("rev-list", "--left-right", "--count", "@{upstream}...HEAD")
        if counts.returncode != 0:
            errors.append("current branch must have a configured upstream")
        else:
            try:
                upstream_behind, upstream_ahead = map(int, counts.stdout.split())
            except ValueError:
                errors.append("cannot parse upstream divergence")
            else:
                if upstream_ahead or upstream_behind:
                    errors.append(
                        f"current branch must match upstream (ahead={upstream_ahead}, behind={upstream_behind})"
                    )

    return {
        "schema": SCHEMA,
        "root": str(ROOT),
        "version": version,
        "head": head,
        "tag": tag,
        "certify": certify,
        "require_tag": require_tag,
        "require_remote": require_remote,
        "upstream_ahead": upstream_ahead,
        "upstream_behind": upstream_behind,
        "ok": not errors,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--require-tag", action="store_true")
    parser.add_argument("--require-remote", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = validate(
        certify=args.certify,
        require_tag=args.require_tag,
        require_remote=args.require_remote,
    )
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif payload["ok"]:
        print(f"release contract verified for {payload['version']}")
    else:
        print("\n".join(payload["errors"]), file=sys.stderr)
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
