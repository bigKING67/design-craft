## 1. Diagnosis

**Static-evidence verdict:** The screen is visually credible but mis-prioritized: it spends the above-fold area on navigation, generic KPIs, nested cards, and weakly aligned metadata while the primary job — finding urgent merchandising exceptions in the next hour — is pushed below the fold and underweighted.

---

## 2. Blocking findings

1. **Primary workflow is below the fold.**  
   The exception table starts below the fold, so analysts must scroll before seeing the items most likely to require action.

2. **Everything important has equal visual weight.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views are presented as identical KPI cards, making urgent operational risk look equivalent to background reporting.

3. **The exception table lacks decision hierarchy.**  
   Product, issue, owner, deadline, financial impact, status, and action use similar text weight, so the analyst cannot quickly rank “what is broken, how costly it is, who owns it, and what to do next.”

4. **Status and actions are ambiguous.**  
   Small colored dots without text and three unlabeled action icons require interpretation, which is risky in a dense operations surface.

5. **Critical identifiers are hidden.**  
   Long product names truncate at 24 characters, which can obscure variant, marketplace, SKU, or campaign details needed to decide whether an exception is actionable.

---

## 3. Secondary findings

1. **Header competes with the work area.**  
   Six equal nav links, global search, three icon buttons, and a bright blue “Create” button consume attention before the analyst reaches the exception workflow.

2. **Page metadata is fragmented.**  
   Title, subtitle, date range, export, and refresh status occupy four separate rows with weak alignment, increasing scanning cost.

3. **Nested cards create visual noise.**  
   A pale card containing another chart card plus three more insight cards adds depth and borders without clarifying what needs action.

4. **Generic insight copy reduces trust.**  
   Phrases like “Monitor performance closely” sound non-operational and do not explain impact, owner, threshold, or next step.

5. **Density is not controlled by a clear rhythm.**  
   Low-contrast 12–13px body text, inconsistent 8–48px gaps, and repeated borders/radius/shadows make the surface feel busy rather than precise.

---

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception table into the first viewport.**  
   - Acceptance: At 1440×900, the page shows the title band, priority summary, table header, and at least the first 6–8 exception rows without scrolling.  
   - Acceptance: The first visible row exposes issue, deadline, impact, status text, and primary action.

2. **Replace eight equal KPI cards with a prioritized exception summary.**  
   - Acceptance: Use 3–4 top-line operational signals only: for example `Revenue at risk`, `Blocked SKUs`, `Due in next hour`, and `Unassigned exceptions`.  
   - Acceptance: Revenue risk and blocked SKUs receive stronger scale/weight than page views or secondary trend metrics.  
   - Acceptance: Page views are removed from the primary band unless directly tied to an exception threshold.

3. **Create a single aligned page command row.**  
   - Acceptance: Title, date range, refresh status, export, and refresh action sit in one compact, left/right-aligned band.  
   - Acceptance: Subtitle is reduced to one short operational sentence or removed if redundant.  
   - Acceptance: Refresh status uses quiet text such as “Updated 4 min ago” near the refresh control.

4. **Flatten the card structure and reduce decorative chrome.**  
   - Acceptance: Remove nested card-in-card treatment around the chart and insight area.  
   - Acceptance: Use one container level per region, with borders/shadows reserved for separation only where needed.  
   - Acceptance: Preserve navy/ink neutrals and amber/red semantic status colors; no gradients, glass, or illustration.

5. **Redesign the table around exception triage.**  
   - Acceptance: Column hierarchy favors `Issue`, `Deadline`, `Financial impact`, `Status`, and `Action`.  
   - Acceptance: Product name remains available but does not visually overpower the exception reason.  
   - Acceptance: Rows with amber/red states have visible but restrained emphasis using semantic color, not only dots.

6. **Replace status dots with labeled status badges.**  
   - Acceptance: Every status includes text, for example `Blocked`, `At risk`, `Due soon`, `Owner needed`, `Monitoring`.  
   - Acceptance: Color is redundant with text and not the sole carrier of meaning.  
   - Acceptance: Badge contrast remains readable against the neutral table background.

7. **Make actions explicit and safe.**  
   - Acceptance: Replace three unlabeled icons with either one primary text action plus secondary menu, or icon+label controls such as `Assign`, `Resolve`, `Open`.  
   - Acceptance: The primary action is consistent per status type and appears in the same column position.  
   - Acceptance: Destructive or irreversible actions are not presented as anonymous icons.

8. **Protect real operational text and edge cases.**  
   - Acceptance: Product names can show meaningful distinguishing information beyond 24 characters, either by wider column, two-line wrapping, or secondary SKU/variant line.  
   - Acceptance: Long owner names, translated labels, large currency values, and long issue names do not collapse the row.  
   - Acceptance: Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are specified before visual signoff.

---

## 5. Static score band

**Exception-finding fitness: 35–45 / 100 based on the static description.**

The screen has the ingredients of an operations workspace — real table data, status colors, KPIs, date range, export, refresh — but the visual hierarchy currently optimizes for dashboard breadth rather than urgent exception triage. The main reason the score is not lower is that the existing workflows and data structure appear salvageable without a ground-up rebrand.

---

## 6. Smallest validation plan that could change the verdict

1. **Viewport check:** Review the actual screen at 1440×900 and 1280×720 to verify whether the exception table is truly below the fold and how many actionable rows are visible.

2. **State fixtures:** Inspect static or implemented states for loading, empty, error, stale refresh, long product names, long translations, and many urgent exceptions.

3. **Keyboard pass:** Verify visible focus order from global search through filters/table/actions, especially the unlabeled icon actions if they remain.

4. **Contrast/readability pass:** Check 12–13px gray body text, status badges, helper copy, and disabled/error states against the navy/ink neutral system.

5. **Triage task test:** Give an analyst five minutes to identify the top three exceptions requiring action in the next hour; if they scroll, hesitate on status meaning, or open rows just to understand actions, the verdict remains blocking.
