# Changelog

All notable local changes to `design-craft` are recorded here.

## 0.5.2 - Unreleased

- Normalize the `actions/upload-artifact` certification digest output from raw
  hexadecimal or canonical `sha256:` form into the canonical release receipt
  format, and enforce that normalization through the workflow contract gate.

## 0.5.1 - 2026-07-24

- Reviewed post-candidate upstream drift without advancing compatibility pins:
  Taste sponsor-only changes are provenance-only; Impeccable's
  workspace-relative artifact guidance is already represented, while forced
  subagent authorization and provider/runtime copies remain rejected.
- Split final certification from publication so evidence and exact assets can
  be certified without granting release-write or attestation permissions, and
  split publication itself into read-only verification plus a digest-only write
  job that executes no repository validation code.
- Made native release-evidence bindings artifact-relative and independently
  relocatable while retaining temporary read compatibility for v0.5.0 absolute
  runner paths.
- Added benchmark result schema v2 with stable runner-family identity, explicit
  v1 migration, and diagnostic-only kernel/image patch metadata.
- Added a fail-closed `RELEASE_GOVERNANCE_TOKEN` preflight with machine-readable
  credential and Administration-permission error classification.
- Archived the exact v0.5.0 comparative and cross-agent evidence under immutable
  history roots and reset active v0.5.1 task directories to definition/pending
  state instead of presenting released evidence as current-source proof.
- Recorded fresh Codex and Pi cross-agent score-v4/run-v2 evidence for the
  dashboard, motion, and native/adaptive tasks against the clean
  `main@7429d8d` Skill tree; Cursor and Claude remain explicitly pending.
- Re-ran all four Pi ablations with an isolated Codex blind judge. `design-craft`
  won motion `98/95/84`, motion planning `96/81/78`, visual critique
  `99/94/97`, and production hardening `96/95/91` against the focused upstream
  and no-skill variants.
- Promoted a schema-v2 Ubuntu 24.04/Python 3.13 full benchmark baseline from
  run `30064094199` (artifact SHA-256
  `8294b7ef04343cd4e72c7733d530fcdbeec8681015c931592d1f0fff388ec1a9`)
  after three hosted full runs and a passing cluster comparison with run
  `30064371635`; the operational-candidate workflow now consumes that v0.5.1
  baseline instead of the legacy v1 baseline.

## 0.5.0 - 2026-07-23

- Added a five-Skill Emil Kowalski absorption contract and human-readable
  matrix. The gate verifies all five entrypoints, three auxiliary Markdown
  files, local capability mappings, the pinned commit, and the upstream fact
  that there is no non-Markdown implementation library to vendor.
- Deepened the Emil fusion with concrete web motion recipes, tooltip/transient
  lifecycle handling, reusable-component craft, optical typography details,
  and the previously omitted spring, ambient-motion, and animation-principle
  vocabulary while explicitly rejecting overbroad static performance claims,
  forced delegation/read-only policy, and promotional response text.
- Fixed remote portability validation by resolving the platform-specific npm
  executable and fetching the privacy-history baseline in portable/Windows CI.
  Hardened iOS runtime evidence around a fresh ephemeral Simulator and a fully
  declared URL scheme so stale hosted-runner migration state cannot invalidate
  the deep-link interaction proof.
- Added a root MIT license, preserved upstream Apache/MIT license and notice
  text, and documented the separate Vercel snapshot redistribution boundary.
- Restricted the Pi/npm payload to the canonical skill plus required legal
  metadata. A deterministic package gate now rejects repository-only paths,
  user-home strings, payloads above 1 MB compressed or 2 MB unpacked, and more
  than 100 files.
- Replaced committed workstation-specific evidence paths with home-relative or
  documented repository aliases and added a whole-repository privacy and
  portability gate for macOS, Linux, and Windows user-home paths.
- Split historical L4 metadata validation from real artifact availability.
  Normal portable/local gates no longer overstate repo-external screenshots,
  while certified releases require every referenced L4 artifact to exist.
- Made 100-point certification two-phase: all source, remote, evidence, native,
  and temporary-install checks now pass before the live skill installation is
  atomically published.
- Added a `desktop` maturity profile for the actual installed computer-based
  frontend workflow. It normalizes the applicable local gates to 100/100 while
  reporting four-host and physical-device gaps as optional release
  certification status; the existing portable/local and `release-certify`
  contracts remain strict and unchanged.
- Replaced the old cross-agent invocation path with isolated run-manifest v2
  workspaces and score schema v3. Every host now copies and hashes the exact
  Skill tree it used, fingerprints the source worktree before/after execution,
  and derives host/model/command metadata from the controlled run. Existing
  Codex/Pi artifacts remain historical until all four hosts are rerun against a
  clean current source; Cursor/Claude evidence is not claimed in advance.
- Moved the former Codex/Pi v2 benchmarks into self-contained historical
  snapshots with their matching old prompts and scorecards. Active cases now
  carry explicit four-host unverified notes until real v3/run-v2 evidence is
  generated; hash editing or field backfills cannot promote history.
- Preserved per-runtime native truth while upgrading certification to evidence
  schema v3 and role-specific artifacts. Earlier Simulator/Emulator v2 evidence
  is archived as immutable history until regenerated against the final clean
  source, and physical-device evidence remains required independently.
- Split operational maturity from certification evidence: validated historical
  run baselines support the normal 95/100 workflow, while current four-host and
  native evidence exclusively controls the 95-to-100 certification cap.
- Added compact JSON and human-readable frontend route outputs so normal agent
  handoffs do not need to ingest the full static delivery contract. Moved
  architecture-intent and performance-surface triggers into the routing JSON
  truth source, added schema and semantic probes, and removed stale `0.4.x`
  wording from the route-v2 delivery contract.
