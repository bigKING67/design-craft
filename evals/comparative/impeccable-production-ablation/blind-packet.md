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

## 1) Correct sequencing + verdict

**Sequencing:** read-only audit → define baseline measurements → harden correctness/recovery/accessibility states → optimize verified hot paths → polish motion/layout details → release validation with rollback gates.

**Verdict:** This surface is not production-ready for a 10,000-row operations workflow until save recovery, drawer accessibility, failure states, and table performance are hardened; the fixes can preserve the existing workflow and design system.

---

## 2) Prioritized findings: source evidence vs runtime hypotheses

| Priority | Finding | Source evidence | Runtime hypothesis / needs verification |
|---|---|---|---|
| **P0** | Save failures can disappear and users can lose edit context. | `catch {}` swallows save errors; no 401/403/409/429/500/timeout/offline states; Escape closes drawer while save is pending. | Need to verify whether upstream APIs retry, whether drafts are persisted elsewhere, and whether concurrent saves can overlap. |
| **P0** | Edit drawer is unsafe for keyboard and assistive-tech users. | Notes say drawer traps neither focus nor background interaction; save/close are icon-only; Escape closes during pending save. | Need runtime focus order, accessible names, and screen-reader tree to confirm exact breakage, but the missing modal contract is decisive within supplied facts. |
| **P1** | The 10,000-row table has an unbounded render/filter hot path. | `rows.map(...)` renders every row; filtering recalculates synchronously on every keystroke; all 10,000 rows render at once. | Actual INP/FPS/memory impact needs measurement, but this is a high-risk production path at the stated scale. |
| **P1** | Loading, empty, permission, conflict, retry, and partial-failure states are absent. | Blank table body during initial/filter loading; listed failure states are not represented. | Need project API semantics to design exact recovery copy/actions, but absence of user-visible states is decisive. |
| **P1** | Tablet and constrained-width behavior are likely broken. | `.page { min-width: 1180px; }`; fixed grid columns; fixed `520px` drawer; `height: 100vh`. | Need viewport runs to confirm clipping/scroll behavior, but fixed geometry conflicts with tablet support. |
| **P2** | Hostile data will degrade scannability and layout stability. | Product names 1–200 chars; labels may expand 60%; prices may be missing; images may be absent or 8MB; image dimensions not reserved. | Need actual row component rendering to confirm wrapping, tooltips, placeholders, and upload constraints. |
| **P2** | Focus and motion implementation are brittle. | `.icon-button { outline: none; }`; `.product-row, .drawer { transition: all 300ms ease-in; }`; reduced motion not described. | Need full CSS to know whether `:focus-visible` exists elsewhere; `transition: all` remains a decisive implementation smell. |
| **P3** | Permission-specific affordances and row-level feedback are underspecified. | Permission-specific affordances not described; single global `saving` state. | Need role matrix and component code to know whether row-level disabled states or read-only explanations exist elsewhere. |

---

## 3) Concrete fixes without redesigning the workflow

### A. Save correctness and state recovery

- Replace `catch {}` with explicit error capture and user-visible recovery.
- Track save state per product or per drawer session, not only one page-level `saving` boolean.
- Keep the drawer open on failed save; preserve the user’s draft.
- While a save is pending:
  - disable destructive close paths or require confirmation;
  - do not allow Escape to silently discard state;
  - show “Saving…”, “Saved”, “Failed — retry”, and “Conflict — review changes”.
- For **409 conflict**:
  - keep local edits;
  - fetch latest server version;
  - show field-level conflict summary;
  - allow retry/overwrite only if product rules permit.
- For **401/403**:
  - preserve draft;
  - show re-auth or permission message;
  - disable save if the user lacks edit permission.
- For **429/timeout/offline/500**:
  - show retry affordance;
  - use bounded retry/backoff where appropriate;
  - avoid duplicate submits;
  - keep autosave status honest.
- For **partial batch failure**:
  - show which rows succeeded, failed, and remain dirty;
  - keep failed selections actionable.

### B. Loading, empty, and failure states

