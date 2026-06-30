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
- `scripts/frontend_craft_pass.sh --target <repo> --mode <critique|audit|polish|harden|optimize|structure|architecture>`
  as the preferred neutral pass wrapper.
- `scripts/frontend_craft_audit.sh --target <repo> --mode <critique|audit|polish|harden|optimize|structure|architecture>`
  as the compatibility entrypoint behind the pass wrapper.
- `scripts/frontend_craft_detect.sh --target <path>` for upstream Impeccable
  findings plus local frontend-craft review signals; use `--json-only` only when
  raw upstream detector compatibility is required.
- `scripts/frontend_craft_seed_design.sh --target <project-dir>` when a new or
  weak developer-product surface needs the bundled Vercel Geist `DESIGN.md`
  pair as its initial design-system authority.
- `scripts/frontend_craft_taste_review.sh --target <screenshot-or-project>`
  when a product UI taste score or screenshot critique needs a stable review
  packet before implementation.
- `scripts/frontend_craft_score.py --self`
- `scripts/upstream_absorption_report.py --remote` when checking whether pinned
  upstreams have newer remote heads before absorption work.
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

## Screenshot evidence

Use screenshot evidence when route output sets `browser_screenshot_required` or
when the visual decision depends on actual rendered style.

Preferred flow with TMWD:

1. Use `browser_tab_lifecycle` with `action:"select_or_create"` and a stable
   `workspace_key` for the project or surface.
2. Use `browser_wait` for `selector`, `dom_stable`, or `network_idle` before
   capturing; do not use fixed sleeps as readiness proof.
3. Use `browser_screenshot_ops target:"viewport"` for baseline visual QA.
4. Use `target:"selector"` or `target:"clip"` for focused changed sections.
5. Use `target:"full_page"` only for bounded pages and pass an explicit
   `max_pixels`.
6. Report artifact `path`, `sha256`, `dimensions`, and `target`. Do not paste
   base64 or claim screenshot validation when no artifact was produced.
7. Finalize the managed tab with `browser_tab_lifecycle action:"finalize_task"`
   unless the user asked to keep it.

If `tmwd_browser` is unavailable, report the skipped reason, residual risk, and
the exact command/tool that should capture the artifact next.

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
- `browser_screenshot_required`
- `preferred_screenshot_tool`
- `screenshot_validation_plan`
- `directory_governance_required`
- `performance_review_required`
- `vercel_geist_seed_applicable` and reason

Never say a subagent was enabled unless it actually spawned. Never say browser
validation passed unless a browser tool verified the target.
Never say screenshot validation passed unless `browser_screenshot_ops` or an
equivalent browser screenshot tool produced artifact path/hash/dimensions.

## Quality score

Use the score helper as a maintenance signal for this skill project, not as a
replacement for task-specific judgment. A score below 80 means the skill is
still seed quality. A score between 80 and 89 is usable v0.x. A score above 90
requires forward evals and real task evidence, not only file-presence checks.

The 100-point score in `product-ui-taste-review.md` is different: it grades one
specific UI surface. When reporting both, name them explicitly as
`frontend-craft source score` versus `product UI taste score`.

For product UI taste reviews, also report the evidence level:

- `L0 static`: screenshot, wireframe, or prose only.
- `L1 contextual`: screenshot plus product/user/task context.
- `L2 browser`: browser screenshot plus DOM/computed style or token evidence.
- `L3 resilient`: responsive and important interaction states checked.
- `L4 before/after`: before/after evidence plus validation commands and diff.

Do not claim states or responsive behavior as verified when the evidence level
does not cover them.

## Unverified work

If validation cannot run, state:

- Exact command or browser check that was skipped.
- Reason.
- Risk.
- Suggested next command.

Do not turn an unverified assumption into "done".
