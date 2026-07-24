## 1. Evidence level and score band

- **Evidence level:** **L0 static / prose-only**, with useful product context. Not L1+ because no screenshot, DOM, tokens, responsive run, interaction states, or browser evidence were verified.
- **Score band:** **60–74: functional but ordinary**. If the described structure is accurate, likely **mid/high 60s**: usable ingredients, but the hierarchy sounds like dashboard card soup rather than an hourly decision surface.
- **Score ceiling from evidence:** I would not score above **74** without seeing real visual hierarchy, data density, states, accessibility, and responsive behavior.

## 2. Design read: optimized job

Reading this as: **a restrained enterprise “Operate” dashboard for ecommerce revenue operators, dense but calm, optimized for deciding which account or campaign needs attention in the next hour.**

The screen should not primarily optimize for “show me everything.” It should optimize for:  
**What is abnormal, why it matters, who/what owns it, and what action should happen next?**

## 3. Top hierarchy / product-fit issues

1. **P1 — Flat KPI grid dilutes operational priority.**  
   Twelve equal KPI cards imply twelve equal decisions. For an hourly operator, this creates scan tax and hides the urgent entity or threshold breach.

2. **P1 — Decorative chart is probably occupying premium attention without answering a question.**  
   An area chart only earns top placement if it explains a decision: anomaly, pacing risk, revenue drop, spend inefficiency, or forecast gap.

3. **P1 — Dense table risks becoming a data dump instead of a task-first queue.**  
   The table should lead with account/campaign identity, status, risk, impact, owner/SLA, and next action—not schema-order metrics.

4. **P1 — Generic right-rail tips are weak product fit.**  
   For revops, advice must be evidence-backed and entity-specific. Generic tips feel like decoration disguised as intelligence.

5. **P1/P2 — State, accessibility, and responsive resilience are unknown.**  
   Loading, empty, error, permission, stale-data, long-label, focus, keyboard, and narrow-width states are unverified; for an internal ops dashboard, these are part of trust, not polish.

## 4. Concrete design moves

1. **Dashboard card soup → decision surface.**  
   Replace the 12-card opening with: **lead operational state + compact supporting metric strip + exception queue**.

2. **Flat KPI grid → priority hierarchy.**  
   Promote 1–2 lead metrics tied to the next-hour job: e.g. “accounts needing action,” “revenue at risk,” “campaigns overspending,” or “SLA breaches.” Demote routine totals into a smaller metric band.

3. **Make every metric comparative.**  
   Each KPI needs period, benchmark, threshold, and semantic state: “vs last hour,” “vs target,” “outside guardrail,” “owner required.” Use color only for semantic status.

4. **Convert the right rail into an action/insight rail.**  
   Keep an insight only if it names **entity + observed change + business impact + recommended next action / owner**. Otherwise remove it.

5. **Reframe the chart as diagnostic evidence.**  
   Move it below the lead decision area unless it directly explains the top anomaly. Add takeaway label, marked threshold/event, accessible legend, and clear time range.

6. **Table as data dump → task-first table.**  
   First columns should support scanning: account/campaign, status/risk, impact, trend, owner, next action. Right-align numeric columns; group secondary metadata later.

7. **Create a density gradient.**  
   Calm enterprise does not mean uniformly dense. Use stronger hierarchy at the top, compact support metrics, then dense rows. Reserve heavy surfaces/elevation for true priority.

8. **Define the resilient state contract before implementation.**  
   Loading, stale data, no exceptions, API error, partial data, permission-limited rows, long names, selected/sorted/filter-active, keyboard focus, and reduced-motion paths should be designed with token-backed states.

## 5. Verified versus unverified claims

**Verified from prompt only:**

- Surface is an internal ecommerce revenue operations dashboard.
- Primary user decides which account/campaign needs attention in the next hour.
- Current concept includes 12 equal KPI cards, decorative area chart, dense table, and generic tips rail.
- Style authority is restrained enterprise console, dense/calm, token-backed color, no marketing hero.

**Not verified:**

- Actual visual quality, spacing, typography, color, contrast, or token usage.
- Whether the KPI cards are truly equal in rendered weight.
- Whether the chart is inaccessible or merely decorative in implementation.
- Table column order, sorting/filtering behavior, keyboard reachability, sticky behavior, or row actions.
- Hover, focus, loading, empty, error, long-content, stale-data, or responsive behavior.
- Browser performance, DOM structure, chart tooltip behavior, or screen-reader semantics.

## 6. Minimal validation plan before implementation

1. **Product validation:** define the top five “needs attention in next hour” scenarios and rank the required signals/actions.
2. **Content/data audit:** map each KPI, chart, table column, and rail insight to a decision; remove or demote anything without a decision role.
3. **Static design review:** produce desktop and narrow-width mocks with real account/campaign names, long labels, empty/error/loading/stale states.
4. **Accessibility pass:** verify contrast, semantic status beyond color, focus order, table semantics, keyboard row actions, and screen-reader labels.
5. **Browser validation later, not claimed here:** check rendered desktop/narrow layouts, table overflow, tooltip clipping, sticky controls, focus walk, and loading/error state behavior.
