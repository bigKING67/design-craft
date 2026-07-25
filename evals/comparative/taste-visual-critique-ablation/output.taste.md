## 1. Diagnosis

**Diagnosis — Static evidence only:** The screen currently behaves like a generic analytics dashboard, not an hourly exception workspace: hierarchy, vertical order, and component emphasis delay the analyst from finding urgent merchandising actions.

## 2. Blocking findings

1. **Primary task is below the fold.**  
   The exception table is the core decision surface, but it starts below the fold after header rows, KPI cards, chart cards, and generic insight cards.

2. **Urgency hierarchy is flattened.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive equal card treatment, so operational severity is visually indistinguishable from background telemetry.

3. **The table does not support fast triage.**  
   Product, issue, owner, deadline, financial impact, status, and action use similar weight; status dots lack text; long names truncate too early; unlabeled icon actions slow recognition and increase error risk.

4. **Page structure is over-fragmented.**  
   Title, subtitle, date range, export, and refresh status occupy four separate rows with weak alignment, consuming valuable scan space before any actionable exception appears.

5. **Generic nested-card pattern dilutes credibility.**  
   Pale card → chart card → insight cards, plus repeated borders/radii/shadows, creates decorative containment rather than operational priority.

## 3. Secondary findings

1. **Header competes with the workspace.**  
   Six equal nav links, global search, three icon buttons, and a bright blue “Create” button make the 64px header feel louder than the exception workflow.

2. **Copy is not decision-grade.**  
   “Monitor performance closely” is too vague for analysts who need owner, cause, urgency, and next action.

3. **Typography is too small and too low contrast for dense work.**  
   12–13px low-contrast gray body text is risky for repeated scanning of financial impact, deadlines, and product names.

4. **Spacing lacks a system.**  
   Gaps ranging from 8px to 48px without rhythm make related information feel unrelated and unrelated information feel grouped.

5. **Missing state definitions weaken production readiness.**  
   Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation behavior are not described, which matters for an operations surface used under time pressure.

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception table into the first viewport.**  
   Acceptance: on a 1440×900 desktop viewport, the analyst sees the page title, priority summary, and at least the table header plus 6–8 exception rows without scrolling.

2. **Replace the eight equal KPI cards with a priority summary row.**  
   Acceptance: only 3–4 top metrics receive primary treatment: revenue risk, blocked SKUs, exceptions due within one hour, and unresolved high-severity issues. Secondary metrics such as page views move to a compact “context” area.

3. **Collapse page metadata into one command bar.**  
   Acceptance: title, subtitle, date range, refresh timestamp, export, and filter controls align in one or two structured rows, with one clear left edge and no orphaned controls.

4. **Turn status dots into labeled operational states.**  
   Acceptance: every status includes text, e.g. “Blocked,” “Due <1h,” “Assigned,” “Waiting vendor,” using preserved amber/red semantics; color is never the only indicator.

5. **Rebuild table hierarchy around triage.**  
   Acceptance: issue/severity, deadline, and financial impact are visually stronger than owner and secondary metadata; impact uses tabular numerals; deadlines show both relative urgency and exact time where useful.

6. **Replace unlabeled icon actions with explicit action affordances.**  
   Acceptance: the primary row action is text-labeled, e.g. “Review,” “Assign,” or “Resolve”; secondary actions may sit in a disclosed menu with accessible labels.

7. **Reduce surface noise while preserving the navy/ink neutral system.**  
   Acceptance: remove unnecessary nested cards; use borders or shadows, not both, for most regions; reserve stronger containment for the table and active exception modules; maintain semantic amber/red status colors.

8. **Define resilient content and state behavior.**  
   Acceptance: long product names wrap or expand with full identity available; loading uses table-shaped skeletons; empty state explains “No exceptions for this filter”; error state offers retry and last successful refresh; keyboard focus is visible on nav, filters, rows, and actions.

## 5. Score band

**Static score band: 4–5 / 10.**  
Justification: the surface appears data-rich and has the right raw objects, but static evidence shows the core decision surface is buried, urgency is flattened, status is under-specified, and production states are missing. The score could rise if runtime behavior, filtering, keyboard support, or responsive layouts already compensate for these issues.

## 6. Smallest validation plan that could change the verdict

1. Check a 1440×900 desktop viewport: is the exception table visible without scrolling?  
2. Check a narrow laptop width around 1280px: do header, command bar, KPI summary, and table remain usable without horizontal crowding?  
3. Keyboard through header, filters, table rows, and actions: is focus visible and order predictable?  
4. Inspect loading, empty, error, and stale-refresh states for the table and priority metrics.  
5. Test long product names, long owner names, and translated labels: do they preserve identity and action clarity?  
6. Verify status semantics: are amber/red states labeled, screen-readable, and not color-only?
