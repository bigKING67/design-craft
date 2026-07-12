---
name: design-craft
description: "Use for web, iOS, Android, and adaptive product UI/UX design engineering: product context, visual critique, design systems, UI polish, motion and interaction, accessibility, responsive behavior, and frontend/native implementation quality. Do not use for backend-only, database-only, algorithm-only, or CLI-only work."
---

# Design Craft

Production-grade design engineering work for this machine: product UI, UX,
visual taste, motion, design systems, web and native implementation,
performance, architecture, project quality, and directory governance in one
workflow.

## When not to use

Do not use `design-craft` for:

- Backend-only API changes with no user-visible product surface.
- Database-only migrations or data-model work with no UI contract.
- Pure algorithm, parsing, or CLI-only tasks.
- Generic refactors that do not affect product UI quality, frontend structure,
  browser behavior, responsive behavior, accessibility, or visual output.
- Copy-only writing where layout, hierarchy, or interface behavior is out of
  scope.

## Non-negotiable authority order

Use this order when evidence conflicts:

1. Live runtime behavior and browser evidence.
2. Scoped `AGENTS.md`, README, framework conventions, and current repo state.
3. Project `PRODUCT.md` for product/platform/user/accessibility context.
4. Project `DESIGN.md` or equivalent visual style authority.
5. Local frontend route planner output.
6. Bundled original developer-product seed templates for new or weak web
   systems.
7. `design-craft` references.
8. Upstream generic visual or Impeccable guidance.

Do not let generic visual rules override a project's product context, design
system, data density, report grammar, or runtime truth.

## First-pass workflow

1. Inspect the real repo before planning: `git status --short`, relevant
   `AGENTS.md`, optional `PRODUCT.md`, `DESIGN.md`, route files, package/build
   scripts, existing components, platform targets, style tokens, and similar
   implementations.
2. For L1+ frontend implementation tasks, run the local route planner when
   available:
   `bash ~/.codex/tools/frontend_route_plan.sh --surface <surface> --intent <intent> --scope <scope> [--platform <auto|web|ios|android|adaptive>] [--product-context-path <abs PRODUCT.md>] [--style-authority-path <abs DESIGN.md>] --output compact-json`.
   Use full `--output json` only when auditing the complete static delivery
   contract, or `--output human` for concise interactive inspection.
   Use only route-planner enum values. Do not put free-form task prose into
   `--surface`, `--intent`, or `--scope`; keep notes outside the command.
3. Treat route `candidate_skills` as candidates, not proof of actual use.
   Report `selected_skills` only for skills actually read and applied.
4. Pick the smallest mode that covers the task:
   - `shape`: UX/design brief before implementation.
   - `craft`: new feature or substantial UI build.
   - `critique`: read-only design-rightness, product fit, hierarchy, and
     anti-slop review.
   - `audit`: read-only quality review.
   - `polish`: finished UI refinement.
   - `harden`: production edge cases, error states, i18n, overflow.
   - `optimize`: measured UI performance work.
   - `structure`: file/directory governance.
   - `architecture`: frontend architecture and data-flow review.
5. Use helper scripts when available. Resolve them from the source repo or from
   `$DESIGN_CRAFT_HOME/scripts` first:
   `scripts/design_craft_route.sh` for route summaries,
   `scripts/design_craft_audit.sh` for read-only critique/audit/polish/harden/
   optimize/structure/architecture passes,
   `scripts/design_craft_pass.sh` as the preferred neutral wrapper,
   `scripts/design_craft_seed_design.sh` for seeding `DESIGN.md` and
   `DESIGN.dark.md` from the bundled original developer-product templates,
   `scripts/design_craft_motion_plan.py` for source-stamped motion implementation
   plan scaffolds,
   `scripts/design_craft_detect.sh` for detector and local design-craft signals,
   `scripts/design_craft_taste_review.sh` for stable product UI taste-review
   packets,
   `scripts/design_craft_l4_eval_case.sh` for L4 before/after eval scaffolds,
   `scripts/design_craft_l4_capture.py` for TMWD-first L4 screenshot capture
   plans and Chrome-headless fallback manifests,
   `scripts/design_craft_browser_evidence.py` for redacted DOM/computed-style
   evidence snippets and product UI score anti-inflation validation,
   `scripts/design_craft_css_smell_scan.py`,
   `scripts/design_craft_focus_audit.py`, and
   `scripts/design_craft_token_audit.py` for static review signals, and
   `scripts/design_craft_platform_scan.py` for platform inference and
   conservative iOS/Android/adaptive source checks,
   `scripts/design_craft_codex_route_pack.py` for auditing or exporting the
   local Codex frontend route-pack manifest, and
   `scripts/design_craft_score.py` for self-audits. When maintaining this skill
   repo, use `scripts/upstream_absorption_report.py` before absorbing new
   upstream commits.
   If the scripts are unavailable in the current agent, do not fail the design
   task only because automation is missing: read the relevant references,
   produce the design read, choose the smallest safe mode, and report the
   skipped automation explicitly.
