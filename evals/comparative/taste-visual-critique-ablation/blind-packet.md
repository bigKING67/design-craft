# Blind comparative judgment
Judge only the supplied outputs. Do not infer which skill produced a label. Apply the machine-readable scorecard exactly, recompute each total from criterion points, and return only JSON matching the supplied schema.

## Task prompt

# Operations workspace visual critique

Critique the following static product-surface description. Do not edit files,
invent screenshots, or claim browser, DOM, responsive, accessibility-tree, or
runtime validation. Do not name, cite, or reveal any skill, repository, author,
or upstream source in the response; the output will be judged blind.

Product authority:

- Desktop Web operations workspace for merchandising analysts.
- Primary job: find the exceptions that need action in the next hour.
- Tone: calm, credible, dense, and precise; not a marketing page.
- Preserve the existing navy/ink neutral system and semantic amber/red status
  colors. No gradients, glass, or decorative illustration.
- Preserve the table's real data and current workflows rather than proposing a
  ground-up rebrand.

Current screen:

- A 64px header contains a logo, six equal navigation links, global search,
  three icon buttons, and a bright blue "Create" button.
- The page title, subtitle, date range, export action, and refresh status occupy
  four separate rows with weak alignment.
- Eight identical KPI cards use the same height, 12px uppercase labels, 28px
  numbers, gray helper copy, and equal blue sparklines. Revenue risk, blocked
  SKUs, sell-through, and yesterday's page views receive equal emphasis.
- A large pale card contains another card for an area chart; below it, three
  nested cards show generic "insights" such as "Monitor performance closely."
- The exception table starts below the fold. Product, issue, owner, deadline,
  financial impact, status, and action all use similar text weight. Status is
  shown by small colored dots without text. Long product names truncate at 24
  characters. The action column uses three unlabeled icons.
- Body text is 12-13px with low-contrast gray. Section gaps range from 8px to
  48px without a clear rhythm. Every region has a border, 16px radius, and soft
  shadow.
- Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation
  states are not described.

Return:

1. One-sentence diagnosis and an evidence label.
2. At most five blocking findings and five secondary findings.
3. At most eight concrete redesign moves with acceptance criteria.
4. A bounded score or score band only if justified by the static evidence.
5. The smallest browser/responsive/state validation plan that could change the
   verdict.

Stay within 150 lines and keep the recommendations specific to this product,
its authority, and its decision flow.


## Human-readable scorecard

# Comparative scorecard

Generated from `scorecard.json`; do not edit by hand.

| Criterion | Weight | Full credit |
|---|---:|---|
| Product hierarchy and decision flow | 15 | Reorders attention around next-hour exceptions and separates lead, support, and historical information. |
| Anti-generic visual judgment | 15 | Identifies card soup, fake insight copy, equal emphasis, and decorative defaults without imposing another generic aesthetic. |
| Typography, color, and surface craft | 15 | Gives specific readable type, semantic color, spacing, border, elevation, and scanability corrections. |
| Product fit and authority | 15 | Preserves the operations job, data, workflows, and stated visual authority rather than rebranding. |
| Concrete redesign moves | 20 | Supplies prioritized implementation-ready moves and observable acceptance criteria across the full surface. |
| Evidence honesty | 10 | Labels static evidence, avoids runtime invention, and names the smallest decisive validation plan. |
| Scope, prioritization, and output discipline | 10 | Stays read-only and within the requested finding, move, and line budgets with clear priorities. |
| **Total** | **100** | |


## Machine-readable scorecard

