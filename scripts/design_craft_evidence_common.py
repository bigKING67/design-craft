#!/usr/bin/env python3
"""Shared evidence hashing and Git provenance helpers."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


INSTALL_METADATA = ".design-craft-install.json"
DEFAULT_IGNORED_DIRS = {".git", "__pycache__"}
DEFAULT_IGNORED_FILES = {".DS_Store", INSTALL_METADATA}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def snapshot_tree(
    root: Path,
    *,
    ignored_dirs: set[str] | None = None,
    ignored_files: set[str] | None = None,
) -> dict[str, str]:
    ignored_dir_names = DEFAULT_IGNORED_DIRS | set(ignored_dirs or ())
    ignored_file_names = DEFAULT_IGNORED_FILES | set(ignored_files or ())
    values: dict[str, str] = {}
    if not root.is_dir():
        return values
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in ignored_dir_names for part in relative.parts):
            continue
        if not path.is_file() or path.name in ignored_file_names or path.suffix in {".pyc", ".pyo"}:
            continue
        values[relative.as_posix()] = sha256_file(path)
    return values


def digest_snapshot(values: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for relative, file_digest in sorted(values.items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_digest.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def tree_sha256(
    root: Path,
    *,
    ignored_dirs: set[str] | None = None,
    ignored_files: set[str] | None = None,
) -> str:
    return digest_snapshot(
        snapshot_tree(root, ignored_dirs=ignored_dirs, ignored_files=ignored_files)
    )


def git_output(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args],
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()


def git_root(path: Path) -> Path:
    return Path(git_output(path, "rev-parse", "--show-toplevel")).resolve()


def git_head(root: Path) -> str:
    return git_output(root, "rev-parse", "HEAD")


def git_dirty(root: Path, path: Path | None = None) -> bool:
    args = ["status", "--porcelain=v1", "--untracked-files=all"]
    if path is not None:
        resolved_root = root.expanduser().resolve()
        resolved_path = path.expanduser().resolve()
        try:
            relative = resolved_path.relative_to(resolved_root)
        except ValueError as exc:
            raise ValueError(f"Git dirty path must stay inside {resolved_root}: {resolved_path}") from exc
        args.extend(("--", relative.as_posix()))
    return bool(git_output(root, *args))


def git_is_ancestor(root: Path, ancestor: str, descendant: str = "HEAD") -> bool:
    result = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", ancestor, descendant],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def read_version(skill_root: Path) -> str:
    path = skill_root / "VERSION"
    return path.read_text(encoding="utf-8").strip() if path.is_file() else ""


def skill_provenance(skill_root: Path) -> dict[str, object]:
    skill_root = skill_root.expanduser().resolve()
    digest = tree_sha256(skill_root)
    metadata_path = skill_root / INSTALL_METADATA
    if metadata_path.is_file():
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
        schema = payload.get("schema")
        if schema not in {"design-craft.install.v1", "design-craft.install.v2"}:
            raise ValueError(f"unsupported installation metadata schema in {metadata_path}")
        recorded_digest = payload.get("source_tree_sha256")
        if recorded_digest != digest:
            raise ValueError(
                f"installed skill tree hash does not match {metadata_path}: "
                f"expected {recorded_digest}, observed {digest}"
            )
        skill_source_dirty = payload.get(
            "skill_source_dirty", payload.get("source_dirty")
        )
        if not isinstance(skill_source_dirty, bool):
            raise ValueError(f"installation metadata has invalid skill dirty state: {metadata_path}")
        repo_dirty = payload.get("repo_dirty")
        if schema == "design-craft.install.v2" and not isinstance(repo_dirty, bool):
            raise ValueError(f"installation metadata has invalid repo dirty state: {metadata_path}")
        return {
            "skill_version": str(payload.get("version", "")),
            "skill_source_commit": str(payload.get("source_commit", "")),
            "skill_source_dirty": skill_source_dirty,
            "repo_dirty": repo_dirty,
            "skill_tree_sha256": digest,
            "skill_path": str(skill_root),
        }

    root = git_root(skill_root)
    return {
        "skill_version": read_version(skill_root),
        "skill_source_commit": git_head(root),
        "skill_source_dirty": git_dirty(root, skill_root),
        "repo_dirty": git_dirty(root),
        "skill_tree_sha256": digest,
        "skill_path": str(skill_root),
    }