6. Implement minimally, verify with the most relevant commands, and use a real
   browser for visible UI, interaction, responsive, report, dashboard, download,
   upload, or login-state changes. When the route requires screenshot evidence,
   report only actual screenshot artifacts, not planned screenshots.

## Reference routing

Read only the references needed for the current task:

- Visual redesign, landing pages, brand pages, portfolios:
  `references/visual-judgment.md`.
- Foundational hierarchy, CRAP/Gestalt-style reasoning, or "why does this feel
  off?" visual diagnosis:
  `references/foundational-visual-principles.md`.
- Design-system contracts, `DESIGN.md` shape, token naming, light/dark parity,
  component state coverage, focus rules, motion policy, and UI copy rules:
  `references/design-system-contract.md`.
- Product context, `PRODUCT.md`, platform discovery, users, purpose,
  positioning, and accessibility requirements:
  `references/product-context.md`.
- Product correctness, agency, responsibility, familiarity, flexibility,
  simplicity, craft, delight, wayfinding, and feedback:
  `references/product-design-principles.md`.
- New or weakly specified developer-product, SaaS, dashboard, admin, infra,
  docs, or tooling surfaces without a stronger style authority:
  `templates/developer-product/design.md` and
  `templates/developer-product/design.dark.md` as the default initial seed.
- Product UI taste scoring, "why not 100", screenshot/product-page review,
  concrete top issues, and acceptance criteria:
  `references/product-ui-taste-review.md`; add
  `references/taste-score-calibration.md` when the exact score or score band is
  the main deliverable.
- Redesign recommendations, concrete implementation moves, dashboard/card-soup
  repair, form/table/modal/navigation polish, and translating critique into
  changes:
  `references/design-move-library.md`.
- Impeccable-style command selection, critique/audit/polish/harden/optimize/live:
  `references/impeccable-workflow.md`.
- Subjective user complaint mapping, such as "太 AI", "颜色平", "排版不对",
  "文案弱", "移动端差", "卡顿", "动效怪", or "目录乱":
  `references/intent-map.md`.
- Motion, animation polish, high-motion surfaces, hover/press feedback, toasts,
  popovers, drawers, gestures, perceived animation performance, or reduced
  motion:
  `references/motion-quality.md`.
- Concrete web motion implementation recipes for press feedback, anchored
  overlays, tooltip groups, `@starting-style`, percentage transforms,
  clip-path, crossfade repair, or transient UI lifecycle:
  `references/motion-patterns.md` together with
  `references/motion-quality.md`.
- Whole-codebase animation improvement, motion inventory, prioritized audit,
  implementation-ready motion plans, or plan reconciliation: read
  `references/motion-audit-planning.md` together with
  `references/motion-quality.md`; if recon finds drag, swipe, sheet, drawer,
  momentum, reordering, or another direct-manipulation surface, also read
  `references/interaction-physics.md`. Scaffold individual plans from
  `templates/motion-plan/plan.md`.
- Gesture-driven motion, direct manipulation, interruption, springs, velocity
  handoff, projection, hysteresis, and rubber-banding:
  `references/interaction-physics.md`.
- Animation naming or reverse lookup, such as "这个弹出来的动画叫什么" or a
  vague motion description the user wants to prompt with:
  `references/motion-vocabulary.md`.
- Code elegance, component boundaries, state, types, errors:
  `references/engineering-quality.md`.
- Reusable component-library APIs, defaults, invisible interaction edge cases,
  and interactive documentation: `references/engineering-quality.md`; add
  `references/motion-patterns.md` when transient or animated UI is involved.
- UI performance, Web Vitals, render hot paths, charts/tables:
  `references/performance-quality.md`.
- Architecture, interfaces, migrations, data flow:
  `references/architecture-quality.md`.
- New files/directories or structure cleanup:
  `references/project-structure.md`.
- Surface-specific rules for landing, dashboard, data-viz, reports, and mobile:
  `references/surface-playbooks.md`.