```json
{
  "schema": "design-craft.comparative-scorecard.v1",
  "total": 100,
  "criteria": [
    {
      "id": "product_hierarchy",
      "label": "Product hierarchy and decision flow",
      "weight": 15,
      "full_credit": "Reorders attention around next-hour exceptions and separates lead, support, and historical information."
    },
    {
      "id": "anti_generic",
      "label": "Anti-generic visual judgment",
      "weight": 15,
      "full_credit": "Identifies card soup, fake insight copy, equal emphasis, and decorative defaults without imposing another generic aesthetic."
    },
    {
      "id": "visual_craft",
      "label": "Typography, color, and surface craft",
      "weight": 15,
      "full_credit": "Gives specific readable type, semantic color, spacing, border, elevation, and scanability corrections."
    },
    {
      "id": "product_fit",
      "label": "Product fit and authority",
      "weight": 15,
      "full_credit": "Preserves the operations job, data, workflows, and stated visual authority rather than rebranding."
    },
    {
      "id": "concrete_moves",
      "label": "Concrete redesign moves",
      "weight": 20,
      "full_credit": "Supplies prioritized implementation-ready moves and observable acceptance criteria across the full surface."
    },
    {
      "id": "evidence_honesty",
      "label": "Evidence honesty",
      "weight": 10,
      "full_credit": "Labels static evidence, avoids runtime invention, and names the smallest decisive validation plan."
    },
    {
      "id": "scope_discipline",
      "label": "Scope, prioritization, and output discipline",
      "weight": 10,
      "full_credit": "Stays read-only and within the requested finding, move, and line budgets with clear priorities."
    }
  ]
}
```