- Replace blank table bodies with stateful table rows:
  - initial loading: skeleton or calm loading row preserving table geometry;
  - filter loading: keep previous results visible with “Updating results…” status;
  - empty results: explain active filters and provide “clear filters” action;
  - error: show retry and preserve filters/selection where safe.
- Autosave status should be tied to actual request state:
  - dirty;
  - saving;
  - saved timestamp;
  - failed;
  - offline queued, if supported.

### C. Hostile data handling

- Product names:
  - preserve single-line density if required, but expose full value through accessible title/details pattern;
  - ensure selection, SKU, and action columns remain stable with 200-character names.
- Prices:
  - render missing values as an explicit neutral state, not `0`, blank, or malformed text.
- Translations:
  - avoid hard-coded label widths for controls;
  - allow filter labels and drawer labels to wrap or use stacked layout at tablet widths.
- Images:
  - reserve width/height or aspect-ratio slots to prevent layout shift;
  - use placeholders for absent images;
  - validate 8MB uploads before upload;
  - show upload progress, failure, retry, and file-size guidance;
  - use thumbnails/object-fit rather than full-size images in table rows.

### D. Responsive layout and tablet support

- Do not make the whole page require `min-width: 1180px`.
- Keep the page shell responsive; isolate unavoidable horizontal overflow to the table region.
- Preserve critical controls outside the horizontal scroll area:
  - filters;
  - bulk actions;
  - autosave status;
  - drawer close/save controls.
- For the table:
  - use a scroll container with sticky header and important identifier columns if already consistent with the system;
  - keep row height predictable.
- For the drawer:
  - use `width: min(520px, 100vw)` or a tablet-specific full-screen/near-full-screen mode;
  - use `height: 100dvh` rather than only `100vh`;
  - account for browser UI and safe-area insets if tablet web is supported.

### E. Accessibility

- Drawer should behave as a modal or explicitly non-modal panel; current facts imply it needs modal behavior:
  - `role="dialog"` or equivalent semantic pattern;
  - accessible name;
  - focus moves into drawer on open;
  - focus is trapped while modal;
  - focus returns to invoking control on close;
  - background is inert or otherwise unavailable to keyboard/screen reader users.
- Save and close icon buttons need accessible names and visible text or tooltip support where appropriate.
- Restore visible focus:
  - remove bare `outline: none`;
  - provide strong `:focus-visible` styling using existing tokens.
- Increase effective hit targets, especially for tablet:
  - 28px visual icon can remain if the interactive target is larger;
  - use a project-approved target size, with 44px as a reasonable tablet comfort baseline.
- Keyboard navigation:
  - define row focus behavior;
  - selection shortcuts;
  - drawer open/close/save order;
  - Escape behavior that does not discard pending or dirty work.
- Announce async state changes with a polite live region:
  - saving;
  - saved;
  - failed;
  - conflict;
  - offline.

### F. Performance

- Virtualize the 10,000-row table or otherwise window visible rows.
- Preserve keyboard selection and row identity across virtualization.
- Memoize row rendering and derived filter results with correct dependencies.
- Avoid synchronous filtering on every keystroke:
  - debounce input where acceptable;
  - use deferred rendering for result updates;
  - precompute normalized searchable fields;
  - consider worker/chunking only if measurement shows main-thread blocking remains.
- Reserve image dimensions and lazy-load thumbnails.
- Replace `transition: all` with specific properties:
  - drawer: transform/opacity where appropriate;
  - row state: color/background/border only if needed;
  - avoid animating layout-affecting properties.
- Add reduced-motion handling:
  - remove non-essential transitions;
  - preserve state feedback through color, text, and position changes.

---

## 4) Static signals: decisive vs context-dependent

### Decisive from supplied source/facts

- `catch {}` means save errors are swallowed in the shown function.
- `rows.map(...)` renders the complete current row set.
- The stated 10,000-row scale makes unbounded rendering a real hot-path risk.
- Blank loading body and missing error/empty/conflict/offline states are absent in the supplied description.
- Fixed `min-width: 1180px`, fixed grid columns, and fixed `520px` drawer are incompatible with robust tablet support unless another layout path exists.
- Drawer lacks focus trap/background isolation per supplied notes.
- Icon-only save/close need accessible names; none are described.
- `transition: all` is unsafe for predictable motion/performance.
- `outline: none` removes default focus indication for `.icon-button`.

