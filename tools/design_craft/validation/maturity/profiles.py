from __future__ import annotations

from dataclasses import dataclass

from ...release.policy import load_policy


PROFILE_NAMES = ("development", "operational_95", "certified_100")
PHASES = ("candidate", "final")

CORE_GATES = (
    "contract_completeness",
    "release_metadata_candidate",
    "portable_runtime_payload",
    "portable_route_fallback",
    "detector_degraded_contract",
    "platform_fixtures",
    "upstream_lock_parity",
    "workflow_contract",
    "package_boundary",
    "active_scope",
    "route_pack",
    "cross_agent_contracts",
    "comparative_contracts",
    "installer_contract",
    "l4_evidence_contract",
)

RELEASE_GATES = (
    "performance_regression",
    "comparative_evaluation",
    "clean_worktree",
    "install_provenance",
    "upstream_remote_review",
)


@dataclass(frozen=True)
class MaturityProfile:
    name: str
    scope: str
    release_level_score: int | None
    required_gate_ids: tuple[str, ...]
    allowed_unverified: tuple[str, ...]


def load_profile(name: str, phase: str) -> MaturityProfile:
    if name not in PROFILE_NAMES:
        raise ValueError(f"unknown maturity profile: {name}")
    if phase not in PHASES:
        raise ValueError(f"unknown maturity phase: {phase}")
    if name == "development":
        return MaturityProfile(
            name=name,
            scope="development_baseline",
            release_level_score=None,
            required_gate_ids=CORE_GATES,
            allowed_unverified=(),
        )

    level = load_policy()[name]
    host_gates = tuple(f"host_{host}_current_source" for host in level.required_hosts)
    native_gates = tuple(
        f"native_{native}_current_source" for native in level.required_native
    )
    final_gates = (
        "release_metadata_final",
        "main_branch",
        "main_ruleset",
    ) if phase == "final" else ()
    return MaturityProfile(
        name=name,
        scope="release_candidate" if phase == "candidate" else "release_final",
        release_level_score=level.score,
        required_gate_ids=(
            *CORE_GATES,
            *RELEASE_GATES,
            *host_gates,
            *native_gates,
            *final_gates,
        ),
        allowed_unverified=level.allowed_unverified,
    )


def check_profile_invariants() -> list[str]:
    errors: list[str] = []
    operational = load_profile("operational_95", "candidate")
    certified = load_profile("certified_100", "candidate")
    required_operational = {
        "host_codex_current_source",
        "host_pi_current_source",
        "native_ios_simulator_current_source",
        "native_android_emulator_current_source",
        "performance_regression",
        "comparative_evaluation",
        "clean_worktree",
        "install_provenance",
        "upstream_remote_review",
    }
    missing = required_operational - set(operational.required_gate_ids)
    if missing:
        errors.append(f"operational_95 is missing required gates: {sorted(missing)}")
    if not set(operational.required_gate_ids) < set(certified.required_gate_ids):
        errors.append("certified_100 must strictly extend operational_95")
    for gate in (
        "host_cursor_current_source",
        "host_claude_current_source",
        "native_physical_device_current_source",
    ):
        if gate not in certified.required_gate_ids:
            errors.append(f"certified_100 is missing {gate}")
    if set(operational.allowed_unverified) != {"cursor", "claude", "physical_device"}:
        errors.append("operational_95 allowed_unverified contract is invalid")
    if certified.allowed_unverified:
        errors.append("certified_100 must not allow unverified targets")
    return errors
