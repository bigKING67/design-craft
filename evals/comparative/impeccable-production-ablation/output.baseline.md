## 1) Sequencing + verdict

**Correct sequence:** audit static risks → harden data/failure/state recovery → fix accessibility blockers → optimize 10,000-row hot paths → add responsive/tablet polish → tune motion and visual states → validate with measurements and rollback gates.

**One-line verdict:** This surface is not production-ready for operations use as described; the main risks are silent save failure, inaccessible drawer/actions, missing recovery states, and unbounded rendering/filtering at 10,000 rows.

---

## 2) Prioritized findings

### P0 — Silent data loss / false save success

**Source evidence**
- `catch {}` swallows save failures.
- `setSaving(false)` runs after failure with no error state.
- Notes say 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.
- Escape closes drawer even while save is pending.

**Runtime hypotheses**
- Operators may believe edits were saved when they were not.
- Closing during pending save may discard unsaved or ambiguous state.
- Conflicts may overwrite newer product data or leave stale drawer contents.

**Fix**
- Replace boolean-only `saving` with explicit save state: `idle | dirty | saving | saved | error | conflict | offline | retrying`.
- Never swallow save errors. Surface actionable copy near the save control and in autosave status.
- Block close during critical save or require confirmation: “Save still in progress. Keep editing / discard changes.”
- Add 409 conflict handling with “reload latest / compare / keep local draft” behavior.
- Add retry policy for transient 429/500/timeout/offline with bounded retries and clear final failure.
- Preserve dirty draft until confirmed saved.

---

### P0 — Drawer interaction is not safely accessible

**Source evidence**
- Drawer traps neither focus nor background interaction.
- Escape closes it even while save is pending.
- Save and close are icon-only.
- `.icon-button { width: 28px; height: 28px; outline: none; }`
- Keyboard navigation, screen-reader labels, and focus-visible are not described.

**Runtime hypotheses**
- Keyboard and screen-reader users can tab behind the drawer, lose context, or trigger background controls.
- Icon-only controls may be announced without useful names.
- Removing outline may make focus location invisible.

**Fix**
- Make drawer modal semantics explicit when open: focus moves into drawer, background is inert/unavailable, focus restores to opener on close.
- Add accessible names for icon buttons: “Save product”, “Close editor”, etc.
- Use `:focus-visible` styling instead of removing outlines.
- Ensure Escape behavior respects dirty/saving state.
- Provide keyboard order matching visual order: drawer title → fields → upload → save/status → close/cancel.
- Add disabled and busy states with accessible announcements for save progress and result.

---

### P1 — Unbounded rendering and synchronous filtering threaten operability

**Source evidence**
- All 10,000 rows render at once.
- `rows.map((row) => <ProductRow ... />)` renders every row.
- Filtering recalculates synchronously on every keystroke.
- Image dimensions are not reserved.

**Runtime hypotheses**
- Keystrokes may lag.
- Bulk selection may cause large re-renders.
- Scroll may jank.
- Images may cause layout shift and repeated repainting.

**Fix**
- Virtualize the product table or window visible rows while preserving keyboard access and selection semantics.
- Debounce or defer filter input work; keep input responsive while recalculating results.
- Memoize filtered rows and expensive cell formatting with correct dependencies.
- Avoid passing unstable props that re-render every row on unrelated save state changes.
- Separate global save state from row rendering where possible.
- Reserve image dimensions; use placeholders for absent images and lazy/deferred loading for offscreen images.
- Keep bulk selection state represented compactly, not by mutating every row object on each toggle.

---

### P1 — Missing production failure and permission states

**Source evidence**
- Initial and filter loading render a blank table body.
- Empty results are not represented.
- 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.
- Permission-specific affordances are not described.

**Runtime hypotheses**
- Blank body may be mistaken for empty inventory or broken data.
- Users may attempt unauthorized edits and only discover failure after work is done.
- Partial batch failures may leave selection and edited rows ambiguous.

**Fix**
- Add distinct states:
  - initial loading skeleton or progress state,
  - filter loading state that preserves previous results if possible,
  - empty filtered state with clear reset action,
  - unauthorized/forbidden state with role-specific copy,
  - conflict state,
  - rate-limit state with retry timing,
  - offline state,
  - partial batch result summary.
- Disable or hide edit/bulk actions based on permissions, but keep explanations available.
- For batch operations, report counts: succeeded, failed, skipped, needs review.

---

### P1 — State recovery is under-specified for an autosave editor

