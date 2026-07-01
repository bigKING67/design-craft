---
name: design-craft
description: "Use for product UI/UX and frontend design-quality work: visual taste critique, design-system enforcement, UI polish, motion review, responsive/browser validation, and frontend craft. Do not use for backend-only logic, database-only migrations, pure algorithms, CLI-only tools, or non-visual refactors unless UI quality is affected."
---

# Design Craft

Production-grade design engineering work for this machine: product UI, UX,
visual taste, motion, design systems, frontend implementation, performance,
architecture, project quality, and directory governance in one workflow.

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
3. Project `DESIGN.md` or equivalent style authority.
4. Local frontend route planner output.
5. Bundled Vercel Geist seed templates for new or weak developer-product
   systems.
6. `design-craft` references.
7. Upstream generic visual or Impeccable guidance.

Do not let generic visual rules override a project's product context, design
system, data density, report grammar, or runtime truth.

## First-pass workflow

1. Inspect the real repo before planning: `git status --short`, relevant
   `AGENTS.md`, `DESIGN.md`, route files, package scripts, existing components,
   style tokens, and similar implementations.
2. For L1+ frontend implementation tasks, run the local route planner when
   available:
   `bash ~/.codex/tools/frontend_route_plan.sh --surface <surface> --intent <intent> --scope <scope> [--style-authority-path <abs DESIGN.md>]`.
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
   `DESIGN.dark.md` from the bundled Vercel Geist templates,
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
- New or weakly specified developer-product, SaaS, dashboard, admin, infra,
  docs, or tooling surfaces without a stronger style authority:
  `templates/vercel-geist/design.md` and
  `templates/vercel-geist/design.dark.md` as the default initial seed.
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
- Animation naming or reverse lookup, such as "这个弹出来的动画叫什么" or a
  vague motion description the user wants to prompt with:
  `references/motion-vocabulary.md`.
- Code elegance, component boundaries, state, types, errors:
  `references/engineering-quality.md`.
- UI performance, Web Vitals, render hot paths, charts/tables:
  `references/performance-quality.md`.
- Architecture, interfaces, migrations, data flow:
  `references/architecture-quality.md`.
- New files/directories or structure cleanup:
  `references/project-structure.md`.
- Surface-specific rules for landing, dashboard, data-viz, reports, mobile:
  `references/surface-playbooks.md`.
- Dashboard exports, static reports, special reports, formal business-review
  pages, and evidence-heavy report surfaces:
  `references/report-quality.md`.
- Validation and delivery fields:
  `references/validation-contract.md`.
- Upstream provenance and pinned source commits:
  `references/source-map.md`.

For broad "make this frontend excellent" tasks, read:
`visual-judgment.md`, `foundational-visual-principles.md`,
`product-ui-taste-review.md`, `design-move-library.md`, `motion-quality.md`,
`impeccable-workflow.md`, `engineering-quality.md`, `performance-quality.md`,
`project-structure.md`, `report-quality.md` when reports/dashboards are in
scope, `intent-map.md` when the brief is subjective, and
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
- Engineering: clear component boundaries, no needless abstraction, observable
  errors, dependency checks before imports.
- Performance: measured or reasoned hot paths, no layout thrashing, no unbounded
  render/data work, sane bundle and asset choices.
- Architecture: interfaces and data flow are explicit; migration and
  compatibility risks are named.
- Structure: new files follow existing project conventions; shared abstractions
  have real repeated callers.
- Validation: targeted type/lint/test/build plus browser validation where UI is
  user-visible; screenshot artifacts are required when route output asks for
  `browser_screenshot_required`.

## Delivery contract

For frontend implementation work, summarize:

- `frontend_tier` and route command used, when applicable.
- `candidate_skills` versus `selected_skills`.
- `style_authority_path` and whether it was enforced or intentionally evolved.
- `design_system_contract`: enforced existing tokens, evolved tokens, inferred
  temporary system, or not applicable.
- Files changed and structure impact.
- Validation commands and observed results.
- Browser validation target and result, or why it was skipped.
- Screenshot validation tool, target, artifact path/hash/dimensions, or why it
  was skipped.
- Performance impact and remaining risks.

Keep output concise, evidence-backed, and honest about anything not verified.
