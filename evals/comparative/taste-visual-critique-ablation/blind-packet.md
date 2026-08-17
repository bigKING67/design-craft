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

**Diagnosis — Static-description evidence only:** the surface reads like a generic analytics dashboard, not an hourly exception workspace, because actionable exceptions are visually delayed while low-urgency metrics, nested cards, and equal-weight chrome consume the first screen.

## 2. Blocking findings

1. **Primary workflow is below the fold.**  
   The exception table is the product’s decision surface, but it appears after KPI cards, an area chart, and generic insight cards; this directly conflicts with “find exceptions that need action in the next hour.”

2. **Urgency hierarchy is flat.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive equal card treatment and equal blue sparklines, so the screen does not distinguish “act now” from “monitor later.”

3. **The table is not optimized for triage.**  
   Product, issue, owner, deadline, financial impact, status, and action all use similar weight; analysts cannot quickly sort by severity, time pressure, ownership, or money at risk.

4. **Critical state and action cues are under-specified.**  
   Status appears as colored dots without text, and the action column uses three unlabeled icons; this weakens scan speed, interpretability, and keyboard/screen-reader confidence.

5. **Layout fragmentation reduces operational trust.**  
   Title, subtitle, date range, export, and refresh status are split across four weakly aligned rows, while every region has the same border/radius/shadow treatment; the page feels assembled rather than governed.

## 3. Secondary findings

1. **Header is over-weighted for this job.**  
   Six equal nav links, search, three icon buttons, and a bright blue Create button compete with exception review; “Create” sounds less relevant than “resolve,” “assign,” “snooze,” or “export.”

2. **Generic insight copy wastes analyst attention.**  
   “Monitor performance closely” is not decision-grade; insight panels should name the exception, expected impact, owner, and next action or be removed.

3. **Text density is high but not precise.**  
   12–13px low-contrast gray body text may fit density goals, but current contrast and hierarchy appear too weak for fast operational reading.

4. **Spacing rhythm is inconsistent.**  
   Gaps from 8px to 48px without a clear scale make the workspace harder to parse and undermine the calm, credible tone.

5. **Long-content and localization risk is visible from the description.**  
   Product names truncate at 24 characters, and long-translation states are not described, so important merchandising context may be hidden exactly where decisions happen.

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception table into the first screen.**  
   **Acceptance:** on a standard desktop workspace, the first viewport includes the page title/control bar, a compact exception summary, and the first several exception rows without requiring the analyst to pass through chart/insight content.

2. **Replace eight equal KPI cards with a triage strip.**  
   **Acceptance:** show 3–4 priority metrics only: revenue at risk, blocked SKUs, exceptions due within 60 minutes, and unresolved owner count; secondary metrics move to a collapsed “context” area or chart module.

3. **Create severity-first KPI hierarchy.**  
   **Acceptance:** revenue risk and blocked SKUs use stronger type, semantic amber/red where appropriate, and clear change labels; page views and general sell-through never receive the same visual weight as urgent exceptions.

4. **Collapse page metadata into one command bar.**  
   **Acceptance:** title, date range, refresh timestamp, export, and refresh action align on one or two rows with clear left/right grouping; refresh status reads as operational metadata, not a separate content row.

5. **Redesign the table for scan order.**  
   **Acceptance:** columns visually prioritize issue, financial impact, deadline/SLA, owner, and next action; product name supports at least two lines or an expandable detail affordance instead of hard 24-character truncation.

6. **Replace status dots with labeled status badges.**  
   **Acceptance:** every status has text plus color, e.g. “Blocked,” “At risk,” “Due soon,” “Assigned,” using preserved amber/red semantics and navy/ink neutrals; color is never the only status carrier.

7. **Make row actions explicit and workflow-aligned.**  
   **Acceptance:** the primary row action is a labeled button or text action such as “Review,” “Assign,” or “Resolve”; secondary actions can remain in an overflow menu with labels/tooltips, not three unexplained icons.

