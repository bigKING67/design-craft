## 1. Sequence + verdict

**Correct sequence:** audit current behavior → harden data/failure/state paths → fix accessibility and keyboard safety → optimize 10,000-row rendering/filtering/images → polish motion/responsive/tablet states within the existing system.

**One-line verdict:** This surface is not production-ready for operations use yet; the core structure is salvageable, but save reliability, failure visibility, accessibility, and large-table performance need hardening before polish.

---

## 2. Prioritized findings

### P0 — Silent save failure can cause data loss or false confidence

**Source evidence**
- `catch {}` swallows all save failures.
- `saving` is a single global boolean, not tied to product, request id, drawer state, or dirty draft.
- No represented states for `409`, `429`, `500`, timeout, offline, retry, or partial batch failure.
- Escape closes the drawer even while save is pending.

**Runtime hypotheses**
- Operators may believe edits were saved when they were not.
- Concurrent saves may race: one save finishing can set `saving` false while another is still pending.
- Closing during save may lose unsaved edits or hide the only place where the error would have been recoverable.

**Concrete fix**
- Replace `saving: boolean` with explicit save state: `idle | dirty | saving | saved | failed | conflict | offline`.
- Use `try/catch/finally`, store the actual error, and surface it near the save action and in autosave status.
- Block destructive close during pending save, or require confirmation while preserving the draft.
- Add request/version guards so stale save responses cannot overwrite newer state.
- Handle `409` with conflict recovery: show server version, local draft, and retry/merge path.
- Handle batch saves with per-row success/failure reporting, not one global success state.

---

### P0 — Drawer accessibility and keyboard safety are blocking issues

**Source evidence**
- Drawer traps neither focus nor background interaction.
- Escape closes it even while save is pending.
- Save and close are icon-only.
- `.icon-button { outline: none; }`
- Screen-reader labels, keyboard navigation, and focus-visible are not described.

**Runtime hypotheses**
- Keyboard users can tab into obscured background content.
- Screen-reader users may not know what save/close buttons do.
- Removing outlines can make the active control invisible.
- Escape may accidentally discard or interrupt an in-flight operation.

**Concrete fix**
- Make drawer a modal/dialog pattern when open: labelled title, focus sent into drawer, focus restored on close, background inert/blocked.
- Add accessible names to icon-only controls: visible text where possible, otherwise `aria-label`.
- Restore visible focus using `:focus-visible`; never remove focus indication without replacement.
- Define Escape behavior:
  - no dirty state: close;
  - dirty state: confirm;
  - saving state: do not close, or show “Save in progress” with cancel only if cancellation is safe.
- Ensure save/close buttons expose disabled/busy states correctly.

---

### P1 — 10,000 rows rendered synchronously is a production performance risk

**Source evidence**
- `{rows.map((row) => <ProductRow ... />)}` renders all rows.
- Route has a 10,000-row product table.
- Filtering recalculates synchronously on every keystroke.
- Image dimensions are not reserved.

**Runtime hypotheses**
- Initial render, filtering, selection, and drawer edits may block input.
- Every filter keystroke can re-render thousands of rows.
- Unreserved images can cause layout shifts as thumbnails load.
- Bulk selection can churn row props and trigger excessive updates.

**Concrete fix**
- Virtualize the table body or paginate/window rows while preserving keyboard navigation and selection semantics.
- Memoize filtered/sorted rows with correct dependencies.
- Debounce or defer filter input work so typing remains responsive.
- Keep selection state in a structure that does not recreate every row unnecessarily.
- Memoize `ProductRow` where props are stable.
- Reserve image boxes with fixed dimensions/aspect ratio and use placeholders for missing images.
- Avoid loading full 8MB images into row thumbnails; use thumbnails or constrained previews.

---

### P1 — Loading and failure states are blank or absent

**Source evidence**
- Initial and filter loading render a blank table body.
- Empty results are not represented.
- `401/403`, `429`, `500`, timeout, offline, retry are not represented.

**Runtime hypotheses**
- Operators may interpret blank content as “no products,” broken filters, or a frozen page.
- Permission errors may look like data loss.
- Rate limits/server failures may trigger repeated user actions, worsening load.

**Concrete fix**
- Add distinct table states:
  - initial loading;
  - filtering/loading;
  - empty results;
  - permission denied;
  - unauthenticated/session expired;
  - server error;
  - rate limited;
  - offline;
  - timeout with retry.
- Keep table headers and layout stable while body state changes.
- Use inline recovery actions: retry, clear filters, reconnect, sign in again, request access.
- Preserve current filters and edits across transient failures.

---

### P1 — Responsive layout is desktop-locked and tablet behavior is undefined

