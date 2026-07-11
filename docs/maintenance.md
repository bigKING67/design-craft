# design-craft maintenance

This document is the local release and maintenance checklist for
`design-craft`.

## Maintenance rules

- Keep `upstreams/` pristine. Do not edit `upstreams/taste-skill`,
  `upstreams/impeccable`, or `upstreams/emilkowalski-skills` directly.
- Keep the installable skill lean. `README.md`, `CHANGELOG.md`, release notes,
  and maintenance docs belong at the repo root or under `docs/`, not inside
  `skills/design-craft/`.
- Keep the published Pi/npm payload narrower than the repository. The package
  may contain only `skills/design-craft`, required root metadata, and preserved
  license/notice files; never publish `upstreams/`, `evals/`, workflows, or
  repository-only scripts.
- Preserve the root MIT license plus upstream license and notice text in
  `LICENSES/`. Do not treat the design-craft MIT license as relicensing the
  Vercel design snapshots.
- Keep project-specific truth above generic visual guidance:
  live runtime behavior, scoped `AGENTS.md`, README/framework conventions, and
  optional project `PRODUCT.md` plus project `DESIGN.md` outrank the fusion
  references. PRODUCT owns product/platform facts; DESIGN remains the only
  visual/token/component/theme/motion authority.
- Treat `upstreams/taste-skill`, `upstreams/impeccable`, and
  `upstreams/emilkowalski-skills` as provenance and deliberate absorption inputs
  only. Do not reintroduce automatic upstream skill overwrites or legacy taste
  routing.
- Keep helper scripts deterministic and cheap enough to run before real
  UI/UX/design/frontend work.
- Keep OS support explicit: repository automation is verified on macOS/Linux;
  Windows requires WSL or a compatible Git Bash environment and remains
  unverified without a native Windows CI lane.
- Keep the deterministic release gate independent of mutable upstream remote
  heads. Remote freshness is a separate release-readiness and scheduled audit.
- Keep GitHub Actions pinned to full reviewed SHAs. Dependabot may propose
  GitHub Actions or npm metadata updates, but those changes still require the
  normal validation and review gates.
- Keep package, public-repository, and workflow/native contract checks in their
  dedicated validators rather than expanding the monolithic validation shell.
- Keep 95/100 operational readiness distinct from certified 100/100. The latter
  requires current-source v2 four-host and native runtime evidence and must not
  be inferred from legacy artifacts or workflow definitions.
- Keep certification prepublish checks non-mutating. Verify installation in a
  temporary skill root first; update the live `~/.agents/skills` copy only
  after all 100-point gates pass.
- Keep agent-specific install behavior in `adapters/` and scripts. Do not fork
  the canonical `skills/design-craft/` content per agent.
- Keep the Codex frontend route layer portable through the route-pack manifest
  helper. Do not copy unrelated `~/.codex` state, credentials, browser profile
  files, caches, or session logs into this repo.
- Record meaningful task evidence under `evals/`; do not claim browser
  validation unless a browser validation actually ran.
- Keep public evidence machine-neutral. Use `~`, repository-relative paths, or
  documented aliases such as `PRODUCT_REPO` and `DESIGN_CRAFT_HOME`; never
  commit named macOS, Linux, or Windows user-home paths.
- Do not add a root `DESIGN.md` to this repository. `design-craft` is a reusable
  skill/workflow system, not a product UI target. Target projects must provide
  their own `DESIGN.md` or pass an explicit style authority path for L1+ route
  checks.

## Portable validation gate

Run this on a fresh clone or another machine before trusting the package shape:

```bash
make validate-portable
```

It expands to portable checks only: required files, package/version
consistency, npm pack size/path hygiene, shell syntax, Python compile,
bundled-runtime independence,
platform fixtures, observed benchmark artifacts, L4 validators, static
scanners, 100/100 source completeness, and 95/100 portable maturity. It does
not depend on local Codex state, installed-skill parity, native SDKs, or remote
upstream freshness.

Expected result:

- Required references, scripts, notices, evals, and version files exist.
- Shell scripts pass `bash -n`.
- Python scripts compile and core validators run.
- Static smell scanners and the aggregate static review packet run against
  fixture targets.
