# Blind comparative judgment
Judge only the supplied outputs. Do not infer which skill produced a label. Apply the machine-readable scorecard exactly, recompute each total from criterion points, and return only JSON matching the supplied schema.

## Task prompt

# Inventory editor production audit

Perform a read-only production audit of this static React product-surface
description. Do not edit files or claim that a detector, browser, build,
profiler, accessibility tree, network throttle, or device run actually
occurred. Do not name, cite, or reveal any skill, repository, author, or
upstream source in the response; the output will be judged blind.

Product context:

- Desktop-first inventory editor used by operations staff, with tablet support.
- The route contains filters, a 10,000-row product table, bulk selection, an
  edit drawer, image uploads, and an autosave status.
- The existing design system and workflow must be preserved; this is a
  production hardening/polish task, not a redesign or new dependency pitch.

Observed source facts:

```tsx
function InventoryPage() {
  const [rows, setRows] = useState(allRows);
  const [saving, setSaving] = useState(false);

  async function saveProduct(product) {
    setSaving(true);
    try {
      await api.save(product);
    } catch {}
    setSaving(false);
  }

  return (
    <div className="page">
      <Filters />
      {rows.map((row) => <ProductRow key={row.id} row={row} />)}
      <EditDrawer onSave={saveProduct} saving={saving} />
    </div>
  );
}
```

```css
.page { min-width: 1180px; }
.product-row { display: grid; grid-template-columns: 64px 280px 1fr 120px 96px; }
.product-row, .drawer { transition: all 300ms ease-in; }
.product-name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.drawer { position: fixed; right: 0; width: 520px; height: 100vh; }
.icon-button { width: 28px; height: 28px; outline: none; }
```

Additional source notes:

- Initial and filter loading render a blank table body.
- Empty results, 401/403, 409 conflict, 429, 500, timeout, offline, retry, and
  partial batch failure states are not represented.
- Product names may be 1-200 characters; prices may be missing; translations
  may expand labels by 60 percent; some images are absent or 8MB.
- The drawer traps neither focus nor background interaction. Escape closes it
  even while a save is pending. Save and close are icon-only.
- All 10,000 rows render at once; filtering recalculates synchronously on every
  keystroke. Image dimensions are not reserved.
- Tablet behavior, keyboard navigation, screen-reader labels, focus-visible,
  reduced motion, and permission-specific affordances are not described.

Return:

1. The correct audit/polish/harden/optimize sequencing and one-line verdict.
2. Prioritized P0-P3 findings with source evidence versus runtime hypotheses.
3. Concrete fixes for hostile data, failures, responsive layout,
   accessibility, state recovery, and performance.
4. Reconcile which static detector-like signals are decisive and which need
   project/runtime context.
5. A measurement-first validation plan with rollback/acceptance conditions.

Stay within 180 lines. Do not turn this into a ground-up redesign.


## Human-readable scorecard

# Comparative scorecard

Generated from `scorecard.json`; do not edit by hand.

| Criterion | Weight | Full credit |
|---|---:|---|
| Mode sequencing and prioritization | 10 | Chooses audit before targeted polish, hardening, and measured optimization with coherent P0-P3 severity. |
| Hostile data and failure hardening | 20 | Covers long and missing data, permissions, conflicts, limits, offline, retry, partial failures, uploads, and truthful save recovery. |
| Responsive and accessibility quality | 15 | Repairs fixed geometry, drawer interaction, keyboard, focus, labels, touch targets, translations, reduced motion, and tablet adaptation. |
| Measurement-first performance | 15 | Identifies render, filter, image, and layout hot paths and requires baselines, thresholds, and rollback conditions. |
| Detector and design-system reconciliation | 10 | Treats static anti-patterns as contextual signals under project authority instead of fabricated runtime proof. |
| Concrete production fixes | 20 | Provides implementation-ready state, error, layout, accessibility, scale, and recovery moves with acceptance conditions. |
| Evidence honesty and scope control | 10 | Separates static proof from hypotheses, claims no unrun tools, stays read-only, and avoids redesign or unjustified dependencies. |
| **Total** | **100** | |


## Machine-readable scorecard

