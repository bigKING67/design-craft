---
name: frontend-craft
description: Personal frontend craft and quality workflow for Codex. Use when working on frontend pages, components, dashboards, admin apps, landing pages, reports, data visualizations, UX polish, visual redesigns, responsive behavior, accessibility, UI performance, frontend architecture, code elegance, project quality, or file/directory structure governance. Fuses the local route-plan/DESIGN.md/browser-validation workflow with anti-slop visual judgment and Impeccable-style audit, polish, harden, optimize, detector, and live iteration practices.
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
5. `frontend-craft` references.
6. Upstream generic visual or Impeccable guidance.

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
   for read-only audit/polish/harden/optimize/structure/architecture passes,
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/frontend_craft_detect.sh`
   for detector signals, and
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/frontend_craft_score.py`
   for self-audits. When maintaining this skill repo, use
   `/Users/gaoqian/Documents/sixseven/codeproject/frontend-craft/scripts/upstream_absorption_report.py`
   before absorbing new upstream commits.
6. Implement minimally, verify with the most relevant commands, and use a real
   browser for visible UI, interaction, responsive, report, dashboard, download,
   upload, or login-state changes.

## Reference routing

Read only the references needed for the current task:

- Visual redesign, landing pages, brand pages, portfolios:
  `references/visual-judgment.md`.
- Impeccable-style command selection, audit/polish/harden/optimize/live:
  `references/impeccable-workflow.md`.
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
`visual-judgment.md`, `impeccable-workflow.md`,
`engineering-quality.md`, `performance-quality.md`,
`project-structure.md`, `report-quality.md` when reports/dashboards are in
scope, and `validation-contract.md`.

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
  user-visible.

## Delivery contract

For frontend implementation work, summarize:

- `frontend_tier` and route command used, when applicable.
- `candidate_skills` versus `selected_skills`.
- `style_authority_path` and whether it was enforced or intentionally evolved.
- Files changed and structure impact.
- Validation commands and observed results.
- Browser validation target and result, or why it was skipped.
- Performance impact and remaining risks.

Keep output concise, evidence-backed, and honest about anything not verified.
