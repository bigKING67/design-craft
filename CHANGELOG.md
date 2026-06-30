# Changelog

All notable local changes to `frontend-craft` are recorded here.

## Unreleased

- Added TMWD `browser_screenshot_ops` screenshot evidence to the frontend
  validation contract, route summary, and delivery expectations.
- Added `references/product-ui-taste-review.md` for concrete product UI scoring,
  top issues, page-type checks, frontend implementation notes, and acceptance
  criteria without bloating `SKILL.md`.
- Added `references/taste-score-calibration.md`,
  `scripts/frontend_craft_taste_review.sh`, and the first
  `evals/product-ui-taste/material-ops-home` calibration case so screenshot
  taste scores carry evidence levels, score bands, and false-positive guards.
- Added `scripts/upstream_absorption_report.py --remote` for non-mutating remote
  upstream drift checks before syncing submodules.
- Updated the pinned `impeccable` upstream to
  `c979ac37c361da564dcce100a4f2623d94ef54c8` and absorbed its critique
  provenance/degraded-run guidance into the local fusion layer.
- Added `scripts/frontend_craft_pass.sh` as the preferred neutral wrapper for
  critique/audit/polish/harden/optimize/structure/architecture passes while
  keeping `frontend_craft_audit.sh` as a compatibility entrypoint.
- Added `references/intent-map.md` to map subjective requests such as "太 AI",
  "颜色平", "排版不对", "文案弱", "移动端差", and "卡顿" to the smallest useful
  frontend-craft pass.
- Added `scripts/frontend_craft_seed_design.sh` to seed `DESIGN.md` and
  `DESIGN.dark.md` from the bundled Vercel Geist templates without overwriting
  existing project authority unless `--force` is explicit.
- Added `critique` as a first-class read-only frontend-craft pass for
  design-rightness, product fit, hierarchy, and anti-slop review.
- Added route-summary `vercel_geist_seed_applicable` output so weak
  developer-product surfaces expose the default seed decision explicitly.
- Vendored Vercel Geist `design.md` and `design.dark.md` as complete default
  seed templates for new or weak developer-product design systems.
- Added a design-system contract reference covering `DESIGN.md` structure,
  token role separation, theme parity, component states, focus-visible, motion,
  and UI copy quality.
- Renamed the internal visual reference from `design-taste.md` to
  `visual-judgment.md` to make `frontend-craft` the active workflow and keep
  upstream taste-skill only as provenance/manual absorption input.
- Added the first golden real-task card for DataHub `marketing/industry-news`
  route behavior and validation expectations.
- Added an upstream absorption report command to classify pinned submodule drift
  before manually merging upstream ideas into the fusion layer.
- Extended the detector wrapper with local frontend-craft review signals while
  preserving raw upstream JSON compatibility.

## 0.1.0 - 2026-06-24

- Initialized `frontend-craft` as a personal Codex frontend workflow skill.
- Added a fusion layer that combines local route planning, `DESIGN.md`
  authority, browser validation, taste-skill anti-slop guidance, and
  Impeccable-style audit/polish/harden/optimize/detector loops.
- Added pinned upstream provenance for `taste-skill` and `impeccable`.
- Added deterministic helper scripts for route summaries, detector runs, source
  scoring, local install, upstream sync, and validation.
- Added forward-test and DataHub/report-oriented evaluation artifacts.
- Added local maintenance and release-gate documentation.
