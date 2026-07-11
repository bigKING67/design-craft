Now I have all the design-craft references for a dashboard critique. Let me compose the full review.

---

# Design-Craft Critique: Revenue Operations Dashboard

**Method:** single-context (prose description only, no screenshot or DOM).
**Mode:** `critique` (read-only, no edits, no browser validation).
**Design-craft references read:** `surface-playbooks.md`, `product-ui-taste-review.md`, `taste-score-calibration.md`, `design-move-library.md`, `foundational-visual-principles.md`, `product-context.md`, `validation-contract.md`.

---

## 1. Evidence Level and Score Band

**Evidence level: L0 static** — prose description only. No screenshot, DOM, responsive run, focus walk, hover state, loading state, error state, or real-content behavior was verified. All interaction, state, responsive, and accessibility claims below are **unverified**.

**Product UI taste score: 74 / 100**
**Band: Functional but ordinary** (60-74, upper edge).

**Why this score:**
- **+** The description implies a restrained enterprise aesthetic (no marketing hero, token-backed color), which aligns with the product register.
- **+** A dense account table suggests the data model is intact and the team has prioritized information over decoration.
- **−** 12 equal KPI cards is a canonical "card soup" antipattern: flat priority with no lead metric, no risk hierarchy, no operational urgency. This alone caps the score at 84 by the anti-inflation rule.
- **−** A decorative area chart, a right rail of generic tips, and a dense table with no visible task structure means the layout lacks a clear decision surface — the central job of the dashboard.
- **−** L0 evidence means interaction states, responsive behavior, keyboard, focus, loading, empty, error, and real-content overflow are all unscored and unclaimed.

**Not scored as verified:** hover, focus, active, selected, disabled, loading, empty, error, success, keyboard navigation, responsive layout, text scaling, reduced motion, real content overflow, or any implementation artifact.

---

## 2. Design Read

> **Reading this as:** an ops command-center dashboard for an internal ecommerce operator, with a restrained enterprise-console mood, optimized for **identifying the account or campaign that needs attention in the next hour**.

The primary job is **triage**: the operator must discriminate anomalous or at-risk accounts from routine traffic within seconds, then route attention to the highest-impact item. The dashboard must prioritize exceptions, not summarize totals.

**Main mismatch:** The current structure (equal KPI grid → decorative chart → dense table → generic tips rail) treats overview as the job, when the real job is exception detection and action routing.

---

## 3. Top Hierarchy and Product-Fit Issues

These are ordered by severity, using design-craft vocabulary from `foundational-visual-principles.md` and `surface-playbooks.md`.

### P0 — Flat priority: 12 equal KPI cards (Attention / Contrast failure)

**Problem:** Twelve equal-sized, equal-weight cards violate the core premise of attention design: "If everything is emphasized, nothing is important." The operator cannot tell which metric is healthy and which signals a problem without decoding all twelve values.

**Why it hurts the product job:** An operator with one hour to act needs the dashboard to flag the anomaly, not present a tidy grid. A 3% CPC drift that could cost real money looks identical to a flat session count.

**Design-craft principle violated:** Attention — "Decide what should be noticed first, second, and last." Contrast — "Different importance, action strength, state, risk, or role must look different enough to scan quickly." Similarity — "Similar-looking objects will be interpreted as similar in function."

### P0 — No exception queue or risk surface (Task Focus failure)

**Problem:** The dashboard describes what happened but does not surface what needs action. There is no dedicated area for accounts that crossed a threshold, campaigns that are overspending, or metrics that are outside their expected range.

**Why it hurts the product job:** The operator's core loop — scan → detect anomaly → investigate → act — has no entry point. Every investigation starts from a level playing field of 12 equal cards and a dense table.

**Design-craft principle violated:** Task Focus — "The main task, first focus, and primary action are obvious." Continuity — "The scan path should follow the user's decision flow."

### P1 — Decorative area chart (Economy violation)

**Problem:** An area chart without a clear analytical question is decoration. If it shows "revenue over time" without threshold bands, anomaly markers, or comparison lines, it consumes space without answering "compared to what?"

**Why it hurts taste:** Decorative charts are a common AI/demo tell. Per the surface playbook for dashboards: "Pick the chart from the analytical question, not decoration."

**Design-craft principle violated:** Economy — "Remove visual decisions that do not clarify task, structure, state, or brand."

