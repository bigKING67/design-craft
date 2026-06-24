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
- Absorbed into:
  - `references/design-system-contract.md`

Use these references for the idea of an agent-readable design contract:
structured tokens plus human-readable rationale, identical light/dark token
names with theme-specific values, role-based color scales, component state
coverage, motion limits, focus rules, and UI copy discipline.

Do not copy Vercel's token tables, Geist-specific values, or brand aesthetic as
defaults. `frontend-craft` absorbs the contract shape and validation method, not
the visual identity.

## Maintenance rule

When updating upstreams:

1. Run `scripts/sync_upstreams.sh`.
2. Run `scripts/upstream_absorption_report.py` to classify changed files as
   `candidate_absorb`, `provenance_only`, or `manual_review` without fetching or
   editing submodules.
3. Inspect upstream changelogs and key skill/command files.
4. Update this source map only after deciding what the fusion layer should
   absorb.
5. Never overwrite `skills/frontend-craft` automatically from upstream.

## Attribution rule

If substantial text, code, scripts, or detector rules are copied into this
project, keep attribution in `THIRD_PARTY_NOTICES.md` and preserve applicable
license headers where required. Prefer original fusion rules that cite the
upstream idea rather than blind copy-paste.