8. **Reduce nested card styling and establish a spacing system.**  
   **Acceptance:** only true containers use borders/shadows; inner modules rely on spacing, dividers, and typographic hierarchy; spacing follows a small scale such as 8/12/16/24/32px with no unexplained 48px jumps.

## 5. Score band

**Static-evidence score band: 45–55 / 100.**  
Justification: the described surface has credible enterprise ingredients—dense data, neutral system, semantic status colors, real table workflow—but the visual hierarchy currently points analysts toward dashboard consumption instead of immediate exception action.

## 6. Smallest validation plan that could change the verdict

Not performed; this is the minimum plan that could materially change the critique:

1. **Desktop first-screen check:** verify whether urgent exception rows are visible before scrolling at common desktop viewport heights.  
2. **Narrow-laptop check:** test the same workflow around 1280px wide to see whether header controls, command bar, and table columns remain usable.  
3. **State pass:** inspect loading, empty, error, stale-refresh, and no-exceptions states for the table and KPI strip.  
4. **Long-content pass:** test long product names, long issue names, long owner names, high financial-impact values, and translated status/action labels.  
5. **Keyboard/action pass:** confirm visible focus order through header, filters, table rows, status badges, and row actions.  
6. **Data-scale pass:** review table behavior with enough rows to represent a real analyst queue, including sorting or prioritization by deadline, impact, and status.


## Output B

## 1. Diagnosis — static evidence

The screen appears optimized for balanced dashboard presentation rather than the merchandising analyst’s urgent job of finding the next-hour exceptions, with priority, scan order, and action clarity weakened by equal-weight cards, nested containers, and a below-fold exception table.

**Evidence label:** Static product-surface description only.

---

## 2. Blocking findings

1. **Primary workflow is buried**
   - The exception table starts below the fold even though it is the core decision surface.
   - Revenue risk, blocked SKUs, owner, deadline, impact, status, and action need to be immediately scannable within the first viewport.

2. **Urgency hierarchy is flat**
   - Eight KPI cards treat revenue risk, blocked SKUs, sell-through, and yesterday’s page views as equally important.
   - Equal card size, equal sparklines, and similar typography prevent analysts from identifying what needs action now.

3. **Table lacks action-grade hierarchy**
   - Product, issue, owner, deadline, financial impact, status, and action use similar weight.
   - Status dots without labels and unlabeled action icons make the table too ambiguous for time-sensitive operations.

4. **Page chrome consumes too much attention**
   - Six equal nav links, global search, three icon buttons, and a bright blue “Create” button compete with the operational task.
   - The “Create” button sounds structurally important but may not be the primary action for exception triage.

5. **Generic insight area dilutes credibility**
   - Nested cards and vague copy like “Monitor performance closely” add noise without supporting concrete next-hour decisions.
   - This conflicts with the required tone: calm, credible, dense, and precise.

---

## 3. Secondary findings

1. **Header and page metadata are fragmented**
   - Title, subtitle, date range, export, and refresh status occupy four rows with weak alignment.
   - This increases vertical cost before the analyst reaches work.

2. **Visual system is over-containerized**
   - Every region having a border, 16px radius, and soft shadow creates unnecessary card noise.
   - Dense operations tools need fewer containers and stronger information grouping.

3. **Text is likely too small and low contrast for prolonged analysis**
   - 12–13px low-contrast gray body text weakens legibility, especially in tables and helper copy.
   - Dense does not mean faint.

4. **Long product names are mishandled**
   - Truncating at 24 characters can hide the differentiating part of a SKU or product family.
   - This is risky in merchandising where similar product names may differ only late in the string.

5. **State coverage is unspecified**
   - Empty, loading, error, focus, narrow-laptop, and long-translation states are absent from the description.
   - These states can materially change whether the workspace remains usable under real operations conditions.

---

## 4. Concrete redesign moves with acceptance criteria

1. **Promote the exception table into the first viewport**
   - Move the table above the large chart and generic insights.
   - **Acceptance criteria:** On a standard desktop workspace layout, the first viewport contains the header, compact page context, triage summary, table header, and at least the first several exception rows.

