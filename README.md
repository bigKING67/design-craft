# design-craft

Portable product design engineering, UI/UX, visual taste, motion, and
implementation-quality workflow across web, iOS, Android, and adaptive products.

`design-craft` is the canonical local fusion layer for high-quality product
experience work on this machine. It supersedes the former `frontend-craft`
name because the workflow now covers more than frontend code: product context,
UI/UX judgment, design-system contracts, motion craft, product taste, native
platform fit, implementation quality, runtime evidence, and long-term project
structure. It keeps scoped project rules, optional `PRODUCT.md`, project
`DESIGN.md`, and live runtime evidence above generic guidance, then folds in:

- anti-slop visual judgment, brief inference, and aesthetic pressure absorbed
  into `design-craft`.
- Impeccable-style audit, polish, harden, optimize, detector, and live-iteration
  loops.
- Design-system contract checks for `DESIGN.md`, token roles, light/dark parity,
  component states, focus, motion, and UI copy.
- Emil Kowalski-style motion purpose, frequency, timing/easing, physicality,
  interruptibility, gesture, performance, reduced-motion, and animation
  vocabulary checks.
- iOS HIG/native-trust, Android Material 3/predictive Back/inset, and adaptive
  shared-versus-platform-specific implementation checks.
- Bundled Vercel Geist `design.md` / `design.dark.md` seed templates for new or
  weakly specified developer-product surfaces.
- Project quality gates for architecture, performance, code elegance, validation,
  and file/directory structure governance.

The skill is intentionally personal and local-first. For dashboards, special
reports, and similar business surfaces, scoped project rules, live
runtime behavior, and project `DESIGN.md` always outrank generic visual rules.
The canonical package is still portable: agent-specific integration belongs in
`adapters/`, while `skills/design-craft/` remains the single source skill.
The `0.5.0` development contract keeps ordinary portable/local operation at
95/100 while reserving certified 100/100 for current-source v2 evidence from
Codex, Pi, Cursor, and Claude plus observed iOS Simulator, Android Emulator,
and real-device evidence. Evidence hashes bind the skill tree, fixtures,
prompt, scorecard, and agent output instead of treating file presence as proof.

## Layout

```text
design-craft/
├── skills/design-craft/        # Installable Codex skill
├── adapters/                     # Thin Codex/Cursor/Claude/Pi/generic install adapters
├── scripts/                      # Deterministic route/pass/detect/score/review tools
├── .github/workflows/            # Portable validation and scheduled upstream audit
├── evals/                        # Forward-test and live-task evidence
│   ├── golden-tasks/             # Reproducible real-task evidence cards
│   └── product-ui-taste/         # Taste-score calibration cases
├── upstreams/                    # Pristine upstream submodules; do not edit
├── docs/                         # Repo maintenance and release process
├── THIRD_PARTY_NOTICES.md        # Attribution and licenses
├── upstreams.lock.json           # Pinned upstream commit provenance
└── VERSION                       # Local release version
```

`skills/design-craft/` should stay lean. Repo-level documents such as this
README, the changelog, and maintenance notes belong at the repository root or in
`docs/`, not inside the installed skill folder.

This repository is not a UI target. It intentionally provides neither a root
`PRODUCT.md` nor `DESIGN.md`; target projects may add `PRODUCT.md` for
product/platform context and must provide `DESIGN.md` or an explicit
`--style-authority-path` for L1+ visual route/preflight checks.

## Install locally

Repository automation is verified on macOS and Linux. Native Windows shells are
not currently certified; Windows users should use WSL or a compatible Git Bash
environment and treat that path as unverified until a Windows CI lane exists.

```bash
bash scripts/install_local.sh
```

The installer stages and validates the complete skill, takes an install lock,
atomically replaces the active copy, restores the previous target on failure,
records `.design-craft-install.json` version/commit/tree-digest provenance plus
separate `skill_source_dirty` and `repo_dirty` states, and retains the newest
ten backups by default. Install parity is scoped to the installed skill tree,
so unrelated benchmark WIP or later ancestor commits do not invalidate an
unchanged installation. The verifier also reconstructs the skill tree at the
recorded source commit, preventing metadata from naming an ancestor that never
contained the installed content. Certified releases still require a clean
whole repo.
It syncs:

