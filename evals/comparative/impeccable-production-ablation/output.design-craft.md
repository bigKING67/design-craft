## 1. Sequencing + verdict

**Correct sequence:** static audit → define measurement baseline → harden correctness/recovery/accessibility/failure states → optimize proven hot paths → polish within the existing design system → validate release gates with rollback criteria.

**One-line verdict:** The surface is directionally recognizable as an inventory editor, but the static evidence shows production blockers around save reliability, state recovery, accessibility, 10k-row rendering, and hostile data handling before any visual polish should be prioritized.

---

## 2. Prioritized findings

### P0 — Save failures can silently lose operator trust and state
- **Source evidence:** `catch {}` swallows `api.save(product)` errors; `setSaving(false)` runs without success/failure distinction.
- **Source evidence:** Missing 409, 429, 500, timeout, offline, retry, and partial batch failure states.
- **Runtime hypothesis:** Operators may believe changes saved when they failed, especially during autosave or drawer close flows.
- **Fix:** Return explicit save states: `idle | saving | saved | failed | conflict | offline | rateLimited`. Preserve dirty edits, show retry, expose conflict resolution, and never clear pending edits solely because a request ended.

### P0 — Drawer interaction is unsafe during editing/saving
- **Source evidence:** Drawer traps neither focus nor background interaction.
- **Source evidence:** Escape closes it even while save is pending.
- **Source evidence:** Save and close are icon-only.
- **Runtime hypothesis:** Keyboard and screen-reader users can lose context or activate background rows while editing; pending saves may be interrupted.
- **Fix:** Make the drawer modal or clearly non-modal by contract. For modal behavior: focus trap, inert/disabled background, labelled title, labelled buttons, restore focus on close, block/destructure close during pending save with confirmation or queue-safe cancellation.

### P1 — 10,000-row synchronous rendering/filtering is a hot-path risk
- **Source evidence:** `{rows.map(...)}` renders all rows.
- **Source evidence:** Filtering recalculates synchronously on every keystroke.
- **Runtime hypothesis:** Keystrokes, selection, drawer edits, and autosave status changes may cause long commits and input delay.
- **Fix:** Virtualize/window the table, debounce or defer filter text application, memoize derived filtered rows, avoid page-wide state churn from `saving`, and isolate row rendering from drawer save status.

### P1 — Required production states are absent
- **Source evidence:** Initial/filter loading render a blank table body.
- **Source evidence:** Empty results, auth/permission, conflict, rate-limit, server, timeout, offline, retry, and partial batch failure states are not represented.
- **Runtime hypothesis:** Users cannot distinguish “no results” from “still loading” or “failed,” increasing duplicate work and support load.
- **Fix:** Add explicit state surfaces in the existing table shell: skeleton/loading rows, empty result copy with filter reset, permission-specific disabled affordances, retry panels, offline banner, conflict callout, and partial batch result summary.

### P1 — Accessibility basics are incomplete for a keyboard-heavy tool
- **Source evidence:** `.icon-button { width: 28px; height: 28px; outline: none; }`
- **Source evidence:** Icon-only save/close.
- **Source evidence:** Keyboard navigation, screen-reader labels, focus-visible, and reduced motion are not described.
- **Runtime hypothesis:** There may be no perceivable focus, insufficient target size on tablet, unlabeled controls, and inaccessible row/drawer workflows.
- **Fix:** Restore visible `:focus-visible`, add accessible names, confirm tab order, support row/action keyboard shortcuts without trapping users, provide table semantics, and set tablet hit targets to a project-approved comfortable size.

### P2 — Hostile data can break layout and comprehension
- **Source evidence:** Product names can be 1–200 characters; `.product-name` truncates nowrap with ellipsis.
- **Source evidence:** Prices may be missing; translations may expand labels by 60%; some images are absent or 8MB.
- **Runtime hypothesis:** Operators may lose critical identifying information, see broken alignment, or suffer layout shift/slow image decode.
- **Fix:** Add tooltip/details access for truncated names, missing-price state, localized label stress tests, reserved image dimensions, fallback image cells, upload size validation/compression guidance, and async image handling.

### P2 — Tablet support conflicts with fixed desktop layout
- **Source evidence:** `.page { min-width: 1180px; }`
- **Source evidence:** Drawer fixed at `width: 520px; height: 100vh;`.
- **Runtime hypothesis:** Tablet users may get horizontal scrolling, clipped drawer content, viewport-height bugs, or unusable touch targets.
- **Fix:** Preserve the desktop workflow but add tablet breakpoints: table horizontal scroll containment, drawer width as `min(520px, 100vw)` or tokenized equivalent, safe viewport units, and touch target spacing.

