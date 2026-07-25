## 1. Sequencing + verdict

**Correct sequence:** audit evidence → harden correctness and failure handling → stabilize accessibility/state recovery → optimize measured hot paths → apply visual polish within the existing design system.

**One-line verdict:** This surface is not production-hardened for a 10,000-row operations workflow; the main risks are silent data loss, inaccessible drawer/actions, missing failure states, tablet breakage, and unbounded rendering/filtering.

---

## 2. Prioritized findings: evidence vs. runtime hypotheses

### P0 — Must fix before production confidence

#### P0.1 Silent save failure and weak save state recovery  
**Source evidence:**  
```tsx
try {
  await api.save(product);
} catch {}
setSaving(false);
```

**Decisive static signal:** errors are swallowed; no user-visible failure, retry, rollback, conflict handling, or telemetry hook is represented.

**Risk:** operators may believe edits saved when they failed. This is especially dangerous with autosave and bulk workflows.

**Runtime context needed:** whether `api.save` has upstream retries, whether the drawer shows per-field dirty state elsewhere, and whether server-side versioning prevents lost updates.

---

#### P0.2 Missing production failure states  
**Source evidence:** source notes say blank loading body and no states for empty results, 401/403, 409, 429, 500, timeout, offline, retry, or partial batch failure.

**Decisive static signal:** absence of represented branches for critical operational states.

**Risk:** users cannot distinguish “still loading,” “no results,” “not permitted,” “conflict,” “rate limited,” or “data unavailable.”

**Runtime context needed:** exact API error shape and whether failures can occur per row, per product, per image, or per bulk action.

---

#### P0.3 Drawer can lose or corrupt work during pending save  
**Source evidence:** drawer does not trap focus/background interaction; Escape closes it even while save is pending.

**Decisive static signal:** closing during pending mutation is explicitly allowed.

**Risk:** interrupted saves, lost edits, duplicate edits, stale drawer state, or accidental background actions while editing.

**Runtime context needed:** whether close discards local draft, whether save is idempotent, and whether product versions are checked.

---

#### P0.4 Icon-only save/close without described accessible names  
**Source evidence:** save and close are icon-only; screen-reader labels are not described.

**Decisive static signal:** icon-only controls require explicit accessible names.

**Risk:** keyboard and screen-reader users cannot reliably understand or operate primary drawer actions.

**Runtime context needed:** whether the actual icon button component injects `aria-label`, tooltip text as accessible name, or hidden text.

---

### P1 — High-priority hardening

#### P1.1 All 10,000 rows render at once  
**Source evidence:**  
```tsx
{rows.map((row) => <ProductRow key={row.id} row={row} />)}
```
Product context confirms 10,000-row table.

**Decisive static signal:** unbounded row rendering is present in the shown route.

**Risk:** slow initial render, expensive updates, poor keyboard interaction, memory pressure, and jank during filtering.

**Runtime context needed:** row complexity, image behavior, memoization inside `ProductRow`, device class, and actual render timings.

---

#### P1.2 Filtering recalculates synchronously on every keystroke  
**Source evidence:** additional notes state synchronous recalculation on every keystroke.

**Decisive static signal:** known hot path tied to user input.

**Risk:** input lag, dropped keystrokes, blocked autosave/status updates, and degraded tablet performance.

**Runtime context needed:** filter complexity, number of fields searched, locale comparison cost, and whether filtering also mutates selection state.

---

#### P1.3 Fixed desktop minimum width and fixed drawer width break tablet support  
**Source evidence:**  
```css
.page { min-width: 1180px; }
.drawer { position: fixed; right: 0; width: 520px; height: 100vh; }
```

**Decisive static signal:** layout has hard desktop assumptions.

**Risk:** tablet users get horizontal clipping, unreachable controls, obscured table content, or drawer overflow.

**Runtime context needed:** supported tablet widths, whether the page sits inside a scroll container, and whether the design system has responsive drawer/table primitives.

---

#### P1.4 Focus visibility is removed  
**Source evidence:**  
```css
.icon-button { width: 28px; height: 28px; outline: none; }
```

**Decisive static signal:** default focus outline is removed.

**Risk:** keyboard users lose visible focus on critical actions.

**Runtime context needed:** whether a replacement `:focus-visible` style exists elsewhere with sufficient contrast.

---

#### P1.5 Motion is too broad and lacks reduced-motion handling  
**Source evidence:**  
```css
.product-row, .drawer { transition: all 300ms ease-in; }
```
Reduced motion is not described.

**Decisive static signal:** `transition: all` can animate layout, color, size, transform, and other unintended properties.

**Risk:** jank, delayed state response, uncomfortable motion, and unpredictable animation when rows update.

**Runtime context needed:** which properties actually change, whether global reduced-motion CSS exists, and whether the drawer uses transform or layout animation.

---

### P2 — Important production polish and resilience

#### P2.1 Hostile data is not fully handled  
**Source evidence:** names can be 1–200 characters; prices may be missing; translations may expand labels by 60%; images can be absent or 8MB.