```json
{
  "schema": "design-craft.comparative-scorecard.v1",
  "total": 100,
  "criteria": [
    {
      "id": "mode_sequence",
      "label": "Mode sequencing and prioritization",
      "weight": 10,
      "full_credit": "Chooses audit before targeted polish, hardening, and measured optimization with coherent P0-P3 severity."
    },
    {
      "id": "hostile_data",
      "label": "Hostile data and failure hardening",
      "weight": 20,
      "full_credit": "Covers long and missing data, permissions, conflicts, limits, offline, retry, partial failures, uploads, and truthful save recovery."
    },
    {
      "id": "responsive_accessibility",
      "label": "Responsive and accessibility quality",
      "weight": 15,
      "full_credit": "Repairs fixed geometry, drawer interaction, keyboard, focus, labels, touch targets, translations, reduced motion, and tablet adaptation."
    },
    {
      "id": "measured_performance",
      "label": "Measurement-first performance",
      "weight": 15,
      "full_credit": "Identifies render, filter, image, and layout hot paths and requires baselines, thresholds, and rollback conditions."
    },
    {
      "id": "detector_reconciliation",
      "label": "Detector and design-system reconciliation",
      "weight": 10,
      "full_credit": "Treats static anti-patterns as contextual signals under project authority instead of fabricated runtime proof."
    },
    {
      "id": "production_fixes",
      "label": "Concrete production fixes",
      "weight": 20,
      "full_credit": "Provides implementation-ready state, error, layout, accessibility, scale, and recovery moves with acceptance conditions."
    },
    {
      "id": "evidence_scope",
      "label": "Evidence honesty and scope control",
      "weight": 10,
      "full_credit": "Separates static proof from hypotheses, claims no unrun tools, stays read-only, and avoids redesign or unjustified dependencies."
    }
  ]
}
```

## Required judgment schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["results", "winner", "rationale"],
  "properties": {
    "results": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": {
        "type": "object",
        "required": ["label", "criteria", "total", "summary"],
        "properties": {
          "label": {"enum": ["A", "B", "C"]},
          "criteria": {
            "type": "object",
            "required": [
              "mode_sequence",
              "hostile_data",
              "responsive_accessibility",
              "measured_performance",
              "detector_reconciliation",
              "production_fixes",
              "evidence_scope"
            ],
            "additionalProperties": false,
            "properties": {
              "mode_sequence": {"type": "integer", "minimum": 0, "maximum": 10},
              "hostile_data": {"type": "integer", "minimum": 0, "maximum": 20},
              "responsive_accessibility": {"type": "integer", "minimum": 0, "maximum": 15},
              "measured_performance": {"type": "integer", "minimum": 0, "maximum": 15},
              "detector_reconciliation": {"type": "integer", "minimum": 0, "maximum": 10},
              "production_fixes": {"type": "integer", "minimum": 0, "maximum": 20},
              "evidence_scope": {"type": "integer", "minimum": 0, "maximum": 10}
            }
          },
          "total": {"type": "integer", "minimum": 0, "maximum": 100},
          "summary": {"type": "string", "minLength": 20}
        },
        "additionalProperties": false
      }
    },
    "winner": {"enum": ["A", "B", "C"]},
    "rationale": {"type": "string", "minLength": 40}
  },
  "additionalProperties": false
}
```

## Output A

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


## Output B

## 1. Sequencing + verdict

**Correct sequence:** static audit → P0/P1 production hardening → performance optimization → responsive/accessibility polish → measured regression audit.

**Verdict:** Not release-ready for operations use: the current surface risks silent data loss, inaccessible drawer interactions, and severe 10,000-row responsiveness failures; this is a hardening/optimization pass, not a redesign.

---

## 2. Prioritized findings: evidence vs. runtime hypotheses

### P0 — Blocking

**P0.1 Silent save failure creates false success**
- **Static evidence:** `catch {}` swallows all save errors; `setSaving(false)` runs after failure with no error state, retry, rollback, or user message.
- **Impact:** Operators can believe a product was saved when it was not.
- **Runtime hypothesis:** Exact autosave UI copy/status is unknown, but the provided save path has no represented failure branch.

**P0.2 Unsafe save/close lifecycle can lose edits**
- **Static evidence:** Drawer closes on Escape even while save is pending; drawer does not trap focus or background interaction.
- **Impact:** Pending or dirty edits may be abandoned, duplicated, or saved against stale context.
- **Runtime hypothesis:** Actual draft persistence is not shown; if none exists, this is a data-loss path.

**P0.3 Required production failure states are absent**
- **Static evidence:** Empty results, 401/403, 409 conflict, 429, 500, timeout, offline, retry, and partial batch failure states are explicitly not represented.
- **Impact:** Operators cannot distinguish “no data,” “not allowed,” “stale conflict,” “rate limited,” and “system failed.”
- **Runtime hypothesis:** Backend may emit these states correctly, but the product surface currently has no described UI contract for them.

---

### P1 — Major

**P1.1 10,000 rows render synchronously**
- **Static evidence:** `{rows.map(...)}` renders every row; notes say filtering recalculates synchronously on every keystroke.
- **Impact:** Typing, bulk selection, drawer edits, and scrolling are likely to jank or freeze on realistic hardware.
- **Runtime hypothesis:** Actual frame drops require measurement, but the implementation pattern is a known hot path.

**P1.2 Drawer is not accessible as a modal editing surface**
- **Static evidence:** No focus trap, no background interaction lock, Escape closes during pending save, icon-only Save/Close.
- **Impact:** Keyboard and screen-reader users can lose context, tab behind the drawer, or activate destructive/ambiguous controls.
- **Runtime hypothesis:** Hidden labels may exist elsewhere, but the notes explicitly say labels and keyboard behavior are not described.

**P1.3 Focus visibility is suppressed**
- **Static evidence:** `.icon-button { outline: none; }`; no replacement `:focus-visible` state is described.
- **Impact:** Keyboard-heavy operators lose their position, especially in dense rows and drawer actions.
- **Runtime hypothesis:** Another stylesheet could restore focus, but this rule is a decisive risk until proven otherwise.

**P1.4 Tablet support is structurally unplanned**
- **Static evidence:** `.page { min-width: 1180px; }`; fixed 520px drawer; fixed table columns.
- **Impact:** Tablet users may get horizontal overflow, clipped drawer content, or unusable touch controls.
- **Runtime hypothesis:** A parent shell could provide scrolling, but that is not equivalent to tablet adaptation.

**P1.5 Hostile product data is not contained**
- **Static evidence:** Product names can reach 200 chars; prices may be missing; labels can expand 60%; images can be absent or 8MB.
- **Impact:** Rows can lose meaning, controls can overflow, missing prices can be mistaken for zero, and images can cause layout shift or slow rendering.
- **Runtime hypothesis:** API normalization or CDN processing may help, but the UI layer still needs explicit display rules.

**P1.6 Permission-specific affordances are missing**
- **Static evidence:** 401/403 and permission-specific affordances are not represented.
- **Impact:** Users may attempt actions they cannot complete or misinterpret authorization as system failure.
- **Runtime hypothesis:** Role data may exist elsewhere; the surface still needs visible disabled/hidden/action-reason states.

---

### P2 — Minor but important

**P2.1 Blank initial/filter loading state**
- **Static evidence:** Initial and filter loading render a blank table body.
- **Impact:** Operators cannot tell whether data is loading, filtered out, broken, or delayed.
- **Runtime hypothesis:** Duration determines severity; even short blanks undermine trust in repeated workflows.

**P2.2 Global `saving` state is too coarse**
- **Static evidence:** Single `saving` boolean for the page/drawer.
- **Impact:** One save can disable or mislabel unrelated actions; concurrent edits have no per-product status.
- **Runtime hypothesis:** If only one product can ever be edited, impact is smaller, but autosave and bulk operations usually need scoped state.

**P2.3 `transition: all 300ms ease-in` is too broad**
- **Static evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`
- **Impact:** Layout/color/size changes can animate accidentally; 300ms ease-in feels delayed for operations UI and may hurt performance.
- **Runtime hypothesis:** Actual animated properties depend on state changes, but `all` is a static anti-pattern.