**Source evidence**
- `.page { min-width: 1180px; }`
- Fixed drawer width: `520px`.
- Product row uses fixed columns: `64px 280px 1fr 120px 96px`.
- Tablet behavior is not described.

**Runtime hypotheses**
- Tablet users may get horizontal clipping, hidden actions, or an unusable drawer.
- A fixed 520px drawer can consume too much tablet width.
- Expanded translations can break fixed columns.

**Concrete fix**
- Preserve the desktop table but define tablet breakpoints.
- Allow the page container to adapt instead of relying only on global `min-width`.
- For tablets, choose one supported behavior:
  - horizontal table scroll with sticky key columns/actions; or
  - condensed row layout with secondary fields collapsed.
- Make drawer width responsive: `min(520px, 100vw)` or design-system equivalent.
- Ensure drawer does not cover critical controls without an obvious close/return path.
- Test long labels and 60% translation expansion in filters, drawer labels, buttons, and headers.

---

### P2 — Hostile product data is not safely represented

**Source evidence**
- Product names may be 1–200 characters.
- Prices may be missing.
- Some images are absent or 8MB.
- Translations may expand labels by 60%.
- `.product-name` truncates with ellipsis.

**Runtime hypotheses**
- Ellipsis alone may hide the distinguishing part of similar product names.
- Missing prices may look like zero or failed rendering.
- Large images may delay row rendering and increase memory pressure.
- Long translations can overflow controls or hide affordances.

**Concrete fix**
- Keep ellipsis, but provide access to full names through accessible title/detail affordance where appropriate.
- Use stable fallbacks:
  - missing price: “No price” / “—” with clear semantics;
  - absent image: neutral placeholder;
  - failed image: retry/fallback state.
- Reserve image dimensions and validate upload size/type before attempting upload.
- Add upload progress, failure, retry, and oversized-file messaging.
- Ensure translated labels wrap or truncate intentionally without hiding required actions.
- Avoid using color alone for missing/invalid data.

---

### P2 — Motion implementation is too broad and may cause jank

**Source evidence**
- `.product-row, .drawer { transition: all 300ms ease-in; }`
- Reduced motion behavior is not described.

**Runtime hypotheses**
- `transition: all` may animate layout-affecting properties and degrade responsiveness.
- Row transitions across many rows can be expensive.
- Ease-in can feel sluggish for drawer entry because it starts slowly.
- Motion-sensitive users have no stated reduced-motion path.

**Concrete fix**
- Limit transitions to intended properties, usually `transform`, `opacity`, or design-system-safe tokens.
- Avoid animating every row during filter/table changes.
- Add reduced-motion handling that removes or shortens nonessential motion while preserving state feedback.
- Use motion to clarify drawer open/close and autosave status, not as a blanket effect.

---

### P2 — Permission-specific affordances are missing

**Source evidence**
- Permission-specific affordances are not described.
- `401/403` states are absent.
- Bulk selection, edit drawer, image uploads, and autosave imply multiple permission boundaries.

**Runtime hypotheses**
- Users may see controls they cannot use.
- Save/upload failures may be misread as network problems instead of access denial.
- Bulk actions may allow selection before failing at commit time.

**Concrete fix**
- Gate controls by capability: view, edit, upload image, bulk edit, approve/publish if relevant.
- Show disabled states with reasons, not silent removal for discoverability where appropriate.
- Represent permission errors separately from generic failures.
- Prevent impossible actions before the user spends time editing.

---

### P3 — State continuity and autosave feedback need polish

**Source evidence**
- Autosave status exists in product context, but snippet only exposes `saving`.
- Blank loading and missing failure states imply weak continuity.

**Runtime hypotheses**
- Operators doing repeated edits may not know whether they are editing saved, dirty, failed, or stale data.
- Navigation/filter changes may discard local intent.

**Concrete fix**
- Show precise autosave status: saved time, saving, failed, offline queued, conflict.
- Preserve drawer draft across transient reloads where safe.
- Warn before losing dirty edits on filter changes, route changes, drawer close, or permission/session interruption.
- Keep selected rows stable when filters change, with clear messaging about hidden selected items.

---

## 3. Concrete production hardening by area

### Hostile data
- Long names: truncate visually, preserve full value accessibly.
- Missing prices: explicit placeholder, not empty cell.
- Missing images: stable placeholder.
- Large images: client-side validation, upload progress, thumbnail generation/server thumbnail use.
- Translations: allow wrapping/truncation by component, not accidental overflow.
- Bulk actions: summarize affected/failed rows with row-level details.

