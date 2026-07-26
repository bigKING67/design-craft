## 1) Sequencing and verdict

**Correct sequence:** baseline/audit → harden correctness and recovery → measure and optimize hot paths → polish within the existing design system → validate with rollback gates.

**One-line verdict:** As described, this surface is not production-ready for a 10,000-row operations workflow because save failures can be silent, required recovery states are absent, drawer accessibility is unsafe, and the table/filter path is unbounded.

---

## 2) Prioritized findings

### P0 — Silent save failure can mislead operators into data loss
- **Source evidence:** `catch {}` swallows `api.save(product)` errors; `setSaving(false)` runs after failure with no error state.
- **Why it matters:** Operators may believe inventory edits saved when they did not.
- **Runtime hypothesis:** Actual backend/API layer may emit global errors, but that is not shown here and cannot be assumed.
- **Fix:** Return explicit save states: `idle | saving | saved | failed | conflict | offline | unauthorized`; surface retry, last-saved timestamp, field-level/server messages, and telemetry-safe error context.

### P0 — Drawer interaction can interrupt pending writes and lacks modal safety
- **Source evidence:** Drawer does not trap focus/background interaction; Escape closes it while save is pending; save/close are icon-only.
- **Why it matters:** Users can lose context, trigger background actions, or close during a pending save with no recovery path.
- **Runtime hypothesis:** A shared `EditDrawer` may add some behavior internally, but notes explicitly say focus trap/background handling are absent.
- **Fix:** Add modal semantics if it is modal, focus trap, focus restore, inert/blocked background, labeled controls, pending-save close guard, and clear “saving / failed / retry / discard” paths.

### P1 — Required production states are missing
- **Source evidence:** Blank table body during initial/filter loading; no empty, 401/403, 409, 429, 500, timeout, offline, retry, or partial batch failure states.
- **Why it matters:** Operations staff cannot distinguish “no products,” “still loading,” “not authorized,” “rate limited,” “conflict,” or “failed but recoverable.”
- **Runtime hypothesis:** Route-level boundaries may catch some failures, but no state ownership is described for this surface.
- **Fix:** Own a state matrix for initial load, filter load, empty results, permission, auth expiry, conflict, rate limit, server error, timeout, offline, retrying, and partial batch outcomes.

### P1 — Table/filter performance is unbounded for stated scale
- **Source evidence:** `{rows.map(...)}` renders all rows; notes say all 10,000 rows render at once and filtering recalculates synchronously on every keystroke.
- **Why it matters:** This is a clear hot path for keyboard-heavy operators.
- **Runtime hypothesis:** Static code proves unbounded work, not actual latency on target devices; severity stays P1 until measured release-blocking lag is observed.
- **Fix:** Bound rendered rows with existing pagination/windowing patterns, memoize derived rows, defer/debounce filter work appropriately, avoid global state churn, and measure keystroke-to-render latency.

### P1 — Responsive/tablet contract is not credible as written
- **Source evidence:** `.page { min-width: 1180px; }`; fixed drawer width `520px`; fixed row columns; tablet behavior not described.
- **Why it matters:** Tablet support can become horizontal page overflow with unreachable actions.
- **Runtime hypothesis:** A parent shell may provide controlled horizontal scrolling, but no evidence says critical actions remain reachable.
- **Fix:** Keep unavoidable horizontal overflow isolated to the data grid, not the whole page; define tablet breakpoints, drawer width constraints, sticky critical actions, and touch target sizing.

### P1 — Accessibility fundamentals are missing or contradicted
- **Source evidence:** `.icon-button { width: 28px; height: 28px; outline: none; }`; icon-only save/close; no labels, keyboard navigation, focus-visible, screen-reader behavior, or reduced motion described.
- **Why it matters:** Keyboard-heavy operators and assistive tech users need predictable focus, names, target sizes, and reduced-motion behavior.
- **Runtime hypothesis:** Components may add aria labels internally, but the source notes say labels/focus behavior are not described; `outline: none` is a decisive risk unless replaced by visible `:focus-visible`.
- **Fix:** Add accessible names, visible focus states, keyboard row navigation, table/grid semantics, drawer focus management, reduced-motion CSS, and larger effective targets for tablet.

