# Design-Craft Critique — Revenue Operations Dashboard

**Mode:** `critique` (read-only, no file edits, no browser validation claimed)
**Method:** single-context (prose concept description only)
**Evidence level:** L0 static — prose description, no screenshot, DOM, responsive, focus walk, hover state, loading, empty, or error state verified
**Style authority:** prompt-described ("restrained enterprise console, dense but calm, no marketing hero treatment, token-backed color only")

---

## Design Read

> **Reading this as:** enterprise revenue operations dashboard for an internal ecommerce operator, with restrained/calm console density, optimized for *triaging which account or campaign needs attention in the next hour* — but the current visual structure buries the triage decision behind equal-weight decoration and non-decision content.

---

## Overall Score

**Score: 72 / 100**
**Design maturity band: Functional but ordinary (60–74)**

### Why this score

| Signal | Impact |
|---|---|
| **−** 12 equal KPI cards enforce zero priority hierarchy — the operator's core job is flatlined | Major deduction (card soup, P1) |
| **−** Decorative area chart consumes space but answers no operational question | P1 structural waste |
| **−** Generic tips rail occupies premium right-column real estate with no triage value | P1 misallocation |
| **−** Dense account table (the only decision-surface object) is buried *below* decoration and equal-weight metrics | P1 inverted information order |
| **−** No exception queue, anomaly callout, or "needs attention" signal — the exact thing the operator needs is absent | P0 task-focus failure |
| **+** Token-backed color discipline and restrained enterprise tone are explicitly stated as the design authority | Calms the visual noise risk |
| **+** A dense table exists, which *is* the right object for account-level triage — it’s just in the wrong position | Positive latent structure |
| **Not scored as verified:** hover, focus, active, disabled, loading, empty, error, success states; responsive behavior; real-content overflow; keyboard accessibility; screen-reader labels; motion; color contrast ratios; token implementation fidelity. All claimed at L0 only. | |

### Anti-inflation guard

The 12 equal KPI cards are the **textbook definition of card soup** (design-move-library: "All KPI cards have equal size, color, and surface weight"). Per `taste-score-calibration.md`: *Do not score above 84 when the main issue is a flat hierarchy or card soup.* The score is further constrained below 78 because the decorative chart and generic tips rail push the surface past "clean but generic" into "actively misaligned with the primary user job."

---

## Top Hierarchy / Product-Fit Issues

| Priority | Location | Category | Problem | Why It Hurts |
|:---|:---|:---|:---|:---|
| **P0** | Entire surface | Task focus | No exception/anomaly/attention signal exists. The operator's explicit job — "decide which account needs attention in the next hour" — has no visual answer on the page. | Operator cannot complete the primary task without decoding 12 equal cards and scanning a dense table manually. |
| **P1** | Top section | Information order, contrast | 12 equal KPI cards. All metrics share the same visual weight, size, surface treatment, and emphasis regardless of risk, trend, or operational urgency. | Positive, negative, warning, and neutral states are indistinguishable. The highest-risk metric looks identical to a benign total. |
| **P1** | Mid section | Composition | Decorative area chart. The prompt itself calls it "decorative" — it answers no analytical question about accounts, campaigns, revenue anomalies, or triage. | Prime vertical space used for ornamentation in a surface where every pixel should serve the decision path. |
| **P1** | Right rail | Task focus, contrast | Generic tips rail. Advice content has no operational relationship to the accounts or campaigns the operator needs to triage. | Wastes the most scannable sidebar real estate on non-decision content; competes for visual attention with the table. |
| **P1** | Below fold | Information order | Dense account table placed after cards + chart + tips rail. This is the only object where the operator can actually *decide*, but it arrives last in the scan path. | Continuity principle violated: summary → decoration → tips → decision makes no cognitive flow. |
| **P2** | Table | Repetition | Schema-order columns (implied by "dense" + no task-first restructuring). Columns likely follow database field order rather than triage order. | Operator must decode horizontally to find status, risk, and next-action columns. |
| **P2** | KPI cards | Alignment, repetition | 12 cards naturally invite alignment drift, inconsistent padding, mismatched label lengths, and varying delta/trend treatments unless rigorously templated. | Without a shared `KpiCard` anatomy and strict token boundary, the grid drifts toward "assembled" rather than "composed." |

---

## Concrete Design Moves

Using design-craft vocabulary and the **dashboard card soup → decision surface** move family from `design-move-library.md`, treatment variant: **Ops command center** (blocker-first hierarchy, high-contrast exceptions, queue/action rail, short labels, strong state semantics).

