## 1. Evidence level and score band

**Evidence level: L0 static / prompt-only concept.**  
Only the product brief and described structure were reviewed. No screenshot, DOM, tokens, responsive behavior, focus, hover, loading, empty, or error states were verified.

**Provisional score band: 60–70 / 100 — functional but ordinary.**  
The concept contains expected dashboard ingredients, but the described hierarchy is “dashboard card soup,” not an operator decision surface.

## 2. Design read

Reading this as: **a restrained enterprise revenue-ops command dashboard for ecommerce operators, optimized for deciding which account or campaign needs attention in the next hour.**

The page should behave less like a reporting overview and more like an **exception triage surface**: what changed, why it matters, who owns it, and what action should happen now.

## 3. Top hierarchy / product-fit issues

1. **P1 — Twelve equal KPI cards flatten urgency.**  
   Equal surfaces imply equal importance, but the user’s job requires priority: biggest risk, missed target, spend anomaly, blocked account, or campaign requiring action.

2. **P1 — The decorative area chart is occupying analytical real estate without a named question.**  
   In an ops dashboard, a chart should explain an anomaly, trend, threshold breach, or forecast risk. If it only adds visual rhythm, it slows scanning.

3. **P1 — The dense account table risks becoming a data dump.**  
   For the “next hour” job, the table must lead with identity, status, risk, impact, cause, owner, and next action — not generic account attributes.

4. **P1 — The right rail with generic tips is mismatched to internal operations work.**  
   Generic advice reads like SaaS onboarding or marketing garnish. Operators need entity-specific evidence, queue context, playbooks, notes, or escalation paths.

5. **P1 — Critical operational context is not named in the structure.**  
   Time range, data freshness, applied filters, business scope, alert thresholds, and source reliability need to be visible; otherwise operators cannot trust the ranking.

## 4. Concrete design moves

1. **Replace the 12-card grid with a lead + support hierarchy.**  
   Use one dominant “needs attention now” object, then a compact supporting metric strip. Keep only metrics that affect triage.

2. **Create an exception queue near the top.**  
   Show the top accounts/campaigns by urgency with: entity, reason, impact, confidence/threshold, owner, and recommended next action.

3. **Add a command/context band.**  
   Include marketplace/account scope, time window, data freshness, applied filters, and alert model/threshold state. Keep it compact and token-backed.

4. **Reframe the chart as a diagnostic module.**  
   Rename it around a question, e.g. “Spend spike vs. revenue response” or “Accounts crossing margin-risk threshold.” Add direct labels, threshold lines, and a takeaway.

5. **Turn the table into a task-first table.**  
   First columns: account/campaign, status, risk reason, revenue/margin impact, trend, owner, next action. Right-align numbers; use tabular figures; group secondary metadata later.

6. **Replace the generic tips rail with a contextual action/detail rail.**  
   When no row is selected, show queue summary and playbook shortcuts. When selected, show evidence, recent changes, notes, owner, escalation, and action history.

7. **Use restrained enterprise visual grammar.**  
   Favor subtle dividers, calm surfaces, tight spacing rhythm, semantic status color only, clear type hierarchy, and minimal elevation. Avoid marketing-card treatment.

8. **Design the state family before implementation.**  
   Define loading, stale data, empty queue, partial data, API error, permission-limited, long labels, large numbers, selected row, keyboard focus, and reduced-width behavior.

## 5. Verified versus unverified claims

**Verified from prompt only:**
- The surface is an internal ecommerce revenue-ops dashboard.
- Primary user is an operator deciding what needs attention in the next hour.
- Current concept uses 12 equal KPI cards, a decorative area chart, dense account table, and generic tips rail.
- Style target is restrained enterprise console with token-backed color.

**Not verified:**
- Actual visual quality, spacing, contrast, typography, alignment, or token usage.
- Whether the KPI cards have deltas, thresholds, comparisons, or semantic states.
- Whether the chart is truly decorative in implementation.
- Table column order, sorting, filtering, row actions, keyboard behavior, or accessibility.
- Responsive behavior, overflow handling, loading/empty/error states, hover/focus states, or performance.
- Browser behavior or screenshot evidence — none was claimed.

## 6. Minimal validation plan before implementation

1. **Decision-flow review:** confirm the top 5 operator decisions and the ranking logic for “needs attention now.”  
2. **Data contract audit:** define source of truth, freshness, thresholds, missing-data behavior, and ambiguity handling for account/campaign risk.  
3. **Low-fidelity hierarchy test:** compare current card-grid layout against lead + queue + diagnostic chart using realistic entities and numbers.  
4. **State inventory:** specify loading, empty, error, stale, permission, long-content, and partial-data states for metrics, chart, table, and rail.  
5. **Accessibility and keyboard plan:** define focus order, table navigation, row selection, semantic status labels, and non-color-only risk indicators.  
6. **Responsive check plan:** validate desktop dense layout plus constrained widths before claiming production readiness.