- Cross-agent task definitions validate.
- Observed dashboard, motion, and native-adaptive Codex/Pi artifacts validate.
- iOS, Android, and adaptive valid/invalid source fixtures separate correctly.
- Portable route/detector degraded paths are explicit, and copied installed-skill
  L4 helpers run without the source repo.
- Project-neutral L4 fixtures validate in strict mode.
- Version in `VERSION` matches `package.json`.
- `npm pack --dry-run` remains within 1 MB compressed, 2 MB unpacked, and 100
  files, contains the canonical skill and required legal metadata, and excludes
  repository-only paths and user-home strings.
- Source completeness is 100; portable maturity is 95 with the native-runtime
  and four-host certification caps stated rather than hidden.
- CI covers Python 3.11, 3.12, and 3.13 across Ubuntu/macOS and Node 22/24.
- Native runtime CI definitions and minimal fixtures validate structurally, but
  only a completed workflow run and reviewed artifact JSON count as observed
  Simulator/Emulator evidence.

## Local release gate

Run this before a version bump, initial commit, or route-policy change:

```bash
make release-gate-local
```

`make release-gate` remains a compatibility alias for the local full gate. It
does not query mutable upstream remote heads.

It expands to:

```bash
bash scripts/validate.sh --portable
python3 scripts/design_craft_package_validate.py --check --validate
python3 scripts/design_craft_public_repo_validate.py --check --validate
python3 "$SKILL_CREATOR_QUICK_VALIDATE" skills/design-craft
python3 "$SKILL_CREATOR_QUICK_VALIDATE" skills/frontend-craft
python3 scripts/design_craft_score.py --self
python3 scripts/design_craft_maturity.py --profile portable --min-score 95
bash scripts/design_craft_pass.sh --target . --mode audit --skip-route
bash scripts/design_craft_audit.sh --target . --mode audit --skip-route
bash scripts/design_craft_audit.sh --target . --mode critique --skip-route
bash scripts/design_craft_pass.sh --target skills/design-craft --mode motion --skip-route --skip-score
bash scripts/design_craft_taste_review.sh --target skills/design-craft --context "release smoke" --evidence-level L0
tmp_dir="$(mktemp -d -t design-craft-seed-dry-run.XXXXXX)" && trap 'rm -rf "${tmp_dir}"' EXIT && bash scripts/design_craft_seed_design.sh --target "${tmp_dir}" --dry-run
make route-smoke
bash scripts/design_craft_doctor.sh --target . --json
make platform-scan-check
python3 scripts/design_craft_codex_route_pack.py --strict
make init-dry-run
make historical-l4-metadata-check
make cross-agent-observed-check
make smell-smoke
python3 scripts/upstream_absorption_report.py
bash scripts/install_local.sh
python3 scripts/design_craft_install_verify.py --source skills/design-craft --installed "${DESIGN_CRAFT_SKILL_ROOT:-$HOME/.agents/skills}/design-craft" --expected-name design-craft --expected-version "$(cat VERSION)" --require-metadata
python3 scripts/design_craft_maturity.py --profile local --min-score 95
bash scripts/install_local.sh --dry-run --include-legacy-alias
```

Expected result:

- Skill schema passes `quick_validate.py`.
- Required references, scripts, notices, evals, and version files exist.
- Shell scripts pass `bash -n`.
- Python scorer compiles and runs.
- Detector smoke passes against `skills/design-craft` and keeps raw
  `--json-only` compatibility for upstream Impeccable output.
- Preferred pass wrapper, audit wrapper, and critique mode smokes pass.
- Motion-specific pass smoke passes and the Emil-derived motion references are
  present.
- Product UI taste-review packet smoke passes and keeps score evidence levels
  explicit.
- Product UI browser evidence helper compiles, emits a redacted TMWD DOM/style
  sampler, and validates score anti-inflation plus DOM evidence JSON.
- Static smell scanners compile and run against fixture targets.
- The aggregate static review helper returns normalized severity counts and
  interpretation prompts.
- Adapter docs exist, and init dry-runs cover Codex, Cursor, Claude, Pi, and
  generic Agent Skills-compatible installs without writing files.
- Doctor output runs without mutating files and reports required optional
  capabilities truthfully.
