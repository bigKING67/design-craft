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
