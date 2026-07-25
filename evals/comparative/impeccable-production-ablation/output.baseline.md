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
