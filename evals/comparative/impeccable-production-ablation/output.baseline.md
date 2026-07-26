## 1. Sequencing and verdict

**Correct sequence:** audit current failure modes → harden data/save/error handling → restore accessibility and state recovery → optimize table/filter/image hot paths → polish responsive layout, motion, and microcopy within the existing design system.

**Verdict:** Static evidence indicates this surface is not production-ready for a 10,000-row operations workflow until silent failures, drawer accessibility, missing recovery states, and unbounded rendering are hardened.

---

## 2. Prioritized findings

### P0 — Silent save failure can hide data loss

**Source evidence**
- `catch {}` swallows all save errors.
- `setSaving(false)` runs after failure with no user-visible state.
- Missing states are explicitly noted for `409`, `429`, `500`, timeout, offline, retry, and partial batch failure.
- Drawer can close via Escape while save is pending.

**Runtime hypothesis**
- Operators may believe an edit was saved when it failed.
- Closing the drawer during a pending save may discard local context or make recovery unclear.
- Conflicts may overwrite newer server data if no 409 resolution path exists.

**Fix**
- Replace silent catch with typed save states: `idle | saving | saved | failed | conflict | offline | retrying`.
- Keep failed edits locally recoverable in the drawer.
- Disable destructive close while save is pending, or require confirmation with clear “save in progress” copy.
- Show conflict resolution for 409: server value, local value, choose/merge/retry.
- Add retry affordance for timeout/429/500/offline with backoff and non-blocking status.

---

### P0 — Drawer is not accessible or interaction-safe

**Source evidence**
- Drawer traps neither focus nor background interaction.
- Escape closes it even while save is pending.
- Save and close are icon-only.
- `.icon-button { outline: none; }`
- Keyboard navigation, screen-reader labels, and focus-visible are not described.

**Runtime hypothesis**
- Keyboard and screen-reader users may lose position, interact with background rows behind the drawer, or fail to understand icon actions.
- Removing outline may make focused controls invisible.

**Fix**
- Treat drawer as a modal or clearly non-modal panel; if modal, trap focus, restore focus to opener, inert/disable background interaction, and label the dialog.
- Add accessible names to icon-only controls: “Save product”, “Close editor”.
- Replace `outline: none` with a visible `:focus-visible` style using existing tokens.
- Gate Escape behavior: if dirty or saving, show confirm/retry state instead of closing immediately.
- Ensure Save button exposes disabled/busy state with `aria-busy` or equivalent status text.

---

### P0 — Critical production states are absent

**Source evidence**
- Initial and filter loading render a blank table body.
- Empty results, 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.

**Runtime hypothesis**
- Blank table can be misread as “no products” or a broken page.
- Permission errors may look identical to loading or empty data.
- Batch operations can leave users unsure which products succeeded.

**Fix**
- Add distinct states for loading, empty filtered results, empty inventory, unauthorized, forbidden, server error, timeout, offline, rate-limited, conflict, and partial success.
- Preserve table/header/filter context during loading instead of blanking the body.
- For partial batch failure, show count-level summary plus row-level retry/errors.
- Use existing status/alert components rather than introducing a new notification pattern.

---

### P1 — 10,000-row rendering and filtering are likely hot-path failures

**Source evidence**
- `{rows.map(...)}` renders all rows.
- “All 10,000 rows render at once.”
- Filtering recalculates synchronously on every keystroke.
- Global `saving` state lives on `InventoryPage`, so save state changes can re-render the page tree.

**Runtime hypothesis**
- Typing in filters may jank.
- Save status changes may cause unnecessary row work.
- Initial load may block the main thread and increase memory pressure.

**Fix**
- Virtualize or window the product rows while preserving keyboard and selection semantics.
- Debounce or defer filtering input; memoize filtered results with correct dependencies.
- Move per-row/per-product save state closer to the edited product or store it by product id.
- Use stable row props and memoized row components where appropriate.
- Keep bulk selection state independent from row rendering churn.