**P2.4 Reduced motion is absent**
- **Static evidence:** No `prefers-reduced-motion` handling described.
- **Impact:** Users requesting reduced motion still receive drawer/row transitions.
- **Runtime hypothesis:** Global CSS may exist, but this component-level motion needs an explicit fallback.

---

### P3 — Polish

**P3.1 Ellipsis alone may hide critical product identity**
- **Static evidence:** `.product-name` truncates with ellipsis.
- **Impact:** Operators may not distinguish similar SKUs without a title/detail affordance or secondary identifier.
- **Runtime hypothesis:** ProductRow may show SKU/image elsewhere; verify with real dense data.

**P3.2 28px icon buttons are cramped**
- **Static evidence:** `.icon-button { width: 28px; height: 28px; }`
- **Impact:** Fine for mouse precision, weak for tablet and accessibility; increases mis-taps.
- **Runtime hypothesis:** Hit area could be larger via padding, but the declared box is below common touch target expectations.

---

## 3. Concrete fixes

### Hostile data
- Define display contracts for every nullable/long field:
  - Missing price: show “Not priced” or an em dash with a tooltip/explanation; never silently render blank or `0`.
  - Long product names: preserve table density with truncation, but expose full name via accessible title/details cell.
  - Expanded translations: reserve flexible label space; avoid fixed labels that assume English length.
  - Missing images: stable placeholder with meaningful alt text or decorative handling when appropriate.
  - 8MB images: use server/CDN thumbnails for the table, validate upload size/type, show upload progress, errors, and retry.
- Reserve image dimensions/aspect ratio in rows and drawer to prevent layout shift.

### Failures and recovery
- Replace `catch {}` with explicit save states: `idle → dirty → saving → saved | error | conflict | offline | rateLimited`.
- Persist the edited draft until the server confirms success.
- On timeout/offline/429/500: keep changes visible, show retry, and avoid claiming saved.
- On 409 conflict: show “server version changed” with compare/overwrite/reload choices.
- On partial batch failure: show counts, failed row identities, reasons, and retry only failed items.
- On 401/403: show permission-specific messaging and disable/hide actions with a reason.

