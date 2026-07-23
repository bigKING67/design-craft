# Validation contract

Use this before calling frontend work complete.

## Contents

- [Minimal command ladder](#minimal-command-ladder)
- [Route planner argument hygiene](#route-planner-argument-hygiene)
- [Browser validation](#browser-validation)
- [Screenshot evidence](#screenshot-evidence)
- [Native runtime validation](#native-runtime-validation)
- [Design-system validation](#design-system-validation)
- [Route summary fields](#route-summary-fields)
- [Quality score](#quality-score)
- [Cross-agent validation](#cross-agent-validation)
- [Unverified work](#unverified-work)

## Minimal command ladder

Pick the smallest command set that covers the change:

- Type-only or props change: type-check.
- Styling/component change: type-check plus lint if available.
- Build-system or route change: type-check, lint, build.
- Data behavior: relevant unit/integration tests plus type-check.
- Visual/report/dashboard work: type/lint/build as relevant plus browser smoke.
- Native UI work only when the resolved target is `ios`, `android`, or
  `adaptive`: platform build/static checks plus simulator/emulator or real
  device validation when the toolchain exists. Native gates are not part of an
  ordinary Web/desktop task.
- Performance work: baseline and after measurement when possible.

Prefer project scripts in `package.json`. Do not invent commands when the repo
has established ones.

For the `design-craft` source repo itself, use:

- `scripts/design_craft_route.sh --target <repo> --surface <surface> --intent <intent> --scope <scope>`
- `scripts/design_craft_platform_scan.py --target <repo> --platform auto --json`
  for platform inference and conservative native source findings.
- `scripts/design_craft_pass.sh --target <repo> --mode <critique|audit|polish|motion|harden|optimize|structure|architecture>`
  as the preferred neutral pass wrapper.
- `scripts/design_craft_audit.sh --target <repo> --mode <critique|audit|polish|motion|harden|optimize|structure|architecture>`
  as the compatibility entrypoint behind the pass wrapper.
- `scripts/design_craft_detect.sh --target <path>` for upstream Impeccable
  findings plus local design-craft review signals; use `--json-only` only when
  raw upstream detector compatibility is required.
- `scripts/design_craft_seed_design.sh --target <project-dir>` when a new or
  weak developer-product surface needs the bundled original `DESIGN.md`
  pair as its initial design-system authority.
- `scripts/design_craft_taste_review.sh --target <screenshot-or-project>`
  when a product UI taste score or screenshot critique needs a stable review
  packet before implementation.
- `scripts/design_craft_browser_evidence.py --print-js` to emit a redacted
  DOM/computed-style sampler for TMWD `browser_execute_js`.
- `scripts/design_craft_browser_evidence.py --validate-score-json <path>` and
  `--validate-evidence-json <path>` to guard product UI score inflation and
  captured browser evidence schema.
- `scripts/design_craft_css_smell_scan.py --target <path>`,
  `scripts/design_craft_focus_audit.py --target <path>`, and
  `scripts/design_craft_token_audit.py --target <path>` to collect static UI
  smell signals. Treat these as review prompts, not automatic design verdicts.
- `scripts/design_craft_static_review.py --target <path> --json` when a single
  normalized static review packet is easier to attach to an agent handoff.
- `scripts/design_craft_doctor.sh --target <path>` for local portability and
  optional capability checks.
- `scripts/design_craft_codex_route_pack.py --strict` to audit the local Codex
  frontend route planner, frontend rule, preflight contract, and route tests as
  a whitelisted migration manifest.
- `scripts/design_craft_cross_agent_validate.py --root evals/cross-agent` for
  benchmark task definitions, and `--observed-task <task-dir>` only after real
  agent outputs have been recorded.
- `scripts/design_craft_init_agent.sh --agent <codex|cursor|claude|pi|generic>
  --target <path> --dry-run` before installing the canonical skill into another
  host agent.
- `scripts/design_craft_score.py --self`
- `scripts/design_craft_maturity.py --profile development` for the repository
  development baseline. Its route-pack gate uses an isolated portable self-check
  and does not read operator `~/.codex` state. Run the explicit `--strict`
  route-pack command above when auditing an installed Codex host. Release
  maintainers use `--profile operational_95` or `--profile certified_100` with a
  committed matching-runner `--baseline`. Those names are evidence tiers with
  all-required gates, not composite quality scores. `design_craft_score.py`
  measures source completeness only.
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
- `--platform`: `auto`, `web`, `ios`, `android`, or `adaptive`.
- `--product-context-path`: absolute path to optional `PRODUCT.md`.

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
when the visual decision depends on actual rendered style. Do not request
screenshots for every frontend change. Follow the route screenshot policy:

- `screenshot_evidence_level=none`: no screenshot artifact required, typical
  for micro copy, font, spacing, or color tweaks.
- `screenshot_evidence_level=optional`: capture only if rendered ambiguity,
  visual regression risk, or state coverage remains after code/browser checks.
- `screenshot_evidence_level=required`: produce screenshot artifact evidence,
  typical for section/page layout, redesign, new page, reference fidelity,
  responsive, state-heavy, mobile, or high-motion work.

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
the exact command/tool that should capture the artifact next. For L4
before/after evals, `scripts/design_craft_l4_capture.py --dry-run` may produce a
TMWD-first capture plan, and the non-dry-run Chrome-headless fallback may write
repo-external PNG artifacts plus `screenshots.json`; neither path verifies
interaction states unless separate state evidence is captured.

## Native runtime validation

For `ios`, `android`, or `adaptive`, static source scan is a floor rather than a
runtime verdict. Skip this section for `web`; a mobile viewport or WebView shell
does not create a native validation requirement.

Report route fields:

- `runtime_validation_required`
- `runtime_validation_kind`
- `native_validation_required`
- `preferred_runtime_tool`

iOS validation should distinguish `xcodebuild` compile/test, Simulator
(`simctl`) behavior, and real-hardware truth. Android validation should
distinguish Gradle compile/test, Emulator/`adb` behavior, and real-hardware
truth. Adaptive validation reports both platforms independently.

If the local machine lacks a simulator/emulator toolchain, run the conservative
platform fixture/source checks and report exactly:

- `iOS Simulator: unverified locally`, when iOS is in scope.
- `Android Emulator: unverified locally`, when Android is in scope.

Do not turn a static scan or CI fixture into an observed native runtime claim.

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
- Whether the bundled developer-product seed templates were used as the initial
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
- Static scanner findings, when used, with clear severity and target path. Do
  not present scanner findings as proof of visual quality without browser or
  runtime evidence.

## Route summary fields

Use `--output compact-json` for normal agent handoff/context ingestion and
`--output json` only when the complete static delivery contract is required.
Use `--output human` for interactive inspection. When route planner is used,
report:

- `frontend_tier`
- `design_tier` (must equal `frontend_tier` under `frontend-route-v2`)
- `platform`, `platform_source`, and `platform_confidence`
- `product_context_path`
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
- `runtime_validation_required`, `runtime_validation_kind`,
  `native_validation_required`, and `preferred_runtime_tool`
- `developer_product_seed_applicable` and reason; legacy route payloads may also
  expose `vercel_geist_seed_applicable` as a compatibility alias

Never say a subagent was enabled unless it actually spawned. Never say browser
validation passed unless a browser tool verified the target.
Never say screenshot validation passed unless `browser_screenshot_ops` or an
equivalent browser screenshot tool produced artifact path/hash/dimensions.

## Quality score

`scripts/design_craft_score.py` reports **source completeness**. It answers
whether the intended source contracts and references exist; it can reach 100
without proving installation or runtime behavior.

`scripts/design_craft_maturity.py` reports **operational maturity**. It gates
runtime scripts, source/install parity, reviewed upstreams, CI, observed evals,
degraded route/detector behavior, and native runtime evidence. A score above 90
requires forward evals and real task evidence, not only file presence.

Operational maturity is profile-specific:

- `desktop` covers the daily computer-based Web/frontend workflow and can reach
  100 without iOS/Android runtime or Cursor/Claude evidence.
- `portable` and normal release readiness use a 95-point boundary while keeping
  optional host/native proof visible rather than silently promoting it.
- certified release maturity 100 requires all four current-source host runs and
  current-source iOS Simulator, Android Emulator, and physical-device evidence.

Do not use the certification profile to declare ordinary Web development
incomplete, and do not use the desktop profile to claim native release proof.

The 100-point score in `product-ui-taste-review.md` is different: it grades one
specific UI surface. When reporting both, name them explicitly as
`design-craft source score` versus `product UI taste score`.

For product UI taste reviews, also report the evidence level:

- `L0 static`: screenshot, wireframe, or prose only.
- `L1 contextual`: screenshot plus product/user/task context.
- `L2 browser`: browser screenshot plus DOM/computed style or token evidence.
- `L3 resilient`: responsive and important interaction states checked.
- `L4 before/after`: before/after evidence plus validation commands and diff.

Do not claim states or responsive behavior as verified when the evidence level
does not cover them.

L3/L4 product UI score cases must include `responsive_viewports` and
`state_checks` in their `score.json`. If flat hierarchy or card soup remains the
main visible issue, do not score above 84 just because the layout fits multiple
viewports.

The `evals/product-ui-taste/before-after/_template/` files are scaffolding only.
They are not real L4 evidence and must not be cited as a completed improvement.

## Cross-agent validation

When validating adapter portability, use:

- `scripts/design_craft_init_agent.sh --agent <agent> --target <temp-dir>
  --scope project --dry-run`
- `scripts/design_craft_doctor.sh --target . --json`
- `scripts/design_craft_cross_agent_validate.py --observed-task <task-dir>`
  only after real agent outputs are collected.

Do not claim Cursor, Claude, Pi, Codex, or another host behaves consistently
until that host has actually run the same benchmark prompt and its output is
recorded.

For the 0.3.0 dashboard benchmark, only Codex and Pi have recorded same-prompt
outputs. Cursor and Claude are explicit unverified hosts for that benchmark.

## Unverified work

If validation cannot run, state:

- Exact command or browser check that was skipped.
- Reason.
- Risk.
- Suggested next command.

Do not turn an unverified assumption into "done".
