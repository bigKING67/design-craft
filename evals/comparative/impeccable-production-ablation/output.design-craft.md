## 1) Sequence + verdict

Static review only: no runtime detector, browser, profiler, accessibility tree, network throttle, or device run was performed.

Correct sequence: **audit evidence → define baseline measurements → harden correctness/recovery/accessibility → remeasure and optimize hot paths → polish motion/layout states → release behind rollbackable guardrails.**

One-line verdict: **Not production-ready for a 10,000-row operations surface until save failure visibility, drawer accessibility, state recovery, bounded rendering, and tablet/data-stress behavior are hardened.**

---

## 2) Prioritized findings: evidence vs hypotheses

### P0 — Silent save failure and data-loss risk

**Source evidence**

```tsx
try {
  await api.save(product);
} catch {}
setSaving(false);
```

- Errors are swallowed.
- Autosave status can return to non-saving without communicating failure.
- No conflict, retry, timeout, offline, or partial batch failure representation is described.
- Escape can close the drawer while a save is pending.

**Runtime hypotheses needing validation**

- Whether unsaved edits are lost on close/navigation.
- Whether server-side versioning, idempotency, or conflict handling exists elsewhere.
- Whether autosave status is global enough to confuse multiple row edits.

**Fix**

- Replace boolean-only `saving` with explicit save state: `idle | dirty | saving | saved | failed | conflict | offline | retrying`.
- Preserve dirty edits locally until confirmed saved.
- Surface failures inline in drawer and in autosave status.
- Make `catch` observable: error classification, retry affordance, telemetry/logging without leaking sensitive data.
- Use `finally` for saving cleanup, but do not mark as saved unless the request succeeds.
- Add request identity/versioning so stale responses do not overwrite newer edits.
- For 409, show conflict resolution: “server changed since you opened this,” compare fields, choose local/server/merge.
- Block Escape/close during critical save, or require confirmation: “Save still in progress. Keep editing / discard / retry.”
- For bulk saves, show per-item partial failure and allow retry only failed rows.

---

### P0 — Drawer is not accessible as a modal/editing surface

**Source evidence**

- Drawer traps neither focus nor background interaction.
- Save and close are icon-only.
- Escape closes even during pending save.
- `.icon-button { width: 28px; height: 28px; outline: none; }`

**Runtime hypotheses needing validation**

- Whether global styles restore focus visibility.
- Whether icon buttons receive `aria-label` inside the actual components.
- Whether product row semantics are table-like, grid-like, or just divs.

**Fix**

- Give drawer `role="dialog"` or appropriate semantic equivalent, `aria-modal="true"`, accessible title, and described save status.
- Trap focus while open; return focus to the invoking row/control on close.
- Mark background inert or otherwise prevent interaction while drawer is modal.
- Provide keyboard order: close, title, fields, validation, save actions.
- Save/close icon buttons need text labels or `aria-label`.
- Restore visible focus using `:focus-visible`; never remove outline without replacement.
- Use `aria-live` for autosave state changes, but avoid noisy announcements on every keystroke.
- Define Escape behavior: disabled/confirmed while saving or dirty.

---

### P0 — Unbounded rendering and synchronous filtering on a 10,000-row table

**Source evidence**

```tsx
{rows.map((row) => <ProductRow key={row.id} row={row} />)}
```

- All rows render at once.
- Notes say filtering recalculates synchronously on every keystroke.
- Image dimensions are not reserved.

**Runtime hypotheses needing validation**

- Actual row complexity, DOM node count, render duration, and memory pressure.
- Whether `ProductRow` is memoized.
- Whether filtering is local-only or server-backed.
- Whether image decoding and layout shift are visible under real assets.

**Fix**

- Window/virtualize visible rows using existing project primitives if available; avoid a dependency pitch unless no internal option exists.
- Keep DOM bounded to viewport plus overscan.
- Memoize row rendering and derived filter data with correct dependencies.
- Debounce or defer filtering input so keystrokes stay responsive.
- Pre-normalize searchable fields instead of lowercasing/parsing all 10,000 rows every keypress.
- For very expensive filters, move computation off the critical input path after measurement.
- Reserve image dimensions/aspect ratio; use placeholders for absent images.
- Lazy-load/decode images and reject/compress oversized uploads before preview where product policy allows.

---

### P1 — Missing failure, permission, loading, and empty states

**Source evidence**

- Initial and filter loading render a blank table body.
- Empty results, 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.
- Permission-specific affordances are not described.