## Required judgment schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["results", "winner", "rationale"],
  "properties": {
    "results": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": {
        "type": "object",
        "required": ["label", "criteria", "total", "summary"],
        "properties": {
          "label": {"enum": ["A", "B", "C"]},
          "criteria": {
            "type": "object",
            "required": [
              "product_hierarchy",
              "anti_generic",
              "visual_craft",
              "product_fit",
              "concrete_moves",
              "evidence_honesty",
              "scope_discipline"
            ],
            "additionalProperties": false,
            "properties": {
              "product_hierarchy": {"type": "integer", "minimum": 0, "maximum": 15},
              "anti_generic": {"type": "integer", "minimum": 0, "maximum": 15},
              "visual_craft": {"type": "integer", "minimum": 0, "maximum": 15},
              "product_fit": {"type": "integer", "minimum": 0, "maximum": 15},
              "concrete_moves": {"type": "integer", "minimum": 0, "maximum": 20},
              "evidence_honesty": {"type": "integer", "minimum": 0, "maximum": 10},
              "scope_discipline": {"type": "integer", "minimum": 0, "maximum": 10}
            }
          },
          "total": {"type": "integer", "minimum": 0, "maximum": 100},
          "summary": {"type": "string", "minLength": 20}
        },
        "additionalProperties": false
      }
    },
    "winner": {"enum": ["A", "B", "C"]},
    "rationale": {"type": "string", "minLength": 40}
  },
  "additionalProperties": false
}
```

## Output A

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


## Output B

1. **Diagnosis — Evidence: supplied static description + product authority only.** The screen is visually tidy but fails the analyst’s primary job because attention is spent on equalized dashboard furniture before the actionable exception queue.

## Blocking findings

1. **The exception workflow is below the fold.** The table is the primary object for “exceptions needing action in the next hour,” but it appears after header rows, KPI grid, chart card, and insight cards.
2. **Priority is flattened.** Revenue risk, blocked SKUs, sell-through, and page views receive the same KPI treatment, so urgent operational risk cannot outcompete routine telemetry.
3. **The table does not support fast triage.** Product, issue, owner, deadline, impact, status, and action have similar weight; long product names truncate; status dots are color-only; row actions are unlabeled icons.
4. **The command area is fragmented.** Title, subtitle, date range, export, and refresh status occupy four weakly aligned rows, while a bright global “Create” button competes with exception handling.
5. **Resilience states are unspecified.** Empty, loading, error, keyboard focus, narrow-laptop, and long-translation states are not described, which is a blocker for a dense operations surface.

## Secondary findings

1. **Over-cardification reduces density.** Repeated borders, 16px radii, and soft shadows on every region make hierarchy depend on decoration rather than structure.
2. **Generic insight copy is not operational.** “Monitor performance closely” does not name an entity, threshold, impact, owner, or next action.
3. **Typography is too timid for decision data.** 12–13px low-contrast gray body text is risky for deadlines, impact, status, and row actions.
4. **Spacing lacks a rhythm.** Gaps ranging from 8px to 48px without a clear scale make relationships ambiguous.
5. **The chart’s job is unclear.** A large chart module appears before the exception table without a stated operational question or action path.

## Concrete redesign moves with acceptance criteria

1. **Collapse the page command band.**  
   Acceptance: title, scope/date range, refresh status, and export live in one compact aligned band; global “Create” is visually secondary unless creation is part of exception resolution.

2. **Move the exception queue into the first viewport.**  
   Acceptance: on a standard desktop/laptop composition, analysts see the top exception rows or a “Needs action next hour” queue before historical charts or generic insights.

3. **Replace the equal KPI grid with priority tiers.**  
   Acceptance: revenue risk and blocked SKUs become the dominant operational summary; sell-through is supporting context; page views move to a diagnostic tier or lower section.

4. **Make every KPI comparative and semantic.**  
   Acceptance: each retained KPI answers “compared to what?” with period, threshold, or target; amber/red are reserved for warning/danger states, not decorative sparklines.

5. **Rebuild the table as a triage surface.**  
   Acceptance: row scan order exposes product identity, issue severity/status text, deadline/SLA, financial impact, owner, and next action; impact is right-aligned; decision-bearing text is at least a readable dense-table role, not muted metadata.

6. **Replace ambiguous status dots and icon-only actions.**  
   Acceptance: status uses text labels plus semantic color; actions have visible verb-object labels such as “Assign owner,” “Resolve block,” or “Review SKU”; keyboard focus is visibly distinct.

7. **Remove or harden the insight cards.**  
   Acceptance: an insight remains only if it names the SKU/segment, observed threshold/change, business impact, owner or recommended action, and provides a direct route into the filtered table.

8. **Simplify the surface system and state contract.**  
   Acceptance: use fewer nested cards, subtler dividers, consistent spacing steps, restrained shadows only for true elevation, WCAG-level normal-text contrast, designed loading/empty/error/long-name/long-translation/focus/narrow-laptop variants.

## Static score band

**55–65 / 100, static-only.** The screen sounds coherent and systemized, but the supplied evidence shows a major task-order failure, weak hierarchy, inaccessible/status-ambiguous table behavior, over-cardification, and missing production states. A higher score would require evidence that the exception queue, states, keyboard flow, and narrow-laptop layout work under real content.

## Smallest validation plan that could change the verdict

1. Render the revised surface at desktop and narrow-laptop sizes, especially around 1440×900 and 1366×768.  
2. Confirm the exception queue/table is visible before charts and that command metadata does not wrap into multiple weak rows.  
3. Test rows with long product names, long translated labels, high financial impact, urgent deadlines, and no-owner cases.  
4. Exercise loading, empty, error, stale-refresh, and partial-data states near the affected module.  
5. Tab through search, date range, export, table rows, status, and row actions to verify visible focus and discoverable labels.


## Output C

## 1. Diagnosis — **[Static evidence only]**

The screen is organized like a generic analytics dashboard rather than an exception-finding workspace, so the highest-value next-hour decisions are visually delayed, underweighted, and harder to scan than lower-priority reporting content.

---

## 2. Blocking findings

1. **Primary workflow is below the fold**
   - The exception table is the core job surface, but it starts below KPI cards, a chart card, and generic insight cards.
   - For analysts trying to act within the next hour, this makes discovery slower and privileges review over action.

2. **Priority hierarchy is flattened**
   - Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive equal KPI treatment.
   - Equal card size, equal sparklines, and similar typography fail to distinguish “needs action now” from “contextual metric.”

3. **The page header and title area consume attention without improving decisions**
   - Six equal nav links, search, three icon buttons, and a bright blue “Create” button compete with exception triage.
   - The page title, subtitle, date range, export action, and refresh status are split across four rows with weak alignment, increasing scan cost before any action data appears.

4. **Exception table does not expose urgency clearly enough**
   - Product, issue, owner, deadline, financial impact, status, and action have similar text weight.
   - Small status dots without text, 24-character truncation, and unlabeled action icons make the table less reliable for fast triage.

5. **Generic card nesting dilutes operational credibility**
   - A pale outer card, inner chart card, and three nested “insight” cards add visual mass without clear decision value.
   - Copy like “Monitor performance closely” is too vague for a merchandising analyst deciding what to fix now.

---

## 3. Secondary findings

1. **Typography is too small and low-contrast for dense repeated use**
   - 12–13px low-contrast body text may be fatiguing on a desktop operations surface, especially in table-heavy workflows.

2. **Spacing lacks a production rhythm**
   - Gaps ranging from 8px to 48px without a clear system make related elements feel randomly grouped.

3. **Every region has the same container treatment**
   - Borders, 16px radius, and soft shadows on every section flatten hierarchy and create unnecessary visual noise.

4. **Semantic color is underused**
   - Amber/red are available status colors, but the current status treatment appears too small and nonverbal to carry operational meaning.

5. **Critical states are unspecified**
   - Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are not described, which leaves the main workflow unproven under realistic operating conditions.

---

## 4. Concrete redesign moves with acceptance criteria

1. **Move exceptions into the first viewport**
   - Place the exception queue directly below a compact page command row.
   - **Acceptance:** On a standard desktop workspace viewport, the user can see the table header and at least the first 6–8 exception rows without scrolling.

2. **Replace the eight equal KPI cards with a triage summary strip**
   - Promote only next-hour decision metrics: revenue at risk, blocked SKUs, overdue exceptions, and due-within-hour.
   - Demote yesterday’s page views and broad sell-through into secondary context or a collapsible summary.
   - **Acceptance:** The top summary has one primary risk metric, two to three supporting exception metrics, and no equal-emphasis decorative sparklines unless they directly explain urgency.

3. **Create a single aligned page command bar**
   - Combine title, date range, refresh status, export, and primary filters into one structured area.
   - Keep refresh status visible but quiet.
   - **Acceptance:** Page title, active date/window, last updated state, and export action align on one baseline or two clearly related rows, not four separate bands.

4. **Rebalance the global header**
   - Reduce the visual dominance of the bright blue “Create” button unless creation is part of exception resolution.
   - Group secondary icon buttons and avoid making all six nav items equal if one section is current.
   - **Acceptance:** Current workspace location is unmistakable; the primary visible action relates to resolving or reviewing exceptions, not generic creation.

5. **Redesign the table for urgency-first scanning**
   - Use stronger hierarchy for issue, deadline, impact, and owner.
   - Add textual status labels beside color: for example, “Blocked,” “At risk,” “Due soon,” “Resolved.”
   - **Acceptance:** A row can be understood without relying on color alone, and the highest-risk row is identifiable from issue, deadline, impact, and status within one horizontal scan.

6. **Stop truncating product identity too aggressively**
   - Allow product names to wrap to two lines or pair a short name with SKU/vendor metadata.
   - Preserve full value via hover/focus disclosure if truncation remains.
   - **Acceptance:** Common long product names remain distinguishable without opening a detail view; truncation never removes the differentiating part of the item name.

7. **Replace unlabeled icon actions with explicit operational actions**
   - Use text buttons or icon+label actions such as “Assign,” “Snooze,” “Fix,” “Open.”
   - Reserve icon-only controls for repeated expert actions with accessible names and visible tooltips/focus labels.
   - **Acceptance:** The primary row action is readable without guessing; secondary actions are grouped under a labeled overflow if space is constrained.

8. **Simplify containers and remove generic insights**
   - Use fewer cards, lighter dividers, and tighter grouping.
   - Replace generic insight cards with actionable exception summaries, such as “12 blocked SKUs have no owner” or “$48k risk due before 2 PM.”
   - **Acceptance:** Every non-table module either helps prioritize the exception queue or can be removed without harming the next-hour workflow.

---

## 5. Static score band

**Score band: 45–55 / 100 based on static evidence only.**

Justification: the surface has recognizable dashboard components and relevant data categories, but the static description shows a major mismatch between the product’s primary job — finding exceptions needing action soon — and the current hierarchy, table placement, status encoding, and action clarity.

---

## 6. Smallest validation plan that could change the verdict

1. **Desktop first-viewport check**
   - Verify whether the exception table header and initial rows appear without scrolling on common analyst laptop and desktop sizes.

2. **Triage task test**
   - Ask users to identify the top three exceptions needing action in the next hour using only the visible screen state.

3. **Table comprehension check**
   - Validate whether users can understand status, urgency, owner, deadline, impact, and next action without tooltips or color-only interpretation.

4. **State coverage review**
   - Inspect empty, loading, error, stale-refresh, long-product-name, long-translation, and no-results states for the exception workflow.

5. **Keyboard path check**
   - Confirm that search, filters, table rows, status controls, and row actions can be reached and understood in a logical keyboard order.
