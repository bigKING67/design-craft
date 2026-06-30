# Source map

This project keeps upstream repositories as pristine submodules under
`upstreams/`. The installed skill is a curated fusion layer; do not edit
upstream files directly.

## Upstreams

### Leonxlnx/taste-skill

- URL: `https://github.com/Leonxlnx/taste-skill`
- License: MIT
- Local path: `upstreams/taste-skill`
- Initial pinned commit:
  `06d6028b5c623016c59ce8536f578e5a1127b499`
- Initial commit note:
  `2026-06-21T00:54:21+02:00 docs(readme): remove sponsor table and tighten logo-to-text spacing`
- Primary material to inspect:
  - `skills/taste-skill/SKILL.md`
  - `skills/redesign-skill/SKILL.md`
  - `skills/minimalist-skill/SKILL.md`
  - `skills/gpt-tasteskill/SKILL.md`
  - `skills/image-to-code-skill/SKILL.md`
  - `skills/stitch-skill/SKILL.md`

Use this upstream for brief inference, anti-slop judgment, visual hierarchy,
motion discipline, redesign protocol, design-system selection, and final
preflight thinking.

### pbakaus/impeccable

- URL: `https://github.com/pbakaus/impeccable`
- License: Apache-2.0
- Local path: `upstreams/impeccable`
- Initial pinned commit:
  `d2ab4ddee6fa63002fae680652b5fbd31735e280`
- Initial commit note:
  `2026-06-22T16:01:16-07:00 Make Copilot built-in note a callout block under the Install header`
- Current absorbed commit:
  `c979ac37c361da564dcce100a4f2623d94ef54c8`
- 2026-06-30 absorption note:
  remote updates were reviewed and selectively absorbed for critique method
  provenance, explicit degraded/single-context reporting, `.impeccable`
  ephemeral artifact guidance, harness/subagent capability caveats, and install
  symlink hardening provenance. Dependency bumps and generated provider output
  remain upstream provenance only.
- Primary material to inspect:
  - `.agents/skills/impeccable/SKILL.md`
  - `site/content/skills/*.md`
  - `site/content/reference/detector.md`
  - `skill/scripts/detect.mjs`
  - `cli/engine/rules/checks.mjs`

Use this upstream for command taxonomy, audit/polish/harden/optimize/live
iteration patterns, deterministic detector checks, design context files, and
production-readiness flows.

## External design references

### Vercel Geist `design.md`

- URLs:
  - `https://vercel.com/design.md`
  - `https://vercel.com/design.dark.md`
- Review note: inspected as public design-system references on 2026-06-24.
- Vendored templates:
  - `templates/vercel-geist/design.md`
  - `templates/vercel-geist/design.dark.md`
- Workflow absorption:
  - `references/design-system-contract.md`

Use the vendored files as the default initial template for new or weakly
specified developer-product, SaaS, dashboard, admin, infra, docs, and tooling
surfaces. They provide a strong complete baseline: structured tokens plus
human-readable rationale, identical light/dark token names with theme-specific
values, role-based color scales, component state coverage, motion limits, focus
rules, and UI copy discipline.

Use `scripts/frontend_craft_seed_design.sh` to copy the vendored pair into a
target project as `DESIGN.md` and `DESIGN.dark.md`. The route wrapper reports
`vercel_geist_seed_applicable` so a new or weak developer-product surface does
not rely on an implicit style-authority guess.

When a project already has a credible `DESIGN.md`, token system, brand guide, or
strong runtime visual language, keep the project authority first and use the
Geist templates as a comparison baseline for missing system pieces.

## Local calibration artifacts

- `references/product-ui-taste-review.md`: product UI taste rubric, output
  contract, page-type checks, and acceptance criteria.
- `references/taste-score-calibration.md`: evidence levels, score bands, and
  anti-inflation rules for numeric taste scores.
- `evals/product-ui-taste/material-ops-home/`: first screenshot-derived
  calibration case for a clean but generic operations dashboard.
- `evals/product-ui-taste/live-browser-samples/`: L2 browser evidence
  calibration set from real TMWD-observed Chrome tabs; screenshot binaries stay
  outside the repo and the eval records artifact path, hash, dimensions, and
  redacted DOM/style summaries.
- `evals/product-ui-taste/groland-content-assets-l3/`: L3 resilient
  calibration case with desktop/mobile TMWD screenshots, selector/clip
  artifacts, redacted DOM/computed-style JSON, and partial focus-state evidence.
- `scripts/frontend_craft_taste_review.sh`: deterministic packet generator for
  product UI taste reviews; it does not replace the agent's judgment.
- `scripts/frontend_craft_browser_evidence.py`: emits the redacted
  `frontend-craft.browser-evidence.v1` browser sampler and validates product UI
  score anti-inflation rules.

## Maintenance rule

When updating upstreams:

1. Run `scripts/upstream_absorption_report.py --remote` when you need to know
   whether a remote head changed without mutating submodules.
2. Run `scripts/sync_upstreams.sh` only after deciding to absorb the remote head.
3. Run `scripts/upstream_absorption_report.py` to classify changed files as
   `candidate_absorb`, `provenance_only`, or `manual_review` without fetching or
   editing submodules.
4. Inspect upstream changelogs and key skill/command files.
5. Update this source map only after deciding what the fusion layer should
   absorb.
6. Never overwrite `skills/frontend-craft` automatically from upstream.

## Attribution rule

If substantial text, code, scripts, or detector rules are copied into this
project, keep attribution in `THIRD_PARTY_NOTICES.md` and preserve applicable
license headers where required. Prefer original fusion rules that cite the
upstream idea rather than blind copy-paste.
