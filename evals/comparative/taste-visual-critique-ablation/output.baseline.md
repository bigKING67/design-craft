## 1. Diagnosis

**Diagnosis — Static evidence only:** the screen appears operationally complete, but its visual hierarchy sends attention to navigation, generic KPI symmetry, and nested cards before the exception queue that merchandising analysts need to act on within the next hour.

## 2. Blocking findings

1. **The primary job is below the fold.**  
   The exception table is the action surface, but it starts after header rows, eight KPI cards, chart cards, and generic insight cards.

2. **All metrics are treated as equally important.**  
   Revenue risk, blocked SKUs, sell-through, and page views share the same card weight, number size, and blue sparkline treatment, which obscures urgent exceptions.

3. **The page header is fragmented and weakly aligned.**  
   Title, subtitle, date range, export, and refresh status occupying four rows creates scanning cost before any operational decision.

4. **The table does not expose action priority clearly.**  
   Product, issue, owner, deadline, impact, status, and action have similar weight; status dots lack text; actions are unlabeled icons.

5. **The surface overuses containers and shadows.**  
   Borders, 16px radii, and soft shadows on every region make all sections feel equally elevated, reducing precision and calm density.

## 3. Secondary findings

1. **Generic insights are not decision-grade.**  
   “Monitor performance closely” does not help an analyst choose the next action.

2. **Long product names are prematurely truncated.**  
   Cutting names at 24 characters risks hiding the distinguishing SKU detail needed for merchandising work.

3. **Low-contrast 12–13px body text weakens dense scanning.**  
   Dense does not need to mean faint; operational tables need durable legibility.

4. **Spacing rhythm is inconsistent.**  
   Gaps from 8px to 48px make the page feel assembled rather than governed by a predictable grid.

5. **Critical production states are undefined.**  
   Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are not described, so the design is not yet production-complete.

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception queue into the first viewport.**  
   - Place the table or a compact exception queue directly below a single command/header row.  
   - **Acceptance:** on a 1366×768 desktop viewport, at least the table header and first 5 exception rows are visible without scrolling.

2. **Collapse page metadata into one aligned command bar.**  
   - Combine title, subtitle, date range, refresh status, export, and any primary page action into one or two disciplined rows.  
   - **Acceptance:** title/date/refresh/export share one horizontal alignment system; no more than two rows are used before the operational content begins.

3. **Prioritize exception-driving KPIs over ambient metrics.**  
   - Promote revenue risk, blocked SKUs, overdue/near-deadline items, and unresolved exceptions.  
   - Demote page views and other context metrics into a secondary strip or hidden detail area.  
   - **Acceptance:** the top KPI group contains no more than 3–4 primary metrics, and the most urgent metric has visibly stronger emphasis than page views.

4. **Replace equal blue sparklines with semantic signal.**  
   - Use navy/ink neutrals for baseline trend and amber/red only for warning or blocking conditions.  
   - **Acceptance:** blue is not used as a universal attention color; red/amber appear only where they map to actual status severity.

5. **Turn generic insight cards into an exception summary.**  
   - Replace “Monitor performance closely” style copy with specific operational summaries: “12 SKUs blocked by missing imagery,” “$48k revenue at risk today,” “5 items need owner reassignment.”  
   - **Acceptance:** every insight names a count, condition, and next likely action.

6. **Rebuild the table hierarchy around decision fields.**  
   - Give issue, deadline, financial impact, and status stronger visual priority than passive metadata.  
   - Allow product names to wrap to two lines or expose distinguishing SKU text before truncation.  
   - **Acceptance:** a row can be scanned left-to-right to answer: what is wrong, how urgent is it, what is the impact, who owns it, what should I do?

7. **Make status and actions explicit.**  
   - Replace dot-only status with text labels such as “Blocked,” “At risk,” “Due today,” or “Monitoring,” using semantic amber/red where appropriate.  
   - Replace three unlabeled action icons with one primary labeled action plus a labeled overflow.  
   - **Acceptance:** status and primary action remain understandable without relying on color or icon recognition.

8. **Reduce container noise and establish a spacing/type rhythm.**  
   - Reserve borders/shadows for major regions only; use separators, whitespace, and typography for internal grouping.  
   - Raise body text to a durable operations size and improve contrast while preserving the navy/ink neutral system.  
   - **Acceptance:** repeated cards no longer compete equally; section spacing follows a small consistent scale, for example compact/standard/large rather than arbitrary 8–48px gaps.

## 5. Score band

**Static score band: 5–6 / 10.**  
Justification: the screen includes the necessary operational ingredients, but the described hierarchy, table placement, ambiguous status/action treatment, and missing production states directly conflict with the primary job of finding next-hour exceptions quickly.

## 6. Smallest validation plan that could change the verdict

1. **Viewport check:** test the real page at 1366×768 and 1440×900 to verify whether exception rows are visible before scrolling.  
2. **Dense-data check:** load realistic long product names, long issue labels, high financial-impact values, and translated labels.  
3. **State check:** inspect loading, empty, partial-error, stale-refresh, and failed-export states.  
4. **Keyboard check:** tab through global search, date range, export, table rows, status controls, and row actions to verify visible focus and usable order.  
5. **Decision-speed check:** with real analysts or a timed internal review, ask: “Which three exceptions need action in the next hour?” and measure whether the table, not the KPI/chart area, drives the answer.
