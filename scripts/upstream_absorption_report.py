#!/usr/bin/env python3
"""Report upstream submodule drift and candidate absorption surfaces."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class ChangedFile:
    status: str
    path: str
    category: str


@dataclass
class UpstreamReport:
    name: str
    repo: str
    path: str
    license: str
    locked_commit: str
    current_commit: str | None
    remote_commit: str | None
    remote_ref: str | None
    exists: bool
    is_git_repo: bool
    lock_commit_available: bool
    drift: bool
    remote_drift: bool | None
    locked_remote_drift: bool | None
    dirty: bool
    status: list[str]
    changed_files: list[ChangedFile]
    notes: list[str]


def run_git(path: Path, args: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(path), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=check,
    )


def git_output(path: Path, args: list[str]) -> str | None:
    result = run_git(path, args)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def remote_head(repo: str) -> tuple[str | None, str | None, str | None]:
    try:
        result = subprocess.run(
            ["git", "ls-remote", repo, "HEAD", "refs/heads/main", "refs/heads/master"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
            check=False,
        )
    except Exception as exc:
        return None, None, str(exc)

    if result.returncode != 0:
        return None, None, result.stderr.strip() or f"git ls-remote exited {result.returncode}"

    refs: dict[str, str] = {}
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) == 2:
            refs[fields[1]] = fields[0]

    for ref in ("HEAD", "refs/heads/main", "refs/heads/master"):
        if ref in refs:
            return refs[ref], ref, None
    return None, None, "remote did not return HEAD, main, or master"


def categorize_changed_file(upstream_name: str, file_path: str) -> str:
    normalized = file_path.lower()
    parts = set(normalized.split("/"))

    candidate_keywords = {
        "skill",
        "skills",
        "reference",
        "references",
        "scripts",
        "script",
        "tests",
        "test",
    }
    if parts & candidate_keywords:
        return "candidate_absorb"

    if upstream_name == "impeccable" and (
        normalized.startswith("cli/engine/rules/")
        or normalized.startswith("site/content/skills/")
        or normalized.startswith("site/content/reference/")
        or normalized.startswith("skill/reference/")
        or normalized.startswith("skill/scripts/")
    ):
        return "candidate_absorb"

    if upstream_name == "taste-skill" and normalized.startswith("skills/"):
        return "candidate_absorb"

    provenance_names = {
        "license",
        "readme.md",
        "changelog.md",
        "store_listing.md",
        "marketplace.json",
        "plugin.json",
        "funding.yml",
    }
    if Path(normalized).name in provenance_names:
        return "provenance_only"

    provenance_prefixes = (
        "assets/",
        "extension/icons/",
        ".github/",
        "examples/",
    )
    if normalized.startswith(provenance_prefixes):
        return "provenance_only"

    return "manual_review"


def parse_name_status(text: str, upstream_name: str) -> list[ChangedFile]:
    files: list[ChangedFile] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        fields = line.split("\t")
        status = fields[0]
        # Rename/copy status emits old and new paths; categorize the resulting path.
        path = fields[-1]
        files.append(
            ChangedFile(
                status=status,
                path=path,
                category=categorize_changed_file(upstream_name, path),
            )
        )
    return files


def build_report(root: Path, check_remote: bool = False) -> list[UpstreamReport]:
    lock_path = root / "upstreams.lock.json"
    payload = json.loads(lock_path.read_text(encoding="utf-8"))
    reports: list[UpstreamReport] = []

    for name, meta in payload.get("upstreams", {}).items():
        rel_path = meta.get("path", "")
        upstream_path = root / rel_path
        locked = meta.get("commit", "")
        notes: list[str] = []
        status_lines: list[str] = []
        changed_files: list[ChangedFile] = []

        exists = upstream_path.exists()
        is_git_repo = False
        lock_available = False
        current: str | None = None
        dirty = False
        drift = False
        remote_commit: str | None = None
        remote_ref: str | None = None
        remote_drift: bool | None = None
        locked_remote_drift: bool | None = None

        if check_remote:
            remote_commit, remote_ref, remote_error = remote_head(meta.get("repo", ""))
            if remote_error:
                notes.append(f"remote check failed: {remote_error}")

        if not exists:
            notes.append("path missing; initialize submodules before absorption review")
        else:
            current = git_output(upstream_path, ["rev-parse", "HEAD"])
            is_git_repo = current is not None
            if not is_git_repo:
                notes.append("path exists but is not a git checkout")
            else:
                lock_available = run_git(upstream_path, ["cat-file", "-e", f"{locked}^{{commit}}"]).returncode == 0
                dirty_status = git_output(upstream_path, ["status", "--short"]) or ""
                status_lines = [line for line in dirty_status.splitlines() if line.strip()]
                dirty = bool(status_lines)
                drift = bool(current and locked and current != locked)

                if dirty:
                    notes.append("submodule working tree has local changes; review before updating locks")
                if not lock_available:
                    notes.append("locked commit is not available in the local checkout")
                elif drift:
                    diff_text = git_output(upstream_path, ["diff", "--name-status", f"{locked}..HEAD"]) or ""
                    changed_files = parse_name_status(diff_text, name)
                else:
                    notes.append("upstream lock matches current checkout")

                if remote_commit:
                    remote_drift = remote_commit != current
                    locked_remote_drift = remote_commit != locked
                    if remote_drift:
                        notes.append("remote head differs from current checkout")
                    else:
                        notes.append("remote head matches current checkout")

        reports.append(
            UpstreamReport(
                name=name,
                repo=meta.get("repo", ""),
                path=rel_path,
                license=meta.get("license", ""),
                locked_commit=locked,
                current_commit=current,
                remote_commit=remote_commit,
                remote_ref=remote_ref,
                exists=exists,
                is_git_repo=is_git_repo,
                lock_commit_available=lock_available,
                drift=drift,
                remote_drift=remote_drift,
                locked_remote_drift=locked_remote_drift,
                dirty=dirty,
                status=status_lines,
                changed_files=changed_files,
                notes=notes,
            )
        )

    return reports


def print_text(reports: list[UpstreamReport]) -> None:
    for index, report in enumerate(reports):
        if index:
            print()
        print(f"{report.name}:")
        print(f"  repo: {report.repo}")
        print(f"  path: {report.path}")
        print(f"  license: {report.license}")
        print(f"  locked_commit: {report.locked_commit}")
        print(f"  current_commit: {report.current_commit or 'unavailable'}")
        if report.remote_commit:
            print(f"  remote_ref: {report.remote_ref}")
            print(f"  remote_commit: {report.remote_commit}")
        print(f"  drift: {str(report.drift).lower()}")
        if report.remote_drift is not None:
            print(f"  remote_drift: {str(report.remote_drift).lower()}")
            print(f"  locked_remote_drift: {str(report.locked_remote_drift).lower()}")
        print(f"  dirty: {str(report.dirty).lower()}")
        for note in report.notes:
            print(f"  note: {note}")

        if report.status:
            print("  working_tree_status:")
            for line in report.status:
                print(f"    {line}")

        if report.changed_files:
            counts: dict[str, int] = {}
            for changed in report.changed_files:
                counts[changed.category] = counts.get(changed.category, 0) + 1
            print("  changed_file_counts:")
            for category in ("candidate_absorb", "manual_review", "provenance_only"):
                if category in counts:
                    print(f"    {category}: {counts[category]}")
            print("  changed_files:")
            for changed in report.changed_files:
                print(f"    {changed.status}\t{changed.category}\t{changed.path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report pinned upstream drift and candidate absorption files without fetching or modifying submodules."
    )
    parser.add_argument("--root", default=str(ROOT), help="frontend-craft repo root")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--remote", action="store_true", help="Also check remote HEAD/main/master with git ls-remote")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    try:
        reports = build_report(root, check_remote=args.remote)
    except Exception as exc:
        print(f"failed to build upstream absorption report: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps([asdict(report) for report in reports], ensure_ascii=False, indent=2))
    else:
        print_text(reports)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
