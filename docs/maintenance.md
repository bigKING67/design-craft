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
bash scripts/frontend_craft_pass.sh --target . --mode audit --skip-route
bash scripts/frontend_craft_audit.sh --target . --mode audit --skip-route
bash scripts/frontend_craft_audit.sh --target . --mode critique --skip-route
bash scripts/frontend_craft_taste_review.sh --target skills/frontend-craft --context "release smoke" --evidence-level L0
bash scripts/frontend_craft_seed_design.sh --target . --dry-run
python3 scripts/upstream_absorption_report.py
python3 scripts/upstream_absorption_report.py --remote
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
- Preferred pass wrapper, audit wrapper, and critique mode smokes pass.
- Product UI taste-review packet smoke passes and keeps score evidence levels
  explicit.
- Product UI browser evidence helper compiles, emits a redacted TMWD DOM/style
  sampler, and validates score anti-inflation plus DOM evidence JSON.
- Vercel Geist seed helper smoke passes and preserves template byte parity.
- Upstream absorption report runs without fetching or modifying submodules; the
  optional `--remote` check reports remote drift with `git ls-remote`.
- Upstream lock commits match checked-out submodule commits.
- Installed skill matches the source skill.

## Upstream sync procedure

1. Inspect current state:

   ```bash
   git status --short
   git submodule status --recursive
   ```

2. Check remote drift without mutating submodules:

   ```bash
   python3 scripts/upstream_absorption_report.py --remote
   ```

3. Sync upstream submodules only after deciding to absorb the remote head:

   ```bash
   bash scripts/sync_upstreams.sh
   ```

4. Generate a local absorption report:

   ```bash
   python3 scripts/upstream_absorption_report.py
   ```

   Treat `candidate_absorb` files as review inputs, not automatic changes.
   `provenance_only` usually means notices or source-map updates; `manual_review`
   requires human judgment before changing the fusion layer.

5. Review upstream licenses and attribution if upstream content changed:

   ```bash
   git diff -- THIRD_PARTY_NOTICES.md upstreams.lock.json skills/frontend-craft/references/source-map.md
   ```

6. Update the fusion layer only under `skills/frontend-craft/`.

7. Run the release gate:

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
- Screenshot validation artifact path/hash/dimensions when route output requires
  screenshot evidence, or the skipped reason.
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
  `frontend-craft.browser-evidence.v1` and pass
  `scripts/frontend_craft_browser_evidence.py --validate-evidence-json`.
- L3 cases must include at least two responsive viewports plus state checks; a
  responsive layout that still preserves weak hierarchy should not inflate the
  score.

Keep binary screenshots out of the repo unless the image itself is required for
reproducibility and attribution is clear.

For live browser cases, keep the screenshot PNGs in the TMWD repo-external run
directory and record only artifact path, SHA-256, dimensions, collection time,
evidence level, and a redacted visual/DOM summary in the eval case.

## Release checklist

Before committing a release:

1. `git status --short`
2. `make release-gate`
3. Route smoke on at least one real project path when route behavior changed.
4. Upstream absorption report reviewed when upstream commits or detector rules changed.
5. Product UI taste calibration still passes when taste scoring changed.
6. Install parity check:
   `diff -qr skills/frontend-craft /Users/gaoqian/.agents/skills/frontend-craft`
7. Confirm no repo docs were added inside `skills/frontend-craft/`.
8. Commit with a scoped message.
