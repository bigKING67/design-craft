# Third-party notices

This project is a personal fusion layer built on top of two upstream open-source
frontend design-skill projects. Upstream repositories are kept as pristine
submodules under `upstreams/`.

## Leonxlnx/taste-skill

- Repository: https://github.com/Leonxlnx/taste-skill
- License: MIT
- Local path: `upstreams/taste-skill`
- Initial pinned commit:
  `06d6028b5c623016c59ce8536f578e5a1127b499`

The fusion layer references and adapts ideas around anti-slop frontend design,
brief inference, design-system selection, visual hierarchy, redesign workflow,
motion discipline, and final preflight review.

The full upstream license is available at:
`upstreams/taste-skill/LICENSE`.

## pbakaus/impeccable

- Repository: https://github.com/pbakaus/impeccable
- License: Apache-2.0
- Local path: `upstreams/impeccable`
- Initial pinned commit:
  `d2ab4ddee6fa63002fae680652b5fbd31735e280`
- Current absorbed commit:
  `c979ac37c361da564dcce100a4f2623d94ef54c8`

The fusion layer references and adapts ideas around command taxonomy, context
setup, audit/polish/harden/optimize/live workflows, deterministic detector
checks, design-system-aware validation, and production-readiness review.

The full upstream license is available at:
`upstreams/impeccable/LICENSE`.

## Vercel Geist design references

- Source: https://vercel.com/design.md
- Source: https://vercel.com/design.dark.md
- Local path: `skills/frontend-craft/templates/vercel-geist/`
- Retrieved: 2026-06-24

The fusion layer vendors these public design-system references as complete seed
templates for new or weakly specified developer-product design systems.

## Fusion-layer policy

- Keep upstream directories pristine.
- Do not automatically overwrite local fusion rules from upstream updates.
- Preserve license notices for copied or derived code and substantial text.
- Prefer original integration rules that cite upstream ideas rather than blind
  copy-paste.
