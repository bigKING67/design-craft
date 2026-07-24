## 1. Diagnosis + evidence label

The surface currently reads like a generic analytics dashboard instead of an exception-resolution workspace: the urgent decision object is pushed below the fold while equalized KPIs, nested cards, weak hierarchy, and unlabeled actions obscure what a merchandising analyst should do in the next hour. **Evidence label: static description only; no browser, DOM, responsive, accessibility-tree, or runtime validation performed.**

---

## 2. Blocking findings

1. **Primary workflow is visually buried.**  
   The exception table is the core job surface, but it starts below the fold after header chrome, fragmented page metadata, eight equal KPI cards, a large chart card, and generic insight cards.

2. **Decision hierarchy is flat where it needs to be ranked.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive equal card treatment, identical sparklines, and similar visual weight, so the screen does not guide attention toward urgent exceptions.

3. **The table cannot be scanned safely under time pressure.**  
   Product, issue, owner, deadline, financial impact, status, and action use similar weight; status is color-dot-only; long product names truncate early; actions are unlabeled icons. This weakens prioritization and increases mis-action risk.

4. **Accessibility and legibility are materially under-specified.**  
   Low-contrast 12–13px body text, color-only status, missing keyboard-focus description, and unlabeled icon actions are incompatible with a dense operations console used repeatedly by keyboard-heavy staff.

5. **State resilience is absent from the design description.**  
   Empty, loading, error, refresh failure, long translation, narrow-laptop, and focus states are not described, which is a blocker for a surface whose value depends on credible, current operational data.

---

## 3. Secondary findings

1. **The header is over-weighted for the task.**  
   Logo, six equal nav links, global search, three icon buttons, and a bright “Create” button compete with the exception-finding workflow.

2. **Page metadata is fragmented.**  
   Title, subtitle, date range, export, and refresh status occupying four separate rows creates weak alignment and consumes vertical space before the user reaches actionable data.

3. **The card system is over-applied.**  
   Borders, 16px radii, and soft shadows on every region create visual noise and reduce the calm precision expected from a serious operations workspace.

4. **The “insights” content is not operationally credible.**  
   Generic copy such as “Monitor performance closely” does not name an exception, owner, deadline, impact, or next action.

5. **Spacing rhythm is inconsistent.**  
   Gaps ranging from 8px to 48px without an apparent scale make the surface feel less systematic and reduce scan confidence.

---

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception table into the first viewport.**  
   - Acceptance: on a typical desktop/laptop height, the table header and at least the first several exception rows are visible without scrolling.  
   - Acceptance: the page leads with “exceptions needing action,” not with generic analytics.

2. **Collapse page metadata into one aligned command row.**  
   - Combine title, subtitle or scope, date range, refresh state, export, and relevant controls into a single structured header area below the global nav.  
   - Acceptance: date range and data freshness are visible beside the workspace title, not stranded across multiple rows.  
   - Acceptance: export and refresh are secondary utilities, not equal to the primary triage path.

3. **Reduce the KPI set to a ranked exception summary.**  
   - Promote only the metrics that answer: “What needs action in the next hour?”  
   - Suggested hierarchy: revenue at risk, blocked SKUs, deadline breaches, owner coverage / unassigned exceptions.  
   - Acceptance: primary risk metrics are visually stronger than passive analytics such as yesterday’s page views.  
   - Acceptance: sparklines are used only where trend changes the action; otherwise use direct deltas, counts, and severity.

4. **Replace generic insight cards with specific exception drivers.**  
   - Example pattern: “17 blocked SKUs over $42k risk — 9 owned by Marketplace Ops — 4 due before 3pm.”  
   - Acceptance: every insight names a metric, segment, urgency, and recommended next step.  
   - Acceptance: remove any insight that could apply to any dashboard.

5. **Redesign the table for triage-first scanning.**  
   - Emphasize issue severity, deadline, financial impact, owner, and next action.  
   - Use readable product names with two-line wrapping or a persistent reveal pattern instead of hard 24-character truncation.  
   - Acceptance: a row can be understood without opening detail: what is wrong, how urgent it is, who owns it, what money is at risk, and what action is available.

6. **Make status text explicit and non-color-dependent.**  
   - Replace dot-only status with label + semantic color: “Blocked,” “At risk,” “Due today,” “Resolved,” etc.  
   - Preserve amber/red semantics for warning and critical states.  
   - Acceptance: status remains understandable in grayscale and to users who cannot rely on color perception.

7. **Replace unlabeled icon actions with explicit, safe actions.**  
   - Use text buttons or icon+label patterns for primary row actions such as “Assign,” “Resolve,” “Review,” or “Escalate.”  
   - Put destructive or irreversible actions behind confirmation or a secondary menu.  
   - Acceptance: each action has a visible label or an accessible name in the design spec, and the primary action is visually distinct from secondary actions.

8. **Tighten the visual system without rebranding.**  
   - Preserve the navy/ink neutral base and semantic amber/red statuses.  
   - Reduce nested cards, unnecessary shadows, and repeated borders.  
   - Establish a consistent spacing scale, likely tighter around related controls and larger only between major regions.  
   - Acceptance: body text is comfortably readable for long sessions, focus states are visible, and section hierarchy is conveyed through alignment, spacing, and typography rather than stacked decorative containers.

---

## 5. Bounded score

**Score band: 4–5 / 10 based on static evidence.**

Justification: the surface has the ingredients of an operations workspace — KPIs, charting, table, refresh, export, global navigation — but the described hierarchy, table affordances, accessibility gaps, and missing states are misaligned with the primary job of finding urgent exceptions in the next hour.

---

## 6. Smallest validation plan that could change the verdict

1. **First-viewport check on common desktop and narrow-laptop sizes.**  
   Verify whether the exception table header and initial rows are visible without scrolling.

2. **Keyboard-only task pass.**  
   Attempt: search/filter, reach table, identify highest-risk row, inspect status, trigger primary action, and return focus safely.

3. **Status and action comprehension check.**  
   Confirm whether users can understand row status and available actions without color, hover, or icon memorization.

4. **State review for operational trust.**  
   Inspect loading, empty, error, stale refresh, save/export failure, and partial-data states.

5. **Long-content and localization stress check.**  
   Test long product names, long owner names, translated labels, large financial values, and high row counts to see whether the triage path remains readable.
