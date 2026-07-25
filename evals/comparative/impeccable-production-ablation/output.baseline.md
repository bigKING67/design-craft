## 1. Sequencing + verdict

**Correct sequence:** Audit risk surface → harden save/error/state recovery paths → optimize 10,000-row interaction performance → polish responsive, motion, and accessibility details within the existing design system.

**One-line verdict:** Static evidence shows this inventory editor is not production-ready for high-volume operations use because save failures, conflict/permission states, keyboard accessibility, and 10,000-row rendering are under-specified or actively unsafe.

---

## 2. Prioritized findings

### P0 — Silent save failure and unsafe close can cause lost work

**Source evidence**

```tsx
try {
  await api.save(product);
} catch {}
setSaving(false);
```

- Save errors are swallowed.
- No user-visible failed state is represented.
- `setSaving(false)` is not in `finally`, so future edits could leave inconsistent state if the function changes or throws outside the awaited call.
- Additional notes say Escape closes the drawer even while a save is pending.
- Autosave status exists in product context, but no failed/retry/conflict state is represented.

**Runtime hypothesis**

- Operators may believe changes were saved when they were not.
- A pending save may be interrupted by drawer close, losing local context.
- Concurrent saves may produce misleading global `saving` state because one boolean covers the whole drawer/page.

**Fix**

- Replace swallowed errors with explicit save state: `idle | saving | saved | failed | conflict | offline | unauthorized`.
- Keep failed edits locally recoverable.
- Block destructive close while save is pending, or require confirmation: “Save in progress. Wait or discard?”
- Use `try/catch/finally`; track save by product id or operation id, not only one page-level boolean.
- Show retry, conflict resolution, and last-saved timestamp.
- Preserve draft values until server confirmation or explicit discard.

---

### P0 — Missing conflict, permission, offline, timeout, and partial-failure states

**Source evidence**

- Notes explicitly say these are not represented: `401/403`, `409 conflict`, `429`, `500`, timeout, offline, retry, partial batch failure.
- Bulk selection and autosave exist in the product context.

**Runtime hypothesis**

- Operators may continue editing without permission, overwrite newer data, or lose trust in bulk actions.
- Batch updates may appear successful even when only some rows saved.

**Fix**

- Add state coverage without redesigning workflow:
  - `401/403`: permission-specific empty/locked affordance; disable unavailable actions with explanation.
  - `409`: conflict banner/drawer panel showing local value, server value, and resolve options.
  - `429`: backoff message and retry-after handling.
  - `500/timeout/offline`: non-destructive error with retry.
  - Partial batch failure: summarize successes/failures, keep failed row ids selected or highlighted.
- Make server responses authoritative; client affordances should guide, not replace backend checks.

---

### P1 — 10,000 rows render at once; filtering runs synchronously per keystroke

**Source evidence**

- Notes say all 10,000 rows render at once.
- Notes say filtering recalculates synchronously on every keystroke.
- Code maps all rows directly:

```tsx
{rows.map((row) => <ProductRow key={row.id} row={row} />)}
```

**Runtime hypothesis**

- Keystrokes may lag.
- Bulk selection and drawer edits may trigger large re-renders.
- Tablet devices are likely worse.

**Fix**

- Virtualize the table/list while preserving existing row layout and workflow.
- Memoize filtered/sorted rows with correct dependencies.
- Debounce or defer filter input work while keeping the input responsive.
- Avoid passing unstable props/functions to every row where possible.
- Split page state so drawer save state does not force all rows to re-render.
- Reserve row/image dimensions to avoid layout shifts.

---

### P1 — Drawer accessibility and keyboard flow are unsafe for operations staff

**Source evidence**

- Drawer traps neither focus nor background interaction.
- Escape closes it even while save is pending.
- Save and close are icon-only.
- `.icon-button { width: 28px; height: 28px; outline: none; }`
- Keyboard navigation, screen-reader labels, and focus-visible are not described.

**Runtime hypothesis**

- Keyboard-heavy users can tab into background content while editing.
- Screen-reader users may not know what icon-only controls do.
- Users may lose current edit position after closing or saving.

**Fix**

- Treat drawer as a modal or clearly non-modal panel; current behavior is neither safe nor explicit.
- If modal: add focus trap, restore focus to the invoking row/control, prevent background interaction, and announce title/state.
- If non-modal: keep background interaction intentional and clearly documented, but do not trap partial focus accidentally.
- Add accessible names for save/close/upload/action buttons.
- Replace `outline: none` with visible `:focus-visible` styling using existing tokens.
- Disable or guard Escape while saving; require explicit discard for unsaved edits.
- Ensure tab order follows the visual workflow.