**Risk:** truncation hides critical product identity, missing prices look like bugs, translated labels overflow, and large/absent images cause layout instability.

**Runtime context needed:** product naming rules, currency requirements, image CDN behavior, and localized copy length.

---

#### P2.2 Image dimensions are not reserved  
**Source evidence:** additional notes state dimensions are not reserved.

**Risk:** layout shift, row height changes, scroll-position jumps, and slower perceived loading.

**Runtime context needed:** actual image component, thumbnail service, and table row height strategy.

---

#### P2.3 Permission-specific affordances are absent  
**Source evidence:** permission-specific affordances are not described.

**Risk:** users may attempt actions they cannot complete, or unauthorized users may see misleading destructive/edit affordances.

**Runtime context needed:** whether permissions are enforced only server-side or also reflected in UI capabilities.

---

#### P2.4 Autosave status appears global and underspecified  
**Source evidence:** single `saving` boolean shared by `EditDrawer`.

**Risk:** concurrent saves, row-level edits, image uploads, and bulk actions cannot express distinct pending/error/saved states.

**Runtime context needed:** whether only one drawer edit can occur at a time and whether uploads share the same save channel.

---

### P3 — Lower-priority polish after hardening

#### P3.1 Blank loading state weakens operator confidence  
**Source evidence:** blank table body during initial/filter loading.

**Risk:** users may think data disappeared.

---

#### P3.2 Dense icon target size may be hostile on tablet  
**Source evidence:**  
```css
.icon-button { width: 28px; height: 28px; }
```

**Risk:** difficult touch interaction and low error tolerance.

**Runtime context needed:** whether visible size differs from hit area through padding or wrapper styles.

---

## 3. Concrete fixes

### Hostile data

- Render missing prices as an intentional placeholder such as `—` plus accessible text like “No price set,” not an empty cell.
- Preserve product-name truncation for table density, but expose the full name through a non-hover-only mechanism: accessible label, details cell, drawer header, or keyboard-reachable disclosure.
- Test 1-character and 200-character names, long unbroken strings, translated labels at +60%, missing images, and large images.
- Reserve image aspect ratio or fixed thumbnail slots before image load.
- Use product-image placeholders for absent images.
- Prefer thumbnail URLs for table rows; keep full-size images out of the row list.
- Validate uploads before sending: file size, type, dimensions, failure copy, retry affordance.

### Failure handling

Replace `saving: boolean` with explicit mutation state:

```ts
type SaveState =
  | { status: 'idle' }
  | { status: 'saving'; productId: string }
  | { status: 'saved'; productId: string; savedAt: number }
  | { status: 'error'; productId: string; reason: string; retryable: boolean }
  | { status: 'conflict'; productId: string };
```

Handle at minimum:

- **401:** session expired; preserve draft, prompt re-authentication.
- **403:** show permission-specific disabled state and explanation.
- **409:** show conflict state with server/client comparison or reload/apply path.
- **429:** honor retry-after where available; avoid repeated immediate retries.
- **500/timeout:** show retry and preserve unsaved draft.
- **Offline:** queue or hold draft locally; mark “not saved.”
- **Partial batch failure:** report per-row success/failure, not only a global banner.

Also:

- Never swallow save errors.
- Use `finally` for pending cleanup.
- Prevent duplicate submissions while the same product is saving.
- Keep dirty state visible until server acknowledgement.
- Make autosave status specific: “Saving,” “Saved 10:42,” “Couldn’t save,” “Conflict,” “Offline — changes not saved.”

### Responsive layout

- Remove unconditional `min-width: 1180px` from the page shell.
- If the table must remain wide, put horizontal overflow on the table region, not the whole route.
- Keep filters, autosave status, drawer controls, and bulk-action bars reachable without horizontal scrolling.
- Use drawer width like `width: min(520px, 100vw)` or a tablet-specific full-height panel.
- Ensure the drawer does not obscure required save/close controls or trap content below viewport height.
- Define tablet behavior explicitly: which columns collapse, which remain sticky, and how bulk selection remains accessible.

### Accessibility

- Add a real focus trap for the drawer while open.
- Restore focus to the invoking row/action when the drawer closes.
- Prevent background interaction while the drawer is active, using inert/aria-hidden behavior where appropriate.
- Do not allow Escape to close during an irreversible pending save; either block it with explanation or require confirmation if dirty.
- Give icon-only save/close buttons accessible names.
- Restore visible keyboard focus using `:focus-visible`.
- Make autosave changes available through a polite live region.
- Ensure disabled and pending states are announced and visually distinct.
- Provide keyboard navigation for rows, selection, drawer fields, save, close, retry, and bulk actions.
- Add reduced-motion handling:
  - avoid `transition: all`;
  - animate only `transform`/`opacity` where needed;
  - disable or shorten nonessential motion under `prefers-reduced-motion`.

### State recovery

- Preserve unsaved drawer drafts across transient failures.
- Track product version/etag for conflict detection.
- Keep selection stable across filtering where appropriate, with clear counts: selected visible vs. selected total.
- On reload or route change with dirty edits, warn or recover draft.
- For image uploads, separate upload state from product metadata save state.
- Avoid closing or clearing the drawer until save success, explicit discard, or conflict resolution.

