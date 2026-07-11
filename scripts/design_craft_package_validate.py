#!/usr/bin/env python3
"""Validate the publishable Pi/npm package boundary and size budget."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA = "design-craft.package-verification.v1"
ROOT = Path(__file__).resolve().parents[1]
MAX_PACKED_BYTES = 1_000_000
MAX_UNPACKED_BYTES = 2_000_000
MAX_ENTRIES = 100

EXPECTED_PACKAGE_FILES = {
    "skills/design-craft",
    "LICENSE",
    "LICENSES",
    "README.md",
    "THIRD_PARTY_NOTICES.md",
    "VERSION",
}

REQUIRED_PACKED_PATHS = {
    "package.json",
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "VERSION",
    "LICENSES/Apache-2.0.txt",
    "LICENSES/MIT-upstreams.txt",
    "LICENSES/NOTICE-impeccable.md",
    "LICENSES/VERCEL-DESIGN-NOTICE.md",
    "skills/design-craft/SKILL.md",
    "skills/design-craft/VERSION",
    "skills/design-craft/COMPATIBILITY.json",
}

ALLOWED_PATHS = {
    "package.json",
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "VERSION",
}
ALLOWED_PREFIXES = ("LICENSES/", "skills/design-craft/")
FORBIDDEN_PREFIXES = (
    ".github/",
    "adapters/",
    "docs/",
    "evals/",
    "scripts/",
    "skills/frontend-craft/",
    "upstreams/",
)
PUBLIC_HOME_PATTERN = re.compile(
    r"(?:/Users/[^/\s]+|/home/[^/\s]+|[A-Za-z]:\\Users\\[^\\\s]+)"
)
TEXT_SUFFIXES = {
    "",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".swift",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def package_errors(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    configured = package.get("files")
    if not isinstance(configured, list) or any(not isinstance(item, str) for item in configured):
        errors.append("package.json files must be a string array")
    elif set(configured) != EXPECTED_PACKAGE_FILES:
        errors.append(
            "package.json files must expose only the canonical skill and required legal metadata"
        )

    pi_skills = package.get("pi", {}).get("skills") if isinstance(package.get("pi"), dict) else None
    if pi_skills != ["skills/design-craft"]:
        errors.append("package.json pi.skills must expose only skills/design-craft")
    return errors


def pack_errors(pack: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    packed_size = pack.get("size")
    unpacked_size = pack.get("unpackedSize")
    entry_count = pack.get("entryCount")
    files = pack.get("files")
    if not isinstance(packed_size, int) or packed_size > MAX_PACKED_BYTES:
        errors.append(f"packed package must be <= {MAX_PACKED_BYTES} bytes")
    if not isinstance(unpacked_size, int) or unpacked_size > MAX_UNPACKED_BYTES:
        errors.append(f"unpacked package must be <= {MAX_UNPACKED_BYTES} bytes")
    if not isinstance(entry_count, int) or entry_count > MAX_ENTRIES:
        errors.append(f"package entry count must be <= {MAX_ENTRIES}")
    if not isinstance(files, list):
        return [*errors, "npm pack result must contain a files array"]

    paths = {
        item.get("path")
        for item in files
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    missing = sorted(REQUIRED_PACKED_PATHS - paths)
    if missing:
        errors.append("package is missing required paths: " + ", ".join(missing))

    for path in sorted(paths):
        if path.startswith(FORBIDDEN_PREFIXES):
            errors.append(f"package contains forbidden path: {path}")
        elif path not in ALLOWED_PATHS and not path.startswith(ALLOWED_PREFIXES):
            errors.append(f"package contains undeclared path: {path}")
    return errors


def public_path_errors(paths: set[str]) -> list[str]:
    errors: list[str] = []
    for relative in sorted(paths):
        path = ROOT / relative
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        match = PUBLIC_HOME_PATTERN.search(text)
        if match:
            errors.append(f"packed text exposes a user-home path: {relative}: {match.group(0)}")
    return errors


def npm_pack() -> tuple[dict[str, Any], list[str]]:
    completed = subprocess.run(
        ["npm", "pack", "--dry-run", "--json", "--ignore-scripts"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "unknown npm pack error"
        return {}, [f"npm pack --dry-run failed: {detail}"]
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {}, [f"npm pack returned invalid JSON: {exc}"]
    if not isinstance(payload, list) or len(payload) != 1 or not isinstance(payload[0], dict):
        return {}, ["npm pack must return exactly one package object"]
    return payload[0], []


def validate() -> dict[str, Any]:
    errors: list[str] = []
    try:
        package = read_json(ROOT / "package.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        package = {}
        errors.append(f"package.json is invalid: {exc}")
    errors.extend(package_errors(package))

    pack, npm_errors = npm_pack()
    errors.extend(npm_errors)
    if pack:
        errors.extend(pack_errors(pack))
        paths = {
            item["path"]
            for item in pack.get("files", [])
            if isinstance(item, dict) and isinstance(item.get("path"), str)
        }
        errors.extend(public_path_errors(paths))

    return {
        "schema": SCHEMA,
        "root": str(ROOT),
        "package": package.get("name"),
        "version": package.get("version"),
        "packed_bytes": pack.get("size"),
        "unpacked_bytes": pack.get("unpackedSize"),
        "entry_count": pack.get("entryCount"),
        "max_packed_bytes": MAX_PACKED_BYTES,
        "max_unpacked_bytes": MAX_UNPACKED_BYTES,
        "max_entries": MAX_ENTRIES,
        "ok": not errors,
        "errors": errors,
    }


def self_check() -> list[str]:
    errors: list[str] = []
    valid_package = {
        "files": sorted(EXPECTED_PACKAGE_FILES),
        "pi": {"skills": ["skills/design-craft"]},
    }
    if package_errors(valid_package):
        errors.append("package validator rejected the valid package boundary fixture")

    valid_pack = {
        "size": 100,
        "unpackedSize": 200,
        "entryCount": len(REQUIRED_PACKED_PATHS),
        "files": [{"path": path} for path in sorted(REQUIRED_PACKED_PATHS)],
    }
    if pack_errors(valid_pack):
        errors.append("package validator rejected the valid npm pack fixture")

    oversized = dict(valid_pack, size=MAX_PACKED_BYTES + 1)
    if not any("packed package" in item for item in pack_errors(oversized)):
        errors.append("package validator did not reject an oversized package")

    forbidden = dict(
        valid_pack,
        entryCount=len(REQUIRED_PACKED_PATHS) + 1,
        files=[*valid_pack["files"], {"path": "upstreams/example/LICENSE"}],
    )
    if not any("forbidden path" in item for item in pack_errors(forbidden)):
        errors.append("package validator did not reject an upstream payload")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Run offline validator invariants.")
    parser.add_argument("--validate", action="store_true", help="Run npm pack and validate the package.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.check and not args.validate:
        args.validate = True

    errors: list[str] = []
    if args.check:
        errors.extend(self_check())
    payload = validate() if args.validate else {
        "schema": SCHEMA,
        "root": str(ROOT),
        "ok": True,
        "errors": [],
    }
    errors.extend(payload["errors"])
    payload["errors"] = errors
    payload["ok"] = not errors

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif payload["ok"]:
        print(
            "package verified: "
            f"{payload.get('packed_bytes', 'n/a')} packed bytes, "
            f"{payload.get('unpacked_bytes', 'n/a')} unpacked bytes, "
            f"{payload.get('entry_count', 'n/a')} files"
        )
    else:
        print("\n".join(errors), file=sys.stderr)
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
