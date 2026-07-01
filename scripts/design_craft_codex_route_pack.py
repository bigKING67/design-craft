#!/usr/bin/env python3
"""Audit or export the local Codex frontend route toolkit.

The route planner and global frontend rules live under ``~/.codex`` on this
machine, which is intentionally outside this repository. This helper makes that
local state portable by producing a whitelisted manifest, and optionally a
copyable bundle, without putting arbitrary Codex home contents under source
control.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = "design-craft.codex-route-pack.v1"


@dataclass(frozen=True)
class PackFile:
    path: str
    required: bool
    kind: str


ROUTE_PACK_FILES = [
    PackFile("AGENTS.md", True, "global-rule"),
    PackFile("rules/frontend.md", True, "frontend-rule"),
    PackFile("tools/frontend_route_plan.sh", True, "route-planner"),
    PackFile("tools/frontend_agent_routing.json", True, "route-config"),
    PackFile("tools/frontend_worker_entry.sh", True, "worker-gate"),
    PackFile("tools/frontend_preflight_spec.json", True, "preflight-config"),
    PackFile("tools/frontend_preflight.py", True, "preflight-runner"),
    PackFile("tools/frontend_preflight_verify.sh", True, "preflight-validator"),
    PackFile("tools/agents_quality_verify.sh", True, "global-validator"),
    PackFile("tools/tests/test_frontend_route_plan.sh", True, "route-test"),
    PackFile("tools/tests/test_frontend_route_contract.sh", True, "route-test"),
    PackFile("tools/tests/test_frontend_delivery_contract.sh", True, "route-test"),
    PackFile("tools/tests/test_frontend_preflight.sh", True, "preflight-test"),
    PackFile("tools/tests/test_frontend_preflight_spec_sync.sh", True, "preflight-test"),
    PackFile("tools/frontend_authority_init.sh", False, "style-authority-helper"),
    PackFile("tools/frontend_preflight_policy.json", False, "preflight-policy"),
    PackFile("tools/frontend_preflight_policy_run.sh", False, "preflight-policy"),
    PackFile("tools/frontend_preflight_report.sh", False, "preflight-report"),
    PackFile("tools/frontend_preflight_run.sh", False, "preflight-compat"),
    PackFile("tools/frontend_preflight_log_summary.sh", False, "preflight-logs"),
    PackFile("tools/frontend_preflight_log_rotate.sh", False, "preflight-logs"),
    PackFile("tools/frontend_preflight_log_maintenance.sh", False, "preflight-logs"),
]


SUGGESTED_VALIDATION_COMMANDS = [
    "bash ~/.codex/tools/tests/test_frontend_route_plan.sh",
    "bash ~/.codex/tools/tests/test_frontend_delivery_contract.sh",
    "bash ~/.codex/tools/tests/test_frontend_route_contract.sh",
    "bash ~/.codex/tools/tests/test_frontend_preflight_spec_sync.sh",
    "bash ~/.codex/tools/tests/test_frontend_preflight.sh",
    "bash ~/.codex/tools/frontend_preflight_verify.sh",
    "bash ~/.codex/tools/agents_quality_verify.sh --fast",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def default_source_root() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_entry(source_root: Path, spec: PackFile) -> dict:
    path = source_root / spec.path
    entry = {
        "path": spec.path,
        "required": spec.required,
        "kind": spec.kind,
        "exists": path.is_file(),
    }
    if path.is_file():
        mode = path.stat().st_mode
        entry.update(
            {
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "executable": bool(mode & stat.S_IXUSR),
            }
        )
    return entry


def build_manifest(source_root: Path) -> dict:
    files = [file_entry(source_root, spec) for spec in ROUTE_PACK_FILES]
    missing_required = [
        item["path"] for item in files if item["required"] and not item["exists"]
    ]
    existing_files = [item for item in files if item["exists"]]
    return {
        "schema": SCHEMA,
        "generated_at": utc_now(),
        "source_root": str(source_root),
        "status": "ok" if not missing_required else "missing-required",
        "summary": {
            "tracked_files": len(files),
            "existing_files": len(existing_files),
            "required_files": sum(1 for item in files if item["required"]),
            "missing_required": missing_required,
        },
        "files": files,
        "validation": {
            "suggested_commands": SUGGESTED_VALIDATION_COMMANDS,
            "screenshot_policy": "Route planner decides screenshot_evidence_level=none|optional|required.",
        },
    }


def copy_pack(source_root: Path, export_dir: Path, dry_run: bool) -> list[str]:
    copied: list[str] = []
    for spec in ROUTE_PACK_FILES:
        source = source_root / spec.path
        if not source.is_file():
            continue
        destination = export_dir / spec.path
        copied.append(spec.path)
        if dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return copied


def write_manifest(payload: dict, manifest_path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def emit_human(payload: dict, copied: list[str], manifest_path: Path | None, dry_run: bool) -> None:
    summary = payload["summary"]
    print(f"schema: {payload['schema']}")
    print(f"source_root: {payload['source_root']}")
    print(f"status: {payload['status']}")
    print(
        "files: "
        f"{summary['existing_files']}/{summary['tracked_files']} existing, "
        f"{len(summary['missing_required'])} missing required"
    )
    if summary["missing_required"]:
        print("missing_required:")
        for rel_path in summary["missing_required"]:
            print(f"- {rel_path}")
    if copied:
        action = "would_copy" if dry_run else "copied"
        print(f"{action}: {len(copied)} files")
    if manifest_path is not None:
        action = "would_write_manifest" if dry_run else "manifest"
        print(f"{action}: {manifest_path}")


def self_check() -> int:
    with tempfile.TemporaryDirectory(prefix="design-craft-route-pack.") as tmp:
        root = Path(tmp) / "codex-home"
        for spec in ROUTE_PACK_FILES:
            if not spec.required:
                continue
            path = root / spec.path
            path.parent.mkdir(parents=True, exist_ok=True)
            if spec.path.endswith(".json"):
                path.write_text("{}\n", encoding="utf-8")
            else:
                path.write_text("# fixture\n", encoding="utf-8")
            if spec.path.endswith(".sh"):
                path.chmod(0o755)

        payload = build_manifest(root)
        if payload["status"] != "ok":
            print("self-check fixture unexpectedly failed", file=sys.stderr)
            print(json.dumps(payload, indent=2), file=sys.stderr)
            return 1

        export_dir = Path(tmp) / "export"
        copied = copy_pack(root, export_dir, dry_run=False)
        if len(copied) != len([item for item in ROUTE_PACK_FILES if item.required]):
            print("self-check copied an unexpected file count", file=sys.stderr)
            return 1
        manifest_path = export_dir / "codex-route-pack.manifest.json"
        write_manifest(payload, manifest_path, dry_run=False)
        if not manifest_path.is_file():
            print("self-check did not write manifest", file=sys.stderr)
            return 1

        missing = root / "tools/frontend_route_plan.sh"
        missing.unlink()
        failed = build_manifest(root)
        if failed["status"] != "missing-required":
            print("self-check missing-required fixture unexpectedly passed", file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit or export the local Codex frontend route toolkit."
    )
    parser.add_argument("--source-root", default=None, help="Codex home root; default: $CODEX_HOME or ~/.codex.")
    parser.add_argument("--export-dir", default=None, help="Optional directory to receive a whitelisted copy.")
    parser.add_argument("--manifest", default=None, help="Optional manifest output path.")
    parser.add_argument("--json", action="store_true", help="Print the manifest JSON to stdout.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when required files are missing.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be written without copying files.")
    parser.add_argument("--check", action="store_true", help="Run built-in self-check fixtures.")
    args = parser.parse_args()

    if args.check:
        return self_check()

    source_root = (
        Path(args.source_root).expanduser().resolve()
        if args.source_root
        else default_source_root().resolve()
    )
    payload = build_manifest(source_root)

    export_dir = Path(args.export_dir).expanduser().resolve() if args.export_dir else None
    manifest_path = Path(args.manifest).expanduser().resolve() if args.manifest else None
    copied: list[str] = []

    if export_dir is not None:
        if export_dir == source_root or source_root in export_dir.parents:
            print("Refusing to export the route pack inside the source Codex home.", file=sys.stderr)
            return 2
        copied = copy_pack(source_root, export_dir, dry_run=args.dry_run)
        if manifest_path is None:
            manifest_path = export_dir / "codex-route-pack.manifest.json"

    if manifest_path is not None:
        write_manifest(payload, manifest_path, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        emit_human(payload, copied, manifest_path, dry_run=args.dry_run)

    if args.strict and payload["status"] != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