---

### P1 — Blank loading and empty states make the table look broken

**Source evidence**

- Initial and filter loading render a blank table body.
- Empty results are not represented.

**Runtime hypothesis**

- Operators may think data disappeared or the page failed.
- Filter changes may feel destructive.

**Fix**

- Add loading rows/skeletons that preserve table structure.
- Add empty filtered result state with active filter summary and “clear filters” action.
- Distinguish initial loading from refiltering/loading-more.
- Keep prior results visible during background refresh when safe, with a subtle updating status.

---

### P2 — Hostile data cases are not visibly protected

**Source evidence**

- Product names may be 1–200 characters.
- Prices may be missing.
- Translations may expand labels by 60%.
- Images may be absent or 8MB.
- `.product-name` truncates with ellipsis.
- Image dimensions are not reserved.

**Runtime hypothesis**

- Critical product names may become indistinguishable.
- Missing prices may be confused with zero.
- Long localized labels may overflow controls.
- Large images may block upload or cause layout instability.

**Fix**

- Long names: keep ellipsis, but provide accessible full name via title/details cell or row expansion pattern already used in the system.
- Missing prices: render explicit “Missing”/“Not set” state, not blank or zero.
- Translations: test longer labels; allow wrapping where appropriate in filters/drawer, not in dense row identifiers unless designed.
- Images: reserve dimensions, show absent-image placeholder, validate file size/type before upload, compress or reject 8MB files per product policy, show progress/error/retry.
- Avoid using only color to distinguish missing/invalid values.

---

### P2 — Responsive behavior conflicts with tablet support

**Source evidence**

```css
.page { min-width: 1180px; }
.product-row { grid-template-columns: 64px 280px 1fr 120px 96px; }
.drawer { position: fixed; right: 0; width: 520px; height: 100vh; }
```

- Tablet behavior is not described.
- Fixed minimum page width and fixed drawer width are specified.

**Runtime hypothesis**

- Tablet users may get horizontal scrolling, obscured rows, or drawer/table overlap.
- Fixed `100vh` may behave poorly with browser UI and soft keyboards.

**Fix**

- Preserve desktop layout, but add tablet rules:
  - Use responsive drawer width: `min(520px, 100vw)` or design-token equivalent.
  - Define how table columns compress or scroll.
  - Keep key identifiers and actions visible.
  - Ensure drawer does not hide required save/error controls.
- Use modern viewport units or safe-area handling where supported.
- Define acceptance breakpoints rather than redesigning the surface.

---

### P2 — Motion is broad, potentially expensive, and lacks reduced-motion path

**Source evidence**

```css
.product-row, .drawer { transition: all 300ms ease-in; }
```

- Reduced motion is not described.

**Runtime hypothesis**

- `transition: all` may animate layout-affecting properties unintentionally.
- Row transitions across 10,000 items can add jank.
- Ease-in can feel sluggish for drawer entry because it starts slowly.

**Fix**

- Replace `transition: all` with named properties, usually `transform`, `opacity`, or tokenized color/border changes.
- Do not animate every row during filtering or bulk state changes.
- Add `prefers-reduced-motion` handling that preserves state feedback without movement.
- Keep duration/easing aligned to the existing design system.

---

### P3 — State ownership is too coarse for bulk/table/drawer interactions

**Source evidence**

```tsx
const [rows, setRows] = useState(allRows);
const [saving, setSaving] = useState(false);
```

- One `saving` flag is shared.
- Bulk selection exists in product context.
- Autosave status exists in product context.

**Runtime hypothesis**

- A single save may disable or mislabel unrelated controls.
- Bulk actions need per-row and batch-level status.
- Optimistic updates may become difficult to reconcile.

**Fix**

- Separate page loading, filter loading, row draft state, drawer save state, and batch save state.
- Use per-row operation status for visible row feedback.
- Keep autosave status specific: “Saving SKU-123”, “Saved 10:42”, “3 failed”, not just a spinner.

---

## 3. Concrete hardening moves by area

### Hostile data

- Explicit missing-value rendering for price, image, and optional fields.
- Full-name access for truncated product names.
- Reserved image boxes with placeholders.
- Upload validation before network transfer.
- Long localized strings tested in filters, drawer labels, buttons, and table cells.

