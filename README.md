# frontend-craft

Personal frontend craft workflow for Codex.

`frontend-craft` is the local fusion layer for high-quality frontend work on this
machine. It keeps the existing Codex route planner, project `DESIGN.md`, and
browser-validation workflow as the source of truth, then folds in:

- taste-skill style anti-slop judgment, brief inference, and aesthetic pressure.
- Impeccable-style audit, polish, harden, optimize, detector, and live-iteration
  loops.
- Project quality gates for architecture, performance, code elegance, validation,
  and file/directory structure governance.

The skill is intentionally personal and local-first. For DataHub, dashboards,
special reports, and similar business surfaces, scoped project rules, live
runtime behavior, and project `DESIGN.md` always outrank generic taste rules.

## Layout

```text
frontend-craft/
├── skills/frontend-craft/        # Installable Codex skill
├── scripts/                      # Deterministic route/audit/detect/score tools
├── evals/                        # Forward-test and live-task evidence
├── upstreams/                    # Pristine upstream submodules; do not edit
├── docs/                         # Repo maintenance and release process
├── THIRD_PARTY_NOTICES.md        # Attribution and licenses
├── upstreams.lock.json           # Pinned upstream commit provenance
└── VERSION                       # Local release version
```

`skills/frontend-craft/` should stay lean. Repo-level documents such as this
README, the changelog, and maintenance notes belong at the repository root or in
`docs/`, not inside the installed skill folder.

## Install locally

```bash
bash scripts/install_local.sh
```

The installer syncs:

```text
skills/frontend-craft -> /Users/gaoqian/.agents/skills/frontend-craft
```

Verify the installed copy when needed:

```bash
diff -qr skills/frontend-craft /Users/gaoqian/.agents/skills/frontend-craft
```

## Validate

Preferred one-command gate:

```bash
make validate
```

Equivalent direct commands:

```bash
bash scripts/validate.sh
python3 scripts/frontend_craft_score.py --self
bash scripts/frontend_craft_audit.sh --target . --mode audit --skip-route
```

## Common commands

Route a frontend task through the local Codex route planner:

```bash
bash scripts/frontend_craft_route.sh \
  --target /path/to/project \
  --surface dashboard \
  --intent visual-refine \
  --scope page
```

Run an audit/polish/harden/optimize/structure/architecture pass:

```bash
bash scripts/frontend_craft_audit.sh \
  --target /path/to/project \
  --mode audit
```

Run the pinned detector directly:

```bash
bash scripts/frontend_craft_detect.sh --target /path/to/project
```

Score this workflow itself:

```bash
python3 scripts/frontend_craft_score.py --self --json
```

## Upstream policy

The upstream repositories are kept as pinned submodules:

- `upstreams/taste-skill`
- `upstreams/impeccable`

Do not edit upstream files directly. Update the fusion layer under
`skills/frontend-craft/`, update attribution when needed, and record upstream
commit changes in `upstreams.lock.json`.

Refresh upstreams with:

```bash
bash scripts/sync_upstreams.sh
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
- `1.x`: stable default frontend workflow for this machine.
- Patch releases: validation, documentation, detector, or maintenance fixes.

Current version is stored in `VERSION`; notable changes are tracked in
`CHANGELOG.md`.