### Move 1: Card soup → priority hierarchy (P0 + P1)

**Before:** 12 equal KPI cards in a flat grid.
**After:** Split into three tiers with distinct visual weight:

1. **Lead risk object** (one dominant module at top-left): the single most urgent metric — e.g., "Accounts at risk (3)" — with trend sparkline, time window, and a direct link to the filtered table below. Occupies ~2× the width of a standard KPI card. Uses the project's semantic warning/danger token only when the threshold is breached.
2. **Supporting metric strip** (compact row of 4–5 secondary KPIs): revenue, margin, order volume, conversion rate. Each shows value + delta + period. Smaller type, flatter surface, no card elevation — a tight horizontal band, not a grid of equal boxes.
3. **Diagnostic metric drawer or collapsed row** for the remaining 6–7 metrics. Disclosed on demand or tucked into a compact secondary row below the fold. These are inspection metrics, not triage metrics.

**Acceptance criteria:** Operator can identify the highest-risk metric within 3 seconds. Positive/negative/warning states are visually distinct without relying solely on color.

### Move 2: Decorative chart → diagnostic chart (P1)

**Before:** Area chart that the prompt itself calls "decorative."
**After:** Replace with a chart that answers *one* operational question directly relevant to triage. Candidates:
- "Revenue anomaly timeline" (highlighting deviations from expected range per hour/day)
- "At-risk account count trend" (30-day rolling, with threshold annotation)
- "Campaign performance variance" (actual vs. target with tolerance band)

**Implementation discipline:** Label axes directly (no legend-only decoding). Use the project's semantic status palette for above/below-threshold regions. Keep tooltips compact with decision-relevant data (account name, delta, action link), not raw series names.

**Acceptance criteria:** The chart answers a named analytical question. Anomalous data points are visually distinct and link to the filtered table.

### Move 3: Generic tips rail → action queue / priority alerts (P1)

**Before:** Right rail with generic tips.
**After:** Convert to an **exception queue** or **action rail** — the operator's "what needs attention" surface:

- **Priority alerts** (top): accounts/campaigns breaching thresholds, sorted by severity. Each row: account name, metric at risk, delta, time since alert, and a one-click filter action on the table below.
- **Pending actions** (mid): operator-owned tasks (approvals, reviews, escalations).
- **Recent activity** (bottom, compact): last 3–5 triage actions taken by the team.

**Surface treatment:** Use the project's raised surface token for the rail container, but keep internal rows flat (dividers, not nested cards). Use semantic status color sparingly — only on the severity indicator, not the entire row.

**Acceptance criteria:** The rail contains only operational decision content. No generic advice. Every row links to a filterable action on the main table.

### Move 4: Table repositioning and task-first columns (P1 + P2)

**Before:** Dense table below all decoration, schema-order columns.
**After:**

1. **Position:** Table moves to center stage, directly below the lead metric + strip + diagnostic chart. It is the primary decision surface and should occupy the main content column, not compete with a tips rail.
2. **Column order (task-first):** Account identity → Status (active/at-risk/paused) → Risk indicator → Revenue impact ($) → Trend (sparkline or delta) → Next action (button or link). Metadata columns (region, manager, created date, last contact) move to a right-side cluster or are disclosed on row expand.
3. **Row hierarchy:** At-risk rows get a subtle left-border accent (semantic danger/warning token) and sort to the top by default. Healthy rows use the default surface treatment.
4. **Empty/loading/error states** scoped to the table region, not a page-level spinner.

**Acceptance criteria:** Operator can scan identity → status → risk → next action without horizontal scrolling. At-risk rows are sorted first. Long account names truncate with tooltip. Narrow viewport gracefully collapses metadata columns.

### Move 5: Layout restructure (P1)

**Before:** 12 cards → decorative chart → table || tips rail.
**After (proposed page grammar):**

```
┌──────────────────────────────────────────────────┐
│  Page header: title, time range selector, export  │
├──────────────────────────┬───────────────────────┤
│ Lead risk object (2col)  │  Exception queue      │
│ + Supporting metric      │  • Alert 1 (severity) │
│   strip (compact row)    │  • Alert 2            │
│                          │  • Alert 3            │
│ Diagnostic chart         │  Pending actions      │
│ (answers one question)   │  Recent activity      │
├──────────────────────────┴───────────────────────┤
│  Account table (task-first columns, at-risk      │
│  rows sorted to top, filters adjacent to data)   │
└──────────────────────────────────────────────────┘
```

This preserves the restrained enterprise tone (no hero treatment, token-backed color) while replacing decoration with operational signal density.

---

