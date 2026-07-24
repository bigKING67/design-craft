## 1. Sequencing + verdict

**Recommended sequence:** audit evidence → harden correctness/state recovery → add failure and permission states → optimize hot paths → polish responsive, motion, and accessibility details.

**One-line verdict:** This surface is not yet production-hardened for a high-volume inventory workflow: the largest risks are silent save failure, unrecoverable/conflicting edits, inaccessible drawer controls, and avoidable 10,000-row rendering cost.

---

## 2. Prioritized findings

### P0 — Silent save failure and unsafe recovery gaps

**Source evidence**
- `catch {}` swallows all save errors.
- `setSaving(false)` runs after both success and failure with no user-visible distinction.
- Additional notes say 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.
- Drawer can close via Escape while save is pending.

**Runtime hypothesis**
- Operators may believe a product was saved when it failed.
- Pending edits may be lost if the drawer closes during save.
- Conflict responses may overwrite newer inventory data or hide stale-edit problems.

**Fix**
- Replace silent catch with explicit save states: `idle | saving | saved | failed | conflict | offline | unauthorized | rateLimited`.
- Surface inline drawer error and page-level autosave status.
- Preserve dirty form data after failure.
- Disable destructive close while saving, or require confirmation when dirty/pending.
- For 409, show conflict resolution: “server value vs your edit,” reload option, and retry after review.
- For 401/403, show permission-specific messaging and disable unavailable actions.
- For partial batch failure, report count succeeded/failed and keep failed rows selected for retry.

---

### P0 — Permission and destructive-action affordances are underspecified

**Source evidence**
- Permission-specific affordances are not described.
- Save and close are icon-only.
- Failure states for 401/403 are missing.

**Runtime hypothesis**
- Users may attempt edits/uploads they cannot complete.
- Icon-only actions may be ambiguous, especially in high-repetition workflows.

**Fix**
- Gate edit, bulk edit, upload, and save controls by permission.
- Use disabled/read-only states with clear reason text, not hidden-only behavior.
- Add accessible names and visible tooltips/help text for icon-only save/close.
- Ensure unauthorized responses do not discard local unsaved changes.

---

### P1 — 10,000 rows render at once and filters run synchronously

**Source evidence**
- `{rows.map(...)}`
- Notes state all 10,000 rows render at once.
- Filtering recalculates synchronously on every keystroke.

**Runtime hypothesis**
- Keystrokes, selection, drawer open/close, and filter changes may jank.
- Memory pressure may increase when image cells are included.
- Bulk selection may trigger full-list re-renders.

**Fix**
- Window/virtualize table rows using existing project patterns if available.
- Keep row height predictable or measured.
- Memoize filtered/sorted row sets with correct dependencies.
- Defer expensive filtering from raw keystrokes: debounce query application or use low-priority updates where supported.
- Isolate selection state so toggling one row does not re-render all rows.
- Memoize `ProductRow` where props are stable.
- Use stable callbacks for row actions.
- Paginate or window bulk operations UI while preserving “select all matching filter” semantics.

---

### P1 — Drawer accessibility and interaction model are unsafe

**Source evidence**
- Drawer traps neither focus nor background interaction.
- Escape closes even while save is pending.
- Save and close are icon-only.
- `.icon-button { width: 28px; height: 28px; outline: none; }`

**Runtime hypothesis**
- Keyboard users may tab into background content while editing.
- Screen-reader users may not receive modal context.
- Users may lose pending edits by pressing Escape.
- Focus may become lost after close.

**Fix**
- If the drawer behaves modally, use dialog semantics, labelled title, focus trap, background inerting, and focus return.
- If it is non-modal, make that explicit and do not trap focus, but provide clear keyboard path and preserve background interaction intentionally.
- Escape behavior:
  - no dirty state: close;
  - dirty state: confirm;
  - saving: block close or queue close after success.
- Add `aria-label` or visible text for icon buttons.
- Restore visible focus indicators; use `:focus-visible`, not `outline: none`.
- Ensure touch target is at least comfortable for tablet use; 28px is likely too small.

---

### P1 — Missing loading, empty, and error states create ambiguous work status

**Source evidence**
- Initial and filter loading render a blank table body.
- Empty results are not represented.
- Autosave status exists only as `saving` boolean in shown snippet.

**Runtime hypothesis**
- Operators may not know whether data is loading, filters returned no results, or the app failed.
- Repeated edits may proceed under stale assumptions.

**Fix**
- Add explicit table-body states:
  - initial loading skeleton/rows;
  - filter loading;
  - empty after filters;
  - empty inventory;
  - recoverable error with retry;
  - auth/permission error;
  - offline mode with queued/unsaved indicator if supported.
