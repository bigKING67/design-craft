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

The screen is structured like a generic analytics dashboard, but the product need is an exception triage workspace, so the most urgent merchandising actions are visually delayed, under-ranked, and harder to execute.  
**Evidence label:** Static product-surface description only; no runtime, DOM, responsive, or accessibility validation performed.

---

## 2. Blocking findings

1. **The primary job is below the fold.**  
   The exception table — the surface that answers “what needs action in the next hour?” — starts after header rows, eight KPIs, a large chart card, and generic insight cards.

2. **Urgency hierarchy is missing.**  
   Revenue risk, blocked SKUs, sell-through, and page views receive equal card treatment, even though only some directly indicate immediate action.

3. **The table does not support fast triage.**  
   Product, issue, owner, deadline, financial impact, status, and action have similar weight, making it difficult to scan for severity, deadline, and next step.

4. **Critical status is under-communicated.**  
   Small colored dots without text rely on color alone and do not clearly distinguish blocked, at-risk, overdue, resolved, or needs-owner states.

5. **Actions are ambiguous.**  
   Three unlabeled icon actions in the highest-value workflow create avoidable decision friction and increase the risk of wrong or delayed action.

---

## 3. Secondary findings

1. **Header competes with work.**  
   Six equal nav links, global search, three icon buttons, and a bright blue “Create” button give broad application chrome more emphasis than hourly exception handling.

2. **Page metadata is fragmented.**  
   Title, subtitle, date range, export, and refresh status occupy four weakly aligned rows instead of forming one clear operational control band.

3. **The nested-card composition wastes density.**  
   A pale card containing another chart card plus three more nested insight cards adds borders, radius, and shadow without improving decision quality.

4. **Copy is too generic for operations.**  
   “Monitor performance closely” does not tell an analyst what changed, what is at risk, who owns it, or what to do next.

5. **Text and spacing reduce confidence.**  
   12–13px low-contrast gray text, inconsistent 8–48px gaps, and repeated shadows/radii create a soft SaaS look rather than a precise control surface.

---

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception queue into the first viewport.**  
   Acceptance: on a typical desktop/laptop viewport, the user can see the page title, active filters/date range, summary of urgent counts, and the first several exception rows without scrolling.

2. **Replace eight equal KPI cards with a prioritized operational summary strip.**  
   Acceptance: no more than 3–4 top metrics appear above the table, ranked by action relevance, such as `Critical exceptions`, `Revenue at risk`, `Blocked SKUs`, and `Due within 60 min`; page views moves lower or into a secondary analytics area.

3. **Create a clear command/header band.**  
   Acceptance: title, subtitle, date range, refresh timestamp, export, and key filters align in one compact region; refresh status is readable but not visually louder than active exceptions.

4. **Make the table the dominant component.**  
   Acceptance: table columns visually prioritize `Issue severity`, `Deadline`, `Financial impact`, `Owner`, and `Next action`; less urgent metadata uses lighter weight or secondary placement.

5. **Replace dot-only status with labeled status badges.**  
   Acceptance: every status has text plus semantic color, e.g. `Blocked`, `Overdue`, `At risk`, `Needs owner`, `In progress`; amber/red preserve existing semantic meaning and are not used decoratively.

6. **Expose row actions as specific text or labeled controls.**  
   Acceptance: primary action is readable without hover, such as `Assign`, `Resolve`, `Escalate`, or `Review`; secondary icon actions have visible labels, tooltips are not the only source of meaning.

7. **Fix truncation for product names.**  
   Acceptance: product names can wrap to two lines or expose a persistent secondary identifier; truncation at 24 characters is avoided for the main recognition field.

8. **Reduce decorative containers and normalize rhythm.**  
   Acceptance: only meaningful regions get borders; shadows are minimized or removed; spacing follows a small set of increments, for example 8/12/16/24/32px, with tighter density around the table.

---

## 5. Score band

**Static evidence score: 4–5 / 10.**  
Justification: the surface appears polished at a generic dashboard level, but it conflicts with the stated operational purpose by delaying the exception queue, flattening urgency, weakening table scanability, and leaving key states unspecified. The score is a band because no actual screen, interaction behavior, responsiveness, or accessibility implementation was validated.

---

## 6. Smallest validation plan that could change the verdict

1. **First-viewport check:** verify what appears without scrolling on common desktop and narrow-laptop widths.  
2. **Triage task test:** ask whether an analyst can identify the highest-risk exception, owner, deadline, financial impact, and next action in under 30 seconds.  
3. **Keyboard path check:** tab through search, filters, table rows, and row actions; confirm visible focus and logical order.  
4. **State review:** inspect loading, empty, error, stale-refresh, long-product-name, long-translation, and no-owner cases.  
5. **Status comprehension check:** confirm that status remains understandable without color and without relying on hover-only labels.


## Output B

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


## Output C

## 1. Diagnosis

**Diagnosis — Evidence: static product-surface description only, no browser/DOM/runtime validation:** the workspace visually over-invests in navigation, equalized KPIs, nested cards, and generic commentary while pushing the exception table—the primary “next hour” decision surface—below the fold and making urgency, ownership, impact, and action too hard to scan.

## 2. Blocking findings

