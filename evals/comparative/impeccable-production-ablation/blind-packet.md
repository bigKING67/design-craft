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

## 1. Correct sequence + verdict

**Sequence:** read-only audit → data/state hardening → accessibility + responsive hardening → measurement-led performance optimization → restrained visual polish → validation + rollback gates.

**Verdict:** This is not a redesign problem; it is a production hardening issue with P0 data-recovery risk and P1 accessibility, tablet, and 10,000-row performance risks that should be fixed before polish.

## 2. Prioritized findings ledger

| ID | Pri | Source evidence | Runtime hypothesis / unknown | Concrete repair | Acceptance evidence needed |
|---|---:|---|---|---|---|
| F1 | P0 | `catch {}` swallows save failures; global `saving`; missing 409/offline/retry/partial failure states; Escape closes drawer during pending save. | API may have server-side safeguards, but UI currently gives no reliable recovery path. | Replace boolean with explicit save state per product/drawer/batch: `idle/dirty/saving/saved/error/conflict/offline/retrying`. Preserve dirty draft, block or confirm close during pending/dirty state, show conflict resolution, retry, and partial-batch result summaries. | Failed save is visible; user can retry or discard intentionally; conflict cannot silently overwrite; pending save cannot be lost by Escape/close. |
| F2 | P1 | `{rows.map(...)}` renders all rows; notes say 10,000 rows and synchronous filtering on every keystroke. | Static source proves unbounded work, but actual latency/INP/memory requires measurement. | Bound table work using existing project pattern: virtualization, pagination, or server/windowed querying. Defer/debounce filter input appropriately, memoize derived rows, keep row props stable, preserve selection across windows/pages. | 10,000-row route stays within ratified input, long-task, memory, and mounted-row budgets. |
| F3 | P1 | Drawer lacks focus trap/background isolation; Save/Close are icon-only; `.icon-button` is 28×28 and `outline: none`; keyboard/screen-reader/focus-visible not described. | Components may add labels elsewhere, but supplied facts do not prove accessible operation. | Treat drawer as modal or non-modal explicitly. If modal: dialog semantics, labelled title, focus trap, focus restore, inert/background block. Add accessible names to icon buttons, visible `:focus-visible`, disabled/loading labels, and effective tablet target size near 44px. | Keyboard-only user can open, edit, save, close, and recover focus; labels are announced; focus is visible; background cannot be accidentally edited. |
| F4 | P1 | `.page { min-width:1180px }`; fixed grid columns; drawer fixed `520px`; tablet support required; translations expand labels by 60%. | A horizontal data-table region may be acceptable if intentional, but fixed page/drawer can make actions unreachable on tablets. | Keep desktop-first table density, but isolate overflow to the table, not the whole page. Use `minmax()`/responsive column rules, sticky critical columns/actions, drawer width `min()/clamp()`, and translation-safe labels. | Tablet viewport retains filters, bulk actions, drawer controls, and save status without page-level clipping. |
| F5 | P1 | Initial/filter loading render blank table body; empty, 401/403, 409, 429, 500, timeout, offline, retry, partial batch failure states absent. | Actual API/error taxonomy may differ, but the UI state contract is incomplete. | Add owned loading skeleton/rows, empty result copy, permission-specific affordances, rate-limit backoff, timeout/offline banners, retry actions, conflict state, and partial-batch success/failure report. | Each listed state renders specific context, user action, and recovery path without losing current filters/selection/draft. |
| F6 | P2 | Product names 1–200 chars; prices may be missing; images absent or 8MB; image dimensions not reserved. | Real data distribution and CDN behavior unknown. | Use resilient cells: truncation with accessible full-name disclosure, missing-price placeholder/status, absent-image fallback, reserved image aspect ratio, size limits, upload validation/compression/progress/error states. | No layout jump from images; long names do not break actions; missing fields remain understandable. |
| F7 | P2 | Bulk selection and permission-specific affordances are route requirements but not represented in the snippet/notes. | Selection implementation may live inside child components. | Ensure selection model is stable across filtering/windowing, with “selected visible/all matching” clarity, permission-aware disabled states, and partial-batch reconciliation. | Bulk actions never apply to an ambiguous set; denied actions explain why and preserve selection safely. |
| F8 | P3 | `.product-row, .drawer { transition: all 300ms ease-in; }`; reduced motion not described. | Actual animated properties unknown. | Narrow transitions to intentional properties, preferably `transform/opacity`; remove row-wide transition unless needed; add reduced-motion behavior; align status/motion copy with existing design tokens. | No broad `transition: all`; motion is purposeful, interruptible, and reduced-motion compatible. |

