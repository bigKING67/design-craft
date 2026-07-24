from __future__ import annotations

from pathlib import Path

from .assets import collect_native_evidence, load_release_evidence
from .github_runs import validate_workflow_binding
from .policy import ReleaseLevel


def validate_release_run_bindings(
    evidence_path: Path,
    *,
    level: ReleaseLevel,
    native_run: dict[str, object],
    physical_run: dict[str, object] | None = None,
    evidence_root: Path | None = None,
) -> dict[str, object]:
    evidence = load_release_evidence(evidence_path, level)
    bindings = collect_native_evidence(
        evidence,
        level,
        evidence_root=evidence_root,
    )
    errors: list[str] = []
    for native, binding in bindings.items():
        is_physical = native == "physical_device"
        run = physical_run if is_physical else native_run
        kind = "physical" if is_physical else "native"
        if run is None:
            errors.append("physical-device evidence requires a selected physical run")
            continue
        errors.extend(
            validate_workflow_binding(
                binding.get("workflow"),
                run,
                kind=kind,
                label=f"release evidence {native}",
            )
        )
    return {
        "schema": "design-craft.release-run-bindings.v1",
        "release_level": level.name,
        "evidence": str(evidence_path),
        "native_targets": sorted(bindings),
        "ok": not errors,
        "errors": errors,
    }


__all__ = ["validate_release_run_bindings"]
