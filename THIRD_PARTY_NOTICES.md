# Third-party notices

This project is a personal fusion layer built on top of upstream open-source
design engineering and frontend quality skill projects. Upstream repositories
are kept as pristine submodules under `upstreams/`.

## Leonxlnx/taste-skill

- Repository: https://github.com/Leonxlnx/taste-skill
- License: MIT
- Local path: `upstreams/taste-skill`
- Initial pinned commit:
  `06d6028b5c623016c59ce8536f578e5a1127b499`
- Current reviewed commit:
  `b17742737e796305d829b3ad39eda3add0d79060`

The fusion layer references and adapts ideas around anti-slop frontend design,
brief inference, design-system selection, visual hierarchy, redesign workflow,
motion discipline, and final preflight review.
The reviewed 2026-07-10 range changed sponsorship/readme assets only, so it is
retained as provenance and did not change design-craft behavior.

The full upstream license is available at:
`upstreams/taste-skill/LICENSE`.

## pbakaus/impeccable

- Repository: https://github.com/pbakaus/impeccable
- License: Apache-2.0
- Local path: `upstreams/impeccable`
- Initial pinned commit:
  `d2ab4ddee6fa63002fae680652b5fbd31735e280`
- Current absorbed commit:
  `da99645a58400ed7acb201e6904f9413efd89c6e`
- Current reviewed commit:
  `630fc2682a5bd39b25a8e61f74b6b3f14f2b1e21`

The fusion layer references and adapts ideas around command taxonomy, context
setup, audit/polish/harden/optimize/live workflows, deterministic detector
checks, design-system-aware validation, and production-readiness review.
The 2026-07-10 review selectively absorbed platform routing, native audit/adapt
guidance, iOS/Android quality rules, and detector/design-system fixes. Generated
provider bundles, site output, dependencies, and store packaging remain
provenance only.
The 2026-07-11 reviewed range changes only GitHub sheriff automation and tests;
no additional fusion-layer behavior was imported.

The full upstream license is available at:
`upstreams/impeccable/LICENSE`.

## Vercel Geist design references

- Source: https://vercel.com/design.md
- Source: https://vercel.com/design.dark.md
- Local path: `skills/design-craft/templates/vercel-geist/`
- Retrieved: 2026-06-24

The fusion layer vendors these public design-system references as complete seed
templates for new or weakly specified developer-product design systems.

## emilkowalski/skills

- Repository: https://github.com/emilkowalski/skills
- License: MIT
- Local path: `upstreams/emilkowalski-skills`
- Initial pinned commit:
  `a47903a06a05d2e24c483bd8961c85969a51a494`
- Current absorbed commit:
  `f76beceb7d3fc8c43309cefad5a095a206103a4e`
- Current reviewed commit:
  `220e8607c90b17337d210125777b7b695f26c221`

The fusion layer references and adapts ideas around motion purpose, animation
frequency, easing and duration standards, physicality, gesture handling,
animation performance, reduced-motion behavior, strict animation review, and
animation vocabulary.
The 2026-07-10 review also absorbed product-design principles, direct
manipulation, presentation-value interruption, spring response/damping,
velocity handoff, momentum projection, rubber-banding, and optical typography
into original design-craft references.
The 2026-07-11 reviewed range changes one README apostrophe only and required no
additional absorption.

The full upstream license is available at:
`upstreams/emilkowalski-skills/LICENSE`.

## Fusion-layer policy

- Keep upstream directories pristine.
- Do not automatically overwrite local fusion rules from upstream updates.
- Preserve license notices for copied or derived code and substantial text.
- Prefer original integration rules that cite upstream ideas rather than blind
  copy-paste.