---

### P1 — Hostile data is not safely represented

**Source evidence**
- Product names may be 1–200 characters.
- Prices may be missing.
- Labels may expand by 60 percent in translation.
- Images may be absent or 8MB.
- `.product-name` truncates with ellipsis only.
- Image dimensions are not reserved.

**Runtime hypothesis**
- Long names may hide distinguishing information.
- Missing prices may be confused with zero.
- Translated labels may overflow fixed columns.
- Large or absent images may cause layout shift or slow rendering.

**Fix**
- Add explicit missing-value treatment: “Price missing”, “No image”, “Not translated”, etc.
- Preserve full product names via accessible title/details pattern, not only visual ellipsis.
- Reserve image dimensions and use placeholders for absent images.
- Use thumbnails or constrained image loading; avoid loading full 8MB assets in table rows.
- Test expanded labels against the existing grid and drawer layout before shipping.

---

### P1 — Permission-specific affordances are unspecified

**Source evidence**
- Permission-specific affordances are not described.
- 401/403 states are not represented.
- Bulk selection, edit drawer, image uploads, and autosave imply role-sensitive actions.

**Runtime hypothesis**
- Users without edit/upload permission may see controls they cannot use.
- Failed save/upload due to permissions may appear as generic failure.

**Fix**
- Hide or disable unavailable actions with explanatory copy.
- Distinguish authentication failure from authorization failure.
- Make read-only rows and drawer fields visibly read-only, not merely non-functional.
- Preserve auditability for blocked bulk actions: which action, which permission, what to do next.

---

### P2 — Tablet and constrained-width behavior are likely brittle

**Source evidence**
- `.page { min-width: 1180px; }`
- Drawer is fixed at `width: 520px; height: 100vh`.
- Tablet behavior is not described.

**Runtime hypothesis**
- Tablet users may get horizontal overflow, clipped drawer content, or unreachable controls.
- Fixed drawer width may consume too much viewport width.

**Fix**
- Define tablet breakpoints within the current layout system.
- Use responsive drawer sizing such as `width: min(520px, 100vw)` with safe-area handling.
- Keep primary table actions reachable when horizontal scrolling is unavoidable.
- Ensure drawer content scrolls internally without trapping page scroll unpredictably.

---

### P2 — Motion is broad, potentially expensive, and lacks reduced-motion path

**Source evidence**
- `.product-row, .drawer { transition: all 300ms ease-in; }`
- Reduced motion is not described.

**Runtime hypothesis**
- `transition: all` can animate layout-affecting properties and produce jank across many rows.
- Users requesting reduced motion may still receive full transitions.

**Fix**
- Replace `transition: all` with specific properties, ideally `transform` and `opacity` where motion is needed.
- Avoid transitions on 10,000 row elements unless scoped to interacted rows.
- Add reduced-motion CSS that removes or shortens movement while preserving state feedback.

---

### P3 — Autosave status is too global for operator confidence

**Source evidence**
- Single `saving` boolean passed to `EditDrawer`.
- Route includes autosave status, but source only represents global saving true/false.

**Runtime hypothesis**
- Operators may not know which product is saving, saved, failed, or conflicted.
- Rapid edits may race if save responses resolve out of order.

**Fix**
- Track status per product/edit session.
- Include last-saved timestamp or “unsaved changes” indicator where appropriate.
- Ignore stale save responses using request ids or revision tokens.
- Keep status calm and persistent enough for repeated operations work.

---

## 3. Concrete hardening moves by area

### Hostile data
- Render explicit placeholders for missing price/image fields.
- Reserve image boxes and use table-safe thumbnails.
- Support 200-character names with accessible full-value access.
- Validate translated labels at +60% expansion.
- Avoid treating null, zero, empty string, and unknown as the same visual state.

### Failures
- Add typed error states for load, filter, save, upload, auth, conflict, rate limit, offline, and partial batch failure.
- Never swallow save/upload errors.
- Preserve user input across retry.
- Provide row-level and batch-level error summaries.
- Make retry idempotent where possible.

