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


## Output B

## 1. Diagnosis

**Static-evidence verdict:** The screen is organized like a generic analytics dashboard, but the product job is an urgent exception queue; the most actionable surface—the table—is visually delayed, under-specified, and less legible than lower-value summary content.

## 2. Blocking findings

1. **Primary workflow is below the fold.**  
   Evidence: the exception table starts below the fold while header, fragmented title rows, eight KPIs, chart card, and insight cards occupy the first screen. For analysts finding next-hour exceptions, this buries the actual work queue.

2. **Priority hierarchy is flat where risk should dominate.**  
   Evidence: revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive equal card treatment, identical sparklines, and similar scale. This makes urgent operational risk compete with informational metrics.

3. **Table does not support fast triage.**  
   Evidence: product, issue, owner, deadline, financial impact, status, and action all use similar weight; long names truncate at 24 characters; status is dot-only; actions are unlabeled icons. The analyst cannot confidently identify severity, ownership, due time, and next action at speed.

4. **The page has excessive container noise.**  
   Evidence: every region has border, 16px radius, and shadow, plus a large pale card containing another chart card and nested insight cards. This reduces density and makes all regions feel equally important.

5. **Production states are not defined.**  
   Evidence: empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are absent from the description. For a dense operations surface, these omissions can break trust and repeated-use efficiency.

## 3. Secondary findings

1. **Header competes with task content.**  
   Six equal nav links, global search, three icon buttons, and a bright blue Create button inside a 64px header create more command competition than the exception workflow needs.

2. **Page metadata is fragmented.**  
   Title, subtitle, date range, export, and refresh status occupy four separate weakly aligned rows, increasing vertical cost before the analyst reaches decisions.

3. **Insight copy is too generic for operations.**  
   “Monitor performance closely” does not add decision value. Insights should identify the exception, confidence/source, owner, deadline, and recommended next step.

4. **Typography and contrast are likely too weak for dense scanning.**  
   Body text at 12–13px with low-contrast gray is risky for prolonged desktop use and fast comparison, especially in table cells.

5. **Spacing rhythm is inconsistent.**  
   Gaps ranging from 8px to 48px without a clear system makes the layout feel less precise and slows visual parsing.

## 4. Concrete redesign moves with acceptance criteria

1. **Promote the exception queue above analytics.**  
   Acceptance: on a standard desktop laptop viewport, the analyst can see the page title, active filters/date range, top risk summary, and at least the first several exception rows without scrolling.

2. **Replace eight equal KPIs with a triage strip.**  
   Acceptance: revenue risk, blocked SKUs, overdue/next-hour deadlines, and unowned exceptions receive primary emphasis; lower-priority metrics such as page views move to secondary context or a collapsed analytics area.

3. **Collapse page metadata into one aligned command bar.**  
   Acceptance: title/subtitle sit left; date range, export, refresh status, and last-updated timestamp align right in one row or two tightly related rows with a consistent baseline.

4. **Rebuild the table for decision scanning.**  
   Acceptance: issue/severity, deadline, financial impact, and action have clear visual priority; financial impact is right-aligned; deadlines use relative urgency; product names allow at least two-line wrapping or an accessible full-name reveal.

5. **Make status and actions self-describing.**  
   Acceptance: status uses text plus semantic color, not color/dot alone; action controls have visible labels or labeled compact buttons for primary actions, with icon-only controls reserved for secondary overflow.

6. **Reduce card nesting and visual chrome.**  
   Acceptance: remove nested cards where a section heading and divider would suffice; reserve shadows/radius for true overlays or grouped panels; preserve navy/ink neutrals and amber/red semantic status colors.

7. **Create a consistent density and type system.**  
   Acceptance: table/body text uses a readable operational size and contrast; labels, helper text, row metadata, and numeric values have distinct roles; spacing follows a small repeatable rhythm rather than arbitrary 8–48px jumps.

8. **Define required operational states.**  
   Acceptance: loading shows table skeletons without layout jump; empty state explains filters and next action; error state preserves filters and offers retry; stale refresh state is visible; keyboard focus is always apparent; long translations and narrow laptop widths do not hide primary actions.

## 5. Score band

**Static score band: 45–55 / 100.**  
Justification: the surface has recognizable dashboard ingredients and an existing neutral/status system to preserve, but the static evidence shows a major mismatch between visual hierarchy and the primary job, plus unresolved table legibility, action labeling, state coverage, and dense-use accessibility risks.

## 6. Smallest validation plan that could change the verdict

1. **Desktop viewport check:** verify at common laptop widths whether the exception queue appears above the fold and whether primary actions remain reachable.  
2. **Table comprehension pass:** ask whether a user can identify the highest-impact next-hour exception, owner, deadline, status, and action within a few seconds.  
3. **Keyboard-only pass:** tab through header, filters, table rows, status, and actions; confirm visible focus and non-icon-only accessible action names.  
4. **State pass:** inspect loading, empty, error, stale-refresh, long-product-name, and long-translation states.  
5. **Contrast/legibility pass:** verify body text, helper text, status labels, and semantic amber/red states meet readable contrast in the actual rendered UI.


## Output C

## 1. Diagnosis