```text
skills/design-craft -> ${DESIGN_CRAFT_SKILL_ROOT:-$HOME/.agents/skills}/design-craft
```

Verify source parity and install provenance:

```bash
python3 scripts/design_craft_install_verify.py \
  --source skills/design-craft \
  --installed "${DESIGN_CRAFT_SKILL_ROOT:-$HOME/.agents/skills}/design-craft" \
  --expected-name design-craft \
  --expected-version "$(cat VERSION)" \
  --require-metadata
```

Check the source/install copy and the separate Codex route-pack authority
without changing either one:

```bash
make sync-status
make sync-status-remote # also checks mutable upstream heads
```

`skills/frontend-craft` is a legacy compatibility alias only. New route and
preflight defaults should use `design-craft`. A fresh install does not create
the alias, but an already-installed alias is refreshed so it cannot silently
drift. Create it explicitly only for old clients that still use the former
name:

```bash
bash scripts/install_local.sh --include-legacy-alias
```

Override retention with `--keep-backups <count>` or
`DESIGN_CRAFT_BACKUP_KEEP`; use `--no-prune-backups` for an explicitly
non-destructive maintenance run. `make release-gate` forwards optional
installer flags through `INSTALL_ARGS`.

## Install as a Pi package

For Pi, prefer package installation over copying into `~/.pi/agent/skills`:

```bash
pi install git:github.com/bigKING67/design-craft@<tag-or-commit>
```

For local development, use the checkout path:

```bash
export DESIGN_CRAFT_HOME=/path/to/design-craft
pi install "$DESIGN_CRAFT_HOME"
```

The `package.json` `pi.skills` manifest exposes only the canonical
`skills/design-craft` skill. This keeps `pi-67` as the Pi configuration repo
while `design-craft` remains the single source skill.

The npm package boundary is also explicit: `package.json.files` includes only
the canonical skill, root version/readme metadata, and required license/notice
files. It excludes upstream checkouts, evals, workflows, and repository-only
maintenance scripts. Verify the packed payload and size budget with:

```bash
make package-check
```

The gate caps the package at 1 MB compressed, 2 MB unpacked, and 100 files,
rejects repository-only paths, and scans packed text for user-home paths.
The broader public-repository gate also rejects workstation-specific macOS,
Linux, and Windows user-home paths anywhere outside pristine upstream
submodules:

```bash
make public-repo-check
```

GitHub Actions and npm metadata updates are tracked separately through
`.github/dependabot.yml`; action executions remain pinned to reviewed full
commit SHAs.

Validate workflow pins, native fixture manifests, real iOS deep-link routing,
Android dialog recovery, and compile-smoke coverage independently with:

```bash
make workflow-check
```

## Agent adapters

Install the same canonical skill into a host-specific location:

```bash
bash scripts/design_craft_init_agent.sh --agent codex --target /path/to/project --scope project --dry-run
bash scripts/design_craft_init_agent.sh --agent cursor --target /path/to/project --scope project --with-rule --dry-run
bash scripts/design_craft_init_agent.sh --agent claude --target /path/to/project --scope project --dry-run
bash scripts/design_craft_init_agent.sh --agent pi --target /path/to/project --scope project --dry-run
bash scripts/design_craft_init_agent.sh --agent generic --target /path/to/project --scope project --dry-run
```

Adapter notes live under:

```text
adapters/codex/
adapters/cursor/
adapters/claude/
adapters/pi/
adapters/generic/
```

Run a portability check without modifying files:

```bash
bash scripts/design_craft_doctor.sh --target . --json
```

Audit or export the local Codex frontend route tools as a whitelisted migration
bundle. This does not copy arbitrary `~/.codex` state; it records only the
route planner, inherited frontend worker, frontend rules, preflight contract,
and related tests selected by the single
`~/.codex/tools/frontend_route_pack_manifest.json` authority. The strict audit
also validates manifest/snapshot coverage, the routing JSON Schema, split
worker Python cores, browser/runtime tool parity, V2 delegation semantics,
dedicated authority/browser/delivery/runtime/telemetry modules, and redacted
runtime model/reasoning profiles against the bundled Codex model catalog. Current
Codex session evidence reads only the latest `turn_context.model/effort`, while
strict audits disable session discovery and route telemetry writes. Privacy-safe
route history exposes p50/p95/max latency and bounded routing distributions.
GPT-5.6 `ultra` is actively probed as a denied unapproved runtime conflict
because it includes automatic task delegation; explicit main-owned frontend
overrides stop at `max`:

