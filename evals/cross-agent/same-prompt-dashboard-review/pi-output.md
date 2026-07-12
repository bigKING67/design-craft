## 1. Evidence level and score band

**Evidence level: L0 — prompt-only / description-only.**  
No screenshot, DOM, responsive behavior, focus order, hover, loading, empty, error, or token implementation was verified.

**Provisional score band: 60–74 / 100 — functional but ordinary.**  
If the described structure is accurate, this likely sits in the low-to-mid part of that band because the dashboard has the classic **dashboard card soup** problem: many modules, weak operational priority, and decoration competing with decision support. It should not be scored above 84 without fixing the flat hierarchy and validating real content/states.

---

## 2. Design read: what job the dashboard should optimize for

Reading this as: **a restrained, dense enterprise revenue-ops command center for internal ecommerce operators, optimized for deciding “which account or campaign needs attention in the next hour, why, and what action should I take?”**

The dashboard should behave less like an executive overview and more like an **exception triage surface**: priority, impact, confidence, owner, and next action should dominate.

---

## 3. Top hierarchy / product-fit issues

1. **P1 — Twelve equal KPI cards flatten operational priority.**  
   Equal size/surface weight implies equal importance. For a next-hour operator, the UI must distinguish blockers, anomalies, revenue risk, and routine totals.

2. **P1 — Decorative area chart is not tied to a decision question.**  
   A chart that does not answer “what changed, where, and what should I inspect?” becomes visual noise in a dense console.

3. **P1 — Dense account table risks becoming a data dump.**  
   If identity, status, risk, impact, trend, owner, and next action are not first-class columns, the table supports lookup more than triage.

4. **P1 — Generic right-rail tips are poor product fit.**  
   Generic advice competes with live operational signals. In this context, the rail should be contextual: exceptions, recommended actions, runbook links, or watchlist notes.

5. **P2/P1 risk — State and token discipline are unproven.**  
   For a revenue dashboard, loading, stale data, empty segments, API errors, permission limits, threshold definitions, and semantic status colors are part of the product contract, not polish.

---

## 4. Concrete design moves

1. **Replace “12 equal KPI cards” with a `lead + support + action queue` layout.**  
   One lead operational state: e.g. “Revenue at risk now,” “Accounts requiring action,” or “Campaigns outside threshold.” Supporting KPIs become a compact metric strip.

2. **Convert the top area into a decision header.**  
   Include time range, data freshness, comparison baseline, threshold logic, and primary filter scope. Every emphasized number should answer: **compared to what?**

3. **Turn the chart from decorative to diagnostic.**  
   Use it to show anomaly timing, forecast variance, spend/revenue divergence, or threshold breach. Add direct labels, event markers, and a clear takeaway caption.

4. **Promote an exception queue above or beside the table.**  
   Show the top 3–5 accounts/campaigns needing action with severity, estimated impact, cause, owner, and next step.

5. **Redesign the table as a task-first table.**  
   First columns: account/campaign identity, status/severity, revenue impact, change vs baseline, suspected cause, owner/SLA, next action. Secondary metadata can be grouped later.

6. **Use restrained enterprise density, not marketing hierarchy.**  
   Prefer compact type, tabular numbers, subtle dividers, quiet surfaces, and semantic status color only. Avoid hero cards, gradients, oversized chart drama, and decorative elevation.

7. **Replace the generic right rail with contextual operations support.**  
   Examples: “Why this is flagged,” “Recommended runbook,” “Recent changes,” “Owner notes,” “Suppressed alerts,” or “Watchlist.” If not contextual, remove it.

8. **Define resilient states before implementation.**  
   Loading skeletons for KPIs/table/chart, stale-data warning, empty “no exceptions” state, API error with retry/recovery, permission-limited rows, long account names, and keyboard/focus states.

---

## 5. Verified versus unverified claims

**Verified from prompt only:**

- Intended surface: internal ecommerce revenue-ops dashboard.
- Primary user: operator deciding account/campaign attention in the next hour.
- Current concept: 12 equal KPI cards, decorative area chart, dense account table, generic tips rail.
- Style authority: restrained enterprise console, dense but calm, token-backed color only.
- No browser, screenshot, DOM, responsive, hover, focus, loading, or error evidence exists.

**Unverified / must not be claimed:**

- Actual visual quality, spacing, typography, contrast, color use, or token compliance.
- Whether the chart is truly decorative in rendered form.
- Whether the table has sorting, filters, sticky columns, row actions, or accessible semantics.
- Whether the dashboard works on narrow screens or with long real ecommerce data.
- Whether hover, focus, keyboard, loading, empty, error, stale-data, or permission states exist.
- Any browser validation or screenshot validation.

---

## 6. Minimal validation plan before implementation

1. **Clarify the decision model.**  
   Define the top operator question, severity thresholds, revenue-risk formula, time window, and what qualifies as “needs attention now.”

2. **Inventory real data fields.**  
   Confirm available account/campaign fields: impact, trend, owner, status, cause, budget/spend, ROAS/CAC, inventory constraints, campaign changes, and freshness timestamp.

3. **Create one low-fidelity hierarchy pass.**  
   Validate lead metric, support strip, exception queue, diagnostic chart, task-first table, and contextual rail before visual polish.

4. **Test with realistic rows.**  
   Use long names, missing metrics, zero-data accounts, high/low severity, stale data, permission-limited rows, and more rows than fit onscreen.

5. **Run visual/accessibility validation only after a build exists.**  
   Required checks: desktop and narrow viewport layout, keyboard focus walk, table scanability, color contrast, semantic status not color-only, loading/empty/error states, chart labels/tooltips, and token usage.

Rules/skill used: **design-craft critique mode** and the **frontend rule**. No files were edited and no browser validation was performed.
