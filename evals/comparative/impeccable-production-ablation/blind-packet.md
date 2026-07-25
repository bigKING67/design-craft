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

**Correct sequence:** static audit → define measurement baseline → harden correctness/recovery/accessibility/failure states → optimize proven hot paths → polish within the existing design system → validate release gates with rollback criteria.

**One-line verdict:** The surface is directionally recognizable as an inventory editor, but the static evidence shows production blockers around save reliability, state recovery, accessibility, 10k-row rendering, and hostile data handling before any visual polish should be prioritized.

---

## 2. Prioritized findings

### P0 — Save failures can silently lose operator trust and state
- **Source evidence:** `catch {}` swallows `api.save(product)` errors; `setSaving(false)` runs without success/failure distinction.
- **Source evidence:** Missing 409, 429, 500, timeout, offline, retry, and partial batch failure states.
- **Runtime hypothesis:** Operators may believe changes saved when they failed, especially during autosave or drawer close flows.
- **Fix:** Return explicit save states: `idle | saving | saved | failed | conflict | offline | rateLimited`. Preserve dirty edits, show retry, expose conflict resolution, and never clear pending edits solely because a request ended.

### P0 — Drawer interaction is unsafe during editing/saving
- **Source evidence:** Drawer traps neither focus nor background interaction.
- **Source evidence:** Escape closes it even while save is pending.
- **Source evidence:** Save and close are icon-only.
- **Runtime hypothesis:** Keyboard and screen-reader users can lose context or activate background rows while editing; pending saves may be interrupted.
- **Fix:** Make the drawer modal or clearly non-modal by contract. For modal behavior: focus trap, inert/disabled background, labelled title, labelled buttons, restore focus on close, block/destructure close during pending save with confirmation or queue-safe cancellation.

### P1 — 10,000-row synchronous rendering/filtering is a hot-path risk
- **Source evidence:** `{rows.map(...)}` renders all rows.
- **Source evidence:** Filtering recalculates synchronously on every keystroke.
- **Runtime hypothesis:** Keystrokes, selection, drawer edits, and autosave status changes may cause long commits and input delay.
- **Fix:** Virtualize/window the table, debounce or defer filter text application, memoize derived filtered rows, avoid page-wide state churn from `saving`, and isolate row rendering from drawer save status.

### P1 — Required production states are absent
- **Source evidence:** Initial/filter loading render a blank table body.
- **Source evidence:** Empty results, auth/permission, conflict, rate-limit, server, timeout, offline, retry, and partial batch failure states are not represented.
- **Runtime hypothesis:** Users cannot distinguish “no results” from “still loading” or “failed,” increasing duplicate work and support load.
- **Fix:** Add explicit state surfaces in the existing table shell: skeleton/loading rows, empty result copy with filter reset, permission-specific disabled affordances, retry panels, offline banner, conflict callout, and partial batch result summary.

### P1 — Accessibility basics are incomplete for a keyboard-heavy tool
- **Source evidence:** `.icon-button { width: 28px; height: 28px; outline: none; }`
- **Source evidence:** Icon-only save/close.
- **Source evidence:** Keyboard navigation, screen-reader labels, focus-visible, and reduced motion are not described.
- **Runtime hypothesis:** There may be no perceivable focus, insufficient target size on tablet, unlabeled controls, and inaccessible row/drawer workflows.
- **Fix:** Restore visible `:focus-visible`, add accessible names, confirm tab order, support row/action keyboard shortcuts without trapping users, provide table semantics, and set tablet hit targets to a project-approved comfortable size.

### P2 — Hostile data can break layout and comprehension
- **Source evidence:** Product names can be 1–200 characters; `.product-name` truncates nowrap with ellipsis.
- **Source evidence:** Prices may be missing; translations may expand labels by 60%; some images are absent or 8MB.
- **Runtime hypothesis:** Operators may lose critical identifying information, see broken alignment, or suffer layout shift/slow image decode.
- **Fix:** Add tooltip/details access for truncated names, missing-price state, localized label stress tests, reserved image dimensions, fallback image cells, upload size validation/compression guidance, and async image handling.

### P2 — Tablet support conflicts with fixed desktop layout
- **Source evidence:** `.page { min-width: 1180px; }`
- **Source evidence:** Drawer fixed at `width: 520px; height: 100vh;`.
- **Runtime hypothesis:** Tablet users may get horizontal scrolling, clipped drawer content, viewport-height bugs, or unusable touch targets.
- **Fix:** Preserve the desktop workflow but add tablet breakpoints: table horizontal scroll containment, drawer width as `min(520px, 100vw)` or tokenized equivalent, safe viewport units, and touch target spacing.