**Runtime hypotheses needing validation**

- Whether route-level error boundaries or API clients handle some states globally.
- Whether permissions are enforced server-side only or also reflected in UI affordances.

**Fix**

- Replace blank body with skeleton/progress state that preserves table structure.
- Add empty state for “no products” and “no matches for filters.”
- 401/403: show re-auth or “permission required”; disable hidden/disallowed actions consistently.
- 429: communicate rate limit and retry timing.
- 500/timeout/offline: retry, keep edits, and explain what is safe.
- Partial batch failure: list failed rows, reasons, and retry path.
- Ensure disabled controls explain why, especially permission-based restrictions.

---

### P1 — Responsive layout is brittle for tablet support

**Source evidence**

```css
.page { min-width: 1180px; }
.product-row { grid-template-columns: 64px 280px 1fr 120px 96px; }
.drawer { position: fixed; right: 0; width: 520px; height: 100vh; }
```

**Runtime hypotheses needing validation**

- Whether the product intentionally uses horizontal scrolling on tablet.
- Whether surrounding layout, zoom, or container queries compensate.
- Whether drawer overlays or crushes key table columns.

**Fix**

- Define supported breakpoints explicitly: desktop dense mode, tablet compact mode.
- Replace hard `min-width: 1180px` with a deliberate overflow container or responsive column strategy.
- Use `width: min(520px, 100vw)` or tokenized/clamped drawer width.
- Use `height: 100dvh` where appropriate to avoid viewport chrome issues.
- Allow less-critical columns to collapse, truncate with accessible full text, or move into row detail on tablet.
- Keep bulk actions and save status visible when the drawer is open.

---

### P1 — Hostile data is under-specified

**Source evidence**

- Product names may be 1–200 characters.
- Prices may be missing.
- Translations may expand labels by 60%.
- Images may be absent or 8MB.
- `.product-name` truncates to one line.

**Runtime hypotheses needing validation**

- Whether full names are available via title, detail drawer, or accessible text.
- Whether missing price is allowed, invalid, or pending.
- Whether image upload constraints exist server-side.

**Fix**

- Use explicit missing price state: em dash, “Not set,” or validation error depending on business meaning.
- Preserve full product names for screen readers and detail view; avoid relying only on visual ellipsis.
- Test expanded labels in filters, drawer actions, empty/error states, and bulk actions.
- Reserve image boxes; show absent-image placeholder.
- Validate upload type/size/dimensions before upload; show progress, cancel, retry, and failure reason.
- Avoid loading full 8MB images into every row thumbnail.

---

### P2 — Motion is broad, potentially janky, and not reduced-motion safe

**Source evidence**

```css
.product-row, .drawer { transition: all 300ms ease-in; }
```

- `transition: all` can animate layout, width, height, shadows, colors, or unintended properties.
- Reduced motion is not described.

**Runtime hypotheses needing validation**

- Whether actual property changes are compositor-friendly.
- Whether transition conflicts with drawer positioning or row updates.

**Fix**

- Transition only intended properties, e.g. `transform`, `opacity`, maybe `background-color`.
- Prefer drawer transform entry/exit over layout-affecting right/width animation.
- Use easing appropriate to entering/leaving; avoid sluggish ease-in for opening feedback.
- Add `prefers-reduced-motion: reduce` path: shorten/remove movement while preserving state feedback.
- Do not animate 10,000 row updates.

---

### P2 — Table interaction model is incomplete for keyboard-heavy operations

**Source evidence**

- Keyboard navigation is not described.
- Bulk selection exists in product context but no accessible selection model is shown.

**Runtime hypotheses needing validation**

- Whether `ProductRow` internally implements table/grid roles.
- Whether shortcuts, range selection, and roving focus exist elsewhere.

**Fix**

- Define whether this is a semantic table, grid, or list; implement the corresponding keyboard model.
- Bulk checkboxes need labels, select-all, indeterminate state, and selected count.
- Support range selection if expected by operations staff.
- Keep focus stable after filter, save, row update, and drawer close.
- Announce selected count and batch results accessibly.

---

### P3 — Polish issues should wait until hardening is underway

**Source evidence**

- Blank body, fixed sizing, icon-only controls, broad transitions, and truncation all reduce perceived trust.

**Fix**

- After P0/P1 fixes, tune spacing, density, sticky headers/actions, clearer autosave copy, and consistent disabled/error styling using the existing design system.
- Avoid redesigning the information architecture or introducing new visual language.

---