```bash
python3 scripts/design_craft_codex_route_pack.py --strict
python3 scripts/design_craft_codex_route_pack.py \
  --strict \
  --export-dir /tmp/design-craft-codex-route-pack
```

Route-pack details live under `adapters/codex/route-pack/`.

## Default design seed

For new or weakly specified developer-product, SaaS, dashboard, admin, infra,
docs, and tooling surfaces, start from the bundled Vercel Geist templates:

```text
skills/design-craft/templates/vercel-geist/design.md
skills/design-craft/templates/vercel-geist/design.dark.md
```

When a project already has a credible `DESIGN.md`, token system, brand guide, or
strong runtime visual language, use these files as the comparison baseline
rather than replacing project authority blindly.

Seed a project directly with:

```bash
bash scripts/design_craft_seed_design.sh --target /path/to/project
```

The helper refuses to overwrite an existing `DESIGN.md` or `DESIGN.dark.md`
unless `--force` is explicit.

## Product and platform authority

`PRODUCT.md` is optional and owns product facts:

- register, platform, users, purpose, positioning, and accessibility

`DESIGN.md` remains the only visual authority:

- typography, color, spacing, components, themes, iconography, and motion

Platform resolution is deterministic:

```text
explicit --platform
> nearest PRODUCT.md ## Platform
> codebase detection
> default web
```

`surface=mobile` is not a native signal. Capacitor, Cordova, and HTML WebView
shells remain `web`; React Native/Expo, Flutter, KMP, and repositories with
real iOS plus Android targets resolve to `adaptive`. Missing `PRODUCT.md`
does not block existing projects; the route reports inferred source,
confidence, signals, and contradictions.

## Validate

Portable gate for a fresh clone or another machine:

```bash
make validate-portable
```

Deterministic source gate, followed by an atomic local publish:

```bash
make release-gate-local
```

Equivalent direct commands:

```bash
bash scripts/validate.sh --portable
python3 scripts/design_craft_active_scope_validate.py --root .
python3 scripts/design_craft_score.py --self
python3 scripts/design_craft_maturity.py --profile portable --min-score 95
python3 scripts/design_craft_maturity.py --profile local --min-score 95
python3 scripts/design_craft_maturity.py --profile desktop --min-score 100
bash scripts/design_craft_pass.sh --target . --mode audit --skip-route
```

`make release-gate` remains a compatibility alias for the local full gate.
Remote upstream freshness is intentionally separate because a moving remote
`HEAD` must not make an unchanged commit's deterministic gate change over time.
Before a new release, run `make release-readiness`; it runs the local gate and
then the actionable remote audit. The source scorer must report 100/100. The
maturity scorer reports 95/100 until schema-valid observed native runtime
evidence removes the explicit cap. Portable CI exercises Ubuntu and macOS with
Node 22/24 and Python 3.11/3.12/3.13 rather than treating one Python runtime as
cross-version proof.

For normal computer-based web/frontend development, use the `desktop` profile.
It verifies the installed skill, local route pack, design authority, browser and
screenshot contracts, CI portability, and Codex/Pi evidence, but does not treat
optional Cursor/Claude portability or physical-device certification as a daily
development blocker. This profile can report 100/100 while `local` and
`release-certify` continue to preserve the stricter cross-host/native release
boundary.

## Common commands

Route a frontend task through the local Codex route planner:

```bash
bash scripts/design_craft_route.sh \
  --target /path/to/project \
  --surface mobile \
  --intent visual-refine \
  --scope page \
  --platform auto \
  --product-context-path /path/to/project/PRODUCT.md
```

Detect platform or run conservative native/adaptive static checks:

```bash
python3 scripts/design_craft_platform_scan.py \
  --target /path/to/project \
  --platform auto \
  --mode scan \
  --json
```

Static platform findings are review evidence only. They do not prove an iOS
Simulator, Android Emulator, or real-device run.

Run a critique/audit/polish/harden/optimize/structure/architecture pass:

```bash
bash scripts/design_craft_pass.sh \
  --target /path/to/project \
  --mode critique
```

`design_craft_audit.sh` remains as a compatibility entrypoint.

