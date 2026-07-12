#!/usr/bin/env python3
"""Shared validation for versioned upstream absorption review state."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


CUMULATIVE_STATUSES = {
    "absorbed",
    "selective_absorbed",
    "provenance_only",
    "deferred",
}
LATEST_RANGE_STATUSES = {
    "absorbed",
    "partial",
    "provenance_only",
    "repository_operations_only",
    "deferred",
}
LEGACY_DECISION_BY_CUMULATIVE_STATUS = {
    "absorbed": "absorbed",
    "selective_absorbed": "partial",
    "provenance_only": "provenance_only",
    "deferred": "deferred",
}
MATRIX_STATUS_LABELS = (
    "absorbed",
    "partial",
    "missing-high-value",
    "intentionally-rejected",
    "provenance-only",
)


def git_output(path: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def git_success(path: Path, *args: str) -> bool:
    return (
        subprocess.run(
            ["git", "-C", str(path), *args],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def validate_review_state(name: str, meta: dict, upstream: Path) -> tuple[dict, list[str]]:
    """Validate the v2 cumulative/latest-range state plus legacy aliases."""

    errors: list[str] = []
    current = git_output(upstream, "rev-parse", "HEAD")
    fields = {
        "commit": meta.get("commit", ""),
        "reviewed_commit": meta.get("reviewed_commit", ""),
        "absorbed_commit": meta.get("absorbed_commit", ""),
        "reviewed_through_commit": meta.get("reviewed_through_commit", ""),
        "behavior_absorbed_through_commit": meta.get(
            "behavior_absorbed_through_commit", ""
        ),
        "latest_range_base_commit": meta.get("latest_range_base_commit", ""),
        "latest_range_head_commit": meta.get("latest_range_head_commit", ""),
    }
    for field, value in fields.items():
        if not re.fullmatch(r"[0-9a-f]{40}", str(value)):
            errors.append(f"{name}: {field} must be a full lowercase Git SHA")

    if current != fields["commit"]:
        errors.append(
            f"{name}: upstream checkout {current or 'unavailable'} does not match lock {fields['commit']}"
        )
    if fields["reviewed_commit"] != fields["reviewed_through_commit"]:
        errors.append(f"{name}: reviewed_commit must alias reviewed_through_commit")
    if fields["absorbed_commit"] != fields["behavior_absorbed_through_commit"]:
        errors.append(
            f"{name}: absorbed_commit must alias behavior_absorbed_through_commit"
        )
    if fields["commit"] != fields["reviewed_through_commit"]:
        errors.append(f"{name}: reviewed_through_commit must match commit")
    if fields["commit"] != fields["latest_range_head_commit"]:
        errors.append(f"{name}: latest_range_head_commit must match commit")
    if fields["latest_range_base_commit"] != fields["behavior_absorbed_through_commit"]:
        errors.append(
            f"{name}: latest_range_base_commit must match behavior_absorbed_through_commit"
        )

    cumulative = meta.get("cumulative_status", "")
    latest = meta.get("latest_range_status", "")
    if cumulative not in CUMULATIVE_STATUSES:
        errors.append(f"{name}: invalid cumulative_status {cumulative!r}")
    if latest not in LATEST_RANGE_STATUSES:
        errors.append(f"{name}: invalid latest_range_status {latest!r}")
    expected_legacy = LEGACY_DECISION_BY_CUMULATIVE_STATUS.get(cumulative)
    if expected_legacy and meta.get("decision") != expected_legacy:
        errors.append(
            f"{name}: legacy decision must be {expected_legacy!r} for cumulative_status {cumulative!r}"
        )
    if not meta.get("reviewed_at") or not meta.get("notes"):
        errors.append(f"{name}: reviewed_at and notes are required")

    for field in ("reviewed_through_commit", "behavior_absorbed_through_commit"):
        value = fields[field]
        if value and not git_success(upstream, "cat-file", "-e", f"{value}^{{commit}}"):
            errors.append(f"{name}: {field} is unavailable in the upstream checkout")
    base = fields["latest_range_base_commit"]
    head = fields["latest_range_head_commit"]
    if base and head:
        ancestor = subprocess.run(
            ["git", "-C", str(upstream), "merge-base", "--is-ancestor", base, head],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if ancestor.returncode != 0:
            errors.append(f"{name}: latest range base must be an ancestor of its head")

    return {
        "current_commit": current,
        "cumulative_status": cumulative,
        "reviewed_through_commit": fields["reviewed_through_commit"],
        "behavior_absorbed_through_commit": fields[
            "behavior_absorbed_through_commit"
        ],
        "latest_range_base_commit": base,
        "latest_range_head_commit": head,
        "latest_range_status": latest,
        "legacy_decision": meta.get("decision"),
    }, errors


def validate_matrix_vocabulary(matrix_text: str) -> list[str]:
    errors: list[str] = []
    for label in MATRIX_STATUS_LABELS:
        if f"`{label}`" not in matrix_text:
            errors.append(f"absorption matrix is missing status vocabulary: {label}")
    return errors
