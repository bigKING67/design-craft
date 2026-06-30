---
name: frontend-craft
description: Personal frontend craft and quality workflow for Codex. Use when working on frontend pages, components, dashboards, admin apps, landing pages, reports, data visualizations, UX polish, visual redesigns, responsive behavior, accessibility, UI performance, frontend architecture, code elegance, project quality, or file/directory structure governance. Fuses the local route-plan/DESIGN.md/browser-validation/screenshot-evidence workflow with anti-slop visual judgment and Impeccable-style audit, polish, harden, optimize, detector, and live iteration practices.
---

# Frontend Craft

Production-grade frontend work for this machine: design quality, code elegance,
performance, architecture, project quality, and directory governance in one
workflow.

## Non-negotiable authority order

Use this order when evidence conflicts:

1. Live runtime behavior and browser evidence.
2. Scoped `AGENTS.md`, README, framework conventions, and current repo state.
3. Project `DESIGN.md` or equivalent style authority.
4. Local frontend route planner output.
5. Bundled Vercel Geist seed templates for new or weak developer-product
   systems.
6. `frontend-craft` references.
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
5. Use the helper scripts from the source repo when available:
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/frontend_craft_route.sh`
   for route summaries,
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/frontend_craft_audit.sh`
   for read-only critique/audit/polish/harden/optimize/structure/architecture
   passes,
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/frontend_craft_pass.sh`
   as the preferred neutral wrapper for those quality passes,
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/frontend_craft_seed_design.sh`
   for seeding `DESIGN.md` and `DESIGN.dark.md` from the bundled Vercel Geist
   templates,
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/frontend_craft_detect.sh`
   for detector signals,
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/frontend_craft_taste_review.sh`
   for stable product UI taste-review packets,
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/frontend_craft_browser_evidence.py`
   for redacted DOM/computed-style evidence snippets and product UI score
   anti-inflation validation, and
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/frontend_craft_score.py`
   for self-audits. When maintaining this skill repo, use
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/upstream_absorption_report.py`
   before absorbing new upstream commits.
6. Implement minimally, verify with the most relevant commands, and use a real
   browser for visible UI, interaction, responsive, report, dashboard, download,
   upload, or login-state changes. When the route requires screenshot evidence,
   report only actual screenshot artifacts, not planned screenshots.

## Reference routing

Read only the references needed for the current task:

- Visual redesign, landing pages, brand pages, portfolios:
  `references/visual-judgment.md`.
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
- Impeccable-style command selection, critique/audit/polish/harden/optimize/live:
  `references/impeccable-workflow.md`.
- Subjective user complaint mapping, such as "太 AI", "颜色平", "排版不对",
  "文案弱", "移动端差", "卡顿", or "目录乱":
  `references/intent-map.md`.
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
- DataHub, dashboard exports, static reports, special reports, and formal
  business-review pages:
  `references/report-quality.md`.
- Validation and delivery fields:
  `references/validation-contract.md`.
- Upstream provenance and pinned source commits:
  `references/source-map.md`.

For broad "make this frontend excellent" tasks, read:
`visual-judgment.md`, `product-ui-taste-review.md`, `impeccable-workflow.md`,
`engineering-quality.md`, `performance-quality.md`,
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