## 3. Fix coverage by concern

- **Hostile data:** covered by F4/F6/F7 — long names, expanded translations, missing prices, absent/large images, and selection across filtered/windowed data.
- **Failures:** covered by F1/F5 — visible save errors, auth/permission, conflict, rate limit, server error, timeout, offline, retry, and partial-batch states.
- **Responsive layout:** covered by F4 — preserve desktop table density while preventing page-level overflow and unreachable drawer controls on tablets.
- **Accessibility:** covered by F3/F8 — focus management, labelled controls, visible focus, target size, keyboard flow, screen-reader semantics, and reduced motion.
- **State recovery:** covered by F1/F5/F7 — dirty draft preservation, close/escape safeguards, conflict handling, retry, partial success, and stable selection.
- **Performance:** covered by F2/F6/F8 — bounded row rendering/filtering, reserved image dimensions, safer animation properties, and measurement before claiming improvement.

## 4. Static signal reconciliation

**Decisive from supplied source/facts:**

- Rendering `rows.map` for a stated 10,000-row table is unbounded DOM work.
- Synchronous filter recalculation on every keystroke is an input hot-path risk.
- `catch {}` proves save failures can be swallowed at this layer.
- Missing represented states are decisive because the notes explicitly list them as absent.
- Fixed `min-width`, fixed grid columns, and fixed drawer width are real layout constraints.
- `outline: none`, 28px icon buttons, icon-only controls, and no described labels/focus trap are accessibility risks requiring repair or contrary evidence.
- `transition: all` is a real maintainability/performance/motion smell.
- Missing image dimensions create a credible layout-shift risk.

**Needs project/runtime context before final severity or exact implementation:**

- Actual filter latency, INP, memory, scroll smoothness, and frame rate.
- Whether existing table primitives already provide virtualization/pagination patterns.
- Whether child components add accessible names, roles, or keyboard behavior not shown here.
- Whether fixed table width is an accepted design-system pattern with isolated horizontal scroll.
- Whether API contracts provide idempotency, optimistic concurrency, draft persistence, or conflict protection.
- Actual tablet breakpoints, supported browsers, device class, and operational network conditions.
- Final visual quality, contrast, and density; static CSS alone cannot prove the rendered experience.

## 5. Measurement-first validation plan

1. **Baseline before changes**
   - Use representative 10,000-row data with 1, 20, 60, and 200-character names, missing prices, absent images, and large upload candidates.
   - Capture current budgets for initial render, filter keystroke latency, long tasks, DOM node count, JS heap, layout shift, drawer open/close, and save-state transitions.
   - Provisional gates to ratify: filter input p95 ≤100ms desktop / ≤150ms tablet; no long task over 50ms during common input; mounted rows bounded to visible window plus overscan; CLS ≤0.1; no base-to-head memory regression over 20% without justification.

2. **State and recovery validation**
   - Exercise save success, 401/403, 409, 429, 500, timeout, offline, retry, partial-batch failure, pending-save close/Escape, and reload after dirty draft.
   - Acceptance: every state has user-facing copy, next action, preserved context, and no silent data loss.

3. **Accessibility validation**
   - Keyboard-only path through filters, table selection, edit drawer, upload, save, close, and error recovery.
   - Check accessible names for icon buttons, focus trap/restore, background interaction blocking, visible focus, disabled/loading semantics, and reduced-motion behavior.
   - Acceptance: no keyboard trap except intentional modal containment; no unlabeled critical action; focus remains visible.

4. **Responsive validation**
   - Desktop and tablet breakpoints with expanded translations and long product names.
   - Acceptance: filters, table actions, bulk controls, drawer controls, and autosave status remain reachable; unavoidable overflow is isolated to the data table.

5. **Performance validation after fixes**
   - Re-measure the same scenarios against baseline.
   - Acceptance: bounded row rendering/filtering is proven at 10,000 rows; image dimensions prevent layout jumps; drawer motion does not create measurable interaction regression.

