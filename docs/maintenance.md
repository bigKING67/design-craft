# frontend-craft maintenance

This document is the local release and maintenance checklist for
`frontend-craft`.

## Maintenance rules

- Keep `upstreams/` pristine. Do not edit `upstreams/taste-skill` or
  `upstreams/impeccable` directly.
- Keep the installable skill lean. `README.md`, `CHANGELOG.md`, release notes,
  and maintenance docs belong at the repo root or under `docs/`, not inside
  `skills/frontend-craft/`.
- Keep project-specific truth above generic visual guidance:
  live runtime behavior, scoped `AGENTS.md`, README/framework conventions, and
  project `DESIGN.md` outrank the fusion references.
- Treat `upstreams/taste-skill` and `upstreams/impeccable` as provenance and
  deliberate absorption inputs only. Do not reintroduce automatic upstream
  skill overwrites or legacy taste routing.
- Keep helper scripts deterministic and cheap enough to run before real frontend
  work.
- Record meaningful task evidence under `evals/`; do not claim browser
  validation unless a browser validation actually ran.

## Local release gate

Run this before a version bump, initial commit, or route-policy change:

```bash
make release-gate
```

It expands to:

```bash
bash scripts/validate.sh
python3 scripts/frontend_craft_score.py --self
bash scripts/frontend_craft_audit.sh --target . --mode audit --skip-route
python3 scripts/upstream_absorption_report.py
bash scripts/install_local.sh
diff -qr skills/frontend-craft /Users/gaoqian/.agents/skills/frontend-craft
```

Expected result:

- Skill schema passes `quick_validate.py`.
- Required references, scripts, notices, evals, and version files exist.
- Shell scripts pass `bash -n`.
- Python scorer compiles and runs.
- Detector smoke passes against `skills/frontend-craft` and keeps raw
  `--json-only` compatibility for upstream Impeccable output.
- Audit wrapper smoke passes.
- Upstream absorption report runs without fetching or modifying submodules.
- Upstream lock commits match checked-out submodule commits.
- Installed skill matches the source skill.

## Upstream sync procedure

1. Inspect current state:

   ```bash
   git status --short
   git submodule status --recursive
   ```

2. Sync upstream submodules:

   ```bash
   bash scripts/sync_upstreams.sh
   ```

3. Generate a local absorption report:

   ```bash
   python3 scripts/upstream_absorption_report.py
   ```

   Treat `candidate_absorb` files as review inputs, not automatic changes.
   `provenance_only` usually means notices or source-map updates; `manual_review`
   requires human judgment before changing the fusion layer.

4. Review upstream licenses and attribution if upstream content changed:

   ```bash
   git diff -- THIRD_PARTY_NOTICES.md upstreams.lock.json skills/frontend-craft/references/source-map.md
   ```

5. Update the fusion layer only under `skills/frontend-craft/`.

6. Run the release gate:

   ```bash
   make release-gate
   ```

## Version policy

- Update `VERSION` for every local release.
- Update `CHANGELOG.md` with user-visible changes.
- Use `0.x` while the workflow is still evolving quickly.
- Use `1.x` only after repeated live frontend tasks prove the workflow stable as
  the default Codex frontend route.

## Live task evidence

Record task evidence under `evals/live-task-log.md` with:

- Date.
- Target repo/path.
- Route command.
- Candidate skills and selected skills.
- Style authority path.
- Validation commands.
- Browser validation status.
- What the run taught the workflow.

Do not use evidence notes as a substitute for verification. If browser smoke,
type-check, lint, build, or route validation did not run, say that explicitly.

## Golden task evidence

Use `evals/golden-tasks/` for stable task cards that should remain reproducible
across `frontend-craft` changes. Each card should record:

- Target path and surface.
- Route command and decisive route output.
- Candidate skills versus selected references.
- Style authority path and authority mode.
- Required validation, including browser validation when user-visible UI is in
  scope.
- What remains unverified.

Golden tasks should be updated only when the project reality or desired workflow
contract changes.

## Release checklist

Before committing a release:

1. `git status --short`
2. `make release-gate`
3. Route smoke on at least one real project path when route behavior changed.
4. Upstream absorption report reviewed when upstream commits or detector rules changed.
5. Install parity check:
   `diff -qr skills/frontend-craft /Users/gaoqian/.agents/skills/frontend-craft`
6. Confirm no repo docs were added inside `skills/frontend-craft/`.
7. Commit with a scoped message.