- Native iOS/iPadOS quality: `references/ios-quality.md`.
- Native Android quality: `references/android-quality.md`.
- Cross-platform native adaptation and parity:
  `references/adaptive-quality.md`.
- Dashboard exports, static reports, special reports, formal business-review
  pages, and evidence-heavy report surfaces:
  `references/report-quality.md`.
- Validation and delivery fields:
  `references/validation-contract.md`.
- Upstream provenance and pinned source commits:
  `references/source-map.md`.

For broad "make this frontend excellent" tasks, start with only
`visual-judgment.md`, `product-ui-taste-review.md`, and
`validation-contract.md`. Add `design-move-library.md` for implementation,
`motion-quality.md` for motion, `performance-quality.md` for measured hot
paths, `project-structure.md` for structural changes, `report-quality.md` for
reports/dashboards, and `intent-map.md` for subjective briefs. Do not load the
entire reference library merely because the request is broad.

For native or cross-platform tasks, also read `product-context.md`,
`product-design-principles.md`, the matching platform reference(s),
`interaction-physics.md` when gestures are involved, and
`validation-contract.md`.

## Design read

Before major visual work, state one concise design read:

`Reading this as: <surface> for <audience>, with <vibe>, optimized for <primary job>.`

If the read changes implementation choices materially and cannot be inferred
from repo evidence or the user's brief, ask one focused question. Otherwise
proceed with the read and record it in the handoff/delivery.

## Quality gates

Block "done" until the relevant gates are satisfied or explicitly reported as
unverified:

- Visual: not templated, clear hierarchy, good density, responsive, accessible
  contrast, no generic AI tells.
- Design system: token roles are respected; hard-coded visual values are
  justified; theme parity, focus-visible states, component states, and UI copy
  quality are covered when relevant.
- Product: solves the user's job, preserves information architecture, handles
  empty/loading/error/long-data states when relevant.
- Platform: native navigation, controls, insets, gestures, accessibility, and
  adaptive structure match the resolved platform; mobile web is not mislabeled
  as native.
- Static evidence: source can prove present or missing branches, property
  ownership, and explicit values; it cannot prove perceived lag, smoothness,
  frame rate, compositing, browser-specific behavior, layout shift, or device
  feel. Label those as risks or runtime hypotheses until observed.
- Direct manipulation: for drag, swipe, sheet, drawer, reorder, momentum, or
  scrubbing work, reject input lockout and require pointer/native capture, grab
  offset, 1:1 tracking, explicit coordinate space and velocity units,
  interruption from the current presentation value without a jump,
  non-conflicting transform ownership, and a non-vestibular Reduced Motion
  path. Make the velocity units and bounded projected-endpoint method explicit,
  but do not change project-owned target-selection semantics unless product
  authority, existing behavior, or runtime evidence establishes momentum-based
  targeting.
- Engineering: clear component boundaries, no needless abstraction, observable
  errors, dependency checks before imports.
- Performance: measured or reasoned hot paths, no layout thrashing, no unbounded
  render/data work, sane bundle and asset choices.
- Architecture: interfaces and data flow are explicit; migration and
  compatibility risks are named.
- Structure: new files follow existing project conventions; shared abstractions
  have real repeated callers.
- Validation: targeted type/lint/test/build plus browser or native runtime
  validation where UI is user-visible; screenshot artifacts are required when
  route output asks for `browser_screenshot_required`.

## Delivery contract

For frontend implementation work, summarize:

- `frontend_tier`/`design_tier` and route command used, when applicable.
- `platform`, source, confidence, `product_context_path`, and whether product
  context was explicit or inferred.
- `candidate_skills` versus `selected_skills`.
- `style_authority_path` and whether it was enforced or intentionally evolved.
- `design_system_contract`: enforced existing tokens, evolved tokens, inferred
  temporary system, or not applicable.
- Files changed and structure impact.
- Validation commands and observed results.
- Browser/native runtime validation kind, target, and result, or why it was
  skipped.
- Screenshot validation tool, target, artifact path/hash/dimensions, or why it
  was skipped.
- Performance impact and remaining risks.

Default critique and audit budget:

- one-sentence diagnosis;
- at most five blocking findings and five secondary findings;
- at most eight concrete design moves;
- the smallest validation plan that can change the decision;
- target 150 lines or fewer unless the user explicitly requests an exhaustive
  review, full scorecard, or report artifact.

Keep output concise, evidence-backed, and honest about anything not verified.
