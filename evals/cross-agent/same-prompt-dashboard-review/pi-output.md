# Pi observed output

- Agent: Pi
- Version: `0.80.3`
- Date: 2026-07-01
- Prompt SHA-256: `b622939ec19d093fc5bee6bc06d93f29f1016f47db66505642bd8752e74f584b`
- Command summary: `pi --skill skills/design-craft --tools read,grep,find,ls --no-session -p ...`
- Skill path observed: `skills/design-craft`

## Output

1. Evidence Level & Score Band

**Evidence level: L0 (prompt-only, no runtime evidence).** No screenshot, DOM, responsive run, focus walk, hover state, loading state, error state, or real data was verified. All judgments below are based solely on the prompt's structural description.

**Score band: 45-55 / 100 (Needs Work).** The described layout has the bones of an enterprise dashboard but exhibits the classic "card soup" anti-pattern: equal-weight KPI cards, decorative chart, dense table with no decision hierarchy, and a right rail of generic tips that wastes prime screen real estate. This is a dashboard that looks assembled rather than composed for a specific operator job.

---

## 2. Design Read

**Reading this as: internal ecommerce revenue operations dashboard for an operator, restrained-enterprise-console mood, optimized for "what needs my attention in the next hour?"**

The current mismatch: the dashboard presents 12 KPI cards as if they're equally important, when the operator's real job is triage - spotting the 1-2 accounts or campaigns that are on fire *right now* and acting on them. The visual weight should bend toward anomaly, risk, and action, not toward decorative symmetry.

---

## 3. Top Hierarchy / Product-Fit Issues

### Issue 1: Equal-weight KPI grid kills decision speed
Twelve equal KPI cards (same size, same surface, same color) force the operator to read all 12 and mentally rank them. This is the defining "card soup" pattern from the design-move-library. The operator's job is *triage* - the dashboard must surface which 1-2 metrics are outside normal range, not present all 12 with equal visual voice.

### Issue 2: Decorative area chart wastes the most valuable screen real estate
An area chart that does not answer a specific operational question is visual noise. If it's showing a trend, the operator needs to know: *trend of what? Compared to what threshold? Is this normal?* Without that context, it's decoration, not a decision tool.

### Issue 3: Dense account table lacks task-first ordering
A table where "database order" wins over "user task order" is a data dump. The operator needs the most at-risk accounts, the ones with payment failures, the ones with anomalously low conversion - not alphabetical or evenly distributed rows. Columns should follow the decision flow: status -> alert -> action, not schema order.

### Issue 4: Right rail with generic tips is dead weight
A right rail is premium screen real estate. Filling it with generic tips means the operator learns to ignore it (banner blindness). This space should hold an exception queue, a next-action panel, or a compact alert log - something that changes scan-to-scan and earns its permanent placement.

### Issue 5: No explicit loading / empty / error states described
An enterprise revenue dashboard that doesn't handle "data is stale," "pipeline is empty," or "API failed" gracefully is unfinished. These states are part of the product, not edge cases.

### Issue 6: "Restrained enterprise console" style authority is stated but unverified
The prompt claims a token-backed, restrained, dense-but-calm style. But 12 equal cards with a decorative chart and a generic tips rail is the opposite of restrained - it's symmetric filler. A truly restrained console would have: one dominant lead metric, a compact supporting strip, and an action queue, with color used only for semantic state.

---

## 4. Concrete Design Moves

Using design-craft vocabulary from the design-move-library and foundational principles:

### Move 1: Card soup -> decision surface
**From:** 12 equal KPI cards.  
**To:** One lead metric (e.g., "Revenue at Risk: $X") at 2x width, 6-8 compact supporting KPIs in a horizontal strip below, and a role-based anomaly panel.  
**Rationale:** Lead + support + action queue layout (design-move-library). The operator identifies the top risk within 3 seconds.  
**Visual:** Variance 2, Density 7, Motion 1 (surface-playbooks dashboard defaults).

### Move 2: Decorative chart -> diagnostic chart with explicit question
**From:** Generic area chart with no context.  
**To:** A chart that answers one question: "Revenue trend vs. target, last 7 days, with threshold band." Or remove it entirely if it doesn't earn its space.  
**Rationale:** A chart should answer a question, not fill space (surface-playbooks: "Pick the chart from the analytical question, not decoration").