6. **Rollback conditions**
   - Roll back or gate the change if save/conflict handling regresses, bulk selection becomes ambiguous, keyboard access is blocked, tablet critical actions become unreachable, or performance misses ratified budgets.
   - Prefer a feature flag or incremental rollout for table virtualization/windowing and revised save-state behavior, because both touch core operational workflows.


## Output B

## 1) Sequencing + verdict

**Correct sequence:** static audit → production hardening → performance optimization → tablet/responsive adaptation → accessibility completion → final polish.  
**One-line verdict:** This should not ship as-is for a 10,000-row operations editor; the main risks are silent save failure/data loss, unusable large-list performance, inaccessible drawer controls, missing recovery states, and desktop-only layout assumptions.

## 2) Prioritized findings: P0-P3

### P0 — Blocking / data integrity / task completion

**P0.1 Silent save failure and false confidence**
- **Source evidence:** `catch {}` swallows save errors; `saving` only tracks a global boolean; additional notes say 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.
- **Impact:** Operators can believe edits were saved when they failed. Conflicts may overwrite newer inventory data. Batch operations can partially fail with no actionable recovery.
- **Runtime hypothesis:** Frequency and severity depend on API behavior, autosave cadence, and conflict model, but the static save path is already insufficient.

**P0.2 Unsafe drawer close during pending save**
- **Source evidence:** “Escape closes it even while a save is pending”; drawer does not trap focus or background interaction.
- **Impact:** Pending edits can be abandoned mid-save, duplicated, or left in ambiguous state. Background changes can occur while the edit context is open.
- **Runtime hypothesis:** Actual data loss depends on whether drawer close cancels, races, or merely hides the pending request.

**P0.3 10,000-row rendering and synchronous filtering**
- **Source evidence:** `rows.map(...)` renders every row; notes say all 10,000 rows render at once and filtering recalculates synchronously on every keystroke.
- **Impact:** Typing filters, selecting rows, opening drawer, and scrolling can become unusable on real operations hardware.
- **Runtime hypothesis:** Exact latency requires measurement, but rendering 10,000 interactive rows at once is a decisive static hot-path risk.

---

### P1 — Major release blockers

**P1.1 Missing critical failure and recovery states**
- **Source evidence:** Blank table body during loading; empty results, 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states absent.
- **Impact:** Users cannot distinguish loading from no data, no permission, broken service, stale conflict, or temporary rate limiting.
- **Fix priority:** Before any visual polish.

**P1.2 Drawer accessibility and modal behavior are incomplete**
- **Source evidence:** Drawer traps neither focus nor background interaction; save/close are icon-only; `.icon-button` removes outline.
- **Impact:** Keyboard and screen-reader users can lose context, activate background controls, or be unable to identify destructive/critical actions.
- **Relevant static signal:** `outline: none` without replacement focus styling is decisive.

**P1.3 Tablet support conflicts with fixed desktop layout**
- **Source evidence:** `.page { min-width: 1180px; }`; fixed product grid columns; drawer fixed at `520px`.
- **Impact:** Tablet users likely get horizontal scrolling, clipped drawer content, or impossible touch targets.
- **Runtime hypothesis:** Exact breakpoints need device/viewport checks, but the fixed minimum width contradicts stated tablet support.

**P1.4 Touch target and keyboard focus regression**
- **Source evidence:** `.icon-button { width: 28px; height: 28px; outline: none; }`.
- **Impact:** Fails practical touch usability and removes visible keyboard focus unless replaced elsewhere.
- **Runtime hypothesis:** Existing shared button component might add labels/focus through composition, but the provided CSS is a strong negative signal.

**P1.5 Bulk selection lacks visible partial-failure model**
- **Source evidence:** Route includes bulk selection; notes say partial batch failure states are not represented.
- **Impact:** Operators cannot tell which products changed, which failed, or how to retry safely.

---

### P2 — Important hardening / quality gaps

**P2.1 Hostile product data not safely represented**
- **Source evidence:** Names may be 1-200 characters; prices may be missing; translations may expand labels by 60%; `.product-name` truncates.
- **Impact:** Key product identity, price state, and translated controls can become ambiguous or clipped.
- **Fix:** Preserve row density but add accessible full names, stable missing-price display, flexible labels, and tested truncation rules.