### P1 — Generic tips right rail (Product-fit failure)

**Problem:** A rail of untargeted tips is a content placeholder, not a decision aid. Tips tied to the specific accounts or metrics showing anomalous behavior would support the job; generic tips consume space and teach the operator to ignore the rail.

**Why it hurts taste:** It signals that the dashboard was laid out from a template skeleton, not designed around the operator's real workflow. A tip that says "Review high-CPC campaigns weekly" when a specific campaign is actively overspending is worse than no tip at all — it undermines trust.

### P2 — Table as data dump (Information Order failure)

**Problem:** The account table is described as "dense" but with no indication of decision-critical column ordering. If it follows schema order (ID → name → date → status → metrics → notes), the operator must horizontally decode rows to find the actionable column.

**Design-craft move indicated:** Table as data dump → task-first table. "Put decision-critical columns first. Group metadata and secondary attributes. Make row action, status, and recovery paths explicit."

---

## 4. Concrete Design Moves

Using vocabulary from `design-move-library.md`, treatment variant: **Ops command center**.

### Move 1: Card soup → Decision surface

**Before:**
```
[KPI 1] [KPI 2] [KPI 3] [KPI 4]   ← 12 equal cards in a 4×3 grid
[KPI 5] [KPI 6] [KPI 7] [KPI 8]
[KPI 9] [KPI 10][KPI 11][KPI 12]
```

**After:**
```
[LEAD RISK METRIC — large, semantic color]   ← "3 accounts overspending (>15% CPC drift)"
[supporting strip: Revenue · ROAS · Conv. Rate · Sessions]   ← compact, tabular style
[EXCEPTION QUEUE]                                              ← ranked by impact
  → Acme Corp: +23% CPC, $4.2k at risk, paused yesterday
  → Beta Store: -18% conv rate, $2.8k below target
  → Gamma Shop: budget 92% consumed, 6 days remaining
[DIAGNOSTIC CHART]                                             ← area chart WITH threshold bands, anomaly markers
[TASK-FIRST TABLE]                                             ← status/risk/next-action columns first
```

Acceptance criteria: operator can identify the top risk within 3 seconds; exceptions precede overview; supporting KPIs are compressed into a single strip.

### Move 2: Flat KPI grid → Priority hierarchy

Split metrics into three tiers:
- **Tier 1 (lead):** One compound metric or operational state — the highest-risk signal. Paired with threshold context ("vs. 7-day avg").
- **Tier 2 (supporting strip):** 4-6 core health metrics in a compact horizontal band with right-aligned numbers, deltas, and minimal decoration.
- **Tier 3 (diagnostic):** Secondary metrics disclosed behind a toggle or placed below the decision surface.

### Move 3: Decorative chart → Diagnostic chart

Add threshold bands, anomaly markers, and a comparison baseline to the chart so it answers a concrete question: "Is this metric outside its expected range today, and if so, since when?" This transforms the chart from decoration into a diagnostic tool.

### Move 4: Generic tips rail → Contextual alert panel

Replace the right rail with an **exception panel** that:
- Lists accounts/campaigns that crossed user-defined or ML-detected thresholds.
- Shows impact ($ at risk, trend direction, time since anomaly began).
- Links directly to the relevant row in the table.
- Collapses to a compact badge when empty.

### Move 5: Table as data dump → Task-first table

Reorder columns: **Account ID/Name → Status (semantic chip) → Risk/Anomaly indicator → Primary metric delta → Next-action → Metadata.** Right-align numeric columns. Add inline row actions (investigate, pause, adjust budget). Make the table filterable by status, anomaly, and owner with filters adjacent to the affected data.

### Move 6: Missing states → Resilient surface

Per design-move-library "Missing states → resilient product surface":
- **Empty:** "No accounts are currently outside expected thresholds. Last check: 2 min ago." Point to healthy overview.
- **Loading:** Skeleton with semantic structure (lead strip → queue placeholder → table skeleton), not a single spinner.
- **Error:** "Could not load account data. Retry or view cached snapshot from 10:42 AM."
- **Long text/data:** Truncation rules, tooltip fallback, and overflow behavior specified for every column and metric.

---

## 5. Verified vs. Unverified Claims

