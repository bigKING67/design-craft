## 1. Diagnosis

**Diagnosis — Evidence: static product description + product authority only.** The surface reads like a generic analytics dashboard, but the product’s real job is an exception triage workspace, so the highest-priority decisions are delayed, visually flattened, and under-specified for real operational use.

## 2. Blocking findings

1. **Primary workflow is below the fold.**  
   The exception table is the core object for “find what needs action in the next hour,” but it appears after header clutter, fragmented page metadata, eight equal KPIs, a chart card, and generic insight cards.

2. **Priority hierarchy is inverted or absent.**  
   Revenue risk, blocked SKUs, sell-through, and page views receive equal visual treatment, making urgent operational risk look equivalent to passive analytics.

3. **The table does not support fast exception scanning.**  
   Product, issue, owner, deadline, financial impact, status, and action all use similar weight; long names truncate too early; status is color-dot-only; actions are unlabeled icons.

4. **Generic “insights” dilute trust.**  
   Copy like “Monitor performance closely” is not decision-grade for merchandising analysts because it names no product, threshold, owner, impact, or next action.

5. **Critical production states are undefined.**  
   Empty, loading, error, focus, narrow-laptop, and long-translation states are not described, which blocks confidence in a dense operational surface.

## 3. Secondary findings

1. **Header has too many equal competitors.**  
   Six equal nav links, global search, three icon buttons, and a bright “Create” button compete with exception triage.

2. **Page command area is fragmented.**  
   Title, subtitle, date range, export, and refresh status spread across four weakly aligned rows, increasing scan cost before work begins.

3. **Over-cardification weakens density.**  
   Borders, 16px radius, and soft shadows on every region create a SaaS-template feel and reduce the calm precision expected of an operations workspace.

4. **Typography is too timid for high-stakes scanning.**  
   12–13px low-contrast gray body text and similar weights make owner, deadline, impact, and status harder to distinguish.

5. **Spacing lacks operational rhythm.**  
   Gaps from 8px to 48px without clear grouping make the page feel assembled rather than composed.

## 4. Concrete redesign moves with acceptance criteria

1. **Replace the fragmented hero rows with one compact command band.**  
   Keep title, date range, refresh status, export, and relevant filters on one aligned horizontal grid beneath the global header.  
   **Acceptance:** User can identify current scope, freshness, and available export/refresh controls in one scan line.

2. **Make “exceptions needing action in the next hour” the lead object.**  
   Put a lead summary and the exception table/queue above the chart block.  
   **Acceptance:** At 1366×768, the first screen shows the exception count, total financial exposure, SLA/deadline pressure, and the first actionable rows.

3. **Convert the eight KPI cards into a priority hierarchy.**  
   Promote revenue risk, blocked SKUs, and urgent deadlines; demote page views and passive diagnostics into a compact secondary strip.  
   **Acceptance:** The highest-risk metric is visually dominant, and every emphasized number includes period, comparison, threshold, or owner context.

4. **Remove generic insight cards unless they become evidence-backed action cards.**  
   Each retained insight must name the affected product/segment, observed change, threshold crossed, financial or operational impact, and recommended owner/action.  
   **Acceptance:** No insight can read as reusable dashboard filler.

5. **Rebuild the table around triage anatomy.**  
   Recommended order: product identity, issue/severity, financial impact, deadline/SLA, owner, status, next action; group secondary metadata behind row expansion or lower-emphasis columns.  
   **Acceptance:** A row can be understood left-to-right as “what is wrong, how bad is it, who owns it, when is it due, what do I do?”

6. **Make status and actions text-supported, not icon/color-only.**  
   Replace colored dots with labeled status pills using semantic amber/red/neutral treatment; replace three unlabeled icons with one primary text action plus a labeled overflow menu.  
   **Acceptance:** Status remains understandable without color, and every row action has a visible or accessible name and keyboard path.

7. **Calm the surface system.**  
   Reduce nested cards, reserve elevation for overlays or selected/active regions, use subtle dividers and spacing before shadows, keep the navy/ink neutral system and semantic amber/red status colors.  
   **Acceptance:** The page uses fewer surface layers, clearer grouping, and no decorative gradients/glass/illustration.

8. **Define resilient state variants as part of the design, not afterthoughts.**  
   Specify populated, empty, loading, partial error, full error, stale refresh, long product name, long translation, keyboard focus, disabled action, and narrow-laptop behavior.  
   **Acceptance:** Each state gives a clear next step and preserves table scanability.

## 5. Score band

**Static score band: 58–66 / 100.**  
Justification: the surface has a coherent enterprise-neutral direction and preserves real workflows/data, but the core exception workflow is buried, hierarchy is flat, table affordances are weak, and state/accessibility/responsive behavior is unproven from the supplied description.

## 6. Smallest validation plan that could change the verdict

1. **Desktop first-screen check:** 1440×900 and 1366×768; verify whether exception count, risk, and first actionable rows appear without scrolling.  
2. **Narrow-laptop check:** 1280×720; check command band wrapping, table overflow, sticky header/controls if present, and action visibility.  
3. **Table stress data:** long product names, long owner names, long translated issue/status labels, high currency values, overdue deadlines, multiple severity levels.  
4. **State pass:** populated, zero exceptions, loading, stale refresh, partial API failure, full API failure, disabled action, permission-limited user.  
5. **Keyboard pass:** tab through header, filters, table rows, status/action controls, overflow menus, and return focus after any menu/dialog.  
6. **Status/action comprehension check:** confirm every status and row action is understandable without relying on color or unlabeled icons.