**P2.2 Image loading can cause jank and broken rows**
- **Source evidence:** Some images absent or 8MB; dimensions not reserved.
- **Impact:** Layout shift, slow row paint, memory pressure, and confusing missing-image cells.
- **Fix:** Reserve image boxes, use placeholders, lazy/deferred loading, decode hints, max upload validation, compression/resizing where appropriate.

**P2.3 Motion is too broad and may animate expensive properties**
- **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`.
- **Impact:** Animating `all` can include layout-affecting properties and makes reduced-motion behavior undefined.
- **Fix:** Limit to `transform`/`opacity` where needed; add reduced-motion alternative.

**P2.4 Global `saving` is too coarse**
- **Source evidence:** Single `saving` state at page level.
- **Impact:** One row or drawer save can block/misrepresent another operation; concurrent saves can race and set `saving` false early.
- **Fix:** Track pending operations by product id / batch id and use request tokens or pending counters.

**P2.5 Permission-specific affordances are unspecified**
- **Source evidence:** Permission-specific affordances not described; 401/403 states absent.
- **Impact:** Users may see actions they cannot perform or lack explanation for disabled controls.
- **Fix:** Render permission-aware disabled states, explanatory text, and no-access recovery paths.

---

### P3 — Polish after hardening

**P3.1 Loading/empty copy and autosave messaging need precision**
- **Source evidence:** Blank table body; autosave status exists but state range is not described.
- **Impact:** Operational confidence suffers even if functionality works.
- **Fix:** Use concise statuses: “Saving…”, “Saved 10:42”, “Save failed — retry”, “Offline — changes queued”, “Conflict — review required”.

**P3.2 Density and visual rhythm should be tuned after virtualization**
- **Source evidence:** Fixed grid columns and row transitions imply a dense table.
- **Impact:** Fine-tuning before performance work may be wasted.
- **Fix:** Polish row alignment, truncation affordances, hover/focus/selected states only after the large-list path is stable.

## 3) Concrete fixes

### Hostile data
- Use explicit display states for missing price: “No price”, “Not set”, or a domain-approved placeholder; do not render blank money cells.
- Keep truncated names visually compact but expose the full name via accessible text and an intentional overflow affordance.
- Test 1, 100, and 200-character names; mixed scripts; translated labels at +60%.
- Ensure price, SKU, stock, and status columns do not collapse when labels expand.
- Use absent-image placeholders with reserved dimensions.
- Reject, compress, or background-process very large uploads; show file size/type errors before upload starts.

### Failure states
- Replace `catch {}` with explicit error handling and a durable save state model.
- Use `try/catch/finally`; never let success UI depend on a swallowed exception.
- Represent at least: loading, empty, unauthorized, forbidden, conflict, rate-limited, server error, timeout, offline, retrying, saved, failed, partial batch failed.
- For 409 conflicts, show “server version vs your draft” recovery, not a generic toast.
- For 429, back off and show when retry will occur.
- For partial batch failure, show counts and failed rows with retry/export options.

### Responsive layout
- Replace hard `min-width: 1180px` with a responsive shell that supports tablet widths.
- Keep the desktop table dense, but provide tablet-safe column priority: freeze key identity/actions, hide secondary metadata behind expansion, or use horizontal table scrolling inside a contained region rather than the whole page.
- Make drawer width `min(520px, calc(100vw - safe margins))`; ensure internal scrolling and sticky actions.
- Test text zoom and translated labels without assuming fixed column widths.

### Accessibility
- Drawer should behave as a modal or non-modal panel intentionally:
  - If modal: `role="dialog"`, `aria-modal`, labelled title, focus trap, focus restore, background inert.
  - If non-modal: clear keyboard path and no hidden background interaction surprises.
- Save and close buttons need accessible names, visible text or tooltips where appropriate, and disabled/pending semantics.
- Do not close on Escape while save is pending unless there is a confirmation/recovery path.
- Restore focus to the invoking row/control after drawer close.
- Replace `outline: none` with a visible `:focus-visible` style.
- Increase icon button hit area to at least practical touch size while preserving visual density.
- Add keyboard navigation rules for table rows, selection, bulk actions, drawer open/close, and upload controls.
- Add reduced-motion handling for drawer and row transitions.

### State recovery
- Use per-product draft state and per-request identifiers to avoid stale responses overwriting newer edits.
- Preserve unsaved drawer edits across transient close/reopen or require confirmation before discard.
- Queue or mark offline edits if autosave is promised; otherwise clearly state unsaved/offline.
- Add idempotency or dedupe strategy for repeated save attempts.
- For bulk edits, maintain a result ledger: selected count, attempted count, succeeded, failed, skipped, retryable.

### Performance
- Do not render all 10,000 rows. Use existing table/list primitives if available; otherwise implement windowing or pagination without changing the product workflow.
- Keep DOM rows to visible rows plus overscan, not full dataset.
- Memoize filtered/sorted results with correct dependencies.
- Defer filter work using debouncing, deferred values, or transitions so typing stays responsive.
- Avoid recreating row callbacks/objects unnecessarily; memoize row components where stable.
- Store selection as an id set/map rather than mutating all row objects on every toggle.
- Reserve image dimensions and lazy-load row images.
- Replace `transition: all` with targeted properties.
- Consider CSS containment for row regions if compatible with sticky headers/columns.

## 4) Static signals: decisive vs context-dependent

### Decisive from the provided source
- `rows.map` over 10,000 rows is a real large-list rendering risk.
- Synchronous filter recalculation on every keystroke is a hot-path risk.
- `catch {}` is insufficient for production save reliability.
- Missing 401/403/409/429/500/offline/timeout/retry/partial-failure states is a hardening gap.
- `min-width: 1180px` conflicts with tablet support.
- `width: 28px; height: 28px` is too small for touch-first affordances.
- `outline: none` is unsafe without a replacement focus-visible style.
- `transition: all` is an avoidable performance and motion-accessibility risk.
- No drawer focus trap/background control is a major interaction/a11y gap.

### Requires project/runtime context
- Actual contrast compliance depends on tokens/colors not shown.
- Whether `ProductRow` uses semantic table/grid roles is not shown.
- Whether shared icon button components add labels/focus styles elsewhere is not shown.
- Actual latency, memory, and input delay require measurement on representative data.
- Exact tablet breakage depends on viewport widths, surrounding shell, and overflow strategy.
- Save race severity depends on API idempotency, autosave frequency, and request cancellation behavior.
- Image impact depends on CDN transforms, browser cache, decoding strategy, and actual dimensions.
- Permission affordance requirements depend on role model and operation policy.

## 5) Measurement-first validation plan with rollback/acceptance

### Baseline before changes
- Capture representative 10,000-row dataset with long names, missing prices, absent images, 8MB image cases, translated labels, and mixed permissions.
- Measure initial render, filter typing latency, scroll smoothness, drawer open/close latency, memory, and layout shift.
- Record current save/error behavior for conflict, offline, timeout, 429, 500, and partial batch failure using controlled test responses.

### Validation after hardening
- Unit-test save state transitions: success, failure, timeout, offline, retry, conflict, stale response, concurrent saves.
- Integration-test drawer close/escape behavior while clean, dirty, saving, failed, and conflicted.
- Verify bulk result ledger for all-success, all-fail, and partial-fail cases.
- Validate uploads for absent image, invalid type, too-large file, slow upload, retry, and canceled upload.

### Validation after performance work
- Confirm rendered row count is bounded to visible rows plus overscan or a documented page size.
- Acceptance target: filter input remains responsive on 10,000 rows; no full-table re-render on every keystroke or selection toggle.
- Acceptance target: drawer interaction remains responsive while table data is present.
- Acceptance target: image loading does not create meaningful layout shift.

### Validation after responsive/a11y work
- Check desktop and tablet breakpoints, text zoom, translated labels, and long product names.
- Keyboard-only path must cover filters, rows, selection, drawer fields, save, close, upload, conflict recovery, and retry.
- Focus must enter drawer predictably, stay there when modal, and restore on close.
- Icon actions must have accessible names and visible focus.
- Reduced-motion preference must avoid nonessential drawer/row animation.

### Rollback conditions
- Roll back or flag-gate the change if save success/error rates worsen, conflicts become unrecoverable, keyboard completion breaks, or filter latency regresses materially.
- Roll back virtualization/windowing if selection, row identity, focus restoration, or bulk actions become inconsistent.
- Roll back responsive changes if desktop operations lose required density without a tablet gain.

### Acceptance conditions
- No silent save failures.
- No ambiguous blank table during loading/errors/empty results.
- 10,000-row dataset remains operational for filtering, scrolling, selection, and drawer edits.
- Tablet layout has no page-level horizontal overflow trap.
- Drawer is keyboard-safe and screen-reader-identifiable.
- Critical network and permission failures provide clear recovery.
- Final polish preserves the existing design system and workflow rather than redesigning the surface.


## Output C

## 1. Sequencing and verdict

**Correct sequence:** audit → stabilize correctness/state recovery → harden failure handling and permissions → fix accessibility blockers → optimize table/filter/image performance → tablet/responsive polish → visual polish within the existing system.

**Verdict:** The surface is not production-hardened for a 10,000-row operations workflow; the main risks are silent save failure, inaccessible drawer/actions, unbounded rendering/filter work, missing failure states, and tablet layout breakage.

---

## 2. Prioritized findings

### P0 — Production blockers

1. **Silent save failure and ambiguous autosave state**
   - **Source evidence:** `catch {}` suppresses errors; `setSaving(false)` is outside `finally`; no error state is rendered.
   - **Impact:** Operators can believe edits saved when they failed. Conflict, offline, timeout, permission, and server failures are unrecoverable.
   - **Runtime hypothesis:** Save races may also cause stale “saved” indicators if multiple saves overlap.

2. **Drawer interaction is unsafe during save**
   - **Source evidence:** Escape closes the drawer even while save is pending; drawer does not trap focus or block background interaction.
   - **Impact:** Edits can be lost or hidden mid-save; keyboard and assistive-technology users can escape into background content.

3. **Critical failure states are absent**
   - **Source evidence:** Empty results, 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.
   - **Impact:** Operators cannot distinguish “no products,” “still loading,” “not authorized,” “conflict,” “rate limited,” or “failed batch.”

4. **10,000 rows render at once**
   - **Source evidence:** `{rows.map(...)}` renders every row.
   - **Impact:** High initial render cost, memory pressure, slow bulk selection, slow filter updates, and poor tablet responsiveness.

5. **Filtering recalculates synchronously on every keystroke**
   - **Source evidence:** Additional notes state synchronous recalculation on every keystroke.
   - **Impact:** Input jank is likely at 10,000 rows, especially with translated labels, price formatting, and image-related layout changes.

---

### P1 — High-priority hardening

1. **Loading renders as a blank table body**
   - **Source evidence:** Initial and filter loading render blank table body.
   - **Impact:** Looks broken; users may retry, navigate away, or assume data loss.

2. **Tablet layout likely overflows**
   - **Source evidence:** `.page { min-width: 1180px; }`; drawer width fixed at `520px`.
   - **Impact:** Tablet support is not credible without a managed overflow/adaptive layout strategy.

3. **Keyboard focus visibility is removed**
   - **Source evidence:** `.icon-button { outline: none; }`.
   - **Impact:** Keyboard users cannot reliably see where focus is.

4. **Icon-only save and close actions are unlabeled**
   - **Source evidence:** Save and close are icon-only; labels are not described.
   - **Impact:** Screen-reader users may hear ambiguous or empty controls.

5. **Transitions animate all properties**
   - **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`.
   - **Impact:** Can animate layout-affecting properties, cause jank, and ignore reduced-motion preferences.