Run a motion-specific review pass:

```bash
bash scripts/design_craft_pass.sh \
  --target /path/to/project \
  --mode motion
```

Create a stable product UI taste-review packet before scoring a screenshot or
page:

```bash
bash scripts/design_craft_taste_review.sh \
  --target /path/to/screenshot-or-project \
  --context "dashboard for internal operators" \
  --evidence-level L0
```

Product UI taste calibration cases live under `evals/product-ui-taste/`. Static
cases use L0/L1 evidence; live browser cases should record TMWD screenshot
artifact paths, SHA-256 hashes, dimensions, DOM/computed-style summaries, and
the states that were not verified. L3 cases must include responsive viewport
evidence and explicit interaction-state checks; responsive fit alone is not
proof of better task hierarchy.

Create a real L4 before/after eval scaffold:

```bash
bash scripts/design_craft_l4_eval_case.sh \
  --case-id generic-review-workbench-local-l4 \
  --surface "http://127.0.0.1:4173/generic-review-workbench/" \
  --primary-user "review operations teammates"
```

The generated case is not evidence by itself. Fill real screenshot metadata,
before/after scores, implementation diff, validation commands, and unverified
states before counting it as L4.

Completed project-neutral fixture examples remain the portable public examples.
The repo may also retain historical real-project L4 provenance; those cases are
validated by the local full gate and must keep their project-specific claims
bounded to the recorded artifacts.

Create a project-neutral L4 screenshot capture plan. Prefer the TMWD evidence
bundle helper when the active agent exposes it; this wrapper gives a repeatable
Chrome-headless fallback and writes only repo-external PNG artifacts plus
`screenshots.json` metadata:

```bash
python3 scripts/design_craft_l4_capture.py \
  --case-id generic-review-workbench-local-l4 \
  --before-url 'http://127.0.0.1:4173/generic-review-workbench/?variant=before' \
  --after-url 'http://127.0.0.1:4173/generic-review-workbench/?variant=after' \
  --viewport desktop=1440x900 \
  --viewport compact500=500x844 \
  --dry-run
```

Remove `--dry-run` and pass `--manifest <case>/screenshots.json` only when the
URLs are safe to capture and PNG artifacts should be written outside the repo.

Emit a redacted DOM/computed-style sampler for TMWD `browser_execute_js`, or
validate captured product UI evidence and score anti-inflation rules:

```bash
python3 scripts/design_craft_browser_evidence.py --print-js
python3 scripts/design_craft_browser_evidence.py \
  --validate-score-json evals/product-ui-taste/before-after/generic-review-workbench-local-l4/score.after.json
python3 scripts/design_craft_browser_evidence.py \
  --validate-score-json evals/product-ui-taste/before-after/generic-review-workbench-local-l4/score.before.json
python3 scripts/design_craft_l4_evidence_manifest.py \
  --validate-screenshots-json evals/product-ui-taste/before-after/generic-review-workbench-local-l4/screenshots.json \
  --strict
```

Validate a completed L4 before/after case directory before citing its metadata:

```bash
python3 scripts/design_craft_l4_case_validate.py \
  --case-dir evals/product-ui-taste/before-after/<case> \
  --strict
```

To claim that the referenced PNG artifacts are available on the current
machine, add `--require-existing-files`. The certified release path does this
through `make real-l4-check`; the normal portable/local 95-point gate uses
`make historical-l4-metadata-check` and does not imply artifact availability.

Current project-neutral completed L4 cases are:

- `generic-review-workbench-local-l4`: a local review-workbench fixture with
  before/after viewport screenshots and responsive metadata.
- `ops-dashboard-decision-surface-l4`: a local operations dashboard fixture
  that demonstrates the `Dashboard card soup -> decision surface` design move.
- `evals/fixtures/l4-pages/gesture-sheet-interaction/`: deterministic
  direct-manipulation fixture with observed browser trace assertions and a
  repo-external viewport PNG recorded in `validation.json`.

Historical real-project L4 provenance is retained for local verification:

- One historical real application workbench before/after case records
  desktop/mobile screenshot metadata, validation commands, and bounded
  unverified states. `make historical-l4-metadata-check` validates the durable
  metadata, while `make real-l4-check` additionally requires every referenced
  artifact to exist locally. Public portable examples remain project-neutral.

