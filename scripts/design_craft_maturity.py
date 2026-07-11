#!/usr/bin/env python3
"""Score design-craft operational maturity with explicit hard gates."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path


SCHEMA = "design-craft.maturity.v1"
ROOT = Path(__file__).resolve().parents[1]
REQUIRED_RUNTIME_SCRIPTS = {
    "design_craft_audit.sh",
    "design_craft_pass.sh",
    "design_craft_detect.sh",
    "design_craft_route.sh",
    "design_craft_seed_design.sh",
    "design_craft_taste_review.sh",
    "design_craft_browser_evidence.py",
    "design_craft_css_smell_scan.py",
    "design_craft_focus_audit.py",
    "design_craft_token_audit.py",
    "design_craft_static_review.py",
    "design_craft_l4_capture.py",
    "design_craft_l4_evidence_manifest.py",
    "design_craft_l4_eval_case.sh",
    "design_craft_l4_case_validate.py",
    "design_craft_platform_scan.py",
}
HARD_GATE_IDS = {
    "source_completeness",
    "portable_runtime_payload",
    "root_wrapper_contract",
    "portable_route_fallback",
    "detector_degraded_contract",
    "platform_fixtures",
    "upstream_review_metadata",
    "submodule_lock_parity",
    "portable_ci",
    "upstream_audit_ci",
    "observed_motion_eval",
    "observed_native_eval",
    "install_parity",
}


@dataclass(frozen=True)
class Gate:
    gate_id: str
    passed: bool
    points: int
    hard: bool
    evidence: str
    gap: str


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def run(command: list[str], *, env: dict[str, str] | None = None, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        check=False,
    )


def make_gate(gate_id: str, passed: bool, evidence: str, gap: str, *, hard: bool | None = None) -> Gate:
    return Gate(
        gate_id=gate_id,
        passed=passed,
        points=5 if passed else 0,
        hard=gate_id in HARD_GATE_IDS if hard is None else hard,
        evidence=evidence if passed else "",
        gap="" if passed else gap,
    )


def source_completeness_gate() -> Gate:
    result = run([sys.executable, "scripts/design_craft_score.py", "--self", "--no-smoke", "--json"])
    try:
        payload = json.loads(result.stdout)
        score = int(payload.get("score", 0))
        schema = payload.get("schema")
    except Exception:
        score = 0
        schema = "invalid"
    passed = result.returncode == 0 and score == 100 and schema == "design-craft.source-completeness.v1"
    return make_gate(
        "source_completeness",
        passed,
        "source completeness scorer reports 100/100",
        f"source completeness must be 100/100 (observed score={score}, schema={schema})",
    )


def runtime_payload_gate() -> Gate:
    runtime = ROOT / "skills/design-craft/scripts"
    missing = sorted(name for name in REQUIRED_RUNTIME_SCRIPTS if not (runtime / name).is_file())
    non_exec = sorted(name for name in REQUIRED_RUNTIME_SCRIPTS if (runtime / name).is_file() and not os.access(runtime / name, os.X_OK))
    passed = not missing and not non_exec
    detail = "portable runtime scripts are present and executable"
    gap = f"runtime payload missing={missing}, non_executable={non_exec}"
    return make_gate("portable_runtime_payload", passed, detail, gap)


def wrapper_gate() -> Gate:
    failures: list[str] = []
    for name in REQUIRED_RUNTIME_SCRIPTS:
        wrapper = ROOT / "scripts" / name
        if not wrapper.is_file():
            failures.append(f"missing:{name}")
            continue
        text = read(wrapper)
        if "skills/design-craft" not in text and '"skills" / "design-craft"' not in text:
            failures.append(f"not-delegating:{name}")
    return make_gate(
        "root_wrapper_contract",
        not failures,
        "repo-root runtime entries delegate to skills/design-craft/scripts",
        "root runtime wrapper failures: " + ", ".join(failures),
    )


def route_fallback_gate() -> Gate:
    with tempfile.TemporaryDirectory(prefix="design-craft-maturity-route-") as raw:
        target = Path(raw)
        (target / "DESIGN.md").write_text(
            "# Design\n\n## Typography System\nSystem type.\n\n## Color Palette\nSemantic roles.\n\n## Motion Language\nReduced motion.\n\n## Component Grammar\nNative states.\n",
            encoding="utf-8",
        )
        (target / "PRODUCT.md").write_text("# Product\n\n## Platform\nadaptive\n", encoding="utf-8")
        env = dict(os.environ)
        env["DESIGN_CRAFT_ROUTE_PLAN"] = str(target / "missing-route-plan.sh")
        result = run(
            [
                "bash",
                "skills/design-craft/scripts/design_craft_route.sh",
                "--target",
                str(target),
                "--surface",
                "mobile",
                "--intent",
                "visual-refine",
                "--scope",
                "component",
                "--json-only",
            ],
            env=env,
        )
    try:
        payload = json.loads(result.stdout)
    except Exception:
        payload = {}
    passed = (
        result.returncode == 0
        and payload.get("route_source") == "portable_fallback"
        and payload.get("degraded") is True
        and payload.get("platform") == "adaptive"
        and payload.get("design_tier") == payload.get("frontend_tier")
        and payload.get("native_validation_required") is True
    )
    return make_gate(
        "portable_route_fallback",
        passed,
        "portable fallback emits degraded route and adaptive runtime contract",
        "portable route fallback contract failed",
    )


def detector_degraded_gate() -> Gate:
    with tempfile.TemporaryDirectory(prefix="design-craft-maturity-detector-") as raw:
        env = dict(os.environ)
        env["HOME"] = raw
        env["DESIGN_CRAFT_SOURCE_ROOT"] = str(Path(raw) / "missing-source")
        env["DESIGN_CRAFT_IMPECCABLE_DETECTOR"] = str(Path(raw) / "missing-detect.mjs")
        result = run(
            [
                "bash",
                "skills/design-craft/scripts/design_craft_detect.sh",
                "--target",
                "evals/fixtures/css-smells",
                "--full-json",
            ],
            env=env,
        )
    try:
        payload = json.loads(result.stdout)
    except Exception:
        payload = {}
    detector = payload.get("upstream_detector") if isinstance(payload.get("upstream_detector"), dict) else {}
    passed = result.returncode == 0 and payload.get("degraded") is True and detector.get("status") == "unavailable"
    return make_gate(
        "detector_degraded_contract",
        passed,
        "missing Impeccable detector is explicit and degraded rather than silently successful",
        "detector unavailable path did not emit degraded=true/status=unavailable",
    )


def platform_fixtures_gate() -> Gate:
    failures: list[str] = []
    scanner = "skills/design-craft/scripts/design_craft_platform_scan.py"
    for platform in ("ios", "android", "adaptive"):
        valid = run([sys.executable, scanner, "--target", f"evals/fixtures/platforms/{platform}/valid", "--json", "--strict"])
        invalid = run([sys.executable, scanner, "--target", f"evals/fixtures/platforms/{platform}/invalid", "--json", "--strict"])
        if valid.returncode != 0:
            failures.append(f"{platform}:valid")
        if invalid.returncode == 0:
            failures.append(f"{platform}:invalid")
    return make_gate(
        "platform_fixtures",
        not failures,
        "iOS, Android, and adaptive valid/invalid fixtures separate cleanly",
        "platform fixture failures: " + ", ".join(failures),
    )


def upstream_metadata_gate() -> Gate:
    try:
        payload = json.loads(read(ROOT / "upstreams.lock.json"))
    except Exception:
        payload = {}
    failures: list[str] = []
    for name, meta in payload.get("upstreams", {}).items():
        if meta.get("reviewed_commit") != meta.get("commit"):
            failures.append(f"{name}:reviewed")
        if meta.get("decision") not in {"absorbed", "partial", "provenance_only", "deferred"}:
            failures.append(f"{name}:decision")
        if not meta.get("reviewed_at") or not meta.get("notes"):
            failures.append(f"{name}:metadata")
        if meta.get("decision") != "deferred" and not meta.get("absorbed_commit"):
            failures.append(f"{name}:absorbed")
    if set(payload.get("upstreams", {})) != {"taste-skill", "impeccable", "emilkowalski-skills"}:
        failures.append("upstream-set")
    return make_gate(
        "upstream_review_metadata",
        not failures,
        "all pinned upstreams have reviewed/absorbed decisions",
        "upstream review metadata failures: " + ", ".join(failures),
    )


def submodule_parity_gate() -> Gate:
    try:
        payload = json.loads(read(ROOT / "upstreams.lock.json"))
    except Exception:
        payload = {}
    failures: list[str] = []
    for name, meta in payload.get("upstreams", {}).items():
        result = run(["git", "-C", str(meta.get("path", "")), "rev-parse", "HEAD"])
        current = result.stdout.strip() if result.returncode == 0 else ""
        if current != meta.get("commit"):
            failures.append(f"{name}:{current or 'unavailable'}")
    return make_gate(
        "submodule_lock_parity",
        not failures,
        "submodule HEAD values match compatibility lock commits",
        "submodule/lock mismatch: " + ", ".join(failures),
    )


def text_gate(gate_id: str, path: str, needles: list[str], evidence: str, gap: str, *, hard: bool | None = None) -> Gate:
    content = read(ROOT / path)
    passed = bool(content) and all(needle in content for needle in needles)
    return make_gate(gate_id, passed, evidence, gap, hard=hard)


def observed_eval_gate(gate_id: str, directory: str) -> Gate:
    result = run(
        [
            sys.executable,
            "scripts/design_craft_cross_agent_validate.py",
            "--observed-task",
            directory,
            "--require-host",
            "codex",
            "--require-host",
            "pi",
        ]
    )
    passed = result.returncode == 0
    return make_gate(
        gate_id,
        passed,
        f"schema-valid Codex/Pi artifacts and explicit remaining-host boundaries exist in {directory}",
        result.stderr.strip() or f"observed cross-agent evidence is invalid in {directory}",
    )


def certified_four_host_status() -> tuple[bool, list[str]]:
    errors: list[str] = []
    for task in (
        "same-prompt-dashboard-review",
        "same-prompt-motion-review",
        "same-prompt-native-adaptive-review",
    ):
        result = run(
            [
                sys.executable,
                "scripts/design_craft_cross_agent_validate.py",
                "--observed-task",
                f"evals/cross-agent/{task}",
                "--require-host",
                "codex",
                "--require-host",
                "pi",
                "--require-host",
                "cursor",
                "--require-host",
                "claude",
                "--require-schema-v2",
                "--require-current-source",
            ],
            timeout=90,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or "validation failed"
            errors.append(f"{task}: {detail}")
    return not errors, errors


def l4_gate(profile: str) -> Gate:
    cases = [
        ROOT / "evals/product-ui-taste/before-after/generic-review-workbench-local-l4",
        ROOT / "evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4",
    ]
    failures: list[str] = []
    for case in cases:
        command = [
            sys.executable,
            "scripts/design_craft_l4_case_validate.py",
            "--case-dir",
            str(case.relative_to(ROOT)),
            "--strict",
        ]
        if profile == "local":
            command.append("--require-existing-files")
        result = run(command)
        if result.returncode != 0:
            failures.append(result.stderr.strip() or result.stdout.strip() or case.name)
    passed = not failures
    evidence = (
        "project-neutral L4 before/after artifacts exist and match their manifests"
        if profile == "local"
        else "project-neutral L4 before/after manifests validate without claiming local artifact availability"
    )
    return make_gate(
        "l4_observed_evidence",
        passed,
        evidence,
        "project-neutral L4 evidence is incomplete: " + "; ".join(failures),
        hard=False,
    )


def trees_equal(source: Path, installed: Path) -> tuple[bool, str]:
    if not installed.is_dir():
        return False, f"installed skill missing: {installed}"

    def snapshot(root: Path) -> dict[str, bytes]:
        values: dict[str, bytes] = {}
        for path in root.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or path.name == ".DS_Store":
                continue
            values[str(path.relative_to(root))] = path.read_bytes()
        return values

    left = snapshot(source)
    right = snapshot(installed)
    if left == right:
        return True, ""
    missing = sorted(set(left) - set(right))
    extra = sorted(set(right) - set(left))
    changed = sorted(key for key in set(left) & set(right) if left[key] != right[key])
    return False, f"missing={missing[:5]} extra={extra[:5]} changed={changed[:5]}"


def install_gate(profile: str) -> Gate:
    source = ROOT / "skills/design-craft"
    if profile == "local":
        install_root = Path(os.environ.get("DESIGN_CRAFT_SKILL_ROOT", Path.home() / ".agents/skills")).expanduser()
        version = read(ROOT / "VERSION").strip()
        result = run(
            [
                sys.executable,
                "scripts/design_craft_install_verify.py",
                "--source",
                str(source),
                "--installed",
                str(install_root / "design-craft"),
                "--expected-name",
                "design-craft",
                "--expected-version",
                version,
                "--require-metadata",
                "--json",
            ]
        )
        try:
            payload = json.loads(result.stdout)
        except Exception:
            payload = {}
        passed = result.returncode == 0 and payload.get("ok") is True
        detail = "; ".join(payload.get("errors", [])) or result.stderr.strip()
        return make_gate(
            "install_parity",
            passed,
            "installed ~/.agents design-craft tree and provenance metadata match source",
            "source/install parity failed: " + detail,
        )

    installer = read(ROOT / "scripts/install_local.sh")
    passed = all(
        needle in installer
        for needle in (
            "mktemp -d",
            ".design-craft-install.lock",
            "Atomic install failed",
            "Post-install verification failed",
            "DESIGN_CRAFT_BACKUP_KEEP",
            ".design-craft-install.json",
        )
    ) and (ROOT / "scripts/design_craft_install_verify.py").is_file()
    return make_gate(
        "install_parity",
        passed,
        "portable installer stages, locks, atomically switches, rolls back, retains backups, and records provenance",
        "atomic portable installer or provenance verifier contract is incomplete",
    )


def route_pack_gate(profile: str) -> Gate:
    try:
        compatibility = json.loads(read(ROOT / "skills/design-craft/COMPATIBILITY.json"))
    except Exception:
        compatibility = {}
    expected_schema = compatibility.get("codex_route_pack", {}).get("schema")
    expected_manifest_schema = compatibility.get("codex_route_pack", {}).get("manifest_schema")
    if profile == "local":
        result = run([sys.executable, "scripts/design_craft_codex_route_pack.py", "--strict", "--json"], timeout=90)
        try:
            payload = json.loads(result.stdout)
        except Exception:
            payload = {}
        passed = (
            result.returncode == 0
            and expected_schema == "design-craft.codex-route-pack.v2"
            and expected_manifest_schema == "codex.frontend-route-pack.manifest.v1"
            and payload.get("schema") == expected_schema
            and payload.get("route_pack_manifest", {}).get("schema")
            == expected_manifest_schema
        )
    else:
        content = read(ROOT / "scripts/design_craft_codex_route_pack.py")
        passed = (
            expected_schema == "design-craft.codex-route-pack.v2"
            and expected_manifest_schema == "codex.frontend-route-pack.manifest.v1"
            and f'SCHEMA = "{expected_schema}"' in content
            and f'ROUTE_PACK_MANIFEST_SCHEMA = "{expected_manifest_schema}"' in content
        )
    return make_gate(
        "route_pack_v2",
        passed,
        "installed compatibility contract matches the route-pack v2 and single-manifest schemas",
        "Codex route-pack compatibility contract is missing, invalid, or mismatched",
        hard=False,
    )


def native_runtime_status(payload: dict) -> dict[str, str]:
    evidence = payload.get("evidence", {}) if isinstance(payload, dict) else {}
    errors = payload.get("errors", []) if isinstance(payload, dict) else []
    if not isinstance(evidence, dict):
        evidence = {}
    if not isinstance(errors, list):
        errors = []

    def status(key: str, filename: str) -> str:
        item = evidence.get(key)
        related_errors = [error for error in errors if isinstance(error, str) and filename in error]
        if isinstance(item, dict) and item.get("verified") is True and not related_errors:
            return "observed_current_source"
        if isinstance(item, dict):
            return "invalid_current_source"
        return "missing"

    return {
        "ios_simulator": status("ios", "ios-observed.json"),
        "android_emulator": status("android", "android-observed.json"),
        "real_device": status("real_device", "real-device-observed.json"),
    }


def native_runtime_gate() -> tuple[Gate, dict[str, str]]:
    result = run(
        [
            sys.executable,
            "scripts/design_craft_native_runtime_validate.py",
            "--validate",
            "--require",
            "ios",
            "--require",
            "android",
            "--require-real-device",
            "--require-current-source",
            "--json",
        ]
    )
    try:
        payload = json.loads(result.stdout)
    except Exception:
        payload = {}
    passed = result.returncode == 0 and payload.get("ok") is True
    detail = "; ".join(payload.get("errors", []))
    return (
        make_gate(
            "native_runtime_observed",
            passed,
            "schema-validated observed iOS, Android, and real-device runtime evidence exists",
            detail
            or "current-source iOS Simulator, Android Emulator, or real-device evidence is incomplete; maturity is capped at 95",
            hard=False,
        ),
        native_runtime_status(payload),
    )


def release_metadata_gate() -> Gate:
    version = read(ROOT / "VERSION").strip()
    content = read(ROOT / "CHANGELOG.md")
    marker = f"## {version} - "
    start = content.find(marker)
    if start < 0:
        section = ""
    else:
        next_header = content.find("\n## ", start + len(marker))
        section = content[start:] if next_header < 0 else content[start:next_header]
    required = ("web", "iOS", "Android", "adaptive", "95", "100")
    passed = bool(version) and bool(section) and all(needle in section for needle in required)
    return make_gate(
        "release_metadata",
        passed,
        f"{version} release metadata names platform scope and 95/100 certification boundaries",
        f"{version} release metadata must name web/iOS/Android/adaptive and both 95/100 boundaries",
        hard=False,
    )


def build_gates(profile: str, native_gate: Gate) -> list[Gate]:
    return [
        source_completeness_gate(),
        runtime_payload_gate(),
        wrapper_gate(),
        route_fallback_gate(),
        detector_degraded_gate(),
        platform_fixtures_gate(),
        text_gate(
            "product_context_contract",
            "skills/design-craft/references/product-context.md",
            ["PRODUCT.md", "DESIGN.md", "Explicit route", "Default `web`"],
            "PRODUCT.md separation and platform precedence are documented",
            "product context contract is incomplete",
            hard=False,
        ),
        text_gate(
            "native_quality_references",
            "skills/design-craft/SKILL.md",
            ["ios-quality.md", "android-quality.md", "adaptive-quality.md", "interaction-physics.md"],
            "SKILL.md routes all native/adaptive quality references",
            "native/adaptive references are not fully routed",
            hard=False,
        ),
        upstream_metadata_gate(),
        submodule_parity_gate(),
        text_gate(
            "portable_ci",
            ".github/workflows/validate.yml",
            ["ubuntu-latest", "macos-latest", '"22"', '"24"', '"3.11"', '"3.12"', '"3.13"', "submodules: recursive", "--profile portable", "--min-score 95"],
            "portable CI covers Ubuntu/macOS, Node 22/24, Python 3.11/3.12/3.13, recursive submodules, and maturity 95",
            "portable CI matrix is incomplete",
        ),
        text_gate(
            "upstream_audit_ci",
            ".github/workflows/upstream-audit.yml",
            ["17 3 * * *", "--remote-details", "--fail-on-unreviewed", "issues: write", "Open or update review issue"],
            "daily actionable upstream audit reports changed paths and opens a review issue",
            "upstream audit workflow is incomplete",
        ),
        observed_eval_gate("observed_dashboard_eval", "evals/cross-agent/same-prompt-dashboard-review"),
        observed_eval_gate("observed_motion_eval", "evals/cross-agent/same-prompt-motion-review"),
        observed_eval_gate("observed_native_eval", "evals/cross-agent/same-prompt-native-adaptive-review"),
        l4_gate(profile),
        route_pack_gate(profile),
        release_metadata_gate(),
        install_gate(profile),
        native_gate,
    ]


def certification_cap(
    native_runtime_observed: bool,
    four_host_certified: bool,
    native_status: dict[str, str] | None = None,
) -> tuple[int, list[str]]:
    reasons: list[str] = []
    if not native_runtime_observed:
        labels = {
            "ios_simulator": "iOS Simulator",
            "android_emulator": "Android Emulator",
            "real_device": "real device",
        }
        incomplete = [
            label
            for key, label in labels.items()
            if not native_status or native_status.get(key) != "observed_current_source"
        ]
        reasons.append(
            "current-source native runtime evidence is incomplete: " + ", ".join(incomplete)
        )
    if not four_host_certified:
        reasons.append(
            "current-source v2 Codex/Pi/Cursor/Claude evidence is incomplete"
        )
    return (100 if not reasons else 95), reasons


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["portable", "local"], default="portable")
    parser.add_argument("--min-score", type=int, default=0)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check", action="store_true", help="Run offline maturity-cap invariants.")
    args = parser.parse_args()

    if args.check:
        expected = {
            (False, False): 95,
            (False, True): 95,
            (True, False): 95,
            (True, True): 100,
        }
        for inputs, cap in expected.items():
            observed, _ = certification_cap(*inputs)
            if observed != cap:
                print(f"certification cap invariant failed for {inputs}: {observed}", file=sys.stderr)
                return 1
        partial_status = native_runtime_status(
            {
                "evidence": {
                    "ios": {"verified": True},
                    "android": {"verified": True},
                },
                "errors": ["missing real-device-observed.json"],
            }
        )
        if partial_status != {
            "ios_simulator": "observed_current_source",
            "android_emulator": "observed_current_source",
            "real_device": "missing",
        }:
            print(f"native runtime status invariant failed: {partial_status}", file=sys.stderr)
            return 1
        return 0

    native_gate, native_status = native_runtime_gate()
    gates = build_gates(args.profile, native_gate)
    raw_score = sum(gate.points for gate in gates)
    native_runtime_observed = next(gate.passed for gate in gates if gate.gate_id == "native_runtime_observed")
    four_host_certified, four_host_errors = certified_four_host_status()
    maturity_cap, maturity_cap_reasons = certification_cap(
        native_runtime_observed,
        four_host_certified,
        native_status,
    )
    score = min(raw_score, maturity_cap)
    hard_failures = [gate.gate_id for gate in gates if gate.hard and not gate.passed]
    ok = score >= args.min_score and not hard_failures
    payload = {
        "schema": SCHEMA,
        "profile": args.profile,
        "root": str(ROOT),
        "score": score,
        "raw_score": raw_score,
        "max_score": 100,
        "maturity_cap": maturity_cap,
        "maturity_cap_reasons": maturity_cap_reasons,
        "hard_failures": hard_failures,
        "ok": ok,
        "gates": [asdict(gate) for gate in gates],
        "native_runtime": native_status,
        "cross_agent_certification": {
            "four_host_current_source": four_host_certified,
            "errors": four_host_errors,
        },
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"design-craft operational maturity ({args.profile}): {score}/100")
        print(f"maturity cap: {maturity_cap}/100")
        for reason in maturity_cap_reasons:
            print(f"cap reason: {reason}")
        for gate in gates:
            marker = "+" if gate.passed else "-"
            detail = gate.evidence if gate.passed else gate.gap
            hard = " [hard]" if gate.hard else ""
            print(f"{marker} {gate.gate_id}{hard}: {detail}")
        if hard_failures:
            print("hard failures: " + ", ".join(hard_failures))

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