- Codex route-pack audit confirms the local frontend route planner, frontend
  rule, preflight contract, and route tests are present and hashable.
- Vercel Geist seed helper smoke passes and preserves template byte parity.
- Route smoke passes against a temporary fixture project with its own
  `DESIGN.md`, preserving the contract that product targets provide their own
  design authority.
- Historical real-project L4 metadata validates in the normal local full gate;
  current public examples stay project-neutral. Certified 100/100 additionally
  runs `make real-l4-check`, which requires every referenced screenshot file to
  exist on the certification machine.
- Observed cross-agent evidence validates for the hosts that actually ran the
  same benchmark prompt. Uncollected hosts must remain explicitly unverified.
- Local maturity reports 95/100. Current-source iOS Simulator and Android
  Emulator artifacts are observed and validated; physical-device evidence
  remains missing. The maturity JSON reports these three statuses separately
  while the aggregate certification gate stays capped at 95 until all pass.
- Desktop maturity reports 100/100 for the installed computer-based frontend
  workflow. It excludes optional four-host and physical-device certification
  from the daily-development score without weakening `release-certify`.
- Upstream absorption report runs without fetching or modifying submodules; the
  optional `--remote` check reports remote drift with `git ls-remote`.
- Upstream lock commits match checked-out submodule commits.
- Installed canonical skill matches the source and carries valid version,
  source commit, dirty-state, exact tree digest, install-time, and source-repo
  provenance.
- The installer uses staging, an install lock, atomic replacement, rollback,
  and bounded backup retention. The `frontend-craft` alias is not created by
  default, but an existing alias is refreshed and verified.
- Use `INSTALL_ARGS=--no-prune-backups` when a maintenance run must preserve
  every historical backup; default installs retain the newest ten per skill.

Run the mutable remote check only for release readiness or upstream review:

```bash
make release-readiness
```

Check whether the canonical skill copy or separate Codex route-pack has drifted:

```bash
make sync-status
make sync-status-remote
```

For a release that claims certified 100/100, run:

```bash
make release-certify
```

The wrapper acquires a single-writer release lock, runs
`release-certify-prepublish`, rechecks the fixed HEAD and clean worktree, then
runs `release-certify-publish`. The prepublish phase uses
`scripts/design_craft_certification_install_check.sh` to verify install parity
and local maturity in a temporary root; it does not mutate the live install.

This additionally requires all four current-source v2 cross-agent runs,
current-source iOS Simulator, Android Emulator, and physical-device evidence,
a dated release section, clean worktree, maturity 100/100, and exact installed
provenance. After the normal push and `v<VERSION>` tag, run
`make release-tag-verify` to require tag/HEAD/upstream parity plus successful
GitHub `Validate` and `Native runtime evidence` runs for that exact HEAD.
Both certification entrypoints use a repository-local single-writer lock and
verify that HEAD and the clean-worktree invariant remain unchanged throughout
the run. Tag verification accepts only the latest tag-push run for each
required workflow.

## Upstream sync procedure

1. Inspect current state:

   ```bash
   git status --short
   git submodule status --recursive
   ```

2. Check remote drift without mutating submodules:

   ```bash
   python3 scripts/upstream_absorption_report.py --remote-details --fail-on-unreviewed
   ```

3. Sync exactly one upstream only after choosing the reviewed commit:

   ```bash
   bash scripts/sync_upstreams.sh \
     --name <taste-skill|impeccable|emilkowalski-skills> \
     --commit <40-character-sha>
   ```

   The helper updates only the compatibility `commit` field. Set
   `reviewed_commit`, `absorbed_commit`, `reviewed_at`, `decision`, and
   `notes` manually after the absorption review.

4. Generate a local absorption report:

   ```bash
   python3 scripts/upstream_absorption_report.py
   ```

   Treat `candidate_absorb` files as review inputs, not automatic changes.
   `provenance_only` usually means notices/readmes,
   `repository_operations_only` means upstream CI or repository automation,
   and `manual_review` requires human judgment before changing the fusion layer.

5. Review upstream licenses and attribution if upstream content changed:

   ```bash
   git diff -- THIRD_PARTY_NOTICES.md upstreams.lock.json skills/design-craft/references/source-map.md
   ```

