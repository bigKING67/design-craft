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

## 1. Diagnosis — evidence label

**Diagnosis:** The surface reads as a generic analytics dashboard rather than an hour-prioritized exception workspace: the urgent merchandising decisions are visually delayed, equally weighted, and under-specified at the table/action layer.  
**Evidence label:** Static product-surface description only; no browser, DOM, runtime, responsive, or accessibility-tree validation claimed.

---

## 2. Blocking findings

1. **Primary job is below the fold.**  
   The exception table is the core “find what needs action in the next hour” surface, but it starts below KPI cards, chart cards, and generic insight cards.

2. **Urgency hierarchy is flattened.**  
   Revenue risk, blocked SKUs, sell-through, and page views receive equal KPI treatment, so operationally urgent exceptions are visually equivalent to background telemetry.

3. **Table is not scannable enough for action.**  
   Product, issue, owner, deadline, impact, status, and action use similar weight; the user cannot quickly rank “what matters now.”

4. **Status and actions are ambiguous.**  
   Small colored dots without text and three unlabeled icons force memory, guessing, and hover dependence in a high-pressure operations flow.

5. **The visual system over-containers everything.**  
   Borders, radius, and soft shadows on every region create card soup, reduce density, and weaken the calm, precise navy/ink operations tone.

---

## 3. Secondary findings

1. **Header competes with the work.**  
   Six equal nav links, global search, three icon buttons, and a bright blue Create button make the top bar feel like a general SaaS shell, not an exception triage cockpit.

2. **Page metadata is fragmented.**  
   Title, subtitle, date range, export, and refresh status across four weakly aligned rows create avoidable scanning cost before the analyst reaches data.

3. **Generic insights reduce credibility.**  
   Copy like “Monitor performance closely” does not explain a specific exception, cause, threshold, owner, or next action.

4. **Typography and contrast sound too light for dense operations.**  
   12–13px low-contrast gray body text risks fatigue and undermines precision, especially in long sessions.

5. **Missing edge-state definitions are material.**  
   Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are not cosmetic here; they determine whether the workspace remains usable under real operational conditions.

---

## 4. Concrete redesign moves with acceptance criteria

1. **Rebuild the top of page around triage, not navigation.**  
   Acceptance: within the first viewport, the analyst can see the page title, active date range, refresh recency, total urgent exceptions, and the top rows of the exception table.

2. **Compress page metadata into one aligned command bar.**  
   Acceptance: title/subtitle sit as one block; date range, export, and refresh status align on the same row or a single secondary row with consistent spacing.

3. **Replace eight equal KPI cards with a priority strip.**  
   Acceptance: only 3–4 metrics appear above the table, led by “Revenue risk,” “Blocked SKUs,” “Deadline within 1h,” or equivalent action-driving measures; page views becomes secondary or moves below.

4. **Demote or contextualize the area chart.**  
   Acceptance: the chart no longer pushes exceptions below the fold unless it directly explains the selected exception set; generic insight cards are removed or replaced with specific rule-based findings.

5. **Make the exception table the main composition anchor.**  
   Acceptance: default sort prioritizes urgency and financial impact; deadline, issue severity, and impact have stronger visual weight than owner or routine metadata.

6. **Use explicit status and action language.**  
   Acceptance: status appears as text-bearing chips such as “Blocked,” “At risk,” “Needs owner,” or “Due <1h”; row actions use visible labels or a labeled primary action plus overflow menu, not three unlabeled icons.

7. **Harden table content for real merchandising data.**  
   Acceptance: long product names have a wider first column, two-line allowance or expandable detail, and a reliable full-name reveal; financial impact remains readable and aligned; translations do not break row height unpredictably.

8. **Tighten the visual system for calm density.**  
   Acceptance: use navy/ink neutrals and semantic amber/red only for meaning; remove decorative shadows from routine regions; use a consistent spacing rhythm such as 8/16/24/32; body text is at least comfortably readable with higher contrast, with 12px reserved for metadata.

---

## 5. Score band

**Static evidence score band: 52–60 / 100.**  
Justification: the surface appears structurally complete and uses a restrained neutral/status palette, but the current hierarchy actively works against the primary job by burying exceptions, flattening urgency, and making table actions/statuses ambiguous. This score could move materially if runtime evidence shows strong keyboard flow, responsive triage behavior, and robust state handling not described here.