### Responsive layout
- Keep desktop-first table workflow but define tablet constraints.
- Change fixed drawer width to bounded responsive width.
- Ensure controls remain reachable at tablet widths.
- Avoid relying on `min-width: 1180px` as the only tablet strategy.

### Accessibility
- Add drawer focus trap, focus restoration, accessible name, and background inerting if modal.
- Add labels for icon-only buttons.
- Restore visible `:focus-visible`.
- Define keyboard navigation for table rows, selection, drawer open/close, save, and upload.
- Announce loading, saving, saved, failed, and conflict states through appropriate status regions.

### State recovery
- Track dirty state separately from saving state.
- Prevent accidental close during dirty/saving states.
- Store pending edit locally until save succeeds or user explicitly discards.
- Handle offline/timeout retry without losing drawer contents.
- Resolve 409 conflicts without silently overwriting.

### Performance
- Window 10,000 rows.
- Defer/debounce filter computation.
- Memoize derived rows.
- Avoid global state updates that re-render the full table.
- Reserve image dimensions and lazy-load/decode thumbnails.
- Measure keystroke latency, initial render time, row interaction latency, and drawer open latency.

---

## 4. Static signals: decisive vs context-dependent

### Decisive from the provided source
- Silent failure exists: `catch {}` is present.
- All rows are rendered with `rows.map(...)`.
- Save state is only a boolean.
- `transition: all` is present.
- Focus outline is removed on icon buttons.
- Page has fixed minimum width.
- Drawer has fixed width and viewport height.
- Current snippet does not represent the listed failure states.
- Current CSS does not include a reduced-motion branch.

### Needs project/runtime context
- Exact jank severity from 10,000 rows.
- Whether `ProductRow` is memoized internally.
- Whether `Filters` already debounce or defer outside the snippet.
- Whether design-system components add labels, focus styles, or status semantics elsewhere.
- Whether image URLs are thumbnailed by the backend/CDN.
- Whether route-level auth wrappers handle 401/403.
- Whether the drawer is intended to be modal or non-modal.
- Exact tablet breakpoints and supported browser/device matrix.
- Whether autosave uses revision tokens or request cancellation elsewhere.

---

## 5. Measurement-first validation plan

### Baseline before changes
- Record initial render time for 10,000 rows.
- Record filter keystroke latency on representative data.
- Record drawer open/close latency.
- Record save success, failure, timeout, offline, 409, and retry behavior using controlled mocked responses.
- Record image loading layout shift with absent and large images.
- Review keyboard-only path through filters, table, selection, drawer, save, upload, and close.

### Acceptance conditions
- No save failure is silent.
- Dirty or saving edits cannot be lost through Escape or accidental close.
- Loading, empty, permission, conflict, offline, rate-limit, timeout, server-error, retry, and partial-failure states are visible and distinguishable.
- Keyboard users can complete core edit/save/upload flows.
- Focus is always visible and restored after drawer close.
- Reduced-motion users receive minimal movement with preserved state feedback.
- 10,000-row table remains responsive during filtering and row interaction.
- Images do not cause visible row layout jumps.
- Tablet layout keeps primary actions reachable.

### Rollback conditions
- Virtualization breaks selection, row focus, or screen-reader row context.
- Debounced/deferred filtering makes result state feel stale without feedback.
- New save-state handling blocks legitimate operator workflows.
- Drawer focus trapping prevents access to required non-modal reference content.
- Error messaging adds noise without clear recovery actions.
- Responsive changes degrade the primary desktop workflow.

### Production rollout
- Ship hardening behind a narrow feature flag if possible.
- Start with save/error recovery and drawer accessibility before performance polish.
- Monitor save failures, retries, conflicts, abandoned dirty drawers, filter latency, and upload failures.
- Keep rollback scoped: state handling, virtualization, drawer behavior, and responsive sizing should be independently reversible.
