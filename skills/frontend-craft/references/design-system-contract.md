# Design system contract

Use this when a project has a `DESIGN.md`, design tokens, theme files,
CSS variables, Tailwind theme values, reusable UI components, light/dark mode,
or when the task changes visual foundations rather than one isolated style.

This reference is about system discipline, not a specific aesthetic. It should
help preserve the product's own visual language instead of making every project
look like one upstream design system.

## Default seed

For a new project or a weakly specified developer-product surface, start from
the bundled Vercel Geist templates:

- `templates/vercel-geist/design.md`
- `templates/vercel-geist/design.dark.md`

Use them as the default initial `DESIGN.md` pair for SaaS, dashboard, admin,
infra, docs, tooling, and other developer-facing product surfaces. If the
project already has a credible `DESIGN.md`, token system, brand guide, or strong
runtime style, keep the project authority first and use the Geist templates as a
comparison baseline for missing token layers, states, focus, motion, and copy.

Use `scripts/frontend_craft_seed_design.sh --target <project-dir>` when the
right move is to create the initial pair directly. The helper refuses to
overwrite existing `DESIGN.md` or `DESIGN.dark.md` unless `--force` is explicit.

## Authority

- Live runtime behavior, scoped project rules, and the project `DESIGN.md`
  outrank this reference.
- Implemented tokens and shared components are evidence. If docs and code
  conflict, verify the current runtime before deciding whether docs are stale.
- Do not create a parallel style authority. Evolve the existing one when the
  user approves a system change.
- The bundled Geist templates are allowed as the default seed when no stronger
  project style authority exists. Once a project-specific system exists, prefer
  adapting it over repeatedly re-applying the seed.
- If `frontend_craft_route.sh` reports `vercel_geist_seed_applicable: true`,
  treat that as a prompt to create or compare against the seed, not as
  permission to ignore live runtime style.

## Recommended DESIGN.md shape

A strong `DESIGN.md` is both machine-readable and readable by agents:

- Front matter or a structured block for tokens:
  - colors
  - typography
  - spacing
  - radii
  - elevation
  - motion
  - component variants
- Markdown rationale for:
  - product feel and audience
  - color semantics
  - typography roles
  - layout rhythm
  - component behavior
  - motion policy
  - voice and content rules
  - do and don't rules

Light and dark themes should use identical token names with different values.
Components should consume semantic tokens, not branch on theme-specific literal
colors.

## Token layers

Keep token roles separate:

- Surface: page, section, card, popover, overlay.
- Text: primary, secondary, muted, disabled, inverse.
- Border and overlay: divider, hairline, default border, hover border, active
  border, hover overlay.
- State and accent: focus, link, success, warning, danger, info.
- Data: chart series, positive/negative deltas, neutral deltas, categorical
  ramps, sequential ramps.

Avoid swapping surface tokens for text gray tokens or using one gray scale for
every role. Hard-coded visual values are acceptable only when the project has
no token layer yet or when the change explicitly creates one.

## Theme parity

For light/dark work:

- Keep token names stable across themes.
- Define hover, active, disabled, focus, and border states for both themes.
- Check focus rings against both backgrounds.
- Do not rely on simple color inversion; re-balance surface contrast, borders,
  muted text, and accent intensity per theme.
- Components should not need `if dark` logic for basic colors when token parity
  can solve the problem.

## Typography roles

Choose typography by role before choosing size:

- Heading: page and section hierarchy; tighter line-height, stronger weight,
  and intentional tracking when needed.
- Label: navigation, form labels, table headers, metadata, chips, control text;
  optimized for single-line scanning.
- Copy: body, helper text, empty states, error explanations; optimized for
  multi-line reading.
- Mono/data: code, IDs, metrics, logs, tabular figures, compact data values.

Avoid three adjacent type sizes that visually collapse into the same hierarchy.
For dashboards and reports, data typography must be as intentional as prose.

## Layout rhythm

Prefer a small spacing scale over ad hoc gaps:

- Use a base scale, usually 4px or the project's established equivalent.
- Use smaller gaps inside a group, medium gaps between groups, and larger gaps
  between sections.
- Cards should have consistent padding tiers for compact, standard, and hero
  contexts.
- Use spacing and borders for hierarchy before adding heavy shadows.
- Responsive layouts should preserve grouping and priority, not merely stack all
  children in source order.

## Component state matrix

Shared interactive components should define the relevant states:

- default
- hover
- active
- disabled
- loading or pending
- focus-visible
- error, invalid, or destructive when applicable
- empty and success states when the component owns feedback

Button and input variants should specify size, height, padding, radius,
typography, icon spacing, and state transitions. Do not leave keyboard focus as
an afterthought; every interactive element needs a visible `:focus-visible`
state.

## Motion

Motion should clarify state, hierarchy, or causality.

- Prefer instant or very short transitions for simple state changes.
- Use slightly longer transitions for popovers, menus, overlays, and dialogs.
- Animate transform and opacity before layout properties.
- Avoid blanket `transition-all` on large surfaces or hot paths.
- Honor `prefers-reduced-motion` for nonessential motion.
- Do not hide content until JavaScript-triggered reveal effects run.

## Voice and content

UI copy is part of the system:

- Buttons and menu actions should name the action and object, such as
  `Create Project` or `Delete Member`.
- Avoid weak generic labels such as `OK`, `Confirm`, `Submit`, and bare verbs
  when a specific action is known.
- Errors should state what happened and what to do next.
- Toasts should name the thing that changed and avoid filler like
  `successfully`.
- Empty states should point to the first useful action.
- Loading states should describe the in-progress action.

## Audit checklist

When the task touches design-system concerns, check:

- Was the project style authority enforced, evolved, inferred, or not
  applicable?
- Did the change add unexplained literal colors, spacing, radii, shadows, font
  sizes, or timing values?
- Do light and dark themes keep token parity?
- Are focus-visible, disabled, loading, error, and empty states covered where
  relevant?
- Does UI copy follow the project voice and avoid generic placeholders?
- Did the change improve the system rather than create a one-off exception?