### Needs project/runtime context before final severity or exact fix

- Whether a separate CSS rule restores `:focus-visible` after `outline: none`.
- Actual table lag, INP, frame drops, memory pressure, and image-related layout shift.
- Whether API/client layers outside the snippet already handle retries, auth refresh, conflict resolution, or draft persistence.
- Whether concurrent saves can occur and whether one global `saving` boolean causes cross-row blocking or stale status.
- Actual tablet breakage across target viewport sizes.
- Screen-reader output, keyboard order, and live-region behavior.
- Whether permissions are enforced server-side only, client-side, or both.
- Whether virtualization is compatible with existing bulk selection, find-in-page expectations, row heights, and keyboard navigation.

---

## 5) Measurement-first validation plan with rollback and acceptance

### Baseline before changes

Use representative fixtures:

- 10,000 rows;
- 1/50/200-character product names;
- missing prices;
- absent images;
- large image uploads;
- 60% longer translated labels;
- mixed permissions;
- conflict, offline, timeout, 429, 500, and partial batch responses.

Capture baseline targets before selecting final optimization details:

- initial table render time;
- filter keystroke latency and p95 interaction delay;
- drawer open/close latency;
- save success/failure recovery time;
- memory during table use;
- layout shift from images;
- keyboard completion path for edit/save/close;
- tablet viewport reachability.

### Functional acceptance

- No save failure is silent.
- Dirty edits survive failed save, auth interruption, offline transition, and conflict.
- Escape cannot discard pending save state without an explicit safe path.
- Partial batch failure reports per-row outcomes.
- Permission-denied users see read-only or disabled affordances with explanation.

### Accessibility acceptance

- Drawer focus enters, traps, and restores correctly.
- Background is not interactable while modal drawer is active.
- Save/close controls have accessible names.
- All interactive controls have visible focus.
- Keyboard-only user can filter, select rows, open drawer, edit, save, recover from failure, and close.
- Reduced-motion mode preserves feedback without broad animation.

### Performance acceptance

- 10,000-row dataset remains responsive under representative hardware.
- Filtering does not block typing beyond the agreed interaction budget.
- Virtualization/windowing does not break selection, focus, or row identity.
- Images do not cause meaningful layout shift.
- Drawer and row transitions do not animate layout-heavy properties.

### Responsive acceptance

- Tablet target widths keep filters, bulk actions, autosave status, and drawer actions reachable.
- Horizontal overflow, if unavoidable, is confined to the data grid.
- Drawer fits the viewport and remains operable with on-screen keyboard/browser chrome.

### Rollback conditions

- Roll back or feature-flag table virtualization if it breaks selection, keyboard navigation, row measurement, or edit targeting.
- Roll back drawer behavior changes if focus becomes trapped incorrectly or save recovery regresses.
- Roll back upload changes if valid existing image workflows fail.
- Roll back motion changes if reduced-motion users lose state feedback.
- Do not ship if save failure, conflict recovery, keyboard drawer operation, or 10,000-row responsiveness fails acceptance.


## Output B

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


## Output C

## 1) Correct sequencing + verdict

**Sequence:** static production audit → P0 hardening for save/failure/state recovery → accessibility and keyboard repair → performance optimization for 10,000-row paths → responsive/tablet adaptation → final polish only after recovery, a11y, and latency are measurable.

**Verdict:** The surface preserves a recognizable workflow, but in its current static shape it is not production-safe: silent save failure, missing failure states, non-trapped drawer interaction, and unbounded rendering create credible data-loss, accessibility, and latency risks.

---

## 2) Prioritized findings — source evidence vs runtime hypotheses

Legend: **[E] decisive from provided source/static facts** · **[H] requires runtime/project context**

### P0 — Blocking / production safety

