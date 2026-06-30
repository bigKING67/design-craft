# Impeccable-style workflow fusion

Use this for command selection and quality passes inspired by Impeccable while
remaining inside this user's local Codex workflow.

## Mode selection

- `shape`: plan UX/UI before code. Use when the feature is vague, the audience
  or job is unclear, or multiple design directions are plausible.
- `craft`: full build flow. Use for new pages, new major components, or new
  feature surfaces that require discovery, implementation, and browser
  iteration.
- `critique`: evaluate whether the UI feels right. Use for heuristic review
  when code changes are not yet requested.
- `audit`: measurable quality check. Use for accessibility, responsiveness,
  performance, theming, and anti-patterns.
- `polish`: final refinement on a functionally complete UI.
- `harden`: real-world resilience: error states, loading states, long text,
  empty states, i18n, permissions, offline, overflow, slow networks.
- `adapt`: make a good design work in another viewport or context.
- `optimize`: performance diagnosis and fixes; measure first.
- `extract`: consolidate repeated UI patterns into tokens/components only
  after repeated real use.
- `document`: capture or update `DESIGN.md` only when the user approves style
  authority evolution.
- `live`: iterate in browser when visual choice is hard to judge from source.

## Shape brief

For nontrivial design work, capture:

- Purpose: what the surface exists to do.
- User: who is using it and under what pressure.
- Content/data: realistic data ranges, empty states, edge cases.
- Primary decision/action: what must become easier.
- Constraints: accessibility, brand, framework, device, deadline.
- Anti-references: what the design must avoid.

Do not over-interview. Ask only if a missing answer changes implementation.

## Critique pass

Use `critique` for a read-only judgment pass before implementation or when a UI
"feels off" but the fix is not yet obvious. It should produce:

- A one-line design read: surface, audience, vibe, primary job.
- Product-fit verdict: what decision or action is clearer or still buried.
- Visual-fit verdict: hierarchy, density, typography, color intent, motion.
- Generic-output verdict: AI tells, nested-card soup, fake polish, vague copy.
- Top P0/P1/P2/P3 issues and the recommended next mode.

If the user asks for a score, why the UI is not full marks, or a concrete
product UI review, read `product-ui-taste-review.md` and use its 100-point
output contract. Keep that score scoped to the reviewed UI, not this
`frontend-craft` repo.

For a full unanchored critique of a viewable target, include method provenance
in the first line:

- `Method: dual-agent (A: <id> · B: <id>)` when independent design review and
  detector/browser evidence were actually delegated.
- `DEGRADED: single-context (<reason>)` when the review could not use isolated
  assessment contexts but still continues.

Do not claim dual-agent, browser overlay, or detector evidence unless those
steps actually ran. For lightweight inline critiques, say the assessment was
single-context instead of silently implying independent review.

Do not turn critique into implementation unless the user asks for changes.

## Audit dimensions

Score mentally or explicitly across:

1. Accessibility: contrast, labels, semantics, keyboard, focus, reduced motion.
2. Performance: Web Vitals, render hot paths, assets, bundle, animation cost.
3. Theming: token use, dark/light parity, hard-coded colors, radius/shadow
   drift.
4. Responsive: layout, overflow, touch targets, mobile viewport behavior.
5. Anti-patterns: generic AI tells, over-decoration, nested cards, poor
   hierarchy.

Severity:

- P0: blocks release or data/task completion.
- P1: should fix in this change if in scope.
- P2: schedule soon; acceptable with explicit risk.
- P3: polish backlog.

## Polish pass

Polish only after the UI works. Check:

- Alignment and spacing.
- Typography hierarchy and line lengths.
- Token consistency and contrast.
- Hover/focus/active/disabled/loading/error/success states.
- Motion easing and reduced-motion fallback.
- Copy voice and placeholder removal.

Do not turn polish into a redesign unless the user asked for redesign.

## Harden pass

Use realistic hostile data:

- 1, 20, 60, 200 character names/titles.
- Missing optional fields.
- Empty lists and first-run states.
- 4xx/5xx/network timeout.
- Permission denied and unauthenticated.
- Long translations and RTL if layout risk is high.
- Large numbers, long currency formats, and 1000+ item lists.

Fix with flexible layout, overflow handling, tooltips/disclosures where useful,
clear error UI, bounded lists, pagination/virtualization, and explicit states.

## Optimize pass

Measure or establish a baseline first. Then target:

- LCP: images, fonts, render-blocking assets, server latency.
- INP: expensive handlers, unnecessary renders, heavy effects.
- CLS: missing dimensions, late content, unstable layout.
- Bundle: unused imports, oversized libraries, missing splitting.
- Animations: layout properties, paint-heavy effects, overuse of `will-change`.

Roll back changes that do not improve the target metric or simplify the code.

## Detector usage

If the source repo is available, the upstream detector can be run manually from
the project root:

```bash
node upstreams/impeccable/skill/scripts/detect.mjs --json <target>
```

In normal user projects, prefer local project validation first. Treat detector
findings as signals, not law. Project `DESIGN.md` can intentionally allow
patterns that generic detector rules dislike; document such exceptions.
