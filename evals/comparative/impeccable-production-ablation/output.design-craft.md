## 1) Sequence and verdict

**Correct sequence:** audit static evidence → harden data integrity/failure recovery/accessibility blockers → establish runtime baselines → optimize only proven hot paths → polish motion/responsive details without changing the workflow.

**One-line verdict:** The surface has the right inventory-editor shape, but it is **not production-ready for 10,000-row operations use** until save failure visibility, drawer safety, failure states, accessibility, hostile data, and table performance are hardened.

---

## 2) Prioritized findings

### P0 — Silent save failure and unsafe state recovery

**Source evidence**
- `catch {}` swallows save failures.
- `setSaving(false)` is not in `finally`.
- `saving` is a single page-level boolean, not per product/batch/request.
- Notes say 409 conflict, timeout, offline, retry, and partial batch failure states are not represented.
- Drawer can close with Escape while a save is pending.

**Runtime hypothesis / risk**
- Operators can believe changes were saved when they were not.
- Concurrent saves may race: one request can clear `saving` while another is still pending.
- Conflict resolution and autosave trust are undefined.

**Production impact**
- Data loss, duplicate work, incorrect inventory records, and low operator trust.

---

### P0 — Drawer is not a safe modal editing surface

**Source evidence**
- Drawer traps neither focus nor background interaction.
- Escape closes it even while save is pending.
- Save and close are icon-only.
- `.drawer { position: fixed; right: 0; width: 520px; height: 100vh; }`

**Runtime hypothesis / risk**
- Keyboard and screen-reader users can tab into the table behind the drawer.
- Users can accidentally close or mutate background state during an edit.
- Pending edits may be lost or become ambiguous.

**Production impact**
- Accessibility blocker and workflow-safety blocker for the primary edit task.

---

### P0 — 10,000-row rendering and filtering are structurally unbounded

**Source evidence**
- `{rows.map((row) => <ProductRow ... />)}` renders every row.
- Notes say all 10,000 rows render at once.
- Notes say filtering recalculates synchronously on every keystroke.
- Image dimensions are not reserved.

**Runtime hypothesis / risk**
- Actual frame rate, memory, and input latency require profiling, but the static shape is already an unbounded hot path.
- Large or missing images can worsen layout shift and scroll instability.

**Production impact**
- Filtering, bulk selection, scrolling, and drawer edits may feel unreliable at stated scale.

---

### P1 — Missing production failure-state coverage

**Source evidence**
- Initial and filter loading render a blank table body.
- Empty results, 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are absent.

**Runtime hypothesis / risk**
- Operators cannot distinguish loading from empty, unauthorized, failed, rate-limited, stale, or partially applied states.

**Production impact**
- Support burden rises; users retry blindly; partial failures can corrupt operational intent.

---

### P1 — Responsive/tablet behavior is not production-specified

**Source evidence**
- `.page { min-width: 1180px; }`
- `.drawer { width: 520px; }`
- Tablet behavior is not described.

**Runtime hypothesis / risk**
- On tablet-width viewports, the fixed page width plus fixed drawer can force horizontal scrolling, clipped controls, or unreachable table columns.
- Whether an outer shell compensates is unknown from the snippet.

**Production impact**
- Tablet support is currently a claim, not a verified contract.

---

### P1 — Hostile data is under-modeled

**Source evidence**
- Product names can be 1–200 characters.
- `.product-name` uses single-line truncation.
- Prices may be missing.
- Translations may expand labels by 60%.
- Images may be absent or 8MB.

**Runtime hypothesis / risk**
- Truncation may hide the only distinguishing product text.
- Missing prices may be confused with zero or loading.
- Expanded labels can break fixed columns/buttons.
- 8MB images can delay edits/uploads without progress or compression.

**Production impact**
- Operators may edit the wrong item or lose confidence in row state.

---

### P1 — Accessibility contract is incomplete

**Source evidence**
- `.icon-button { width: 28px; height: 28px; outline: none; }`
- Save and close are icon-only.
- Keyboard navigation, screen-reader labels, focus-visible, and permission-specific affordances are not described.

**Runtime hypothesis / risk**
- `outline: none` may be compensated elsewhere, but no replacement focus style is shown.
- 28px controls are likely too small for tablet comfort unless another hit area exists.
- Table semantics, bulk-selection labels, and autosave announcements are unknown.

