## 1. Sequencing + verdict

**Correct sequence:** **audit → harden → optimize → polish → measured validation/rollback gate.**  
Do not polish motion, spacing, or visual density before fixing save failure handling, state recovery, drawer accessibility, and 10,000-row rendering.

**One-line verdict:** Static evidence shows a production-risky operations surface: the workflow is recognizable, but save failures, missing recovery states, drawer accessibility gaps, fixed desktop layout, and unbounded rendering make it unsafe to ship without hardening and performance work.

---

## 2. Prioritized findings: source evidence vs runtime hypotheses

### P0 — Silent save failure can cause data loss or false confidence

**Source evidence**

```tsx
try {
  await api.save(product);
} catch {}
setSaving(false);
```

- Save errors are swallowed.
- The UI can return to non-saving state after failure with no error, retry, conflict resolution, or recovery path.
- Additional notes say 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.

**Impact**

Operations users may believe inventory changes were saved when they were not. This is a data-integrity issue, not just UX polish.

**Runtime hypotheses needing verification**

- Whether `api.save` has global interceptors, toast handling, or server-side optimistic conflict protection.
- Whether autosave has a queue, local draft persistence, or retry outside this component.

**Fix**

- Replace `catch {}` with typed save outcomes: success, validation error, conflict, auth, rate-limit, server error, timeout, offline.
- Keep failed edits recoverable in the drawer.
- Show inline save failure near the affected product, not only global status.
- Add retry and “copy/export unsaved changes” escape hatch for persistent failure.
- Treat 409 as a merge/refresh decision, not a generic error.

---

### P0 — Drawer can close during pending save and does not protect interaction state

**Source evidence**

- “Escape closes it even while a save is pending.”
- “The drawer traps neither focus nor background interaction.”
- Save and close are icon-only.

**Impact**

A user can accidentally dismiss the edit context during a pending save, lose track of unsaved edits, or interact with the background while the drawer is active. Keyboard and assistive-technology users are especially exposed.

**Runtime hypotheses needing verification**

- Whether drawer close actually discards local edits or only hides them.
- Whether background table actions mutate the same product while the drawer is open.

**Fix**

- While save is pending, make Escape either disabled or require confirmation if there are unsaved/pending changes.
- Add explicit dirty/pending/error states.
- Preserve draft state on close failure.
- Trap focus inside the drawer when modal-like.
- Mark background inert or otherwise block background interaction.
- Restore focus to the invoking row/control after close.

---

### P1 — Core failure and permission states are absent

**Source evidence**

- Blank table body during initial/filter loading.
- Empty results, 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states not represented.
- Permission-specific affordances are not described.

**Impact**

Users cannot distinguish “still loading,” “no matches,” “not allowed,” “server failed,” “conflict,” and “saved partially.” In operations software, ambiguity creates duplicate work and support escalations.

**Runtime hypotheses needing verification**

- Whether route-level boundaries or API clients provide some of these states.
- Whether permission restrictions are hidden server-side only or reflected in UI capabilities.

**Fix**

- Replace blank loading with skeleton rows matching table geometry.
- Add empty state with active filter summary and clear-filter action.
- Add 401/403 state with reauth/request-access path.
- Add 409 conflict UI: show stale fields, server values, user values, and resolution action.
- Add 429 state with retry-after messaging and disabled repeated save spam.
- Add timeout/offline state with queued draft indicator.
- For partial batch failure, show per-item success/failure summary and retry failed only.
- Gate affordances by permission: visible disabled state with explanation where useful; hide only when the action is irrelevant.

---

### P1 — 10,000 rows render synchronously and filtering blocks keystrokes

**Source evidence**

```tsx
{rows.map((row) => <ProductRow key={row.id} row={row} />)}
```

Additional note:

- “All 10,000 rows render at once.”
- “Filtering recalculates synchronously on every keystroke.”

**Impact**

The page is likely to have slow initial render, input jank, high memory use, and expensive re-renders. For keyboard-heavy operators, filter latency directly harms throughput.

**Runtime hypotheses needing verification**

- Actual row complexity inside `ProductRow`.
- Hardware baseline for operations staff.
- Whether React concurrent features, memoization, or server-side filtering exist elsewhere.

**Fix**