## Verified vs. Unverified Claims

### Verified (by prompt only)

- ✅ 12 equal KPI cards exist — self-declared in the prompt.
- ✅ Decorative area chart exists — self-declared in the prompt.
- ✅ Dense account table exists.
- ✅ Generic tips rail exists.
- ✅ Style intent: restrained enterprise console, token-backed color.

### Unverified (claimed but not confirmed)

| Claim | Why unverified | Risk if false |
|---|---|---|
| "Token-backed color only" | No DESIGN.md, token file, or CSS variable dump inspected. Hard-coded hex values unknown. | Color may contain untracked one-offs that drift from the restrained intent. |
| All 12 cards share equal visual weight | No screenshot or DOM. "Equal KPI cards" could mean equal conceptual role but slightly varied size. | If cards already have some priority differentiation, the scoring is conservative. |
| Table is truly dense and useful | No row count, column count, or sample data. "Dense" could mean noisy rather than information-rich. | The table might need its own redesign prior to repositioning. |
| No loading/empty/error states exist | Implied by omission in the prompt, not confirmed. | If these states are actually designed, polish is higher than scored. |
| No focus-visible, hover, or keyboard behavior | L0 evidence cannot verify interaction states. | Accessibility baseline unknown. |
| Responsive behavior | No viewport testing. A 3-column layout with right rail likely breaks on narrow screens. | Mobile/tablet operator scenario unaddressed. |
| Chart is truly decorative | Prompt self-describes it as "decorative." But decorative is a judgment, not a fact. The chart might carry implicit meaning the prompt author dismissed. | If the chart answers a real question, the score is slightly low. |

---

## Minimal Validation Plan (Before Implementation)

Per `validation-contract.md`, the absolute minimum before any implementation work:

### 1. Capture current-state screenshot (L0 → L1)
- **Tool:** any browser screenshot at 1440×900 viewport.
- **What to capture:** the full dashboard showing all 12 cards, chart, table, and tips rail.
- **Purpose:** establishes baseline layout truth — confirms actual card sizes, spacing, chart type, column count, and whether the "dense" table is scannable or noisy.

### 2. Real-content stress test
- Load the dashboard with **real production data** for a known bad hour (e.g., 3 accounts at risk, 1 campaign failing).
- Ask: *Does the operator see the 3 at-risk accounts within 3 seconds?* If yes, the current structure works better than this critique assumes. If no, the P0 finding is confirmed.

### 3. Operator task walk
- Observe one operator performing their actual triage workflow on the current dashboard.
- Record: first thing they look at, first click, time to decision, and any manual scanning they do to compensate for missing hierarchy.
- This directly validates or refutes the "no exception surface" P0 finding.

### 4. State inventory (L0 → L2)
- Manually trigger and screenshot: **empty state** (no accounts), **loading state** (initial fetch), **error state** (API failure), and **all-normal state** (no accounts at risk).
- Catalog which states are designed vs. which are browser-default spinners or blank containers.
- This determines whether state-work is a polish task or a build-from-scratch task.

### 5. Token audit (if DESIGN.md or CSS variable file exists)
- Run `design_craft_token_audit.py` or manual grep for hard-coded hex values.
- Confirm that the "token-backed color only" claim holds.
- If tokens don't exist, they need to be established before any visual restructuring.

### Gate before implementation
- **Do not restructure** until the current-state screenshot and real-content test confirm that the operator is not already served by the existing layout.
- **Do not polish** until the state inventory confirms which loading/empty/error variants need to be built.
- **Do not finalize score** without at least one screenshot artifact (L1 minimum).

---

## Summary

| Field | Value |
|---|---|
| Evidence level | L0 static (prose only) |
| Score | 72 / 100 |
| Band | Functional but ordinary |
| Primary diagnosis | Card soup + decorative chart + non-operational rail bury the only decision surface (the table), and no exception signal exists for the operator's explicit triage job |
| P0 issues | 1 (no anomaly/attention surface) |
| P1 issues | 4 (card soup, decorative chart, generic tips rail, inverted information order) |
| P2 issues | 2 (schema-order columns, card alignment drift risk) |
| Validated claims | 5 (prompt-self-declared only) |
| Unverified claims | 7 (states, responsive, interaction, tokens, real content, chart intent, table quality) |
| Design authority | Enforced as stated — restrained enterprise console, token-backed color, no hero treatment |
| Recommended treatment variant | Ops command center (blocker-first, exception queue, short labels, strong state semantics) |
| Next step | Capture screenshot → real-content stress test → operator task walk → state inventory → redesign, not before |
