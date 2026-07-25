# Blind comparative judgment
Judge only the supplied outputs. Do not infer which skill produced a label. Apply the machine-readable scorecard exactly, recompute each total from criterion points, and return only JSON matching the supplied schema.

## Task prompt

# Inventory editor production audit

Perform a read-only production audit of this static React product-surface
description. Do not edit files or claim that a detector, browser, build,
profiler, accessibility tree, network throttle, or device run actually
occurred. Do not name, cite, or reveal any skill, repository, author, or
upstream source in the response; the output will be judged blind.

Product context:

- Desktop-first inventory editor used by operations staff, with tablet support.
- The route contains filters, a 10,000-row product table, bulk selection, an
  edit drawer, image uploads, and an autosave status.
- The existing design system and workflow must be preserved; this is a
  production hardening/polish task, not a redesign or new dependency pitch.

Observed source facts:

```tsx
function InventoryPage() {
  const [rows, setRows] = useState(allRows);
  const [saving, setSaving] = useState(false);

  async function saveProduct(product) {
    setSaving(true);
    try {
      await api.save(product);
    } catch {}
    setSaving(false);
  }

  return (
    <div className="page">
      <Filters />
      {rows.map((row) => <ProductRow key={row.id} row={row} />)}
      <EditDrawer onSave={saveProduct} saving={saving} />
    </div>
  );
}
```

```css
.page { min-width: 1180px; }
.product-row { display: grid; grid-template-columns: 64px 280px 1fr 120px 96px; }
.product-row, .drawer { transition: all 300ms ease-in; }
.product-name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.drawer { position: fixed; right: 0; width: 520px; height: 100vh; }
.icon-button { width: 28px; height: 28px; outline: none; }
```

Additional source notes:

- Initial and filter loading render a blank table body.
- Empty results, 401/403, 409 conflict, 429, 500, timeout, offline, retry, and
  partial batch failure states are not represented.
- Product names may be 1-200 characters; prices may be missing; translations
  may expand labels by 60 percent; some images are absent or 8MB.
- The drawer traps neither focus nor background interaction. Escape closes it
  even while a save is pending. Save and close are icon-only.
- All 10,000 rows render at once; filtering recalculates synchronously on every
  keystroke. Image dimensions are not reserved.
- Tablet behavior, keyboard navigation, screen-reader labels, focus-visible,
  reduced motion, and permission-specific affordances are not described.

Return:

1. The correct audit/polish/harden/optimize sequencing and one-line verdict.
2. Prioritized P0-P3 findings with source evidence versus runtime hypotheses.
3. Concrete fixes for hostile data, failures, responsive layout,
   accessibility, state recovery, and performance.
4. Reconcile which static detector-like signals are decisive and which need
   project/runtime context.
5. A measurement-first validation plan with rollback/acceptance conditions.

Stay within 180 lines. Do not turn this into a ground-up redesign.


## Human-readable scorecard

# Comparative scorecard

Generated from `scorecard.json`; do not edit by hand.

| Criterion | Weight | Full credit |
|---|---:|---|
| Mode sequencing and prioritization | 10 | Chooses audit before targeted polish, hardening, and measured optimization with coherent P0-P3 severity. |
| Hostile data and failure hardening | 20 | Covers long and missing data, permissions, conflicts, limits, offline, retry, partial failures, uploads, and truthful save recovery. |
| Responsive and accessibility quality | 15 | Repairs fixed geometry, drawer interaction, keyboard, focus, labels, touch targets, translations, reduced motion, and tablet adaptation. |
| Measurement-first performance | 15 | Identifies render, filter, image, and layout hot paths and requires baselines, thresholds, and rollback conditions. |
| Detector and design-system reconciliation | 10 | Treats static anti-patterns as contextual signals under project authority instead of fabricated runtime proof. |
| Concrete production fixes | 20 | Provides implementation-ready state, error, layout, accessibility, scale, and recovery moves with acceptance conditions. |
| Evidence honesty and scope control | 10 | Separates static proof from hypotheses, claims no unrun tools, stays read-only, and avoids redesign or unjustified dependencies. |
| **Total** | **100** | |


## Machine-readable scorecard

