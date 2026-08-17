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