6. Update the fusion layer only under `skills/design-craft/`.

7. Run the deterministic release gate, then release readiness:

   ```bash
   make release-gate
   make release-readiness
   ```

## Version policy

- Update `VERSION` for every local release.
- Update `CHANGELOG.md` with user-visible changes.
- Use `0.x` while the workflow is still evolving quickly.
- Use `1.x` only after repeated live UI/UX/design/frontend tasks prove the
  workflow stable as the default Codex route baseline.

## Live task evidence

Record task evidence under `evals/live-task-log.md` with:

- Date.
- Target repo/path.
- Route command.
- Candidate skills and selected skills.
- Style authority path.
- Validation commands.
- Browser validation status.
- Screenshot validation artifact path/hash/dimensions when route output requires
  screenshot evidence, or the skipped reason.
- What the run taught the workflow.

Do not use evidence notes as a substitute for verification. If browser smoke,
type-check, lint, build, or route validation did not run, say that explicitly.

## Golden task evidence

Use `evals/golden-tasks/` for stable task cards that should remain reproducible
across `design-craft` changes. Each card should record:

- Target path and surface.
- Route command and decisive route output.
- Candidate skills versus selected references.
- Style authority path and authority mode.
- Required validation, including browser validation when user-visible UI is in
  scope.
- Required screenshot evidence when `browser_screenshot_required=true`.
- What remains unverified.

Golden tasks should be updated only when the project reality or desired workflow
contract changes.

## Product UI taste calibration

Use `evals/product-ui-taste/` for stable screenshot or page-review calibration
cases. Each case should record:

- Product context and primary user job.
- Evidence level (`L0` through `L4`).
- Expected score or acceptable score range.
- Required findings that a good review should surface.
- False-positive guards, especially claims that cannot be made from the
  available evidence.
- Browser evidence JSON, when captured, should use
  `design-craft.browser-evidence.v1` and pass
  `scripts/design_craft_browser_evidence.py --validate-evidence-json`.
  The validator still accepts the old `frontend-craft.browser-evidence.v1`
  schema for historical artifacts. New captures should emit the canonical
  schema; old TMWD run directory names may remain in evidence records when they
  point to immutable historical artifacts.
- L3 cases must include at least two responsive viewports plus state checks; a
  responsive layout that still preserves weak hierarchy should not inflate the
  score.

Keep binary screenshots out of the repo unless the image itself is required for
reproducibility and attribution is clear.

For live browser cases, keep the screenshot PNGs in the TMWD repo-external run
directory and record only artifact path, SHA-256, dimensions, collection time,
evidence level, and a redacted visual/DOM summary in the eval case.

## L4 before/after evidence

Use `evals/product-ui-taste/before-after/` only for real implementation
improvement evidence. The `_template/` directory is scaffolding and must not be
counted as a completed L4 case.

A completed L4 case must include:

- Before and after screenshot artifact path, SHA-256 hash, and dimensions.
- Before and after scores with `evidence_level: "L4"`.
- Diff summary naming actual changed files or implementation boundaries.
- Validation commands and observed results.
- Explicit unverified states.

Active project-neutral completed cases:

- `generic-review-workbench-local-l4`
- `ops-dashboard-decision-surface-l4`

Validate them with `scripts/design_craft_l4_case_validate.py --strict` before
citing either as completed before/after evidence. Use `--require-existing-files`
only on the machine that still has the repo-external PNG artifacts.

## Cross-agent benchmarks

Use `evals/cross-agent/` to compare how Codex, Cursor, Claude, Pi, or another
Agent Skills-compatible client applies the same `design-craft` prompt.

Do not claim cross-agent stability until real outputs are recorded. Template
cases define prompts and scorecards only. Legacy v1 dashboard, gesture-motion,
and native-adaptive cases have observed Codex/Pi artifacts; Cursor and Claude
remain explicitly unverified. Certified 0.5.0 evidence must use v2 records that
bind the current skill tree, prompt, scorecard, and exact output, with the score
recomputed from criterion-earned points.

## Codex route-pack portability

