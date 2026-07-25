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

**Diagnosis — Static evidence only:** The screen currently behaves like a generic analytics dashboard, not an hourly exception workspace: hierarchy, vertical order, and component emphasis delay the analyst from finding urgent merchandising actions.

## 2. Blocking findings

1. **Primary task is below the fold.**  
   The exception table is the core decision surface, but it starts below the fold after header rows, KPI cards, chart cards, and generic insight cards.

2. **Urgency hierarchy is flattened.**  
   Revenue risk, blocked SKUs, sell-through, and yesterday’s page views receive equal card treatment, so operational severity is visually indistinguishable from background telemetry.

3. **The table does not support fast triage.**  
   Product, issue, owner, deadline, financial impact, status, and action use similar weight; status dots lack text; long names truncate too early; unlabeled icon actions slow recognition and increase error risk.

4. **Page structure is over-fragmented.**  
   Title, subtitle, date range, export, and refresh status occupy four separate rows with weak alignment, consuming valuable scan space before any actionable exception appears.

5. **Generic nested-card pattern dilutes credibility.**  
   Pale card → chart card → insight cards, plus repeated borders/radii/shadows, creates decorative containment rather than operational priority.

## 3. Secondary findings

1. **Header competes with the workspace.**  
   Six equal nav links, global search, three icon buttons, and a bright blue “Create” button make the 64px header feel louder than the exception workflow.

2. **Copy is not decision-grade.**  
   “Monitor performance closely” is too vague for analysts who need owner, cause, urgency, and next action.

3. **Typography is too small and too low contrast for dense work.**  
   12–13px low-contrast gray body text is risky for repeated scanning of financial impact, deadlines, and product names.

4. **Spacing lacks a system.**  
   Gaps ranging from 8px to 48px without rhythm make related information feel unrelated and unrelated information feel grouped.

5. **Missing state definitions weaken production readiness.**  
   Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation behavior are not described, which matters for an operations surface used under time pressure.

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception table into the first viewport.**  
   Acceptance: on a 1440×900 desktop viewport, the analyst sees the page title, priority summary, and at least the table header plus 6–8 exception rows without scrolling.

2. **Replace the eight equal KPI cards with a priority summary row.**  
   Acceptance: only 3–4 top metrics receive primary treatment: revenue risk, blocked SKUs, exceptions due within one hour, and unresolved high-severity issues. Secondary metrics such as page views move to a compact “context” area.

3. **Collapse page metadata into one command bar.**  
   Acceptance: title, subtitle, date range, refresh timestamp, export, and filter controls align in one or two structured rows, with one clear left edge and no orphaned controls.

4. **Turn status dots into labeled operational states.**  
   Acceptance: every status includes text, e.g. “Blocked,” “Due <1h,” “Assigned,” “Waiting vendor,” using preserved amber/red semantics; color is never the only indicator.

5. **Rebuild table hierarchy around triage.**  
   Acceptance: issue/severity, deadline, and financial impact are visually stronger than owner and secondary metadata; impact uses tabular numerals; deadlines show both relative urgency and exact time where useful.

6. **Replace unlabeled icon actions with explicit action affordances.**  
   Acceptance: the primary row action is text-labeled, e.g. “Review,” “Assign,” or “Resolve”; secondary actions may sit in a disclosed menu with accessible labels.

7. **Reduce surface noise while preserving the navy/ink neutral system.**  
   Acceptance: remove unnecessary nested cards; use borders or shadows, not both, for most regions; reserve stronger containment for the table and active exception modules; maintain semantic amber/red status colors.

8. **Define resilient content and state behavior.**  
   Acceptance: long product names wrap or expand with full identity available; loading uses table-shaped skeletons; empty state explains “No exceptions for this filter”; error state offers retry and last successful refresh; keyboard focus is visible on nav, filters, rows, and actions.

## 5. Score band

**Static score band: 4–5 / 10.**  
Justification: the surface appears data-rich and has the right raw objects, but static evidence shows the core decision surface is buried, urgency is flattened, status is under-specified, and production states are missing. The score could rise if runtime behavior, filtering, keyboard support, or responsive layouts already compensate for these issues.

## 6. Smallest validation plan that could change the verdict

1. Check a 1440×900 desktop viewport: is the exception table visible without scrolling?  
2. Check a narrow laptop width around 1280px: do header, command bar, KPI summary, and table remain usable without horizontal crowding?  
3. Keyboard through header, filters, table rows, and actions: is focus visible and order predictable?  
4. Inspect loading, empty, error, and stale-refresh states for the table and priority metrics.  
5. Test long product names, long owner names, and translated labels: do they preserve identity and action clarity?  
6. Verify status semantics: are amber/red states labeled, screen-readable, and not color-only?


## Output B

1. **Diagnosis — Evidence label: L1 static contextual.** The surface is visually orderly but operationally misprioritized: it spends the first screen on equal cards and decorative containers while the analyst’s real job—finding next-hour exceptions—starts below the fold.