```json
{
  "schema": "design-craft.comparative-scorecard.v1",
  "total": 100,
  "criteria": [
    {
      "id": "mode_sequence",
      "label": "Mode sequencing and prioritization",
      "weight": 10,
      "full_credit": "Chooses audit before targeted polish, hardening, and measured optimization with coherent P0-P3 severity."
    },
    {
      "id": "hostile_data",
      "label": "Hostile data and failure hardening",
      "weight": 20,
      "full_credit": "Covers long and missing data, permissions, conflicts, limits, offline, retry, partial failures, uploads, and truthful save recovery."
    },
    {
      "id": "responsive_accessibility",
      "label": "Responsive and accessibility quality",
      "weight": 15,
      "full_credit": "Repairs fixed geometry, drawer interaction, keyboard, focus, labels, touch targets, translations, reduced motion, and tablet adaptation."
    },
    {
      "id": "measured_performance",
      "label": "Measurement-first performance",
      "weight": 15,
      "full_credit": "Identifies render, filter, image, and layout hot paths and requires baselines, thresholds, and rollback conditions."
    },
    {
      "id": "detector_reconciliation",
      "label": "Detector and design-system reconciliation",
      "weight": 10,
      "full_credit": "Treats static anti-patterns as contextual signals under project authority instead of fabricated runtime proof."
    },
    {
      "id": "production_fixes",
      "label": "Concrete production fixes",
      "weight": 20,
      "full_credit": "Provides implementation-ready state, error, layout, accessibility, scale, and recovery moves with acceptance conditions."
    },
    {
      "id": "evidence_scope",
      "label": "Evidence honesty and scope control",
      "weight": 10,
      "full_credit": "Separates static proof from hypotheses, claims no unrun tools, stays read-only, and avoids redesign or unjustified dependencies."
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
              "mode_sequence",
              "hostile_data",
              "responsive_accessibility",
              "measured_performance",
              "detector_reconciliation",
              "production_fixes",
              "evidence_scope"
            ],
            "additionalProperties": false,
            "properties": {
              "mode_sequence": {"type": "integer", "minimum": 0, "maximum": 10},
              "hostile_data": {"type": "integer", "minimum": 0, "maximum": 20},
              "responsive_accessibility": {"type": "integer", "minimum": 0, "maximum": 15},
              "measured_performance": {"type": "integer", "minimum": 0, "maximum": 15},
              "detector_reconciliation": {"type": "integer", "minimum": 0, "maximum": 10},
              "production_fixes": {"type": "integer", "minimum": 0, "maximum": 20},
              "evidence_scope": {"type": "integer", "minimum": 0, "maximum": 10}
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

## 1) Correct sequence + verdict

**Sequence:** static audit → P0/P1 hardening for data loss and failure states → performance optimization of table/filter/image hot paths → accessibility and responsive fixes → visual polish only after behavior is safe → measured release with rollback gates.

**One-line verdict:** The surface is not production-ready for operations use: the static evidence shows high data-loss risk, missing recovery states, table-scale performance risk, and accessibility/responsive blockers, but it can be hardened without a ground-up redesign.

---

## 2) Prioritized findings: evidence vs runtime hypotheses

### P0 — Blocking / data-loss risk

**P0.1 Silent save failure hides failed writes**
- **Source evidence:** `catch {}` swallows `api.save(product)` errors; `saving` returns false regardless of outcome.
- **Impact:** Operators can believe a product was saved when it was not.
- **Runtime hypothesis:** Actual backend errors, timeouts, or conflicts may be more or less common; frequency needs measurement.
- **Fix:** Return explicit save states: `idle | saving | saved | failed | conflict | offline | retrying`. Preserve failed draft, show inline error, expose retry, and never mark success without confirmation.

**P0.2 Drawer can close during pending save**
- **Source evidence:** “Escape closes it even while a save is pending.”
- **Impact:** Unsaved edits can be lost or become ambiguous.
- **Runtime hypothesis:** Whether form state survives drawer unmount is unknown.
- **Fix:** While save is pending, disable destructive close or require confirmation. If close is allowed, keep draft state and show recoverable “save still pending / failed” status.

**P0.3 Conflict and auth states are absent**
- **Source evidence:** 401/403, 409 conflict, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.
- **Impact:** Operators cannot resolve permission loss, stale edits, rate limits, or partial bulk failures.
- **Runtime hypothesis:** Exact API status mapping needs project context.
- **Fix:** Add state-specific UI: re-auth/permission message, conflict compare/refresh, retry-after handling, offline queue notice, and per-row partial failure summary.

---

### P1 — Major release blockers

**P1.1 All 10,000 rows render at once**
- **Source evidence:** `{rows.map((row) => <ProductRow ... />)}` with 10,000-row context.
- **Impact:** Slow initial render, heavy reconciliation, poor keyboard/search responsiveness.
- **Runtime hypothesis:** Exact frame drops depend on row complexity and device.
- **Fix:** Window visible rows with overscan, preserve selection across offscreen rows, keep row height deterministic, and avoid remounting edited rows unnecessarily.

**P1.2 Filtering is synchronous on every keystroke**
- **Source evidence:** Additional note says filtering recalculates synchronously on every keystroke.
- **Impact:** Input lag on the main workflow.
- **Runtime hypothesis:** Cost depends on predicate complexity and row shape.
- **Fix:** Debounce or defer filter computation, memoize derived rows, tokenize searchable fields once, and keep input controlled responsiveness separate from expensive table updates.

**P1.3 Drawer lacks modal accessibility containment**
- **Source evidence:** “The drawer traps neither focus nor background interaction.”
- **Impact:** Keyboard and screen-reader users can interact with obscured content; focus can escape the task context.
- **Runtime hypothesis:** Underlying markup may have partial semantics, but the stated behavior is already enough to fail.
- **Fix:** Use dialog semantics or equivalent: labelled drawer, initial focus, focus trap, inert/blocked background, restore focus to opener, Escape behavior gated by dirty/saving state.

**P1.4 Icon-only save/close controls are under-specified**
- **Source evidence:** “Save and close are icon-only”; screen-reader labels are not described.
- **Impact:** Assistive tech and some sighted users may not know what actions do.
- **Runtime hypothesis:** Hidden labels may exist elsewhere, but not in the provided facts.
- **Fix:** Add accessible names, visible tooltip/help where useful, disabled/loading labels, and confirm destructive close when dirty.

**P1.5 Focus indicators are explicitly removed**
- **Source evidence:** `.icon-button { ... outline: none; }`
- **Impact:** Keyboard users can lose location, especially in dense table/drawer flows.
- **Runtime hypothesis:** A replacement `:focus-visible` style could exist elsewhere, but none is shown.
- **Fix:** Restore visible `:focus-visible` using existing focus token; minimum 2px high-contrast ring or equivalent offset state.

**P1.6 Tablet support conflicts with fixed desktop width**
- **Source evidence:** `.page { min-width: 1180px; }`; tablet behavior not described.
- **Impact:** Likely horizontal overflow or unusable drawer/table on tablets.
- **Runtime hypothesis:** A parent shell may provide horizontal scroll, but usability remains unproven.
- **Fix:** Define tablet behavior: pinned horizontal table scroll with sticky key columns, drawer width clamped to viewport, filters wrapping/collapsing predictably, touch targets enlarged.

---

### P2 — Important hardening/polish

**P2.1 Blank loading state creates false emptiness**
- **Source evidence:** Initial/filter loading render a blank table body.
- **Impact:** Users cannot distinguish loading, empty results, failed load, or filtered-out inventory.
- **Runtime hypothesis:** Loading duration unknown.
- **Fix:** Use table skeleton rows for initial/filter load; use explicit empty state with active filter summary and clear-filter action.

**P2.2 Hostile product data can break table clarity**
- **Source evidence:** Names 1–200 chars; prices may be missing; labels can expand 60%; images absent or 8MB.
- **Impact:** Truncation hides critical product identity; missing prices/images may look like load failures; translations may overflow.
- **Runtime hypothesis:** Actual localization strings and image dimensions need fixture coverage.
- **Fix:** Add long-name title/secondary line pattern, missing-price placeholder distinct from zero, image fallback state, localized label wrapping, and max-width/min-width rules per column.

**P2.3 Image layout shift and memory risk**
- **Source evidence:** Image dimensions are not reserved; some images are 8MB.
- **Impact:** Row jumpiness, expensive decode, slower scroll.
- **Runtime hypothesis:** CDN resizing/lazy loading unknown.
- **Fix:** Reserve aspect-ratio boxes, lazy-load offscreen images, request thumbnails for rows, decode async where supported, cap upload previews.

**P2.4 `transition: all` on rows and drawer is unsafe**
- **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`
- **Impact:** Accidental layout-property animation, sluggish drawer, unnecessary repaint/reflow, poor reduced-motion behavior.
- **Runtime hypothesis:** Which properties actually change requires code review/runtime inspection.
- **Fix:** Transition only `transform`, `opacity`, or tokenized color where needed; shorten to ~150–250ms for product UI; add reduced-motion alternative.