### Move 3: Dense table -> task-first table
**From:** Columns in database/schema order.  
**To:** Decision-critical columns first: status indicator -> account name -> risk score -> revenue delta -> next action. Metadata columns collapsed or moved right. Row actions (e.g., "Investigate," "Escalate") anchored to the right edge.  
**Rationale:** Right-align numerics, left-align text, put status and action where the eye lands first (design-move-library).

### Move 4: Generic tips -> exception queue / action panel
**From:** Static tips the operator ignores.  
**To:** A live "Needs Attention" queue: accounts with payment failures, campaigns with cost-per-acquisition spikes, anomalies flagged by the system. Each item is scannable and actionable.  
**Rationale:** Proximity principle - related items (risk, action) should be close. The right rail earns its permanence with fresh, actionable content.

### Move 5: Color as semantic state, not decoration
**From:** Color used for card surfaces or chart fills.  
**To:** Color only for status: red for at-risk, amber for warning, green for healthy, neutral for neutral. No decorative gradients, no tinted cards without meaning.  
**Rationale:** Contrast principle - "Weak contrast feels timid; excessive contrast feels noisy." Token-backed color means every color has a job.

---

## 5. Verified vs. Unverified Claims

| Claim | Status |
|---|---|
| Dashboard has 12 equal KPI cards | **Unverified** - prompt assertion only |
| Area chart is decorative | **Unverified** - could serve a real purpose; no evidence |
| Account table is dense and untasked | **Unverified** - column order, row density, and action availability unknown |
| Right rail has generic tips | **Unverified** - prompt assertion only |
| Style is "restrained enterprise console" | **Unverified** - no visual evidence, token file, or DESIGN.md |
| Empty/loading/error states exist | **Unverified** - not mentioned in prompt |
| Responsive behavior | **Unverified** - no viewport testing |
| Focus, hover, keyboard accessibility | **Unverified** - no interaction evidence |
| Color contrast meets WCAG | **Unverified** - no color values or contrast check |

**All claims above are prompt-only. A real critique would require at minimum: one screenshot at 1440px, one at 1280px, a hover pass on the table, and a focus walk.**

---

## 6. Minimal Validation Plan Before Implementation

1. **Screenshot audit (desktop 1440px, 1280px):** Confirm the actual layout, card count, chart type, table columns, and right rail content. Capture with `design_craft_browser_evidence.py` or equivalent.
2. **DOM / computed-style snapshot:** Extract actual token values (colors, spacing, typography scales, border radii) and compare against the claimed "restrained enterprise" style authority.
3. **Task walkthrough:** With a real operator or a scenario list, time how long it takes to answer: "Which account needs attention right now?" Baseline this before any redesign.
4. **State audit:** Manually verify empty-state, loading-state, error-state, and stale-data treatments for KPI cards, the chart, and the table.
5. **Accessibility pass:** Contrast check on all status colors, focus-visible on all interactive elements, keyboard navigation through the table and right rail.
6. **Design read sign-off:** Confirm with stakeholders that the primary job is "triage for the next hour," not "general overview." If the real job is different, the entire critique changes.

---

### Delivery Summary

| Field | Value |
|---|---|
| `frontend_tier` | N/A (read-only critique) |
| Mode | `critique` |
| `style_authority_path` | None verified; prompt describes "restrained enterprise console" but no DESIGN.md or token file was provided |
| `design_system_contract` | Not applicable - no tokens or components verified |
| `candidate_skills` | `design-craft` (used) |
| `selected_skills` | `design-craft` |
| References used | `visual-judgment.md`, `product-ui-taste-review.md`, `design-move-library.md`, `surface-playbooks.md`, `foundational-visual-principles.md` |
| Browser validation | Skipped (read-only benchmark, no runtime evidence available) |
| Screenshot validation | Skipped (no screenshot provided) |
| Performance impact | Not applicable (read-only) |
| Remaining risks | All judgments are prompt-only; real dashboard may differ materially from the description |
