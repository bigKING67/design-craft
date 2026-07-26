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

**Diagnosis — Static-evidence verdict:** The surface reads as a generic analytics dashboard, not an exception-first merchandising workspace; the primary decision object — “what needs action in the next hour” — is visually delayed, under-weighted, and harder to act on than low-priority summary content.

---

## 2. Blocking findings

1. **Primary workflow is below the fold.**  
   The exception table starts after header chrome, fragmented page controls, eight KPI cards, a large chart card, and three insight cards, so analysts must scan past non-actionable content before reaching the work queue.

2. **Urgency is flattened across metrics.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive equal card treatment and identical blue sparklines, which obscures which signals are operationally urgent.

3. **Table hierarchy does not support fast triage.**  
   Product, issue, owner, deadline, financial impact, status, and action all use similar weight, making it hard to distinguish severity, money at risk, due time, and next step.

4. **Critical state is encoded too weakly.**  
   Status is shown only as small colored dots, and actions are three unlabeled icons. That is too ambiguous for a dense operations console where mistakes and hesitation are costly.

5. **Navigation and page controls consume too much attention.**  
   A 64px header with six equal nav links, search, three icon buttons, and a bright blue Create button competes with the exception workflow. The title, date, export, and refresh status then occupy four more weakly aligned rows.

---

## 3. Secondary findings

1. **Nested cards and repeated shadows reduce density.**  
   A pale card containing another chart card, plus three nested insight cards, adds visual ceremony without improving exception resolution.

2. **Generic insight copy lacks operational value.**  
   Text like “Monitor performance closely” does not tell an analyst what changed, what is at risk, who owns it, or what action to take.

3. **Spacing rhythm is inconsistent.**  
   Gaps ranging from 8px to 48px without an evident system make the page feel assembled rather than instrumented.

4. **Text treatment is too quiet for long sessions.**  
   12–13px low-contrast gray body text may suit helper copy, but it is too weak for product names, deadlines, impact values, and status language.

5. **Unspecified production states are a risk.**  
   Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are not described, so the design cannot yet be trusted under real operational conditions.

---

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception queue into the first viewport.**  
   **Acceptance criteria:** On a 1366×768 desktop viewport, the analyst can see the page title/context, primary filters, refresh state, and the start of the exception table without scrolling; at least 6–10 actionable rows are visible depending on row density.

2. **Replace the fragmented page header with one aligned command bar.**  
   Combine title, date range, refresh status, export, and key filters into a single structured row below the global header.  
   **Acceptance criteria:** Page-level controls occupy one row, align to a clear grid, and do not push the table below the fold.

3. **Demote non-urgent navigation and creation affordances.**  
   Keep global navigation, but reduce equal emphasis across six links and reconsider the bright blue “Create” button if creation is not the dominant hourly task.  
   **Acceptance criteria:** The highest-contrast action on the page relates to exception review or resolution, not generic creation.

4. **Reduce eight KPI cards to a triage summary strip.**  
   Prioritize revenue risk, blocked SKUs, urgent deadlines, and exception count. Move page views and lower-priority trend metrics to secondary placement.  
   **Acceptance criteria:** The first summary row answers: “How many exceptions? How much money at risk? How many are due soon? What is blocked?” within one glance.

5. **Use semantic status language, not dots alone.**  
   Replace dot-only statuses with compact text badges such as “Blocked,” “At risk,” “Due <1h,” “Awaiting owner,” preserving amber/red semantics.  
   **Acceptance criteria:** Every status remains understandable without relying on color alone.

6. **Rebuild the table around decision priority.**  
   Make issue severity, deadline, and financial impact visually stronger than owner and metadata. Allow product names to wrap to two lines with SKU or channel as secondary text instead of truncating at 24 characters.  
   **Acceptance criteria:** A reviewer can identify the top three most urgent rows by severity, deadline, and impact without opening details.

7. **Replace icon-only row actions with explicit actions.**  
   Use labeled actions such as “Assign,” “Resolve,” “Escalate,” or a primary “Review” button with a secondary overflow menu.  
   **Acceptance criteria:** No destructive, status-changing, or workflow-critical row action is represented only by an unlabeled icon.

8. **Replace generic insights with actionable exception summaries.**  
   Convert “Monitor performance closely” cards into statements like “14 red exceptions due in 60 minutes,” “$48.2k risk concentrated in 3 SKUs,” or “5 blocked items missing owner,” each linking to a filtered table view.  
   **Acceptance criteria:** Every insight names a count, severity, business impact, owner gap, or deadline and changes the table filter when selected.

---

## 5. Score band

**Static visual/product-fit score: 4–5 / 10.**

Justification: The screen has the ingredients of an operations dashboard — KPIs, charting, table, refresh/export controls — but the hierarchy is misaligned with the stated job. The most actionable surface is delayed, urgency is visually flattened, and table states/actions are too ambiguous for fast exception handling.

---

## 6. Smallest validation plan that could change the verdict

1. **Desktop first-viewport check:**  
   At 1366×768 and 1440×900, verify whether the exception table and urgent rows are visible without scrolling.

2. **Triage task test:**  
   Give an analyst 30 seconds to identify the top three exceptions needing action in the next hour; record whether they use the KPI cards, chart, insights, or table.