---

## 6. Smallest validation plan that could change the verdict

1. **First-viewport check at common desktop and narrow-laptop widths.**  
   Verify whether urgent exceptions and their top actions are visible without scrolling.

2. **Real data table pass.**  
   Test long product names, high financial values, many urgent rows, missing owners, overdue deadlines, and translated labels.

3. **State coverage pass.**  
   Review loading, empty, partial-error, full-error, stale-refresh, and no-results states for the table and KPI area.

4. **Keyboard-only task path.**  
   Confirm the analyst can search/filter, reach the first urgent row, identify status, open the action, and recover focus without mouse dependence.

5. **Contrast and focus-visible check.**  
   Validate low-contrast gray text, semantic status colors, icon controls, and focus states against the navy/ink system.


## Output B

## 1. Diagnosis

The screen currently presents an analytics dashboard before an exception workspace, so the highest-value task—finding SKUs needing action in the next hour—is visually delayed, under-prioritized, and made harder to scan.  
**Evidence label:** Static product-surface description only; no browser, DOM, runtime, responsive, or accessibility-tree validation performed.

---

## 2. Blocking findings

1. **Primary workflow is below the fold**
   - The exception table is the core job surface, but it appears after KPI cards, chart cards, and generic insight cards.
   - This conflicts with the stated goal: “find the exceptions that need action in the next hour.”

2. **Urgency hierarchy is flattened**
   - Revenue risk, blocked SKUs, sell-through, and page views receive equal card treatment.
   - Equal card size, equal blue sparklines, and similar number styling make operational risk look no more urgent than passive analytics.

3. **Table does not support fast exception triage**
   - Product, issue, owner, deadline, financial impact, status, and action use similar text weight.
   - Long names truncate at 24 characters, status is dot-only, and actions are unlabeled icons.
   - This makes the row difficult to parse under time pressure.

4. **Status and action affordances are too ambiguous**
   - Colored dots without text rely on color alone and require memorization.
   - Three unlabeled action icons create interpretation risk, especially for repeated operations work.

5. **Visual system is over-containerized**
   - Every region has border, 16px radius, and soft shadow.
   - Nested cards inside pale cards create hierarchy noise instead of helping analysts locate exceptions.

---

## 3. Secondary findings

1. **Header competes with workspace content**
   - Six equal nav links, global search, three icon buttons, and a bright blue “Create” button make the header feel like a generic app shell rather than a focused operations surface.

2. **Page metadata is fragmented**
   - Title, subtitle, date range, export, and refresh status occupying four rows weakens alignment and wastes vertical space.

3. **Insight cards are generic**
   - Copy like “Monitor performance closely” does not describe a concrete merchandising exception, owner, deadline, or action.

4. **Typography and contrast are too weak for dense operational use**
   - 12–13px low-contrast gray body text risks fatigue and slows scanning.

5. **Spacing lacks an operational rhythm**
   - Gaps ranging from 8px to 48px without a clear system create uneven density and reduce predictability.

---

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception queue into the first viewport**
   - Replace the dashboard-first layout with an “Exceptions needing action” table or queue directly beneath the page command bar.
   - **Acceptance criteria:** At 1366×768, the analyst can see the page title, key controls, and at least 6–8 exception rows without scrolling.

2. **Create a risk-first KPI hierarchy**
   - Reduce eight equal KPI cards to a prioritized strip: `Revenue at risk`, `Blocked SKUs`, `Deadline breaches`, `Owner coverage`.
   - Move passive metrics like page views and general sell-through into secondary context or chart filters.
   - **Acceptance criteria:** The most urgent operational metric is visually dominant through placement, weight, and semantic color—not through decorative effects.

3. **Consolidate the page command area**
   - Combine title, subtitle, date range, export, refresh status, and last-updated text into one aligned command row plus one compact supporting line.
   - **Acceptance criteria:** No more than two rows above the primary exception surface; refresh state remains visible but subdued.

4. **Redesign table hierarchy for triage**
   - Make `Issue`, `Deadline`, `Financial impact`, and `Status` the strongest scanning columns.
   - Product name should support two-line wrapping or a hover/focus reveal rather than hard truncation at 24 characters.
   - **Acceptance criteria:** In a 5-second scan, the highest-risk row is identifiable by issue severity, deadline, and impact without opening details.

