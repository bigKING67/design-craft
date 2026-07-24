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


## Output B

1. **Diagnosis — [Static description only]:** The surface has credible operations ingredients, but its hierarchy is inverted: the urgent exception workflow is pushed below decorative/secondary summary content, while critical table signals are visually and semantically under-specified.

2. **Blocking findings**

- **Primary job is below the fold.** For a workspace whose job is “find exceptions needing action in the next hour,” the exception table should be the center of gravity, not placed after KPI cards, a chart card, and generic insight cards.
- **Urgency and impact are not visually rankable.** Revenue risk, blocked SKUs, sell-through, and page views receive equal KPI treatment, making operational risk compete with background metrics.
- **The table cannot support fast triage.** Product, issue, owner, deadline, financial impact, status, and action use similar weight, so the analyst has to read every cell instead of scanning for severity, deadline, and next action.
- **Status and actions are too opaque.** Small colored dots without text and three unlabeled action icons are weak for speed, accessibility, translation, and error prevention.
- **Density is achieved at the cost of legibility.** 12–13px low-contrast body text, 24-character product truncation, and uniform card shadows/radii reduce precision in a data-heavy operations surface.

3. **Secondary findings**

- **Header has too many equal competitors.** Six equal nav links, global search, three icon buttons, logo, and a bright “Create” button create a broad control band without clear relevance to exception response.
- **Page metadata is fragmented.** Title, subtitle, date range, export, and refresh status across four rows weakens alignment and wastes vertical space.
- **Nested cards dilute authority.** A pale card containing another chart card, followed by three more cards, adds visual ceremony without improving the next-hour decision.
- **Insight copy is generic.** “Monitor performance closely” does not meet the product’s tone of dense, precise operational guidance.
- **State coverage is absent.** Empty, loading, error, focus, narrow-laptop, and long-translation states are not defined, so the design is not yet production-resilient.

4. **Concrete redesign moves with acceptance criteria**

- **Move the exception queue above the fold.**  
  Acceptance: at 1366×768, the analyst can see the page title, exception summary, table header, and at least 6–8 actionable rows without scrolling.

- **Replace eight equal KPIs with a triage strip.**  
  Acceptance: show 3–4 prioritized operational measures first: `Revenue at risk`, `Blocked SKUs`, `Missed deadline / due <1h`, and `Owner coverage`; demote page views and similar context metrics to a secondary area.

- **Collapse the four page-title rows into one command bar.**  
  Acceptance: title + concise subtitle align left; date range, export, last refreshed, and refresh action align right in one or two predictable rows with a consistent baseline.

- **Flatten the chart/insight region.**  
  Acceptance: remove nested card-on-card treatment; keep one compact trend module only if it explains exception volume, revenue risk, or deadline pressure; otherwise place it below the table.

- **Make table hierarchy operational.**  
  Acceptance: first columns prioritize `Issue severity`, `Product`, `Financial impact`, `Deadline`, `Owner`, `Status`, `Action`; use stronger weight for issue/deadline/impact and quieter treatment for supporting metadata.

- **Replace dot-only status with labeled status chips.**  
  Acceptance: every status has visible text such as `Blocked`, `Needs review`, `Escalated`, `Ready`, with existing amber/red semantics preserved and not dependent on color alone.

- **Replace unlabeled icon actions with explicit primary actions.**  
  Acceptance: each row has one clear primary text action, e.g. `Resolve`, `Assign`, `Escalate`, or `Review`; secondary actions can sit behind a labeled overflow menu.

- **Tighten the visual system for dense use.**  
  Acceptance: body text is no smaller than a legible operations baseline, contrast is increased, product names have a predictable two-line or expandable treatment, shadows are reduced, and spacing follows a small set of repeated increments.

5. **Bounded score**

**4–5 / 10 based on static evidence.**  
The surface has the right domain objects and a restrained navy/neutral/status-color direction, but the decision flow, scan hierarchy, table affordances, and state planning are not yet strong enough for a next-hour exception workspace.

6. **Smallest validation plan that could change the verdict**

- Review the redesigned first viewport at **1366×768** and **1280×720** to confirm the exception queue is visible without scrolling.
- Test with realistic data: long product names, multiple urgent deadlines, high financial impact values, missing owners, and mixed statuses.
- Check keyboard flow for header controls, table rows, row actions, export, refresh, and focus visibility.
- Verify loading, empty, error, stale-refresh, and no-results states for the table.
- Test long translated labels in nav, status chips, KPI labels, and row actions.
- Confirm that status/action meaning remains clear without relying on color or icon-only controls.


## Output C

## 1. Diagnosis + evidence label

**Diagnosis:** The screen reads like a generic analytics dashboard, but the product job is an exception-triage workspace; the current hierarchy delays action, equalizes unequal signals, and hides the table where decisions actually happen.  
**Evidence label:** Static description only — no browser, DOM, responsive, accessibility-tree, or runtime validation performed.

---

## 2. Blocking findings

1. **The primary decision surface starts below the fold.**  
   For analysts trying to find exceptions needing action in the next hour, the exception table should be the dominant first-screen object, not something discovered after KPI cards, chart cards, and insight cards.

2. **Severity is visually flattened.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive similar card treatment, type scale, and blue sparklines, which makes urgent operational risk look equivalent to passive reporting.

