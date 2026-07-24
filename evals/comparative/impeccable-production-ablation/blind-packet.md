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


## Output B

## 1. Sequencing + verdict

**Correct sequence:** audit the existing surface → harden data/failure/state recovery → optimize table/filter/image hot paths → repair accessibility/responsive behavior → polish motion and copy inside the current design system.

**One-line verdict:** Not release-ready for production operations use: the surface has blocking save-state, accessibility, failure-state, and large-table performance risks, but it can be hardened without a redesign or new visual system.

---

## 2. Prioritized findings

### P0 — Blocking / data-loss / task-completion risks

**P0. Silent save failure and false confidence after failed persistence**  
- **Source evidence:** `catch {}` swallows all save errors; no 401/403, 409, 429, 500, timeout, offline, retry, or partial batch failure states are represented.  
- **Impact:** Operators may believe edits were saved when they were not; conflicts and permission failures become invisible.  
- **Runtime hypothesis:** Exact loss rate depends on API behavior and autosave semantics, but the source already proves failures are not surfaced.

**P0. Drawer can close during pending save with no recovery path**  
- **Source evidence:** Escape closes the drawer even while save is pending; drawer has no focus trap or background interaction lock.  
- **Impact:** Users can interrupt or lose context during a save, background controls can be activated accidentally, and keyboard users may leave the editing flow unintentionally.  
- **Runtime hypothesis:** Whether data is actually lost depends on API/draft handling, but the interaction is unsafe as described.

**P0. Icon-only save/close without described accessible names**  
- **Source evidence:** Save and close are icon-only; screen-reader labels are not described.  
- **Impact:** Assistive-tech users may not know which action saves, closes, cancels, or is currently pending.  
- **Runtime hypothesis:** If hidden labels or `aria-label`s exist outside the snippet, severity drops; static description says they are not represented.

---

### P1 — Major production hardening issues

**P1. 10,000 rows render synchronously**  
- **Source evidence:** `{rows.map(...)}` renders all rows; notes confirm all 10,000 rows render at once.  
- **Impact:** Slow first render, expensive reconciliation, poor keyboard interaction, high memory use, and likely input jank.  
- **Runtime hypothesis:** Actual frame cost depends on row complexity and device class, but this is a decisive hot-path risk.

**P1. Filtering recalculates synchronously on every keystroke**  
- **Source evidence:** Notes state filtering recalculates synchronously on every keystroke.  
- **Impact:** Search/filter input can block, especially with 10,000 rows, image cells, formatting, or multi-column predicates.  
- **Runtime hypothesis:** Needs measurement for exact threshold, but the architecture is wrong for the stated scale.

**P1. Blank table body during initial/filter loading**  
- **Source evidence:** Initial and filter loading render a blank table body.  
- **Impact:** Users cannot distinguish loading, empty results, permissions failure, network failure, or a broken page.  
- **Runtime hypothesis:** If a global loader exists elsewhere it may soften first load, but filter-state blankness remains a local problem.

**P1. Missing empty, auth, conflict, rate-limit, server, timeout, offline, retry, and partial-failure states**  
- **Source evidence:** Explicitly listed as not represented.  
- **Impact:** Production operators get dead ends instead of recovery paths. Bulk edits become especially risky.  
- **Runtime hypothesis:** API may return structured errors, but UI currently has nowhere to present them.

**P1. Drawer is not a real modal/dialog interaction**  
- **Source evidence:** No focus trap, no background interaction lock, fixed right drawer.  
- **Impact:** Keyboard users can tab behind it; screen-reader users may not understand context; accidental background edits are possible.  
- **Runtime hypothesis:** If the drawer is meant to be non-modal, then background interaction must be intentionally designed and announced; current notes say neither.

**P1. Tablet support conflicts with fixed desktop layout**  
- **Source evidence:** `.page { min-width: 1180px; }`; drawer fixed width `520px`; row columns hard-coded.  
- **Impact:** Tablet users likely get horizontal overflow, clipped content, or an oversized drawer.  
- **Runtime hypothesis:** Some tablets in landscape may fit 1180px CSS pixels; portrait and zoomed/text-scaled modes likely fail.

**P1. Touch targets are too small**  
- **Source evidence:** `.icon-button { width: 28px; height: 28px; }`.  
- **Impact:** Poor tablet usability and accessibility; close/save become easy to miss.  
- **Runtime hypothesis:** If padding expands the hit area elsewhere, severity drops; static CSS shows the target itself is undersized.

**P1. Focus visibility is actively removed**  
- **Source evidence:** `.icon-button { outline: none; }`; focus-visible behavior is not described.  
- **Impact:** Keyboard users lose location and control confidence.  
- **Runtime hypothesis:** If an equivalent `:focus-visible` ring exists elsewhere, severity drops; static CSS is a strong negative signal.

