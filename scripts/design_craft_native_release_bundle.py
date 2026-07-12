#!/usr/bin/env python3
"""Build and validate durable native-runtime GitHub Release assets."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

from design_craft_native_runtime_validate import (
    DEFAULT_FIXTURE_ROOT,
    DEFAULT_SKILL_ROOT,
    EVIDENCE_SCHEMA,
    validate_evidence,
)


SCHEMA = "design-craft.native-release-bundle.v1"
ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ".github/workflows/native-runtime.yml"
WORKFLOW_NAME = "Native runtime evidence"
NORMALIZED_MODE = 0o644
EVIDENCE_LAYOUT = {
    "ios": ("ios", "ios-observed.json", "ios_simulator"),
    "android": ("android", "android-observed.json", "android_emulator"),
    "real_device": ("real-device", "real-device-observed.json", None),
}


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def current_head() -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True
    ).strip()


def asset_names(version: str) -> tuple[str, str, str]:
    bundle = f"design-craft-v{version}-native-runtime.tgz"
    return bundle, f"{bundle}.sha256", f"design-craft-v{version}-native-runtime.json"


def safe_relative(raw: str) -> str:
    if not raw or "\\" in raw or raw.startswith("/") or raw.endswith("/"):
        raise ValueError(f"unsafe relative path: {raw!r}")
    parts = raw.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"unsafe relative path: {raw!r}")
    normalized = PurePosixPath(raw).as_posix()
    if normalized != raw:
        raise ValueError(f"non-canonical relative path: {raw!r}")
    return normalized


def parse_json_output(result: subprocess.CompletedProcess[str], label: str) -> object:
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"cannot query {label}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON from {label}: {exc}") from exc


def repository_name(explicit: str | None = None) -> str:
    if explicit:
        return explicit
    if not shutil.which("gh"):
        raise RuntimeError("gh CLI is required to inspect native runtime runs")
    result = run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"]
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(result.stderr.strip() or "cannot resolve GitHub repository")
    return result.stdout.strip()


def validate_run_observation(
    observed: dict,
    *,
    expected_run: dict | None = None,
) -> list[str]:
    errors: list[str] = []
    version = current_version()
    head = current_head()
    if not isinstance(observed.get("id"), int) or observed["id"] <= 0:
        errors.append("native GitHub run id must be a positive integer")
    if not isinstance(observed.get("attempt"), int) or observed["attempt"] <= 0:
        errors.append("native GitHub run attempt must be a positive integer")
    if observed.get("workflow") != WORKFLOW_PATH:
        errors.append(f"native GitHub run workflow must be {WORKFLOW_PATH}")
    if observed.get("workflow_name") != WORKFLOW_NAME:
        errors.append(f"native GitHub run workflow_name must be {WORKFLOW_NAME}")
    if observed.get("event") != "push":
        errors.append("native GitHub run event must be push")
    if observed.get("head_branch") != f"v{version}":
        errors.append(f"native GitHub run head_branch must be v{version}")
    if observed.get("head_sha") != head:
        errors.append("native GitHub run head_sha must match current HEAD")
    if observed.get("status") != "completed":
        errors.append("native GitHub run status must be completed")
    if observed.get("conclusion") != "success":
        errors.append("native GitHub run conclusion must be success")
    repository = observed.get("repository")
    if not isinstance(repository, str) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository
    ):
        errors.append("native GitHub run repository must be owner/name")
    url = observed.get("url")
    if not isinstance(url, str) or not re.fullmatch(
        r"https://github\.com/[^/]+/[^/]+/actions/runs/[0-9]+", url
    ):
        errors.append("native GitHub run url must identify a GitHub Actions run")

    if expected_run is not None:
        expected_values = {
            "id": expected_run.get("databaseId", expected_run.get("id")),
            "attempt": expected_run.get("attempt"),
            "workflow_name": expected_run.get(
                "workflowName", expected_run.get("workflow_name")
            ),
            "event": expected_run.get("event"),
            "head_branch": expected_run.get(
                "headBranch", expected_run.get("head_branch")
            ),
            "head_sha": expected_run.get("headSha", expected_run.get("head_sha")),
            "status": expected_run.get("status"),
            "conclusion": expected_run.get("conclusion"),
            "url": expected_run.get("url"),
        }
        for key, expected_value in expected_values.items():
            if expected_value is not None and observed.get(key) != expected_value:
                errors.append(
                    f"native release manifest run {key} must match the selected tag run"
                )
    return errors


def latest_native_tag_run(repository: str) -> dict:
    head = current_head()
    tag = f"v{current_version()}"
    result = run(
        [
            "gh",
            "run",
            "list",
            "--repo",
            repository,
            "--workflow",
            "native-runtime.yml",
            "--commit",
            head,
            "--limit",
            "20",
            "--json",
            "attempt,databaseId,status,conclusion,headSha,headBranch,url,event,createdAt,workflowName",
        ]
    )
    payload = parse_json_output(result, "native-runtime.yml runs")
    if not isinstance(payload, list):
        raise RuntimeError("native-runtime.yml run list must be an array")
    matching = [
        item
        for item in payload
        if isinstance(item, dict)
        and item.get("headSha") == head
        and item.get("headBranch") == tag
        and item.get("event") == "push"
    ]
    matching.sort(key=lambda item: str(item.get("createdAt", "")), reverse=True)
    if not matching:
        raise RuntimeError(f"native-runtime.yml has no tag-push run for {tag} at {head}")
    latest = matching[0]
    if latest.get("status") != "completed" or latest.get("conclusion") != "success":
        raise RuntimeError(
            "latest native-runtime.yml tag-push run is not completed/success: "
            + str(latest.get("url", "unknown run"))
        )
    return latest


def observe_run(
    run_id: str | int,
    *,
    repository: str | None = None,
    require_latest: bool = True,
) -> dict:
    raw_id = str(run_id)
    if not re.fullmatch(r"[1-9][0-9]*", raw_id):
        raise ValueError("native GitHub run id must contain only decimal digits")
    repo = repository_name(repository)
    view = parse_json_output(
        run(
            [
                "gh",
                "run",
                "view",
                raw_id,
                "--repo",
                repo,
                "--json",
                "attempt,conclusion,databaseId,event,headBranch,headSha,status,url,workflowName",
            ]
        ),
        f"GitHub run {raw_id}",
    )
    api = parse_json_output(
        run(["gh", "api", f"repos/{repo}/actions/runs/{raw_id}"]),
        f"GitHub run API {raw_id}",
    )
    if not isinstance(view, dict) or not isinstance(api, dict):
        raise RuntimeError("GitHub run observation must be an object")
    observed = {
        "id": view.get("databaseId"),
        "attempt": view.get("attempt"),
        "workflow": api.get("path"),
        "workflow_name": view.get("workflowName"),
        "event": view.get("event"),
        "head_branch": view.get("headBranch"),
        "head_sha": view.get("headSha"),
        "status": view.get("status"),
        "conclusion": view.get("conclusion"),
        "url": view.get("url"),
        "repository": repo,
    }
    errors = validate_run_observation(observed)
    if api.get("id") != observed["id"]:
        errors.append("gh run view and Actions API disagree on run id")
    if api.get("run_attempt") != observed["attempt"]:
        errors.append("gh run view and Actions API disagree on run attempt")
    if api.get("html_url") != observed["url"]:
        errors.append("gh run view and Actions API disagree on run url")
    if require_latest:
        latest = latest_native_tag_run(repo)
        if latest.get("databaseId") != observed["id"]:
            errors.append("selected run is not the latest successful native tag-push run")
        errors.extend(validate_run_observation(observed, expected_run=latest))
    if errors:
        raise RuntimeError("; ".join(errors))
    return observed


def copy_evidence(source_dir: Path, target_dir: Path, json_name: str) -> dict:
    source_dir = source_dir.expanduser().resolve()
    source_json = source_dir / json_name
    if source_json.is_symlink() or not source_json.is_file():
        raise FileNotFoundError(f"native evidence JSON is missing or unsafe: {source_json}")
    payload = json.loads(source_json.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"native evidence JSON must be an object: {source_json}")
    target_dir.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(source_json, target_dir / json_name)
    observed_paths: set[str] = set()
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError(f"native evidence artifacts must be an array: {source_json}")
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError(f"native evidence artifact must be an object: {source_json}")
        relative_raw = artifact.get("path")
        if not isinstance(relative_raw, str):
            raise ValueError(f"native artifact path is missing: {source_json}")
        relative = safe_relative(relative_raw)
        if relative in observed_paths:
            raise ValueError(f"duplicate native artifact path: {relative}")
        observed_paths.add(relative)
        source = source_dir / Path(relative)
        resolved_source = source.resolve()
        if source.is_symlink() or not source.is_file():
            raise FileNotFoundError(f"native artifact is missing or unsafe: {source}")
        if source_dir != resolved_source and source_dir not in resolved_source.parents:
            raise ValueError(f"native artifact escapes its evidence root: {source}")
        destination = target_dir / Path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    return payload


def evidence_members(prefix: str, json_name: str, payload: dict) -> set[str]:
    expected = {f"{prefix}/{json_name}"}
    artifact_paths: set[str] = set()
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError(f"{json_name} artifacts must be an array")
    for artifact in artifacts:
        if not isinstance(artifact, dict) or not isinstance(artifact.get("path"), str):
            raise ValueError(f"{json_name} contains an invalid artifact")
        relative = safe_relative(artifact["path"])
        if relative in artifact_paths:
            raise ValueError(f"{json_name} repeats artifact path {relative}")
        artifact_paths.add(relative)
        expected.add(f"{prefix}/{relative}")
    return expected


def archive_files(evidence_root: Path, payloads: dict[str, dict]) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for key, payload in payloads.items():
        prefix, json_name, _ = EVIDENCE_LAYOUT[key]
        for relative in evidence_members(prefix, json_name, payload):
            path = evidence_root / Path(relative)
            if path.is_symlink() or not path.is_file():
                raise FileNotFoundError(f"native release member is missing or unsafe: {path}")
            files[relative] = path.read_bytes()
    return files


def regular_tar_info(name: str, size: int) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.size = size
    info.mode = NORMALIZED_MODE
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.type = tarfile.REGTYPE
    return info


def write_deterministic_tar(files: dict[str, bytes], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with tarfile.open(
                fileobj=zipped, mode="w", format=tarfile.USTAR_FORMAT
            ) as archive:
                for relative, content in sorted(files.items()):
                    safe_relative(relative)
                    archive.addfile(
                        regular_tar_info(relative, len(content)), io.BytesIO(content)
                    )


def inspect_archive(bundle: Path) -> tuple[dict[str, bytes], dict[str, dict], list[str]]:
    entries: dict[str, bytes] = {}
    errors: list[str] = []
    try:
        with tarfile.open(bundle, mode="r:gz") as archive:
            for member in archive.getmembers():
                try:
                    name = safe_relative(member.name)
                except ValueError as exc:
                    errors.append(f"native bundle has an unsafe member: {exc}")
                    continue
                if name in entries:
                    errors.append(f"native bundle contains duplicate member: {name}")
                    continue
                if not member.isfile():
                    errors.append(f"native bundle member must be a regular file: {name}")
                    continue
                if member.pax_headers:
                    errors.append(f"native bundle member must not use PAX headers: {name}")
                if member.mode != NORMALIZED_MODE:
                    errors.append(f"native bundle member mode is not normalized: {name}")
                if member.mtime != 0:
                    errors.append(f"native bundle member mtime is not normalized: {name}")
                if member.uid != 0 or member.gid != 0:
                    errors.append(f"native bundle member ownership is not normalized: {name}")
                if member.uname or member.gname:
                    errors.append(f"native bundle member owner names are not normalized: {name}")
                handle = archive.extractfile(member)
                if handle is None:
                    errors.append(f"native bundle member cannot be read: {name}")
                    continue
                entries[name] = handle.read()
    except (OSError, tarfile.TarError) as exc:
        return {}, {}, [f"cannot read native release bundle: {exc}"]

    payloads: dict[str, dict] = {}
    expected: set[str] = set()
    for key, (prefix, json_name, _) in EVIDENCE_LAYOUT.items():
        member_name = f"{prefix}/{json_name}"
        raw = entries.get(member_name)
        if raw is None:
            errors.append(f"native bundle is missing required member: {member_name}")
            continue
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"native bundle contains invalid {member_name}: {exc}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"native bundle {member_name} must contain a JSON object")
            continue
        payloads[key] = payload
        try:
            expected.update(evidence_members(prefix, json_name, payload))
        except ValueError as exc:
            errors.append(f"native bundle {member_name} is invalid: {exc}")
    if len(payloads) == len(EVIDENCE_LAYOUT):
        missing = sorted(expected - set(entries))
        unexpected = sorted(set(entries) - expected)
        if missing:
            errors.append("native bundle is missing declared files: " + ", ".join(missing))
        if unexpected:
            errors.append("native bundle contains unexpected files: " + ", ".join(unexpected))
    return entries, payloads, errors


def extract_entries(entries: dict[str, bytes], target: Path) -> None:
    for relative, content in entries.items():
        safe_relative(relative)
        destination = target / Path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)


def validate_bundle_evidence(
    bundle: Path,
    *,
    require_current_source: bool,
) -> tuple[dict[str, dict], list[str]]:
    entries, payloads, errors = inspect_archive(bundle)
    if errors:
        return payloads, errors
    with tempfile.TemporaryDirectory(prefix="design-craft-native-verify-") as raw:
        extracted = Path(raw)
        extract_entries(entries, extracted)
        for key, (prefix, json_name, expected_kind) in EVIDENCE_LAYOUT.items():
            payload = payloads[key]
            platform = key if key in {"ios", "android"} else payload.get("platform")
            if platform not in {"ios", "android"}:
                errors.append("real-device evidence platform must be ios or android")
                continue
            runtime_kind = expected_kind or f"{platform}_device"
            _, evidence_errors = validate_evidence(
                extracted / prefix / json_name,
                platform,
                runtime_kind,
                require_current_source=require_current_source,
                skill_root=DEFAULT_SKILL_ROOT,
                fixture_root=DEFAULT_FIXTURE_ROOT,
            )
            errors.extend(evidence_errors)
    return payloads, errors


def evidence_summary(prefix: str, json_name: str, payload: dict, root: Path) -> dict:
    evidence_path = root / prefix / json_name
    return {
        "path": f"{prefix}/{json_name}",
        "sha256": sha256_file(evidence_path),
        "schema": payload.get("schema"),
        "platform": payload.get("platform"),
        "runtime_kind": payload.get("runtime_kind"),
        "source_commit": payload.get("source_commit"),
        "contract_sha256": payload.get("contract_sha256"),
        "artifact_count": len(payload.get("artifacts", [])),
    }


def publish_assets(staging: Path, output_dir: Path, names: tuple[str, ...], *, force: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    existing = [output_dir / name for name in names if (output_dir / name).exists()]
    if existing and not force:
        raise FileExistsError(
            "native release assets already exist: "
            + ", ".join(str(path) for path in existing)
        )
    with tempfile.TemporaryDirectory(
        prefix=".native-release-backup-", dir=output_dir
    ) as backup_value:
        backup = Path(backup_value)
        moved_existing: list[tuple[Path, Path]] = []
        published: list[Path] = []
        try:
            for destination in existing:
                backup_path = backup / destination.name
                destination.replace(backup_path)
                moved_existing.append((destination, backup_path))
            for name in names:
                destination = output_dir / name
                (staging / name).replace(destination)
                published.append(destination)
        except OSError:
            for destination in published:
                destination.unlink(missing_ok=True)
            for destination, backup_path in moved_existing:
                if backup_path.exists():
                    backup_path.replace(destination)
            raise


def build_from_sources(
    output_dir: Path,
    run_observation: dict,
    *,
    ios_source: Path,
    android_source: Path,
    real_device_source: Path,
    force: bool,
    require_current_source: bool,
) -> dict:
    run_errors = validate_run_observation(run_observation)
    if run_errors:
        raise RuntimeError("; ".join(run_errors))
    version = current_version()
    bundle_name, checksum_name, manifest_name = asset_names(version)
    names = (bundle_name, checksum_name, manifest_name)
    with tempfile.TemporaryDirectory(prefix="design-craft-native-release-") as tmp_value:
        tmp = Path(tmp_value)
        evidence_root = tmp / "evidence"
        payloads = {
            "ios": copy_evidence(
                ios_source, evidence_root / EVIDENCE_LAYOUT["ios"][0], "ios-observed.json"
            ),
            "android": copy_evidence(
                android_source,
                evidence_root / EVIDENCE_LAYOUT["android"][0],
                "android-observed.json",
            ),
            "real_device": copy_evidence(
                real_device_source,
                evidence_root / EVIDENCE_LAYOUT["real_device"][0],
                "real-device-observed.json",
            ),
        }
        bundle_path = tmp / bundle_name
        write_deterministic_tar(archive_files(evidence_root, payloads), bundle_path)
        validated_payloads, errors = validate_bundle_evidence(
            bundle_path, require_current_source=require_current_source
        )
        if errors:
            raise RuntimeError("; ".join(errors))
        if require_current_source:
            for key, payload in validated_payloads.items():
                if key in {"ios", "android"} and payload.get(
                    "source_commit"
                ) != run_observation.get("head_sha"):
                    raise RuntimeError(
                        f"{key} CI evidence source_commit must match the selected tag run"
                    )
                if payload.get("schema") != EVIDENCE_SCHEMA:
                    raise RuntimeError(
                        f"{key} native evidence must use the current evidence schema"
                    )
        digest = sha256_file(bundle_path)
        checksum_path = tmp / checksum_name
        checksum_path.write_text(f"{digest}  {bundle_name}\n", encoding="utf-8")
        manifest = {
            "schema": SCHEMA,
            "version": version,
            "tag": f"v{version}",
            "source_commit": current_head(),
            "github_run": run_observation,
            "bundle": {
                "path": bundle_name,
                "bytes": bundle_path.stat().st_size,
                "sha256": digest,
            },
            "checksum": {
                "path": checksum_name,
                "sha256": sha256_file(checksum_path),
            },
            "evidence": {
                key: evidence_summary(
                    EVIDENCE_LAYOUT[key][0], EVIDENCE_LAYOUT[key][1], payload, evidence_root
                )
                for key, payload in payloads.items()
            },
        }
        manifest_path = tmp / manifest_name
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        staged_validation = validate(
            tmp,
            expected_run=run_observation,
            verify_remote_run=False,
            require_current_source=require_current_source,
        )
        if not staged_validation["ok"]:
            raise RuntimeError("; ".join(staged_validation["errors"]))
        publish_assets(tmp, output_dir, names, force=force)
    return validate(
        output_dir,
        expected_run=run_observation,
        verify_remote_run=False,
        require_current_source=require_current_source,
    )


def build(
    output_dir: Path,
    run_id: str,
    *,
    real_device_root: Path,
    repository: str | None,
    force: bool,
) -> dict:
    observed_run = observe_run(run_id, repository=repository, require_latest=True)
    with tempfile.TemporaryDirectory(prefix="design-craft-native-download-") as tmp_value:
        download_root = Path(tmp_value)
        download = run(
            [
                "gh",
                "run",
                "download",
                str(observed_run["id"]),
                "--repo",
                observed_run["repository"],
                "--dir",
                str(download_root),
            ]
        )
        if download.returncode != 0:
            raise RuntimeError(
                download.stderr.strip() or f"cannot download run {observed_run['id']}"
            )
        return build_from_sources(
            output_dir,
            observed_run,
            ios_source=download_root / f"native-runtime-ios-{observed_run['id']}",
            android_source=download_root
            / f"native-runtime-android-{observed_run['id']}",
            real_device_source=real_device_root,
            force=force,
            require_current_source=True,
        )


def validate(
    output_dir: Path,
    *,
    expected_run: dict | None = None,
    verify_remote_run: bool = False,
    require_current_source: bool = True,
) -> dict:
    version = current_version()
    bundle_name, checksum_name, manifest_name = asset_names(version)
    bundle_path = output_dir / bundle_name
    checksum_path = output_dir / checksum_name
    manifest_path = output_dir / manifest_name
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        manifest = {}
        errors.append(f"invalid native release manifest: {exc}")
    if manifest.get("schema") != SCHEMA:
        errors.append(f"native release manifest schema must be {SCHEMA}")
    if manifest.get("version") != version or manifest.get("tag") != f"v{version}":
        errors.append("native release manifest version/tag must match VERSION")
    if manifest.get("source_commit") != current_head():
        errors.append("native release manifest source_commit must match current HEAD")
    run_payload = manifest.get("github_run")
    if not isinstance(run_payload, dict):
        errors.append("native release manifest github_run must be an object")
        run_payload = {}
    else:
        errors.extend(validate_run_observation(run_payload, expected_run=expected_run))
        if verify_remote_run and not errors:
            try:
                live_run = observe_run(
                    run_payload.get("id", ""),
                    repository=run_payload.get("repository"),
                    require_latest=True,
                )
            except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
                errors.append(f"cannot verify native release GitHub run: {exc}")
            else:
                errors.extend(validate_run_observation(run_payload, expected_run=live_run))

    bundle_payload = (
        manifest.get("bundle") if isinstance(manifest.get("bundle"), dict) else {}
    )
    checksum_payload = (
        manifest.get("checksum") if isinstance(manifest.get("checksum"), dict) else {}
    )
    if not bundle_path.is_file():
        errors.append(f"missing native release bundle: {bundle_path}")
    else:
        digest = sha256_file(bundle_path)
        if bundle_payload.get("path") != bundle_name:
            errors.append("native release bundle path is invalid")
        if bundle_payload.get("bytes") != bundle_path.stat().st_size:
            errors.append("native release bundle byte count is invalid")
        if bundle_payload.get("sha256") != digest:
            errors.append("native release bundle hash is invalid")
        payloads, bundle_errors = validate_bundle_evidence(
            bundle_path, require_current_source=require_current_source
        )
        errors.extend(bundle_errors)
        manifest_evidence = manifest.get("evidence")
        if not isinstance(manifest_evidence, dict):
            errors.append("native release manifest evidence must be an object")
        elif len(payloads) == len(EVIDENCE_LAYOUT):
            with tempfile.TemporaryDirectory(prefix="design-craft-native-summary-") as raw:
                extracted = Path(raw)
                entries, _, inspect_errors = inspect_archive(bundle_path)
                errors.extend(inspect_errors)
                if not inspect_errors:
                    extract_entries(entries, extracted)
                    for key, payload in payloads.items():
                        expected = evidence_summary(
                            EVIDENCE_LAYOUT[key][0],
                            EVIDENCE_LAYOUT[key][1],
                            payload,
                            extracted,
                        )
                        if manifest_evidence.get(key) != expected:
                            errors.append(
                                f"native release manifest evidence.{key} is invalid"
                            )
    if not checksum_path.is_file():
        errors.append(f"missing native release checksum: {checksum_path}")
    elif bundle_path.is_file():
        digest = sha256_file(bundle_path)
        if checksum_path.read_text(encoding="utf-8") != f"{digest}  {bundle_name}\n":
            errors.append("native release checksum does not match the bundle")
        if checksum_payload.get("path") != checksum_name:
            errors.append("native release checksum path is invalid")
        if checksum_payload.get("sha256") != sha256_file(checksum_path):
            errors.append("native release checksum metadata is invalid")
    return {
        "schema": SCHEMA,
        "root": str(output_dir),
        "version": version,
        "github_run": run_payload,
        "assets": [str(bundle_path), str(checksum_path), str(manifest_path)],
        "ok": not errors,
        "errors": errors,
    }


def fixture_artifact(role: str, path: Path) -> dict:
    return {
        "role": role,
        "path": path.name,
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
    }


def write_fixture_evidence(root: Path, *, kind: str) -> None:
    root.mkdir(parents=True)
    platform = "ios" if kind == "ios_simulator" else "android"
    if kind == "ios_simulator":
        before = root / "before.png"
        after = root / "after.png"
        marker = root / "interaction.txt"
        launch = root / "launch.txt"
        before.write_bytes(b"\x89PNG\r\n\x1a\nbefore")
        after.write_bytes(b"\x89PNG\r\n\x1a\nafter")
        marker.write_text("Runtime interaction confirmed\n", encoding="utf-8")
        launch.write_text("fixture launched\n", encoding="utf-8")
        assertions = {
            "build_succeeded": True,
            "install_and_launch_succeeded": True,
            "runtime_interaction_observed": True,
            "before_and_after_screenshots_captured": True,
        }
        artifacts = [
            fixture_artifact("before_screenshot", before),
            fixture_artifact("after_screenshot", after),
            fixture_artifact("interaction_marker", marker),
            fixture_artifact("launch_log", launch),
        ]
        output_name = "ios-observed.json"
    else:
        before_xml = root / "before.xml"
        after_xml = root / "after.xml"
        screenshot = root / "after.png"
        launch = root / "launch.txt"
        before_xml.write_text(
            '<hierarchy><node content-desc="Native runtime evidence title" /></hierarchy>',
            encoding="utf-8",
        )
        after_xml.write_text(
            '<hierarchy><node text="Runtime interaction confirmed" /></hierarchy>',
            encoding="utf-8",
        )
        screenshot.write_bytes(b"\x89PNG\r\n\x1a\nafter")
        launch.write_text("fixture launched\n", encoding="utf-8")
        assertions = {
            "build_succeeded": True,
            "install_and_launch_succeeded": True,
            "accessibility_tree_observed": True,
            "interaction_observed": True,
            "screenshot_captured": True,
        }
        if kind == "android_device":
            assertions.update(
                {
                    "physical_device_confirmed": True,
                    "device_authorization_confirmed": True,
                }
            )
        artifacts = [
            fixture_artifact("before_accessibility_tree", before_xml),
            fixture_artifact("after_accessibility_tree", after_xml),
            fixture_artifact("after_screenshot", screenshot),
            fixture_artifact("launch_log", launch),
        ]
        output_name = (
            "real-device-observed.json"
            if kind == "android_device"
            else "android-observed.json"
        )
    payload = {
        "schema": EVIDENCE_SCHEMA,
        "platform": platform,
        "verified": True,
        "runtime_kind": kind,
        "evidence_level": "runtime_observed",
        "observed_at": "2026-01-01T00:00:00Z",
        "runtime_id_kind": "sha256",
        "runtime_id": "sha256:" + "a" * 64,
        "tool": "fixture",
        "source_commit": current_head(),
        "source_dirty": False,
        "skill_source_dirty": False,
        "repo_dirty": False,
        "skill_version": current_version(),
        "skill_tree_sha256": "b" * 64,
        "fixture_tree_sha256": "c" * 64,
        "contract_sha256": "d" * 64,
        "capture_context": "fixture",
        "commands": ["fixture command"],
        "assertions": assertions,
        "artifacts": artifacts,
    }
    (root / output_name).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_test_archive(
    output: Path,
    entries: list[tuple[tarfile.TarInfo, bytes]],
) -> None:
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode="w", format=tarfile.USTAR_FORMAT) as archive:
                for info, content in entries:
                    archive.addfile(info, io.BytesIO(content) if info.isfile() else None)


def run_self_check() -> None:
    with tempfile.TemporaryDirectory(prefix="design-craft-native-bundle-check-") as raw:
        root = Path(raw)
        ios = root / "sources/ios"
        android = root / "sources/android"
        device = root / "sources/device"
        write_fixture_evidence(ios, kind="ios_simulator")
        write_fixture_evidence(android, kind="android_emulator")
        write_fixture_evidence(device, kind="android_device")
        run_observation = {
            "id": 123,
            "attempt": 1,
            "workflow": WORKFLOW_PATH,
            "workflow_name": WORKFLOW_NAME,
            "event": "push",
            "head_branch": f"v{current_version()}",
            "head_sha": current_head(),
            "status": "completed",
            "conclusion": "success",
            "url": "https://github.com/example/design-craft/actions/runs/123",
            "repository": "example/design-craft",
        }
        mismatched_run = {
            "databaseId": 124,
            "attempt": 1,
            "workflowName": WORKFLOW_NAME,
            "event": "push",
            "headBranch": f"v{current_version()}",
            "headSha": current_head(),
            "status": "completed",
            "conclusion": "success",
            "url": "https://github.com/example/design-craft/actions/runs/124",
        }
        if not any(
            "selected tag run" in error
            for error in validate_run_observation(
                run_observation, expected_run=mismatched_run
            )
        ):
            raise RuntimeError("native bundle self-check accepted a different tag run id")
        outputs = [root / "output-a", root / "output-b"]
        for output in outputs:
            result = build_from_sources(
                output,
                run_observation,
                ios_source=ios,
                android_source=android,
                real_device_source=device,
                force=False,
                require_current_source=False,
            )
            if not result["ok"]:
                raise RuntimeError("native bundle self-check build failed")
        for name in asset_names(current_version()):
            if (outputs[0] / name).read_bytes() != (outputs[1] / name).read_bytes():
                raise RuntimeError(f"native bundle double build is not deterministic: {name}")

        bundle_name, _, _ = asset_names(current_version())
        valid_bundle = outputs[0] / bundle_name
        entries, _, errors = inspect_archive(valid_bundle)
        if errors:
            raise RuntimeError("native bundle self-check could not inspect valid archive")
        base_entries = [
            (regular_tar_info(name, len(content)), content)
            for name, content in sorted(entries.items())
        ]

        mutations: list[tuple[str, list[tuple[tarfile.TarInfo, bytes]], str]] = []
        extra = regular_tar_info("unexpected.txt", 5)
        mutations.append(("unexpected", [*base_entries, (extra, b"extra")], "unexpected"))
        duplicate_info, duplicate_content = base_entries[0]
        mutations.append(
            (
                "duplicate",
                [*base_entries, (regular_tar_info(duplicate_info.name, len(duplicate_content)), duplicate_content)],
                "duplicate",
            )
        )
        traversal = regular_tar_info("../escape.txt", 6)
        mutations.append(("traversal", [*base_entries, (traversal, b"escape")], "unsafe"))
        for label, member_type in (
            ("symlink", tarfile.SYMTYPE),
            ("hardlink", tarfile.LNKTYPE),
            ("device", tarfile.CHRTYPE),
        ):
            special = regular_tar_info(f"{label}.entry", 0)
            special.type = member_type
            special.linkname = "ios/ios-observed.json" if label != "device" else ""
            mutations.append((label, [*base_entries, (special, b"")], "regular file"))
        bad_mode_entries = [
            (regular_tar_info(info.name, len(content)), content)
            for info, content in base_entries
        ]
        bad_mode_entries[0][0].mode = 0o600
        mutations.append(("metadata", bad_mode_entries, "mode is not normalized"))

        for label, mutation_entries, expected_error in mutations:
            invalid = root / f"invalid-{label}.tgz"
            write_test_archive(invalid, mutation_entries)
            _, _, mutation_errors = inspect_archive(invalid)
            if not any(expected_error in error for error in mutation_errors):
                raise RuntimeError(
                    f"native bundle self-check accepted {label} archive mutation"
                )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="dist/release")
    parser.add_argument("--run-id")
    parser.add_argument("--repo")
    parser.add_argument("--real-device-root", default="evals/native-runtime")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--verify-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.check:
        try:
            run_self_check()
        except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
            print(f"native_release_bundle_self_check=failed: {exc}", file=sys.stderr)
            return 1
        print("native_release_bundle_self_check=ok")
        return 0
    output_dir = Path(args.output_dir).expanduser().resolve()
    if args.build and not args.run_id:
        parser.error("--build requires --run-id")
    if args.verify_run and args.build:
        parser.error("--verify-run is only valid with --validate")
    if not args.build and not args.validate:
        args.validate = True
    try:
        payload = (
            build(
                output_dir,
                args.run_id,
                real_device_root=Path(args.real_device_root).expanduser().resolve(),
                repository=args.repo,
                force=args.force,
            )
            if args.build
            else validate(
                output_dir,
                verify_remote_run=args.verify_run,
                require_current_source=True,
            )
        )
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        payload = {
            "schema": SCHEMA,
            "root": str(output_dir),
            "version": current_version(),
            "ok": False,
            "errors": [str(exc)],
        }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    elif payload["ok"]:
        print("native release bundle verified: " + ", ".join(payload.get("assets", [])))
    else:
        print("\n".join(payload["errors"]), file=sys.stderr)
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