**Source evidence**
- Only `saving` boolean is modeled.
- Autosave status exists in product context, but source only shows `saving`.
- Failure, conflict, offline, retry, and partial batch states are absent.
- Drawer can close while pending.

**Runtime hypotheses**
- Autosave may race with later edits.
- A slower save response may overwrite a newer local change.
- Reload/navigation may discard drafts.

**Fix**
- Track per-product draft version, dirty fields, last saved timestamp, and pending request id.
- Ignore stale save responses that do not match the current draft version.
- Persist local draft during network loss or navigation risk.
- Add navigation/close guards for dirty or saving states.
- Show status with specific meaning: “Unsaved changes”, “Saving…”, “Saved 10:42”, “Couldn’t save”, “Conflict”.
- Provide retry and discard paths.

---

### P2 — Hostile data cases will break layout clarity

**Source evidence**
- Product names may be 1–200 characters.
- Prices may be missing.
- Translations may expand labels by 60%.
- Some images are absent or 8MB.
- `.product-name` truncates with ellipsis.
- Fixed grid columns: `64px 280px 1fr 120px 96px`.

**Runtime hypotheses**
- Long names may hide distinguishing SKU details.
- Missing prices may appear as zero or blank if not explicitly handled.
- Expanded labels may overflow fixed controls.
- Large images may slow upload preview and consume memory.

**Fix**
- Define display rules for long product names: preserve key identifiers, add accessible full-name exposure, avoid relying only on hover.
- Render missing price as an explicit placeholder such as “No price” or “—” with consistent sorting behavior.
- Reserve image boxes and show absent-image placeholders.
- Validate image size/type before upload; provide compression/resizing guidance if supported by existing stack.
- Add upload failure states for too large, unsupported type, timeout, and retry.
- Test copy expansion by allowing labels/buttons to wrap or use wider adaptive containers.

---

### P2 — Fixed desktop layout blocks tablet support

**Source evidence**
- `.page { min-width: 1180px; }`
- Drawer fixed at `width: 520px; height: 100vh;`
- Tablet behavior is not described.

**Runtime hypotheses**
- Tablet users may get forced horizontal scrolling, clipped drawer content, or inaccessible actions.
- Fixed drawer may cover too much of the table and obscure context.

**Fix**
- Preserve desktop workflow but add tablet breakpoints.
- Use `width: min(520px, 100vw)` or equivalent for the drawer.
- Ensure drawer content scrolls internally without trapping controls below the viewport.
- Keep table usable on narrower screens through controlled horizontal scroll, sticky key columns, or reduced secondary columns.
- Maintain touch target sizes larger than the current 28px icon buttons.
- Avoid redesigning the workflow; adapt the existing table/drawer pattern.

---

### P2 — Motion is broad and may animate expensive properties

**Source evidence**
- `.product-row, .drawer { transition: all 300ms ease-in; }`
- Reduced motion is not described.

**Runtime hypotheses**
- `transition: all` can animate layout-affecting properties and cause jank.
- Rows may animate unexpectedly during filtering or selection.
- Motion may be uncomfortable for reduced-motion users.

**Fix**
- Replace `transition: all` with explicit properties, usually `transform`, `opacity`, `background-color`, or `box-shadow` only where needed.
- Use reduced-motion media query to remove or shorten nonessential transitions while preserving state feedback.
- Avoid animating 10,000 row-level elements during filter, sort, or bulk selection.
- Use direct, short drawer motion that does not block input.

---

### P3 — Visual polish gaps reduce operator confidence

**Source evidence**
- Blank loading body.
- Icon-only save/close.
- Truncation without described full-value access.
- No disabled, error, empty, or partial states described.

**Runtime hypotheses**
- Operators may pause because they cannot tell whether the app is loading, empty, broken, or unauthorized.
- Repeated use may feel brittle even if core data eventually saves.

**Fix**
- Add calm, low-noise status areas rather than modal-heavy interruptions.
- Keep row density, table structure, and existing workflow.
- Use consistent inline affordances for warnings, missing data, upload state, and autosave state.
- Add acceptance copy for every non-happy path.

---

## 3) Concrete fixes by concern

### Hostile data
- Long names: clamp visually but expose full text accessibly; preserve SKU/identifier visibility.
- Missing prices: explicit placeholder and sort/filter behavior.
- Translations: allow labels/buttons to expand; avoid fixed text containers where possible.
- Missing images: reserved placeholder slot.
- 8MB images: pre-upload validation, progress, failure, retry, and memory-safe preview handling.

