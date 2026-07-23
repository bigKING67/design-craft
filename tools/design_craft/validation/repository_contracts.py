from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from ..repo import REPO_ROOT


SCHEMA = "design-craft.repository-contracts.v1"
REQUIRED_SCHEMA = "design-craft.required-files.v1"
RELEASE_TARGETS = (
    "release-readiness-operational",
    "release-tag-verify-operational",
    "release-assets-build-operational",
    "release-assets-verify-operational",
    "release-final-verify-operational",
    "release-readiness-certified",
    "release-tag-verify-certified",
    "release-assets-build-certified",
    "release-assets-verify-certified",
    "release-final-verify-certified",
)
NOTICE_TOKENS = ("MIT", "Apache-2.0", "Vercel design reference history", "emilkowalski/skills")
RETIRED_ALIAS_BOUNDARY_DOCS = (
    "SECURITY.md",
    "docs/security/threat-model.md",
    "docs/maintenance.md",
)
RETIRED_ALIAS_BOUNDARY = "outside the v0.5 installer boundary"


def _load_required(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != REQUIRED_SCHEMA:
        raise ValueError(f"required file registry must use {REQUIRED_SCHEMA}")
    for key in ("files", "directories", "forbidden_paths"):
        values = payload.get(key)
        if (
            not isinstance(values, list)
            or not all(isinstance(item, str) and item for item in values)
            or len(values) != len(set(values))
        ):
            raise ValueError(f"required file registry {key} must contain unique strings")
    return payload


def validate(root: Path = REPO_ROOT) -> dict[str, object]:
    errors: list[str] = []
    registry_path = root / "contracts/validation/required-files.json"
    try:
        registry = _load_required(registry_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {"schema": SCHEMA, "root": str(root), "ok": False, "errors": [str(exc)]}

    for relative in registry["files"]:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")
    for relative in registry["directories"]:
        if not (root / relative).is_dir():
            errors.append(f"missing required directory: {relative}")
    for relative in registry["forbidden_paths"]:
        if (root / relative).exists() or (root / relative).is_symlink():
            errors.append(f"retired path must remain absent: {relative}")

    installer = (root / "scripts/install_local.sh").read_text(encoding="utf-8")
    if "frontend-craft" in installer or "frontend_craft" in installer:
        errors.append("installer must not manage the retired frontend-craft alias")
    for relative in RETIRED_ALIAS_BOUNDARY_DOCS:
        document = re.sub(
            r"\s+",
            " ",
            (root / relative).read_text(encoding="utf-8"),
        )
        if RETIRED_ALIAS_BOUNDARY not in document:
            errors.append(f"{relative} must document the retired alias boundary")

    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        package = json.loads((root / "package.json").read_text(encoding="utf-8"))
        lock = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))
        skill_version = (root / "skills/design-craft/VERSION").read_text(encoding="utf-8").strip()
        if re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version) is None:
            errors.append("VERSION must be a stable semantic version")
        if package.get("version") != version:
            errors.append("package.json version must match VERSION")
        if lock.get("version") != version or lock.get("packages", {}).get("", {}).get("version") != version:
            errors.append("package-lock.json versions must match VERSION")
        if skill_version != version:
            errors.append("skills/design-craft/VERSION must match VERSION")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"version metadata is invalid: {exc}")

    notices = (root / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8", errors="replace")
    for token in NOTICE_TOKENS:
        if token not in notices:
            errors.append(f"THIRD_PARTY_NOTICES.md is missing {token}")

    skill = (root / "skills/design-craft/SKILL.md").read_text(encoding="utf-8")
    for reference in sorted((root / "skills/design-craft/references").glob("*.md")):
        text = reference.read_text(encoding="utf-8")
        if len(text.splitlines()) > 100 and "## Contents" not in text:
            errors.append(f"long reference must provide Contents: {reference.relative_to(root)}")
        if reference.name not in skill:
            errors.append(f"SKILL.md does not route reference: {reference.name}")
    if "[TODO" in skill or "TODO:" in skill:
        errors.append("canonical SKILL.md must not contain TODO markers")
    if (root / "DESIGN.md").exists():
        errors.append("repository root must not contain DESIGN.md")

    makefile = (root / "Makefile").read_text(encoding="utf-8")
    for target in ("maturity-development", "maturity-operational", "maturity-certified", *RELEASE_TARGETS):
        if re.search(rf"(?m)^{re.escape(target)}(?:\s|:)", makefile) is None:
            errors.append(f"Makefile is missing target: {target}")
    source_line = next(
        (line for line in makefile.splitlines() if line.startswith("release-gate-source:")),
        "",
    )
    if "upstream-freshness" in source_line or "upstream-remote" in source_line:
        errors.append("release-gate-source must not depend on mutable upstream state")
    if "maturity-development" not in source_line:
        errors.append("release-gate-source must require maturity-development")
    for retired in ("maturity-portable:", "maturity-local:", "maturity-desktop:", "release-certify:"):
        if retired in makefile:
            errors.append(f"retired Make target must remain absent: {retired[:-1]}")

    for document in (root / "README.md", root / "docs/maintenance.md"):
        text = document.read_text(encoding="utf-8")
        for target in ("release-readiness-operational", "release-final-verify-certified"):
            if target not in text:
                errors.append(f"{document.relative_to(root)} must document {target}")

    return {
        "schema": SCHEMA,
        "root": str(root),
        "required_file_count": len(registry["files"]),
        "ok": not errors,
        "errors": errors,
    }


def self_check() -> None:
    fixture = {
        "schema": REQUIRED_SCHEMA,
        "files": ["a"],
        "directories": ["b"],
        "forbidden_paths": [],
    }
    if len(fixture["files"]) != 1 or fixture["schema"] != REQUIRED_SCHEMA:
        raise RuntimeError("repository contract self-check failed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.check:
        self_check()
    payload = validate()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif payload["ok"]:
        print(f"repository contracts verified: {payload['required_file_count']} required files")
    else:
        print("\n".join(payload["errors"]), file=sys.stderr)
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
