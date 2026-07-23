## 1. Evidence level and score band

**Evidence level: L0 static / prompt-only concept.**  
No screenshot, DOM, responsive run, focus walk, hover/loading/error verification, or real data sample was checked.

**Score band: ~60–70 / 100 — “functional but ordinary.”**  
The concept has recognizable dashboard parts, but the described hierarchy is “dashboard card soup,” not an hour-by-hour revenue operations decision surface. Score is capped because runtime states, data density, accessibility, and visual execution are unverified.

## 2. Design read

**Reading this as:** an enterprise ecommerce revenue-ops dashboard for internal operators, dense but calm, optimized for **deciding which account or campaign needs attention in the next hour**.

The dashboard should optimize for **triage speed**: detect the highest-impact exception, understand why it matters, and take or route the next action.

## 3. Top hierarchy / product-fit issues

1. **P1 — No operational focal point.**  
   Twelve equal KPI cards make routine totals visually equal to urgent revenue risk. The first scan does not answer “what needs attention now?”

2. **P1 — KPI hierarchy is flat and under-contextualized.**  
   KPIs need comparison, threshold, time window, owner, and semantic state. Equal cards without “compared to what?” encourage passive monitoring, not action.

3. **P1 — Decorative area chart misuses analytical space.**  
   A chart in this context must answer a named ops question: pacing risk, spend efficiency anomaly, conversion drop, margin leakage, inventory constraint, etc. Decorative trend art is noise.

4. **P1 — Dense table may be a data dump rather than a task-first table.**  
   If account/campaign identity, risk, impact, status, owner, and next action are not first-class, operators must decode instead of decide.

5. **P1/P2 — Generic tips rail is low-trust.**  
   A right rail should not contain generic advice. In an ops console, it should either become an exception/action rail with evidence or disappear to preserve table width.

## 4. Concrete design moves

1. **Replace the top card grid with a lead decision object.**  
   Example anatomy: “Top revenue risk now,” affected account/campaign, estimated impact, cause signal, freshness, owner, and primary next action.

2. **Convert 12 KPIs into a compact supporting metric strip.**  
   Group by decision tier: revenue pacing, spend efficiency, conversion health, margin/fulfillment constraints. Use tabular numerals, deltas, thresholds, and semantic state color only.

3. **Add a command/context band above the decision surface.**  
   Include time window, market/store scope, currency, data freshness, active filters, and last refresh. This prevents metric ambiguity.

4. **Turn the area chart into a diagnostic chart.**  
   It should answer one explicit question, e.g. “Revenue pacing vs target by hour,” “ROAS anomaly by campaign,” or “Spend up / orders down divergence.” Use direct labels and restrained enterprise chart color.

5. **Promote an exception queue near the top.**  
   Show the next 5–10 accounts/campaigns needing attention, ranked by impact × urgency. This is the operating surface, not a sidebar novelty.

6. **Rework the table as a task-first table.**  
   First columns: identity, status/risk, impact, reason, owner, next action. Push metadata later. Right-align numeric columns, keep filters adjacent to affected data, support sorting by urgency and revenue impact.

7. **Replace generic tips with evidence-backed insights or remove the rail.**  
   Keep an insight only if it names entity, observed change, threshold/baseline, business impact, and action/owner.

8. **Define resilient state contracts before implementation.**  
   Loading, empty, error, stale data, permission-limited, long account names, zero values, delayed metrics, disabled actions, focus-visible, and keyboard navigation need designed treatments.

## 5. Verified versus unverified claims

**Verified from prompt only**
- Dashboard concept includes 12 equal KPI cards, decorative area chart, dense account table, and generic tips rail.
- Product context is internal ecommerce revenue operations.
- Primary user needs next-hour attention decisions.
- Style authority is restrained enterprise console, dense but calm, token-backed color only.

**Unverified / must not be claimed**
- Actual visual quality, spacing, typography, contrast, color token usage, or surface treatment.
- Whether the table has usable sorting/filtering, sticky columns, row actions, or numeric alignment.
- Accessibility: keyboard order, focus-visible states, labels, contrast, screen-reader semantics.
- Responsive behavior, overflow, long labels, chart tooltip clipping, or mobile/narrow layout.
- Loading, empty, error, stale, disabled, hover, active, selected, or permission states.
- Browser/runtime performance or perceived scan speed.

## 6. Minimal validation plan before implementation

1. **Product/data validation**
   - Confirm the top 3 operator decisions made in the next hour.
   - Define source-of-truth metrics, freshness expectations, thresholds, and owner/action rules.

2. **Information architecture prototype**
   - Test lead object + support strip + exception queue + task-first table against realistic account/campaign data.
   - Validate that the top action is identifiable within ~3 seconds.

3. **Visual/design-system check**
   - Map typography, spacing, surfaces, borders, and semantic colors to existing tokens.
   - Verify dense enterprise treatment without marketing hero styling.

4. **State and content stress cases**
   - Long names, missing owner, stale data, zero revenue, delayed metrics, empty queue, API error, partial permissions.

5. **Runtime/browser validation later, not claimed here**
   - Desktop and narrow responsive pass.
   - Keyboard/focus walk.
   - Chart label/tooltip overflow.
   - Table scrolling, sorting, filtering, and row-action behavior.