## Blocking findings

1. **Primary workflow is buried.** The exception table is below the fold even though it is the action surface for “find exceptions in the next hour.”
2. **Priority hierarchy is flat.** Revenue risk, blocked SKUs, sell-through, and page views receive equal card weight, equal sparkline treatment, and similar typography.
3. **Decision evidence is diluted by card soup.** A pale outer card, nested chart card, and generic “insights” add surface mass without naming specific exceptions, owners, thresholds, or actions.
4. **The table does not support fast exception triage.** Product, issue, owner, deadline, impact, status, and action have similar weight; status is color-only; product names truncate too early; icon actions are unlabeled.
5. **Production states are under-specified.** Empty, loading, error, focus, narrow-laptop, and long-translation states are absent from the static description, which blocks confidence in an operations workspace.

## Secondary findings

1. **Header competition is too high.** Six equal nav links, search, three icons, and a bright “Create” button compete with exception review.
2. **Page command metadata is fragmented.** Title, subtitle, date range, export, and refresh status occupy four rows with weak alignment.
3. **Typography is too timid for dense work.** 12–13px low-contrast gray body text risks slow scanning and weak confidence for deadlines, owners, and financial impact.
4. **Spacing rhythm is inconsistent.** Gaps from 8px to 48px without clear grouping make the screen feel assembled rather than composed.
5. **Surface treatment is overused.** Every region having border, 16px radius, and soft shadow makes true hierarchy harder to perceive.

## Concrete redesign moves with acceptance criteria

1. **Create a single command band under the header.**  
   Acceptance: title, scope/date range, refresh status, export, and relevant filters align on one grid; refresh status is visible but not a row of its own; “Create” is visually secondary unless creation is part of exception resolution.

2. **Move the exception queue/table into the first viewport.**  
   Acceptance: at 1440×900 and narrow laptop height, analysts can see the top exceptions without scrolling; the first screen answers “what needs action now?”

3. **Replace eight equal KPI cards with a priority stack.**  
   Acceptance: one lead risk module surfaces next-hour revenue risk or blocked-SKU count; 3–4 supporting metrics appear as a compact strip; page views and other diagnostic metrics are lower emphasis.

4. **Make KPI context explicit.**  
   Acceptance: every emphasized number includes comparison, period, threshold, or breached rule; sparklines use semantic amber/red only for state, not equal decorative blue across all cards.

5. **Reframe the chart as diagnostic evidence, not a centerpiece.**  
   Acceptance: the chart answers a named operational question, such as “Which risk trend is driving today’s exceptions?”; generic insights are removed unless each names entity, condition, impact, owner, and next action.

6. **Redesign the table for triage scanning.**  
   Acceptance: row anatomy prioritizes product identity, issue severity, financial impact, deadline, owner, status, and next action; status includes text plus semantic color; product names allow at least two-line expansion or reveal-on-focus; numeric impact is right-aligned.

7. **Replace icon-only actions with explicit action grammar.**  
   Acceptance: the primary row action is labeled with verb-object copy such as “Assign owner,” “Resolve block,” or “Review SKU”; secondary actions are available by menu with labels and keyboard reachability.

8. **Tighten the visual system for dense operations.**  
   Acceptance: use the existing navy/ink neutrals and amber/red semantics; reduce nested cards; reserve shadows/elevation for overlays or selected states; establish a spacing rhythm such as 8/12/16/24/32; body/table text meets readable contrast and uses clear weight differences.

## Static score band

**58–66 / 100, L1 static contextual.** Justification: the surface has recognizable dashboard structure and real table data, but static evidence shows major failures in task focus, hierarchy, table scanability, state coverage, and surface restraint. The score should not be treated as a runtime verdict.

## Smallest validation plan that could change the verdict

1. Browser-check first viewport at 1440×900 and 1280×720: does the top exception/action surface appear without scrolling?
2. Verify responsive behavior at narrow laptop widths: header controls, KPI strip, chart, and table must not crowd or overflow.
3. Exercise table states with representative data: long product names, long translated labels, high financial impact, overdue deadline, no owner, and mixed statuses.
4. Check state coverage: loading, empty, error with retry, partial data, disabled export, and refresh-in-progress.
5. Keyboard smoke test: search, date range, filters, table rows, status text, row actions, export, and refresh must have visible focus and logical order.
6. Contrast and color check: muted text, status labels, amber/red states, and focus rings must remain legible without relying on color alone.


## Output C

## 1. Diagnosis

**Diagnosis — Static evidence only:** the screen appears operationally complete, but its visual hierarchy sends attention to navigation, generic KPI symmetry, and nested cards before the exception queue that merchandising analysts need to act on within the next hour.

## 2. Blocking findings

1. **The primary job is below the fold.**  
   The exception table is the action surface, but it starts after header rows, eight KPI cards, chart cards, and generic insight cards.