### P2 — Hostile data will break layout and trust
- **Source evidence:** Names can be 1–200 chars; prices may be missing; translations expand labels 60%; images may be absent or 8MB; `.product-name` truncates; fixed grid columns.
- **Why it matters:** Operators need enough context to identify products and avoid editing the wrong row.
- **Runtime hypothesis:** Tooltips/detail drawer may expose full values elsewhere, but not shown.
- **Fix:** Provide full-name access on focus/hover or drawer, missing-price affordance, resilient localized labels, reserved image boxes, fallback thumbnails, image size validation/compression, and non-shifting placeholders.

### P2 — Motion implementation is too broad and may be expensive or inaccessible
- **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`; reduced motion not described.
- **Why it matters:** `transition: all` can animate layout/paint properties accidentally; `ease-in` can feel sluggish for drawer entry; reduced-motion users get no alternative.
- **Runtime hypothesis:** Actual changed properties are unknown, so jank is not proven.
- **Fix:** Transition only `transform`/`opacity` where appropriate, use purposeful durations/easing, disable or simplify under `prefers-reduced-motion`, and avoid animating many rows.

### P3 — Autosave status is underspecified
- **Source evidence:** Only a boolean `saving` is stored.
- **Why it matters:** A single global boolean cannot distinguish which product is saving, saved, failed, stale, conflicted, or retrying.
- **Runtime hypothesis:** `EditDrawer` may localize details, but not shown.
- **Fix:** Track per-edit lifecycle with timestamps and recoverable error payloads; prevent false “saved” states after failures.

---

## 3) Concrete fixes by area

### Hostile data
- Reserve image dimensions in every row; show absent-image fallback.
- Reject/compress oversized uploads before save where product rules allow; show progress and failure.
- Treat missing price as an explicit state, not blank text.
- Keep 200-character names identifiable: truncate in rows but expose full value via focusable disclosure, title/details, or drawer context.
- Test labels with 60% expansion and long currency/number formats.
- Ensure grid columns can shrink safely; do not let product names push controls offscreen.

### Failures and recovery
- Replace `catch {}` with typed error handling and user-visible outcomes.
- Add specific UI for 401/403, 409 conflict, 429, 500, timeout, offline, retry, and partial batch failure.
- Preserve edits locally while retrying or after failed save.
- For 409, show server version versus local change and require explicit resolve.
- For partial batch failure, identify failed rows and allow retry only failed items.
- Make autosave status truthful: saving, saved at time, failed, retrying, offline queued, conflict.

### Responsive layout
- Remove page-level minimum width as the only tablet strategy.
- Constrain horizontal scrolling to the table region if dense columns must remain.
- Make drawer width `min(520px, viewport-safe-width)` with tablet-specific behavior.
- Keep filters, bulk actions, save/close, and row primary identifiers reachable.
- Define tablet breakpoints and minimum effective target sizes before polish.

### Accessibility
- Add accessible names to icon-only save and close controls.
- Restore visible `:focus-visible`; do not rely on removed outlines without replacement.
- Trap focus in the drawer, restore focus on close, and block background interaction when modal.
- Disable Escape close while saving, or require confirmation with recovery copy.
- Provide keyboard navigation for rows, selection, filters, drawer actions, and bulk actions.
- Use semantic table/grid structure appropriate to the interaction model.
- Respect `prefers-reduced-motion`.
- Confirm screen-reader announcements for loading, save success/failure, conflict, and upload progress.

### State recovery
- Keep unsaved edits across transient failures, drawer close attempts, and auth interruptions where safe.
- Confirm destructive close/discard when pending or failed changes exist.
- Store enough local state to retry without retyping.
- Prevent stale saves from overwriting newer edits; handle out-of-order save responses.
- Make permission-specific affordances explicit: disabled with reason, hidden only when policy requires it.

### Performance
- Bound row rendering via existing table pagination/windowing/virtualization patterns.
- Memoize filtered/sorted rows with correct dependencies.
- Avoid synchronous recalculation on every keystroke; use deferred input or debounced filtering where it preserves operator flow.
- Keep row components memoized and avoid passing unstable props/functions.
- Lazy-load or defer noncritical images; reserve dimensions to prevent layout shift.
- Replace `transition: all` with property-specific transitions.
- Do not introduce a new heavy table dependency unless current project primitives cannot meet measured budgets.

---

## 4) Static detector-like signal reconciliation

**Decisive from the supplied source/notes:**
- `catch {}` means this save path has no local error handling.
- Blank loading body and missing listed states mean this surface does not represent required production states as described.
- Rendering all 10,000 rows and synchronous filtering prove unbounded render/filter work.
- `outline: none` on icon buttons is an accessibility failure unless a replacement focus style exists elsewhere.
- No focus trap/background lock in the drawer is unsafe for a modal edit surface.
- `transition: all` is a concrete implementation smell.
- Fixed `min-width`, fixed grid columns, and fixed drawer width are responsive risks for tablet support.

**Needs project/runtime context before final severity or exact implementation:**
- Actual perceived latency, INP, memory use, and scroll smoothness.
- Whether route-level auth/error boundaries already cover some failures.
- Whether shared components inject aria labels, focus styles, or modal behavior despite this snippet.
- Whether the existing design system already defines table density, drawer motion, error banners, toasts, or upload components.
- Whether server-side filtering, pagination, caching, or API conflict semantics exist.
- Whether horizontal table overflow is an accepted pattern in this product.
- Actual contrast, hit target comfort, screen-reader output, and reduced-motion behavior.
- Real upload constraints, image processing location, and offline policy.

---

## 5) Measurement-first validation plan with rollback/acceptance

### Baseline before changes
- Capture current behavior for 10,000 rows: initial render, filter keystroke latency, row selection, drawer open/close, save success/failure, and image-heavy rows.
- Record mounted row count, long tasks, memory trend, layout shifts, and p95 key-to-visible-results time.
- Exercise state cases with controlled API responses: 401/403, 409, 429, 500, timeout, offline, and partial batch failure.
- Keyboard-only pass: filters → table → bulk selection → drawer → save/close → recovery.
- Assistive-tech-oriented pass: names, roles, announcements, focus order, and focus restoration.
- Responsive pass for desktop and tablet widths.

### Provisional acceptance conditions
- No save failure can end in a false-success or silent state.
- Closing during pending/failed save cannot discard edits without an explicit recoverable choice.
- Every listed loading/empty/error/permission/conflict/offline/partial state renders specific copy and an available next action.
- 10,000-row path has bounded DOM work; mounted row count remains within the chosen table strategy’s expected window/page size.
- Provisional performance budget: p95 filter input-to-visible-update under 150ms on target desktop hardware and under 250ms on supported tablet hardware; no repeated long tasks over 50ms during ordinary filtering/selection.
- Image rows reserve dimensions; no noticeable layout shift from late image load, with CLS budget ratified by the project.
- Keyboard focus is always visible; drawer traps/restores focus; icon-only actions have accessible names.
- Reduced-motion mode preserves state feedback without broad motion.

### Rollback conditions
- Roll back or feature-flag optimization changes if measured input latency, memory, or error rate regresses beyond agreed budget.
- Roll back visual/motion polish if it breaks existing design-system tokens, focus visibility, reduced-motion behavior, or operator task speed.
- Roll back table strategy if it loses selection state, keyboard position, screen-reader usability, or bulk-action correctness.
- Roll back autosave changes if they introduce duplicate writes, stale overwrites, or unrecoverable conflicts.

No runtime detector, browser, build, profiler, accessibility tree, network throttle, or device validation is claimed here; this is a static production audit based only on the supplied facts.