1. **Silent save failure can mislead operators into believing edits persisted**  
   - Evidence: **[E]** `catch {}` swallows errors; `setSaving(false)` runs after failure with no error state, retry, rollback, or conflict handling.  
   - Impact: Operators may close the drawer or move to the next product after a failed save, causing inventory drift.  
   - Fix: Return a structured save result: `idle | saving | saved | failed | conflict | offline | rateLimited`. Surface inline error, keep dirty state, offer retry, and prevent “saved” language unless the server acknowledged persistence.

2. **Drawer can close during pending save**  
   - Evidence: **[E]** “Escape closes it even while a save is pending.”  
   - Impact: User can lose context during an unresolved mutation.  
   - Fix: While saving, either block close with clear copy (“Save in progress…”) or allow close only after preserving a recoverable draft and showing persistent pending status.

3. **Conflict and partial batch failure states are absent**  
   - Evidence: **[E]** 409 conflict and partial batch failure states not represented.  
   - Impact: Bulk edits and concurrent inventory changes can overwrite newer data or hide partial failures.  
   - Fix: Add conflict resolution UI: “server changed since you opened,” show changed fields, allow reload/apply-anyway where policy permits, and summarize per-row batch failures with retry for failed rows only.

---

### P1 — Major usability, accessibility, and latency risks

4. **10,000 rows render synchronously**  
   - Evidence: **[E]** `rows.map(...)` renders all rows; note says all 10,000 rows render at once.  
   - Impact: Slow initial render, high memory use, keyboard lag, expensive selection/filter redraws.  
   - Fix: Virtualize/window rows using existing table/list infrastructure if present; preserve keyboard navigation and selection semantics across offscreen rows.

5. **Filtering recalculates synchronously on every keystroke**  
   - Evidence: **[E]** additional note states synchronous recalculation on every keystroke.  
   - Impact: Input lag on the primary “find exceptions quickly” workflow.  
   - Fix: Debounce or defer non-critical filtering, memoize normalized searchable fields, avoid repeated formatting/parsing in the hot path, and keep the input responsive while results update.

6. **Initial/filter loading shows a blank table body**  
   - Evidence: **[E]** blank body during initial and filter loading.  
   - Impact: Looks broken; removes state continuity for operators.  
   - Fix: Use table-shaped skeleton rows for initial load and “updating results…” affordance for filter refresh. Keep previous results visible if safe, with a subtle pending indicator.

7. **No empty/error/auth/rate-limit/offline states**  
   - Evidence: **[E]** empty results, 401/403, 429, 500, timeout, offline, retry states not represented.  
   - Impact: Operators cannot distinguish “no products match” from “system failed” or “permission denied.”  
   - Fix: Add state-specific table panels: empty filter guidance, permission-specific locked affordance, retryable transient failure, rate-limit wait copy, offline queued/draft state.

8. **Drawer lacks focus trap and background interaction lock**  
   - Evidence: **[E]** drawer traps neither focus nor background interaction.  
   - Impact: Keyboard and assistive-tech users can tab behind the drawer or activate stale page controls.  
   - Fix: Use modal/dialog semantics where appropriate: focus initial field, trap focus, restore focus to invoker on close, make background inert, and provide labelled title/description.

9. **Icon-only save/close controls are not described as labelled**  
   - Evidence: **[E]** “Save and close are icon-only”; screen-reader labels not described.  
   - Impact: Assistive-tech users may encounter unnamed buttons.  
   - Fix: Add accessible names, tooltips if already in the system, visible confirmation text for destructive/pending states, and disabled/loading labels that announce status.

10. **Focus indicator has likely been removed**  
   - Evidence: **[E]** `.icon-button { outline: none; }`; focus-visible not described.  
   - Impact: Keyboard-heavy operators lose their position.  
   - Fix: Restore `:focus-visible` using design tokens; never remove outlines without an equivalent visible replacement.

11. **Touch targets are too small for tablet support**  
   - Evidence: **[E]** `.icon-button` is `28px × 28px`; tablet support required.  
   - Impact: Miss-taps and inaccessible controls on touch devices.  
   - Fix: Keep visual icon size if needed, but provide at least a 44px hit area through padding or wrapper sizing.