### Failures
- Replace blank body with loading, empty, error, unauthorized, offline, conflict, rate-limit, and retry states.
- For batch operations, show partial success with row-level recovery.
- Use typed error states rather than generic failure copy.
- Do not clear pending edits on failed save.

### Responsive layout
- Keep desktop-first table/drawer.
- Add tablet breakpoint behavior.
- Constrain drawer with viewport-aware width.
- Make drawer body scrollable and actions persistent.
- Avoid global `min-width: 1180px` as the only tablet strategy.

### Accessibility
- Restore visible focus using `:focus-visible`.
- Add labels to icon-only buttons.
- Implement drawer focus trap, inert background, focus return, and semantic title.
- Respect reduced motion.
- Define keyboard navigation for rows, selection, drawer open/close, save, upload, and filters.
- Ensure busy/error/save status is announced without stealing focus.

### State recovery
- Model dirty/saving/saved/error/conflict/offline states.
- Preserve drafts across failed saves and unsafe close.
- Guard close/navigation during pending or dirty edits.
- Make autosave ordering safe against stale responses.
- Provide explicit retry/discard/reload paths.

### Performance
- Virtualize/window 10,000 rows.
- Defer/debounce filtering; keep input responsive.
- Memoize derived rows and stable row props.
- Avoid row-wide re-render on global saving state.
- Reserve image dimensions and lazy-load offscreen media.
- Avoid animating all row properties.

---

## 4) Static detector-like signals: decisive vs needs context

### Decisive from provided source
- `catch {}` is a production hardening blocker for save reliability.
- `outline: none` without an alternative focus style is an accessibility risk.
- Icon-only save/close without labels is an accessibility risk.
- No drawer focus trap/background blocking is a modal accessibility blocker.
- `transition: all` is unsafe for predictable motion/performance.
- Rendering `rows.map` over 10,000 rows is a hot-path risk.
- Synchronous filtering on each keystroke is a responsiveness risk.
- Blank loading table body is an incomplete state.
- Missing represented states for auth, conflict, rate-limit, offline, retry, and partial failure are production gaps.
- Fixed `min-width: 1180px` conflicts with tablet support unless paired with a deliberate overflow/adaptive strategy.

### Needs project/runtime context
- Exact severity of scroll jank and input latency.
- Whether child components already memoize expensive cells.
- Whether a global CSS layer restores focus styles elsewhere.
- Whether table semantics, labels, and keyboard behavior exist inside omitted components.
- Actual API guarantees for save ordering, idempotency, retries, and conflicts.
- Image pipeline behavior: CDN resizing, client compression, upload limits, preview memory use.
- Permission model and whether unauthorized actions are prevented server-side.
- Tablet impact across actual target viewport sizes and browser/device mix.

---

## 5) Measurement-first validation plan with rollback/acceptance gates

### Baseline before changes
- Record static state inventory: loading, empty, error, offline, conflict, permission denied, partial batch, dirty, saving, saved.
- Measure current interaction budgets in the app environment:
  - initial table render,
  - filter keystroke responsiveness,
  - scroll smoothness,
  - drawer open/close,
  - save success/failure paths,
  - image upload preview.
- Capture accessibility checks for keyboard-only drawer use, focus visibility, labels, Escape behavior, and reduced motion.

### Acceptance conditions
- Failed save never appears as saved.
- Dirty edits survive save failure, offline, retry, and blocked close.
- 409 conflict has a visible recovery path.
- Drawer traps focus, restores focus, labels icon controls, blocks background interaction, and handles Escape safely.
- Filtering remains responsive at 10,000 rows.
- Scrolling remains usable with images and selection enabled.
- Loading, empty, auth, conflict, rate-limit, server error, timeout, offline, retry, and partial batch states are visible and distinct.
- Tablet viewport has no clipped critical controls.
- Reduced-motion mode preserves state feedback without unnecessary animation.

### Rollback conditions
- Any change increases risk of data loss or ambiguous save state.
- Virtualization breaks keyboard navigation, selection persistence, or screen-reader row context.
- Responsive changes disrupt the established desktop workflow.
- Error handling blocks legitimate saves without a clear recovery path.
- Motion changes introduce layout jank or hide state changes.

### Validation order
1. Save/error/conflict/offline recovery.
2. Drawer accessibility and close behavior.
3. 10,000-row render/filter/scroll performance.
4. Hostile data and upload cases.
5. Tablet layout and reduced motion.
6. Final regression pass across permissions, bulk selection, autosave, and drawer editing.