5. **Replace dot-only statuses with labeled semantic chips**
   - Use concise labels such as `Blocked`, `At risk`, `Due <1h`, `Assigned`, `Needs owner`.
   - Preserve amber/red semantics for risk states.
   - **Acceptance criteria:** Status remains understandable without relying on color alone.

6. **Make row actions explicit and task-specific**
   - Replace three unlabeled icons with a primary text action such as `Resolve`, `Assign`, or `Open`, plus a secondary overflow menu if needed.
   - **Acceptance criteria:** Each row has one obvious next action; icon-only controls are reserved for universally understood secondary actions with labels/tooltips.

7. **Remove nested decorative card structure**
   - Keep the navy/ink neutral system, but reduce borders, shadows, and repeated radius.
   - Use separators, section headers, density, and alignment instead of stacked cards.
   - **Acceptance criteria:** The page has clear zones without every region appearing equally important.

8. **Define production states for the actual decision flow**
   - Add described states for loading, empty, error, stale data, keyboard focus, narrow laptop, long product names, and long translated labels.
   - **Acceptance criteria:** The exception workflow remains usable when data is loading, unavailable, partially stale, or text expands by 30–50%.

---

## 5. Score band

**Static evidence score band: 45–55 / 100.**

Justification: the surface appears visually organized at a component level, but the core decision flow is inverted, risk hierarchy is flattened, table semantics are weak, and important production states are unspecified. The score could rise materially if runtime validation shows the table is reachable, keyboard-friendly, responsive, and state-complete despite the described layout.

---

## 6. Smallest validation plan that could change the verdict

1. **First-viewport check**
   - Test 1440×900, 1366×768, and 1280×720.
   - Confirm whether actionable exceptions are visible without scrolling.

2. **Triage scan check**
   - Give a reviewer 10 seconds to identify:
     - highest revenue risk,
     - soonest deadline,
     - unowned issue,
     - required next action.
   - If they cannot do this from the table, hierarchy fails.

3. **Keyboard path check**
   - Tab through search, filters/date range, table rows, status/action controls, and export/refresh.
   - Confirm visible focus and no icon-only ambiguity.

4. **State check**
   - Review loading, empty, error, stale refresh, no results, and partial-data states.
   - Confirm each state keeps the analyst oriented and offers a next step.

5. **Content stress check**
   - Use long product names, long owner names, large currency values, and 30–50% longer translated labels.
   - Confirm rows remain scannable without destructive truncation.

6. **Narrow-laptop density check**
   - Validate the same workflow at 1280×720.
   - Confirm the table remains the primary surface and does not collapse into a card stack that slows bulk review.


## Output C

## 1. Diagnosis

The screen is organized like a generic analytics dashboard, but the product’s stated job is exception triage in the next hour; the current hierarchy delays the table, equalizes unequal signals, and hides action-critical status.  
**Evidence label:** Static description only; no screenshot, DOM, runtime, responsive, or accessibility-tree validation performed.

## 2. Blocking findings

1. **Primary workflow is below the fold.**  
   The exception table is the core decision surface, but KPI cards, chart cards, and generic insights take priority over the actionable list.

2. **Signal hierarchy is flattened.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive equal card treatment, making urgent operational exceptions compete with passive reporting metrics.

3. **Table rows are not scannable enough for one-hour triage.**  
   Product, issue, owner, deadline, financial impact, status, and action use similar weight, so the analyst must read across every row instead of spotting severity, deadline, and impact first.

4. **Status and actions are under-specified.**  
   Colored dots without text and three unlabeled action icons create ambiguity, especially for fast repeated use, color-blind users, keyboard users, and long sessions.

5. **Visual chrome is consuming attention.**  
   Universal borders, 16px radii, shadows, nested cards, and inconsistent spacing create a busy frame around the data rather than a calm operations surface.

## 3. Secondary findings

1. **Header has too many equal-priority controls.**  
   Six equal nav links, global search, three icon buttons, and a bright Create button compete with the current task.

2. **Page metadata is fragmented.**  
   Title, subtitle, date range, export, and refresh status across four rows weaken alignment and delay entry into the work.

3. **KPI design is visually repetitive.**  
   Identical height, label size, number size, helper copy, and blue sparklines make the cards look polished but not decision-oriented.

