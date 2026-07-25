## 1. Evidence level and score band

- **Evidence level: L0 static / prompt-only concept.**
- **Score band if implemented literally: 60–74, “functional but ordinary.”**
- Could fall below that if dense table behavior, data freshness, accessibility, or error states are weak. No precise score is defensible without a screenshot, DOM, real data, or interaction evidence.

## 2. Design read

Reading this as: **an enterprise revenue-ops command surface for ecommerce operators**, restrained and dense, optimized for **deciding which account or campaign needs attention in the next hour, why, and what to do next**.

The dashboard should behave less like a KPI gallery and more like an **attention triage surface**.

## 3. Top hierarchy / product-fit issues

1. **P1 — 12 equal KPI cards flatten operational priority.**  
   Equal card weight creates “dashboard card soup”: routine totals, risk signals, and urgent exceptions all compete equally.

2. **P1 — Decorative chart is misfit for the job.**  
   An area chart that does not answer a named operational question consumes attention without improving the next-hour decision.

3. **P1 — Primary work object is likely buried.**  
   For this user, the account/campaign table or exception queue is probably the decision surface. Placing it after KPI cards and chart delays action.

4. **P1 — Generic tips rail weakens trust.**  
   A right rail with generic advice feels like SaaS decoration. Rev-ops operators need evidence, ownership, thresholds, and next actions.

5. **P0/P1 risk — State and data contracts are unspecified.**  
   The prompt does not define freshness, metric source-of-truth, loading, empty, stale, error, permission, or long-data behavior. For revenue operations, that is not polish; it affects safe use.

## 4. Concrete design moves

1. **Dashboard card soup → decision surface.**  
   Replace the 12-card grid with: one lead operational state, a compact supporting KPI strip, and an exception/action queue above the fold.

2. **Flat KPI grid → priority hierarchy.**  
   Split metrics into **lead / supporting / diagnostic** tiers. Every emphasized number needs period, comparison, threshold, and semantic state.

3. **Promote an exception queue.**  
   Add a top module such as “Needs attention now” ranked by revenue impact, risk, SLA breach, anomaly severity, or owner. This should answer: *who needs action first?*

4. **Task-first table.**  
   Reorder columns around operator scanning: account/campaign identity, status/risk, revenue or spend impact, cause, owner, last change, next action. Right-align numeric columns and keep filters adjacent to the affected table.

5. **Turn the right rail into contextual evidence.**  
   Replace generic tips with selected-row detail, anomaly explanation, recommended action, owner, escalation path, or recent changes. If it cannot be contextual, remove it.

6. **Make charts analytical, not decorative.**  
   Keep a chart only if it answers a named question, e.g. “Which campaigns are driving revenue risk over the last 24h?” Use direct labels, thresholds, annotations, and accessible semantic color.

7. **Use restrained enterprise density.**  
   Favor compact type, subtle dividers, tabular numbers, calm spacing rhythm, and token-backed surfaces. Use color only for semantic status: warning, danger, success, neutral, info.

8. **Design the state matrix before visual polish.**  
   Specify loading, empty, stale data, API failure, permission-limited data, long labels, many campaigns, zero revenue, negative deltas, and delayed metric refresh.

## 5. Verified versus unverified claims

**Verified from prompt only:**

- Surface is an internal ecommerce revenue-ops dashboard.
- Primary user is an operator making next-hour attention decisions.
- Current concept has 12 equal KPI cards, decorative area chart, dense table, and generic tips rail.
- Style authority is restrained enterprise console, token-backed color, no marketing hero treatment.
- No screenshot, DOM, runtime, responsive, focus, hover, loading, or error evidence was provided.

**Unverified and should not be claimed:**

- Actual visual polish, contrast, typography, spacing, or token compliance.
- Whether the table is scannable with real account/campaign data.
- Whether keyboard flow, focus states, hover states, tooltips, sorting, filters, or row actions work.
- Whether KPI definitions, data freshness, duplicate/missing records, or metric source-of-truth are correct.
- Whether the chart is truly decorative in implementation beyond the stated concept.
- Responsive behavior, performance under dense data, and accessibility compliance.

## 6. Minimal validation plan before implementation

1. **Metric/source-of-truth audit:** define each KPI, freshness, time window, owner, threshold, and affected downstream reports.  
2. **Real-data content pass:** test with representative accounts, campaigns, long names, zero/negative values, missing data, and high-volume rows.  
3. **Operator triage test:** with 3–5 operators, verify they can identify the top action and reason within 3 seconds.  
4. **State matrix review:** loading, empty, error, stale, permission-limited, and partial-data states for cards, chart, table, and rail.  
5. **Accessibility pass:** keyboard order, visible focus, semantic table structure, non-color-only status, contrast, and screen-reader labels.  
6. **Responsive/density check:** desktop primary, narrower laptop viewport, horizontal overflow behavior, sticky headers/filters, and long-content degradation.  
7. **Performance risk check:** table rendering, sorting/filtering latency, chart redraw cost, and update frequency under realistic row counts.