6. **Images do not reserve dimensions**
   - **Source evidence:** Image dimensions are not reserved; some images are absent or 8MB.
   - **Impact:** Layout shift, slow rows, expensive decoding, and unstable scroll positions.

---

### P2 — Important polish and resilience

1. **Hostile product data is under-specified**
   - **Source evidence:** Product names may be 1–200 characters; prices may be missing; translations may expand labels by 60%; images may be absent or large.
   - **Impact:** Truncation, broken alignment, ambiguous missing values, clipped translated text, and layout instability.

2. **Global `saving` state is too coarse**
   - **Source evidence:** One `saving` boolean is passed to the drawer.
   - **Impact:** Cannot represent per-field, per-row, batch, retrying, failed, partially saved, or conflict states.

3. **Permission-specific affordances are missing**
   - **Source evidence:** Permission-specific affordances are not described.
   - **Impact:** Users may see actions they cannot complete; 403 becomes a late, avoidable failure.

4. **Bulk failure handling is absent**
   - **Source evidence:** Partial batch failure states are not represented.
   - **Impact:** Operations staff cannot tell which products changed, failed, or require retry.

5. **Long names only visually truncate**
   - **Source evidence:** `.product-name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }`.
   - **Impact:** Full value may be inaccessible unless an explicit reveal/copy/title/detail pattern exists.

