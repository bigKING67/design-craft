## 1. Diagnosis

**Evidence label: static-contextual prose only.** The surface reads like a generic dashboard organized around modules, not an operations workspace optimized to surface the next-hour merchandising exceptions that require action.

## 2. Blocking findings

1. **Primary decision object is below the fold.**  
   The exception table is the core workflow, but it appears after KPI grids, nested chart cards, and generic insights, delaying the analyst’s first actionable read.

2. **Priority hierarchy is flat where urgency should dominate.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views use equal KPI treatment, identical sparklines, and similar card weight, so operational blockers do not visually outrank diagnostics.

3. **The exception table is not action-scannable.**  
   Product, issue, owner, deadline, financial impact, status, and action share similar text weight; status uses color-only dots; long product names truncate; row actions are unlabeled icons.

4. **Surface treatment creates noise instead of structure.**  
   Repeated borders, 16px radii, soft shadows, nested cards, and inconsistent 8–48px gaps make every region compete while weakening figure/ground and scan rhythm.

5. **Production states and accessibility-critical behavior are unspecified.**  
   Empty, loading, error, focus, narrow-laptop, and long-translation states are absent; low-contrast 12–13px text, color-only status, and unlabeled icon actions are high-risk for operators.

## 3. Secondary findings

1. **Header command hierarchy is overloaded.**  
   Six equal nav links, search, three icon buttons, logo, and a bright blue Create button compete with exception-finding, especially if “Create” is not the next-hour primary action.

2. **Page context is fragmented.**  
   Title, subtitle, date range, export, and refresh status occupying four separate weakly aligned rows increases orientation cost before the user reaches work.

3. **Insights are too generic to earn space.**  
   “Monitor performance closely” does not name an SKU, threshold, owner, impact, or next action, so it behaves as decorative copy rather than operational guidance.

4. **Charts appear to answer no named question.**  
   A large area chart plus equal blue sparklines consumes attention without being tied to exception triage, deadline risk, or financial exposure.

5. **Typography is too timid for dense decision work.**  
   Low-contrast gray 12–13px body text may be acceptable for metadata, but not for issue, deadline, status, impact, or action labels.

## 4. Concrete redesign moves with acceptance criteria

1. **Collapse the page command area into one aligned operations band.**  
   - Put title, scope/date range, refresh timestamp, export, and relevant filters into one compact header band beneath global nav.  
   - Acceptance: at 1366×768, the first exception or lead exception summary appears without scrolling; refresh state is adjacent to the data it qualifies.

2. **Reframe the top of page around “exceptions needing action.”**  
   - Replace the equal dashboard-first flow with: lead exception summary → priority metric strip → exception queue/table → diagnostics.  
   - Acceptance: within three seconds, an analyst can identify count of urgent exceptions, total financial exposure, and the next row/action to address.

3. **Tier the KPI system by operational importance.**  
   - Promote urgent risk, blocked SKUs, deadline breaches, and financial impact; demote page views and broad diagnostics to a compact secondary strip.  
   - Acceptance: only semantically urgent metrics use amber/red; every emphasized number includes comparison, threshold, or time basis.

4. **Move or rewrite charts and insights so they support triage.**  
   - Area chart should answer a named question such as “risk exposure by deadline window” or move below the table.  
   - Generic insight cards should be removed unless they include entity/segment, observed threshold, impact, owner, and direct action/filter.  
   - Acceptance: every retained insight can route the analyst to affected table rows.

5. **Redesign the exception table around row decisions.**  
   - First columns: issue severity/status with text, product identity, financial impact, deadline, owner, next action.  
   - Use text labels plus semantic color for status; right-align money; keep actions labeled, e.g. “Assign,” “Resolve,” “Review.”  
   - Acceptance: no critical state depends on color alone; row actions have visible labels or accessible names; long product names wrap to two lines or reveal full text on expansion.

6. **Reduce card density and normalize spacing.**  
   - Remove nested cards; reserve elevation for overlays, selected rows, or genuinely raised panels. Use subtle dividers and section spacing instead.  
   - Acceptance: one consistent spacing rhythm is visible, e.g. 8px tight, 16px component, 24px group, 32px section; repeated shadows are not used as the primary grouping mechanism.

7. **Raise decision-bearing typography and contrast.**  
   - Keep 12px only for metadata; use at least 14px/1.4 for table cells and operational copy, with stronger ink for issue, deadline, impact, and action.  
   - Acceptance: primary table text meets normal-text contrast expectations against its surface; secondary helper text remains visibly subordinate but readable.

8. **Define the state and resilience contract.**  
   - Add designed loading, empty, error/retry, stale refresh, disabled action, keyboard-focus, long-name, long-translation, and narrow-laptop states.  
   - Acceptance: each state preserves current filters/scope, explains what happened, and gives the operator a local next action without losing table context.

## 5. Static score band

**48–58 / 100, static-contextual only.**  
The surface has recognizable dashboard components and an existing neutral/status system, but the primary workflow is buried, hierarchy is flat, action semantics are weak, and major production states are unspecified. Runtime evidence could move this band, but the described structure cannot score as polished operations software while the exception table starts below the fold.

## 6. Smallest validation plan that could change the verdict

No browser, DOM, responsive, accessibility-tree, or runtime validation was performed here. The smallest future check that could change the verdict:

1. **Desktop browser smoke at 1440×900 and 1366×768:** verify what appears before scrolling and whether urgent exceptions are visible immediately.  
2. **Narrow-laptop check around 1280×720:** verify header wrapping, KPI compression, table reachability, and action visibility.  
3. **State pass:** capture loading, empty, error/retry, stale data, and disabled action states for the KPI area and exception table.  
4. **Hostile-content pass:** test long product names, long translated labels, large currency values, many owners, and mixed red/amber statuses.  
5. **Keyboard pass:** tab through nav, filters, table rows, and row actions; verify visible focus and understandable action/status labels.