### Failures

- Add visible states for unauthorized, forbidden, conflict, rate limit, server error, timeout, offline, retry, and partial batch failure.
- Keep user edits until confirmed saved or discarded.
- Provide retry at the failed operation scope: row, drawer, or batch.
- Avoid replacing table content with blank space during loading.

### Responsive layout

- Keep desktop-first grid.
- Add tablet-specific drawer width and table overflow rules.
- Define minimum usable viewport and fallback behavior.
- Ensure fixed drawer does not cover toasts, save state, or required row actions.

### Accessibility

- Restore visible focus styles.
- Add accessible names for icon-only buttons.
- Decide and implement drawer modality.
- Trap focus only if modal; otherwise manage non-modal navigation deliberately.
- Restore focus after close.
- Guard Escape during pending save or unsaved changes.
- Add status announcements for save success/failure where appropriate.

### State recovery

- Model drafts separately from persisted rows.
- Track last successful save.
- On failure, keep draft and show recovery action.
- On conflict, show local/server values and resolution options.
- On route leave or drawer close with unsaved edits, confirm or autosave safely.

### Performance

- Virtualize 10,000 rows.
- Memoize filter results.
- Defer/debounce expensive filtering.
- Prevent drawer save state from re-rendering every row.
- Reserve image dimensions.
- Avoid `transition: all` on rows.
- Measure input latency, render cost, and memory before/after.

---

## 4. Static detector-like signals: decisive vs context-dependent

### Decisive from static evidence

- `catch {}` is unsafe for production saves.
- Blank loading/empty/error states are insufficient for an operations table.
- Rendering 10,000 rows directly is a serious performance risk.
- `outline: none` without a replacement focus style is an accessibility failure.
- Icon-only save/close require accessible names.
- Drawer without focus/background management is unsafe.
- `transition: all` is too broad for rows and drawer.
- Fixed `min-width: 1180px` conflicts with unspecified tablet support.
- Missing conflict/offline/partial-failure states are unacceptable for autosave and bulk workflows.

### Needs project/runtime context

- Exact virtualization strategy depends on row height, sticky headers, column resizing, and selection model.
- Whether the drawer should be modal or non-modal depends on intended workflow.
- The acceptable debounce/defer timing depends on operator speed and filter complexity.
- Upload limits depend on backend policy and image pipeline.
- Tablet breakpoints depend on supported devices.
- Whether 10,000 rows is always loaded or eventually paginated depends on data contract.
- Exact reduced-motion behavior should follow the existing motion tokens.

---

## 5. Measurement-first validation plan with rollback/acceptance

### Baseline before changes

- Record current row count, filter input latency, drawer open/close responsiveness, memory use, and save failure behavior.
- Capture representative cases: 10,000 rows, long names, missing prices, absent images, 8MB image, empty filter result, failed save, conflict, offline, forbidden user, partial batch failure.
- Define keyboard path through filters, table, bulk selection, drawer, save, close, and upload.

### Acceptance conditions

- Failed saves are visible, recoverable, and never reported as successful.
- Pending save cannot be silently discarded by Escape or close.
- Conflict and permission states have clear operator actions.
- Initial loading, filter loading, empty, error, offline, and partial-failure states are represented.
- 10,000-row filtering keeps typing responsive within the agreed threshold.
- Drawer interaction does not force unnecessary full-table re-renders.
- Keyboard users can complete the core edit workflow.
- Focus is visible and restored after drawer close.
- Icon-only controls have accessible names.
- Tablet layout has a defined, usable behavior without hidden critical actions.
- Reduced-motion users receive state feedback without large movement.
- Images do not cause avoidable layout shifts.

### Rollback conditions

- Virtualization breaks selection, keyboard navigation, row measurement, or bulk actions.
- Save hardening blocks valid edits or creates duplicate submissions.
- Responsive changes hide critical columns/actions on desktop.
- Focus trapping prevents access to required non-modal workflow.
- Upload validation rejects valid production files.
- Performance work improves scrolling but worsens edit/save reliability.

### Release approach

- Ship in small layers: save/error hardening first, then failure-state coverage, then performance virtualization/filtering, then responsive/accessibility polish.
- Keep each layer reversible behind narrow implementation boundaries where possible.
- Do not introduce a new design system or dependency unless an existing component cannot meet the measured requirement.