---

### P3 — Lower-priority polish

1. **Grid columns are rigid**
   - **Source evidence:** `64px 280px 1fr 120px 96px`.
   - **Impact:** Works for a narrow happy path but may degrade with translation, missing images, or tablet width.

2. **Drawer height uses `100vh`**
   - **Source evidence:** `.drawer { height: 100vh; }`.
   - **Impact:** Can be awkward on devices with dynamic browser chrome; safer sizing may be needed.

3. **No stated reduced-motion behavior**
   - **Source evidence:** Reduced motion is not described.
   - **Impact:** Motion-sensitive users may be forced through drawer and row animations.

---

## 3. Concrete fixes

### Hostile data

- Product names:
  - Preserve single-line table density, but add a reliable full-value access path: details drawer field, tooltip/popover using existing system pattern, or copyable full name.
  - Ensure truncation works for 1–200 characters and translated strings.
- Prices:
  - Represent missing price explicitly, e.g. “Not set” or an approved placeholder, not `0` or blank.
  - Keep sorting/filtering semantics distinct from display formatting.
- Translations:
  - Audit fixed-width labels and icon-only controls for 60% expansion.
  - Prefer `minmax()` and wrapping where the existing layout allows.
- Images:
  - Reserve thumbnail dimensions.
  - Use placeholders for absent images.
  - Validate upload size/type before upload.
  - Show upload progress, failure, retry, and remove/replace states.
  - Avoid decoding full 8MB images in table rows; use generated thumbnails or constrained previews if available.

