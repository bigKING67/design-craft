## 1. Evidence level and score band

- **Evidence level:** **L0 static / prompt-only concept review**. Product context is supplied, but there is **no screenshot, DOM, token audit, responsive run, interaction walk, or state verification**.
- **Score band:** **60–74: functional but ordinary**, with product-fit risk at the lower end. The concept may show data, but it does not yet shape attention toward the operator’s next-hour decision.
- **Mode used:** design-craft `critique`; no files edited; no browser validation claimed.

## 2. Design read

Reading this as: **an internal ecommerce revenue-ops dashboard for operators**, with a **restrained enterprise-console / ops command-center** tone, optimized for **finding the account or campaign that needs action in the next hour**.

The dashboard’s primary job is not “show revenue information.” It is: **triage exceptions, compare impact, expose likely cause, and make the next action obvious.**

## 3. Top hierarchy / product-fit issues

**F1 — KPI card soup hides priority.**  
Source proof: “12 equal KPI cards at the top.”  
Risk: equal surface weight makes routine totals compete with urgent risks.  
Repair: convert to **lead risk object + compact supporting metric strip**.

**F2 — Decorative chart is not earning attention.**  
Source proof: “one decorative area chart.”  
Risk: visual drama without a named operational question wastes the first scan path.  
Repair: make it a **diagnostic chart** tied to anomaly, threshold, account segment, or campaign movement.

**F3 — Dense account table is probably the real product, but it is placed as raw data.**  
Source proof: “dense account table.”  
Risk: if the operator is choosing whom to act on, the table needs to be a **task-first queue**, not a schema dump.  
Repair: order columns by **identity → status/risk → impact → cause signal → next action/owner**.

**F4 — Generic tips right rail is low-trust guidance.**  
Source proof: “right rail with generic tips.”  
Risk: generic advice competes with real exceptions and may feel like decoration disguised as insight.  
Repair: replace with **action rail / exception queue** that names entity, evidence, impact, owner, and recommended action.

**F5 — State and data-quality confidence are unproven.**  
Source proof: prompt says no loading, error, hover, focus, responsive, or source verification.  
Risk: dashboard decisions depend on freshness, metric definitions, thresholds, and failure visibility.  
Repair: add explicit **freshness, filter scope, empty/loading/error/partial states, and metric definition affordances** before implementation sign-off.

## 4. Concrete design moves

1. **Dashboard card soup → decision surface:** make the first module “What needs attention now?” not “all KPIs equally.”
2. **Flat KPI grid → priority hierarchy:** use one lead operational state, 4–6 supporting KPIs, and diagnostic metrics below.
3. **Exception-first composition:** top area should show highest-risk account/campaign, impact estimate, trigger, owner, and next action.
4. **Task-first table:** sort by urgency or revenue impact by default; expose filters near the table; keep row actions keyboard reachable.
5. **Semantic status color only:** reserve color for warning, critical, success, neutral, stale, and filtered states; avoid decorative gradients.
6. **Enterprise dense treatment:** compact type, tabular numerals, subtle dividers, minimal elevation, consistent token-backed spacing.
7. **Chart with a question:** replace the decorative area chart with “Which accounts/campaigns changed materially vs threshold in the last N hours?”
8. **Right rail as action rail:** show “stale spend spike,” “ROAS below floor,” “budget pacing risk,” or “missing feed data” only when evidence and action exist.

## 5. Verified versus unverified claims

**Verified from prompt only:**
- Intended user is an internal ecommerce revenue-ops operator.
- Current concept has 12 equal KPI cards, decorative area chart, dense table, and generic tips rail.
- Style target is restrained enterprise console, dense but calm, token-backed color only.
- No runtime or visual artifacts were verified.

**Unverified / not claimed:**
- Actual visual polish, spacing, contrast, typography, or token compliance.
- Browser behavior, responsiveness, keyboard flow, focus states, hover states.
- Loading, empty, error, permission, stale-data, partial-data, or recovery states.
- Metric source-of-truth, freshness, thresholds, duplicate/missing account data, or filter correctness.
- Table performance, row count handling, chart tooltip behavior, or small-viewport usability.

## 6. Minimal validation plan before implementation

1. Confirm the **decision model**: what counts as urgent in the next hour: revenue drop, ROAS, budget pacing, feed issue, inventory, campaign anomaly, or account SLA.
2. Define metric **source-of-truth, freshness, time window, thresholds, and ownership** for each surfaced KPI or alert.
3. Prototype one desktop layout with **lead + support + action queue + diagnostic chart + task-first table**.
4. Validate with realistic data: long account names, zero data, stale data, many rows, conflicting statuses, and ambiguous ownership.
5. Run visual review from screenshot/browser artifact: hierarchy, density, token color, contrast, numeric alignment, and table scan speed.
6. Run interaction/accessibility checks: keyboard table navigation, focus visibility, row actions, filters, tooltips, and non-color status meaning.
7. Check responsive behavior: preserve critical actions and isolate unavoidable overflow to the data table region.
8. Only then score beyond L0; until browser/runtime evidence exists, this remains a concept-level critique.