### Performance

- Virtualize or window the 10,000-row list/table.
- Keep row heights predictable if possible; if variable, measure carefully and avoid layout thrash.
- Memoize derived filtered rows with correct dependencies.
- Debounce or defer filter input work so typing remains responsive.
- Avoid recreating heavy row props/functions for every row render.
- Memoize `ProductRow` if row props are stable.
- Move expensive search normalization outside the keystroke path where possible.
- Reserve image dimensions and lazy-load below-the-fold thumbnails.
- Avoid animating table rows with broad transitions during bulk updates/filter changes.

---

## 4. Static signals: decisive vs. context-dependent

### Decisive from the supplied source

- `catch {}` means save failures are swallowed at this layer.
- A single `saving` boolean cannot express conflict, retry, offline, partial failure, or multiple concurrent operations.
- `rows.map(...)` renders every row represented by `rows`.
- `transition: all` is unsafe for a large interactive table and drawer.
- `outline: none` removes default focus indication unless replaced elsewhere.
- `min-width: 1180px` and `width: 520px` encode desktop assumptions.
- Blank loading and absent error/empty states are production-state gaps.
- No focus trap/background isolation for the drawer is an accessibility and data-safety gap.
- Closing with Escape during pending save is unsafe without confirmation or recovery.

### Needs project/runtime context

- Exact performance severity of 10,000 rows depends on row complexity, device class, memoization, image loading, and browser behavior.
- Actual accessibility compliance depends on hidden labels, shared button components, global focus styles, and semantic table/grid implementation.
- Permission risk depends on server enforcement and how UI capabilities are derived.
- Tablet severity depends on supported breakpoints and surrounding layout containers.
- Conflict severity depends on backend versioning and whether stale writes are rejected.
- Image impact depends on CDN thumbnails, intrinsic dimensions, caching, and upload pipeline.
- Whether a new virtualization primitive is needed depends on existing design-system/table capabilities.

---

## 5. Measurement-first validation plan with acceptance and rollback

### Baseline before changes

Use a production-like fixture set:

- 10,000 products.
- Long names up to 200 characters.
- Missing prices.
- Missing images.
- Large image references/uploads.
- Expanded translated labels.
- Mixed permissions.
- Simulated 401, 403, 409, 429, 500, timeout, offline, and partial batch failure responses.

### Validate hardening first

Acceptance:

- Save failure is visible and recoverable.
- Draft is not lost on failed save, timeout, offline, conflict, or session expiry.
- Pending save cannot be accidentally dismissed without safe handling.
- Partial batch failure identifies failed rows and next action.
- Empty, loading, forbidden, unauthorized, conflict, rate-limit, server-error, offline, and retry states are distinct.

Rollback condition:

- Any change causes silent save success/failure ambiguity or draft loss.

### Validate accessibility

Acceptance:

- Drawer traps focus while open.
- Focus returns to the opener after close.
- Save/close/retry/bulk actions have accessible names.
- Keyboard-only users can complete filter, select, edit, save, retry, and close flows.
- Visible focus is present and high contrast.
- Reduced-motion mode preserves state feedback without broad animation.
- Autosave status changes are announced without being noisy.

Rollback condition:

- Keyboard path regresses, focus becomes invisible, or background interaction remains possible while drawer is open.

### Validate responsive/tablet behavior

Acceptance:

- Tablet widths keep filters, table controls, drawer actions, autosave, and bulk actions reachable.
- Horizontal scrolling, if required, is limited to the table region.
- Drawer fits the viewport and does not hide primary actions.
- Long labels and translated text do not overlap controls.

Rollback condition:

- Any supported tablet viewport blocks save/close, hides status, or creates whole-page horizontal scrolling that traps core controls.

### Validate performance

Measure before and after:

- Initial table readiness with 10,000 rows.
- Filter keystroke latency.
- Row selection responsiveness.
- Drawer open/close responsiveness.
- Bulk selection update time.
- Scroll smoothness.
- Layout shift from images.
- Memory growth during repeated filtering/editing.

Acceptance targets should be set from current product standards, but minimum production gates should include:

- Filtering does not visibly block typing.
- Scrolling remains stable with 10,000 rows.
- Drawer interaction stays responsive during table updates.
- Image loading does not shift rows unexpectedly.
- Bulk selection does not re-render unrelated heavy content unnecessarily.

Rollback condition:

- Virtualization/windowing breaks selection, keyboard navigation, row focus, or screen-reader semantics.
- Filtering optimization returns stale or incorrect rows.
- Image optimization hides errors or prevents retry.

### Release approach

- Ship in small hardening slices: save/error state machine, drawer accessibility, failure states, responsive containment, then row/filter performance.
- Keep old behavior behind a short-lived rollback path where feasible.
- Monitor save failures, retries, conflicts, abandoned dirty drawers, upload failures, and filter latency after release.
- Do not introduce a new design language or dependency unless existing primitives cannot meet the measured production requirements.