| Claim | Status |
|---|---|
| 12 equal KPI cards exist | **Unverified** — accepted from prompt description |
| Area chart is decorative (no threshold bands, no markers) | **Unverified** — inferred from "decorative" descriptor; actual chart may have partial analysis |
| Right rail contains generic tips | **Unverified** — accepted from prompt description |
| Account table is data-dense but not task-ordered | **Unverified** — accepted from prompt description |
| Token-backed color only | **Unverified** — no token definition or computed-style evidence |
| Restrained enterprise aesthetic | **Unverified** — no screenshot confirms visual restraint |
| Responsive behavior exists | **Not claimed** — explicitly excluded from evidence scope |
| Hover, focus, active, disabled states exist | **Not claimed** |
| Loading, empty, error, success states exist | **Not claimed** |
| Keyboard navigation works | **Not claimed** |
| Data updates in real-time or near-real-time | **Not claimed** — unknown from prompt |

---

## 6. Minimal Validation Plan Before Implementation

Per `validation-contract.md`, before any implementation begins, the following gates must be passed. This plan assumes the dashboard has a working dev environment.

### Gate 1: Live evidence capture (L2 minimum)

Capture a full-viewport screenshot of the current dashboard with real data. This moves the evidence level from L0 to L2 and confirms the structural diagnosis before changes are made.

**Tool path:** `browser_screenshot_ops target:"viewport"` or Chrome DevTools full-page capture.

### Gate 2: Static smell scan

If source code is available:
```bash
# Token audit for hardcoded colors/spacing vs. design tokens
scripts/design_craft_token_audit.py --target <dashboard-component-dir>

# CSS smell scan for fragile layout, magic numbers, missing states
scripts/design_craft_css_smell_scan.py --target <dashboard-component-dir>

# Focus audit for keyboard accessibility gaps
scripts/design_craft_focus_audit.py --target <dashboard-component-dir>
```
Treat scanner output as review prompts, not verdicts.

### Gate 3: Responsive baseline

Check the current dashboard at 1280px, 1440px, and 1024px widths. Record:
- Whether the 12-card grid collapses or overflows.
- Whether the right rail stacks, disappears, or causes horizontal scroll.
- Whether the table has horizontal overflow with frozen columns.

### Gate 4: State inventory

List every component in the dashboard and map its required states:
- KPI cards: nominal, warning, critical, loading, error, empty/no-data.
- Chart: loading, empty, error, single-data-point, threshold-visible.
- Table: loading, empty, error, single-row, many-rows, filtered-to-zero.
- Rail: loading, empty, error, single-tip, many-tips.

Any component missing >2 of these states should be hardened before structural redesign begins.

### Gate 5: Operator workflow confirmation

Interview or observe 2-3 operators for 15 minutes each. Confirm:
- Which metric they look at first.
- Whether they scan the table by column or by row.
- Whether they ever read the tips rail.
- What their actual triage sequence is: which anomaly types trigger the fastest response.

This gates the design read before implementation commits to a specific decision-surface shape.

### Gate 6: Token authority check

If a `DESIGN.md` or token file exists:
- Confirm the dashboard uses token references, not hardcoded hex/rgba/spacing.
- Identify any "enterprise dense" treatment tokens needed but not yet defined (e.g., `--status-critical`, `--metric-delta-negative`, `--table-row-hover`).

### Unverified assumptions to resolve

Before finalizing the redesign:
1. Is the dashboard static or does it update in near-real-time? (Changes the loading/animation strategy.)
2. Are thresholds user-configurable or system-defined? (Changes the exception-queue design.)
3. Does the operator need to act inside the dashboard (pause campaign, adjust budget) or does it link to another tool? (Changes whether inline row actions are needed or just navigation.)
4. What is the actual data refresh interval? (Changes skeleton vs. spinner vs. stale-while-revalidate strategy.)

---

**Summary:** The current dashboard structure is a functional data display surface dressed as an operational decision tool. It presents information but does not prioritize action. The four structural changes — lead risk metric, exception queue replacing the tips rail, diagnostic chart replacing the decorative chart, and task-first table — would realign the surface with the operator's triage job. Score band (74) reflects a coherent data model let down by flat hierarchy and missing decision grammar, not visual incompetence. No score above 84 is justified until the card soup is restructured, and no score above 92 is justified without L3 browser evidence across states, viewports, and real content.