### Failures

- Add explicit states for:
  - Initial loading.
  - Filter loading.
  - Empty filtered result.
  - Empty inventory.
  - Unauthorized/session expired.
  - Forbidden/read-only permission.
  - Conflict/version mismatch.
  - Rate limited with retry timing if available.
  - Server error.
  - Timeout.
  - Offline.
  - Partial batch success/failure.
- Replace silent `catch {}` with visible error handling.
- Use `try/catch/finally` so saving state always clears.
- Keep failed edits recoverable in the drawer instead of discarding local input.

### Responsive layout

- Remove page-level hard dependency on `min-width: 1180px` as the only tablet behavior.
- Preserve desktop table workflow, but add tablet-safe behavior:
  - Container-level horizontal scroll for dense table if necessary.
  - Sticky key columns/actions only if already supported by the design system.
  - Drawer width using bounded responsive sizing, e.g. max width plus viewport clamp.
  - Ensure filters wrap or collapse according to existing patterns.
- Avoid redesigning into cards unless the product explicitly supports that workflow.

### Accessibility

- Restore visible keyboard focus:
  - Do not use `outline: none` without a replacement `:focus-visible` style.
- Icon-only buttons:
  - Add accessible names for save, close, upload, retry, bulk actions, and row actions.
- Drawer:
  - Trap focus while open.
  - Return focus to the invoking control on close.
  - Mark or inert background content while drawer is active.
  - Prevent background interaction.
  - Do not close on Escape while save is pending unless a confirmation/recovery path exists.
- Keyboard:
  - Define row navigation, selection, bulk action access, drawer open/close behavior, and disabled states.
- Motion:
  - Replace `transition: all` with targeted properties.
  - Respect reduced-motion preferences.

### State recovery

- Track dirty state separately from saving state.
- Represent save lifecycle explicitly: idle, dirty, saving, saved, failed, conflict, retrying.
- For overlapping saves:
  - Ignore stale responses or serialize saves per product.
  - Use request IDs, version numbers, or abortable saves where appropriate.
- For conflicts:
  - Show server-changed fields.
  - Offer reload, overwrite if permitted, or merge where supported.
- For batch operations:
  - Keep a per-row result map.
  - Allow retry only failed rows.
  - Preserve selection after partial failure unless user clears it.

### Performance