**P2.5 Global `saving` state is too coarse**
- **Source evidence:** Single `saving` boolean at page level passed to `EditDrawer`.
- **Impact:** One save can disable or misrepresent unrelated edits; concurrent saves are ambiguous.
- **Runtime hypothesis:** UI may allow only one open drawer, but bulk actions also exist.
- **Fix:** Track save state by product id or operation id. Keep separate autosave, manual save, and bulk save statuses.

**P2.6 Permission affordances are missing**
- **Source evidence:** “Permission-specific affordances are not described”; 401/403 states absent.
- **Impact:** Users may attempt unavailable edits/uploads/bulk actions and discover failure late.
- **Runtime hypothesis:** Permission model unknown.
- **Fix:** Render disabled/hidden actions according to permission policy, with reason text for disabled controls and audit-safe messaging.

---

### P3 — Polish / lower-risk improvements

**P3.1 Ellipsis needs disclosure behavior**
- **Source evidence:** `.product-name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }`
- **Impact:** Long names are preserved visually but not fully discoverable.
- **Runtime hypothesis:** Native title or detail drawer may already reveal full name.
- **Fix:** Ensure full name is available in drawer, accessible name, copy affordance, or non-blocking tooltip.

**P3.2 Column widths may not survive localization**
- **Source evidence:** Fixed grid columns: `64px 280px 1fr 120px 96px`; translations may expand labels by 60%.
- **Impact:** Header/control labels may clip.
- **Runtime hypothesis:** Actual column content unknown.
- **Fix:** Test with pseudo-localized strings and allow key labels to wrap or abbreviate with accessible full text.

---

## 3) Concrete fixes by area

**Hostile data**
- Add fixtures for 1-char and 200-char names, missing price, zero price, absent image, 8MB image, long SKU/category, and pseudo-localized labels.
- Use explicit placeholders: “No price set,” “No image,” “Unavailable,” not blank cells.
- Reserve image dimensions and request table thumbnails, not full uploads, for row display.

**Failures and recovery**
- Replace swallowed errors with typed outcomes.
- Show autosave state with timestamp and failed/retry state.
- Keep dirty draft after failed save or accidental close.
- For 409: show “This product changed elsewhere” with refresh/compare/reapply choices.
- For bulk partial failure: report affected rows, successful count, failed count, retry only failed.