- Reworked iOS certification around a real `simctl openurl` transition against
  the running app with a cold deep-link fallback, explicit URL-received logs,
  and no test-only confirmation argument. Strengthened Android activity/UI
  readiness and system-dialog recovery, and upgraded GitHub Actions pins to
  their current Node 24 runtime releases.
- Added Dependabot coverage for GitHub Actions and npm metadata while retaining
  full-SHA action pinning and normal review gates.
- Added a Windows Git Bash portable CI lane while keeping its status explicit:
  native Windows remains pending until the current-source remote lane succeeds;
  WSL is a compatible fallback rather than separate certification evidence.
- Reduced broad-task context loading to a three-reference core with explicit
  conditional additions, preventing cross-host context dilution from loading
  the full reference library by default.
- Extracted package metadata and workflow/native contract checks from the
  monolithic validation shell into independently testable validators.
- Split installation provenance into `skill_source_dirty` and `repo_dirty`.
  Install parity now remains valid across unrelated ancestor commits and
  repo-level benchmark WIP when the installed skill tree is unchanged, while
  release certification continues to require a completely clean worktree.
- Bound installation provenance to the actual `skills/<name>` tree stored at
  the recorded source commit, so naming an unrelated ancestor can no longer
  pass merely because the current and installed trees happen to match.
- Added a single-writer release lock with start/end HEAD and clean-worktree
  invariants, and bound tag verification to the latest tag-triggered workflow
  runs instead of accepting any older success for the same commit.
- Fixed the native-runtime workflow by compiling the UIKit fixture as a
  library-style `@main` module, enabling KVM access for the Android runner, and
  replacing fragile `/sdcard` UIAutomator pulls with retried
  `/data/local/tmp` capture and `adb exec-out` reads. The iOS deep-link
  interaction now uses the required `UIScene` lifecycle for both cold-launch
  and already-running URL contexts, then waits for a bounded,
  filesystem-backed confirmation marker.
- Hardened native evidence with platform-specific assertion and artifact-role
  contracts, hashed runtime identifiers, XML/PNG content validation, decisive
  Android before/after tree hashes, push-time fixture builds, and a reproducible
  physical Android device capture runner.
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
  current-source score schema v3/run-manifest v2 evidence from Codex, Pi,
  Cursor, and Claude plus observed
  iOS Simulator, Android Emulator, and real-device runtime evidence.
- Added cryptographically bound cross-agent evidence with skill version,
  source commit, skill-tree, prompt, scorecard, output, run-manifest, and
  runner/adapter-contract hashes; v3 scores are recomputed from per-criterion
  earned points instead of accepting arbitrary headline integers.
- Added two controlled no-skill/current-Emil/design-craft ablations. The Pi
  runner isolates all three variants, anonymizes outputs, and requires an
  independent blind judge whose raw output, normalized judgment, host metadata,
  and worktree fingerprints are preserved. Real observed runs remain a strict
  release requirement rather than being inferred from offline self-checks.
- Selectively absorbed Emil's `improve-animations` recon, frequency-map,
  eight-dimension audit, vetted prioritization, self-contained planning, and
  reconciliation workflow. Added `motion-plan` mode and a deterministic plan
  scaffold while keeping absolute heuristics subordinate to project authority
  and runtime evidence.
- Added a deterministic native Release bundle that binds the exact latest
  successful `v<VERSION>` tag-push run, iOS Simulator, Android Emulator, and
  physical-device evidence. Its validator rejects undeclared or duplicate tar
  members, links/devices, path traversal, non-normalized metadata, stale source
  hashes, and non-deterministic builds. GitHub Release verification now requires
  six assets across the package and native triplets.
- Added dependency-free Python/shell/JSON/Node lint plus a dedicated contract
  test lane for cross-agent, comparative, native, release, workflow, and
  governance self-checks. All Validate jobs now have timeouts and workflow
  concurrency policies.
- Hardened GitHub branch/tag ruleset validation: both rulesets require empty
  bypass lists, the main branch requires all 12 matrix jobs plus Android,
  Windows, lint, and contract-test contexts, and branch creation remains exempt
  only through `do_not_enforce_on_create=true`.
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
- Reviewed pinned Impeccable repository-operations-only and Emil README-only
  ranges without importing unrelated behavior; mutable remote freshness remains
  a release-time gate rather than a historical changelog claim.
- Rebuilt local installation around a lock, same-filesystem staging, atomic
  replacement, rollback, bounded backups, generated provenance metadata, and a
  dedicated source/install verifier that rejects non-ancestor source commits,
  skill-scoped dirty-state, source-root, and source-path mismatches even when
  tree hashes match.
- Removed active-install parity from `release-gate-source`; the atomic installer
  now runs first and `sync-status-check` is enforced immediately afterward,
  eliminating the stale-install circular dependency.
- Added installed `VERSION` and Codex route-pack compatibility contracts,
  refreshed existing legacy aliases by default, and exposed install/route
  compatibility through doctor and maturity checks.
- Replaced duplicate Codex route-pack file lists with the global route-pack
  manifest, added required snapshot-coverage enforcement, included the split
  route/worker cores and routing schema, and moved strict semantic validation to
  the real Python cores plus browser-tool and unauthorized-`ultra` probes.
- Expanded portable CI from a single Python 3.13 lane to a Python
  3.11/3.12/3.13 matrix across Ubuntu/macOS and Node 22/24, plus Windows Git
  Bash, Android fixture build, lint, and contract-test lanes.
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