2. **Replace the eight equal KPI cards with a prioritized triage strip**
   - Lead with metrics tied to next-hour action: revenue risk, blocked SKUs, SLA/deadline breaches, and unresolved owner queue.
   - Demote yesterday’s page views and secondary performance metrics.
   - **Acceptance criteria:** The most urgent operational metric is visually dominant; no more than four primary metrics appear in the top triage row.

3. **Collapse page title, subtitle, date range, export, and refresh into one aligned command band**
   - Use one clear title line, one concise context line, and right-aligned controls.
   - **Acceptance criteria:** Page context uses one compact block rather than four separate rows; refresh status remains visible but not dominant.

4. **Reduce header competition**
   - Keep the navy/ink neutral system, but reduce equal emphasis across navigation, icons, search, and “Create.”
   - If “Create” is not part of exception handling, demote it to a secondary action.
   - **Acceptance criteria:** The header supports orientation and search without visually outranking the exception workflow.

5. **Rebuild table hierarchy around triage decisions**
   - Make issue, deadline, financial impact, and status more prominent than owner and generic metadata.
   - Use tabular alignment for money and deadlines.
   - **Acceptance criteria:** A row can be scanned left-to-right as: what product, what problem, how urgent, financial exposure, who owns it, what action is available.

6. **Replace status dots with labeled status treatments**
   - Preserve amber/red semantic colors, but add text such as “Blocked,” “At risk,” “Due <1h,” or “Escalated.”
   - **Acceptance criteria:** Status remains understandable without relying on color alone.

7. **Make actions explicit**
   - Replace three unlabeled icons with a primary row action plus secondary overflow where needed.
   - Example: “Review,” “Assign,” “Resolve,” or “Escalate,” depending on the real workflow.
   - **Acceptance criteria:** Each row has one obvious next action; secondary actions do not require icon interpretation.

8. **Remove vague insight cards and keep only decision-supporting analysis**
   - Replace “Monitor performance closely” style copy with specific exception explanations, thresholds, or recommended next steps.
   - **Acceptance criteria:** Every insight names the affected SKU/group, the triggering condition, impact, and suggested owner/action—or it is removed.

---

## 5. Static score band

**Score band: 4–5 / 10 for this product surface as described.**

Justification: the visual system sounds coherent enough to be usable as a dashboard, but the primary operations job is structurally deprioritized. The table is below the fold, urgency cues are weak, actions are ambiguous, and the screen spends too much space on equal-weight KPIs and generic insight cards.

---

## 6. Smallest validation plan that could change the verdict

1. **First-viewport check**
   - Confirm whether exception rows are visible without scrolling at common desktop and narrow-laptop sizes.

2. **Triage task pass**
   - Give an analyst one prompt: “Find the highest-risk exception to act on in the next hour.”
   - Measure whether the answer can be reached from the first viewport and whether the next action is clear.

3. **Table stress states**
   - Check long product names, long translations, high financial-impact values, missing owners, overdue deadlines, and mixed amber/red statuses.

4. **State coverage check**
   - Review loading, empty, error, and refresh-failure states for the table and KPI areas.

5. **Keyboard and focus pass**
   - Confirm that table actions, filters, search, export, and refresh can be reached and understood through visible focus order.


## Output C

## 1. Diagnosis

**Diagnosis — Evidence: static product-description only.** The screen is visually organized around generic dashboard furniture instead of the analyst’s urgent decision flow: identify high-impact merchandising exceptions, understand ownership/deadline, and act within the next hour.

## 2. Blocking findings

1. **Primary task is buried.** The exception table starts below the fold even though it is the operational surface’s core work queue; summary cards and generic chart content consume the first screen.
2. **Priority hierarchy is flat.** Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive equal card weight, equal sparkline treatment, and similar typography, so urgent exceptions do not visually outrank ambient monitoring.
3. **Table scanability is too weak for hourly action.** Product, issue, owner, deadline, financial impact, status, and action use similar weight; long product names truncate early; financial impact and deadline do not appear visually dominant.
4. **Status and actions are under-specified.** Color-only dots and three unlabeled action icons make state and next step ambiguous, especially in a dense operations context where speed and confidence matter.
5. **State and resilience coverage is missing.** Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are not described, so the surface cannot yet be judged reliable under real operational conditions.

