# Changelog

All notable local changes to `design-craft` are recorded here.

## 0.5.0 - Unreleased

- Split installation provenance into `skill_source_dirty` and `repo_dirty`.
  Install parity now remains valid across unrelated ancestor commits and
  repo-level benchmark WIP when the installed skill tree is unchanged, while
  release certification continues to require a completely clean worktree.
- Fixed the native-runtime workflow by compiling the UIKit fixture as a
  library-style `@main` module, enabling KVM access for the Android runner, and
  replacing fragile `/sdcard` UIAutomator pulls with retried
  `/data/local/tmp` capture and `adb exec-out` reads.
- Split the Codex frontend route core into dedicated authority, browser,
  delivery, runtime, and telemetry modules and made all five required by the
  route-pack/snapshot manifest and strict semantic audit.
- Added live runtime truth resolution for `gpt-5.6-sol/max`: paired explicit
  environment evidence wins, the current session's latest `turn_context`
  provides verified fallback evidence, and `config.toml` remains explicitly
  unverified. Session reads are field-limited and evidence paths are redacted
  to Codex-home-relative paths.
- Added privacy-safe route telemetry with context isolation, bounded rotation,
  p50/p95/max summaries, distribution counts, latency thresholds, and a
  dedicated regression test. General route tests, release route smoke, and
  strict route-pack probes now disable telemetry writes and session discovery
  to avoid production-log pollution or caller-session reads.
- Defined two honest maturity levels: the normal portable/local release path
  remains usable at 95/100, while certified 100/100 now additionally requires
  current-source v2 evidence from Codex, Pi, Cursor, and Claude plus observed
  iOS Simulator, Android Emulator, and real-device runtime evidence.
- Added cryptographically bound cross-agent evidence with skill version,
  source commit, skill-tree, prompt, scorecard, and output hashes; v2 scores are
  recomputed from per-criterion earned points instead of accepting arbitrary
  headline integers.
- Allowed host-specific Claude/Cursor skill copies to use separate clean
  provenance only when their complete skill trees match, and made custom score
  output paths validate the artifact that was actually written.
- Bound native evidence to the current `web | iOS | Android | adaptive` release
  skill and fixture trees, required a clean source for certification, and added
  a real iOS runtime interaction with before/after artifacts.
- Added `make release-certify`, release metadata verification, and source/install
  plus Codex route-pack `sync-status` reporting. These contracts prevent the
  95/100 operational release gate from being mistaken for certified 100/100.

- Split the deterministic local release gate from mutable upstream freshness;
  `make release-readiness` now adds the remote review requirement explicitly.
- Changed the scheduled upstream audit from weekly to daily, added GitHub
  compare details, path classification, workflow summaries, retained artifacts,
  and an automatically maintained review-required issue.
- Reviewed the latest Impeccable repository-operations-only commit and Emil
  Kowalski README-only commit without importing unrelated behavior.
- Rebuilt local installation around a lock, same-filesystem staging, atomic
  replacement, rollback, bounded backups, generated provenance metadata, and a
  dedicated source/install verifier that rejects non-ancestor source commits,
  skill-scoped dirty-state, source-root, and source-path mismatches even when
  tree hashes match.
- Added installed `VERSION` and Codex route-pack compatibility contracts,
  refreshed existing legacy aliases by default, and exposed install/route
  compatibility through doctor and maturity checks.
- Replaced duplicate Codex route-pack file lists with the global route-pack
  manifest, added required snapshot-coverage enforcement, included the split
  route/worker cores and routing schema, and moved strict semantic validation to
  the real Python cores plus browser-tool and unauthorized-`ultra` probes.
- Expanded portable CI from a single Python 3.13 lane to a Python
  3.11/3.12/3.13 matrix across both Ubuntu/macOS and Node 22/24.
- Added strict native-runtime evidence schemas, environment probing, and
  self-checks; evidence now requires a present, non-empty, directory-contained
  artifact with matching byte count and SHA-256, so placeholder JSON cannot
  satisfy the maturity gate.
- Added minimal UIKit and Android framework fixtures plus a manual/tag-triggered
  Simulator/Emulator workflow that builds, launches, interacts where supported,
  hashes artifacts, records evidence JSON, and validates it before upload.
- Generalized cross-agent evidence validation so Cursor and Claude can move
  independently from explicit unverified notes to real output/score artifacts.

## 0.4.0 - 2026-07-10

- Expanded the canonical workflow from web/frontend quality into explicit
  `web | iOS | Android | adaptive` product design engineering, with conservative
  platform detection, platform-specific references, native/adaptive fixtures,
  and runtime-validation contracts.
- Added optional `PRODUCT.md` authority for register, platform, users, purpose,
  positioning, and accessibility. `DESIGN.md` remains the sole authority for
  visual direction, tokens, components, themes, and motion.
- Added portable runtime scripts under `skills/design-craft/scripts/`; repo-root
  entries now remain compatibility wrappers, and missing Codex/Impeccable
  integrations emit explicit degraded contracts instead of silent success.
- Added direct-manipulation and interaction-physics guidance covering
  presentation-value interruption, spring response/damping, velocity handoff,
  momentum projection, hysteresis, rubber-banding, and Reduced Motion.
- Separated deterministic source completeness from operational maturity:
  `design_craft_score.py` targets 100/100 source completeness, while
  `design_craft_maturity.py` enforces portable/local maturity gates.
- Set the 0.4.0 operational maturity boundary to 95/100 because iOS Simulator,
  Android Emulator, and real-device native runtime evidence remain unverified
  locally; static scans and fixtures are never presented as runtime proof.
- Added Ubuntu/macOS CI across Node 22/24 and Python 3.13, scheduled
  fail-on-unreviewed upstream audits, platform fixture gates, installed-skill
  runtime checks, and observed Codex/Pi motion plus native-adaptive benchmarks.
- Preserved the remotely added npm lockfile, aligned it to 0.4.0, and made
  `VERSION`, `package.json`, and `package-lock.json` parity a release gate.
- Reviewed the current upstream heads and recorded explicit provenance
  decisions: Emil Kowalski's design-engineering interaction principles were
  absorbed, Impeccable was selectively absorbed, and taste-skill remained
  provenance-only for this range.
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