- Virtualize the table body with preserved keyboard semantics and accessible row counts.
- Debounce or defer expensive filter recalculation.
- Memoize derived filtered/sorted rows with correct dependencies.
- Avoid re-rendering every row when `saving` changes.
- Keep selection state stable by product id, not visible index.
- For very large datasets, consider server-side pagination/filtering if business workflow allows it; do not introduce it blindly if users need cross-result bulk selection.

---

### P1 — Accessibility blockers in drawer and controls

**Source evidence**

```css
.icon-button { width: 28px; height: 28px; outline: none; }
```

Additional notes:

- Drawer has no focus trap.
- Save and close are icon-only.
- Keyboard navigation, screen-reader labels, focus-visible are not described.

**Impact**

Icon-only controls may be unnamed to screen readers. Small controls are hard to target, especially on tablet. Removing outline can erase visible keyboard focus. Drawer focus leakage can make the page difficult or impossible to use with keyboard navigation.

**Runtime hypotheses needing verification**

- Whether icon buttons have `aria-label` or visually hidden text inside components.
- Whether another stylesheet restores focus with `:focus-visible`.
- Whether hit area is enlarged by padding not shown here.

**Fix**

- Give save/close buttons accessible names.
- Use visible text where space allows; otherwise icon + tooltip + accessible label.
- Ensure minimum interactive target is at least 44×44 CSS px on tablet/touch contexts.
- Restore visible focus with `:focus-visible`.
- Use semantic buttons, not clickable divs.
- Add drawer role/name/description appropriate to modality.
- Preserve logical tab order and focus return.

---

### P1 — Fixed desktop layout does not satisfy tablet support

**Source evidence**

```css
.page { min-width: 1180px; }
.product-row {
  display: grid;
  grid-template-columns: 64px 280px 1fr 120px 96px;
}
.drawer {
  position: fixed;
  right: 0;
  width: 520px;
  height: 100vh;
}
```

Additional note:

- Tablet behavior is not described.

**Impact**

A desktop minimum width and fixed drawer can force horizontal page overflow, hide table columns, or cover too much of the viewport on tablet.

**Runtime hypotheses needing verification**

- Whether a containing table scroller intentionally owns horizontal overflow.
- Whether tablet is landscape-only by product requirement.
- Whether CSS media queries outside the snippet override these values.

**Fix**

- Keep desktop density, but constrain overflow to the table region, not the whole page.
- Define tablet breakpoints explicitly.
- On tablet, allow drawer width like `min(520px, 100vw)` or a full-height sheet/panel pattern that preserves close/save access.
- Collapse lower-priority columns or provide column controls if table semantics allow.
- Keep critical identifiers, status, price, and selection reachable without page-level horizontal scroll.
- Validate translations expanded by 60%.

---

### P1 — Hostile data cases are undercovered

**Source evidence**

- Product names may be 1–200 characters.
- Prices may be missing.
- Translations may expand labels by 60%.
- Some images are absent or 8MB.
- Product name truncates:

```css
.product-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

**Impact**

Users may lose distinguishing product information, misread missing price as zero, see broken image slots, or encounter layout overflow in translated UI.

**Runtime hypotheses needing verification**

- Whether full product names are available in drawer, tooltip, title, or detail view.
- Whether price formatting handles null distinctly.
- Whether image service generates thumbnails.

**Fix**

- For long names: preserve row height but expose full value through drawer/detail, accessible tooltip, or expandable cell.
- For missing prices: display an explicit “Missing price” state, not blank or `0`.
- For absent images: reserve dimensions and show a neutral placeholder with accessible alt behavior.
- For 8MB images: use server-generated thumbnails, lazy loading, decoding hints, size limits, and upload validation.
- For translations: test labels/actions at +60% length and avoid fixed-width text-only assumptions.

---

### P2 — Broad layout animation is risky and ignores reduced motion

**Source evidence**

```css
.product-row, .drawer {
  transition: all 300ms ease-in;
}
```

Additional note:

- Reduced motion is not described.

**Impact**

`transition: all` can animate layout-affecting properties accidentally. `ease-in` makes exits feel sluggish and state feedback delayed. Rows should not animate arbitrary changes in a dense operations table.

**Runtime hypotheses needing verification**

- Which properties actually change at runtime.
- Whether a later `prefers-reduced-motion` rule exists.
- Whether row transitions are visible during filtering/selection.

**Fix**

- Replace `transition: all` with specific properties, usually `transform`, `opacity`, `background-color`, `box-shadow`, or `border-color`.
- Use shorter product UI timings, roughly 150–250ms.
- Prefer ease-out for drawer entrance and direct state feedback.
- Add `@media (prefers-reduced-motion: reduce)` to remove or shorten motion while preserving state indication.
- Avoid animating 10,000 row layout changes.

---

### P2 — Global `saving` state is too coarse

**Source evidence**

```tsx
const [saving, setSaving] = useState(false);
<EditDrawer onSave={saveProduct} saving={saving} />
```

**Impact**

A single boolean cannot represent queued saves, per-product failures, conflicts, partial batch results, or overlapping requests. It also risks incorrect state if multiple save attempts overlap.

**Runtime hypotheses needing verification**

- Whether the drawer allows only one product and one save at a time.
- Whether bulk selection uses a separate save path.

**Fix**

- Track save status by product id and operation id.
- Use a finite state model: idle, dirty, saving, saved, failed, conflict, offline queued.
- Prevent stale requests from overwriting newer state.
- Show last saved time and failed item count where relevant.

---

### P2 — Image layout instability likely

**Source evidence**

- “Image dimensions are not reserved.”
- Some images are absent or 8MB.

**Impact**

Rows may shift as images load, hurting scanning and causing misclicks. Large images can delay interaction and waste memory.

**Runtime hypotheses needing verification**

- Whether product rows include images in the omitted markup.
- Whether CDN transformation or CSS aspect-ratio exists elsewhere.

**Fix**

- Reserve image box size with `width`, `height`, or `aspect-ratio`.
- Load thumbnails, not originals.
- Add absent-image state.
- Use lazy loading only where it does not break virtualized rows or immediate visible content.
- Validate upload size/type before network transfer when possible.

---

### P3 — Final polish should wait until hardening is complete

**Source evidence**

- Existing system and workflow must be preserved.
- Production task surface, not redesign.

**Impact**

Visual tweaks before state and performance fixes would hide the highest-risk failures.

**Fix**

- After hardening and optimization, polish only within the existing design system:
  - clearer save/error copy,
  - consistent disabled/loading/error states,
  - tighter focus treatment,
  - reduced-motion-safe drawer transition,
  - better table skeleton/empty-state copy,
  - no new decorative visual language.

---

## 3. Concrete fixes by category

### Hostile data

- Long names: keep ellipsis in dense rows, but provide full accessible disclosure in drawer/detail.
- Missing price: show explicit missing/null state; do not format as zero.
- Expanded translations: test action labels and filter controls at +60%; allow wrapping where labels are not table cells.
- Absent images: reserve slot, show placeholder, avoid broken icon.
- 8MB images: thumbnail pipeline, upload size validation, progress/error state, retry/remove action.

### Failures

- Replace swallowed errors with typed UI states.
- Represent 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure.
- Keep failed edits recoverable.
- Add conflict resolution for stale product edits.
- Add retry with backoff awareness for rate limits.
- Add per-row/per-batch status, not only a global spinner.

### Responsive layout

- Keep desktop-first table density.
- Move horizontal overflow into the table viewport if needed.
- Avoid page-level `min-width: 1180px` as the only strategy.
- Make drawer width responsive: fixed desktop max, viewport-bounded tablet behavior.
- Define tablet column priority and action placement.
- Ensure icon/action controls are touch-safe on tablet.

### Accessibility

- Add accessible names to icon-only save/close controls.
- Restore visible keyboard focus with `:focus-visible`.
- Use semantic buttons and form labels.
- Trap focus inside active drawer if modal; make background inert.
- Restore focus to the opener on close.
- Do not close on Escape during pending save without safe handling.
- Add reduced-motion alternative.
- Validate keyboard navigation across filters, table rows, bulk selection, drawer, upload, save, and errors.

### State recovery

- Track dirty/saving/saved/failed/conflict/offline states explicitly.
- Persist unsaved draft locally during transient failure where appropriate.
- Prevent close/navigation from discarding pending edits silently.
- Make autosave status specific: “Saving…”, “Saved 10:42”, “Failed — retry”, “Offline — changes queued.”
- For partial batch operations, allow retry failed only and preserve selection context.

### Performance

- Virtualize 10,000-row rendering.
- Memoize filtering/sorting.
- Debounce or defer filter input work.
- Avoid global state changes that re-render all rows.
- Reserve image dimensions.
- Use thumbnails and lazy/deferred image loading carefully.
- Keep row components stable with memoized props/callbacks where measurable.
- Avoid `transition: all` on rows.

---

## 4. Static detector-like signals: decisive vs context-dependent

### Decisive from the provided source

- `catch {}` in save is a real silent failure path unless an outer layer is proven to handle it.
- Rendering 10,000 rows with `rows.map` is an unbounded render strategy in this component.
- `transition: all` is a concrete CSS risk.
- `outline: none` on `.icon-button` is unsafe without a proven replacement focus style.
- `width: 28px; height: 28px` is below touch-friendly target size.
- `.page { min-width: 1180px; }` conflicts with tablet support unless overflow/adaptive rules exist elsewhere.
- Missing represented states are decisive because the notes explicitly say they are absent.

### Needs project/runtime context before final judgment

- Actual frame rate, input latency, memory use, and render cost.
- Whether `ProductRow` is semantically a table row, grid row, or accessible list item.
- Whether icon buttons already have `aria-label` or hidden text.
- Whether global CSS restores focus-visible.
- Whether API interceptors handle auth, retry, conflict, or toast errors.
- Whether image CDN resizing already exists.
- Whether tablet support is landscape-only or includes portrait.
- Whether permissions are enforced visibly elsewhere.
- Whether colors meet contrast; no color values were provided.
- Whether autosave is truly this `saveProduct` path or a simplified excerpt.

---

## 5. Measurement-first validation plan with rollback and acceptance gates

### Baseline before changes

- Measure initial render with 10,000 rows.
- Measure filter keystroke latency at p50/p95.
- Measure row selection and drawer open latency.
- Measure memory after scrolling/filtering/editing.
- Record layout shift from image loading.
- Document current failure behavior for 401/403/409/429/500/timeout/offline.

### Hardening validation

Acceptance conditions:

- No save failure can end in a false “saved” state.
- 401/403/409/429/500/timeout/offline each has a distinct, actionable UI.
- Failed edits remain recoverable.
- Partial batch failures identify failed items and allow retry failed only.
- Pending save blocks unsafe close or requires explicit confirmation.
- Conflict handling prevents silent overwrite.

Rollback trigger:

- Any new save-state logic causes duplicate saves, lost edits, or incorrect success reporting.

### Accessibility validation

Acceptance conditions:

- Full workflow is keyboard-operable: filters → table → selection → drawer → upload → save/close.
- Drawer focus is contained while open and restored on close.
- Save/close controls have accessible names.
- Visible focus is present on all interactive controls.
- Reduced-motion setting removes nonessential motion.
- Tablet touch targets meet practical minimum size.

Rollback trigger:

- Focus trap prevents escape/recovery, traps users permanently, or blocks assistive-technology navigation.

### Performance validation

Acceptance conditions:

- 10,000-row route remains interactive on target hardware.
- Filter keystrokes stay within agreed latency budget, ideally p95 under 100ms for visible feedback.
- Drawer open/close does not re-render all rows unnecessarily.
- No large image causes major layout shift or long main-thread blocking.
- Virtualization preserves selection, keyboard navigation, and screen-reader expectations.

Rollback trigger:

- Virtualization breaks bulk selection, row identity, findability, or keyboard navigation.

### Responsive validation

Acceptance conditions:

- Desktop workflow remains dense and familiar.
- Tablet layout has no page-level horizontal scroll except intentional table-region scrolling.
- Drawer remains usable at tablet widths.
- Critical actions are reachable without hidden overflow.
- Translated labels at +60% do not obscure primary actions.

Rollback trigger:

- Tablet adaptation removes required columns/actions or changes the established workflow.

### Final polish gate

Only after the above pass:

- Tighten loading, empty, error, and saved-state copy.
- Normalize icon button sizing and labels.
- Refine drawer motion with reduced-motion support.
- Preserve the existing design system and table workflow.
- Avoid new dependencies unless measurements prove the existing approach cannot meet the performance/accessibility targets.