2. **All metrics are treated as equally important.**  
   Revenue risk, blocked SKUs, sell-through, and page views share the same card weight, number size, and blue sparkline treatment, which obscures urgent exceptions.

3. **The page header is fragmented and weakly aligned.**  
   Title, subtitle, date range, export, and refresh status occupying four rows creates scanning cost before any operational decision.

4. **The table does not expose action priority clearly.**  
   Product, issue, owner, deadline, impact, status, and action have similar weight; status dots lack text; actions are unlabeled icons.

5. **The surface overuses containers and shadows.**  
   Borders, 16px radii, and soft shadows on every region make all sections feel equally elevated, reducing precision and calm density.

## 3. Secondary findings

1. **Generic insights are not decision-grade.**  
   “Monitor performance closely” does not help an analyst choose the next action.

2. **Long product names are prematurely truncated.**  
   Cutting names at 24 characters risks hiding the distinguishing SKU detail needed for merchandising work.

3. **Low-contrast 12–13px body text weakens dense scanning.**  
   Dense does not need to mean faint; operational tables need durable legibility.

4. **Spacing rhythm is inconsistent.**  
   Gaps from 8px to 48px make the page feel assembled rather than governed by a predictable grid.

5. **Critical production states are undefined.**  
   Empty, loading, error, keyboard-focus, narrow-laptop, and long-translation states are not described, so the design is not yet production-complete.

## 4. Concrete redesign moves with acceptance criteria

1. **Move the exception queue into the first viewport.**  
   - Place the table or a compact exception queue directly below a single command/header row.  
   - **Acceptance:** on a 1366×768 desktop viewport, at least the table header and first 5 exception rows are visible without scrolling.

2. **Collapse page metadata into one aligned command bar.**  
   - Combine title, subtitle, date range, refresh status, export, and any primary page action into one or two disciplined rows.  
   - **Acceptance:** title/date/refresh/export share one horizontal alignment system; no more than two rows are used before the operational content begins.

3. **Prioritize exception-driving KPIs over ambient metrics.**  
   - Promote revenue risk, blocked SKUs, overdue/near-deadline items, and unresolved exceptions.  
   - Demote page views and other context metrics into a secondary strip or hidden detail area.  
   - **Acceptance:** the top KPI group contains no more than 3–4 primary metrics, and the most urgent metric has visibly stronger emphasis than page views.

4. **Replace equal blue sparklines with semantic signal.**  
   - Use navy/ink neutrals for baseline trend and amber/red only for warning or blocking conditions.  
   - **Acceptance:** blue is not used as a universal attention color; red/amber appear only where they map to actual status severity.

5. **Turn generic insight cards into an exception summary.**  
   - Replace “Monitor performance closely” style copy with specific operational summaries: “12 SKUs blocked by missing imagery,” “$48k revenue at risk today,” “5 items need owner reassignment.”  
   - **Acceptance:** every insight names a count, condition, and next likely action.

6. **Rebuild the table hierarchy around decision fields.**  
   - Give issue, deadline, financial impact, and status stronger visual priority than passive metadata.  
   - Allow product names to wrap to two lines or expose distinguishing SKU text before truncation.  
   - **Acceptance:** a row can be scanned left-to-right to answer: what is wrong, how urgent is it, what is the impact, who owns it, what should I do?

7. **Make status and actions explicit.**  
   - Replace dot-only status with text labels such as “Blocked,” “At risk,” “Due today,” or “Monitoring,” using semantic amber/red where appropriate.  
   - Replace three unlabeled action icons with one primary labeled action plus a labeled overflow.  
   - **Acceptance:** status and primary action remain understandable without relying on color or icon recognition.

8. **Reduce container noise and establish a spacing/type rhythm.**  
   - Reserve borders/shadows for major regions only; use separators, whitespace, and typography for internal grouping.  
   - Raise body text to a durable operations size and improve contrast while preserving the navy/ink neutral system.  
   - **Acceptance:** repeated cards no longer compete equally; section spacing follows a small consistent scale, for example compact/standard/large rather than arbitrary 8–48px gaps.

## 5. Score band

**Static score band: 5–6 / 10.**  
Justification: the screen includes the necessary operational ingredients, but the described hierarchy, table placement, ambiguous status/action treatment, and missing production states directly conflict with the primary job of finding next-hour exceptions quickly.

## 6. Smallest validation plan that could change the verdict

1. **Viewport check:** test the real page at 1366×768 and 1440×900 to verify whether exception rows are visible before scrolling.  
2. **Dense-data check:** load realistic long product names, long issue labels, high financial-impact values, and translated labels.  
3. **State check:** inspect loading, empty, partial-error, stale-refresh, and failed-export states.  
4. **Keyboard check:** tab through global search, date range, export, table rows, status controls, and row actions to verify visible focus and usable order.  
5. **Decision-speed check:** with real analysts or a timed internal review, ask: “Which three exceptions need action in the next hour?” and measure whether the table, not the KPI/chart area, drives the answer.