## 3. Secondary findings

1. **Header is over-equalized.** Six equal nav links, global search, three icon buttons, and a bright blue Create button compete with the exception workflow; “Create” may be louder than “act on exception.”
2. **Page controls lack a single command row.** Title, subtitle, date range, export, and refresh status occupying four rows creates weak alignment and slows orientation.
3. **Nested card structure adds noise.** A pale card containing another chart card plus three more insight cards creates visual bureaucracy without improving decision quality.
4. **Generic insight copy reduces trust.** “Monitor performance closely” does not name affected products, thresholds, owners, impact, or the action path.
5. **Surface treatment is overused.** Borders, 16px radii, and soft shadows on every region flatten hierarchy; everything looks equally containerized instead of operationally ranked.

## 4. Concrete redesign moves with acceptance criteria

1. **Make the exception queue the first-screen anchor.**  
   Acceptance: at 1440×900 and 1366×768 planning targets, the table header and at least the first 5–8 exception rows are visible without scrolling; summary modules move beside or below the queue.

2. **Replace eight equal KPI cards with a triage summary strip.**  
   Acceptance: top metrics are grouped by action relevance: `Needs action now`, `Financial exposure`, `Blocked SKUs`, and `Trend/watchlist`; yesterday’s page views becomes secondary metadata unless tied to an exception.

3. **Create one aligned page command bar.**  
   Acceptance: title, date range, refresh status, export, and any primary workflow action sit on one coherent grid; refresh status is timestamped and subdued; export is secondary unless it is part of the hourly workflow.

4. **Redesign the table for decision-first scanning.**  
   Acceptance: product name supports two-line wrapping before truncation; issue and impact are visually paired; financial impact uses tabular/right-aligned numbers; deadline uses urgency treatment; owner remains scannable but secondary.

5. **Replace dot-only status with labeled semantic badges.**  
   Acceptance: every status includes text plus amber/red semantic color, e.g. `Blocked`, `Due <1h`, `At risk`, `Escalated`; color is never the only state cue.

6. **Replace unlabeled icon actions with explicit row actions.**  
   Acceptance: the primary row action is text-labeled, such as `Review`, `Assign`, or `Resolve`; secondary actions can sit in an overflow menu with accessible labels and visible focus states.

7. **Remove generic insight cards or make them actionable exception summaries.**  
   Acceptance: each insight names a product/segment, threshold, count, impact, owner or recommended next step, and links directly to a filtered table state.

8. **Normalize density, type, spacing, and surfaces.**  
   Acceptance: decision-bearing body/table text uses at least a readable dense-product baseline around 14px/1.4; muted text meets normal-text contrast expectations; spacing follows a small rhythm such as 8/12/16/24/32; shadows are reserved for true overlays or active elevation, not every card.

## 5. Score band

**Static score band: 58–66 / 100.** The screen sounds functional and data-rich, but the static evidence shows major task-focus, hierarchy, table-action, status-clarity, and state-resilience gaps. I would not assign a narrower score without rendered layout, real data density, interaction states, and responsive evidence.

## 6. Smallest validation plan that could change the verdict

1. **Baseline rendered layout check:** inspect the current first fold at 1440×900 and 1366×768; verify whether the exception queue is actually below the fold and how many rows are visible.
2. **Computed readability check:** sample body, table, helper, status, and action text sizes/contrast; confirm whether 12–13px low-contrast text affects decision-bearing content.
3. **Keyboard path check:** tab through header, filters/date range, table rows, status, and row actions; confirm visible focus and whether unlabeled icons expose clear names.
4. **State check:** view loading, empty, error, long product name, long translation, high-impact exception, and no-owner/deadline-missed rows.
5. **Narrow-laptop check:** test 1280×720 or comparable constrained desktop; confirm the command bar, table columns, row actions, and horizontal overflow strategy remain usable.