**Responsive/tablet**
- Remove hard `min-width: 1180px` as the only strategy.
- Define tablet breakpoint behavior: horizontal table scroller, sticky identifier column, drawer `width: min(520px, 100vw)` or tablet-specific full-height panel.
- Increase touch targets to at least 44px on tablet, especially icon buttons.

**Accessibility**
- Restore `:focus-visible`.
- Use semantic buttons for icon actions with accessible names.
- Drawer needs role/dialog semantics, labelled title, focus trap, inert background, Escape rules, and focus return.
- Define keyboard table navigation: tab order, row action access, bulk selection behavior, and visible selected state.
- Add reduced-motion handling for drawer/row transitions.

**State recovery**
- Model row edits as durable draft state until confirmed saved.
- Add operation IDs to prevent late responses overwriting newer edits.
- On offline/timeout, keep local draft and display “not synced” rather than clearing saving.
- Make close behavior conditional: clean closes immediately; dirty/saving requires save, discard, or keep editing.

**Performance**
- Virtualize/window 10,000 rows.
- Memoize filtered rows and row render props.
- Defer expensive filtering from keystroke input.
- Avoid global `saving` rerendering all rows.
- Lazy-load and size row images.
- Replace `transition: all` with specific composited properties.

---

## 4) Static detector-like signal reconciliation

**Decisive from static evidence**
- `catch {}` is a real silent-failure defect.
- Rendering `rows.map` for 10,000 rows is a real scale risk.
- `outline: none` without shown replacement is a serious focus-risk signal.
- `transition: all` is a real animation/performance smell.
- `min-width: 1180px` conflicts with stated tablet support unless an explicit overflow strategy exists.
- Missing represented states for 401/403/409/429/500/offline/partial failure is a production hardening gap.

**Needs project/runtime context**
- Exact accessibility pass/fail for ProductRow semantics, table roles, labels, and reading order.
- Actual contrast ratios and focus-ring visibility.
- Actual render time, memory, and input latency.
- Whether existing design tokens already provide responsive/focus/error states.
- Whether API client already retries, times out, cancels, or maps error types.
- Whether image CDN/upload pipeline already resizes or validates files.
- Whether permissions are enforced server-side only or also available client-side.

---

## 5) Measurement-first validation plan with rollback/acceptance

**Before changes**
- Capture baseline on representative data: 10,000 rows, long names, missing prices/images, large images, pseudo-localized labels, and failure responses.
- Measure initial render time, filter input latency, drawer open/close responsiveness, save failure recovery, and row scroll smoothness.
- Record keyboard-only completion path: filter → open drawer → edit → save → close → bulk select.

**Acceptance conditions**
- Failed save is visible, recoverable, and never reported as success.
- Dirty/saving drawer cannot lose edits through Escape or background interaction.
- 401/403/409/429/500/timeout/offline/partial batch states have distinct user actions.
- 10,000-row table remains responsive during scroll and filtering on target hardware.
- Filter input remains responsive while results update.
- Tablet layout has no uncontrolled page-level overflow except intentional table scrolling.
- All icon-only controls have accessible names and visible focus.
- Reduced-motion mode removes nonessential motion while preserving state feedback.
- Images do not cause major row layout shift.

**Rollback conditions**
- Save success/failure ambiguity remains.
- Conflict/offline paths can still discard edits.
- Table optimization breaks selection, edit targeting, or bulk actions.
- Accessibility containment blocks normal keyboard escape/recovery.
- Tablet changes hide required columns/actions without an alternate path.
- Performance work introduces stale rows, wrong filters, or mismatched save status.

**Release approach**
- Ship behind a guarded rollout if possible: first error-state/save recovery, then table/windowing, then responsive/a11y polish.
- Keep telemetry focused on task health: save failures, retry success, conflict frequency, filter latency, drawer abandon rate, and bulk partial failures.
- Roll back the smallest layer that regresses task completion; do not roll back visual polish together with data-safety fixes unless they are coupled.


## Output B

## 1. Correct sequence + verdict

**Sequence:** static audit → define baseline measurements → harden data/failure/recovery/accessibility blockers → optimize measured table/filter/image hot paths → polish visual states within the existing system → release validation with rollback gates.

**Verdict:** Not production-ready for a 10,000-row operations editor: the supplied source shows decisive save-error invisibility, missing recovery states, drawer accessibility gaps, hostile-data fragility, and high-risk unbounded rendering; fix by hardening the existing workflow, not redesigning it.

---

## 2. Prioritized findings: source evidence vs runtime hypotheses

