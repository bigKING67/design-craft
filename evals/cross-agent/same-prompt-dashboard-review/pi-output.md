## 1. Evidence level and score band

**Evidence level: L0 static / prose-only concept review.**  
Only the product context and described layout were reviewed. No screenshot, DOM, tokens, real data, responsive behavior, interaction states, accessibility, or browser runtime evidence was verified.

**Score band: 60–74 / functional but ordinary.**  
Likely in the lower half of that band if the described hierarchy is accurate: the concept sounds operationally plausible, but “12 equal KPI cards + decorative chart + dense table + generic tips” is classic dashboard card soup rather than a decision surface.

---

## 2. Design read: what job this dashboard should optimize for

**Reading this as:** a restrained enterprise revenue-ops dashboard for ecommerce operators, dense but calm, optimized for answering:  
**“Which account or campaign needs attention in the next hour, why, and what should I do next?”**

The dashboard should not optimize for broad business reporting or executive visual polish. It should optimize for **triage, exception detection, confidence, and fast handoff into action**.

---

## 3. Top hierarchy / product-fit issues

### P1 — Equal KPI grid hides operational priority
Twelve equal cards make every metric look equally urgent. For a next-hour operator, that delays the first decision: risk, opportunity, blocked spend, pacing miss, account issue, or campaign anomaly.

### P1 — Decorative area chart consumes attention without a decision role
A chart that does not answer a named operational question becomes visual noise. In this surface, a chart should explain a priority, trend break, pacing risk, or anomaly—not decorate the top of the page.

### P1 — Dense account table is probably the real work object, but it is visually demoted
If operators decide which account/campaign needs attention, the table or exception queue is likely the primary object. Putting it after undifferentiated KPIs makes the dashboard report-like instead of task-first.

### P1 — Generic right-rail tips mismatch internal ops use
Generic tips are low-trust in an enterprise console. They compete with real signals unless they name the entity, evidence, threshold, impact, owner, and next action.

### P2 — State, data-quality, and accessibility contracts are undefined
For a revenue dashboard, loading, stale data, missing metrics, permission-limited rows, error states, focus order, keyboard table use, semantic status color, and metric source-of-truth are not polish; they are trust infrastructure.

---

## 4. Concrete design moves

1. **Convert “dashboard card soup” into a decision surface.**  
   Use a top command/context band: date range, data freshness, account scope, channel filter, and last sync status.

2. **Replace 12 equal KPI cards with a lead/support hierarchy.**  
   Promote 1–2 lead operational states, such as “Accounts needing action now” or “Campaigns pacing outside threshold.” Move the rest into a compact supporting metric strip.

3. **Create an exception queue above or alongside the table.**  
   Show ranked items by severity, revenue impact, confidence, and owner/action. The first screen should answer “what should I inspect first?”

4. **Make the table task-first, not schema-first.**  
   Order columns as: identity → status/risk → impact → reason → next action → owner → supporting metrics. Right-align numeric values; use tabular numbers; keep filters adjacent to the table.

5. **Demote or replace the decorative chart with diagnostic evidence.**  
   Retain a chart only if it answers a named question, e.g. “Which campaigns broke pacing in the last 6 hours?” Add direct labels, threshold lines, and a linked row/detail path.

6. **Replace generic tips with evidence-backed operational insight cards.**  
   Each insight must include entity, observed change, threshold or comparison, business impact, and recommended next action. Otherwise remove the rail.

7. **Use restrained enterprise surface treatment.**  
   Prefer subtle dividers, compact spacing rhythm, semantic status color, and token-backed surfaces over heavy cards, arbitrary accents, gradients, or marketing hero scale.

8. **Design resilient states as component contracts.**  
   Define loading, empty, stale, partial-data, permission-denied, error, long-label, dense-row, selected-row, hover, focus-visible, and keyboard states before implementation.

---

## 5. Verified versus unverified claims

**Verified from prompt:**
- The intended user is an internal ecommerce revenue-ops operator.
- The primary decision window is the next hour.
- The current concept uses 12 equal KPI cards, a decorative area chart, dense table, and generic right rail.
- The style target is restrained enterprise console with token-backed color.

**Not verified:**
- Actual visual quality, spacing, typography, contrast, or token use.
- Whether the KPI cards have comparisons, thresholds, owners, or semantic status.
- Whether the chart is truly decorative in implementation.
- Table column order, sort/filter behavior, keyboard support, sticky headers, row actions, or virtualization.
- Loading, empty, error, stale-data, permission, hover, focus, selected, and responsive states.
- Metric definitions, source-of-truth, freshness, duplicate/missing account mapping, or filter correctness.
- Accessibility, screen-reader semantics, focus order, color contrast, or reduced-motion behavior.
- Browser/runtime behavior; no browser validation was performed.

---

## 6. Minimal validation plan before implementation

1. **Decision-task validation:** give 3–5 operators realistic data and ask them to identify the top account/campaign needing action in under 3 minutes.

2. **Metric source-of-truth check:** confirm canonical definitions for each KPI, freshness timestamp, account/campaign joins, missing records, duplicate entities, and filtered-out entities.

3. **Information hierarchy test:** compare current equal-card layout against a lead metric + exception queue + task-first table layout.

4. **Real-data stress pass:** test long account names, many campaigns, zero results, stale data, partial API failure, negative/positive deltas, and permission-limited rows.

5. **Accessibility pass:** verify keyboard table navigation, visible focus, semantic labels, non-color-only status, contrast, and screen-reader order.

6. **Responsive/browser validation:** after implementation only, verify desktop and narrower widths in browser with actual rendered tokens, table overflow behavior, chart labels/tooltips, and state variants.

No files were edited, and no browser validation is claimed.
