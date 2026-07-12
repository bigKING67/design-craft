## 1. Evidence level and score band

**Evidence level: L0 static / prose-only.**  
The prompt provides product context and a structural description, but no screenshot, DOM, token evidence, responsive run, focus walk, or state verification. This is **not browser-validated**.

**Score band: 60–74 / functional but ordinary.**  
Likely in the **low-to-mid 60s** if the described hierarchy is literal. I would cap it below 75 because the concept sounds like dashboard “card soup”: many equal KPI cards, decorative charting, dense table, and generic advice instead of an operational priority surface.

---

## 2. Design read

Reading this as: **a restrained enterprise revenue-ops command dashboard for ecommerce operators, optimized for deciding which account or campaign needs attention in the next hour.**

The job is not to summarize everything evenly. It should answer, fast:

- What needs attention now?
- Why is it urgent?
- What is the revenue/spend impact?
- Who or what is affected?
- What action should the operator take next?

---

## 3. Top hierarchy / product-fit issues

1. **Equal KPI grid weakens operational priority.**  
   Twelve same-weight KPI cards force the operator to interpret the page instead of being guided to the next action.

2. **Decorative area chart is a product mismatch.**  
   A chart on this surface must answer a triage question: anomaly, trend break, budget burn, ROAS drop, revenue at risk. If it is only decorative, it steals attention from action.

3. **Dense table risks becoming a data dump.**  
   For this user, table anatomy should start with account/campaign identity, status, severity, impact, cause, owner, and next action — not schema-order metrics.

4. **Generic tips rail is low-value for expert internal operators.**  
   A right rail should be contextual: selected-row inspector, anomaly explanation, action checklist, recent changes, or escalation notes. Generic advice makes the console feel less operational.

5. **Missing decision context: thresholds, comparison, time scope, and state semantics.**  
   KPI values need “compared to what?”, time range, freshness, benchmarks, and semantic status. Without that, the dashboard cannot reliably support hour-by-hour decisions.

---

## 4. Concrete design moves

1. **Replace “12 equal cards” with a `lead + support + queue` layout.**  
   Promote one lead operational object: “Revenue at risk,” “Accounts needing action,” or “Campaigns breaching threshold.” Move secondary KPIs into a compact supporting strip.

2. **Create an exception queue above the table.**  
   Show top urgent accounts/campaigns with severity, impact, likely cause, owner, last updated, and recommended next action.

3. **Make the table task-first.**  
   First columns: account/campaign, status, severity, impact, driver, next action. Group diagnostic metrics later. Right-align numbers and use tabular numerals.

4. **Turn the area chart into a diagnostic chart.**  
   Tie it to the selected issue or top queue item. Add threshold lines, annotations, direct labels, and a clear analytical question.

5. **Convert the right rail into a contextual inspector.**  
   When a row is selected: show explanation, recent changes, suggested action, dependencies, and escalation path. If nothing is selected: show only the top blockers or collapse it.

6. **Use semantic token-backed color only.**  
   Reserve color for state: danger, warning, success, info, neutral. Avoid decorative chart fills or arbitrary KPI accents.

7. **Add a scope/control band close to affected data.**  
   Time range, marketplace/account filters, saved views like “Needs action,” “Spend spike,” “ROAS drop,” and “Budget capped.” Active states should be visible beyond color.

8. **Design the state contract before implementation.**  
   Loading, empty, stale data, error, permissions, long labels, zero values, delayed metrics, and keyboard/focus states need first-class treatment.

---

## 5. Verified versus unverified claims

**Verified from prompt only:**

- Surface is an internal ecommerce revenue-ops dashboard.
- Primary user is an operator making next-hour attention decisions.
- Current structure is described as 12 equal KPI cards, decorative area chart, dense account table, and generic tips rail.
- Style authority is restrained enterprise console, dense but calm, token-backed color only.
- No screenshot, DOM, responsive behavior, focus, hover, loading, or error states were verified.

**Reasonable critique based on provided structure:**

- The concept likely under-prioritizes triage.
- Equal cards likely reduce hierarchy.
- Decorative charting likely hurts product fit.
- Generic tips likely mismatch expert internal workflow.

**Unverified and not claimed:**

- Actual visual polish, spacing, contrast, typography, or token compliance.
- Whether the table is truly poorly ordered.
- Whether the chart has useful tooltips, labels, axes, or thresholds.
- Responsive behavior.
- Accessibility, keyboard flow, focus-visible states.
- Loading, empty, error, stale, or permission states.
- Browser performance or runtime behavior.

---

## 6. Minimal validation plan before implementation

1. **Obtain visual artifact or route:** screenshot, Figma, or running page.
2. **Confirm decision model:** what counts as urgent, what thresholds matter, and which metric is source-of-truth.
3. **Run a 3-second hierarchy check:** can an operator identify the top account/campaign needing action?
4. **Validate table anatomy with real data:** long names, many accounts, zero/negative values, missing metrics, stale rows.
5. **Browser-check desktop and narrow viewport:** layout, overflow, sticky controls, chart readability, rail behavior.
6. **Verify state coverage:** loading, empty, error, stale data, permission-limited, and no-urgent-items states.
7. **Check accessibility basics:** contrast, keyboard order, visible focus, non-color-only severity, labels for controls/charts.
8. **Inspect token use:** color, spacing, radius, typography, and state styles should come from the design system, not one-off values.

No files were edited and no browser validation was performed.