| ID | Pri | Finding | Source evidence | Runtime/context boundary | Concrete fix / acceptance |
|---|---:|---|---|---|---|
| F1 | P0 | Save failures can be silent, causing false confidence and possible data loss. | `catch {}` swallows errors; `setSaving(false)` runs without error state; autosave/status behavior not represented. | Exact server/API semantics and whether parent state mutates optimistically are unknown. | Return typed save result; show success/error/conflict/offline states; retain dirty edits after failure; expose retry; log/report errors; never mark failed save as saved. Acceptance: forced 500/timeout/offline keeps drawer data, announces failure, and allows retry without losing edits. |
| F2 | P0 | Pending save can be interrupted by drawer close. | Notes: Escape closes drawer even while save is pending. | Whether close also discards local edits is not shown, but the interruption path is explicit. | While saving: disable destructive close or require confirmation; allow cancel only if request is abortable and state is recoverable; show “Saving…” with deterministic completion/failure. Acceptance: Escape during pending save cannot silently discard or hide unsaved state. |
| F3 | P1 | Required operational failure states are absent. | Notes explicitly list missing empty, 401/403, 409, 429, 500, timeout, offline, retry, partial batch failure; loading renders blank body. | Exact visual components are unknown, but absence is stated in supplied scope. | Add table-body states: skeleton/progress for loading; empty result with filter reset; permission-specific locked affordances; conflict compare/reload/apply path; rate-limit wait/retry; server/timeout/offline retry; partial batch result summary with per-row status. Acceptance: every listed state renders clear cause, next action, and preserves filters/selection/drawer context where safe. |
| F4 | P1 | Drawer is not accessible as a modal editing surface. | Notes: no focus trap, no background interaction blocking; Save/close are icon-only. CSS: fixed drawer. | Whether drawer is intended modal or non-modal needs product confirmation; current notes describe unsafe modal-like behavior. | If modal: use dialog semantics, labelled title, focus trap, restore focus on close, background inert, Escape policy aware of dirty/saving state. If non-modal: keep table keyboard reachable intentionally and define focus order. Icon buttons need accessible names and visible labels/tooltips where appropriate. |
| F5 | P1 | Keyboard and visible focus support are likely broken for controls. | `.icon-button { width:28px; height:28px; outline:none; }`; notes: keyboard navigation, screen-reader labels, focus-visible not described. | Inherited focus styles could compensate, but `outline:none` is a decisive risk until replaced. | Restore `:focus-visible` ring using existing tokens; ensure 44px-ish tablet hit area or project-approved equivalent; add `aria-label`/text labels; define row, selection, bulk-action, drawer tab order. Acceptance: keyboard-only user can filter, select rows, open/edit/save/close drawer with visible focus. |
| F6 | P1 | 10,000-row rendering and synchronous filtering are hot-path risks. | `rows.map(...)` renders all rows; notes: all 10,000 rows render; filtering recalculates synchronously on every keystroke. | Actual latency/FPS is unmeasured; static source proves unbounded work, not exact user-perceived lag. | Virtualize table/window rows; memoize filtered results; defer or debounce filter input; keep selection state independent of rendered window; avoid recreating row props unnecessarily. Acceptance: defined keystroke and scroll budgets pass on target desktop/tablet hardware. |
| F7 | P1 | Layout is brittle on tablet and constrained desktop widths. | `.page { min-width:1180px; }`; fixed grid columns; `.drawer { width:520px; height:100vh; }`; tablet behavior not described. | Exact tablet viewport targets unknown. | Keep table horizontally scrollable inside data region, not whole page; keep filters and critical actions reachable; bound drawer with `width:min(520px,100vw)` or approved full-screen tablet drawer; reserve safe-area/viewport height handling. Acceptance: tablet can filter, inspect, edit, save without hidden critical actions. |
| F8 | P2 | Hostile data can damage scannability and correctness. | Names 1–200 chars; translations +60%; missing prices; absent/8MB images; `.product-name` truncates only one field. | Actual column renderers unknown. | Define per-field fallbacks: missing price as explicit “Not set”/em dash with edit affordance; long names truncate with accessible full value; labels wrap or use responsive copy; absent images use stable placeholder; reject/compress oversized uploads with progress/error. |
| F9 | P2 | Image loading may cause layout shift and memory/network pressure. | Image dimensions not reserved; some images absent or 8MB. | Actual image components and CDN behavior unknown. | Reserve width/height/aspect ratio; lazy-load offscreen images; generate thumbnails; enforce upload size/type validation; show per-image upload progress and failure. Acceptance: no visible row jump when images load; 8MB upload has clear progress/failure path. |
| F10 | P2 | Motion choices are broad and potentially uncomfortable/performance-hostile. | `.product-row, .drawer { transition: all 300ms ease-in; }`; reduced motion not described. | Actual animated properties and frame behavior need runtime inspection. | Replace `transition: all` with named properties, mostly transform/opacity; use faster, interruptible drawer motion; disable or simplify under reduced motion while preserving state feedback. |
| F11 | P2 | Single `saving` boolean is too coarse for complex operations. | `const [saving,setSaving]`; passed to one `EditDrawer`. | Source does not prove concurrent saves or bulk operations share this flag. | Track save state by product/request ID; distinguish idle/dirty/saving/saved/error/conflict; prevent stale completion from overwriting newer edits. |
| F12 | P3 | Blank loading body and missing disabled states reduce trust. | Notes: blank body during initial/filter loading; disabled/permission affordances not described. | Visual severity depends on surrounding chrome. | Use compact skeleton or progress row; disable unavailable actions with reason; keep existing density and table grammar. |

---

## 3. Concrete hardening/polish moves by area