### Failures
- Replace blank/errorless paths with typed states.
- Map common failures:
  - `401`: session recovery;
  - `403`: no permission;
  - `409`: conflict resolution;
  - `429`: backoff/retry later;
  - `500`: retry/report;
  - timeout/offline: retry and preserve draft.
- Never swallow save/upload failures.
- Partial batch failure must be first-class.

### Responsive layout
- Keep desktop-first table.
- Add tablet-specific behavior instead of relying on `min-width: 1180px`.
- Make drawer width viewport-safe.
- Maintain sticky headers/actions where horizontal scrolling is used.
- Ensure touch targets are not stuck at 28px on tablet.

### Accessibility
- Modal drawer semantics, focus trap, inert background, focus restoration.
- Accessible names for icon-only controls.
- Visible `:focus-visible`.
- Keyboard navigation for rows, selection, filters, drawer actions, and bulk operations.
- Announce save status changes through an appropriate live region.
- Do not close pending/dirty work on Escape without safe handling.
- Reduced-motion support.

### State recovery
- Preserve dirty draft on save failure, offline, timeout, and conflict.
- Distinguish saved server state from local draft.
- Guard against stale save responses.
- Confirm or prevent destructive close/navigation.
- Restore filters/selection/drawer context after recoverable failures.

### Performance
- Virtualize/window 10,000-row rendering.
- Memoize filtering/sorting and row rendering.
- Defer/debounce filter recalculation.
- Reserve image dimensions.
- Avoid `transition: all`.
- Keep bulk selection updates localized.
- Avoid loading full-size images in table rows.

---

## 4. Static signals: decisive vs needing runtime context

### Decisive from static facts
- `catch {}` is unacceptable for production save behavior.
- Rendering 10,000 rows with direct `.map()` is a major scalability risk.
- Blank loading/error states are insufficient for an operations tool.
- No focus trap/background inertness in a fixed drawer is an accessibility defect.
- Icon-only save/close without labels is an accessibility defect.
- `outline: none` without replacement is an accessibility defect.
- `transition: all` is unsafe for performance and motion quality.
- Fixed `min-width: 1180px` plus fixed drawer width needs explicit tablet handling.
- Missing conflict/offline/timeout/partial failure states are hardening gaps.

### Needs project/runtime context
- Exact row virtualization strategy: depends on table semantics, sticky columns, row heights, and keyboard model.
- Whether 28px icon buttons fail target-size requirements in the actual density system.
- Actual render cost of each `ProductRow`.
- Actual filtering latency and whether work is CPU, network, or state-management bound.
- Whether image uploads are client-resized, server-transformed, cached, or already thumbnailed.
- Whether the drawer should be modal or non-modal in the broader workflow; current facts still require focus/background rules.
- Exact responsive breakpoint behavior, because the design system may already define tablet patterns.
- The best conflict-resolution UI, because it depends on backend versioning and edit granularity.

---

## 5. Measurement-first validation plan

### Baseline before changes
- Record current behavior for:
  - initial load with 10,000 rows;
  - filter typing latency;
  - row selection and bulk selection;
  - drawer open/save/close;
  - image-heavy rows;
  - failed save;
  - offline/timeout/conflict scenarios if they can be simulated in the app layer.
- Capture interaction timings and visible layout stability for table and drawer flows.
- Inventory current keyboard path and focus order from filters → table → drawer → bulk actions.

### Acceptance conditions
- Save failures are visible, recoverable, and never reported as success.
- Dirty edits survive failed save, timeout, offline, and conflict paths.
- Pending save cannot be accidentally hidden or discarded by Escape/close.
- Initial, loading, empty, permission, conflict, retry, offline, and partial batch states are represented.
- 10,000-row route remains responsive during typing, selection, drawer open, and save status updates.
- Images do not cause meaningful layout shift in table rows.
- Drawer has correct focus containment/restoration and labelled controls.
- Keyboard users can complete filter, select, edit, save, and close flows.
- Reduced-motion users receive non-disorienting state changes.
- Tablet layout has an intentional supported behavior.

### Rollback conditions
- Virtualization breaks keyboard navigation, selection persistence, sticky headers, or screen-reader semantics.
- Save-state changes hide errors or make conflict recovery harder.
- Responsive changes reduce desktop operator efficiency.
- Motion changes remove necessary state feedback.
- Image optimizations degrade upload reliability or obscure missing/failed image states.
- Permission gating hides required context instead of explaining unavailable actions.

### Release approach
- Ship hardening in narrow slices:
  1. save/error/state recovery;
  2. drawer accessibility;
  3. table performance;
  4. hostile data/image handling;
  5. tablet/responsive polish;
  6. motion cleanup.
- Keep each slice reversible.
- Use production-like row counts and hostile data fixtures before accepting the optimization and polish work.