- Virtualize or window the 10,000-row table using an existing approved pattern if available.
- Memoize derived filtered/sorted rows with correct dependencies.
- Debounce or defer filter input work so typing remains responsive.
- Avoid recalculating expensive formatting per cell on every render.
- Stabilize row props and callbacks where row rendering is hot.
- Reserve image dimensions and lazy-load non-critical images.
- Avoid `transition: all` on rows; do not animate properties that trigger layout.
- Ensure bulk selection does not require touching 10,000 React row components synchronously when possible.

---

## 4. Static signals: decisive vs context-dependent

### Decisive from the provided source

- `catch {}` means save failures are swallowed.
- `rows.map(...)` means all rows render if `rows` has 10,000 items.
- One global `saving` boolean cannot fully model concurrent row/batch/drawer save states.
- Blank loading body is an explicit missing state.
- Absence of listed error states is a production hardening gap.
- `min-width: 1180px` conflicts with tablet support unless contained by a deliberate overflow strategy.
- `transition: all` is risky for row/drawer performance and motion accessibility.
- `outline: none` without a replacement focus style is an accessibility failure.
- Fixed drawer width needs responsive constraints for tablet.
- No focus trap/background blocking for a fixed edit drawer is an accessibility and data-safety issue.
- Unreserved image dimensions can cause layout shift.

### Needs project/runtime context

- Exact render time and memory impact of 10,000 rows.
- Whether an existing table component already supports virtualization.
- Actual filter complexity and whether filtering blocks noticeably on target devices.
- Whether row height is fixed enough for simple virtualization.
- API save semantics: idempotency, conflict versioning, retries, and cancellation.
- Whether image uploads are direct, presigned, chunked, compressed, or proxied.
- Permission model and whether unauthorized controls should be hidden or disabled.
- Exact tablet breakpoints and supported browser/device matrix.
- Existing accessible-name conventions in the design system.
- Whether autosave means field-level, drawer-level, row-level, or batch-level save.
- Whether server supports partial batch result reporting.

---

## 5. Measurement-first validation plan

### Baseline before changes

- Capture current expected workflow:
  - Load inventory.
  - Filter products.
  - Select bulk rows.
  - Open drawer.
  - Edit product.
  - Upload image.
  - Save successfully.
  - Simulate save failure paths at the API boundary in test/staging.
- Record:
  - Initial render time for 10,000 rows.
  - Filter input responsiveness.
  - Drawer open/close responsiveness.
  - Scroll smoothness.
  - Image layout shift.
  - Save lifecycle timing.
  - Error recovery success rate.
  - Keyboard-only task completion.

### Validation after hardening

- Correctness acceptance:
  - No silent save failures.
  - Saving state always resolves.
  - Failed edits remain recoverable.
  - Conflicts are visible and actionable.
  - Partial batch failures identify failed rows.
- Failure-state acceptance:
  - Loading, empty, 401/403, 409, 429, 500, timeout, offline, retry, and partial failure states are represented.
- Accessibility acceptance:
  - Drawer traps focus.
  - Background is not interactive while drawer is open.
  - Focus returns correctly.
  - Icon-only controls have accessible names.
  - Keyboard users can filter, select, edit, save, retry, and close.
  - Visible focus is present.
  - Reduced-motion preference is respected.
- Responsive acceptance:
  - Desktop workflow remains unchanged in structure.
  - Tablet has no unusable clipped controls.
  - Drawer and filters remain operable.
  - Dense table overflow, if used, is intentional and discoverable.
- Performance acceptance:
  - 10,000-row load and filter interactions remain within agreed product thresholds.
  - Typing in filters does not visibly stall.
  - Scrolling remains stable.
  - Image loading does not shift row layout.
  - Bulk selection does not freeze the surface.

### Rollback conditions

- Roll back or feature-flag if:
  - Save reliability regresses.
  - Operators lose edits during drawer close, navigation, retry, or conflict.
  - Keyboard access regresses.
  - Tablet workflow becomes less usable than current behavior.
  - Virtualization breaks selection, row height, sticky affordances, or screen-reader navigation.
  - Error-state handling hides successful saves or blocks valid work.

### Acceptance condition

Ship only when the existing workflow is preserved, failure states are explicit, edits are recoverable, keyboard/drawer behavior is safe, and the 10,000-row path is measured against agreed desktop and tablet thresholds.