**Production impact**
- Keyboard-heavy operations users lose speed and confidence; assistive technology support is likely incomplete.

---

### P2 — Motion implementation is broad and potentially disruptive

**Source evidence**
- `.product-row, .drawer { transition: all 300ms ease-in; }`
- Reduced motion is not described.

**Runtime hypothesis / risk**
- `transition: all` can animate layout, color, width, height, or other accidental properties.
- `ease-in` can feel sluggish for entrance/opening transitions.
- Actual jank requires runtime validation.

**Production impact**
- Motion may reduce perceived responsiveness in a dense operations workflow.

---

### P2 — Permission-specific affordances are absent

**Source evidence**
- Permission-specific affordances are not described.
- 401/403 states are absent.

**Runtime hypothesis / risk**
- Users may see controls they cannot use, or errors only after attempting an action.

**Production impact**
- Avoidable failed actions and unclear responsibility boundaries.

---

### P3 — Polish gaps reduce operational clarity

**Source evidence**
- Blank loading body.
- Icon-only primary drawer actions.
- Global `saving` boolean.
- Single-line truncation without described reveal path.

**Runtime hypothesis / risk**
- The UI may look visually calm but fail to communicate enough state during repeated work.

**Production impact**
- Lower scannability, more hesitation, more support tickets.

---

## 3) Concrete fixes

### Data integrity and save recovery

- Replace `catch {}` with typed error handling and user-visible outcomes.
- Use `try/catch/finally` so pending state always resolves when the request settles.
- Track save state by product/request, not only one global `saving` boolean.
- Add request IDs or version tokens so stale responses cannot overwrite newer edits.
- Represent autosave states explicitly: `idle`, `dirty`, `saving`, `saved`, `failed`, `conflict`, `offline`, `retrying`.
- Block, confirm, or defer drawer close while a save is pending or dirty.
- Add 409 conflict handling: compare server version, show conflicting fields, allow reload/merge/retry.
- Add retry with backoff for timeout/429/offline where safe; never retry non-idempotent writes without an idempotency key.
- Preserve drafts locally during network loss, route changes, and drawer close attempts.

### Failure states

- Initial load: show skeleton or structured loading rows, not a blank body.
- Filter load: preserve previous rows with a “updating results” state, or show a scoped loading state.
- Empty results: show filter-aware empty copy and clear-filter action.
- 401/403: show session/permission state with no destructive controls.
- 429: show rate-limit explanation and retry timing if available.
- 500/timeout/offline: show recoverable error, retry, and unsaved-change preservation.
- Partial batch failure: show batch summary, failed row list, retry failed only, and export/copy diagnostics if appropriate.

### Hostile data

- Product names: preserve row density, but provide an accessible full-name reveal via cell expansion, tooltip/popover, or drawer detail.
- Missing prices: render a distinct placeholder such as “—”/“Not set”; never conflate with zero.
- Long translations: avoid fixed-label assumptions; allow buttons and form labels to wrap or use minmax layouts.
- Images: reserve dimensions, use placeholders for missing assets, lazy-load thumbnails, validate size/type, compress or resize before upload when allowed, and show upload progress/failure/retry.
- Ensure row identity remains visible when text truncates: SKU/image/name should not all disappear or collapse at once.

### Responsive layout

- Replace global `min-width: 1180px` as the only layout strategy with a responsive shell.
- Keep desktop density, but define tablet behavior explicitly:
  - horizontal table scroll with sticky key columns, or
  - column-priority hiding with drawer detail, if already consistent with the system.
- Use drawer width like `clamp(360px, 42vw, 520px)` or a tablet-specific full-width/near-full-width drawer.
- Ensure drawer plus table never makes primary actions unreachable.
- Reserve safe spacing for touch targets without making the desktop table overly loose.

### Accessibility

- Treat the drawer as a modal editing surface when open:
  - `role="dialog"` or equivalent semantic structure,
  - accessible title,
  - focus moves into drawer on open,
  - focus trap while open,
  - background inert/disabled,
  - focus returns to the invoking row/control on close.
- Save/close icon buttons need accessible names; consider visible text where the workflow needs clarity.
- Restore visible focus styling; do not rely on `outline: none` without a replacement.
- Define keyboard row navigation, selection behavior, and drawer shortcuts.
- Announce autosave changes through an appropriate live region.
- Do not let Escape discard pending/dirty work without confirmation.
- Add reduced-motion handling that preserves state feedback without large transitions.

