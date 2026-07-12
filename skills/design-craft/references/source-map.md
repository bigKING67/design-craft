# Source map

This project keeps upstream repositories as pristine submodules under
`upstreams/`. The installed skill is a curated fusion layer; do not edit
upstream files directly.

## Contents

- [Upstreams](#upstreams)
- [External design references](#external-design-references)
- [Local calibration artifacts](#local-calibration-artifacts)
- [Maintenance rule](#maintenance-rule)
- [Attribution rule](#attribution-rule)

## Upstreams

### Leonxlnx/taste-skill

- URL: `https://github.com/Leonxlnx/taste-skill`
- License: MIT
- Local path: `upstreams/taste-skill`
- Initial pinned commit:
  `06d6028b5c623016c59ce8536f578e5a1127b499`
- Initial commit note:
  `2026-06-21T00:54:21+02:00 docs(readme): remove sponsor table and tighten logo-to-text spacing`
- Current reviewed commit:
  `b17742737e796305d829b3ad39eda3add0d79060`
- Cumulative status: `selective_absorbed`; behavior through the initial
  `06d6028b5c623016c59ce8536f578e5a1127b499` snapshot is represented in the
  local visual-judgment, product-taste, design-move, and design-system layers.
- Latest-range status: `provenance_only`; the range after `06d6028b` changes
  README sponsorship and image assets only.
- Contract: `docs/taste-skill-absorption.md`, validated by
  `scripts/design_craft_taste_absorption.py` in the canonical repository.
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
  `da99645a58400ed7acb201e6904f9413efd89c6e`
- Current reviewed commit:
  `630fc2682a5bd39b25a8e61f74b6b3f14f2b1e21`
- Cumulative status: `selective_absorbed` through
  `da99645a58400ed7acb201e6904f9413efd89c6e` for the command taxonomy,
  detector/native guidance, hardening, measurement, and evidence contracts.
- Latest-range status: `repository_operations_only` for the sheriff stale-clock
  change from `da99645a` to `630fc268`.
- Contract: `docs/impeccable-absorption.md`, validated by
  `scripts/design_craft_impeccable_absorption.py` in the canonical repository.
- 2026-06-30 absorption note:
  remote updates were reviewed and selectively absorbed for critique method
  provenance, explicit degraded/single-context reporting, `.impeccable`
  ephemeral artifact guidance, harness/subagent capability caveats, and install
  symlink hardening provenance. Dependency bumps and generated provider output
  remain upstream provenance only.
- 2026-07-10 absorption note:
  selectively absorbed platform routing, native audit/adapt guidance, iOS and
  Android quality rules, mechanical pre-scan discipline, and detector/design
  system corrections. Generated provider bundles, site output, dependencies,
  and store packaging remain provenance only.
- 2026-07-11 review note:
  the new range changes only GitHub sheriff automation and its tests. It is
  repository-operations provenance and adds no design-craft behavior.
- Primary material to inspect:
  - `.agents/skills/impeccable/SKILL.md`
  - `site/content/skills/*.md`
  - `site/content/reference/detector.md`
  - `skill/scripts/detect.mjs`
  - `cli/engine/rules/checks.mjs`

Use this upstream for command taxonomy, audit/polish/harden/optimize/live
iteration patterns, deterministic detector checks, design context files, and
production-readiness flows.

### emilkowalski/skills

- URL: `https://github.com/emilkowalski/skills`
- License: MIT
- Local path: `upstreams/emilkowalski-skills`
- Initial pinned commit:
  `a47903a06a05d2e24c483bd8961c85969a51a494`
- Initial commit note:
  `2026-06-29T15:30:16+02:00 Update README.md`
- Current absorbed commit:
  `b57fc72f8415d84db1e9cfb43270466bf12ac6e2`
- Current reviewed commit:
  `7bb7061b5cf7de15ea1aeaf00fbd9e6592a20fce`
- Cumulative status: `absorbed` through
  `b57fc72f8415d84db1e9cfb43270466bf12ac6e2`.
- Latest-range status: `provenance_only` for the newsletter and typo-only
  README changes through `7bb7061`.
- 2026-07-10 decision: `absorbed`; original design-craft references now cover
  product-design principles, Apple-style direct manipulation,
  presentation-value interruption, spring response/damping, velocity handoff,
  momentum projection, rubber-banding, accessibility variants, and optical
  typography.
- 2026-07-11 audit-to-plan absorption note: selectively absorbed the new
  `improve-animations` recon, frequency mapping, eight-dimension audit, finding
  vetting, impact/effort prioritization, self-contained plan, and reconciliation
  workflow into original design-craft guidance and templates. Absolute upstream
  heuristics remain calibrated by project authority and runtime evidence.
- 2026-07-11 provenance note: the following `b024c8b` commit changes only README
  newsletter copy; no additional behavior was imported.
- 2026-07-12 provenance note: `4691d39` and merge commit `7bb7061` correct two
  README typos only; no additional behavior was imported.
- 2026-07-12 five-Skill deep-audit note: all five `SKILL.md` entrypoints plus
  `AUDIT.md`, `PLAN-TEMPLATE.md`, and `STANDARDS.md` are now mapped in
  `docs/emilkowalski-absorption.md` and checked by
  `scripts/design_craft_emil_absorption.py`. This pass added original local web
  motion recipes, component-lifecycle craft, optical typography detail, and
  the previously omitted spring/ambient/principle vocabulary. The upstream
  Skill tree has no non-Markdown implementation files to vendor.
- Primary material to inspect:
  - `skills/emil-design-eng/SKILL.md`
  - `skills/apple-design/SKILL.md`
  - `skills/review-animations/SKILL.md`
  - `skills/review-animations/STANDARDS.md`
  - `skills/improve-animations/SKILL.md`
  - `skills/improve-animations/AUDIT.md`
  - `skills/improve-animations/PLAN-TEMPLATE.md`
  - `skills/animation-vocabulary/SKILL.md`

Use this upstream for motion purpose, frequency-based animation decisions,
easing and duration standards, origin-aware physicality, interruptibility,
gesture craft, animation performance, reduced-motion behavior, strict motion
reviews, codebase-wide audit-to-plan workflows, and animation vocabulary. Do
not absorb standalone tone or unqualified framework/performance claims; keep
the local `design-craft` voice evidence-led, measured, and project-aware.
In the canonical source repository, see `docs/emilkowalski-absorption.md` for
the capability-level status matrix, including deliberate rejections and
contextual partial coverage.

## External design references

### Vercel design references and clean-room replacement

- URLs:
  - `https://vercel.com/design.md`
  - `https://vercel.com/design.dark.md`
- Review note: inspected as public design-system references on 2026-06-24.
- Historical package paths:
  - `templates/vercel-geist/design.md`
  - `templates/vercel-geist/design.dark.md`
- Current original templates:
  - `templates/developer-product/design.md`
  - `templates/developer-product/design.dark.md`
- Workflow absorption:
  - `references/design-system-contract.md`

The Vercel endpoints were reviewed as design-system research. The current
package no longer redistributes their verbatim snapshots. It ships an original
design-craft developer-product pair with structured semantic tokens, matched
light/dark roles, component states, motion limits, focus rules, and UI copy
discipline.

Use `scripts/design_craft_seed_design.sh` to copy the original pair into a
target project as `DESIGN.md` and `DESIGN.dark.md`. The route wrapper reports
`developer_product_seed_applicable` so a new or weak developer-product surface does
not rely on an implicit style-authority guess.

When a project already has a credible `DESIGN.md`, token system, brand guide, or
strong runtime visual language, keep the project authority first and use the
developer-product templates as a comparison baseline for missing system pieces.

## Local calibration artifacts

- `references/product-context.md`: original PRODUCT.md/DESIGN.md authority
  separation and platform-resolution contract.
- `references/product-design-principles.md`: curated product-correctness,
  agency, familiarity, feedback, simplicity, and craft principles.
- `references/interaction-physics.md`: curated direct-manipulation,
  interruption, spring, velocity, projection, hysteresis, and rubber-band
  contract.
- `references/motion-patterns.md`: original web implementation recipes for
  press feedback, anchored overlays, tooltip groups, interruptible state,
  percentage transforms, clip-path, crossfade repair, and transient lifecycle.
- `references/ios-quality.md`, `references/android-quality.md`, and
  `references/adaptive-quality.md`: original platform-specific audit and
  evidence boundaries built from the reviewed upstream principles.
- `scripts/design_craft_platform_scan.py`: conservative platform inference and
  native/adaptive static scan wrapper; static results are not runtime proof.
- `references/product-ui-taste-review.md`: product UI taste rubric, output
  contract, page-type checks, and acceptance criteria.
- `references/taste-score-calibration.md`: evidence levels, score bands, and
  anti-inflation rules for numeric taste scores.
- `references/foundational-visual-principles.md`: original compact visual
  principle layer for attention, proximity, alignment, repetition, contrast,
  figure/ground, similarity, continuity, closure, and economy.
- `references/design-move-library.md`: original action library that translates
  recurring critique patterns into concrete UI moves and acceptance criteria.
- `evals/product-ui-taste/material-ops-home/`: first screenshot-derived
  calibration case for a clean but generic operations dashboard.
- `evals/product-ui-taste/live-browser-samples/`: L2 browser evidence
  calibration set from real TMWD-observed Chrome tabs; screenshot binaries stay
  outside the repo and the eval records artifact path, hash, dimensions, and
  redacted DOM/style summaries.
- `evals/product-ui-taste/before-after/generic-review-workbench-local-l4/`:
  generic L4 before/after calibration case with desktop/compact screenshot
  metadata, strict case validation, and TMWD evidence-bundle dry-run
  verification against repo-external PNG artifacts.
- `scripts/design_craft_taste_review.sh`: deterministic packet generator for
  product UI taste reviews; it does not replace the agent's judgment.
- `scripts/design_craft_browser_evidence.py`: emits the redacted
  `design-craft.browser-evidence.v1` browser sampler and validates product UI
  score anti-inflation rules.
- `scripts/design_craft_css_smell_scan.py`,
  `scripts/design_craft_focus_audit.py`, and
  `scripts/design_craft_token_audit.py`: original static scanners that provide
  review signals for CSS smells, focus-state risks, and token bypasses.
- `adapters/`: original thin host adapters for installing the canonical skill
  into Codex, Cursor, Claude, Pi, or a generic Agent Skills-compatible client.
- `evals/product-ui-taste/before-after/`: L4 before/after evidence scaffold;
  the template is not itself completed evidence.
- `evals/cross-agent/`: cross-agent benchmark scaffold for comparing how host
  agents apply the same design-craft prompt.

## Maintenance rule

When updating upstreams:

1. Run `scripts/upstream_absorption_report.py --remote` when you need to know
   whether a remote head changed without mutating submodules.
2. Run `scripts/sync_upstreams.sh --name <name> --commit <40-char-sha>` only
   after selecting an explicit commit; the helper never advances review or
   absorption metadata automatically.
3. Run `scripts/upstream_absorption_report.py --remote --fail-on-unreviewed`
   to block unreviewed remote drift, then run the local report to classify files as
   `candidate_absorb`, `provenance_only`, or `manual_review` without fetching or
   editing submodules.
4. Inspect upstream changelogs and key skill/command files.
5. Update this source map only after deciding what the fusion layer should
   absorb.
6. Update the matching absorption matrix and strict validator. Keep cumulative
   behavior state separate from the latest reviewed commit range.
7. Never overwrite `skills/design-craft` automatically from upstream.

## Attribution rule

If substantial text, code, scripts, or detector rules are copied into this
project, keep attribution in `THIRD_PARTY_NOTICES.md` and preserve applicable
license headers where required. Prefer original fusion rules that cite the
upstream idea rather than blind copy-paste.
