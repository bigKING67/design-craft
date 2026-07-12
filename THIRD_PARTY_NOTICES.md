# Third-party notices

This project is a personal fusion layer built on top of upstream open-source
design engineering and frontend quality skill projects. Upstream repositories
are kept as pristine submodules under `upstreams/`.

## Leonxlnx/taste-skill

- Repository: https://github.com/Leonxlnx/taste-skill
- License: MIT
- Copyright: 2026 Leonxlnx
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

The preserved distribution license is available at:
`LICENSES/MIT-upstreams.txt`.

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

The preserved distribution license and notice are available at:
`LICENSES/Apache-2.0.txt` and `LICENSES/NOTICE-impeccable.md`.

## Vercel design reference history

- Source: https://vercel.com/design.md
- Source: https://vercel.com/design.dark.md
- Local path: `skills/design-craft/templates/vercel-geist/`
- Retrieved: 2026-06-24

Historical commits used these public design-system references as seed inputs.
Because no separate redistribution license was identified, the current package
replaces the snapshots with original design-craft templates under
`skills/design-craft/templates/developer-product/`. The compatibility paths no
longer contain Vercel-authored snapshot text. See
`LICENSES/VERCEL-DESIGN-NOTICE.md` for provenance and scope.

## emilkowalski/skills

- Repository: https://github.com/emilkowalski/skills
- License: MIT
- Copyright: 2026 Emil Kowalski
- Local path: `upstreams/emilkowalski-skills`
- Initial pinned commit:
  `a47903a06a05d2e24c483bd8961c85969a51a494`
- Current absorbed commit:
  `b57fc72f8415d84db1e9cfb43270466bf12ac6e2`
- Current reviewed commit:
  `7bb7061b5cf7de15ea1aeaf00fbd9e6592a20fce`

The fusion layer references and adapts ideas around motion purpose, animation
frequency, easing and duration standards, physicality, gesture handling,
animation performance, reduced-motion behavior, strict animation review, and
animation vocabulary.
The 2026-07-10 review also absorbed product-design principles, direct
manipulation, presentation-value interruption, spring response/damping,
velocity handoff, momentum projection, rubber-banding, and optical typography
into original design-craft references.
The later 2026-07-11 range added `improve-animations`; design-craft selectively
adapted its codebase recon, prioritized audit, self-contained plan, and plan
reconciliation workflow while retaining project-authority and runtime-evidence
calibration instead of copying absolute heuristics.
The following `b024c8b` update changes README newsletter copy only and remains
provenance-only.
The subsequent `4691d39` and `7bb7061` range corrects two README typos only and
also remains provenance-only.
The 2026-07-12 five-Skill deep audit maps every upstream Skill entrypoint and
auxiliary Markdown file. The local fusion adds original calibrated rules and
implementation recipes rather than redistributing an upstream component
library; the reviewed upstream Skill tree contains no non-Markdown runtime
source. Substantial adapted text and code snippets remain covered by the
preserved MIT notice below.

The preserved distribution license is available at:
`LICENSES/MIT-upstreams.txt`.

## cameroncooke/AXe

- Repository: https://github.com/cameroncooke/AXe
- License: MIT
- CI tool version: `v1.7.1`
- Pinned release asset SHA-256:
  `26a64009c09a3ae980b1f1b4b377bd2a2dd96cbbde24821935e47352cb71cc69`

The native-runtime workflow downloads this pinned tool only on the ephemeral
macOS runner when a current iOS Simulator presents its system URL-opening
confirmation. AXe taps the real `Open` control by accessibility label; the
fixture must still receive the URL callback and write the interaction marker.
The AXe binary is not stored in this repository, included in the npm package,
or redistributed in release assets.

## Fusion-layer policy

- Keep upstream directories pristine.
- Do not automatically overwrite local fusion rules from upstream updates.
- Preserve license notices for copied or derived code and substantial text.
- Prefer original integration rules that cite upstream ideas rather than blind
  copy-paste.
