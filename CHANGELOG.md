# Changelog

All notable local changes to `design-craft` are recorded here.

## Unreleased

- Renamed the canonical workflow from `frontend-craft` to `design-craft` to
  reflect the broader long-term scope: UI, UX, visual taste, motion,
  design-system governance, frontend implementation, and product experience
  quality.
- Kept `skills/frontend-craft` and `scripts/frontend_craft_*` as legacy
  compatibility aliases/wrappers only; new route, preflight, install, and
  release-gate paths use `design-craft`.
- Added pinned `emilkowalski/skills` provenance and absorbed its motion quality
  guidance into `references/motion-quality.md` and
  `references/motion-vocabulary.md`.
- Added a first-class `motion` quality pass plus detector signals for
  transition-all, ease-in UI responses, scale(0), origin-aware popovers, long UI
  durations, layout-property animation, hover gating, and reduced-motion review.
- Added `scripts/design_craft_browser_evidence.py` plus the
  `evals/product-ui-taste/groland-content-assets-l3` case to validate
  redacted DOM/computed-style evidence, responsive/state L3 coverage, and
  anti-inflation rules for product UI taste scores.
- Added `evals/product-ui-taste/live-browser-samples` with four real Chrome
  tab L2 product UI taste calibration samples backed by TMWD screenshot
  artifacts and DOM/computed-style evidence.
- Validation now checks every product UI taste `score.json` and requires at
  least one L2+ browser evidence case.
- Added TMWD `browser_screenshot_ops` screenshot evidence to the frontend
  validation contract, route summary, and delivery expectations.
- Added `references/product-ui-taste-review.md` for concrete product UI scoring,
  top issues, page-type checks, frontend implementation notes, and acceptance
  criteria without bloating `SKILL.md`.
- Added `references/taste-score-calibration.md`,
  `scripts/design_craft_taste_review.sh`, and the first
  `evals/product-ui-taste/material-ops-home` calibration case so screenshot
  taste scores carry evidence levels, score bands, and false-positive guards.
- Added `scripts/upstream_absorption_report.py --remote` for non-mutating remote
  upstream drift checks before syncing submodules.
- Updated the pinned `impeccable` upstream to
  `c979ac37c361da564dcce100a4f2623d94ef54c8` and absorbed its critique
  provenance/degraded-run guidance into the local fusion layer.
- Added `scripts/design_craft_pass.sh` as the preferred neutral wrapper for
  critique/audit/polish/harden/optimize/structure/architecture passes while
  keeping `design_craft_audit.sh` as a compatibility entrypoint.
- Added `references/intent-map.md` to map subjective requests such as "太 AI",
  "颜色平", "排版不对", "文案弱", "移动端差", and "卡顿" to the smallest useful
  design-craft pass.
- Added `scripts/design_craft_seed_design.sh` to seed `DESIGN.md` and
  `DESIGN.dark.md` from the bundled Vercel Geist templates without overwriting
  existing project authority unless `--force` is explicit.
- Added `critique` as a first-class read-only design-craft pass for
  design-rightness, product fit, hierarchy, and anti-slop review.
- Added route-summary `vercel_geist_seed_applicable` output so weak
  developer-product surfaces expose the default seed decision explicitly.
- Vendored Vercel Geist `design.md` and `design.dark.md` as complete default
  seed templates for new or weak developer-product design systems.
- Added a design-system contract reference covering `DESIGN.md` structure,
  token role separation, theme parity, component states, focus-visible, motion,
  and UI copy quality.
- Renamed the internal visual reference from `design-taste.md` to
  `visual-judgment.md` to make `design-craft` the active workflow and keep
  upstream taste-skill only as provenance/manual absorption input.
- Added the first golden real-task card for DataHub `marketing/industry-news`
  route behavior and validation expectations.
- Added an upstream absorption report command to classify pinned submodule drift
  before manually merging upstream ideas into the fusion layer.
- Extended the detector wrapper with local design-craft review signals while
  preserving raw upstream JSON compatibility.

## 0.1.0 - 2026-06-24

- Initialized `design-craft` as a personal Codex frontend workflow skill.
- Added a fusion layer that combines local route planning, `DESIGN.md`
  authority, browser validation, taste-skill anti-slop guidance, and
  Impeccable-style audit/polish/harden/optimize/detector loops.
- Added pinned upstream provenance for `taste-skill` and `impeccable`.
- Added deterministic helper scripts for route summaries, detector runs, source
  scoring, local install, upstream sync, and validation.
- Added forward-test and DataHub/report-oriented evaluation artifacts.
- Added local maintenance and release-gate documentation.
