## 1. Diagnosis

**Diagnosis — Static evidence only:** The screen is organized like a generic analytics dashboard, not an exception triage workspace, so the data most relevant to “what needs action in the next hour” is visually delayed, under-prioritized, and weakened by uniform emphasis, low contrast, and unclear action affordances.

## 2. Blocking findings

1. **Primary workflow starts below the fold**
   - The exception table is the core decision surface, but it appears after header rows, eight KPI cards, a large chart card, and generic insight cards.
   - This conflicts with the stated job: finding near-term exceptions quickly.

2. **Hierarchy treats unequal signals as equal**
   - Revenue risk, blocked SKUs, sell-through, and page views share the same KPI treatment, size, card weight, and blue sparklines.
   - Operational severity is not visually distinguishable from context metrics.

3. **Table rows are not scannable enough for triage**
   - Product, issue, owner, deadline, financial impact, status, and action use similar text weight.
   - Status dots lack text, long names truncate too early, and action icons are unlabeled.
   - This makes it harder to identify severity, ownership, urgency, and next step.

4. **The visual system is over-carded**
   - Every region has a border, 16px radius, and soft shadow, including nested cards.
   - This creates excessive surface competition and weakens the difference between navigation, summary, analysis, and action areas.

5. **Critical states are undefined**
   - Empty, loading, error, focus, narrow-laptop, and long-translation states are not described.
   - For an operations workspace, these are not edge cases; they determine whether analysts can trust and recover from the surface under pressure.

## 3. Secondary findings

1. **Header density competes with page work**
   - Six equal nav links, search, three icon buttons, and a bright blue Create button consume attention before the user reaches exception work.
   - “Create” may be over-emphasized if the primary job is exception triage.

2. **Page metadata is fragmented**
   - Title, subtitle, date range, export, and refresh status occupy four rows with weak alignment.
   - This increases vertical cost and makes freshness/date scope harder to verify at a glance.

3. **Generic insights reduce credibility**
   - Cards saying “Monitor performance closely” do not appear actionable.
   - They occupy decision space without naming affected SKUs, owners, severity, or recommended next action.

4. **Typography is too small and low contrast for repeated use**
   - 12–13px low-contrast gray body text is fragile for dense operational scanning.
   - It also risks making deadlines, owners, and impact values feel secondary.

5. **Spacing rhythm is inconsistent**
   - Gaps ranging from 8px to 48px without a clear pattern make the page feel assembled rather than operationally structured.
   - This reduces calmness and scan confidence.

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception table into the first viewport**
   - Place the exception queue directly below a compact page command row and a short priority summary.
   - **Acceptance criteria:** On a typical desktop viewport, at least the table header and 5–8 exception rows are visible without scrolling.

2. **Replace eight equal KPI cards with a priority strip**
   - Use 3–4 operational priority metrics: revenue at risk, blocked SKUs, overdue/next-hour exceptions, and owner coverage.
   - Move lower-priority context metrics such as page views into a secondary analytics section.
   - **Acceptance criteria:** The most urgent metric has stronger visual priority than context metrics through position, label, value treatment, and semantic status color where appropriate.

3. **Create a compact, aligned page command row**
   - Combine title, date range, refresh status, export, and refresh action into one or two aligned rows.
   - Keep the title left, scope/freshness adjacent, and actions right.
   - **Acceptance criteria:** Date range and data freshness are visible within the page header area without adding extra vertical bands.

4. **Rebuild table hierarchy around triage**
   - Make issue/severity, deadline, financial impact, and owner the strongest scanning anchors.
   - Product name should remain readable, but not dominate the exception reason.
   - **Acceptance criteria:** A user can identify “what is wrong,” “how urgent,” “who owns it,” and “what to do next” from a row without opening details.

5. **Replace dot-only statuses with labeled status pills**
   - Preserve amber/red semantic colors, but pair color with text such as `Blocked`, `At risk`, `Due <1h`, `Overdue`, or `Needs owner`.
   - **Acceptance criteria:** Status meaning is understandable without relying on color alone.

6. **Make actions explicit and role-specific**
   - Replace three unlabeled icons with one primary text action plus a secondary overflow if needed.
   - Example: `Resolve`, `Assign`, `Review`, or `Open`.
   - **Acceptance criteria:** Each row has a clearly named next action; icon-only controls include visible labels or are moved behind a labeled overflow.

7. **Reduce decorative container weight**
   - Keep the navy/ink neutral system, but reserve borders/shadows for active panels or grouped data that needs separation.
   - Flatten nested insight/chart areas and reduce repeated 16px-radius cards.
   - **Acceptance criteria:** The exception queue has the strongest surface priority; secondary analytics do not visually compete with it.

8. **Define production states before visual polish**
   - Specify loading skeletons, empty states, error/retry states, keyboard focus, narrow-laptop behavior, and long-content wrapping.
   - **Acceptance criteria:** Every primary region has a documented loading, empty, error, and focus state; long product names and translated labels preserve row comprehension without destructive truncation.

## 5. Bounded score

**Static evidence score band: 5/10–6/10.**

Justification: The screen appears functionally complete and uses an existing restrained operations palette, but the static description shows major hierarchy and workflow mismatches: the exception table is delayed, critical statuses are under-labeled, action affordances are unclear, and production states are unspecified. The score should not be lower because the described surface has real data structures and relevant operational content; it should not be higher because the primary decision flow is not yet leading the layout.

## 6. Smallest validation plan that could change the verdict

1. **First-viewport check**
   - Verify whether exception rows are visible on common desktop and narrow-laptop widths.
   - Verdict changes if the table is already visible and usable without scrolling.

2. **Triage task timing**
   - Ask analysts to identify the highest-risk exception, owner, deadline, and next action from the static page.
   - Verdict changes if users can do this quickly and consistently despite the current hierarchy.

3. **State coverage review**
   - Inspect loading, empty, error, long-name, long-translation, and stale-data states.
   - Verdict changes if these states are already designed and maintain table comprehension.

4. **Keyboard and focus pass**
   - Check whether search, filters, table rows, status, and row actions have visible focus and logical order.
   - Verdict changes if keyboard-heavy operation is already strong.

5. **Responsive density pass**
   - Review the same surface on narrow laptop widths where dense operations tools often fail.
   - Verdict changes if hierarchy, labels, and row actions remain readable without hiding critical triage data.
