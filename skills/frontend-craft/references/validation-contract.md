# Validation contract

Use this before calling frontend work complete.

## Minimal command ladder

Pick the smallest command set that covers the change:

- Type-only or props change: type-check.
- Styling/component change: type-check plus lint if available.
- Build-system or route change: type-check, lint, build.
- Data behavior: relevant unit/integration tests plus type-check.
- Visual/report/dashboard work: type/lint/build as relevant plus browser smoke.
- Performance work: baseline and after measurement when possible.

Prefer project scripts in `package.json`. Do not invent commands when the repo
has established ones.

For the `frontend-craft` source repo itself, use:

- `scripts/frontend_craft_route.sh --target <repo> --surface <surface> --intent <intent> --scope <scope>`
- `scripts/frontend_craft_audit.sh --target <repo> --mode <audit|polish|harden|optimize|structure|architecture>`
- `scripts/frontend_craft_detect.sh --target <path>` for upstream Impeccable
  findings plus local frontend-craft review signals; use `--json-only` only when
  raw upstream detector compatibility is required.
- `scripts/frontend_craft_score.py --self`
- `scripts/validate.sh`

## Route planner argument hygiene

Route planner arguments must use fixed enum values:

- `--surface`: `auto`, `dashboard`, `app`, `admin`, `data-app`, `landing`,
  `promo`, `homepage`, `marketing`, `mobile`, or `brand`.
- `--intent`: `auto`, `functional`, `visual-refine`, `redesign`, `new-page`,
  `high-motion`, `brand`, `mobile-flow`, or `reference-only`.
- `--scope`: `auto`, `micro`, `component`, `section`, `page`, or
  `multi-page`.

Do not pass natural-language task descriptions as route argument values. Record
those notes in the plan or delivery summary instead.

## Browser validation

Use browser validation for:

- User-visible pages and components.
- Interactions, forms, navigation, uploads/downloads.
- Login-state or protected routes.
- Responsive behavior.
- Charts, reports, dashboards, canvas/SVG sizing.
- Motion, focus, hover, or keyboard behavior.

Default flow:

1. Start or identify the dev server.
2. Open the route in a managed browser tab when possible.
3. Check desktop and a narrow mobile viewport for layout overflow when visual
   changes are involved.
4. Inspect DOM/computed style only when needed to prove a specific condition.
5. Finalize managed tabs unless the user asked to keep them.

## Design-system validation

Use design-system validation when:

- A project `DESIGN.md` exists or is changed.
- Theme files, CSS variables, design tokens, Tailwind theme values, or shared UI
  component styles are changed.
- Light/dark mode, focus styles, motion primitives, form states, toast/error UI,
  or empty states are changed.
- A visual polish changes colors, typography, spacing, radii, shadows, or motion.

Check and report:

- Whether the design-system contract was enforced, evolved, inferred from code,
  or not applicable.
- Whether the bundled Vercel Geist seed templates were used as the initial
  baseline, and whether the project had a stronger style authority.
- New hard-coded colors, arbitrary spacing, arbitrary radii, arbitrary shadows,
  font sizes, or timing values, and why they are justified.
- Light/dark token parity for the touched tokens and states.
- Visible `:focus-visible` for touched interactive elements.
- Disabled, loading, error, empty, and success states where the changed surface
  owns those states.
- UI copy quality for actions, errors, toasts, empty states, and loading labels;
  avoid weak labels such as `OK`, `Confirm`, `Submit`, `Success`, and
  `Something went wrong` when a specific action or recovery step is known.

## Route summary fields

When route planner is used, report:

- `frontend_tier`
- `candidate_skills`
- `selected_skills`
- `execution_mode` and `subagent_required`
- `style_authority_path`, source, mode, and revision policy
- `design_system_contract`
- `preflight_status` and `preflight_code`
- `browser_validation_required`
- `directory_governance_required`
- `performance_review_required`

Never say a subagent was enabled unless it actually spawned. Never say browser
validation passed unless a browser tool verified the target.

## Quality score

Use the score helper as a maintenance signal for this skill project, not as a
replacement for task-specific judgment. A score below 80 means the skill is
still seed quality. A score between 80 and 89 is usable v0.x. A score above 90
requires forward evals and real task evidence, not only file-presence checks.

## Unverified work

If validation cannot run, state:

- Exact command or browser check that was skipped.
- Reason.
- Risk.
- Suggested next command.

Do not turn an unverified assumption into "done".