- **Hostile data:** add field-level display contracts for long names, missing prices, long translations, absent images, oversized uploads, and upload failures; preserve full values through accessible labels/tooltips or detail cells.
- **Failures/recovery:** model request state explicitly: loading, empty, unauthorized, forbidden, conflict, rate-limited, server error, timeout, offline, partial success, dirty, saving, saved, failed; each state needs message, action, and preserved context.
- **Responsive layout:** remove page-level forced overflow as the only strategy; confine horizontal overflow to the table; keep filters/bulk actions/drawer controls reachable; cap drawer width to viewport or switch to an approved tablet full-screen drawer.
- **Accessibility:** restore visible focus, label icon-only controls, define keyboard row navigation/selection, trap or intentionally manage drawer focus, restore focus on close, block background interaction if modal, and announce save/error state changes.
- **State recovery:** never clear local edits or dirty state on failed save; handle 409 with compare/reload/apply choice; protect pending saves from Escape/close; support retry without resetting filters, selection, or drawer content.
- **Performance:** virtualize 10,000 rows, memoize/defer filtering, reserve image dimensions, thumbnail/lazy-load images, isolate row re-renders, and measure before/after rather than relying on static smell alone.

---

## 4. Static detector-like signal reconciliation

**Decisive from supplied source/scope:**
- `catch {}` with no error branch proves save errors are swallowed in this snippet.
- Explicit notes prove missing listed states in the supplied surface description.
- `rows.map` plus 10,000-row note proves unbounded initial row rendering.
- Fixed `min-width:1180px`, fixed columns, and fixed 520px drawer prove responsive constraints exist.
- `outline:none` proves native outline is removed on `.icon-button`.
- Explicit notes prove no drawer focus trap/background blocking and icon-only save/close.

**Needs project/runtime context before final severity or implementation choice:**
- Exact perceived slowness, FPS, input delay, layout shift, and memory impact.
- Whether inherited CSS restores focus visibility despite `outline:none`.
- Whether the drawer is intended modal, modeless inspector, or hybrid.
- Whether optimistic updates mutate `rows` before save confirmation.
- Whether global `saving` conflicts with concurrent saves or bulk operations.
- Exact tablet breakpoints, supported browsers, API retry semantics, image CDN behavior, and permission model.

---

## 5. Measurement-first validation plan with rollback/acceptance

1. **Baseline first, before optimization claims**
   - Measure initial render, filter keystroke latency, scroll responsiveness, drawer open/close responsiveness, image load shift, and save-state transitions on target desktop and tablet-class hardware.
   - Record row count, image mix, network profiles, and browser versions.

2. **Failure-state validation**
   - Inject or mock 401/403/409/429/500/timeout/offline/partial batch responses.
   - Acceptance: every state renders cause + next action; filters/selection/drawer edits survive where appropriate; failed save never appears successful.

3. **Accessibility validation**
   - Keyboard-only pass for filters, table rows, selection, bulk actions, drawer open/save/close.
   - Screen-reader/name pass for icon buttons, drawer title, save status, errors.
   - Acceptance: visible focus at all times, no background focus leak for modal drawer, Escape cannot destroy pending/dirty work.

4. **Responsive validation**
   - Test supported desktop widths and tablet widths/orientations.
   - Acceptance: table may scroll within its region, but primary actions, filters, drawer controls, and status remain reachable.

5. **Performance validation**
   - Compare baseline vs virtualized/deferred implementation.
   - Acceptance targets should be set by the product team, but release should require no obvious typing stalls while filtering, smooth practical scrolling through 10,000 rows, bounded row renders, and no major image-induced layout jumps.

6. **Rollback conditions**
   - Roll back if virtualization breaks selection, row identity, keyboard navigation, screen-reader order, bulk operations, or edit-drawer context.
   - Roll back if new save guards block legitimate recovery, hide API errors, or make offline/conflict resolution worse.
   - Roll back if responsive changes hide columns/actions without an accessible way to reach them.

7. **Release acceptance**
   - Ship only when P0 issues are closed, P1 issues have verified behavior or explicit product sign-off, performance measurements meet agreed budgets, and all newly added states preserve the existing workflow and design system.


## Output C

## 1) Correct sequencing + verdict

**Sequencing:** audit static risks → harden correctness/failure/state recovery → fix accessibility and keyboard safety → optimize measured hot paths → polish responsive layout, motion, and visual states without changing the workflow.

**Verdict:** Static evidence shows this inventory editor is not production-hardened yet: silent save failure, missing recovery states, unsafe drawer behavior, unbounded 10,000-row rendering, and incomplete accessibility should block release before visual polish.

---

## 2) Prioritized findings

### P0 — Data-loss and false-success risk in saving
- **Source evidence:** `catch {}` swallows `api.save(product)` failures; `saving` is reset with no error state, retry path, conflict handling, or user-visible failure.
- **Source evidence:** Escape closes the drawer even while save is pending.
- **Source evidence:** 409 conflict, timeout, offline, retry, and partial batch failure states are not represented.
- **Runtime hypothesis:** Users may believe edits are saved when they are not; pending edits may be lost if the drawer closes during save or network failure.

**Fix:** Replace silent catch with explicit save result states: `idle | dirty | saving | saved | failed | conflict | offline`. Use `finally` for cleanup, surface errors inline and in autosave status, block or confirm close while dirty/saving, and preserve the draft until server acknowledgement.