**P1. Hostile data is not accommodated**  
- **Source evidence:** product names up to 200 chars, prices may be missing, labels may expand 60%, images can be absent or 8MB; CSS truncates names to one line.  
- **Impact:** Operators may lose distinguishing product details, see broken price/image cells, or encounter layout overflow in translated locales.  
- **Runtime hypothesis:** Some may be handled in `ProductRow`, but no states are described.

**P1. Images do not reserve dimensions**  
- **Source evidence:** Image dimensions are not reserved.  
- **Impact:** Layout shift during load; row heights and pointer targets can move while operators work.  
- **Runtime hypothesis:** Exact shift depends on image placement and caching, but the risk is decisive from the note.

---

### P2 — Important quality and resilience gaps

**P2. Global `saving` state is too coarse**  
- **Source evidence:** single `saving` boolean controls `EditDrawer`.  
- **Impact:** Concurrent saves, autosave, row-specific status, and batch partial failure cannot be represented accurately.  
- **Runtime hypothesis:** If only one product can ever save at a time, this is less severe but still weak for autosave/bulk workflows.

**P2. `setSaving(false)` is not protected by `finally` or lifecycle guards**  
- **Source evidence:** save flow manually resets after `try/catch`.  
- **Impact:** Future early returns, aborts, or thrown code around the save path can strand saving state.  
- **Runtime hypothesis:** Current snippet resets after the empty catch, but the pattern is fragile.

