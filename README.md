# design-craft

Personal design engineering, product UI, UX, visual taste, motion, and frontend
quality workflow for Codex.

`design-craft` is the canonical local fusion layer for high-quality product
experience work on this machine. It supersedes the former `frontend-craft`
name because the workflow now covers more than frontend code: UI/UX judgment,
design-system contracts, motion craft, product taste, implementation quality,
browser evidence, and long-term project structure. It keeps the existing Codex
route planner, project `DESIGN.md`, and browser-validation workflow as the
source of truth, then folds in:

- anti-slop visual judgment, brief inference, and aesthetic pressure absorbed
  into `design-craft`.
- Impeccable-style audit, polish, harden, optimize, detector, and live-iteration
  loops.
- Design-system contract checks for `DESIGN.md`, token roles, light/dark parity,
  component states, focus, motion, and UI copy.
- Emil Kowalski-style motion purpose, frequency, timing/easing, physicality,
  interruptibility, gesture, performance, reduced-motion, and animation
  vocabulary checks.
- Bundled Vercel Geist `design.md` / `design.dark.md` seed templates for new or
  weakly specified developer-product surfaces.
- Project quality gates for architecture, performance, code elegance, validation,
  and file/directory structure governance.

The skill is intentionally personal and local-first. For DataHub, dashboards,
special reports, and similar business surfaces, scoped project rules, live
runtime behavior, and project `DESIGN.md` always outrank generic visual rules.

## Layout

```text
design-craft/
├── skills/design-craft/        # Installable Codex skill
├── scripts/                      # Deterministic route/pass/detect/score/review tools
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

## Install locally

```bash
bash scripts/install_local.sh
```

The installer syncs:

```text
skills/design-craft -> /Users/gaoqian/.agents/skills/design-craft
skills/frontend-craft -> /Users/gaoqian/.agents/skills/frontend-craft
```

Verify the installed copy when needed:

```bash
diff -qr skills/design-craft /Users/gaoqian/.agents/skills/design-craft
```

`skills/frontend-craft` is a legacy compatibility alias only. New route and
preflight defaults should use `design-craft`.

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

## Validate

Preferred one-command gate:

```bash
make validate
```

Equivalent direct commands:

```bash
bash scripts/validate.sh
python3 scripts/design_craft_score.py --self
bash scripts/design_craft_pass.sh --target . --mode audit --skip-route
```

## Common commands

Route a frontend task through the local Codex route planner:

```bash
bash scripts/design_craft_route.sh \
  --target /path/to/project \
  --surface dashboard \
  --intent visual-refine \
  --scope page
```

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

Emit a redacted DOM/computed-style sampler for TMWD `browser_execute_js`, or
validate captured product UI evidence and score anti-inflation rules:

```bash
python3 scripts/design_craft_browser_evidence.py --print-js
python3 scripts/design_craft_browser_evidence.py \
  --validate-score-json evals/product-ui-taste/groland-content-assets-l3/score.json
python3 scripts/design_craft_browser_evidence.py \
  --validate-evidence-json evals/product-ui-taste/groland-content-assets-l3/dom-evidence.desktop.json
```

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

Check remote drift without mutating submodules:

```bash
python3 scripts/upstream_absorption_report.py --remote
```

Score this workflow itself:

```bash
python3 scripts/design_craft_score.py --self --json
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
bash scripts/sync_upstreams.sh
```

Before absorbing upstream changes, run:

```bash
python3 scripts/upstream_absorption_report.py --remote
```

## Local release gate

Before tagging or treating a version as stable, run:

```bash
make release-gate
```

The release gate is documented in `docs/maintenance.md`. It checks the skill
schema, required references, shell/Python syntax, detector smoke, score smoke,
audit wrapper smoke, upstream lock consistency, and local install parity.

## Versioning

This repo uses local semantic versioning:

- `0.x`: personal pre-1.0 workflow, allowed to evolve quickly.
- `1.x`: stable default design-craft workflow for this machine.
- Patch releases: validation, documentation, detector, or maintenance fixes.

Current version is stored in `VERSION`; notable changes are tracked in
`CHANGELOG.md`.