### P2 — Motion implementation is over-broad and may be uncomfortable
- **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`
- **Source evidence:** Reduced motion is not described.
- **Runtime hypothesis:** Unintended properties may animate, drawer motion may feel delayed, and users requesting reduced motion may still get full transitions.
- **Fix:** Transition only intended properties, usually `transform`/`opacity`; avoid animating layout properties; use reduced-motion media query that preserves state feedback without large movement.

### P3 — Global save state is too coarse for a dense editor
- **Source evidence:** Single `saving` boolean is owned by the page and passed to `EditDrawer`.
- **Runtime hypothesis:** Concurrent saves, autosave, bulk actions, and row-level edits may produce ambiguous status.
- **Fix:** Track save state by product/batch/request id where needed; expose global autosave summary separately from row/drawer pending state.

---

## 3. Concrete hardening/polish/optimization moves

1. **Save contract hardening:** replace swallowed errors with typed outcomes, visible status, retry, dirty-state preservation, conflict handling, and close protection while pending.
2. **State shell:** keep the table frame visible during loading/error/empty states so operators retain orientation; never use a blank body as the only feedback.
3. **Drawer accessibility:** labelled controls, focus trap or explicit non-modal behavior, background interaction policy, Escape rules, focus restoration, pending-save confirmation.
4. **Table performance:** introduce row windowing, stable row keys, memoized filtered data, deferred filter updates, and localized state updates so autosave does not rerender 10,000 rows.
5. **Hostile data coverage:** long-name expansion path, missing price placeholder, absent/large image handling, reserved media dimensions, upload validation, translation expansion checks.
6. **Responsive containment:** preserve desktop density but make tablet behavior explicit with constrained drawer width, scrollable table region, safe viewport sizing, and larger touch targets where needed.
7. **Permission-aware UI:** render disabled or hidden actions based on capability, with explanatory affordances for 401/403 rather than generic failure.
8. **Motion polish:** replace `transition: all` with scoped transitions and reduced-motion alternatives; avoid motion that obscures save/error state changes.

---

## 4. Static detector-like signal reconciliation

**Decisive from the supplied source/scope**
- Empty `catch {}` proves save errors are swallowed in the shown path.
- Missing listed state branches are decisive within the provided source notes.
- `rows.map(...)` proves unwindowed rendering in the shown component.
- `min-width: 1180px` proves a fixed desktop floor exists.
- `outline: none` proves the default outline is removed for `.icon-button`.
- Icon-only save/close plus missing labels note proves accessible naming is not represented.
- “Drawer traps neither focus nor background interaction” is decisive as supplied product evidence.

**Signals that are strong risks but need project/runtime context**
- Actual typing latency, commit duration, memory use, and frame rate require profiling.
- Actual layout shift from images requires dimensions/runtime rendering evidence.
- Whether focus is fully invisible requires checking inherited/custom `:focus-visible` styles.
- Whether `transition: all` causes jank depends on which properties change at runtime.
- Whether global `saving` causes concurrency bugs depends on actual autosave/bulk call paths.
- Tablet usability needs viewport testing against target tablet sizes and input modes.
- Screen-reader quality requires semantic DOM/accessibility tree validation.

---

## 5. Measurement-first validation plan with rollback/acceptance

**Baseline before changes**
- Measure initial render time, row count mounted, memory, long tasks, and filter keystroke latency with 10,000 rows.
- Measure drawer open/close interaction, save pending state, image loading/layout shift, and tablet viewport behavior.
- Capture failure-path behavior for save failure, conflict, offline, timeout, 401/403, 429, 500, and partial batch failure.
- Audit keyboard path: filters → table rows/actions → drawer → save/close → focus restore.

**Acceptance conditions**
- No save failure is silent; dirty edits survive failed/retried saves.
- Closing during pending save is blocked, confirmed, or safely resumable.
- Loading, empty, permission, conflict, offline, retry, timeout, server error, and partial batch states render clear user actions.
- 10,000-row filtering remains responsive under agreed thresholds, with no full-table rerender on unrelated drawer save state.
- Keyboard users can complete the core edit/save flow with visible focus and labelled controls.
- Tablet layout remains usable without destructive clipping of table actions or drawer controls.
- Large/missing images do not collapse layout or block primary editing.

**Rollback conditions**
- Any change hides inventory data, breaks bulk selection, drops unsaved edits, removes existing workflow affordances, or worsens measured input latency.
- Any optimization that changes row order, selection persistence, permission behavior, or save semantics without explicit product approval should be reverted.
- Any visual polish that bypasses existing tokens/components or reduces density without solving a documented production issue should be deferred.


## Output B

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


## Output C

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
