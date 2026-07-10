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
    root = ROOT / directory
    required = [root / "codex-output.md", root / "pi-output.md", root / "score.codex.json", root / "score.pi.json"]
    passed = all(path.is_file() and path.stat().st_size > 20 for path in required)
    return make_gate(
        gate_id,
        passed,
        f"observed Codex and Pi artifacts exist in {directory}",
        f"missing observed Codex/Pi artifacts in {directory}",
    )


def l4_gate() -> Gate:
    cases = [
        ROOT / "evals/product-ui-taste/before-after/generic-review-workbench-local-l4",
        ROOT / "evals/product-ui-taste/before-after/ops-dashboard-decision-surface-l4",
    ]
    passed = all((case / "screenshots.json").is_file() and (case / "score.after.json").is_file() for case in cases)
    return make_gate(
        "l4_observed_evidence",
        passed,
        "project-neutral L4 before/after evidence cases exist",
        "project-neutral L4 observed evidence is incomplete",
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
        passed, detail = trees_equal(source, install_root / "design-craft")
        return make_gate(
            "install_parity",
            passed,
            "installed ~/.agents design-craft tree matches source",
            "source/install parity failed: " + detail,
        )

    installer = read(ROOT / "scripts/install_local.sh")
    passed = "cp -R" in installer and (source / "scripts/design_craft_route.sh").is_file()
    return make_gate(
        "install_parity",
        passed,
        "portable install image includes runtime scripts and installer copies the full skill tree",
        "portable install image or installer contract is incomplete",
    )


def route_pack_gate(profile: str) -> Gate:
    if profile == "local":
        result = run([sys.executable, "scripts/design_craft_codex_route_pack.py", "--strict", "--json"], timeout=90)
        try:
            payload = json.loads(result.stdout)
        except Exception:
            payload = {}
        passed = result.returncode == 0 and payload.get("schema") == "design-craft.codex-route-pack.v2"
    else:
        content = read(ROOT / "scripts/design_craft_codex_route_pack.py")
        passed = 'SCHEMA = "design-craft.codex-route-pack.v2"' in content
    return make_gate(
        "route_pack_v2",
        passed,
        "Codex route pack remains on the validated v2 ownership/delegation contract",
        "Codex route-pack v2 contract is missing or invalid",
        hard=False,
    )


def native_runtime_gate() -> Gate:
    ios = ROOT / "evals/native-runtime/ios-observed.json"
    android = ROOT / "evals/native-runtime/android-observed.json"
    passed = ios.is_file() and android.is_file()
    return make_gate(
        "native_runtime_observed",
        passed,
        "observed iOS and Android runtime evidence exists",
        "iOS Simulator and Android Emulator are unverified locally; maturity is capped at 95",
        hard=False,
    )


def build_gates(profile: str) -> list[Gate]:
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
            ["ubuntu-latest", "macos-latest", '"22"', '"24"', '"3.13"', "submodules: recursive", "--profile portable", "--min-score 95"],
            "portable CI covers Ubuntu/macOS, Node 22/24, Python 3.13, recursive submodules, and maturity 95",
            "portable CI matrix is incomplete",
        ),
        text_gate(
            "upstream_audit_ci",
            ".github/workflows/upstream-audit.yml",
            ["schedule:", "--remote", "--fail-on-unreviewed"],
            "scheduled upstream audit fails on unreviewed remote drift",
            "upstream audit workflow is incomplete",
        ),
        observed_eval_gate("observed_dashboard_eval", "evals/cross-agent/same-prompt-dashboard-review"),
        observed_eval_gate("observed_motion_eval", "evals/cross-agent/same-prompt-motion-review"),
        observed_eval_gate("observed_native_eval", "evals/cross-agent/same-prompt-native-adaptive-review"),
        l4_gate(),
        route_pack_gate(profile),
        text_gate(
            "release_metadata",
            "CHANGELOG.md",
            ["0.4.0", "web", "iOS", "Android", "adaptive", "95"],
            "0.4.0 release metadata names platform scope and maturity boundary",
            "0.4.0 release metadata is incomplete",
            hard=False,
        ),
        install_gate(profile),
        native_runtime_gate(),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["portable", "local"], default="portable")
    parser.add_argument("--min-score", type=int, default=0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    gates = build_gates(args.profile)
    raw_score = sum(gate.points for gate in gates)
    native_runtime_observed = next(gate.passed for gate in gates if gate.gate_id == "native_runtime_observed")
    maturity_cap = 100 if native_runtime_observed else 95
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
        "maturity_cap_reasons": [] if native_runtime_observed else [
            "iOS Simulator and Android Emulator are unverified locally; observed real-device evidence is also absent"
        ],
        "hard_failures": hard_failures,
        "ok": ok,
        "gates": [asdict(gate) for gate in gates],
        "native_runtime": {
            "ios_simulator": "observed" if native_runtime_observed else "unverified locally",
            "android_emulator": "observed" if native_runtime_observed else "unverified locally",
        },
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"design-craft operational maturity ({args.profile}): {score}/100")
        print(f"maturity cap: {maturity_cap}/100")
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