12. **Fixed desktop minimum width conflicts with tablet support**  
   - Evidence: **[E]** `.page { min-width: 1180px; }`; tablet support required.  
   - Impact: Forced horizontal scrolling or clipped controls on tablets.  
   - Fix: Define tablet behavior explicitly: table horizontal scroll within a contained region, pinned key columns, condensed columns, drawer width as `min(520px, 100vw)`, and preserved bulk actions.

13. **Unreserved image dimensions cause layout shifts**  
   - Evidence: **[E]** image dimensions not reserved; images can be absent or 8MB.  
   - Impact: Table rows jump as images load; large images harm load time and memory.  
   - Fix: Reserve aspect-ratio boxes, show absent-image placeholders, lazy/decode images, enforce upload size validation/compression where product policy allows.

---

### P2 — Important polish/hardening

14. **`transition: all 300ms ease-in` is broad and slow for a work surface**  
   - Evidence: **[E]** `.product-row, .drawer { transition: all 300ms ease-in; }`.  
   - Impact: Animates unintended properties, risks layout jank, and ease-in feels sluggish because it starts slowly.  
   - Fix: Transition only `transform`, `opacity`, or tokenized color where needed; use shorter state motion around 150–250ms; add reduced-motion alternatives.

15. **No reduced-motion path**  
   - Evidence: **[E]** reduced motion not described; transitions exist.  
   - Impact: Motion-sensitive users cannot opt out while retaining state feedback.  
   - Fix: Add `@media (prefers-reduced-motion: reduce)` to shorten/remove movement while preserving instant visual state changes.

16. **Hostile text and i18n expansion are under-specified**  
   - Evidence: **[E]** names may be 1–200 chars; translations expand labels by 60%; `.product-name` truncates visually.  
   - Impact: Critical product identity may be hidden; labels may overflow or collide.  
   - Fix: Preserve truncation in dense rows, but expose full name on focus/hover/details, ensure accessible full text, test long unbroken strings, and avoid fixed label slots for translated controls.

17. **Missing price is not given a semantic display**  
   - Evidence: **[E]** prices may be missing.  
   - Impact: Blank cells can be mistaken for zero, loading, or rendering failure.  
   - Fix: Use an explicit missing-value token/copy such as “Not set,” with sorting/filtering behavior defined separately from zero.

18. **Global `saving` flag is likely too coarse**  
   - Evidence: **[E]** single `saving` state at page level; **[H]** exact concurrency behavior depends on drawer and row editing model.  
   - Impact: One save may disable or mislabel unrelated product actions; concurrent saves can race.  
   - Fix: Track saving/error state per product or mutation operation; guard stale responses with request IDs or abort logic.

---

### P3 — Final polish once P0–P2 are addressed

19. **Permission-specific affordances are not described**  
   - Evidence: **[E]** permission-specific affordances not described.  
   - Impact: Users may discover restrictions only after failure.  
   - Fix: Disable or explain forbidden actions upfront based on role, while still handling server-side 401/403.

20. **No stated keyboard model for the table**  
   - Evidence: **[E]** keyboard navigation not described.  
   - Impact: Keyboard-heavy operators may face inconsistent movement through rows, filters, selection, and drawer.  
   - Fix: Define tab order, row action access, bulk-selection shortcuts if already part of the workflow, and focus restoration after save/close.

---

## 3) Concrete fixes by concern

### Hostile data
- Long product names: keep row ellipsis, but expose full value in drawer, accessible name, and focus/hover affordance.
- Missing prices: render “Not set” or equivalent; do not use blank or `0`.
- Expanded translations: test labels at +60%; avoid fixed-width button text where action labels can grow.
- Missing images: stable placeholder with alt/label policy.
- 8MB images: validate upload size, show upload progress/error, reserve dimensions, and avoid decoding full-size assets in table rows.

### Failures
- Represent: loading, filtered loading, empty results, 401/403, 409, 429, 500, timeout, offline, retry, partial batch failure.
- Do not use one generic error for all; operators need to know whether to retry, request access, resolve conflict, or wait.
- Preserve prior table state during transient refresh where safe.

