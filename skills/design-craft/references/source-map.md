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

Mutable remote review state is repository governance metadata recorded in
`upstreams.lock.json` and the matching absorption matrices under `docs/`. The
installed Skill records only pinned compatibility and selected-behavior
boundaries, so provenance-only upstream changes do not invalidate behavioral
evidence for an otherwise unchanged Skill tree.

### Leonxlnx/taste-skill

- URL: `https://github.com/Leonxlnx/taste-skill`
- License: MIT
- Canonical provenance path: `upstreams/taste-skill`
- Pinned compatibility commit:
  `b17742737e796305d829b3ad39eda3add0d79060`
- Selected-behavior boundary:
  `06d6028b5c623016c59ce8536f578e5a1127b499`
- Cumulative status: `selective_absorbed`; behavior through the initial
  `06d6028b5c623016c59ce8536f578e5a1127b499` snapshot is represented in the
  local visual-judgment, product-taste, design-move, and design-system layers.
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
- Canonical provenance path: `upstreams/impeccable`
- Pinned compatibility commit:
  `630fc2682a5bd39b25a8e61f74b6b3f14f2b1e21`
- Selected-behavior boundary:
  `8634c538fbf860fcdd2a54c31676beb78a44eff4`
- Cumulative status: `selective_absorbed` for the command taxonomy,
  brief/change-scope authority, surface modes, craft floor, applicable scoring,
  detector/native guidance, hardening, measurement, evidence contracts, and
  at-most-two batched rendered-verification passes.
- Contract: `docs/impeccable-absorption.md`, validated by
  `scripts/design_craft_impeccable_absorption.py` in the canonical repository.
- Stable boundary: random concept selection, forced delegation, upstream
  live/provider/hooks runtime, full detector/vendor bundles, generated provider
  copies, promotional tone, and universal ecosystem prescriptions remain
  outside the baseline.
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
- Canonical provenance path: `upstreams/emilkowalski-skills`
- Pinned compatibility commit:
  `7bb7061b5cf7de15ea1aeaf00fbd9e6592a20fce`
- Selected-behavior boundary:
  `d62b0d8f9a8eb795a512b76239bb873ab9ac7cd5`
- Cumulative status: `selective_absorbed`; the motion-opportunity gate is local,
  while the opinionated library picker and Base UI-only prescription are
  intentionally rejected.
- Stable selected behavior: original design-craft references cover
  product-design principles, Apple-style direct manipulation,
  presentation-value interruption, spring response/damping, velocity handoff,
  momentum projection, rubber-banding, accessibility variants, and optical
  typography.
- Stable boundary: absolute heuristics remain calibrated by project authority
  and runtime evidence; opinionated library substitution and README-only
  provenance do not enter the installed behavior layer.
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
   whether a remote head changed without mutating submodules. The pinned
   compatibility commit may intentionally lag repository review metadata.
2. Run `scripts/sync_upstreams.sh --name <name> --commit <40-char-sha>` only
   after selecting an explicit commit; the helper never advances review or
   absorption metadata automatically.
3. Run `scripts/upstream_absorption_report.py --remote --fail-on-unreviewed`
   to block unreviewed remote drift, then run the local report to classify files as
   `candidate_absorb`, `provenance_only`, or `manual_review` without fetching or
   editing submodules.
4. Inspect upstream changelogs and key skill/command files.
5. Update this source map only when the pinned compatibility commit or selected
   behavior boundary changes. Provenance-only reviews must not change the
   installed Skill tree.
6. Record every mutable review range and decision in `upstreams.lock.json` and
   the matching absorption matrix, then update the strict validator when local
   behavior coverage changes.
7. Never overwrite `skills/design-craft` automatically from upstream.

## Attribution rule

If substantial text, code, scripts, or detector rules are copied into this
project, keep attribution in `THIRD_PARTY_NOTICES.md` and preserve applicable
license headers where required. Prefer original fusion rules that cite the
upstream idea rather than blind copy-paste.
