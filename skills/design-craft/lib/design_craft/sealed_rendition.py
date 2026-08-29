"""Hash-bound orchestration for sealed visual-rendition evidence."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable

from .comp_fidelity import CompFidelityError, compare, load_spec, read_png, validate_report


SPEC_SCHEMA = "design-craft.sealed-rendition-gate-spec.v1"
PLAN_SCHEMA = "design-craft.sealed-rendition-capture-plan.v1"
REPORT_SCHEMA = "design-craft.sealed-rendition-gate-report.v1"
VALIDATION_SCHEMA = "design-craft.sealed-rendition-gate-validation.v1"
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
MAX_JSON_BYTES = 4 * 1024 * 1024
MAX_FILE_BYTES = 128 * 1024 * 1024
MAX_AUTHORITY_FILES = 5_000
MAX_AUTHORITY_BYTES = 512 * 1024 * 1024
MAX_CAPTURES = 12
BINARY_READ_FLAGS = (
    os.O_RDONLY
    | getattr(os, "O_BINARY", 0)
    | getattr(os, "O_CLOEXEC", 0)
    | getattr(os, "O_NOFOLLOW", 0)
)
VISUAL_DECISIONS = {"pending", "pass", "blocked", "incomplete"}
ShadowLabVerifier = Callable[[Path], dict[str, Any]]


class SealedRenditionError(RuntimeError):
    """Expected gate-spec, authority, capture, or evidence failure."""


@dataclass(frozen=True)
class FileSnapshot:
    path: Path
    data: bytes
    size: int
    sha256: str


@dataclass(frozen=True)
class AuthorityState:
    snapshot: dict[str, Any]
    capture_root: Path
    protected_roots: tuple[Path, ...]


def _identity(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _snapshot_file(
    path_value: Path,
    *,
    label: str,
    max_bytes: int = MAX_FILE_BYTES,
) -> FileSnapshot:
    path = path_value.expanduser().absolute()
    if path.is_symlink():
        raise SealedRenditionError(f"{label} must be a non-symlink file")
    try:
        descriptor = os.open(path, BINARY_READ_FLAGS)
    except OSError as exc:
        raise SealedRenditionError(
            f"{label} must be an existing non-symlink file: {exc}"
        ) from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise SealedRenditionError(f"{label} must be a regular file")
        if before.st_size > max_bytes:
            raise SealedRenditionError(f"{label} exceeds {max_bytes} bytes")
        data = bytearray()
        digest = hashlib.sha256()
        while len(data) <= max_bytes:
            chunk = os.read(descriptor, min(1024 * 1024, max_bytes + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
            digest.update(chunk)
        if len(data) > max_bytes:
            raise SealedRenditionError(f"{label} exceeds {max_bytes} bytes")
        after = os.fstat(descriptor)
        if _identity(before) != _identity(after) or after.st_size != len(data):
            raise SealedRenditionError(f"{label} changed while it was read")
    finally:
        os.close(descriptor)
    return FileSnapshot(path, bytes(data), len(data), digest.hexdigest())


def _json_snapshot(path: Path, *, label: str) -> tuple[FileSnapshot, dict[str, Any]]:
    snapshot = _snapshot_file(path, label=label, max_bytes=MAX_JSON_BYTES)
    try:
        payload = json.loads(snapshot.data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise SealedRenditionError(f"{label} is invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise SealedRenditionError(f"{label} must contain a JSON object")
    return snapshot, payload


def _file_record(snapshot: FileSnapshot, *, path: str | None = None) -> dict[str, Any]:
    return {
        "path": path or str(snapshot.path),
        "bytes": snapshot.size,
        "sha256": snapshot.sha256,
    }


def _record_matches(record: Any, snapshot: FileSnapshot, *, label: str) -> None:
    expected = _file_record(snapshot, path=str(snapshot.path))
    if record != expected:
        raise SealedRenditionError(f"{label} file record mismatch")


def _canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _utc_timestamp(value: str | None, *, label: str) -> str:
    if value is None:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        )
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SealedRenditionError(f"{label} must be an ISO-8601 timestamp") from exc
    if "T" not in value or parsed.tzinfo is None:
        raise SealedRenditionError(f"{label} must include a time and UTC offset")
    return value


def _exact_fields(value: Any, fields: set[str], *, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        actual = set(value) if isinstance(value, dict) else set()
        raise SealedRenditionError(
            f"{label} fields mismatch: missing={sorted(fields - actual)}, "
            f"unsupported={sorted(actual - fields)}"
        )
    return value


def _slug(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or SLUG.fullmatch(value) is None:
        raise SealedRenditionError(f"{label} must be a lowercase slug")
    return value


def _absolute_path(value: Any, *, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise SealedRenditionError(f"{label} must be a non-empty absolute path")
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise SealedRenditionError(f"{label} must be an absolute path")
    return path.absolute()


def _safe_relative(value: Any, *, label: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value:
        raise SealedRenditionError(f"{label} must be a safe POSIX relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise SealedRenditionError(f"{label} must be a safe POSIX relative path")
    return path


def _real_directory(path: Path, *, label: str) -> Path:
    if path.is_symlink() or not path.is_dir():
        raise SealedRenditionError(f"{label} must be an existing non-symlink directory")
    return path.resolve(strict=True)


def _contained_file(root: Path, relative: PurePosixPath, *, label: str) -> Path:
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise SealedRenditionError(f"{label} must not traverse a symlink")
    try:
        current.resolve(strict=False).relative_to(root)
    except ValueError as exc:
        raise SealedRenditionError(f"{label} leaves its authority root") from exc
    if not current.is_file():
        raise SealedRenditionError(f"{label} must be an existing file")
    return current.absolute()


def _paths_overlap(left: Path, right: Path) -> bool:
    left_resolved = left.resolve(strict=False)
    right_resolved = right.resolve(strict=False)
    try:
        left_resolved.relative_to(right_resolved)
        return True
    except ValueError:
        pass
    try:
        right_resolved.relative_to(left_resolved)
        return True
    except ValueError:
        return False


def _manifest_record(value: Any, *, label: str) -> tuple[PurePosixPath, int | None, str]:
    if not isinstance(value, dict):
        raise SealedRenditionError(f"{label} must be an object")
    relative = _safe_relative(value.get("path"), label=f"{label}.path")
    expected_sha = value.get("sha256")
    if not isinstance(expected_sha, str) or SHA256.fullmatch(expected_sha) is None:
        raise SealedRenditionError(f"{label}.sha256 must be a lowercase SHA-256")
    expected_bytes = value.get("bytes")
    if expected_bytes is not None and (
        isinstance(expected_bytes, bool)
        or not isinstance(expected_bytes, int)
        or expected_bytes < 0
    ):
        raise SealedRenditionError(f"{label}.bytes must be a non-negative integer")
    return relative, expected_bytes, expected_sha


def _snapshot_declared_file(
    root: Path,
    value: Any,
    *,
    label: str,
    scope: str,
) -> dict[str, Any]:
    relative, expected_bytes, expected_sha = _manifest_record(value, label=label)
    path = _contained_file(root, relative, label=label)
    snapshot = _snapshot_file(path, label=label)
    if expected_bytes is not None and snapshot.size != expected_bytes:
        raise SealedRenditionError(f"size mismatch: {relative.as_posix()}")
    if snapshot.sha256 != expected_sha:
        raise SealedRenditionError(f"hash mismatch: {relative.as_posix()}")
    return {
        "scope": scope,
        "path": relative.as_posix(),
        "bytes": snapshot.size,
        "sha256": snapshot.sha256,
    }


def _inventory_paths(root: Path, manifest: Path) -> set[str]:
    paths: set[str] = set()
    manifest_relative = manifest.relative_to(root).as_posix()
    for current_root, directories, files in os.walk(root, followlinks=False):
        current = Path(current_root)
        directories.sort()
        files.sort()
        for name in [*directories, *files]:
            candidate = current / name
            if candidate.is_symlink():
                raise SealedRenditionError(
                    f"sealed authority contains a symlink: {candidate.relative_to(root)}"
                )
        for name in files:
            candidate = current / name
            metadata = candidate.stat()
            if not stat.S_ISREG(metadata.st_mode):
                raise SealedRenditionError(
                    f"sealed authority contains a special file: {candidate.relative_to(root)}"
                )
            relative = candidate.relative_to(root).as_posix()
            if relative != manifest_relative:
                paths.add(relative)
                if len(paths) > MAX_AUTHORITY_FILES:
                    raise SealedRenditionError("sealed authority file count exceeds the bound")
    return paths


def _snapshot_sealed_authority(authority: dict[str, Any]) -> AuthorityState:
    _exact_fields(
        authority,
        {"kind", "root", "manifest", "expected_schema", "inventory_key", "anchors"},
        label="spec.authority",
    )
    root = _real_directory(_absolute_path(authority["root"], label="authority.root"), label="authority.root")
    manifest_path = _absolute_path(
        authority["manifest"], label="authority.manifest"
    ).resolve(strict=False)
    try:
        manifest_relative = manifest_path.relative_to(root)
    except ValueError as exc:
        raise SealedRenditionError("authority.manifest must be inside authority.root") from exc
    manifest_path = _contained_file(
        root,
        PurePosixPath(manifest_relative.as_posix()),
        label="authority.manifest",
    )
    manifest_snapshot, manifest = _json_snapshot(manifest_path, label="sealed manifest")
    expected_schema = authority["expected_schema"]
    if not isinstance(expected_schema, str) or not expected_schema:
        raise SealedRenditionError("authority.expected_schema must be a non-empty string")
    if manifest.get("schema") != expected_schema:
        raise SealedRenditionError("sealed manifest schema mismatch")
    inventory_key = authority["inventory_key"]
    if not isinstance(inventory_key, str) or not inventory_key:
        raise SealedRenditionError("authority.inventory_key must be a non-empty string")
    inventory = manifest.get(inventory_key)
    if not isinstance(inventory, list) or not inventory:
        raise SealedRenditionError("sealed manifest inventory must be a non-empty array")
    if len(inventory) > MAX_AUTHORITY_FILES:
        raise SealedRenditionError("sealed manifest inventory exceeds the file-count bound")
    records: list[dict[str, Any]] = []
    expected_paths: set[str] = set()
    for index, raw in enumerate(inventory):
        record = _snapshot_declared_file(
            root,
            raw,
            label=f"sealed manifest {inventory_key}[{index}]",
            scope="inventory",
        )
        if record["path"] in expected_paths:
            raise SealedRenditionError("sealed manifest inventory paths must be unique")
        expected_paths.add(record["path"])
        records.append(record)
    actual_paths = _inventory_paths(root, manifest_path)
    if actual_paths != expected_paths:
        missing = sorted(expected_paths - actual_paths)
        unexpected = sorted(actual_paths - expected_paths)
        raise SealedRenditionError(
            f"sealed inventory membership mismatch: missing={missing}, unexpected={unexpected}"
        )

    anchors = authority["anchors"]
    if not isinstance(anchors, list) or len(anchors) > 16:
        raise SealedRenditionError("authority.anchors must be an array with at most 16 entries")
    anchor_ids: set[str] = set()
    protected_roots = [root]
    for index, anchor in enumerate(anchors):
        _exact_fields(anchor, {"id", "root", "records_key"}, label=f"authority.anchors[{index}]")
        anchor_id = _slug(anchor["id"], label=f"authority.anchors[{index}].id")
        if anchor_id in anchor_ids:
            raise SealedRenditionError("authority anchor ids must be unique")
        anchor_ids.add(anchor_id)
        anchor_root = _real_directory(
            _absolute_path(anchor["root"], label=f"authority.anchors[{index}].root"),
            label=f"authority.anchors[{index}].root",
        )
        protected_roots.append(anchor_root)
        records_key = anchor["records_key"]
        if not isinstance(records_key, str) or not records_key:
            raise SealedRenditionError("authority anchor records_key must be non-empty")
        raw_records = manifest.get(records_key)
        if isinstance(raw_records, dict):
            items = sorted(raw_records.items())
        elif isinstance(raw_records, list):
            items = [(str(item_index), item) for item_index, item in enumerate(raw_records)]
        else:
            raise SealedRenditionError(
                f"sealed manifest {records_key} must be an object or array"
            )
        for record_id, raw in items:
            record = _snapshot_declared_file(
                anchor_root,
                raw,
                label=f"sealed manifest {records_key}.{record_id}",
                scope=f"anchor:{anchor_id}",
            )
            records.append(record)

    total_bytes = manifest_snapshot.size + sum(record["bytes"] for record in records)
    if len(records) > MAX_AUTHORITY_FILES or total_bytes > MAX_AUTHORITY_BYTES:
        raise SealedRenditionError("sealed authority exceeds the processing bound")
    manifest_record = _file_record(manifest_snapshot)
    digest_input = {
        "kind": "sealed_manifest",
        "manifest": manifest_record,
        "records": records,
    }
    snapshot = {
        "kind": "sealed_manifest",
        "root": str(root),
        "manifest": manifest_record,
        "expected_schema": expected_schema,
        "record_count": len(records),
        "total_bytes": total_bytes,
        "records": records,
        "digest": _canonical_digest(digest_input),
    }
    return AuthorityState(snapshot, root, tuple(protected_roots))


def _snapshot_git_authority(
    authority: dict[str, Any],
    shadow_lab_verifier: ShadowLabVerifier | None,
) -> AuthorityState:
    _exact_fields(authority, {"kind", "shadow_lab_manifest"}, label="spec.authority")
    if shadow_lab_verifier is None:
        raise SealedRenditionError("git_commit authority requires the Shadow Lab verifier")
    manifest_path = _absolute_path(
        authority["shadow_lab_manifest"], label="authority.shadow_lab_manifest"
    )
    manifest_snapshot = _snapshot_file(
        manifest_path,
        label="Shadow Lab manifest",
        max_bytes=MAX_JSON_BYTES,
    )
    try:
        verification = shadow_lab_verifier(manifest_path)
    except Exception as exc:
        raise SealedRenditionError(f"Shadow Lab verification failed: {exc}") from exc
    source = verification.get("source")
    boundary = verification.get("boundary")
    lab = verification.get("lab")
    if (
        verification.get("ok") is not True
        or not isinstance(source, dict)
        or source.get("source_unchanged") is not True
        or not isinstance(boundary, dict)
        or boundary.get("source_writes_allowed") is not False
        or boundary.get("source_and_output_disjoint") is not True
        or not isinstance(lab, dict)
    ):
        raise SealedRenditionError("Shadow Lab authority is not verified and source-read-only")
    manifest_after = _snapshot_file(
        manifest_path,
        label="Shadow Lab manifest",
        max_bytes=MAX_JSON_BYTES,
    )
    if (
        manifest_after.size != manifest_snapshot.size
        or manifest_after.sha256 != manifest_snapshot.sha256
    ):
        raise SealedRenditionError("Shadow Lab manifest changed during verification")
    capture_root = _real_directory(
        _absolute_path(lab.get("worktree"), label="Shadow Lab worktree"),
        label="Shadow Lab worktree",
    )
    source_root = _real_directory(
        _absolute_path(source.get("repo_path"), label="Shadow Lab source repo"),
        label="Shadow Lab source repo",
    )
    commit = source.get("commit")
    if not isinstance(commit, str) or re.fullmatch(r"[0-9a-f]{40,64}", commit) is None:
        raise SealedRenditionError("Shadow Lab verification commit is invalid")
    manifest_record = _file_record(manifest_snapshot)
    digest_input = {
        "kind": "git_commit",
        "manifest": manifest_record,
        "source_repo": str(source_root),
        "commit": commit,
    }
    snapshot = {
        "kind": "git_commit",
        "root": str(capture_root),
        "shadow_lab_manifest": manifest_record,
        "source_repo": str(source_root),
        "commit": commit,
        "record_count": 1,
        "total_bytes": manifest_snapshot.size,
        "records": [
            {
                "scope": "shadow-lab",
                "path": manifest_path.name,
                "bytes": manifest_snapshot.size,
                "sha256": manifest_snapshot.sha256,
            }
        ],
        "digest": _canonical_digest(digest_input),
    }
    return AuthorityState(snapshot, capture_root, (source_root, capture_root))


def _snapshot_authority(
    authority: dict[str, Any],
    shadow_lab_verifier: ShadowLabVerifier | None,
) -> AuthorityState:
    kind = authority.get("kind") if isinstance(authority, dict) else None
    if kind == "sealed_manifest":
        return _snapshot_sealed_authority(authority)
    if kind == "git_commit":
        return _snapshot_git_authority(authority, shadow_lab_verifier)
    raise SealedRenditionError("spec.authority.kind must be sealed_manifest or git_commit")


def _capture_contract(value: Any, *, kind: str, label: str) -> dict[str, Any]:
    if kind == "browser_viewport":
        contract = _exact_fields(
            value,
            {
                "runtime",
                "viewport",
                "device_scale_factor",
                "theme",
                "network",
                "wait_for",
            },
            label=label,
        )
        if contract["runtime"] != "browser67":
            raise SealedRenditionError(f"{label}.runtime must be browser67")
        viewport = _exact_fields(
            contract["viewport"], {"width", "height"}, label=f"{label}.viewport"
        )
        for dimension in ("width", "height"):
            value = viewport[dimension]
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise SealedRenditionError(f"{label}.viewport.{dimension} must be positive")
        if contract["device_scale_factor"] != 1:
            raise SealedRenditionError(
                f"{label}.device_scale_factor must be 1 for exact-coordinate capture"
            )
        if contract["theme"] not in {"light", "dark", "system"}:
            raise SealedRenditionError(f"{label}.theme is invalid")
        if contract["network"] not in {"offline", "loopback_only"}:
            raise SealedRenditionError(f"{label}.network is invalid")
        if contract["wait_for"] != "document_complete":
            raise SealedRenditionError(f"{label}.wait_for must be document_complete")
        return contract
    if kind == "pdf_page":
        contract = _exact_fields(
            value, {"runtime", "page", "output"}, label=label
        )
        if contract["runtime"] != "pdf_renderer":
            raise SealedRenditionError(f"{label}.runtime must be pdf_renderer")
        page = contract["page"]
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise SealedRenditionError(f"{label}.page must be a positive integer")
        output = _exact_fields(
            contract["output"], {"width", "height"}, label=f"{label}.output"
        )
        for dimension in ("width", "height"):
            value = output[dimension]
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise SealedRenditionError(f"{label}.output.{dimension} must be positive")
        return contract
    raise SealedRenditionError(f"{label} has unsupported capture kind {kind!r}")


def _load_gate_spec(path: Path) -> tuple[FileSnapshot, dict[str, Any]]:
    snapshot, payload = _json_snapshot(path, label="gate spec")
    _exact_fields(payload, {"schema", "gate_id", "authority", "captures"}, label="gate spec")
    if payload["schema"] != SPEC_SCHEMA:
        raise SealedRenditionError(f"gate spec.schema must be {SPEC_SCHEMA}")
    _slug(payload["gate_id"], label="gate spec.gate_id")
    captures = payload["captures"]
    if not isinstance(captures, list) or not 1 <= len(captures) <= MAX_CAPTURES:
        raise SealedRenditionError(f"gate spec.captures must contain 1 to {MAX_CAPTURES} entries")
    capture_ids: set[str] = set()
    for index, capture in enumerate(captures):
        label = f"gate spec.captures[{index}]"
        _exact_fields(
            capture,
            {"id", "kind", "source", "reference", "comparison_spec", "contract"},
            label=label,
        )
        capture_id = _slug(capture["id"], label=f"{label}.id")
        if capture_id in capture_ids:
            raise SealedRenditionError("gate spec capture ids must be unique")
        capture_ids.add(capture_id)
        if capture["kind"] not in {"browser_viewport", "pdf_page"}:
            raise SealedRenditionError(f"{label}.kind is invalid")
        _safe_relative(capture["source"], label=f"{label}.source")
        _safe_relative(capture["reference"], label=f"{label}.reference")
        _absolute_path(capture["comparison_spec"], label=f"{label}.comparison_spec")
        _capture_contract(capture["contract"], kind=capture["kind"], label=f"{label}.contract")
    return snapshot, payload


def _planned_captures(
    spec: dict[str, Any],
    state: AuthorityState,
    output_root: Path,
) -> list[dict[str, Any]]:
    planned: list[dict[str, Any]] = []
    for ordinal, capture in enumerate(spec["captures"], start=1):
        capture_id = capture["id"]
        source = _contained_file(
            state.capture_root,
            _safe_relative(capture["source"], label=f"capture {capture_id}.source"),
            label=f"capture {capture_id}.source",
        )
        reference = _contained_file(
            state.capture_root,
            _safe_relative(capture["reference"], label=f"capture {capture_id}.reference"),
            label=f"capture {capture_id}.reference",
        )
        comparison_spec = _absolute_path(
            capture["comparison_spec"], label=f"capture {capture_id}.comparison_spec"
        )
        comparison_snapshot = _snapshot_file(
            comparison_spec,
            label=f"capture {capture_id} comparison spec",
            max_bytes=MAX_JSON_BYTES,
        )
        try:
            _, comparison = load_spec(comparison_spec)
            reference_image = read_png(reference)
        except CompFidelityError as exc:
            raise SealedRenditionError(f"capture {capture_id} preflight failed: {exc}") from exc
        coordinate = comparison["coordinate_space"]
        if [reference_image.width, reference_image.height] != [
            coordinate["width"],
            coordinate["height"],
        ]:
            raise SealedRenditionError(
                f"capture {capture_id} reference dimensions disagree with comparison spec"
            )
        contract = capture["contract"]
        contract_coordinate = (
            contract["viewport"]
            if capture["kind"] == "browser_viewport"
            else contract["output"]
        )
        if contract_coordinate != coordinate:
            raise SealedRenditionError(
                f"capture {capture_id} contract dimensions disagree with comparison spec"
            )
        source_snapshot = _snapshot_file(source, label=f"capture {capture_id} source")
        reference_snapshot = _snapshot_file(reference, label=f"capture {capture_id} reference")
        planned.append(
            {
                "ordinal": ordinal,
                "id": capture_id,
                "kind": capture["kind"],
                "source": _file_record(source_snapshot),
                "reference": {
                    **_file_record(reference_snapshot),
                    "width": reference_image.width,
                    "height": reference_image.height,
                },
                "comparison_spec": _file_record(comparison_snapshot),
                "rendered_path": str(output_root / "captures" / capture_id / "rendered.png"),
                "contract": contract,
            }
        )
    return planned


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def prepare_gate(
    *,
    spec_path: Path,
    output_root: Path,
    shadow_lab_verifier: ShadowLabVerifier | None = None,
    prepared_at: str | None = None,
) -> dict[str, Any]:
    spec_snapshot, spec = _load_gate_spec(spec_path)
    state = _snapshot_authority(spec["authority"], shadow_lab_verifier)
    output = output_root.expanduser().absolute()
    if output.exists():
        raise SealedRenditionError("output root must not already exist")
    if output.parent.is_symlink() or not output.parent.is_dir():
        raise SealedRenditionError("output parent must be an existing non-symlink directory")
    for protected in state.protected_roots:
        if _paths_overlap(output, protected):
            raise SealedRenditionError("output root must be disjoint from all authority roots")
    captures = _planned_captures(spec, state, output)
    timestamp = _utc_timestamp(prepared_at, label="prepared_at")
    plan = {
        "schema": PLAN_SCHEMA,
        "gate_id": spec["gate_id"],
        "prepared_at": timestamp,
        "spec": _file_record(spec_snapshot),
        "output_root": str(output),
        "authority": state.snapshot,
        "capture_order": [capture["id"] for capture in captures],
        "captures": captures,
        "capture_owner": "external_runtime",
        "source_writes_allowed": False,
        "closeout": {
            "comparison_engine": "design-craft.comp-fidelity-report.v1",
            "strict_validation_required": True,
            "global_pixel_pass_threshold": None,
            "human_visual_decision_required": True,
        },
    }
    stage = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=output.parent))
    try:
        for capture in captures:
            (stage / "captures" / capture["id"]).mkdir(parents=True)
        _atomic_write_json(stage / "capture-plan.json", plan)
        if output.exists():
            raise SealedRenditionError("output root appeared before atomic promotion")
        os.replace(stage, output)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return plan


def _load_plan(path: Path) -> tuple[FileSnapshot, dict[str, Any]]:
    snapshot, plan = _json_snapshot(path, label="capture plan")
    _exact_fields(
        plan,
        {
            "schema",
            "gate_id",
            "prepared_at",
            "spec",
            "output_root",
            "authority",
            "capture_order",
            "captures",
            "capture_owner",
            "source_writes_allowed",
            "closeout",
        },
        label="capture plan",
    )
    if plan["schema"] != PLAN_SCHEMA:
        raise SealedRenditionError(f"capture plan.schema must be {PLAN_SCHEMA}")
    _slug(plan["gate_id"], label="capture plan.gate_id")
    _utc_timestamp(plan["prepared_at"], label="capture plan.prepared_at")
    if plan["capture_owner"] != "external_runtime" or plan["source_writes_allowed"] is not False:
        raise SealedRenditionError("capture plan ownership boundary is invalid")
    expected_closeout = {
        "comparison_engine": "design-craft.comp-fidelity-report.v1",
        "strict_validation_required": True,
        "global_pixel_pass_threshold": None,
        "human_visual_decision_required": True,
    }
    if plan["closeout"] != expected_closeout:
        raise SealedRenditionError("capture plan closeout boundary is invalid")
    return snapshot, plan


def _validated_plan(
    plan_path: Path,
    shadow_lab_verifier: ShadowLabVerifier | None,
) -> tuple[FileSnapshot, dict[str, Any], FileSnapshot, dict[str, Any], AuthorityState]:
    plan_snapshot, plan = _load_plan(plan_path)
    if plan_snapshot.path.name != "capture-plan.json":
        raise SealedRenditionError("capture plan must be named capture-plan.json")
    output_root = _absolute_path(plan["output_root"], label="capture plan.output_root")
    if plan_snapshot.path.parent != output_root or not output_root.is_dir() or output_root.is_symlink():
        raise SealedRenditionError("capture plan path does not match its output root")
    spec_record = _exact_fields(plan["spec"], {"path", "bytes", "sha256"}, label="capture plan.spec")
    spec_path = _absolute_path(spec_record["path"], label="capture plan.spec.path")
    spec_snapshot, spec = _load_gate_spec(spec_path)
    _record_matches(spec_record, spec_snapshot, label="capture plan.spec")
    if spec["gate_id"] != plan["gate_id"]:
        raise SealedRenditionError("capture plan gate id disagrees with its spec")
    state = _snapshot_authority(spec["authority"], shadow_lab_verifier)
    if state.snapshot != plan["authority"]:
        raise SealedRenditionError("authority changed after capture preflight")
    expected_captures = _planned_captures(spec, state, output_root)
    expected_order = [capture["id"] for capture in expected_captures]
    if plan["capture_order"] != expected_order or plan["captures"] != expected_captures:
        raise SealedRenditionError("capture plan no longer matches its ordered spec contract")
    return plan_snapshot, plan, spec_snapshot, spec, state


def _visual_review(decision: str, reviewer: str | None, note: str) -> dict[str, Any]:
    if decision not in VISUAL_DECISIONS:
        raise SealedRenditionError(
            f"visual decision must be one of {sorted(VISUAL_DECISIONS)}"
        )
    if not isinstance(note, str) or not note.strip():
        raise SealedRenditionError("visual review note must be non-empty")
    if reviewer is not None and (not isinstance(reviewer, str) or not reviewer.strip()):
        raise SealedRenditionError("visual reviewer must be non-empty when provided")
    if decision in {"pass", "blocked"} and reviewer is None:
        raise SealedRenditionError("pass or blocked visual decisions require a reviewer")
    return {"decision": decision, "reviewer": reviewer, "note": note.strip()}


def _relative_file_record(path: Path, root: Path) -> dict[str, Any]:
    snapshot = _snapshot_file(path, label="gate evidence artifact")
    return _file_record(snapshot, path=path.relative_to(root).as_posix())


def closeout_gate(
    *,
    plan_path: Path,
    visual_decision: str,
    visual_note: str,
    reviewer: str | None = None,
    shadow_lab_verifier: ShadowLabVerifier | None = None,
    observed_at: str | None = None,
) -> dict[str, Any]:
    plan_snapshot, plan, spec_snapshot, spec, state = _validated_plan(
        plan_path, shadow_lab_verifier
    )
    visual_review = _visual_review(visual_decision, reviewer, visual_note)
    completed_at = _utc_timestamp(observed_at, label="observed_at")
    output_root = plan_snapshot.path.parent
    comparisons_root = output_root / "comparisons"
    report_path = output_root / "gate-report.json"
    if comparisons_root.exists() or report_path.exists():
        raise SealedRenditionError("gate closeout outputs must not already exist")
    stage = Path(tempfile.mkdtemp(prefix=".closeout-", dir=output_root))
    comparisons: list[dict[str, Any]] = []
    captures: list[dict[str, Any]] = []
    try:
        for capture in plan["captures"]:
            capture_id = capture["id"]
            rendered = _absolute_path(
                capture["rendered_path"], label=f"capture {capture_id}.rendered_path"
            )
            rendered_relative = PurePosixPath("captures") / capture_id / "rendered.png"
            expected_rendered = _contained_file(
                output_root.resolve(strict=True),
                rendered_relative,
                label=f"capture {capture_id} rendered PNG",
            )
            if rendered.resolve(strict=True) != expected_rendered.resolve(strict=True):
                raise SealedRenditionError(
                    f"capture {capture_id} rendered PNG is missing or outside its planned path"
                )
            reference = _absolute_path(
                capture["reference"]["path"], label=f"capture {capture_id}.reference"
            )
            comparison_spec = _absolute_path(
                capture["comparison_spec"]["path"],
                label=f"capture {capture_id}.comparison_spec",
            )
            comparison_dir = stage / capture_id
            try:
                comparison = compare(
                    reference_path=reference,
                    rendered_path=rendered,
                    spec_path=comparison_spec,
                    output_dir=comparison_dir,
                    observed_at=completed_at,
                )
                validation = validate_report(
                    comparison_dir / "report.json",
                    reference_path=reference,
                    rendered_path=rendered,
                    spec_path=comparison_spec,
                    strict=True,
                )
            except CompFidelityError as exc:
                raise SealedRenditionError(
                    f"capture {capture_id} comparison failed: {exc}"
                ) from exc
            rendered_snapshot = _snapshot_file(
                rendered, label=f"capture {capture_id} rendered PNG"
            )
            captures.append(
                {
                    "ordinal": capture["ordinal"],
                    "id": capture_id,
                    "kind": capture["kind"],
                    "rendered": _file_record(
                        rendered_snapshot,
                        path=rendered.relative_to(output_root).as_posix(),
                    ),
                }
            )
            report_record = _relative_file_record(
                comparison_dir / "report.json", stage
            )
            report_record["path"] = (
                PurePosixPath("comparisons") / report_record["path"]
            ).as_posix()
            comparisons.append(
                {
                    "id": capture_id,
                    "report": report_record,
                    "strict_validation": {
                        "schema": validation["schema"],
                        "ok": validation["ok"],
                        "artifact_count": validation["artifact_count"],
                        "strict": validation["strict"],
                    },
                    "overall_metrics": comparison["overall_metrics"],
                    "regions": [
                        {"id": region["id"], "metrics": region["metrics"]}
                        for region in comparison["regions"]
                    ],
                    "advisory": comparison["advisory"],
                    "verdict": "measurement_only",
                }
            )
        post_state = _snapshot_authority(spec["authority"], shadow_lab_verifier)
        if post_state.snapshot != state.snapshot:
            raise SealedRenditionError("authority changed during gate closeout")
        statuses = {
            "input_integrity": "pass",
            "capture_integrity": "pass",
            "comparison_integrity": "pass",
            "source_mutation_audit": "pass",
            "visual_decision": visual_review["decision"],
        }
        report = {
            "schema": REPORT_SCHEMA,
            "gate_id": plan["gate_id"],
            "verdict": visual_review["decision"],
            "completed_at": completed_at,
            "paths": {
                "output_root": str(output_root),
                "spec": _file_record(spec_snapshot),
                "capture_plan": _file_record(plan_snapshot),
            },
            "authority": {
                "preflight": plan["authority"],
                "postflight": post_state.snapshot,
            },
            "statuses": statuses,
            "capture_order": plan["capture_order"],
            "captures": captures,
            "comparisons": comparisons,
            "visual_review": visual_review,
            "decision_boundary": {
                "global_pixel_pass_threshold": None,
                "measurement_verdict": "measurement_only",
                "visual_acceptance_authority": "explicit_human_or_system_review",
            },
        }
        os.replace(stage, comparisons_root)
        try:
            _atomic_write_json(report_path, report)
        except Exception:
            shutil.rmtree(comparisons_root, ignore_errors=True)
            raise
        return report
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def _artifact_from_record(root: Path, record: Any, *, label: str) -> FileSnapshot:
    root = root.resolve(strict=True)
    value = _exact_fields(record, {"path", "bytes", "sha256"}, label=label)
    relative = _safe_relative(value["path"], label=f"{label}.path")
    path = _contained_file(root, relative, label=label)
    snapshot = _snapshot_file(path, label=label)
    expected = {
        "path": relative.as_posix(),
        "bytes": snapshot.size,
        "sha256": snapshot.sha256,
    }
    if value != expected:
        raise SealedRenditionError(f"{label} hash or size mismatch")
    return snapshot


def validate_gate_report(
    report_path: Path,
    *,
    strict: bool = False,
    shadow_lab_verifier: ShadowLabVerifier | None = None,
) -> dict[str, Any]:
    report_snapshot, report = _json_snapshot(report_path, label="gate report")
    _exact_fields(
        report,
        {
            "schema",
            "gate_id",
            "verdict",
            "completed_at",
            "paths",
            "authority",
            "statuses",
            "capture_order",
            "captures",
            "comparisons",
            "visual_review",
            "decision_boundary",
        },
        label="gate report",
    )
    if report["schema"] != REPORT_SCHEMA:
        raise SealedRenditionError(f"gate report.schema must be {REPORT_SCHEMA}")
    _slug(report["gate_id"], label="gate report.gate_id")
    _utc_timestamp(report["completed_at"], label="gate report.completed_at")
    paths = _exact_fields(
        report["paths"], {"output_root", "spec", "capture_plan"}, label="gate report.paths"
    )
    output_root = _absolute_path(paths["output_root"], label="gate report.paths.output_root")
    if report_snapshot.path.parent != output_root:
        raise SealedRenditionError("gate report path does not match its output root")
    plan_record = _exact_fields(
        paths["capture_plan"], {"path", "bytes", "sha256"}, label="gate report capture plan"
    )
    plan_path = _absolute_path(plan_record["path"], label="gate report capture plan path")
    plan_snapshot, plan, spec_snapshot, _spec, state = _validated_plan(
        plan_path, shadow_lab_verifier
    )
    _record_matches(plan_record, plan_snapshot, label="gate report capture plan")
    spec_record = _exact_fields(
        paths["spec"], {"path", "bytes", "sha256"}, label="gate report spec"
    )
    _record_matches(spec_record, spec_snapshot, label="gate report spec")
    if report["gate_id"] != plan["gate_id"]:
        raise SealedRenditionError("gate report id disagrees with its capture plan")
    authority = _exact_fields(
        report["authority"], {"preflight", "postflight"}, label="gate report.authority"
    )
    if authority["preflight"] != plan["authority"] or authority["postflight"] != state.snapshot:
        raise SealedRenditionError("gate report authority audit mismatch")
    visual_review = _exact_fields(
        report["visual_review"], {"decision", "reviewer", "note"}, label="gate report.visual_review"
    )
    expected_visual = _visual_review(
        visual_review["decision"], visual_review["reviewer"], visual_review["note"]
    )
    if visual_review != expected_visual or report["verdict"] != visual_review["decision"]:
        raise SealedRenditionError("gate report visual decision mismatch")
    expected_statuses = {
        "input_integrity": "pass",
        "capture_integrity": "pass",
        "comparison_integrity": "pass",
        "source_mutation_audit": "pass",
        "visual_decision": visual_review["decision"],
    }
    if report["statuses"] != expected_statuses:
        raise SealedRenditionError("gate report statuses are invalid")
    expected_boundary = {
        "global_pixel_pass_threshold": None,
        "measurement_verdict": "measurement_only",
        "visual_acceptance_authority": "explicit_human_or_system_review",
    }
    if report["decision_boundary"] != expected_boundary:
        raise SealedRenditionError("gate report decision boundary is invalid")
    if report["capture_order"] != plan["capture_order"]:
        raise SealedRenditionError("gate report capture order mismatch")
    captures = report["captures"]
    comparisons = report["comparisons"]
    if (
        not isinstance(captures, list)
        or not isinstance(comparisons, list)
        or len(captures) != len(plan["captures"])
        or len(comparisons) != len(plan["captures"])
    ):
        raise SealedRenditionError("gate report capture or comparison inventory mismatch")
    artifact_count = 0
    for planned, captured, comparison in zip(plan["captures"], captures, comparisons):
        _exact_fields(captured, {"ordinal", "id", "kind", "rendered"}, label="gate report capture")
        if (captured["ordinal"], captured["id"], captured["kind"]) != (
            planned["ordinal"],
            planned["id"],
            planned["kind"],
        ):
            raise SealedRenditionError("gate report capture identity mismatch")
        rendered_snapshot = _artifact_from_record(
            output_root, captured["rendered"], label=f"capture {captured['id']} rendered"
        )
        if rendered_snapshot.path.resolve(strict=True) != Path(
            planned["rendered_path"]
        ).resolve(strict=True):
            raise SealedRenditionError("gate report rendered path disagrees with capture plan")
        _exact_fields(
            comparison,
            {
                "id",
                "report",
                "strict_validation",
                "overall_metrics",
                "regions",
                "advisory",
                "verdict",
            },
            label="gate report comparison",
        )
        if comparison["id"] != planned["id"] or comparison["verdict"] != "measurement_only":
            raise SealedRenditionError("gate report comparison identity is invalid")
        comparison_snapshot = _artifact_from_record(
            output_root,
            comparison["report"],
            label=f"comparison {comparison['id']} report",
        )
        reference = Path(planned["reference"]["path"])
        rendered = Path(planned["rendered_path"])
        comparison_spec = Path(planned["comparison_spec"]["path"])
        try:
            validation = validate_report(
                comparison_snapshot.path,
                reference_path=reference if strict else None,
                rendered_path=rendered if strict else None,
                spec_path=comparison_spec if strict else None,
                strict=strict,
            )
        except CompFidelityError as exc:
            raise SealedRenditionError(
                f"comparison {comparison['id']} validation failed: {exc}"
            ) from exc
        _, comparison_payload = _json_snapshot(
            comparison_snapshot.path, label=f"comparison {comparison['id']} report"
        )
        expected_regions = [
            {"id": region["id"], "metrics": region["metrics"]}
            for region in comparison_payload["regions"]
        ]
        expected_strict_validation = {
            "schema": validation["schema"],
            "ok": validation["ok"],
            "artifact_count": validation["artifact_count"],
            "strict": True,
        }
        if (
            comparison["strict_validation"] != expected_strict_validation
            or comparison["overall_metrics"] != comparison_payload["overall_metrics"]
            or comparison["regions"] != expected_regions
            or comparison["advisory"] != comparison_payload["advisory"]
        ):
            raise SealedRenditionError("gate report comparison summary mismatch")
        artifact_count += int(validation["artifact_count"])
    return {
        "schema": VALIDATION_SCHEMA,
        "ok": True,
        "report": str(report_snapshot.path),
        "strict": strict,
        "capture_count": len(captures),
        "comparison_artifact_count": artifact_count,
        "visual_decision": visual_review["decision"],
        "global_pixel_pass_threshold": None,
    }