1. **Primary job is structurally delayed.**  
   The exception table starts below the fold, while header chrome, fragmented title metadata, KPI cards, chart cards, and “insights” consume the first screen. For merchandising analysts, the first viewport should expose what needs action now.

2. **Triage hierarchy is flat.**  
   Revenue risk, blocked SKUs, sell-through, and page views receive equal card weight and equal blue sparklines. In this product, blocked inventory, deadline, financial impact, and status severity should dominate yesterday’s attention metrics.

3. **The table does not encode decision priority strongly enough.**  
   Product, issue, owner, deadline, financial impact, status, and action use similar text weight; status is only a small colored dot; action uses unlabeled icons. This makes the highest-risk exception harder to identify and act on quickly.

4. **Critical information is being hidden or made ambiguous.**  
   Long product names truncate at 24 characters, status lacks text, and icon-only actions lack labels. Static evidence indicates real operational context may be lost before the analyst can verify the item.

5. **Production states are unspecified.**  
   Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are not described. For an operations workspace, those are not polish details; they affect trust, recovery, and repeated-use efficiency.

## 3. Secondary findings

1. **Header priority is too democratic.**  
   Six equal nav links, global search, three icon buttons, and a bright blue Create button compete with the exception workflow. “Create” sounds less central than finding and resolving exceptions.

2. **Page metadata is fragmented.**  
   Title, subtitle, date range, export, and refresh status occupy four separate rows with weak alignment, increasing vertical cost without improving comprehension.

3. **Nested cards create false structure.**  
   A pale card containing another chart card, followed by three more cards, adds visual ceremony but not clearer triage.

4. **Generic insight copy weakens credibility.**  
   Phrases like “Monitor performance closely” do not match the product’s precise, operational tone unless they are tied to named SKUs, owners, thresholds, and actions.

5. **Density is present but not disciplined.**  
   12–13px low-contrast body text, inconsistent 8–48px gaps, and repeated borders/radii/shadows create noise rather than calm precision.

## 4. Concrete redesign moves with acceptance criteria

1. **Make the first viewport exception-led.**  
   Move the exception table above the large chart/insight region.  
   **Accept:** at a 1366×768 design target, the table header and at least the first several exception rows are visible without scrolling.

2. **Collapse page metadata into one aligned command bar.**  
   Combine title, subtitle/context, date range, refresh status, and export into a single two-tier header area below global nav.  
   **Accept:** no more than two rows are used for page identity and page-level controls; refresh status is visually tied to the data it describes.

3. **Replace eight equal KPI cards with a prioritized triage strip.**  
   Promote revenue risk, blocked SKUs, approaching deadlines, and unassigned/high-severity exceptions; demote page views and secondary health metrics.  
   **Accept:** urgent operational metrics have visibly stronger weight than observational metrics, while semantic amber/red remain reserved for status/risk.

4. **Rebuild table hierarchy around actionability.**  
   Use stronger weight for product identity, issue severity, deadline, and financial impact; right-align currency; show owner clearly; convert status dots into text + color.  
   **Accept:** status is understandable without color, financial impact scans as a numeric column, and the highest-impact due-soon row is visually discoverable.

5. **Replace unlabeled icon actions with explicit primary actions.**  
   Use one labeled primary action per row, with secondary actions in a labeled overflow if needed.  
   **Accept:** each row’s next action is readable without tooltip dependence; icon-only controls have accessible names in implementation.

6. **Protect full product identification.**  
   Avoid hard truncation at 24 characters for product names; use two-line wrapping, SKU/vendor secondary text, or an expansion affordance.  
   **Accept:** critical product identity is recoverable in-table without opening a separate workflow.

7. **Flatten the card system.**  
   Remove nested card-within-card structures and reduce repeated shadows. Use navy/ink neutrals, restrained borders, and a consistent spacing scale.  
   **Accept:** each region has a clear purpose, one container level, and spacing follows a predictable 8/16/24/32px rhythm.

8. **Replace generic insights with accountable exception summaries.**  
   Convert “Monitor performance closely” into statements like “12 blocked SKUs exceed $48k risk; 5 are due within 60 minutes; 3 lack owners.”  
   **Accept:** every insight includes count, threshold/cause, affected entity, and a direct path to the filtered table.

## 5. Static score band

**45–55 / 100 for product-surface fit, based only on the supplied static description.**  
The screen appears to preserve real data, dense layout, and a neutral operations tone, but the core exception workflow is below the fold, the hierarchy is flattened, key states are unspecified, and action/status semantics are too ambiguous for a next-hour operational surface.

## 6. Smallest validation plan that could change the verdict

1. **First-viewport check:** test 1366×768 and 1440×900 layouts for whether actionable exception rows are visible without scrolling.  
2. **Keyboard path:** verify focus order through nav, search, filters/date range, table rows, row actions, export, and refresh.  
3. **State samples:** inspect loading, empty results, API/error/stale-data, long product names, long translated labels, and many-row table states.  
4. **Accessibility spot check:** verify status text, action names, focus visibility, contrast, and non-color-only severity communication.  
5. **Decision-flow task test:** give an analyst three representative exceptions and confirm they can identify the highest financial-impact item due soon, its owner, status, and next action from the first screen.