---

### P0 — Missing production failure and permission states
- **Source evidence:** Empty results, 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are absent.
- **Source evidence:** Permission-specific affordances are not described.
- **Runtime hypothesis:** Operators may see blank content or disabled workflows without knowing whether data is loading, unavailable, unauthorized, filtered out, rate-limited, or partially saved.

**Fix:** Add explicit state surfaces while preserving the existing page structure:
- loading: table skeleton or calm loading rows, not blank body;
- empty: “No products match these filters” with clear filter reset;
- 401/403: auth/permission message with allowed next action;
- 409: conflict resolver showing local vs server value;
- 429/timeout/offline: retry with backoff and offline persistence;
- 500: retryable server failure message;
- partial batch failure: per-row failure summary and retry failed only.

---

### P1 — Drawer is not a safe modal/editing surface
- **Source evidence:** Drawer traps neither focus nor background interaction.
- **Source evidence:** Escape closes it even during pending save.
- **Source evidence:** Save and close are icon-only.
- **Runtime hypothesis:** Keyboard and screen-reader users can lose context, interact behind the drawer, or trigger destructive close behavior accidentally.

**Fix:** Treat the drawer as a controlled editing region:
- `role="dialog"` or equivalent semantic pattern with labelled title;
- focus moves into drawer on open and returns to the invoking row on close;
- trap focus while open and make background inert/unreachable;
- Escape closes only when clean, or opens a discard/pending-save confirmation;
- save/close buttons get visible text or robust accessible names;
- pending save disables destructive close or requires confirmation.

---

### P1 — 10,000-row rendering and synchronous filtering are hot-path risks
- **Source evidence:** `{rows.map(...)}` renders all rows at once.
- **Source evidence:** Source notes say filtering recalculates synchronously on every keystroke.
- **Source evidence:** Image dimensions are not reserved.
- **Runtime hypothesis:** Initial render, filter typing, selection updates, image loading, and scrolling may produce long tasks, input delay, memory pressure, and layout shift.

**Fix:** Keep the workflow but change the implementation:
- render a windowed/virtualized table body or equivalent internal windowing;
- memoize row rendering and derived filtered rows;
- debounce or defer filter work while keeping input responsive;
- avoid global `saving` re-rendering every row if save is drawer/row-specific;
- reserve thumbnail dimensions and lazy-load non-critical images;
- keep selection state stable by product id, not visible index.

---

