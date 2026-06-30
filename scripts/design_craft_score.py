#!/usr/bin/env python3
"""Deterministic design-craft quality scorer."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


WEIGHTS = {
    "Visual Judgment": 20,
    "Product Fit": 15,
    "Engineering Quality": 15,
    "Performance": 15,
    "Architecture": 15,
    "Project Structure": 10,
    "Validation Evidence": 10,
}


@dataclass
class Dimension:
    name: str
    score: int
    weight: int
    evidence: list[str]
    gaps: list[str]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def has(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def iter_product_ui_score_entries(root: Path):
    score_paths = [
        *sorted((root / "evals/product-ui-taste").glob("*/score.json")),
        *sorted((root / "evals/product-ui-taste/before-after").glob("*/score.before.json")),
        *sorted((root / "evals/product-ui-taste/before-after").glob("*/score.after.json")),
    ]
    for score_path in score_paths:
        try:
            payload = json.loads(score_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        entries = payload.get("cases")
        if entries is None:
            entries = [payload]
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            yield score_path, payload, entry


def has_product_ui_l2_case(root: Path) -> bool:
    for _score_path, payload, entry in iter_product_ui_score_entries(root):
        level = entry.get("evidence_level") or payload.get("evidence_level")
        if level in {"L2", "L3", "L4"} and entry.get("screenshot_sha256"):
            return True
    return False


def has_product_ui_l3_case(root: Path) -> bool:
    for _score_path, payload, entry in iter_product_ui_score_entries(root):
        level = entry.get("evidence_level") or payload.get("evidence_level")
        if level in {"L3", "L4"} and entry.get("responsive_viewports") and entry.get("state_checks"):
            return True
    return False


def has_product_ui_l4_before_after_case(root: Path) -> bool:
    case_root = root / "evals/product-ui-taste/before-after"
    for screenshots_path in sorted(case_root.glob("*/screenshots.json")):
        case_dir = screenshots_path.parent
        if (case_dir / "score.before.json").is_file() and (case_dir / "score.after.json").is_file():
            return True
    return False


def infer_root(target: Path) -> Path:
    target = target.expanduser().resolve()
    if target.is_file():
        target = target.parent
    if (target / "skills/design-craft/SKILL.md").is_file():
        return target
    if target.name == "design-craft" and (target / "SKILL.md").is_file():
        return target.parents[1]
    for parent in [target, *target.parents]:
        if (parent / "skills/design-craft/SKILL.md").is_file():
            return parent
    return target


def check_command(command: list[str], cwd: Path) -> bool:
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=30,
            check=False,
        )
    except Exception:
        return False
    return result.returncode == 0


def score_dimension(name: str, weight: int, checks: list[tuple[bool, str, str]]) -> Dimension:
    passed = [label for ok, label, _gap in checks if ok]
    gaps = [gap for ok, _label, gap in checks if not ok]
    score = round(weight * len(passed) / len(checks)) if checks else 0
    return Dimension(name=name, score=score, weight=weight, evidence=passed, gaps=gaps)


def build_score(root: Path, run_smoke: bool) -> list[Dimension]:
    skill = read_text(root / "skills/design-craft/SKILL.md")
    validation = read_text(root / "skills/design-craft/references/validation-contract.md")
    design_system = read_text(root / "skills/design-craft/references/design-system-contract.md")
    product_review = read_text(root / "skills/design-craft/references/product-ui-taste-review.md")
    taste_calibration = read_text(root / "skills/design-craft/references/taste-score-calibration.md")
    foundational_principles = read_text(root / "skills/design-craft/references/foundational-visual-principles.md")
    design_moves = read_text(root / "skills/design-craft/references/design-move-library.md")
    motion_quality = read_text(root / "skills/design-craft/references/motion-quality.md")
    motion_vocabulary = read_text(root / "skills/design-craft/references/motion-vocabulary.md")
    browser_evidence_helper = read_text(root / "scripts/design_craft_browser_evidence.py")
    report = read_text(root / "skills/design-craft/references/report-quality.md")
    surface = read_text(root / "skills/design-craft/references/surface-playbooks.md")
    source_map = read_text(root / "skills/design-craft/references/source-map.md")

    detector_smoke = False
    score_smoke = False
    pass_smoke = False
    critique_smoke = False
    motion_smoke = False
    seed_smoke = False
    taste_review_smoke = False
    if run_smoke:
        detector_smoke = check_command(
            ["bash", "scripts/design_craft_detect.sh", "--target", "skills/design-craft", "--json-only"],
            root,
        )
        score_smoke = check_command(
            [sys.executable, "scripts/design_craft_score.py", "--target", str(root), "--no-smoke", "--json"],
            root,
        )
        pass_smoke = check_command(
            ["bash", "scripts/design_craft_pass.sh", "--target", "skills/design-craft", "--mode", "audit", "--skip-route", "--skip-score"],
            root,
        )
        critique_smoke = check_command(
            ["bash", "scripts/design_craft_audit.sh", "--target", "skills/design-craft", "--mode", "critique", "--skip-route", "--skip-score"],
            root,
        )
        motion_smoke = check_command(
            ["bash", "scripts/design_craft_pass.sh", "--target", "skills/design-craft", "--mode", "motion", "--skip-route", "--skip-score"],
            root,
        )
        seed_smoke = check_command(
            ["bash", "scripts/design_craft_seed_design.sh", "--target", "skills/design-craft", "--dry-run"],
            root,
        )
        taste_review_smoke = check_command(
            ["bash", "scripts/design_craft_taste_review.sh", "--target", "skills/design-craft", "--context", "score smoke", "--evidence-level", "L0"],
            root,
        )

    return [
        score_dimension(
            "Visual Judgment",
            WEIGHTS["Visual Judgment"],
            [
                (has(root, "skills/design-craft/references/visual-judgment.md"), "visual-judgment reference exists", "Add visual-judgment reference."),
                ("anti-slop" in skill.lower() or "anti-slop" in read_text(root / "skills/design-craft/references/visual-judgment.md").lower(), "anti-slop encoded", "Encode anti-slop visual judgment."),
                ("design read" in skill.lower(), "design read required", "Require a concise design read for major visual work."),
                ("generic AI tells" in skill or "generic" in read_text(root / "skills/design-craft/references/visual-judgment.md").lower(), "generic-output guard present", "Add generic-output failure modes."),
                (has(root, "skills/design-craft/references/product-ui-taste-review.md"), "product UI taste review reference exists", "Add product UI taste review reference."),
                (has(root, "skills/design-craft/references/foundational-visual-principles.md"), "foundational visual principles reference exists", "Add compact CRAP/Gestalt visual principles."),
                ("Proximity" in foundational_principles and "Contrast" in foundational_principles, "foundational principles cover CRAP anchors", "Cover proximity, alignment, repetition, and contrast."),
                (has(root, "skills/design-craft/references/design-move-library.md"), "design move library exists", "Add a design move library for actionable redesign guidance."),
                ("Dashboard card soup" in design_moves and "Generic AI landing page" in design_moves, "design moves cover dashboard and landing repairs", "Cover concrete dashboard and landing design moves."),
                ("100-point score" in product_review, "100-point UI taste score present", "Add a concrete product UI scoring rubric."),
                ("Output contract" in product_review, "product UI review output contract present", "Add a structured product UI review output contract."),
                (has(root, "skills/design-craft/references/taste-score-calibration.md"), "taste score calibration reference exists", "Add taste score calibration examples."),
                ("Evidence levels" in taste_calibration, "taste evidence levels calibrated", "Define evidence levels for screenshot/browser taste scores."),
                (has(root, "skills/design-craft/references/intent-map.md"), "intent map reference exists", "Add an intent map for subjective frontend requests."),
                (has(root, "skills/design-craft/references/motion-quality.md"), "motion quality reference exists", "Add a motion-quality reference."),
                (has(root, "skills/design-craft/references/motion-vocabulary.md"), "motion vocabulary reference exists", "Add a motion-vocabulary reference."),
                ("scale(0)" in motion_quality and "transition-all" in motion_quality, "motion anti-patterns encoded", "Encode motion anti-patterns such as scale(0) and transition-all."),
                ("Origin-aware animation" in motion_vocabulary, "origin-aware motion vocabulary present", "Add origin-aware animation vocabulary."),
            ],
        ),
        score_dimension(
            "Product Fit",
            WEIGHTS["Product Fit"],
            [
                ("authority order" in skill.lower(), "authority order documented", "Document authority order."),
                ("DESIGN.md" in skill, "DESIGN.md precedence present", "Make DESIGN.md/style authority explicit."),
                ("DataHub" in report or "report" in report.lower(), "report/data surface covered", "Add report/DataHub-specific grammar."),
                ("surface-specific" in surface.lower() or "surface playbooks" in surface.lower(), "surface playbooks present", "Cover surface-specific product jobs."),
                ("candidate_skills" in skill, "route candidate semantics present", "Separate route candidates from selected skills."),
                (has(root, "skills/design-craft/references/design-system-contract.md"), "design-system contract exists", "Add design-system contract reference."),
                (
                    has(root, "skills/design-craft/templates/vercel-geist/design.md")
                    and has(root, "skills/design-craft/templates/vercel-geist/design.dark.md"),
                    "Vercel Geist seed templates vendored",
                    "Vendor the default Vercel Geist seed templates.",
                ),
                (
                    "templates/vercel-geist/design.md" in skill
                    and "templates/vercel-geist/design.dark.md" in skill,
                    "Vercel Geist seed routed from SKILL.md",
                    "Route the Vercel Geist seed templates from SKILL.md.",
                ),
                (
                    "default seed" in design_system.lower() and "Vercel Geist" in design_system,
                    "default seed policy documented",
                    "Document when to use the bundled Vercel Geist seed.",
                ),
                (
                    has(root, "scripts/design_craft_seed_design.sh"),
                    "Vercel Geist seed helper exists",
                    "Add a helper for seeding DESIGN.md from the bundled Geist templates.",
                ),
                (
                    "vercel_geist_seed_applicable" in read_text(root / "scripts/design_craft_route.sh"),
                    "route summary reports Vercel seed applicability",
                    "Make route summaries say when the Geist seed is applicable.",
                ),
                ("theme parity" in design_system.lower(), "theme parity guidance present", "Cover light/dark token parity."),
                ("token layers" in design_system.lower(), "token layer guidance present", "Cover token role separation."),
                ("Page-type checks" in product_review, "page-type taste checks present", "Cover forms, tables, dashboards, modals, navigation, landing, and settings review."),
                ("emilkowalski-skills" in source_map, "Emil Kowalski upstream source mapped", "Map the emilkowalski/skills upstream in source-map."),
            ],
        ),
        score_dimension(
            "Engineering Quality",
            WEIGHTS["Engineering Quality"],
            [
                (has(root, "skills/design-craft/references/engineering-quality.md"), "engineering reference exists", "Add engineering-quality reference."),
                ("component" in read_text(root / "skills/design-craft/references/engineering-quality.md").lower(), "component boundary guidance present", "Add component boundary guidance."),
                ("observable" in skill.lower() or "errors" in read_text(root / "skills/design-craft/references/engineering-quality.md").lower(), "error observability covered", "Cover observable errors."),
                (has(root, "scripts/design_craft_route.sh"), "route wrapper exists", "Add route wrapper script."),
                (has(root, "scripts/design_craft_pass.sh"), "pass wrapper exists", "Add a neutral pass wrapper script."),
                (has(root, "scripts/design_craft_detect.sh"), "detector wrapper exists", "Add detector wrapper script."),
                (has(root, "scripts/design_craft_css_smell_scan.py"), "CSS smell scanner exists", "Add static CSS smell scanner."),
                (has(root, "scripts/design_craft_focus_audit.py"), "focus audit scanner exists", "Add static focus audit scanner."),
                (has(root, "scripts/design_craft_token_audit.py"), "token audit scanner exists", "Add token bypass scanner."),
            ],
        ),
        score_dimension(
            "Performance",
            WEIGHTS["Performance"],
            [
                (has(root, "skills/design-craft/references/performance-quality.md"), "performance reference exists", "Add performance-quality reference."),
                ("Web Vitals" in read_text(root / "skills/design-craft/references/performance-quality.md"), "Web Vitals covered", "Cover Web Vitals."),
                ("charts" in read_text(root / "skills/design-craft/references/performance-quality.md").lower(), "chart/table performance covered", "Cover chart/table performance."),
                ("measure" in skill.lower() or "baseline" in read_text(root / "skills/design-craft/references/impeccable-workflow.md").lower(), "measurement-first rule present", "Require measurement before optimization."),
                ("transform" in motion_quality and "opacity" in motion_quality, "motion performance properties covered", "Cover transform/opacity animation performance guidance."),
                ("prefers-reduced-motion" in motion_quality, "reduced-motion policy covered", "Cover reduced-motion handling for UI motion."),
            ],
        ),
        score_dimension(
            "Architecture",
            WEIGHTS["Architecture"],
            [
                (has(root, "skills/design-craft/references/architecture-quality.md"), "architecture reference exists", "Add architecture-quality reference."),
                (has(root, "upstreams.lock.json"), "upstream lock exists", "Add upstream lock file."),
                (has(root, "skills/design-craft/references/source-map.md"), "source map exists", "Add source-map reference."),
                (has(root, "scripts/upstream_absorption_report.py"), "upstream absorption report exists", "Add upstream absorption report script."),
                ("--remote" in read_text(root / "scripts/upstream_absorption_report.py"), "remote upstream drift check exists", "Add remote upstream drift reporting."),
                (has(root, "adapters/codex/README.md"), "Codex adapter docs exist", "Add Codex adapter docs."),
                (has(root, "adapters/cursor/README.md"), "Cursor adapter docs exist", "Add Cursor adapter docs."),
                (has(root, "adapters/claude/README.md"), "Claude adapter docs exist", "Add Claude adapter docs."),
                (has(root, "adapters/pi/README.md"), "Pi adapter docs exist", "Add Pi adapter docs."),
                (has(root, "scripts/design_craft_init_agent.sh"), "cross-agent init helper exists", "Add init helper for host-specific installs."),
                (has(root, "scripts/design_craft_doctor.sh"), "doctor helper exists", "Add doctor helper for portability checks."),
                ("templates/vercel-geist/design.md" in source_map, "Vercel Geist source map present", "Map vendored Vercel templates in source-map."),
                (("data flow" in read_text(root / "skills/design-craft/references/architecture-quality.md").lower()) or ("data-flow" in read_text(root / "skills/design-craft/references/architecture-quality.md").lower()), "data-flow guidance present", "Add data-flow guidance."),
                ("migration" in read_text(root / "skills/design-craft/references/architecture-quality.md").lower(), "migration risk covered", "Add migration/compatibility guidance."),
            ],
        ),
        score_dimension(
            "Project Structure",
            WEIGHTS["Project Structure"],
            [
                (has(root, "skills/design-craft/references/project-structure.md"), "structure reference exists", "Add project-structure reference."),
                ("shared" in read_text(root / "skills/design-craft/references/project-structure.md").lower(), "shared abstraction rule present", "Define when shared abstractions are allowed."),
                ("directory" in skill.lower(), "directory governance trigger present", "Include directory governance in SKILL.md."),
                (has(root, "scripts/install_local.sh"), "installer exists", "Add local installer."),
            ],
        ),
        score_dimension(
            "Validation Evidence",
            WEIGHTS["Validation Evidence"],
            [
                (has(root, "scripts/validate.sh"), "validation script exists", "Add validation script."),
                ("browser validation" in validation.lower(), "browser validation contract present", "Document browser validation rules."),
                ("browser_screenshot_required" in validation and "browser_screenshot_ops" in validation, "screenshot evidence contract present", "Document screenshot artifact evidence rules."),
                (has(root, "evals/golden-tasks/generic-review-workbench.md"), "generic golden task evidence exists", "Add at least one generic golden real-task card."),
                (has(root, "scripts/design_craft_score.py"), "score script exists", "Add deterministic score script."),
                ("focus-visible" in design_system.lower(), "focus-visible guidance present", "Cover keyboard focus states."),
                ("component state matrix" in design_system.lower(), "component state matrix present", "Cover shared component states."),
                (("voice" in design_system.lower()) and ("content" in design_system.lower()), "voice/content guidance present", "Cover action, error, toast, and empty-state copy."),
                (
                    "vercel geist seed templates" in validation.lower(),
                    "Geist seed validation contract present",
                    "Require delivery to report whether the Geist seed was used.",
                ),
                ("product UI taste score" in validation, "product UI score is distinct from source score", "Distinguish UI taste scores from the workflow source score."),
                (has(root, "scripts/design_craft_taste_review.sh"), "taste review wrapper exists", "Add a stable product UI taste review wrapper."),
                (has(root, "scripts/design_craft_browser_evidence.py"), "browser evidence helper exists", "Add a redacted DOM/computed-style evidence helper."),
                ("anti-inflation" in browser_evidence_helper and "validate_score_json" in browser_evidence_helper, "taste anti-inflation validator exists", "Add a validator for score anti-inflation rules."),
                ("design-craft.browser-evidence.v1" in browser_evidence_helper, "design-craft browser evidence schema exists", "Emit the design-craft browser evidence schema."),
                (has(root, "evals/product-ui-taste/material-ops-home/score.json"), "product UI taste golden case exists", "Add at least one product UI taste calibration case."),
                (has_product_ui_l2_case(root), "product UI taste L2 browser case exists", "Add at least one product UI taste case with browser screenshot and DOM/style evidence."),
                (has_product_ui_l3_case(root), "product UI taste L3 resilient case exists", "Add at least one product UI taste case with responsive and state evidence."),
                (has(root, "evals/product-ui-taste/before-after/README.md"), "L4 before/after eval scaffold exists", "Add L4 before/after eval scaffold."),
                (has_product_ui_l4_before_after_case(root), "product UI taste L4 before/after case exists", "Add a completed L4 before/after product UI case."),
                (has(root, "evals/cross-agent/README.md"), "cross-agent benchmark scaffold exists", "Add cross-agent benchmark scaffold."),
                (has(root, "evals/fixtures/css-smells/card-soup.css"), "static scanner fixture exists", "Add scanner fixtures."),
                ("critique" in read_text(root / "scripts/design_craft_audit.sh"), "critique mode present", "Add a lightweight critique mode."),
                ("motion" in read_text(root / "scripts/design_craft_audit.sh"), "motion mode present", "Add a motion-specific quality pass."),
                ("太 AI" in read_text(root / "skills/design-craft/references/intent-map.md"), "subjective intent mapping present", "Map subjective user phrases to workflow modes."),
                (detector_smoke or not run_smoke, "detector smoke passes", "Fix detector smoke."),
                (score_smoke or not run_smoke, "score smoke passes", "Fix score script smoke."),
                (pass_smoke or not run_smoke, "pass wrapper smoke passes", "Fix pass wrapper smoke."),
                (critique_smoke or not run_smoke, "critique smoke passes", "Fix critique mode smoke."),
                (motion_smoke or not run_smoke, "motion pass smoke passes", "Fix motion pass smoke."),
                (seed_smoke or not run_smoke, "seed helper smoke passes", "Fix Vercel Geist seed helper smoke."),
                (taste_review_smoke or not run_smoke, "taste review wrapper smoke passes", "Fix taste review wrapper smoke."),
            ],
        ),
    ]


def maturity_cap(root: Path) -> tuple[int, list[str]]:
    cap = 100
    reasons: list[str] = []

    eval_files = sorted((root / "evals").glob("*.md")) if (root / "evals").is_dir() else []
    if len(eval_files) < 3:
        cap = min(cap, 86)
        reasons.append("fewer than three forward evals under evals/*.md")

    golden_tasks = sorted((root / "evals/golden-tasks").glob("*.md")) if (root / "evals/golden-tasks").is_dir() else []
    if not golden_tasks:
        cap = min(cap, 94)
        reasons.append("no golden real-task cards under evals/golden-tasks/*.md")

    if not has(root, "scripts/design_craft_audit.sh"):
        cap = min(cap, 90)
        reasons.append("no unified audit/polish/harden/optimize command wrapper yet")

    if not has(root, "evals/forward-test-log.md"):
        cap = min(cap, 92)
        reasons.append("eval prompts exist but no independent forward-test log yet")
    elif not has(root, "evals/live-task-log.md"):
        cap = min(cap, 96)
        reasons.append("independent forward tests passed, but no live implementation task log yet")
    elif "Browser validation: not claimed" in read_text(root / "evals/live-task-log.md") and not has_product_ui_l2_case(root):
        reasons.append("live task log exists; browser validation is intentionally not claimed yet")

    return cap, reasons


def main() -> int:
    parser = argparse.ArgumentParser(description="Score design-craft quality out of 100.")
    parser.add_argument("--target", default=None, help="Repo root or skill path to score.")
    parser.add_argument("--self", action="store_true", help="Score the repo containing this script.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--no-smoke", action="store_true", help="Skip command smoke checks.")
    args = parser.parse_args()

    if args.self:
        root = Path(__file__).resolve().parents[1]
    elif args.target:
        root = infer_root(Path(args.target))
    else:
        root = infer_root(Path.cwd())

    dimensions = build_score(root, run_smoke=not args.no_smoke)
    raw_total = sum(item.score for item in dimensions)
    cap, cap_reasons = maturity_cap(root)
    total = min(raw_total, cap)

    if args.json:
        print(
            json.dumps(
                {
                    "root": str(root),
                    "score": total,
                    "raw_score": raw_total,
                    "maturity_cap": cap,
                    "maturity_cap_reasons": cap_reasons,
                    "max_score": 100,
                    "dimensions": [
                        {
                            "name": item.name,
                            "score": item.score,
                            "weight": item.weight,
                            "evidence": item.evidence,
                            "gaps": item.gaps,
                        }
                        for item in dimensions
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0 if total >= 80 else 1

    print(f"design-craft quality score: {total}/100")
    if total != raw_total:
        print(f"raw heuristic score: {raw_total}/100")
        print(f"maturity cap: {cap}/100")
        for reason in cap_reasons:
            print(f"  - {reason}")
    print(f"root: {root}")
    for item in dimensions:
        print(f"\n{item.name}: {item.score}/{item.weight}")
        for evidence in item.evidence:
            print(f"  + {evidence}")
        for gap in item.gaps:
            print(f"  - {gap}")

    if total < 80:
        print("\nStatus: seed-quality; improve gaps before treating as the default design workflow.")
        return 1
    if total < 90:
        print("\nStatus: usable v0.x; add forward evals and deeper automation before calling it v1.")
    elif total < 94:
        print("\nStatus: advanced v0.3; run independent forward tests before calling it v1.")
    elif total < 97:
        print("\nStatus: v1 pre-release; run one live implementation task before calling it final v1.")
    else:
        print("\nStatus: release-quality; keep validating against real UI/UX/frontend tasks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