**Diagnosis — [Static evidence only]:** The surface reads as a generic analytics dashboard rather than an exception triage workspace; hierarchy, density, and table access currently work against the primary job of finding what needs action in the next hour.

---

## 2. Blocking findings

1. **The primary work object is below the fold.**  
   The exception table is the core decision surface, but the header, fragmented page controls, eight KPI cards, chart, and insight cards all appear before it.

2. **Urgency hierarchy is flattened.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive equal card treatment, which makes time-sensitive exceptions compete with observational metrics.

3. **The table is not scannable enough for triage.**  
   Product, issue, owner, deadline, financial impact, status, and action use similar weight, so the analyst has to read every cell instead of scanning severity, deadline, impact, and ownership.

4. **Status and actions are under-specified.**  
   Small colored dots without text and three unlabeled action icons create ambiguity in a high-stakes operations surface where users need fast, confident decisions.

5. **The visual system overuses containers.**  
   Borders, 16px radius, and soft shadows on every region create card noise and reduce precision; the workspace feels assembled from interchangeable panels instead of tuned for dense operations.

---

## 3. Secondary findings

1. **Header competes with the work.**  
   Six equal nav links, global search, three icon buttons, and a bright blue “Create” button make the top bar busy and mis-prioritized for analysts trying to resolve exceptions.

2. **Page controls are fragmented.**  
   Title, subtitle, date range, export, and refresh status occupy four separate rows, weakening alignment and wasting vertical space.

3. **Generic insight copy reduces trust.**  
   “Monitor performance closely” does not explain what changed, who owns it, or what action should happen next.

4. **Typography is too small and low-contrast for sustained use.**  
   12–13px low-contrast gray body text may be fatiguing in a dense desktop workflow, especially for deadlines, owners, and financial impact.

5. **Production states are absent from the design brief.**  
   Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are not described, so the static design cannot be considered production-ready.

---

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception table into the first viewport.**  
   Acceptance: on a 1366×768 desktop viewport, the user can see the page heading, the priority metric strip, and at least the first 5–7 exception rows without scrolling.

2. **Collapse page metadata into one aligned command row.**  
   Combine title, subtitle, date range, refresh timestamp, export, and refresh action into a single structured header area.  
   Acceptance: page controls use one baseline/grid system; no more than two rows are used before the KPI/triage content begins.

3. **Replace eight equal KPI cards with a priority strip.**  
   Promote only next-hour decision metrics: revenue risk, blocked SKUs, missed/near deadline count, and unresolved high-impact exceptions. Demote page views and broad performance metrics to compact secondary text or filters.  
   Acceptance: the top-priority metrics are visually larger or positioned first; observational metrics cannot be mistaken for urgent exception counts.

4. **Reduce decorative card nesting.**  
   Remove the pale outer card + inner chart card + nested insight cards pattern. Use one calm analytics panel or place the chart behind the table in priority.  
   Acceptance: no section has more than one level of card nesting; shadows are reserved for overlays or active surfaces, not every container.

5. **Turn generic insights into operational exception summaries.**  
   Replace “Monitor performance closely” with specific summaries such as “12 blocked SKUs over $18.4k risk, 5 due within 60 minutes, 3 unassigned.”  
   Acceptance: every insight names a metric, severity, time window, and implied next action.

6. **Rebuild table hierarchy around triage.**  
   Make product and issue the primary cell group, then deadline, financial impact, status, owner, and action. Use stronger weight for issue/severity and tabular numbers for impact.  
   Acceptance: within three seconds, a user can identify highest financial risk, soonest deadline, current owner, and required action from the visible rows.

7. **Replace status dots and unlabeled icons with explicit controls.**  
   Use text status labels with semantic amber/red treatment: “Blocked,” “Due <1h,” “At risk,” “Needs owner.” Convert icon-only actions into labeled buttons or icon+label controls for primary actions.  
   Acceptance: status remains understandable without color; each row has one clear primary action and any secondary actions are discoverable by label or menu text.

8. **Define resilient dense-work states.**  
   Specify loading skeletons matching the table, empty states for “no exceptions,” inline error/retry for failed refresh/export, visible keyboard focus, narrow-laptop compression, and long-name/translation behavior.  
   Acceptance: product names can wrap to two lines or expand on demand; focus is visible on every interactive element; error and loading states preserve the user’s place in the workflow.

---

## 5. Bounded score

**Static score band: 40–50 / 100 for exception-triage fitness.**  
Justification: the described screen has a credible neutral/status palette and real workflow elements, but the primary decision surface is buried, urgency is visually flattened, controls are ambiguous, and key production states are unspecified.

---

## 6. Smallest validation plan that could change the verdict

1. **Desktop first-viewport check:** verify at 1366×768 and 1440×900 whether the exception table and first actionable rows are visible without scrolling.  
2. **Keyboard pass:** tab through header, filters, table rows, status, and actions; confirm visible focus and understandable action names.  
3. **State pass:** inspect loading, empty, failed refresh, failed export, long product names, and long translated labels.  
4. **Responsive compression pass:** check a narrow laptop width around 1280px and confirm table priority columns remain usable.  
5. **Triage timing check:** ask whether a user can identify the highest-risk exception, its owner, deadline, and next action within 10 seconds.