- Make autosave status durable enough to show last saved time, failed retry, and unsaved changes.

---

### P1 — Hostile data is not contained

**Source evidence**
- Product names can be 1–200 characters.
- Prices may be missing.
- Translations may expand labels by 60%.
- Images may be absent or 8MB.
- `.product-name` truncates with ellipsis only.
- Grid columns are fixed: `64px 280px 1fr 120px 96px`.

**Runtime hypothesis**
- Long names, missing prices, and expanded labels may hide important operational data.
- Large or missing images may cause layout shifts, slow decode, or broken visual rhythm.
- Internationalized labels may overflow fixed controls.

**Fix**
- Provide title/detail access for truncated product names, preferably through an accessible disclosure or tooltip pattern.
- Define missing price display: em dash, “Not set,” or permission-aware placeholder; avoid ambiguous blank cells.
- Reserve image dimensions and show absent-image placeholder.
- Use thumbnails generated server-side or constrained client-side; avoid rendering raw 8MB images in rows.
- Validate upload size/type before upload, show progress, and handle failure/retry.
- Audit translated strings in controls and drawer footer; allow wrapping where safe.

---

### P2 — Responsive/tablet behavior is brittle

**Source evidence**
- `.page { min-width: 1180px; }`
- Drawer fixed width: `520px`.
- Desktop-first with tablet support required.
- Tablet behavior is not described.

**Runtime hypothesis**
- Tablet users may get horizontal scrolling, clipped drawer content, or unreachable actions.
- A 520px fixed drawer may dominate smaller tablet widths.

**Fix**
- Preserve desktop table density, but define breakpoints:
  - desktop: current multi-column grid/table;
  - tablet landscape: reduce nonessential columns, allow drawer width as `min(520px, 100vw)`;
  - tablet portrait: use horizontal table scroll with sticky key columns or a compact row detail pattern.
- Keep filter and bulk-action bars reachable.
- Ensure drawer height accounts for browser UI and safe areas where relevant.
- Avoid redesigning the whole surface; adapt existing layout tokens and components.

---

### P2 — Motion may harm usability and performance

**Source evidence**
- `.product-row, .drawer { transition: all 300ms ease-in; }`
- Reduced motion support is not described.

**Runtime hypothesis**
- `transition: all` can animate layout-affecting properties unintentionally.
- Row transitions across large lists can amplify rendering cost.
- Motion-sensitive users have no alternate behavior.

**Fix**
- Replace `transition: all` with specific properties, likely `transform`, `opacity`, or color tokens only.
- Avoid per-row transitions for large table updates unless narrowly scoped.
- Use faster, clearer easing for operational UI; avoid slow ease-in for state changes that should feel immediate.
- Add reduced-motion handling that removes transform-heavy animation while preserving state feedback.

---

### P2 — Table semantics and keyboard navigation are not established

**Source evidence**
- Rows render as repeated components in a `div.page`; no table/grid semantics shown.
- Keyboard navigation and screen-reader labels are not described.

**Runtime hypothesis**
- Screen-reader users may not understand row/column relationships.
- Keyboard-heavy operators may lack efficient row navigation, selection, and drawer handoff.

**Fix**
- Use semantic table markup if the layout is tabular, or ARIA grid only if interactive grid behavior is fully implemented.
- Provide column headers, row labels, selection labels, and bulk selection state.
- Define keyboard interactions for:
  - row focus;
  - open drawer;
  - select row;
  - bulk selection;
  - save/cancel in drawer;
  - upload controls.
- Keep focus visible and predictable after filter changes.

---

### P3 — Visual polish issues that should follow hardening

**Source evidence**
- Fixed dense columns.
- Ellipsis-only product names.
- Blank loading body.
- Small icon buttons.
- Generic transitions.

**Runtime hypothesis**
- The UI may feel unstable or unclear during repeated operations.

**Fix**
- Add calm loading placeholders, empty copy, and consistent status badges.
- Improve spacing and hit areas within existing design tokens.
- Add stable image placeholders to prevent row jump.
- Use consistent disabled, saving, failed, and retry states.

---

## 3. Concrete hardening checklist

### Hostile data
- Long names: truncate visually but expose full value accessibly.
- Missing prices: explicit placeholder and validation state.
- Expanded translations: test labels at +60%; allow wrapping in drawer/footer controls.
- Absent images: reserved placeholder.
- 8MB images: validate, compress/thumbnail via existing pipeline, show upload progress and failure.

### Failures
- Represent 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure.
- Do not clear dirty state on failed save.
- Show last successful save time and current unsaved/failed state.
- Make retry idempotent where possible.
- Preserve selected failed rows after partial bulk failure.