### Drawer lifecycle
- While save is pending:
  - Disable Escape close, or convert it into a confirmation that preserves the draft.
  - Prevent background edits that can invalidate the drawer context.
  - Keep Save/Close labels available to assistive tech and visible enough for keyboard-heavy users.
- Restore focus to the invoking row/control after close.
- If dirty changes exist, require save/discard confirmation.

### Responsive layout
- Do not rely on `min-width: 1180px` as the tablet strategy.
- Keep the desktop workflow, but add structural breakpoints:
  - Desktop: dense table + side drawer.
  - Tablet landscape: table with horizontal overflow only for data columns, sticky identity/actions, drawer width capped by viewport.
  - Tablet portrait: drawer becomes near-full-width overlay or full-screen edit panel.
- Use `max-width: min(520px, 100vw)` or equivalent for the drawer; account for safe areas.
- Ensure touch targets are at least 44px where tablet interaction is supported.

### Accessibility
- Give icon-only Save/Close accessible names; consider visible text where space allows.
- Add focus trap, `aria-modal`/dialog semantics, background inerting, and focus restoration for the drawer.
- Restore visible keyboard focus with `:focus-visible`; never remove outline without replacement.
- Define keyboard behavior for table navigation, selection, edit open/close, save, cancel, and bulk actions.
- Ensure loading, error, conflict, and autosave status changes are announced without being noisy.
- Add reduced-motion CSS: disable or shorten nonessential transitions; preserve instant state feedback.

### Performance
- Virtualize the 10,000-row table or otherwise render only visible rows plus overscan.
- Memoize row components and derived filtered data; keep selection/save state scoped to avoid rerendering every row.
- Debounce or defer filter keystrokes; cancel stale filter/save requests where applicable.
- Avoid `transition: all`; animate only `transform` and `opacity` for drawer movement.
- Lazy-load row images, reserve dimensions, and use thumbnails.
- Keep bulk selection operations set-based and avoid cloning/sorting the full row array on every interaction.

---

## 4. Static signals: decisive vs. needing runtime context

### Decisive from the provided source/facts
- `catch {}` with no error state is a real silent-failure path.
- Rendering `rows.map(...)` for 10,000 rows is a real scalability risk.
- Synchronous filtering on every keystroke is a real input hot path.
- `transition: all` is a real implementation smell.
- `outline: none` without described replacement is a real accessibility risk.
- `min-width: 1180px`, fixed grid columns, and fixed 520px drawer are real responsive risks.
- Missing represented states for auth, conflict, rate limit, offline, timeout, empty, retry, and partial failure is a real production-state gap.

### Needs project/runtime context before final severity locking
- Exact frame time, memory use, and input delay on target hardware.
- Whether `ProductRow` internally uses table/grid semantics, memoization, labels, or image sizing.
- Whether global styles restore focus-visible or reduced-motion behavior.
- Whether image processing, thumbnailing, and upload validation happen outside this surface.
- Whether API saves are idempotent, abortable, retry-safe, and conflict-aware.
- Whether permission metadata is available client-side.
- Whether tablet support means full editing parity or limited review/edit workflows.

---

## 5. Measurement-first validation plan

### Baseline before fixes
- Create fixtures for: 10,000 rows, 200-character names, missing prices, 60% longer labels, absent images, 8MB uploads, auth failures, conflicts, offline, timeout, 429, 500, and partial batch failure.
- Record current interaction budgets for initial render, filter typing, row selection, drawer open/close, save, upload, and bulk actions.
- Capture keyboard-only task completion paths for filtering, selecting, opening drawer, saving, handling errors, and closing.

### Acceptance conditions
- **Data safety:** no save failure is silent; dirty edits survive failed saves; pending saves cannot be accidentally dismissed without preservation/confirmation.
- **Failure clarity:** every listed production state has a distinct UI state, operator-readable copy, and next action.
- **Performance:** 10,000-row filtering and selection remain responsive on target desktop hardware; tablet remains usable with defined row/image budgets.
- **Accessibility:** drawer traps focus, restores focus, exposes named controls, preserves visible focus, supports Escape safely, and announces status changes appropriately.
- **Responsive:** supported tablet widths have no inaccessible controls, clipped drawer actions, or unusable fixed-width assumptions.
- **Motion:** reduced-motion mode preserves state feedback without unnecessary transitions.

### Rollback conditions
- Roll back or feature-flag virtualization if bulk selection, row identity, keyboard navigation, or scroll restoration regresses.
- Roll back drawer lifecycle changes if operators cannot recover drafts or if save/cancel semantics become ambiguous.
- Roll back image/upload changes if upload success rate or preview reliability drops.
- Do not ship polish-only changes until P0 data integrity and P1 performance/accessibility risks are resolved.


## Output C

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