The local frontend route planner, platform detector, route config, frontend
rule, preflight contract, and route tests live under `~/.codex`. They are
runtime policy, not skill contents. Use the route-pack helper to make that
policy auditable. The file-list authority is
`~/.codex/tools/frontend_route_pack_manifest.json`; the helper and global
snapshot must derive their scopes from that manifest rather than maintaining
parallel lists:

```bash
python3 scripts/design_craft_codex_route_pack.py --strict --json
```

For migration or backup, export only the whitelisted bundle:

```bash
python3 scripts/design_craft_codex_route_pack.py \
  --strict \
  --export-dir /tmp/design-craft-codex-route-pack
```

After restoring to another Codex home, run the validation commands listed in
`adapters/codex/route-pack/README.md`. Do not treat the manifest alone as proof
that the restored route planner works. A strict audit must also pass routing
JSON Schema validation, split authority/browser/delivery/runtime/telemetry
module checks, a telemetry self-check, browser/runtime tool-parity probes, a
verified `gpt-5.6-sol/max` environment-runtime probe, and the unapproved GPT-5.6
`ultra` runtime-conflict denial probe. Strict probes set
`FRONTEND_ROUTE_TELEMETRY_LOG_ENABLED=0` and
`FRONTEND_RUNTIME_SESSION_DISCOVERY=0`; audit runs must not write production
telemetry or read the caller's session JSONL.

The live planner may verify the current runtime from the latest session
`turn_context`, but only `model`, `effort`, `turn_id`, and `current_date` are
read. Prompt/message/tool payloads remain outside the contract, and evidence
paths are relative to `CODEX_HOME`. `config.toml` values are candidates, not
proof of the active turn.

Review production route latency and distributions separately:

```bash
python3 ~/.codex/tools/frontend_route_telemetry.py \
  --include-rotated \
  --context prod \
  --min-events 6 \
  --max-p95-ms 1000 \
  --json
```

The default privacy-safe log rotates at 2 MB with seven retained files. Use a
non-production context for fixtures and keep general route tests plus release
route smoke telemetry-off; `test_frontend_route_telemetry.sh` owns telemetry
behavior coverage.

## Release checklist

Before committing a release:

1. `git status --short`
2. `make validate-portable`
3. `make release-gate-local`
4. `make release-readiness`
5. Confirm source completeness 100/100 and portable/local maturity 95/100.
6. Route smoke on the fixture (`make route-smoke`) or on at least one real
   project path with its own `DESIGN.md` when route behavior changed.
7. Upstream absorption report reviewed when upstream commits or detector rules changed.
8. Product UI taste calibration and completed L4 case validation still pass
   when taste scoring changed.
9. Install parity/provenance check:
   `make install-verify`
   This checks the installed skill tree and skill-scoped dirty state. Separate
   `repo_dirty` provenance remains visible for audit, while the release
   certification gate independently requires the whole worktree to be clean.
   The recorded source commit must also contain the exact installed skill tree;
   ancestor status alone is not sufficient provenance.
10. Legacy alias source check:
   `grep -Fq 'renamed to \`design-craft\`' skills/frontend-craft/SKILL.md`
11. Optional legacy install dry-run:
   `bash scripts/install_local.sh --dry-run --include-legacy-alias`
12. Confirm no repo docs were added inside `skills/design-craft/` except the
    machine-readable `VERSION` and `COMPATIBILITY.json` contracts.
13. Record each maturity JSON status independently. Current evidence should say
    `ios_simulator: observed_current_source`,
    `android_emulator: observed_current_source`, and `real_device: missing`
    until a current-source physical-device artifact is admitted.
14. For a release claiming native runtime evidence, dispatch
    `.github/workflows/native-runtime.yml`, download both artifacts, verify their
    hashes and assertions, and then validate the admitted JSON with
    `make native-runtime-check`.
    Runtime identifiers must be hashed, and the decisive Android before/after
    accessibility trees must be present in the JSON artifact-role set. Capture
    a physical Android device with `scripts/native_runtime_device_android.sh`;
    do not hand-author `real-device-observed.json`.
15. For a release claiming certified 100/100, run `make release-certify`; do
    not substitute the normal 95/100 release-readiness gate.
16. Commit with a scoped message.
17. After push/tag, run `make release-tag-verify`.