### P1 — Accessibility gaps are source-visible
- **Source evidence:** `.icon-button { outline: none; }`.
- **Source evidence:** Save and close are icon-only.
- **Source evidence:** Keyboard navigation, screen-reader labels, focus-visible, and reduced motion are not described.
- **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`.
- **Runtime hypothesis:** Focus may become invisible, controls may be unnamed, motion may be excessive, and table/drawer navigation may be unreliable.

**Fix:** Restore accessible interaction:
- use `:focus-visible` styling aligned to the design system;
- add accessible names to icon buttons;
- provide keyboard row selection, bulk selection, and drawer controls;
- expose autosave and errors through a polite/assertive live region as appropriate;
- respect `prefers-reduced-motion`;
- transition only safe properties such as `transform` and `opacity`, not `all`.

---

### P2 — Responsive/tablet layout is under-specified and brittle
- **Source evidence:** `.page { min-width: 1180px; }`.
- **Source evidence:** drawer is fixed `width: 520px; height: 100vh; right: 0`.
- **Source evidence:** tablet behavior is not described.
- **Runtime hypothesis:** Tablet users may get clipped content, unreachable controls, body scroll conflicts, or a drawer that consumes too much of the viewport.

**Fix:** Preserve desktop-first layout but add adaptive constraints:
- make the table region horizontally scrollable instead of forcing the entire page;
- use `width: min(520px, calc(100vw - safe margins))` for the drawer;
- handle tablet breakpoints with reduced columns, sticky key columns, or detail expansion;
- lock background scroll while drawer is open;
- account for safe areas and dynamic viewport height where relevant.

---

### P2 — Hostile product data will break polish and comprehension
- **Source evidence:** product names can be 1–200 characters.
- **Source evidence:** prices may be missing.
- **Source evidence:** translations may expand labels by 60%.
- **Source evidence:** images may be absent or 8MB.
- **Source evidence:** product names are truncated with ellipsis.
- **Runtime hypothesis:** Operators may lose identifying information, see ambiguous blanks, suffer layout shift, or wait on oversized media.

**Fix:** Harden data rendering:
- preserve full product name in accessible text and a deliberate reveal pattern;
- render missing prices as explicit “No price” / “Not set”, not blank;
- allow labels/buttons to grow or wrap where safe;
- reserve image boxes and provide absent-image placeholders;
- validate upload size/type before upload, show progress, and support retry/cancel;
- compress or resize large images server-side or in the existing upload pipeline if available.

---

### P3 — Motion and visual polish should come after hardening
- **Source evidence:** `transition: all 300ms ease-in` on rows and drawer.
- **Runtime hypothesis:** Broad transitions can animate layout/color/size unexpectedly, create sluggish interaction, and conflict with reduced-motion needs.

**Fix:** Replace with intentional motion:
- drawer: transform-based open/close transition;
- row updates: subtle background/color transition only where meaningful;
- reduced motion: instant state change with non-motion feedback;
- no transition on layout-heavy table properties.

---

## 3) Concrete production fixes by area

### Hostile data
- Add display contracts for long names, missing prices, absent images, oversized images, and expanded translations.
- Reserve image dimensions in every row.
- Use explicit placeholders instead of blanks.
- Keep full identifiers available to assistive tech and keyboard users.
- Validate upload type/size early and show upload progress/error/retry.

### Failures
- Stop swallowing errors.
- Use typed API outcomes for success, validation failure, auth failure, conflict, rate limit, timeout, offline, and server failure.
- Add retry paths with idempotency/version protection.
- Add per-row and batch-level partial failure summaries.
- Keep failed drafts recoverable until explicitly discarded.

### Responsive layout
- Keep the existing table workflow but constrain overflow to the table area.
- Make the drawer viewport-aware.
- Define tablet behavior for filters, columns, bulk actions, and drawer open state.
- Avoid page-level horizontal scrolling where possible.

### Accessibility
- Restore visible focus.
- Label icon-only controls.
- Add drawer focus trap, background inertness, initial focus, and focus return.
- Protect pending saves from Escape/discard.
- Add keyboard affordances for row navigation, selection, bulk actions, and save.
- Respect reduced motion.
- Announce autosave/failure states.

### State recovery
- Track dirty state separately from saving state.
- Persist local draft while save is pending or failed.
- Restore filters, selection, drawer target, and unsaved draft after refresh when safe.
- Resolve conflicts using server versioning or ETags.
- Prevent stale saves from overwriting newer edits.

### Performance
- Window the 10,000-row table.
- Memoize filtered rows and row components.
- Defer/debounce filtering work.
- Avoid global state changes that re-render all rows.
- Reserve image layout and lazy-load thumbnails.
- Limit transitions to compositor-friendly properties.

---

## 4) Static signals: decisive vs needing runtime context

### Decisive from the provided source/static facts
- Empty `catch {}` means save failures are hidden.
- No represented error states means failure UX is incomplete.
- `rows.map` over all rows means the implementation attempts full render.
- Synchronous filtering on every keystroke is a hot-path risk.
- `outline: none` without described replacement is an accessibility failure risk.
- Icon-only save/close without labels is unsafe.
- Drawer without focus trap/background isolation is not accessible modal behavior.
- `transition: all` is unsafe for a large table and drawer.
- Fixed `min-width: 1180px` and fixed `520px` drawer need tablet handling.

### Needs project/runtime context before final severity or exact fix
- Exact render time, memory use, input delay, and scroll performance.
- Whether `ProductRow` internally memoizes, labels controls, or reserves media.
- Existing design-system tokens for focus, error, loading, and motion.
- Whether the API client already supports retries, aborts, idempotency, or auth handling.
- Actual permission model and which actions should be hidden, disabled, or explained.
- Real tablet breakpoints and supported device sizes.
- Actual screen-reader output and keyboard order.
- Real image CDN/upload behavior and whether thumbnails are pre-generated.

---

## 5) Measurement-first validation plan with rollback/acceptance

### Baseline before changes
- Measure initial render with 10,000 rows.
- Measure filter keystroke latency and long tasks.
- Measure drawer open/close interaction latency.
- Measure scroll smoothness and memory use.
- Measure image layout shift with absent and large images.
- Exercise mocked responses for 401, 403, 409, 429, 500, timeout, offline, and partial batch failure.

### Validation after hardening
- Save failure is visible and recoverable.
- Pending save cannot be silently discarded.
- Dirty draft survives failed save and intentional close rules are clear.
- Conflict state prevents stale overwrite.
- Partial batch save reports failed rows and allows retry failed only.

### Accessibility validation
- Keyboard can reach filters, table rows, bulk actions, drawer fields, save, and close.
- Focus is visible.
- Drawer traps focus and restores it on close.
- Background is not interactive while drawer is open.
- Icon buttons have accessible names.
- Autosave and failure states are announced appropriately.
- Reduced-motion mode removes nonessential animation while preserving state feedback.

### Performance acceptance targets
- Only visible rows plus modest overscan render during normal table use.
- Filter typing remains responsive at 10,000 rows.
- No avoidable large layout shifts from images.
- Row selection and drawer save do not re-render the full table unnecessarily.
- Motion does not animate layout-heavy properties.

### Responsive acceptance
- Desktop workflow remains intact.
- Tablet viewport does not lose critical actions.
- Drawer remains usable without covering all context unless intentionally full-screen.
- Table overflow is contained and predictable.

### Rollback conditions
- Roll back windowing/filter changes if selection, bulk actions, or row identity become inconsistent.
- Roll back save-state changes if they block legitimate saves or discard confirmed user intent incorrectly.
- Roll back drawer changes if focus becomes trapped with no escape path.
- Roll back responsive changes if desktop operator density or existing workflows regress.

### Release condition
Ship only when correctness and recovery are safe, keyboard/accessibility paths are verified, 10,000-row interactions meet agreed latency targets, and all listed failure states have deliberate user-facing outcomes.
