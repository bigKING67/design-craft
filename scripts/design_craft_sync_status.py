#!/usr/bin/env python3
"""Report source/install, Codex route-pack, and optional upstream sync status."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


SCHEMA = "design-craft.sync-status.v1"
ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def parse_json_result(result: subprocess.CompletedProcess[str]) -> dict:
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "ok": False,
            "errors": [result.stderr.strip() or result.stdout.strip() or "invalid JSON output"],
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remote", action="store_true", help="Also perform the mutable upstream freshness audit.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    skill_root = Path(
        os.environ.get("DESIGN_CRAFT_SKILL_ROOT", Path.home() / ".agents/skills")
    ).expanduser()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    install_result = run(
        [
            sys.executable,
            "scripts/design_craft_install_verify.py",
            "--source",
            "skills/design-craft",
            "--installed",
            str(skill_root / "design-craft"),
            "--expected-name",
            "design-craft",
            "--expected-version",
            version,
            "--require-metadata",
            "--json",
        ]
    )
    route_result = run(
        [sys.executable, "scripts/design_craft_codex_route_pack.py", "--strict", "--json"]
    )
    install = parse_json_result(install_result)
    route_pack = parse_json_result(route_result)

    upstream: dict[str, object] = {"checked": False, "ok": None}
    if args.remote:
        upstream_result = run(
            [
                sys.executable,
                "scripts/upstream_absorption_report.py",
                "--remote-details",
                "--fail-on-unreviewed",
                "--json",
            ]
        )
        upstream = {
            "checked": True,
            "ok": upstream_result.returncode == 0,
            "report": parse_json_result(upstream_result),
            "stderr": upstream_result.stderr.strip(),
        }

    ok = bool(install.get("ok")) and route_pack.get("status") == "ok" and upstream.get("ok") is not False
    payload = {
        "schema": SCHEMA,
        "root": str(ROOT),
        "version": version,
        "ok": ok,
        "install": install,
        "route_pack": {
            "status": route_pack.get("status"),
            "source_root": route_pack.get("source_root"),
            "summary": route_pack.get("summary"),
            "semantic_validation": route_pack.get("semantic_validation"),
        },
        "upstream": upstream,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"design-craft sync status: {'ok' if ok else 'drift'}")
        print(f"install: {'ok' if install.get('ok') else 'drift'}")
        print(f"route_pack: {route_pack.get('status', 'invalid')}")
        print(f"upstream: {'not checked' if not args.remote else 'ok' if upstream.get('ok') else 'drift'}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
