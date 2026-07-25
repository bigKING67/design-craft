Method: design-craft critique, read-only. No files edited. No browser validation claimed.

## 1. Evidence level and score band

- **Evidence level:** L0, prompt-only static concept. Product context is known, but no screenshot, DOM, tokens, states, responsive behavior, or interaction evidence was verified.
- **Score band:** **60–72 / 100** if implemented as described.
- **Maturity read:** functional but ordinary; likely “dashboard card soup” rather than an operations decision surface.

## 2. Design read

Reading this as: **a dense revenue-operations command dashboard for ecommerce operators, restrained and enterprise-grade, optimized for deciding what account or campaign needs attention in the next hour.**

The dashboard should optimize for **triage speed**: identify the highest-risk entity, understand why it matters, compare impact, and take or route the next action.

## 3. Top hierarchy / product-fit issues

1. **P1 — Twelve equal KPI cards flatten urgency.**  
   Equal card weight makes routine totals visually compete with exceptions, risk, freshness, or owner/action state.

2. **P1 — Decorative area chart is misaligned with the job.**  
   A chart that does not answer a named operational question adds visual mass without improving the next-hour decision.

3. **P1 — Dense table may be the real work surface, but appears demoted.**  
   If operators act on accounts/campaigns, the table should become the primary exception queue, not a downstream data dump.

4. **P1 — Generic tips right rail is weak product fit.**  
   Generic advice consumes scarce horizontal space. Ops dashboards need entity-specific insight: affected account, threshold, impact, owner, and next action.

5. **P1/P2 — Missing state and trust contract.**  
   No verified loading, empty, error, stale-data, permission, long-content, focus, or responsive behavior. For revenue ops, freshness and recoverability are part of the design, not edge polish.

## 4. Concrete design moves

1. **Convert “dashboard card soup” into a decision surface.**  
   Replace the 12-card grid with: one lead operational state, a compact supporting KPI strip, an exception queue/table, and diagnostics below.

2. **Create a lead risk object.**  
   First visual focus should answer: “What needs attention now?” Example anatomy: top account/campaign at risk, revenue impact, reason, SLA/freshness, owner, and primary action.

3. **Tier KPIs by decision value.**  
   Use **lead / supporting / diagnostic** hierarchy. Every emphasized metric needs period, comparison, threshold, and semantic state. Use color only for success/warning/danger/info tokens.

4. **Make the table task-first.**  
   Reorder columns around operator scanning: account/campaign identity, status/risk, impact, reason, freshness, owner, next action. Right-align numeric values; keep decision-bearing text at a provisional **14px / 1.4** minimum.

5. **Replace the decorative chart with a diagnostic chart.**  
   Keep a chart only if it answers a named question, such as “Is today’s revenue drop isolated to one account, channel, or campaign?” Add direct labels, threshold markers, and a route back to filtered rows.

6. **Replace generic tips with an action rail or remove it.**  
   A retained rail must contain specific insights: named entity/segment, observed change or threshold, business impact, owner/next action, and direct filter/action. Otherwise, give the width back to the table.

7. **Use restrained enterprise surface grammar.**  
   Favor flat/raised surfaces, subtle dividers, token-backed semantic color, consistent radius, minimal elevation, tabular numbers, and quiet density. Avoid marketing-style hero blocks, decorative gradients, and loud cards.

8. **Define the resilient state contract before implementation.**  
   Design loading, empty, error, stale data, partial data, permission-limited, long-label, selected-row, hover, focus-visible, disabled, and keyboard states. Errors should explain recovery locally.

## 5. Verified versus unverified claims

**Verified from prompt only:**

- Surface is an internal ecommerce revenue-operations dashboard.
- Primary user is an operator deciding what needs attention in the next hour.
- Current concept includes 12 equal KPI cards, decorative area chart, dense account table, and generic tips rail.
- Style authority is restrained enterprise console, dense but calm, token-backed color only.
- No screenshot, DOM, responsive run, interaction state, or browser evidence was provided.

**Unverified / not claimed:**

- Actual visual quality, spacing, typography, contrast, color tokens, and component polish.
- Whether the table is sortable, filterable, keyboard reachable, or accessible.
- Whether KPIs have correct definitions, freshness, comparisons, thresholds, or source-of-truth alignment.
- Whether the chart is truly decorative in implementation; this is inferred from the prompt wording.
- Loading, empty, error, hover, focus, selected, stale-data, permission, and responsive behavior.
- Runtime performance, table density under real data, and browser behavior.

## 6. Minimal validation plan before implementation

1. **Decision-path validation:** with operators, confirm the top 3 next-hour decisions and the fields required to act.  
2. **Metric/data audit:** define KPI source-of-truth, freshness, thresholds, comparison periods, and anomaly rules.  
3. **Content inventory:** sample real account/campaign names, long labels, nulls, extreme values, and permission-limited rows.  
4. **Static design review:** produce one desktop mock covering normal, high-risk, empty, stale/error, and long-content states.  
5. **Accessibility checklist:** verify semantic headings, table structure, keyboard order, focus-visible, non-color-only status, and WCAG contrast.  
6. **Responsive/layout plan:** define what happens to the rail, KPI strip, filters, sticky columns, and table overflow on narrower widths.  
7. **Runtime validation later:** only after implementation, run browser checks for layout, focus, hover, table interaction, loading/error states, and representative data volume.
