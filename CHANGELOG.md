# Changelog

All notable local changes to `design-craft` are recorded here.

## Unreleased

- Upgraded the local Codex route-pack contract to V2: the main agent owns every
  frontend tier by default, model/reasoning inherit from runtime profiles, and
  delegation is conditional on independent work, bounded write scopes,
  authorization, and net coordination benefit.
- Added semantic route-pack validation for stale model pins, worker inheritance,
  V2 route invariants, and redacted runtime model/reasoning compatibility against
  `codex debug models --bundled`.
- Added `agents/worker.toml` and `tools/frontend_preflight_run.sh` to the required
  portable route pack so the executable route contract can no longer drift
  outside structural audits.
- Aligned GPT-5.6 reasoning semantics: explicit frontend overrides now cover
  `low` through `max`, while `ultra` remains runtime-profile-only because the
  bundled model catalog defines it as automatic task delegation.

## 0.3.0 - 2026-07-01

- Added a Codex frontend route-pack audit/export helper plus adapter docs, so
  local `~/.codex` frontend route policy can be hashed, validated, and migrated
  without copying unrelated Codex state.
- Narrowed the canonical `design-craft` trigger description and added an
  explicit "when not to use" boundary for backend-only, database-only,
  algorithm-only, CLI-only, and non-visual refactor tasks.
- Added cross-agent adapter docs for Codex, Cursor, Claude, Pi, and generic
  Agent Skills-compatible clients, plus `design_craft_init_agent.sh` and
  `design_craft_doctor.sh` for portable install dry-runs and capability checks.
- Added `foundational-visual-principles.md` and `design-move-library.md` so the
  workflow can translate taste critique into concrete design moves.
- Added static scanner helpers for CSS smells, focus-state risks, and token
  bypasses, and wired them into detector/validation smoke coverage.
- Added an aggregate `design_craft_static_review.py` helper that normalizes
  scanner results into one JSON handoff packet with severity counts, top
  findings, and design interpretation prompts.
- Expanded the design move library with product-mood treatment variants and
  before/after anatomy patterns for dashboards, tables, forms, landing pages,
  and mobile adaptations.
- Added L4 before/after and cross-agent benchmark scaffolds without counting
  templates as completed evidence.
- Recorded Codex and Pi same-prompt dashboard benchmark outputs while keeping
  Cursor and Claude explicitly unverified for this release.
- Split validation into portable clone-safe checks and local full release
  checks, and changed the default Pi package/install surface to expose only the
  canonical `design-craft` skill unless the legacy alias is requested.
- Added an L4 screenshot manifest validator so before/after cases can check
  screenshot artifact paths, hashes, dimensions, viewport metadata, and layout
  metrics before claiming real evidence.
- Added a generic strict L4 manifest fixture and allowed either
  `path`/`sha256` or `artifact_path`/`artifact_sha256` naming in screenshot
  manifests so TMWD artifact metadata can stay tool-shaped without schema
  rewrites.
- Added a generic invalid L4 manifest fixture plus negative validation so
  strict mode must reject base64 paths, bad hashes, zero dimensions, invalid
  layout metric types, and unmatched before/after artifact keys.
- Added complete L4 before/after case-directory validation with generic valid
  and invalid fixtures, checking required files, placeholder text, score
  evidence, screenshot manifest alignment, and before/after score direction.
- Added the `ops-dashboard-decision-surface-l4` project-neutral L4 fixture,
  capturing a dashboard card-soup to decision-surface before/after improvement
  with repo-external viewport screenshot metadata and strict case validation.

## 0.2.1 - 2026-06-30

- Removed the repository-root `DESIGN.md` because this repository is a reusable
  agent-skill system, not a product UI target.
- Changed route smoke to use a temporary fixture project with its own
  `DESIGN.md`, preserving the rule that real target projects must provide a
  design authority.
- Removed root `DESIGN.md` from validation requirements and clarified that
  `design-craft` supplies workflow guidance only.

## 0.2.0 - 2026-06-30

- Added root `DESIGN.md` as the repository-level style authority for route
  smoke and maintenance checks, without overriding target project authority.
- Documented repository-root route smoke in the README and maintenance
  checklist.
- Added repository-root route smoke to `make release-gate` and moved seed
  dry-run checks to a temporary directory so root `DESIGN.md` stays protected.
- Updated the L3 browser evidence JSON files to the canonical
  `design-craft.browser-evidence.v1` schema while preserving historical
  screenshot artifact paths.
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