### Responsive layout
- Replace page-level `min-width: 1180px` as the only strategy.
- Define tablet breakpoints: contained horizontal table scroll, sticky key identifiers/actions, responsive drawer width, larger hit targets.
- Ensure the 520px drawer does not consume unusable space on smaller tablets.

### Accessibility
- Drawer: labelled dialog semantics, focus trap, background inert, Escape policy that respects pending save, focus restoration.
- Buttons: accessible names for save/close; minimum 44px touch target; visible `:focus-visible`.
- Table: semantic table/grid decision, row/selection labels, keyboard path through filters → table → drawer → return.
- Status: saving/saved/error announcements via a polite live region where appropriate.

### State recovery
- Keep dirty draft until confirmed saved or explicitly discarded.
- On save failure, retain edits and show retry.
- On conflict, show field-level conflict resolution.
- On offline/timeout, queue or preserve draft based on product policy; never silently discard.
- On close during dirty/pending state, require confirm or auto-save draft with visible recovery.

### Performance
- Virtualize 10,000 rows.
- Defer/debounce filtering and memoize normalized search data.
- Avoid recreating heavy row props and callbacks across all rows.
- Keep selection state efficient, especially “select all filtered” cases.
- Reserve image dimensions and lazy-load thumbnails.
- Replace `transition: all` with property-specific transitions.

---

## 4) Static detector-like signals: decisive vs context-dependent

### Decisive from static facts
- `catch {}` with no error state is a production safety defect.
- Rendering 10,000 rows via direct `map` is a scalability risk.
- `outline: none` without described replacement is an accessibility defect.
- 28px icon buttons fail common touch-target expectations for tablet support.
- `transition: all` is a maintainability/performance smell.
- Fixed `min-width: 1180px` conflicts with unspecified tablet behavior.
- Missing represented states for listed failures are hardening gaps.
- No focus trap/background inert for a fixed drawer is a major keyboard/modal defect.

### Needs project/runtime context
- Exact frame rate impact of 10,000 rows.
- Whether existing row components are memoized internally.
- Whether CSS elsewhere restores focus indicators.
- Whether icon buttons receive `aria-label` inside shared components.
- Whether the drawer is intended as modal, non-modal inspector, or persistent panel.
- Actual API semantics for retries, conflicts, permissions, and offline behavior.
- Whether table semantics should be native table, ARIA grid, or list based on interaction complexity.
- Actual image CDN/thumb pipeline and upload constraints.

---

## 5) Measurement-first validation plan with rollback/acceptance

### Baseline before changes
- Capture initial render time, filter keystroke latency, drawer open/close latency, save success/failure paths, and memory behavior with 10,000 rows.
- Define fixtures: long names, missing prices, absent images, 8MB images, expanded translations, unauthorized user, conflict, offline, timeout, 429, 500, partial batch failure.
- Record keyboard-only task path: filter product → select row → edit → save → recover from error → close drawer.

### Acceptance conditions
- Failed save never appears successful; dirty edits remain recoverable.
- 409 conflict has a visible resolution path.
- Offline/timeout/500/429 states provide clear next action.
- Initial/filter loading never renders as unexplained blank content.
- Keyboard user can open, use, save, cancel, and close drawer without losing focus.
- Focus indicator is visible on all interactive controls.
- Tablet hit targets are at least 44px where touch is supported.
- 10,000-row table remains responsive under the agreed latency budget.
- Filtering does not block typing beyond the agreed threshold.
- Images do not cause meaningful layout shift in rows.
- Reduced-motion mode preserves state feedback without large movement.

### Rollback conditions
- Virtualization breaks selection, row counts, screen-reader navigation, or bulk actions.
- Save hardening increases false conflicts or traps users in unrecoverable pending states.
- Responsive changes hide required columns/actions without an accessible alternative.
- Motion changes obscure state or make pending/error status less visible.
- Image handling blocks valid operational uploads without a clear policy/error message.

### Release strategy
- Ship behind narrow flags where possible: save-state hardening first, then drawer a11y, then table virtualization/filter optimization, then responsive polish.
- Validate with seeded hostile-data fixtures and forced API responses before broad rollout.
- Keep the old table path temporarily available if virtualization has unresolved selection or accessibility regressions.