### Responsive layout
- Replace hard `min-width: 1180px` as the only strategy with defined desktop/tablet behavior.
- Constrain drawer to viewport: `width: min(520px, 100vw)`.
- Ensure drawer content scrolls internally without hiding footer actions.
- Decide which columns collapse, abbreviate, or move into row details on tablet.

### Accessibility
- Restore focus indicators.
- Add accessible names for icon-only buttons.
- Trap focus/background only if drawer is modal; otherwise document and implement non-modal behavior intentionally.
- Return focus to the opener after drawer close.
- Block or confirm Escape when dirty/saving.
- Add reduced-motion support.
- Ensure row selection and bulk controls are keyboard-operable and announced.

### State recovery
- Track dirty, saving, saved, failed, conflict, unauthorized, offline, and retrying states separately.
- Keep local edits until confirmed saved or intentionally discarded.
- Confirm close on dirty drawer.
- On reload/navigation, warn if unsaved changes exist if that matches product policy.
- For conflicts, fetch latest server version and let the user choose.

### Performance
- Virtualize/window 10,000 rows.
- Memoize filter results.
- Debounce or defer keystroke filtering.
- Avoid full-table re-render for selection and saving changes.
- Reserve image dimensions and lazy-load row thumbnails.
- Avoid `transition: all`, especially on rows.

---

## 4. Static signals: decisive vs context-dependent

### Decisive from the supplied source
- `catch {}` is a production correctness risk.
- Blank loading/empty/error states are insufficient for this workflow.
- Rendering 10,000 rows with `.map()` is a clear scalability risk.
- Synchronous filtering on every keystroke is a likely input-latency risk.
- `outline: none` without replacement is an accessibility failure.
- Icon-only save/close need accessible names and clear affordance.
- No focus trap/background strategy for the drawer is unsafe if modal behavior is intended.
- Escape close while saving is unsafe without explicit recovery policy.
- `transition: all` is too broad and risky.
- Fixed `min-width: 1180px` conflicts with tablet support unless paired with a deliberate overflow/adaptive strategy.
- Unreserved image dimensions can cause layout shift.

### Needs project/runtime context
- Exact frame rate, input latency, memory use, and long-task severity.
- Whether existing components already provide labels, table semantics, or focus management outside the snippet.
- Whether the drawer is intended to be modal or non-modal.
- Whether backend supports conflict resolution, idempotency keys, upload preprocessing, and partial-failure details.
- Whether current design tokens already define focus, motion, disabled, and status patterns.
- Whether virtualization can preserve current row height, sticky headers, bulk selection, and keyboard behavior without regressions.
- Actual tablet breakpoints and supported devices.
- Exact severity of image performance, depending on CDN thumbnails and cache behavior.

---

## 5. Measurement-first validation plan

### Baseline before changes
- Record static inventory route scenarios:
  - initial load;
  - filter typing;
  - open drawer;
  - edit/save success;
  - save failure;
  - conflict;
  - unauthorized;
  - offline/timeout;
  - image missing/large image;
  - 10,000-row bulk selection.
- Capture target metrics:
  - keystroke-to-filter response;
  - time to first usable table;
  - row render count on selection/save;
  - drawer open/close responsiveness;
  - layout shift from images;
  - save failure visibility;
  - keyboard path completion.

### Acceptance conditions
- No silent save failures.
- Failed save preserves edits and shows actionable recovery.
- Conflict state is visible and does not overwrite blindly.
- Dirty or saving drawer cannot be accidentally dismissed without policy.
- Loading, empty, auth, offline, timeout, 429, 500, and partial batch states are represented.
- 10,000-row interaction remains responsive under defined product thresholds.
- Filtering does not block typing under expected data scale.
- Keyboard-only user can filter, select, open drawer, edit, save, handle failure, and return focus.
- Icon-only controls have accessible names.
- Focus indicator is visible.
- Reduced-motion mode keeps state feedback without unnecessary animation.
- Tablet layout remains usable without hidden primary actions.

### Rollback conditions
- Virtualization breaks selection, row height, sticky headers, or screen-reader/keyboard behavior.
- Error handling introduces duplicate saves or lost edits.
- Conflict handling blocks normal successful saves.
- Responsive changes reduce desktop operator efficiency.
- Motion changes remove necessary state feedback.
- Upload handling prevents valid existing workflows.

### Release approach
- Ship in small hardening slices:
  1. save/error/state recovery;
  2. drawer accessibility and close policy;
  3. loading/empty/auth/offline states;
  4. row/filter performance;
  5. tablet and motion polish.
- Keep each slice behind a reversible implementation path where practical.
- Preserve the existing design system, density, and workflow; this is hardening, not a new inventory experience.