3. **The table does not support fast triage.**  
   Product, issue, owner, deadline, impact, status, and action use similar weight; status is color-dot-only; product names truncate too aggressively; and action icons are unlabeled. This forces interpretation instead of enabling immediate decisions.

4. **Nested cards and repeated chrome compete with the work.**  
   A pale card containing another chart card, followed by three more cards, creates dashboard ornamentation and vertical drag without clearly advancing the “what needs action now?” flow.

5. **Critical interaction and failure states are unspecified.**  
   Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are absent, so the surface cannot yet be judged production-ready for repeated operations use.

---

## 3. Secondary findings

1. **The header is over-weighted for a task workspace.**  
   Six equal nav links, global search, three icon buttons, and a bright blue “Create” button compete with the exception workflow.

2. **Page context is fragmented across too many rows.**  
   Title, subtitle, date range, export, and refresh status occupying four rows weakens alignment and consumes space that should expose exceptions.

3. **Typography is too small and low-contrast for sustained scanning.**  
   12–13px gray body text may be dense, but it risks fatigue and missed urgency in a high-repetition operational surface.

4. **Spacing lacks a governing rhythm.**  
   Gaps from 8px to 48px without clear hierarchy make the page feel assembled rather than intentionally prioritized.

5. **Generic “insights” copy undermines credibility.**  
   Text like “Monitor performance closely” does not match the precise operational tone and should be replaced with specific exception explanations or removed.

---

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception table into the first screen.**  
   - Redesign the page so the exception queue begins immediately after a compact command/context band.  
   - **Acceptance:** On a typical desktop workspace, the table header and at least the first several exception rows are visible without scrolling.

2. **Replace the eight equal KPI cards with a priority strip.**  
   - Show only the metrics that change next-hour action: blocked SKUs, revenue at risk, deadlines due soon, unresolved owner gaps.  
   - Demote passive metrics such as yesterday’s page views to a secondary analytics area.  
   - **Acceptance:** A reviewer can identify the top operational risk in under five seconds from the first screen.

3. **Give status semantic text, not just dots.**  
   - Use preserved amber/red semantics, but pair color with explicit labels such as “Blocked,” “Due soon,” “Overdue,” “Owner needed,” or “At risk.”  
   - **Acceptance:** Status remains understandable if color is unavailable or ambiguous.

4. **Rebuild the table hierarchy around triage decisions.**  
   - Product name: allow two-line wrapping or a structured primary/secondary line.  
   - Issue: make it more prominent than owner metadata.  
   - Deadline and financial impact: use stronger weight when urgent or high-value.  
   - Action: use labeled primary actions rather than three unlabeled icons.  
   - **Acceptance:** Each row answers: what is wrong, how urgent is it, what is the impact, who owns it, and what can I do next?

5. **Collapse charting into evidence, not decoration.**  
   - If the area chart remains, make it explain the selected exception set or risk trend. Otherwise move it below the table.  
   - Remove generic insight cards unless they contain specific, attributable operational findings.  
   - **Acceptance:** Every chart or insight directly explains a current exception, escalation, or risk driver.

6. **Create a compact command row for page context.**  
   - Combine title, date range, refresh status, export, and relevant filters into one aligned band.  
   - Keep the tone calm and precise; avoid promotional emphasis.  
   - **Acceptance:** Page context uses one stable visual row, with refresh/export secondary to exception discovery.

7. **Reduce visual chrome and standardize rhythm.**  
   - Keep the navy/ink neutral system and semantic amber/red, but reduce repeated borders, shadows, and identical 16px-radius cards.  
   - Use a consistent spacing scale, with tighter spacing around related controls and larger gaps only between major work zones.  
   - **Acceptance:** The page has fewer competing containers, and hierarchy is carried by type, alignment, and density rather than repeated card styling.

8. **Specify operational states before judging final quality.**  
   - Define loading skeletons for KPI/table data, empty states for no exceptions, error states for stale or failed data, long-name behavior, keyboard focus states, and narrow-laptop compression.  
   - **Acceptance:** The same triage workflow remains usable when data is missing, delayed, long, translated, or navigated by keyboard.

---

## 5. Bounded score

**Static evidence score band: 45–55 / 100.**  
Justification: the surface has recognizable operational ingredients — header, KPIs, chart, table, status, actions — but the hierarchy is inverted for the stated job, urgency is flattened, the table is under-designed, and essential production states are unspecified. The score could rise materially if the actual implementation handles keyboard flow, responsive density, state recovery, and table interaction better than the description indicates.

---

## 6. Smallest validation plan that could change the verdict

1. **Desktop first-screen check:** verify whether the exception table is visible without scrolling on a common analyst laptop viewport.  
2. **Keyboard pass:** tab through search, filters/date range, table rows, statuses, and actions; confirm visible focus and understandable action names.  
3. **State pass:** inspect loading, empty, data-error, stale-refresh, and no-permission states for the table and priority metrics.  
4. **Long-content pass:** test long product names, long owner names, high financial values, and translated labels.  
5. **Narrow-laptop pass:** check whether the command row, KPI strip, and table preserve triage priority without hiding critical columns.  
6. **Color-independence pass:** confirm amber/red statuses are paired with text and do not rely on dots alone.