Run the cross-agent dashboard benchmark validators:

```bash
python3 scripts/design_craft_cross_agent_validate.py --root evals/cross-agent
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-dashboard-review
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-motion-review
python3 scripts/design_craft_cross_agent_validate.py \
  --observed-task evals/cross-agent/same-prompt-native-adaptive-review
```

Legacy v1 Codex/Pi dashboard, gesture-motion, and native-adaptive outputs remain
valid as the 95/100 baseline. Certified `0.5.0` evidence must be regenerated as
v2 against the current skill tree for all four hosts; Cursor and Claude remain
explicitly unverified until those real runs exist.

Record a v2 score only after preserving the exact host output and filling a
criteria JSON copied from `evals/cross-agent/_template/criteria.json`:

```bash
python3 scripts/design_craft_cross_agent_record.py \
  --task-dir evals/cross-agent/same-prompt-motion-review \
  --agent codex \
  --agent-version "codex-cli <version>" \
  --model "<observed-model>" \
  --reasoning-profile "<observed-profile>" \
  --skill-root skills/design-craft \
  --command-summary "<redacted runner summary>" \
  --criteria-json /path/to/criteria.json
```

The recorder computes the headline score from criterion-earned points and binds
the output, prompt, scorecard, version, source commit, and skill tree hashes.
For a host-specific copy such as `~/.claude/skills/design-craft` or a project
`.cursor/skills/design-craft`, pass that exact directory as `--skill-root` and
use `--provenance-skill-root ~/.agents/skills/design-craft` for clean install
metadata. Recording fails unless both trees are byte-for-byte equivalent.

Run static UI smell scanners. These are review signals, not a replacement for
design judgment or browser evidence:

```bash
python3 scripts/design_craft_static_review.py --target /path/to/project --json
python3 scripts/design_craft_css_smell_scan.py --target /path/to/project
python3 scripts/design_craft_focus_audit.py --target /path/to/project
python3 scripts/design_craft_token_audit.py --target /path/to/project
```

`design_craft_static_review.py` normalizes the three scanner outputs into one
handoff-friendly JSON packet with severity counts, top findings, and design
interpretation prompts.

Run the detector. Default text output includes pinned Impeccable findings plus
local design-craft review signals; `--json-only` remains raw upstream JSON for
compatibility, and `--full-json` emits the combined payload.

```bash
bash scripts/design_craft_detect.sh --target /path/to/project
```

Review pinned upstream drift and absorption candidates without fetching:

```bash
make upstream-report
```

Check remote drift with commit titles, changed paths, and an absorption
recommendation without changing submodule checkouts:

```bash
python3 scripts/upstream_absorption_report.py --remote-details
```

Score source completeness and operational maturity separately:

```bash
python3 scripts/design_craft_score.py --self --json
python3 scripts/design_craft_maturity.py --profile portable --min-score 95 --json
python3 scripts/design_craft_maturity.py --profile local --min-score 95 --json
python3 scripts/design_craft_maturity.py --profile desktop --min-score 100 --json
```

## Upstream policy

The upstream repositories are kept as pinned submodules:

- `upstreams/taste-skill`
- `upstreams/impeccable`
- `upstreams/emilkowalski-skills`

Do not edit upstream files directly. Update the fusion layer under
`skills/design-craft/`, update attribution when needed, and record upstream
commit changes in `upstreams.lock.json`.

Runtime routing should use `design-craft` as the baseline. The upstream
`taste-skill`, `impeccable`, and `emilkowalski-skills` checkouts are retained
only for provenance and deliberate manual absorption, not as automatic updaters
or legacy route sources.

Refresh upstreams with:

```bash
bash scripts/sync_upstreams.sh \
  --name emilkowalski-skills \
  --commit <reviewed-40-character-sha>
```

The sync helper advances one explicit submodule and only the compatibility
`commit` field. It never advances `reviewed_commit`, `absorbed_commit`, or
the decision metadata. Before absorbing upstream changes, run:

```bash
python3 scripts/upstream_absorption_report.py --remote-details --fail-on-unreviewed
```

## Licensing

Original design-craft code and documentation are distributed under the MIT
License in `LICENSE`. Required upstream license and notice text is preserved in
`LICENSES/` and summarized in `THIRD_PARTY_NOTICES.md`. The Vercel design
snapshots remain attributable to Vercel and are not relicensed by the
design-craft MIT license; see `LICENSES/VERCEL-DESIGN-NOTICE.md` before
redistributing those files outside this package.

