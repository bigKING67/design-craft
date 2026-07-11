#!/usr/bin/env python3
"""Verify a design-craft installation and its generated provenance metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


SCHEMA = "design-craft.install-verification.v1"
METADATA_SCHEMA = "design-craft.install.v1"
METADATA_NAME = ".design-craft-install.json"


def ignored(path: Path) -> bool:
    return (
        "__pycache__" in path.parts
        or path.name in {".DS_Store", METADATA_NAME}
        or path.suffix in {".pyc", ".pyo"}
    )


def snapshot(root: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not root.is_dir():
        return values
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ignored(path):
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        values[str(path.relative_to(root))] = digest
    return values


def tree_digest(values: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for path, file_digest in sorted(values.items()):
        digest.update(path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_digest.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def validate_metadata(
    installed: Path,
    *,
    expected_name: str | None,
    expected_version: str | None,
    expected_tree_digest: str,
) -> tuple[dict, list[str]]:
    path = installed / METADATA_NAME
    if not path.is_file():
        return {}, [f"missing installation metadata: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"invalid installation metadata: {exc}"]

    errors: list[str] = []
    if payload.get("schema") != METADATA_SCHEMA:
        errors.append(f"metadata schema must be {METADATA_SCHEMA}")
    if expected_name and payload.get("skill_name") != expected_name:
        errors.append(f"metadata skill_name must be {expected_name}")
    if expected_version and payload.get("version") != expected_version:
        errors.append(f"metadata version must be {expected_version}")
    if payload.get("source_tree_sha256") != expected_tree_digest:
        errors.append("metadata source_tree_sha256 must match the installed source tree")
    source_commit = str(payload.get("source_commit", ""))
    if source_commit != "unavailable" and not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        errors.append("metadata source_commit must be a full lowercase Git SHA or unavailable")
    if not isinstance(payload.get("source_dirty"), bool):
        errors.append("metadata source_dirty must be boolean")
    if not isinstance(payload.get("installed_at"), str) or not payload["installed_at"].endswith("Z"):
        errors.append("metadata installed_at must be a UTC timestamp ending in Z")
    if payload.get("installer_version") != 2:
        errors.append("metadata installer_version must be 2")
    for field in ("source_root", "source_path", "source_repo"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            errors.append(f"metadata {field} must be a non-empty string")
    return payload, errors


def verify(
    source: Path,
    installed: Path,
    *,
    expected_name: str | None,
    expected_version: str | None,
    require_metadata: bool,
) -> dict:
    source_files = snapshot(source)
    installed_files = snapshot(installed)
    missing = sorted(set(source_files) - set(installed_files))
    extra = sorted(set(installed_files) - set(source_files))
    changed = sorted(
        path
        for path in set(source_files) & set(installed_files)
        if source_files[path] != installed_files[path]
    )

    metadata: dict = {}
    metadata_errors: list[str] = []
    if require_metadata:
        metadata, metadata_errors = validate_metadata(
            installed,
            expected_name=expected_name,
            expected_version=expected_version,
            expected_tree_digest=tree_digest(source_files),
        )

    errors: list[str] = []
    if not source.is_dir():
        errors.append(f"source directory missing: {source}")
    if not installed.is_dir():
        errors.append(f"installed directory missing: {installed}")
    if missing:
        errors.append(f"missing files: {missing[:10]}")
    if extra:
        errors.append(f"extra files: {extra[:10]}")
    if changed:
        errors.append(f"changed files: {changed[:10]}")
    errors.extend(metadata_errors)

    return {
        "schema": SCHEMA,
        "source": str(source),
        "installed": str(installed),
        "ok": not errors,
        "source_file_count": len(source_files),
        "installed_file_count": len(installed_files),
        "missing": missing,
        "extra": extra,
        "changed": changed,
        "metadata": metadata,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--installed", required=True)
    parser.add_argument("--expected-name")
    parser.add_argument("--expected-version")
    parser.add_argument("--require-metadata", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = verify(
        Path(args.source).expanduser().resolve(),
        Path(args.installed).expanduser().resolve(),
        expected_name=args.expected_name,
        expected_version=args.expected_version,
        require_metadata=args.require_metadata,
    )
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif payload["ok"]:
        print(f"install parity verified: {payload['installed']}")
    else:
        print("\n".join(payload["errors"]), file=sys.stderr)
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