**P2. `transition: all 300ms ease-in` on rows and drawer**  
- **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`.  
- **Impact:** Accidental animation of layout, width, height, grid, color, shadow, or position; slower perceived state changes; possible jank in a large table.  
- **Runtime hypothesis:** Actual harm depends on which properties change, but `all` on repeated rows is a strong anti-pattern.

**P2. Reduced motion is absent**  
- **Source evidence:** reduced motion not described; transitions apply broadly.  
- **Impact:** Motion-sensitive users cannot opt out; state changes may be uncomfortable or distracting.  
- **Runtime hypothesis:** A global stylesheet could override this, but no evidence is provided.

**P2. Permission-specific affordances are missing**  
- **Source evidence:** permission-specific affordances are not described; 401/403 states missing.  
- **Impact:** Users may attempt unavailable edits, hit silent failures, or misunderstand read-only inventory states.  
- **Runtime hypothesis:** Backend may enforce permissions, but UI affordance is still required.

**P2. Bulk selection failure semantics are unspecified**  
- **Source evidence:** route includes bulk selection; partial batch failure states are absent.  
- **Impact:** Operators cannot know which products succeeded, failed, or require retry.  
- **Runtime hypothesis:** Needs product-specific batch behavior, but the missing state model is a clear risk.

---

### P3 — Polish / consistency issues

**P3. One-line truncation may hide critical disambiguators**  
- **Source evidence:** `.product-name` truncates with ellipsis.  
- **Impact:** Similar long product names may become indistinguishable.  
- **Runtime hypothesis:** If a drawer/details view exposes the full name on focus/selection, this is acceptable.

**P3. Motion duration/easing feels sluggish for repetitive operations**  
- **Source evidence:** `300ms ease-in`.  
- **Impact:** Drawer and row state changes may feel delayed in keyboard-heavy workflows.  
- **Runtime hypothesis:** Subjective; validate with task timing and operator feedback.

---

## 3. Concrete fixes

### Hostile data
- Render missing price as a deliberate state: `—`, “Not priced”, or permission-aware copy, not blank/zero.
- Preserve full product names through accessible expansion: full name in drawer/header, row title on focus, or two-line wrap at wider row heights where appropriate.
- Use resilient columns: `minmax()` for translated labels, avoid fixed text-only assumptions, and test 60% expansion.
- For absent images: stable placeholder with the same reserved dimensions as loaded images.
- For 8MB images: validate size/type before upload, show progress, support cancel/retry, and surface compression/server rejection errors.

### Failures and save behavior
- Replace `catch {}` with typed error handling and user-visible status.
- Use `try/catch/finally`; track save state per product or per draft, not only globally.
- Represent: unauthorized, forbidden, conflict, rate-limited, server error, timeout, offline, retrying, saved, unsaved, saving, and partially saved.
- Add conflict handling with version/ETag semantics: “server changed since you opened this,” show safe merge/reload choices.
- Prevent Escape/close while saving, or require confirmation if unsaved/pending changes exist.
- Add retry with backoff for transient failures; do not auto-retry permission/conflict errors.
- For batch edits, return a result summary: succeeded, failed, skipped, retryable, not permitted.

### Responsive layout
- Remove unconditional `min-width: 1180px`; use a table viewport strategy instead.
- For desktop: preserve dense table with sticky header and useful pinned columns.
- For tablet: allow horizontal table scroll within the table region, not the whole page, or switch to a denser stacked row pattern only at clear breakpoints.
- Make drawer width responsive: e.g. bounded `min(520px, 100vw)` plus tablet full-height/full-width behavior when needed.
- Increase icon hit areas to at least 44×44 CSS px while preserving visual density with inner icons.
- Verify translated labels and text scaling do not clip primary actions.

### Accessibility
- Treat the drawer as a dialog if it blocks editing context: role/name, focus trap, initial focus, inert background, focus return on close.
- If non-modal, explicitly support background interaction and announce relationship to selected row.
- Add accessible names to save/close icon buttons; include pending state with `aria-disabled`/disabled and live status text.
- Restore visible focus using `:focus-visible`; never remove outline without equivalent replacement.
- Provide keyboard navigation for row selection, bulk selection, drawer open/close, save, cancel, and filter traversal.
- Announce autosave status changes politely; errors should be discoverable and not vanish.
- Ensure image cells have appropriate alt behavior: product image alt when meaningful, empty alt for decorative placeholders.

### State recovery
- Keep a draft model separate from persisted row data.
- Persist unsaved draft locally or in route state if accidental close/reload is plausible.
- Add “last saved” timestamp and failed-save recovery message.
- On reconnect, show queued changes and allow retry/discard.
- Do not overwrite local edits with stale server responses.
- On auth expiration, preserve draft and route users through re-auth without losing edits.

### Performance
- Virtualize the 10,000-row table; render only visible rows plus overscan.
- Memoize row components and derived cell formatting; keep callbacks stable.
- Move filtering to memoized derived data keyed by filter state; use debouncing or deferred input so typing stays responsive.
- For expensive multi-column filtering, consider indexing or workerized filtering before adding dependencies.
- Reserve image dimensions, lazy-load offscreen images, and avoid decoding large images on the critical path.
- Replace `transition: all` with specific properties such as `transform`, `opacity`, or color tokens only.
- Add `prefers-reduced-motion` handling and shorten product-state transitions to the 150–250ms range.

---

## 4. Static signals: decisive vs context-dependent

### Decisive from the supplied source/notes
- `catch {}` means save errors are swallowed.
- No represented error/empty/offline/conflict states means recovery UX is missing.
- `rows.map(...)` with 10,000 rows means unvirtualized full render.
- Synchronous filtering on every keystroke is a hot-path risk.
- `min-width: 1180px` conflicts with tablet support.
- `width: 28px; height: 28px` is below accessible touch-target expectations.
- `outline: none` without described replacement is an accessibility failure signal.
- Drawer without focus trap/background control is unsafe for modal editing.
- `transition: all` on rows/drawer is over-broad and performance-sensitive.
- Missing reserved image dimensions creates layout-shift risk.

### Needs project/runtime context before final severity
- Whether icon-only buttons already have hidden text or `aria-label`.
- Whether a global focus-visible style overrides `.icon-button`.
- Actual frame time and memory cost of 10,000 rows on supported hardware.
- Whether table semantics are native table, ARIA grid, or plain div rows.
- Whether full product names are available in another reachable view.
- Whether image upload processing is client-side, server-side, CDN-backed, or rejected before render.
- Whether permissions are global route-level, row-level, or action-level.
- Whether drawer is intended to be modal or a non-modal inspector.

---

## 5. Measurement-first validation plan

### Baseline before changes
- Record supported viewport matrix: desktop widths, tablet landscape/portrait, browser zoom, and text scaling.
- Measure initial render time, filter input latency, row scroll smoothness, drawer open/close responsiveness, and image-induced layout shift.
- Capture save-flow timing and failure behavior for success, timeout, offline, 401/403, 409, 429, 500, and partial batch failure.
- Map keyboard path: filters → table rows → bulk selection → drawer → save/close → return focus.
- Inventory hostile data fixtures: 1-char name, 200-char name, missing price, long translations, absent image, 8MB image.

### Acceptance conditions
- No silent save failures; every failed save has visible recovery.
- Pending/unsaved drawer cannot be dismissed accidentally without safe handling.
- Keyboard-only users can complete filter, select, edit, save, close, and recover from errors.
- Focus is visible and restored predictably.
- Initial/filter loading, empty results, auth/permission, conflict, offline, timeout, retry, and partial batch states are represented.
- 10,000-row interactions stay within agreed input-latency and scroll-smoothness budgets on supported devices.
- No major layout shift from images.
- Tablet layout remains usable without whole-page horizontal overflow.
- Reduced-motion users receive equivalent state feedback without broad animation.

### Rollback conditions
- Filter typing becomes slower than baseline.
- Save recovery introduces duplicate writes or stale overwrite risk.
- Virtualization breaks keyboard navigation, selection persistence, or screen-reader row context.
- Responsive changes reduce desktop operator efficiency.
- Drawer focus management traps users or prevents emergency recovery.
- Error handling hides successful saves or creates ambiguous autosave status.

### Safe rollout
- Ship hardening behind narrow flags where possible: save-state model, virtualized table, drawer focus behavior.
- Start with internal/staff dogfood using seeded hostile data.
- Monitor save failures, retries, conflict frequency, abandoned drafts, filter latency, and client errors.
- Keep rollback scoped: table rendering, save workflow, and drawer behavior should be independently reversible.


## Output C

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