## 3) Concrete hardening plan by concern

**Hostile data**

- Long names: truncation plus accessible full value and detail view.
- Missing prices: explicit placeholder or validation state.
- Expanded translations: test labels at +60%; avoid fixed text-only button widths.
- Images: reserved dimensions, fallback placeholder, size/type validation, upload progress, retry/cancel.

**Failures**

- Model all listed states: loading, empty, 401/403, 409, 429, 500, timeout, offline, retry, partial batch failure.
- Keep failed edits recoverable.
- Distinguish “not saved,” “saving,” “saved,” and “save failed.”

**Responsive layout**

- Keep desktop density but define tablet compact behavior.
- Replace hard page minimum with intentional overflow or adaptive columns.
- Clamp drawer to viewport and prevent it from hiding critical status/actions.

**Accessibility**

- Focus trap, background inertness, focus return, labeled icon buttons.
- Visible `:focus-visible`.
- Dialog semantics, live save status, semantic table/grid structure.
- Keyboard selection, edit, close, and save paths.

**State recovery**

- Dirty-state guard on close/navigation.
- Retry failed saves without losing edits.
- Conflict flow for 409.
- Offline-safe draft retention where product policy permits.
- Request sequencing to avoid stale response overwrite.

**Performance**

- Virtualize/window rows.
- Defer or memoize filtering.
- Bound image work.
- Memoize rows and callbacks where it reduces actual re-render cost.
- Avoid animating layout or large row sets.

---

## 4) Static detector-like signals: decisive vs context-dependent

**Decisive within the supplied code/notes**

- `catch {}` swallows save errors in the shown save path.
- `rows.map(...)` renders all current rows in the shown page.
- The supplied CSS removes icon-button outline without showing a replacement.
- `transition: all 300ms ease-in` is explicitly broad.
- `min-width: 1180px`, fixed drawer `520px`, and `100vh` are explicit static constraints.
- The source notes explicitly state missing loading/error/empty states, absent focus trap, no background interaction lock, no reduced motion, and synchronous filtering.

**Needs project/runtime context before becoming a final claim**

- Actual frame rate, input latency, and scroll smoothness.
- Whether global CSS restores focus styles.
- Whether icon-only controls have hidden accessible names.
- Whether row components use semantic table/grid roles.
- Whether layout shift occurs from real images.
- Whether server/API layers provide retries, idempotency, auth handling, or conflict prevention.
- Whether fixed minimum width is an approved tablet strategy with horizontal scrolling.
- Whether existing design tokens already define drawer width, hit targets, and motion policy.

---

## 5) Measurement-first validation, acceptance, and rollback

**Baseline before changes**

- Measure initial render time, DOM node count, memory, and scroll responsiveness with 10,000 rows.
- Measure filter keystroke latency p50/p95 on representative hardware.
- Record row re-render counts during filter, selection, drawer open, and save.
- Test image-heavy data: absent images, large images, slow decode, upload failure.
- Exercise save matrix: success, 409, 429, 500, timeout, offline, partial batch failure.
- Keyboard-only pass: open drawer, edit, save, close, return focus, bulk select.
- Screen-reader-oriented semantic pass: labels, dialog name, status announcements.
- Tablet viewport pass at supported widths.
- Reduced-motion pass.

**Acceptance conditions**

- Save failures are visible, recoverable, and do not falsely report saved state.
- Dirty edits survive retry, close guard, offline/timeout, and conflict paths.
- Drawer traps focus, labels icon controls, prevents background interaction, and returns focus.
- Keyboard users can filter, select, edit, save, and recover from errors.
- 10,000-row rendering is bounded; filter input remains responsive under target data.
- Images do not cause avoidable layout shifts or row-height jumps.
- Tablet behavior is intentional and documented.
- Reduced motion preserves state clarity without unnecessary movement.
- Existing design system and workflow remain intact.

**Rollback conditions**

- Roll back virtualization/filter changes if selection, focus retention, row height, or scroll position becomes unreliable.
- Roll back drawer behavior changes if they block recovery or trap users during errors.
- Roll back autosave changes if request ordering or conflict handling risks overwriting newer data.
- Keep failure visibility and data-preservation fixes as non-negotiable unless they introduce a worse correctness bug.

**Release approach**

- Ship behind small, separable gates: save-state hardening, drawer accessibility, table performance, image handling, responsive polish.
- Compare each gate against baseline measurements.
- Do not declare performance success from static code alone; require measured improvement on representative data and devices.