### P2 — Motion implementation is over-broad and may be uncomfortable
- **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`
- **Source evidence:** Reduced motion is not described.
- **Runtime hypothesis:** Unintended properties may animate, drawer motion may feel delayed, and users requesting reduced motion may still get full transitions.
- **Fix:** Transition only intended properties, usually `transform`/`opacity`; avoid animating layout properties; use reduced-motion media query that preserves state feedback without large movement.

### P3 — Global save state is too coarse for a dense editor
- **Source evidence:** Single `saving` boolean is owned by the page and passed to `EditDrawer`.
- **Runtime hypothesis:** Concurrent saves, autosave, bulk actions, and row-level edits may produce ambiguous status.
- **Fix:** Track save state by product/batch/request id where needed; expose global autosave summary separately from row/drawer pending state.

---

## 3. Concrete hardening/polish/optimization moves

1. **Save contract hardening:** replace swallowed errors with typed outcomes, visible status, retry, dirty-state preservation, conflict handling, and close protection while pending.
2. **State shell:** keep the table frame visible during loading/error/empty states so operators retain orientation; never use a blank body as the only feedback.
3. **Drawer accessibility:** labelled controls, focus trap or explicit non-modal behavior, background interaction policy, Escape rules, focus restoration, pending-save confirmation.
4. **Table performance:** introduce row windowing, stable row keys, memoized filtered data, deferred filter updates, and localized state updates so autosave does not rerender 10,000 rows.
5. **Hostile data coverage:** long-name expansion path, missing price placeholder, absent/large image handling, reserved media dimensions, upload validation, translation expansion checks.
6. **Responsive containment:** preserve desktop density but make tablet behavior explicit with constrained drawer width, scrollable table region, safe viewport sizing, and larger touch targets where needed.
7. **Permission-aware UI:** render disabled or hidden actions based on capability, with explanatory affordances for 401/403 rather than generic failure.
8. **Motion polish:** replace `transition: all` with scoped transitions and reduced-motion alternatives; avoid motion that obscures save/error state changes.

---

## 4. Static detector-like signal reconciliation

**Decisive from the supplied source/scope**
- Empty `catch {}` proves save errors are swallowed in the shown path.
- Missing listed state branches are decisive within the provided source notes.
- `rows.map(...)` proves unwindowed rendering in the shown component.
- `min-width: 1180px` proves a fixed desktop floor exists.
- `outline: none` proves the default outline is removed for `.icon-button`.
- Icon-only save/close plus missing labels note proves accessible naming is not represented.
- “Drawer traps neither focus nor background interaction” is decisive as supplied product evidence.

**Signals that are strong risks but need project/runtime context**
- Actual typing latency, commit duration, memory use, and frame rate require profiling.
- Actual layout shift from images requires dimensions/runtime rendering evidence.
- Whether focus is fully invisible requires checking inherited/custom `:focus-visible` styles.
- Whether `transition: all` causes jank depends on which properties change at runtime.
- Whether global `saving` causes concurrency bugs depends on actual autosave/bulk call paths.
- Tablet usability needs viewport testing against target tablet sizes and input modes.
- Screen-reader quality requires semantic DOM/accessibility tree validation.

---

## 5. Measurement-first validation plan with rollback/acceptance

**Baseline before changes**
- Measure initial render time, row count mounted, memory, long tasks, and filter keystroke latency with 10,000 rows.
- Measure drawer open/close interaction, save pending state, image loading/layout shift, and tablet viewport behavior.
- Capture failure-path behavior for save failure, conflict, offline, timeout, 401/403, 429, 500, and partial batch failure.
- Audit keyboard path: filters → table rows/actions → drawer → save/close → focus restore.

**Acceptance conditions**
- No save failure is silent; dirty edits survive failed/retried saves.
- Closing during pending save is blocked, confirmed, or safely resumable.
- Loading, empty, permission, conflict, offline, retry, timeout, server error, and partial batch states render clear user actions.
- 10,000-row filtering remains responsive under agreed thresholds, with no full-table rerender on unrelated drawer save state.
- Keyboard users can complete the core edit/save flow with visible focus and labelled controls.
- Tablet layout remains usable without destructive clipping of table actions or drawer controls.
- Large/missing images do not collapse layout or block primary editing.

**Rollback conditions**
- Any change hides inventory data, breaks bulk selection, drops unsaved edits, removes existing workflow affordances, or worsens measured input latency.
- Any optimization that changes row order, selection persistence, permission behavior, or save semantics without explicit product approval should be reverted.
- Any visual polish that bypasses existing tokens/components or reduces density without solving a documented production issue should be deferred.
