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
