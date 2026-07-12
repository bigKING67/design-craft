#!/usr/bin/env python3
"""Build and validate deterministic design-craft release assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from design_craft_package_validate import pack_errors, public_path_errors


SCHEMA = "design-craft.release-assets.v1"
ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def head() -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        text=True,
    ).strip()


def asset_names(current_version: str) -> tuple[str, str, str]:
    package_name = f"design-craft-{current_version}.tgz"
    return (
        package_name,
        f"{package_name}.sha256",
        f"design-craft-v{current_version}-release-assets.json",
    )


def npm_pack(output_dir: Path) -> tuple[dict, list[str]]:
    result = subprocess.run(
        [
            "npm",
            "pack",
            "--json",
            "--ignore-scripts",
            "--pack-destination",
            str(output_dir),
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return {}, [result.stderr.strip() or result.stdout.strip() or "npm pack failed"]
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {}, [f"npm pack returned invalid JSON: {exc}"]
    if not isinstance(payload, list) or len(payload) != 1 or not isinstance(payload[0], dict):
        return {}, ["npm pack must return exactly one package object"]
    return payload[0], []


def build(output_dir: Path, *, force: bool) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    current_version = version()
    package_name, checksum_name, manifest_name = asset_names(current_version)
    expected_paths = [output_dir / name for name in (package_name, checksum_name, manifest_name)]
    existing = [path for path in expected_paths if path.exists()]
    if existing and not force:
        raise FileExistsError(
            "release assets already exist: " + ", ".join(str(path) for path in existing)
        )
    for path in existing:
        path.unlink()

    pack, errors = npm_pack(output_dir)
    errors.extend(pack_errors(pack) if pack else [])
    paths = {
        item["path"]
        for item in pack.get("files", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    errors.extend(public_path_errors(paths))
    if errors:
        raise RuntimeError("; ".join(errors))

    packed_path = output_dir / str(pack.get("filename", ""))
    canonical_path = output_dir / package_name
    if not packed_path.is_file():
        raise FileNotFoundError(f"npm pack output is missing: {packed_path}")
    if packed_path != canonical_path:
        packed_path.replace(canonical_path)
    digest = sha256_file(canonical_path)
    checksum_path = output_dir / checksum_name
    checksum_path.write_text(f"{digest}  {package_name}\n", encoding="utf-8")
    manifest = {
        "schema": SCHEMA,
        "version": current_version,
        "tag": f"v{current_version}",
        "source_commit": head(),
        "package": {
            "path": package_name,
            "bytes": canonical_path.stat().st_size,
            "sha256": digest,
            "unpacked_bytes": pack.get("unpackedSize"),
            "entry_count": pack.get("entryCount"),
        },
        "checksum": {"path": checksum_name, "sha256": sha256_file(checksum_path)},
    }
    manifest_path = output_dir / manifest_name
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return validate(output_dir)


def validate(output_dir: Path) -> dict:
    current_version = version()
    package_name, checksum_name, manifest_name = asset_names(current_version)
    package_path = output_dir / package_name
    checksum_path = output_dir / checksum_name
    manifest_path = output_dir / manifest_name
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        manifest = {}
        errors.append(f"invalid release asset manifest: {exc}")
    if manifest.get("schema") != SCHEMA:
        errors.append(f"release asset manifest schema must be {SCHEMA}")
    if manifest.get("version") != current_version or manifest.get("tag") != f"v{current_version}":
        errors.append("release asset manifest version/tag must match VERSION")
    try:
        current_head = head()
    except subprocess.CalledProcessError:
        current_head = ""
        errors.append("cannot resolve current Git HEAD for release assets")
    if manifest.get("source_commit") != current_head:
        errors.append("release asset manifest source_commit must match current HEAD")
    if not package_path.is_file():
        errors.append(f"missing release package: {package_path}")
    if not checksum_path.is_file():
        errors.append(f"missing release checksum: {checksum_path}")
    package_payload = manifest.get("package") if isinstance(manifest.get("package"), dict) else {}
    if package_path.is_file():
        digest = sha256_file(package_path)
        if package_payload.get("path") != package_name:
            errors.append("release manifest package path is invalid")
        if package_payload.get("bytes") != package_path.stat().st_size:
            errors.append("release manifest package byte count is invalid")
        if package_payload.get("sha256") != digest:
            errors.append("release manifest package hash is invalid")
        if checksum_path.is_file() and checksum_path.read_text(encoding="utf-8") != f"{digest}  {package_name}\n":
            errors.append("release checksum content does not match the package")
    checksum_payload = manifest.get("checksum") if isinstance(manifest.get("checksum"), dict) else {}
    if checksum_path.is_file():
        if checksum_payload.get("path") != checksum_name:
            errors.append("release manifest checksum path is invalid")
        if checksum_payload.get("sha256") != sha256_file(checksum_path):
            errors.append("release manifest checksum hash is invalid")
    return {
        "schema": SCHEMA,
        "root": str(output_dir),
        "version": current_version,
        "assets": [str(package_path), str(checksum_path), str(manifest_path)],
        "ok": not errors,
        "errors": errors,
    }


def self_check() -> None:
    with tempfile.TemporaryDirectory(prefix="design-craft-release-assets-") as tmp_value:
        output_dir = Path(tmp_value)
        result = build(output_dir, force=False)
        if not result["ok"]:
            raise RuntimeError("release asset self-check build failed")
        package_name, _, _ = asset_names(version())
        package_path = output_dir / package_name
        package_path.write_bytes(package_path.read_bytes() + b"tampered")
        invalid = validate(output_dir)
        if invalid["ok"] or not any("hash" in error or "checksum" in error for error in invalid["errors"]):
            raise RuntimeError("release asset self-check accepted a tampered package")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="dist/release")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.check:
        self_check()
        print("release_assets_self_check=ok")
        return 0
    if not args.build and not args.validate:
        args.validate = True
    output_dir = Path(args.output_dir).expanduser().resolve()
    try:
        payload = build(output_dir, force=args.force) if args.build else validate(output_dir)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        payload = {
            "schema": SCHEMA,
            "root": str(output_dir),
            "version": version(),
            "ok": False,
            "errors": [str(exc)],
        }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif payload["ok"]:
        print("release assets verified: " + ", ".join(payload.get("assets", [])))
    else:
        print("\n".join(payload["errors"]), file=sys.stderr)
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