4. **The “insights” area sounds non-operational.**  
   Generic text like “Monitor performance closely” does not support a merchandising analyst deciding what to do next.

5. **Missing state definitions create production risk.**  
   Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are not described, so the surface may fail exactly when operators need reliability.

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception table into the first viewport.**  
   - Acceptance: at common desktop heights, the first visible content after header/page summary includes table header and at least 5–8 exception rows.  
   - Acceptance: chart and secondary insights no longer push the table below the fold.

2. **Replace eight equal KPI cards with a triage summary strip.**  
   - Acceptance: only next-hour decision metrics are promoted: urgent exceptions, revenue at risk, blocked SKUs, overdue/near-deadline items.  
   - Acceptance: passive metrics such as yesterday’s page views are demoted, grouped, or moved to a secondary analytics section.  
   - Acceptance: semantic amber/red are used only for actual risk states, not decorative emphasis.

3. **Create a single aligned page command row.**  
   - Acceptance: title, date range, refresh state, export, and any filter entry point sit on one coherent grid.  
   - Acceptance: refresh state is visible but quiet, e.g. “Updated 2 min ago,” with clear stale/error variants.  
   - Acceptance: export is secondary unless it is part of the immediate exception workflow.

4. **Redesign the table around triage priority.**  
   - Acceptance: each row exposes issue severity, deadline, financial impact, and owner with stronger visual hierarchy than secondary metadata.  
   - Acceptance: status uses text labels plus semantic color, not dots alone.  
   - Acceptance: financial impact and deadline are visually sortable/scannable, with urgent deadlines distinguishable without relying on color alone.

5. **Stop truncating product names at a fixed 24 characters.**  
   - Acceptance: product column supports two-line names or a structured product cell with name, SKU, and channel/store context.  
   - Acceptance: truncation, when unavoidable, preserves the differentiating suffix or exposes the full value on focus/hover.  
   - Acceptance: row height remains predictable enough for dense scanning.

6. **Replace unlabeled icon actions with explicit primary/secondary actions.**  
   - Acceptance: the dominant action is text-labeled, such as “Review,” “Assign,” or “Resolve,” depending on workflow truth.  
   - Acceptance: secondary actions move into a labeled overflow menu with accessible names and keyboard reachability.  
   - Acceptance: destructive or irreversible actions require clearer confirmation than an icon.

7. **Reduce nested carding and establish a spacing rhythm.**  
   - Acceptance: remove unnecessary cards inside cards; use section dividers, table grouping, or subtle background planes instead.  
   - Acceptance: spacing follows a small set of increments, for example 8/16/24/32, rather than arbitrary 8–48px gaps.  
   - Acceptance: borders/shadows are reserved for separation where layout alone is insufficient.

8. **Define production states for the exact workflow.**  
   - Acceptance: loading preserves table structure with skeleton rows or progressive data fill.  
   - Acceptance: empty state explains whether there are no exceptions or filters are hiding them.  
   - Acceptance: error state keeps stale data visible when possible and offers retry.  
   - Acceptance: keyboard focus is visible on nav, filters, table rows, actions, and pagination.  
   - Acceptance: long translations and narrow laptop widths do not hide status, deadline, impact, or the primary action.

## 5. Score

**Static evidence score band: 4–5 / 10.**

Justification: the surface appears visually complete, dense, and aligned with a navy/neutral operations tone, but the described hierarchy conflicts with the core job. The most important action surface starts below the fold, urgent and passive metrics are treated equally, and table affordances hide decision-critical meaning.

## 6. Smallest validation plan that could change the verdict

1. **Desktop viewport check:** verify at 1366×768 and 1440×900 whether the exception table appears in the first viewport and how many actionable rows are visible.  
2. **Real-data scan test:** use a representative exception set with long product names, mixed severities, deadlines, owners, and financial impacts; time whether an analyst can identify the top three next-hour actions without opening row details.  
3. **State pass:** inspect loading, empty, stale-data, save/error, and no-results states for the exception table and KPI/summary area.  
4. **Keyboard pass:** tab through header, filters, table rows, status, and actions; confirm visible focus and understandable action names.  
5. **Narrow-laptop and long-text pass:** check whether 1280px-wide layouts and longer translated labels preserve status text, deadline, impact, owner, and primary action.
