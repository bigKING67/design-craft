#!/usr/bin/env python3
"""Deterministic frontend-craft quality scorer."""

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


def infer_root(target: Path) -> Path:
    target = target.expanduser().resolve()
    if target.is_file():
        target = target.parent
    if (target / "skills/frontend-craft/SKILL.md").is_file():
        return target
    if target.name == "frontend-craft" and (target / "SKILL.md").is_file():
        return target.parents[1]
    for parent in [target, *target.parents]:
        if (parent / "skills/frontend-craft/SKILL.md").is_file():
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
    skill = read_text(root / "skills/frontend-craft/SKILL.md")
    validation = read_text(root / "skills/frontend-craft/references/validation-contract.md")
    design_system = read_text(root / "skills/frontend-craft/references/design-system-contract.md")
    report = read_text(root / "skills/frontend-craft/references/report-quality.md")
    surface = read_text(root / "skills/frontend-craft/references/surface-playbooks.md")
    source_map = read_text(root / "skills/frontend-craft/references/source-map.md")

    detector_smoke = False
    score_smoke = False
    critique_smoke = False
    seed_smoke = False
    if run_smoke:
        detector_smoke = check_command(
            ["bash", "scripts/frontend_craft_detect.sh", "--target", "skills/frontend-craft", "--json-only"],
            root,
        )
        score_smoke = check_command(
            [sys.executable, "scripts/frontend_craft_score.py", "--target", str(root), "--no-smoke", "--json"],
            root,
        )
        critique_smoke = check_command(
            ["bash", "scripts/frontend_craft_audit.sh", "--target", "skills/frontend-craft", "--mode", "critique", "--skip-route", "--skip-score"],
            root,
        )
        seed_smoke = check_command(
            ["bash", "scripts/frontend_craft_seed_design.sh", "--target", "skills/frontend-craft", "--dry-run"],
            root,
        )

    return [
        score_dimension(
            "Visual Judgment",
            WEIGHTS["Visual Judgment"],
            [
                (has(root, "skills/frontend-craft/references/visual-judgment.md"), "visual-judgment reference exists", "Add visual-judgment reference."),
                ("anti-slop" in skill.lower() or "anti-slop" in read_text(root / "skills/frontend-craft/references/visual-judgment.md").lower(), "anti-slop encoded", "Encode anti-slop visual judgment."),
                ("design read" in skill.lower(), "design read required", "Require a concise design read for major visual work."),
                ("generic AI tells" in skill or "generic" in read_text(root / "skills/frontend-craft/references/visual-judgment.md").lower(), "generic-output guard present", "Add generic-output failure modes."),
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
                (has(root, "skills/frontend-craft/references/design-system-contract.md"), "design-system contract exists", "Add design-system contract reference."),
                (
                    has(root, "skills/frontend-craft/templates/vercel-geist/design.md")
                    and has(root, "skills/frontend-craft/templates/vercel-geist/design.dark.md"),
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
                    has(root, "scripts/frontend_craft_seed_design.sh"),
                    "Vercel Geist seed helper exists",
                    "Add a helper for seeding DESIGN.md from the bundled Geist templates.",
                ),
                (
                    "vercel_geist_seed_applicable" in read_text(root / "scripts/frontend_craft_route.sh"),
                    "route summary reports Vercel seed applicability",
                    "Make route summaries say when the Geist seed is applicable.",
                ),
                ("theme parity" in design_system.lower(), "theme parity guidance present", "Cover light/dark token parity."),
                ("token layers" in design_system.lower(), "token layer guidance present", "Cover token role separation."),
            ],
        ),
        score_dimension(
            "Engineering Quality",
            WEIGHTS["Engineering Quality"],
            [
                (has(root, "skills/frontend-craft/references/engineering-quality.md"), "engineering reference exists", "Add engineering-quality reference."),
                ("component" in read_text(root / "skills/frontend-craft/references/engineering-quality.md").lower(), "component boundary guidance present", "Add component boundary guidance."),
                ("observable" in skill.lower() or "errors" in read_text(root / "skills/frontend-craft/references/engineering-quality.md").lower(), "error observability covered", "Cover observable errors."),
                (has(root, "scripts/frontend_craft_route.sh"), "route wrapper exists", "Add route wrapper script."),
                (has(root, "scripts/frontend_craft_detect.sh"), "detector wrapper exists", "Add detector wrapper script."),
            ],
        ),
        score_dimension(
            "Performance",
            WEIGHTS["Performance"],
            [
                (has(root, "skills/frontend-craft/references/performance-quality.md"), "performance reference exists", "Add performance-quality reference."),
                ("Web Vitals" in read_text(root / "skills/frontend-craft/references/performance-quality.md"), "Web Vitals covered", "Cover Web Vitals."),
                ("charts" in read_text(root / "skills/frontend-craft/references/performance-quality.md").lower(), "chart/table performance covered", "Cover chart/table performance."),
                ("measure" in skill.lower() or "baseline" in read_text(root / "skills/frontend-craft/references/impeccable-workflow.md").lower(), "measurement-first rule present", "Require measurement before optimization."),
            ],
        ),
        score_dimension(
            "Architecture",
            WEIGHTS["Architecture"],
            [
                (has(root, "skills/frontend-craft/references/architecture-quality.md"), "architecture reference exists", "Add architecture-quality reference."),
                (has(root, "upstreams.lock.json"), "upstream lock exists", "Add upstream lock file."),
                (has(root, "skills/frontend-craft/references/source-map.md"), "source map exists", "Add source-map reference."),
                (has(root, "scripts/upstream_absorption_report.py"), "upstream absorption report exists", "Add upstream absorption report script."),
                ("templates/vercel-geist/design.md" in source_map, "Vercel Geist source map present", "Map vendored Vercel templates in source-map."),
                (("data flow" in read_text(root / "skills/frontend-craft/references/architecture-quality.md").lower()) or ("data-flow" in read_text(root / "skills/frontend-craft/references/architecture-quality.md").lower()), "data-flow guidance present", "Add data-flow guidance."),
                ("migration" in read_text(root / "skills/frontend-craft/references/architecture-quality.md").lower(), "migration risk covered", "Add migration/compatibility guidance."),
            ],
        ),
        score_dimension(
            "Project Structure",
            WEIGHTS["Project Structure"],
            [
                (has(root, "skills/frontend-craft/references/project-structure.md"), "structure reference exists", "Add project-structure reference."),
                ("shared" in read_text(root / "skills/frontend-craft/references/project-structure.md").lower(), "shared abstraction rule present", "Define when shared abstractions are allowed."),
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
                (has(root, "evals/golden-tasks/datahub-industry-news.md"), "golden task evidence exists", "Add at least one golden real-task card."),
                (has(root, "scripts/frontend_craft_score.py"), "score script exists", "Add deterministic score script."),
                ("focus-visible" in design_system.lower(), "focus-visible guidance present", "Cover keyboard focus states."),
                ("component state matrix" in design_system.lower(), "component state matrix present", "Cover shared component states."),
                (("voice" in design_system.lower()) and ("content" in design_system.lower()), "voice/content guidance present", "Cover action, error, toast, and empty-state copy."),
                (
                    "vercel geist seed templates" in validation.lower(),
                    "Geist seed validation contract present",
                    "Require delivery to report whether the Geist seed was used.",
                ),
                ("critique" in read_text(root / "scripts/frontend_craft_audit.sh"), "critique mode present", "Add a lightweight critique mode."),
                (detector_smoke or not run_smoke, "detector smoke passes", "Fix detector smoke."),
                (score_smoke or not run_smoke, "score smoke passes", "Fix score script smoke."),
                (critique_smoke or not run_smoke, "critique smoke passes", "Fix critique mode smoke."),
                (seed_smoke or not run_smoke, "seed helper smoke passes", "Fix Vercel Geist seed helper smoke."),
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

    if not has(root, "scripts/frontend_craft_audit.sh"):
        cap = min(cap, 90)
        reasons.append("no unified audit/polish/harden/optimize command wrapper yet")

    if not has(root, "evals/forward-test-log.md"):
        cap = min(cap, 92)
        reasons.append("eval prompts exist but no independent forward-test log yet")
    elif not has(root, "evals/live-task-log.md"):
        cap = min(cap, 96)
        reasons.append("independent forward tests passed, but no live implementation task log yet")
    elif "Browser validation: not claimed" in read_text(root / "evals/live-task-log.md"):
        reasons.append("live task log exists; browser validation is intentionally not claimed yet")

    return cap, reasons


def main() -> int:
    parser = argparse.ArgumentParser(description="Score frontend-craft quality out of 100.")
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

    print(f"frontend-craft quality score: {total}/100")
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
        print("\nStatus: seed-quality; improve gaps before treating as the default frontend workflow.")
        return 1
    if total < 90:
        print("\nStatus: usable v0.x; add forward evals and deeper automation before calling it v1.")
    elif total < 94:
        print("\nStatus: advanced v0.3; run independent forward tests before calling it v1.")
    elif total < 97:
        print("\nStatus: v1 pre-release; run one live implementation task before calling it final v1.")
    else:
        print("\nStatus: release-quality; keep validating against real frontend tasks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