### Performance

- Virtualize the table or otherwise window rendered rows; keep selection and focus stable across virtualization.
- Memoize filtered results with correct dependencies.
- Debounce or defer filter input work so typing remains responsive.
- Use stable row props/callbacks and memoized row components where useful.
- Move very heavy filtering/search transforms to a worker only if measurement shows main-thread pressure remains.
- Reserve image dimensions and lazy-load thumbnails.
- Replace `transition: all` with specific properties, preferably `transform` and `opacity` for drawer motion.
- Avoid animating grid dimensions, width, height, or layout-affecting properties in the table hot path.

---

## 4) Detector-like signals: decisive vs context-dependent

### Decisive from supplied evidence

- `catch {}` proves save errors are swallowed in the shown flow.
- `rows.map(...)` plus the note proves 10,000 product rows are rendered at once.
- Missing state notes decisively establish absent represented states within the supplied scope.
- Drawer notes decisively establish no focus trap/background lock in the described implementation.
- `transition: all` decisively exists for `.product-row` and `.drawer`.
- `min-width: 1180px` and fixed `520px` drawer decisively exist in the provided CSS.
- `outline: none` decisively removes the default outline for `.icon-button` in this snippet.

### Needs project/runtime context before final severity or implementation choice

- Whether another stylesheet restores focus-visible styling.
- Whether `ProductRow` is cheap enough for some machines, though the unbounded render remains a structural risk.
- Actual filter latency, memory, scroll FPS, and layout shift.
- Whether existing API clients already apply timeouts, retries, idempotency, or auth handling.
- Whether an outer layout already supplies tablet scrolling or responsive constraints.
- Whether image processing is handled before these components receive image data.
- Whether table semantics, accessible names, and live regions exist inside omitted components.
- Whether the design system already has modal, drawer, toast, status, table, and skeleton primitives that should be reused.

---

## 5) Measurement-first validation plan

### Baseline before changes

- Define canonical datasets:
  - 10,000 rows,
  - 200-character names,
  - missing prices,
  - 60% longer translated labels,
  - absent images,
  - multiple 8MB images,
  - mixed permissions,
  - partial batch failures.
- Measure initial render, filter keystroke latency, scroll smoothness, memory, image layout shift, drawer open/close cost, and save-state timing.
- Run failure scenarios for 401, 403, 409, 429, 500, timeout, offline, retry success, retry failure, and partial batch failure.
- Audit keyboard path: filters → table → row actions → drawer → save/close → return focus.
- Audit screen-reader names and announcements for icon buttons, table selection, drawer title, errors, and autosave status.

### Acceptance conditions

- No save failure is silent.
- Dirty/pending edits cannot be accidentally discarded.
- Every listed failure state has a visible, recoverable UI state.
- Conflict handling prevents stale overwrite.
- Drawer traps focus, blocks background interaction, labels controls, restores focus, and handles Escape safely.
- 10,000-row filtering and scrolling meet agreed latency/frame budgets on target hardware.
- Images do not cause meaningful layout shift in the table.
- Tablet viewport has reachable filters, rows, drawer controls, and save/close actions.
- Reduced-motion mode removes nonessential movement while preserving state feedback.
- Permission-restricted users see disabled/hidden/explained actions before failure.

### Rollback conditions

- Save error rate, conflict rate, or support-reported lost edits increases.
- Filter latency or scroll performance regresses beyond the agreed budget.
- Virtualization breaks selection, focus restoration, row identity, or bulk actions.
- Drawer changes trap users or block legitimate background workflow unexpectedly.
- Tablet layout hides primary actions or increases task completion time.
- New retry behavior creates duplicate writes or stale overwrites.

### Rollout strategy

- Ship hardening behind narrow flags where possible: save-state handling, drawer safety, virtualization, and upload pipeline can be staged separately.
- Keep a fallback table path until selection, focus, and bulk actions are verified with large datasets.
- Instrument save outcomes, conflict frequency, retry behavior, filter latency, row render count, image failures, and drawer abandonment.
- Release only when production metrics and operator task checks confirm the workflow is safer without becoming slower or unfamiliar.