## Local release gate

Before treating the current source and local install as stable, run:

```bash
make validate-portable
make release-gate-local
```

`make release-gate` remains a compatibility alias for `make release-gate-local`.
Before tagging a new release, additionally run:

```bash
make release-readiness
```

`release-readiness` is the normal 95/100 release boundary. A release claiming
certified 100/100 must instead pass the stricter non-bypassable contract:

```bash
make release-certify
```

It requires all four current-source v2 host runs, current-source Simulator,
Emulator, and physical-device evidence, a dated release section, a clean
worktree, local maturity 100/100, and install provenance parity. After pushing
and tagging, verify tag/HEAD/upstream parity plus successful `Validate` and
`Native runtime evidence` workflow runs with `make release-tag-verify`.

Certification is intentionally two-phase. `release-certify-prepublish` runs
all source, remote, L4, four-host, native, and 100-point gates and verifies the
installer in an isolated temporary skill root. Only after those checks pass
does `release-certify-publish` atomically update the live
`~/.agents/skills/design-craft` installation. A failed prepublish phase cannot
leave the active installation on an uncertified tree.
The certification entrypoints acquire a repository-local single-writer lock
and reject a changed HEAD or dirty worktree at the end of the run. Tag
verification requires the latest `push` run whose `headBranch` is the release
tag; an older manual success for the same commit cannot satisfy the contract.

The gate split is documented in `docs/maintenance.md`. The portable gate checks
package shape, syntax, bundled runtime independence, platform fixtures,
validators, static scanners, project-neutral L4 fixtures, source completeness,
and portable maturity without local Codex or install-state assumptions. The
local gate adds skill quick validation, Codex route-pack checks, observed
cross-agent evidence, historical real-project L4 provenance, atomic install,
installed-skill provenance/parity, and local maturity. `release-readiness`
adds mutable remote-upstream freshness only after the deterministic gate passes.

Probe native SDK/runtime availability and validate real evidence separately:

```bash
python3 scripts/design_craft_native_runtime_validate.py --probe --json
python3 scripts/design_craft_native_runtime_validate.py --validate --require ios --require android --require-real-device --require-current-source --json
```

`.github/workflows/native-runtime.yml` runs a real iOS Simulator fixture and a
real Android Emulator fixture on manual dispatch and release tags. It builds,
installs, launches, captures runtime artifacts, exercises the Android control
and a real iOS `simctl openurl` transition against the running app with a cold
deep-link fallback,
hashes the evidence, and validates the generated JSON before upload. Downloaded
artifacts must still be reviewed before `ios-observed.json` and
`android-observed.json` are admitted as durable evidence. A separate physical
device run must provide `real-device-observed.json`; workflow existence is not
itself runtime proof.

Runtime evidence stores only a SHA-256-derived runtime identifier. Raw
Simulator UDIDs, iOS device identifiers, and Android serials must not be
committed. Each runtime kind has required assertion names and artifact roles;
the validator parses decisive accessibility XML, verifies PNG signatures, and
binds every artifact by path, byte count, and SHA-256. Normal `Validate` runs
compile-only iOS and Android fixture jobs so deterministic build failures are
caught before the release-only runtime workflow.

Capture a connected, authorized physical Android device into a repo-external
evidence directory with:

```bash
bash scripts/native_runtime_device_android.sh \
  --serial <adb-serial> \
  --evidence-dir /tmp/design-craft-android-device
```

The raw serial is used only for the live ADB session; the recorded JSON contains
its SHA-256-derived identifier. Review the output before admitting
`real-device-observed.json` and its artifacts under `evals/native-runtime/`.

Route smoke uses a temporary fixture project with its own `DESIGN.md`, because
`design-craft` itself is a reusable skill system rather than a product UI target:

```bash
make route-smoke
```

## Versioning

This repo uses local semantic versioning:

- `0.x`: personal pre-1.0 workflow, allowed to evolve quickly.
- `1.x`: stable default design-craft workflow for this machine.
- Patch releases: validation, documentation, detector, or maintenance fixes.

Current version is stored in `VERSION`; notable changes are tracked in
`CHANGELOG.md`.