3. **Table comprehension pass:**  
   Check whether status, deadline, impact, and next action are understandable without hover, color-only cues, or icon interpretation.

4. **State coverage review:**  
   Inspect designed states for loading, empty, error, stale data, refresh failure, long product names, long translated labels, keyboard focus, and narrow laptop widths.

5. **Density and readability check:**  
   Validate that body text, row height, contrast, and spacing remain readable during repeated operations use without making the queue feel like a marketing dashboard.


## Output B

## 1. Diagnosis

**Diagnosis — Static evidence only:** The screen appears visually polished but is structurally misaligned with the primary job because exception discovery is pushed below KPI, chart, and generic insight content while the actual action table lacks hierarchy, labels, and decision cues.

## 2. Blocking findings

1. **Primary workflow is below the fold.**  
   The exception table—the surface needed to find issues requiring action in the next hour—starts below KPI cards, a large chart area, and generic insight cards.

2. **Equal emphasis hides operational urgency.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive the same card treatment, even though only some directly indicate near-term action.

3. **The table does not expose the next action clearly.**  
   Product, issue, owner, deadline, financial impact, status, and action use similar weight, so analysts must parse every row instead of scanning for urgency.

4. **Status and actions are under-specified.**  
   Small colored dots without text and three unlabeled action icons make state and available actions ambiguous, especially in a dense operations context.

5. **Chrome and decorative structure compete with decision content.**  
   Six equal nav links, three icon buttons, a bright Create button, four title/tool rows, nested cards, repeated borders, shadows, and large gaps dilute the exception-finding path.

## 3. Secondary findings

1. **Header hierarchy is too generic for an operations workspace.**  
   The bright “Create” button likely draws more attention than exception triage, despite not being described as the dominant analyst task.

2. **Page metadata is fragmented.**  
   Title, subtitle, date range, export, and refresh status across four weakly aligned rows create avoidable scanning cost.

3. **KPI cards are visually monotonous.**  
   Identical height, label scale, number scale, helper copy, and blue sparklines prevent quick differentiation between risk, volume, trend, and background metrics.

4. **Generic insight copy weakens credibility.**  
   Phrases like “Monitor performance closely” do not meet the product tone of calm, precise operational guidance.

5. **Text density is not matched by readability.**  
   12–13px low-contrast gray body text, inconsistent 8–48px spacing, and universal shadows/radii create fatigue without improving comprehension.

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception queue into the first viewport.**  
   Acceptance: At 1366×768, the analyst can see the page title, active date/range context, critical summary, table header, and at least the first 5 exception rows without scrolling.

2. **Create an “Action needed next hour” command band above the table.**  
   Acceptance: The band shows count of urgent exceptions, total financial impact, oldest/soonest deadline, and last refresh timestamp using existing navy/ink neutrals plus amber/red semantics.

3. **Reduce KPI cards from eight equal cards to prioritized operational metrics.**  
   Acceptance: Revenue risk, blocked SKUs, and deadline-breaching exceptions receive primary visual weight; supporting metrics like page views move to a secondary row, compact strip, or table-side context.

4. **Replace generic insight cards with precise exception drivers.**  
   Acceptance: Each insight names the affected SKU/category/vendor, the reason, the impact, and the recommended next step; no card uses generic copy such as “monitor closely.”

5. **Rebuild table hierarchy around triage.**  
   Acceptance: Row scan order is issue severity → product → deadline → financial impact → owner → status → action; severity and deadline are visually stronger than owner and secondary metadata.

6. **Replace status dots with labeled semantic pills.**  
   Acceptance: Every status includes text plus color, e.g. “Blocked,” “At risk,” “Due <1h,” “Waiting on owner”; red/amber are reserved for true exception states.

7. **Make actions explicit and keyboard-friendly in the row.**  
   Acceptance: The primary row action is a labeled button such as “Resolve,” “Assign,” or “Open”; secondary icon actions have visible labels or tooltips and a documented focus state.

8. **Normalize density, spacing, and container treatment.**  
   Acceptance: Use a consistent 4/8px spacing rhythm, remove unnecessary nested cards, reserve shadows for active overlays or elevation changes, and keep body text at a readable contrast and size for sustained analyst use.

## 5. Static score band

**Static fit for stated job: 4–5 / 10.**  
Justification: The surface includes the right raw ingredients—KPIs, status, financial impact, deadlines, owners, and actions—but the current hierarchy prioritizes dashboard presentation over exception triage, and the table interaction cues are too weak for fast operational decisions.

## 6. Smallest validation plan that could change the verdict

1. **Viewport check:** Review the screen at 1440×900, 1366×768, and a narrow laptop width to confirm whether urgent exceptions are visible without scrolling.  
2. **State check:** Inspect loading, empty, error, stale-refresh, long product name, long translation, and high-exception-count states.  
3. **Keyboard pass:** Verify tab order from header to filters to first table action, with visible focus on all actionable controls.  
4. **Scan task:** Ask an analyst to identify the single exception needing action next and explain why within 30 seconds.  
5. **Status/action comprehension:** Confirm users can interpret every status and row action without relying on color-only dots or unlabeled icons.


## Output C

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
