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

Read-only static audit only; no browser/build/profiler/accessibility-tree/network/device run is claimed.

## 1) Correct sequencing + verdict

**Sequence:** audit static evidence → define baseline measurements before optimizing → harden correctness, failure handling, accessibility, hostile data, and state recovery → optimize proven hot paths and already-decisive unbounded work → polish responsive layout/motion within the existing design system → validate release gates with rollback.

**One-line verdict:** **Not production-ready for a 10,000-row operations editor**: current evidence shows silent data-loss risk, inaccessible drawer/actions, missing failure states, unbounded rendering/filtering, and brittle layout/motion.

## 2) Prioritized findings: evidence vs hypothesis

### P0 — Data integrity and recovery blockers

1. **Silent save failure**
   - **Source evidence:** `catch {}` swallows `api.save(product)` errors; `saving` is reset without user-visible failure.
   - **Impact:** Operators can believe inventory changes were saved when they were not.
   - **Runtime hypothesis:** API/client layers might surface errors elsewhere, but this component currently provides no visible path.

2. **No represented conflict/permission/rate-limit/offline recovery**
   - **Source evidence:** notes explicitly say 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are absent.
   - **Impact:** Common production failures become blank, stuck, misleading, or destructive workflows.
   - **Runtime hypothesis:** global interceptors may exist, but route-level recovery and task continuity are not described.

3. **Unsafe drawer close during pending save**
   - **Source evidence:** Escape closes the drawer even while save is pending.
   - **Impact:** Can interrupt/obscure an in-flight mutation and cause uncertainty about final state.
   - **Runtime hypothesis:** API may still complete, but the user loses clear agency and confirmation.

### P1 — Accessibility, keyboard, and modal correctness

4. **Drawer is not a real modal interaction**
   - **Source evidence:** drawer traps neither focus nor background interaction.
   - **Impact:** Keyboard and assistive-tech users can tab into hidden/background controls; pointer users can mutate conflicting context.
   - **Runtime hypothesis:** a parent shell may add inert behavior, but given source notes this should be treated as absent.

5. **Icon-only save/close actions are under-specified**
   - **Source evidence:** save and close are icon-only; screen-reader labels are not described.
   - **Impact:** Action purpose may be unavailable to screen readers and ambiguous to low-vision/keyboard users.
   - **Runtime hypothesis:** icons might include labels internally, but no evidence confirms that.

6. **Focus visibility is likely broken**
   - **Source evidence:** `.icon-button { outline: none; }`; `focus-visible` is not described.
   - **Impact:** Keyboard-heavy operations staff lose orientation.
   - **Runtime hypothesis:** another CSS layer could restore focus rings, but this rule is a decisive risk signal.

7. **Insufficient touch/tablet target sizing**
   - **Source evidence:** icon buttons are `28px × 28px`; tablet support is required.
   - **Impact:** Error-prone touch operation and poor accessibility.
   - **Runtime hypothesis:** padding around the button may enlarge the hit area, but not shown.

### P1 — Performance and responsiveness blockers

8. **All 10,000 rows render at once**
   - **Source evidence:** `{rows.map(...)}` directly renders every row.
   - **Impact:** High initial render cost, memory pressure, slow updates, poor assistive-tech navigation.
   - **Runtime hypothesis:** `rows` may sometimes be filtered smaller, but route requirement includes 10,000 rows, so an explicit bound is needed.

9. **Filtering recalculates synchronously on every keystroke**
   - **Source evidence:** additional notes state synchronous recalculation on every keystroke.
   - **Impact:** Input jank and long tasks in a high-frequency workflow.
   - **Runtime hypothesis:** actual cost depends on filter complexity and device, but the unbounded hot path is clear.

10. **Image layout and bandwidth risk**
   - **Source evidence:** image dimensions are not reserved; some images are absent or 8MB.
   - **Impact:** layout shift, slow table rendering, wasted bandwidth, memory spikes.
   - **Runtime hypothesis:** CDN thumbnails may exist, but the UI contract does not require them.

### P2 — Layout, hostile data, and internationalization

11. **Hard desktop width conflicts with tablet support**
   - **Source evidence:** `.page { min-width: 1180px; }`.
   - **Impact:** Tablet users may get forced horizontal panning or clipped workflow.
   - **Runtime hypothesis:** outer shell might scroll horizontally; that is still a degraded tablet contract unless intentional.

12. **Rigid row grid is fragile**
   - **Source evidence:** fixed columns `64px 280px 1fr 120px 96px`; labels may expand 60%; product names up to 200 chars.
   - **Impact:** truncation, overlap, hidden actions, poor localization resilience.
   - **Runtime hypothesis:** exact rendering depends on row content, but the static grid lacks adaptive rules.

13. **Missing price and absent image states are not specified**
   - **Source evidence:** prices may be missing; some images are absent.
   - **Impact:** blank cells can be confused with load failure, zero price, or data corruption.
   - **Runtime hypothesis:** `ProductRow` may render fallbacks, but no evidence is provided.

### P2 — Motion and perceived stability

14. **Broad layout-affecting transitions**
   - **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`.
   - **Impact:** can animate unintended properties, delay response, and cause jank across many rows.
   - **Runtime hypothesis:** if few properties change it may appear acceptable, but `all` on repeated rows is an avoidable production smell.

15. **Reduced motion absent**
   - **Source evidence:** reduced motion is not described.
   - **Impact:** motion-sensitive users have no accommodation; frequent operators may experience unnecessary delay.
   - **Runtime hypothesis:** global CSS could cover it, but route-specific drawer/table movement still needs confirmation.

### P3 — Product polish and operational clarity

16. **Blank initial/filter loading**
   - **Source evidence:** blank table body during initial and filter loading.
   - **Impact:** looks broken, causes repeated actions, and hides system progress.
   - **Runtime hypothesis:** data may be fast locally, but production latency will expose it.

17. **Permission-specific affordances absent**
   - **Source evidence:** not described.
   - **Impact:** users may discover restrictions only after failed actions.
   - **Runtime hypothesis:** server enforcement may be correct, but UI affordance is still missing.

## 3) Concrete fixes

### Hostile data
- Render explicit fallbacks: “No image”, “Price not set”, “Unknown SKU/status” rather than empty cells.
- Constrain product names with accessible full text via title/description pattern or row detail, not only visual ellipsis.
- Use resilient grid sizing: `minmax(0, …)`, localized label wrapping where safe, and stable action columns.
- Reserve image aspect ratio/dimensions; request thumbnails where available; lazy-load non-visible images.
- Validate upload size/type/dimensions before upload; show per-file progress and failure, especially for 8MB images.
- Treat missing price distinctly from `0`; prevent accidental bulk overwrite with null/empty values.

### Failures and recovery
- Replace `catch {}` with typed error handling and visible autosave state: saving, saved, failed, retrying, offline, conflict.
- Keep failed edits dirty and recoverable; never mark success on failed save.
- Add retry with user control for timeout/500/offline; use backoff for 429 and communicate wait state.
- For 401/403, disable forbidden actions up front when known and show a permission-specific explanation.
- For 409, show conflict resolution: reload server value, keep local draft, compare fields, or retry after refresh.
- For partial batch failure, report failed item count and let users retry only failed rows.
- Use request cancellation or stale-response guards when switching products/filters while saves are in flight.

### Responsive/tablet layout
- Preserve the desktop workflow, but remove the unconditional `1180px` route lock for tablet breakpoints.
- Use a bounded horizontal table region only if necessary, with sticky key identifiers/actions and clear scroll affordance.
- Let the drawer adapt: side drawer on wide desktop, wider/near-full-width panel on tablet, no offscreen clipped controls.
- Ensure filters wrap into usable groups rather than compressing controls below readable/tappable sizes.
- Define long-content behavior for translated labels before shipping.

### Accessibility
- Make the drawer modal semantics correct when open: focus trap, background inertness, focus restore, labelled title, Escape behavior that respects pending save.
- If save is pending, Escape should either be disabled, ask for confirmation, or close only after preserving/revealing save state.
- Give icon-only buttons accessible names and visible tooltips where useful.
- Restore visible keyboard focus using `:focus-visible`; do not rely on `outline: none`.
- Provide keyboard paths for filtering, row navigation, selection, bulk actions, drawer open/save/close, and upload.
- Announce autosave and error states via appropriate live regions without being noisy.
- Respect reduced motion: remove/reduce positional drawer/table movement while preserving state feedback.
- Increase effective hit targets for tablet and pointer users.

### State recovery
- Track dirty state per product or draft, not only a global `saving` boolean.
- Preserve unsaved drawer edits across transient errors, filter changes, and accidental close attempts.
- Add navigation/close guards when there are unsaved edits or pending uploads.
- Persist recoverable draft state locally if operationally appropriate and privacy-safe.
- Make autosave status specific: which item saved, failed, conflicted, or is queued.

### Performance
- Establish a row-rendering bound: virtualization, pagination, server-side windowing, or an existing table primitive with equivalent behavior.
- Keep mounted row count bounded for 10,000-row datasets; avoid rendering all rows and images simultaneously.
- Memoize/filter derived rows with correct dependencies after baseline measurement; use deferred input/debounce only where it improves measured typing responsiveness.
- Avoid recreating heavy row props/handlers unnecessarily; isolate row rendering and prevent global `saving` from rerendering every row.
- Reserve image dimensions and load only visible thumbnails.
- Replace `transition: all` with explicit properties, e.g. drawer `transform/opacity`; avoid transitions on every row unless tied to a clear state.
- Avoid layout-property animation and `ease-in` for interaction response.

## 4) Static detector-like signals: decisive vs context-dependent

**Decisive from provided static evidence**
- `catch {}` around save is a production blocker unless another visible failure path is proven.
- Direct `rows.map` for a 10,000-row route requires an explicit rendering bound.
- `transition: all` on repeated rows and drawer is unsafe and over-broad.
- `outline: none` without described replacement is an accessibility failure risk.
- Fixed `min-width: 1180px` conflicts with tablet support unless paired with an intentional adaptive container.
- Missing loading/empty/error/conflict/offline/partial-failure states are real route contract gaps.
- Non-modal drawer behavior is invalid for an edit drawer that overlays page content.

**Needs project/runtime context before final implementation choice**
- Whether to use virtualization, pagination, or server-side windowing depends on existing table architecture and operator workflow.
- Exact performance budgets require target devices, browser mix, row complexity, and API latency.
- Some accessibility labels/focus styles may exist inside shared components or global CSS.
- Image optimization depends on CDN/backend thumbnail support and upload pipeline constraints.
- Permission affordances depend on auth model and whether capabilities are known client-side.
- Tablet layout choice depends on supported tablet sizes, orientation, and task priority.
- Error taxonomy depends on API conventions, but the UI must still represent the listed states.

## 5) Measurement-first validation plan with rollback/acceptance

### Baseline before changes
- Record current initial load/render behavior with 10,000 rows and realistic images.
- Measure filter keystroke latency, result update time, long tasks, memory, and mounted DOM node count.
- Exercise save success/failure cases using controlled API responses: 401/403/409/429/500/timeout/offline/partial batch.
- Review keyboard-only flow: filters → rows → selection → drawer → save/close → focus restore.
- Check tablet viewport behavior and translated labels with 60% expansion.
- Check reduced-motion mode and image layout stability.
- Confirm autosave messaging and recovery behavior for pending, failed, retried, and conflicted edits.

### Provisional acceptance gates to ratify
- No silent save failure; every failed mutation leaves a visible, retryable, recoverable state.
- No data loss on Escape, close, route change, filter change, offline transition, or conflict.
- 10,000-row dataset has bounded rendering; mounted row count stays intentionally capped.
- Filter input remains responsive: provisional target p95 input feedback under 100ms and visible result update under 250ms on target hardware.
- No repeated long tasks over 50ms during ordinary filtering/scrolling after optimization.
- Images do not cause meaningful layout shift; provisional CLS target under 0.1 for the route.
- Drawer passes keyboard modal expectations: trap, inert background, labelled controls, Escape policy, focus restore.
- Icon actions have accessible names and visible focus.
- Tablet layout remains usable without hidden primary actions.
- Reduced-motion mode removes nonessential movement while preserving feedback.

### Rollback conditions
- Roll back or gate any performance optimization that changes row selection, bulk edit, save ordering, or keyboard behavior.
- Roll back drawer changes if focus trapping blocks upload dialogs, browser file pickers, or legitimate nested popovers.
- Roll back virtualization/windowing if it breaks screen-reader row semantics, selection persistence, or find/filter correctness.
- Do not release if P0 save/error/recovery paths or P1 modal/accessibility paths remain unvalidated.


## Output B

## 1. Sequencing + verdict

**Recommended sequence:** audit evidence → harden correctness/state recovery → add failure and permission states → optimize hot paths → polish responsive, motion, and accessibility details.

**One-line verdict:** This surface is not yet production-hardened for a high-volume inventory workflow: the largest risks are silent save failure, unrecoverable/conflicting edits, inaccessible drawer controls, and avoidable 10,000-row rendering cost.

---

## 2. Prioritized findings

### P0 — Silent save failure and unsafe recovery gaps

**Source evidence**
- `catch {}` swallows all save errors.
- `setSaving(false)` runs after both success and failure with no user-visible distinction.
- Additional notes say 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.
- Drawer can close via Escape while save is pending.

**Runtime hypothesis**
- Operators may believe a product was saved when it failed.
- Pending edits may be lost if the drawer closes during save.
- Conflict responses may overwrite newer inventory data or hide stale-edit problems.

**Fix**
- Replace silent catch with explicit save states: `idle | saving | saved | failed | conflict | offline | unauthorized | rateLimited`.
- Surface inline drawer error and page-level autosave status.
- Preserve dirty form data after failure.
- Disable destructive close while saving, or require confirmation when dirty/pending.
- For 409, show conflict resolution: “server value vs your edit,” reload option, and retry after review.
- For 401/403, show permission-specific messaging and disable unavailable actions.
- For partial batch failure, report count succeeded/failed and keep failed rows selected for retry.

---

### P0 — Permission and destructive-action affordances are underspecified

**Source evidence**
- Permission-specific affordances are not described.
- Save and close are icon-only.
- Failure states for 401/403 are missing.

**Runtime hypothesis**
- Users may attempt edits/uploads they cannot complete.
- Icon-only actions may be ambiguous, especially in high-repetition workflows.

**Fix**
- Gate edit, bulk edit, upload, and save controls by permission.
- Use disabled/read-only states with clear reason text, not hidden-only behavior.
- Add accessible names and visible tooltips/help text for icon-only save/close.
- Ensure unauthorized responses do not discard local unsaved changes.

---

### P1 — 10,000 rows render at once and filters run synchronously

**Source evidence**
- `{rows.map(...)}`
- Notes state all 10,000 rows render at once.
- Filtering recalculates synchronously on every keystroke.

**Runtime hypothesis**
- Keystrokes, selection, drawer open/close, and filter changes may jank.
- Memory pressure may increase when image cells are included.
- Bulk selection may trigger full-list re-renders.

**Fix**
- Window/virtualize table rows using existing project patterns if available.
- Keep row height predictable or measured.
- Memoize filtered/sorted row sets with correct dependencies.
- Defer expensive filtering from raw keystrokes: debounce query application or use low-priority updates where supported.
- Isolate selection state so toggling one row does not re-render all rows.
- Memoize `ProductRow` where props are stable.
- Use stable callbacks for row actions.
- Paginate or window bulk operations UI while preserving “select all matching filter” semantics.

---

### P1 — Drawer accessibility and interaction model are unsafe

**Source evidence**
- Drawer traps neither focus nor background interaction.
- Escape closes even while save is pending.
- Save and close are icon-only.
- `.icon-button { width: 28px; height: 28px; outline: none; }`

**Runtime hypothesis**
- Keyboard users may tab into background content while editing.
- Screen-reader users may not receive modal context.
- Users may lose pending edits by pressing Escape.
- Focus may become lost after close.

**Fix**
- If the drawer behaves modally, use dialog semantics, labelled title, focus trap, background inerting, and focus return.
- If it is non-modal, make that explicit and do not trap focus, but provide clear keyboard path and preserve background interaction intentionally.
- Escape behavior:
  - no dirty state: close;
  - dirty state: confirm;
  - saving: block close or queue close after success.
- Add `aria-label` or visible text for icon buttons.
- Restore visible focus indicators; use `:focus-visible`, not `outline: none`.
- Ensure touch target is at least comfortable for tablet use; 28px is likely too small.

---

### P1 — Missing loading, empty, and error states create ambiguous work status

**Source evidence**
- Initial and filter loading render a blank table body.
- Empty results are not represented.
- Autosave status exists only as `saving` boolean in shown snippet.

**Runtime hypothesis**
- Operators may not know whether data is loading, filters returned no results, or the app failed.
- Repeated edits may proceed under stale assumptions.

**Fix**
- Add explicit table-body states:
  - initial loading skeleton/rows;
  - filter loading;
  - empty after filters;
  - empty inventory;
  - recoverable error with retry;
  - auth/permission error;
  - offline mode with queued/unsaved indicator if supported.
- Make autosave status durable enough to show last saved time, failed retry, and unsaved changes.

---

### P1 — Hostile data is not contained

**Source evidence**
- Product names can be 1–200 characters.
- Prices may be missing.
- Translations may expand labels by 60%.
- Images may be absent or 8MB.
- `.product-name` truncates with ellipsis only.
- Grid columns are fixed: `64px 280px 1fr 120px 96px`.

**Runtime hypothesis**
- Long names, missing prices, and expanded labels may hide important operational data.
- Large or missing images may cause layout shifts, slow decode, or broken visual rhythm.
- Internationalized labels may overflow fixed controls.

**Fix**
- Provide title/detail access for truncated product names, preferably through an accessible disclosure or tooltip pattern.
- Define missing price display: em dash, “Not set,” or permission-aware placeholder; avoid ambiguous blank cells.
- Reserve image dimensions and show absent-image placeholder.
- Use thumbnails generated server-side or constrained client-side; avoid rendering raw 8MB images in rows.
- Validate upload size/type before upload, show progress, and handle failure/retry.
- Audit translated strings in controls and drawer footer; allow wrapping where safe.

---

### P2 — Responsive/tablet behavior is brittle

**Source evidence**
- `.page { min-width: 1180px; }`
- Drawer fixed width: `520px`.
- Desktop-first with tablet support required.
- Tablet behavior is not described.

**Runtime hypothesis**
- Tablet users may get horizontal scrolling, clipped drawer content, or unreachable actions.
- A 520px fixed drawer may dominate smaller tablet widths.

**Fix**
- Preserve desktop table density, but define breakpoints:
  - desktop: current multi-column grid/table;
  - tablet landscape: reduce nonessential columns, allow drawer width as `min(520px, 100vw)`;
  - tablet portrait: use horizontal table scroll with sticky key columns or a compact row detail pattern.
- Keep filter and bulk-action bars reachable.
- Ensure drawer height accounts for browser UI and safe areas where relevant.
- Avoid redesigning the whole surface; adapt existing layout tokens and components.

---

### P2 — Motion may harm usability and performance

**Source evidence**
- `.product-row, .drawer { transition: all 300ms ease-in; }`
- Reduced motion support is not described.

**Runtime hypothesis**
- `transition: all` can animate layout-affecting properties unintentionally.
- Row transitions across large lists can amplify rendering cost.
- Motion-sensitive users have no alternate behavior.

**Fix**
- Replace `transition: all` with specific properties, likely `transform`, `opacity`, or color tokens only.
- Avoid per-row transitions for large table updates unless narrowly scoped.
- Use faster, clearer easing for operational UI; avoid slow ease-in for state changes that should feel immediate.
- Add reduced-motion handling that removes transform-heavy animation while preserving state feedback.

---

### P2 — Table semantics and keyboard navigation are not established

**Source evidence**
- Rows render as repeated components in a `div.page`; no table/grid semantics shown.
- Keyboard navigation and screen-reader labels are not described.

**Runtime hypothesis**
- Screen-reader users may not understand row/column relationships.
- Keyboard-heavy operators may lack efficient row navigation, selection, and drawer handoff.

**Fix**
- Use semantic table markup if the layout is tabular, or ARIA grid only if interactive grid behavior is fully implemented.
- Provide column headers, row labels, selection labels, and bulk selection state.
- Define keyboard interactions for:
  - row focus;
  - open drawer;
  - select row;
  - bulk selection;
  - save/cancel in drawer;
  - upload controls.
- Keep focus visible and predictable after filter changes.

---

### P3 — Visual polish issues that should follow hardening

**Source evidence**
- Fixed dense columns.
- Ellipsis-only product names.
- Blank loading body.
- Small icon buttons.
- Generic transitions.

**Runtime hypothesis**
- The UI may feel unstable or unclear during repeated operations.

**Fix**
- Add calm loading placeholders, empty copy, and consistent status badges.
- Improve spacing and hit areas within existing design tokens.
- Add stable image placeholders to prevent row jump.
- Use consistent disabled, saving, failed, and retry states.

---

## 3. Concrete hardening checklist

### Hostile data
- Long names: truncate visually but expose full value accessibly.
- Missing prices: explicit placeholder and validation state.
- Expanded translations: test labels at +60%; allow wrapping in drawer/footer controls.
- Absent images: reserved placeholder.
- 8MB images: validate, compress/thumbnail via existing pipeline, show upload progress and failure.

### Failures
- Represent 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure.
- Do not clear dirty state on failed save.
- Show last successful save time and current unsaved/failed state.
- Make retry idempotent where possible.
- Preserve selected failed rows after partial bulk failure.

### Responsive layout
- Replace hard `min-width: 1180px` as the only strategy with defined desktop/tablet behavior.
- Constrain drawer to viewport: `width: min(520px, 100vw)`.
- Ensure drawer content scrolls internally without hiding footer actions.
- Decide which columns collapse, abbreviate, or move into row details on tablet.

### Accessibility
- Restore focus indicators.
- Add accessible names for icon-only buttons.
- Trap focus/background only if drawer is modal; otherwise document and implement non-modal behavior intentionally.
- Return focus to the opener after drawer close.
- Block or confirm Escape when dirty/saving.
- Add reduced-motion support.
- Ensure row selection and bulk controls are keyboard-operable and announced.

### State recovery
- Track dirty, saving, saved, failed, conflict, unauthorized, offline, and retrying states separately.
- Keep local edits until confirmed saved or intentionally discarded.
- Confirm close on dirty drawer.
- On reload/navigation, warn if unsaved changes exist if that matches product policy.
- For conflicts, fetch latest server version and let the user choose.

### Performance
- Virtualize/window 10,000 rows.
- Memoize filter results.
- Debounce or defer keystroke filtering.
- Avoid full-table re-render for selection and saving changes.
- Reserve image dimensions and lazy-load row thumbnails.
- Avoid `transition: all`, especially on rows.

---

## 4. Static signals: decisive vs context-dependent

### Decisive from the supplied source
- `catch {}` is a production correctness risk.
- Blank loading/empty/error states are insufficient for this workflow.
- Rendering 10,000 rows with `.map()` is a clear scalability risk.
- Synchronous filtering on every keystroke is a likely input-latency risk.
- `outline: none` without replacement is an accessibility failure.
- Icon-only save/close need accessible names and clear affordance.
- No focus trap/background strategy for the drawer is unsafe if modal behavior is intended.
- Escape close while saving is unsafe without explicit recovery policy.
- `transition: all` is too broad and risky.
- Fixed `min-width: 1180px` conflicts with tablet support unless paired with a deliberate overflow/adaptive strategy.
- Unreserved image dimensions can cause layout shift.

### Needs project/runtime context
- Exact frame rate, input latency, memory use, and long-task severity.
- Whether existing components already provide labels, table semantics, or focus management outside the snippet.
- Whether the drawer is intended to be modal or non-modal.
- Whether backend supports conflict resolution, idempotency keys, upload preprocessing, and partial-failure details.
- Whether current design tokens already define focus, motion, disabled, and status patterns.
- Whether virtualization can preserve current row height, sticky headers, bulk selection, and keyboard behavior without regressions.
- Actual tablet breakpoints and supported devices.
- Exact severity of image performance, depending on CDN thumbnails and cache behavior.

---

## 5. Measurement-first validation plan

### Baseline before changes
- Record static inventory route scenarios:
  - initial load;
  - filter typing;
  - open drawer;
  - edit/save success;
  - save failure;
  - conflict;
  - unauthorized;
  - offline/timeout;
  - image missing/large image;
  - 10,000-row bulk selection.
- Capture target metrics:
  - keystroke-to-filter response;
  - time to first usable table;
  - row render count on selection/save;
  - drawer open/close responsiveness;
  - layout shift from images;
  - save failure visibility;
  - keyboard path completion.

### Acceptance conditions
- No silent save failures.
- Failed save preserves edits and shows actionable recovery.
- Conflict state is visible and does not overwrite blindly.
- Dirty or saving drawer cannot be accidentally dismissed without policy.
- Loading, empty, auth, offline, timeout, 429, 500, and partial batch states are represented.
- 10,000-row interaction remains responsive under defined product thresholds.
- Filtering does not block typing under expected data scale.
- Keyboard-only user can filter, select, open drawer, edit, save, handle failure, and return focus.
- Icon-only controls have accessible names.
- Focus indicator is visible.
- Reduced-motion mode keeps state feedback without unnecessary animation.
- Tablet layout remains usable without hidden primary actions.

### Rollback conditions
- Virtualization breaks selection, row height, sticky headers, or screen-reader/keyboard behavior.
- Error handling introduces duplicate saves or lost edits.
- Conflict handling blocks normal successful saves.
- Responsive changes reduce desktop operator efficiency.
- Motion changes remove necessary state feedback.
- Upload handling prevents valid existing workflows.

### Release approach
- Ship in small hardening slices:
  1. save/error/state recovery;
  2. drawer accessibility and close policy;
  3. loading/empty/auth/offline states;
  4. row/filter performance;
  5. tablet and motion polish.
- Keep each slice behind a reversible implementation path where practical.
- Preserve the existing design system, density, and workflow; this is hardening, not a new inventory experience.


## Output C

## 1. Sequencing + verdict

**Correct sequence:** audit the production risks first → harden save/failure/state recovery → optimize table/filter/image hot paths → adapt tablet/accessibility behavior inside the existing system → polish motion, copy, and state presentation → validate with measured acceptance gates.

**One-line verdict:** This surface is not production-ready for a high-volume operations workflow yet; the biggest risks are silent data loss, inaccessible drawer/actions, missing failure states, and unbounded rendering of 10,000 rows.

---

## 2. Prioritized findings: evidence vs. runtime hypotheses

### P0 — Blocking / data-loss risks

| Finding | Source evidence | Runtime hypothesis |
|---|---|---|
| Silent save failure | `catch {}` swallows all save errors; `saving` resets with no user-visible failure | Operators may believe edits persisted when they did not |
| Save state is global, not product-specific | Single `saving` boolean for the whole page/drawer | Concurrent edits, quick row changes, or retry flows may show the wrong saving state |
| Drawer can close during pending save | Notes: Escape closes while save pending; no focus/background trap | Pending edits can be lost or leave user uncertain whether save completed |
| No recovery path for conflicts/offline/timeouts | Notes explicitly list 401/403/409/429/500/timeout/offline/retry/partial batch failure as absent | Common production failures become dead ends or silent corruption |

### P1 — Major release blockers

| Finding | Source evidence | Runtime hypothesis |
|---|---|---|
| 10,000 rows render synchronously | `{rows.map(...)}` renders every `ProductRow` | Initial load, filter typing, selection, and drawer updates may jank or freeze |
| Filtering recalculates on every keystroke | Source notes state synchronous recalculation | Keystroke latency may exceed usable thresholds on real data |
| Drawer is not an accessible modal/panel | Notes: no focus trap, background interaction allowed | Keyboard and screen-reader users can tab behind the drawer or lose context |
| Icon-only save/close actions lack described labels | Notes: save and close are icon-only | Actions may be undiscoverable to assistive tech and ambiguous visually |
| Focus indicators are explicitly removed | `.icon-button { outline: none; }` | Keyboard users may not know where focus is |
| Touch targets are too small for tablet | `.icon-button { width: 28px; height: 28px; }` | Tablet users miss controls; minimum target should be closer to 44×44 CSS px |
| Desktop min-width blocks tablet adaptation | `.page { min-width: 1180px; }` | Tablet support likely devolves into horizontal overflow instead of usable adaptation |
| Layout shift from images | Notes: image dimensions not reserved | Rows may jump during image load, disrupting scanning and selection |

### P2 — Significant hardening gaps

| Finding | Source evidence | Runtime hypothesis |
|---|---|---|
| Blank loading state | Notes: initial/filter loading render blank table body | Users may interpret loading as no results or broken data |
| Empty results state missing | Notes explicitly state absent empty results | Filtering gives no guidance or recovery action |
| Hostile data not handled | Product names 1–200 chars; missing prices; labels expand 60%; absent/8MB images | Fixed columns and nowrap truncation may hide critical identifying data |
| Animation is too broad and potentially expensive | `.product-row, .drawer { transition: all 300ms ease-in; }` | Layout-affecting properties may animate accidentally; 300ms ease-in can feel sluggish |
| Reduced motion not represented | Notes explicitly say reduced motion is not described | Motion-sensitive users lack an equivalent low-motion experience |
| Permission affordances missing | Notes: permission-specific affordances not described | Users may see actions they cannot perform or fail late after 403 |

### P3 — Polish / consistency

| Finding | Source evidence | Runtime hypothesis |
|---|---|---|
| Autosave status likely under-specified | Only `saving` is modeled | It may not distinguish saved, saving, failed, queued, conflict, offline, or retrying |
| Long names are only ellipsized | `.product-name` nowrap/ellipsis | Dense tables remain scannable, but users need a reliable way to inspect full names |
| Fixed drawer width | `.drawer { width: 520px; }` | May be acceptable on desktop, but should clamp on smaller tablet widths |
| Motion duration/easing needs product tuning | `300ms ease-in` | For operations tools, 150–250ms ease-out is usually more responsive |

---

## 3. Concrete fixes

### Hostile data

- Treat product data as adversarial:
  - Product names: keep table scannability, but expose full name through an accessible detail affordance, row detail, or drawer header; do not rely only on visual truncation.
  - Missing prices: render a deliberate state such as `—`, “Not priced”, or “Missing price” depending on workflow severity.
  - Long localized labels: avoid fixed label containers where possible; allow wrapping in filters/drawer forms.
  - Images: reserve dimensions with `width`/`height` or `aspect-ratio`; provide absent-image placeholders; reject/compress/queue large 8MB uploads with clear copy.
- Keep sorting/filtering semantics stable when values are missing; do not let `null` prices or absent images break row rendering.

### Failures and save behavior

- Replace `catch {}` with explicit save outcomes:
  - `saving`, `saved`, `failed`, `retrying`, `offlineQueued`, `conflict`, `forbidden`.
- Use `try/catch/finally` so saving state always resolves.
- Track saving/error state per product or per edit session, not globally.
- Add specific handling:
  - **401:** session expired; preserve draft and request re-auth.
  - **403:** show permission-specific disabled affordance before save where possible.
  - **409:** show conflict resolution with server value vs. local draft.
  - **429:** respect retry-after/backoff.
  - **500/timeout:** retry with user-visible failure state.
  - **Offline:** preserve draft locally and mark as queued or unsynced.
  - **Partial batch failure:** show which rows succeeded, failed, and can be retried.
- Prevent Escape/close while save is pending, or require confirmation if dirty/unsynced edits exist.

### Responsive layout

- Remove page-level `min-width: 1180px` as the only tablet strategy.
- Preserve the desktop workflow, but add structural tablet behavior:
  - table container may scroll horizontally only as a fallback, not as the primary adaptation;
  - pin key columns such as selection, image/name, status/price;
  - collapse secondary columns into drawer/detail view;
  - make filters wrap, collapse, or move into a filter panel at tablet widths;
  - use `width: min(520px, 100vw)` or `clamp(...)` for the drawer.
- Ensure text expansion of 60% does not overlap controls.

### Accessibility

- Treat the drawer as a modal/dialog or true complementary panel:
  - `role="dialog"` or appropriate semantic equivalent;
  - accessible name;
  - focus moves into drawer on open;
  - focus is trapped while modal;
  - background is inert/unreachable;
  - focus returns to the opener on close.
- Save/close icon buttons need visible or programmatic names: `aria-label="Save product"` / `aria-label="Close editor"`.
- Restore focus-visible styling; never remove outlines without an equivalent.
- Increase interactive targets to at least 44×44 on tablet/touch contexts.
- Add keyboard support for table selection, bulk actions, drawer open/close, save, cancel, retry.
- Announce autosave state changes with a polite live region.
- Respect reduced motion:
  - disable nonessential transitions;
  - keep state feedback through copy/icon/color, not motion alone.

### State recovery

- Maintain a draft model separate from server-confirmed row data.
- Add dirty tracking and unsaved-change protection.
- Use request cancellation or sequencing to avoid stale saves overwriting newer edits.
- Use optimistic updates only with rollback and visible failure state.
- Persist in-progress drafts across refresh/navigation when data loss would be costly.
- Use server versioning/ETags or revision IDs for conflict detection.
- Bulk operations should produce an auditable result summary, not a single success/failure toast.

### Performance

- Virtualize or paginate the 10,000-row table; preserve selection by stable row IDs, not index.
- Memoize derived filtered/sorted rows with correct dependencies.
- Debounce or defer filter input work so typing remains responsive.
- Memoize `ProductRow` where useful and keep callbacks stable.
- Avoid causing all rows to re-render when drawer saving state changes.
- Lazy-load row images and reserve dimensions to prevent layout shift.
- Replace `transition: all` with explicit properties, likely `transform`, `opacity`, and perhaps `box-shadow` only where necessary.
- Avoid animating grid dimensions, width, height, right, or other layout-heavy properties.

---

## 4. Static detector-like signals: decisive vs. context-dependent

### Decisive from the provided source

- `catch {}` on save is a decisive silent-failure risk.
- Rendering `rows.map(...)` for 10,000 rows is a decisive scalability risk unless another layer virtualizes, which is not shown.
- `.page { min-width: 1180px; }` is decisive evidence of poor tablet support without additional responsive overrides.
- `.icon-button { width: 28px; height: 28px; outline: none; }` is decisive evidence of target-size and focus-visibility risk.
- `transition: all` is decisive evidence of unsafe motion scope.
- Missing represented states are decisive because the notes explicitly say they are absent.
- No focus trap/background interaction control is decisive because the notes explicitly say so.
- Unreserved image dimensions are decisive layout-stability risk.

### Needs project/runtime context before final severity

- Actual contrast, typography, token usage, and dark/light theme behavior.
- Whether `ProductRow` internally has accessible semantics or labels.
- Whether a parent route already supplies error boundaries, auth recovery, or offline handling.
- Actual filter algorithm cost and row complexity.
- Whether images are transformed by CDN/server before reaching the browser.
- Whether the table is intended to be a true data grid, simple list, or hybrid.
- Whether tablet support means full editing parity or limited review/triage.
- Whether backend APIs support versioning, idempotency, conflict resolution, and partial batch reporting.

---

## 5. Measurement-first validation plan with rollback/acceptance

### Baseline before changes

- Capture current behavior against representative datasets:
  - 10,000 rows;
  - 200-character names;
  - missing prices;
  - 60% longer translated labels;
  - absent images;
  - large image uploads;
  - permission-limited users.
- Record current timings for:
  - initial table render;
  - filter keystroke latency;
  - row selection;
  - drawer open/close;
  - save success/failure paths;
  - image load layout shift.

### Validation matrix

- **Data/failure:** simulate 401, 403, 409, 429, 500, timeout, offline, retry success, retry failure, and partial batch failure.
- **Save recovery:** verify no edit disappears silently; drafts survive failed save, accidental close, and re-auth.
- **Accessibility:** keyboard-only completion of filter → select row → edit → save → close; focus never escapes drawer unexpectedly.
- **Screen reader semantics:** named controls, announced drawer, announced autosave state, understandable error messages.
- **Responsive:** desktop and tablet widths, longer translations, increased text size, touch target checks.
- **Performance:** 10,000-row dataset with worst-case filtering and image mix; verify stable interaction latency.
- **Motion:** default and reduced-motion modes; ensure feedback remains clear without animation.

### Acceptance conditions

- No silent save failures; every failure has visible, actionable state.
- Pending or failed edits cannot be lost through Escape, close, navigation, or auth expiry.
- Filter typing remains responsive on 10,000 rows.
- Initial/filter loading, empty results, permission limits, conflicts, offline, and partial batch failure are represented.
- Drawer meets keyboard/focus expectations and restores focus on close.
- Icon-only controls have accessible names and visible focus states.
- Tablet layout remains usable without relying solely on page-wide overflow.
- Images do not cause disruptive row layout shift.
- Reduced-motion users receive equivalent state feedback.

### Rollback conditions

- If virtualization breaks selection, row height, keyboard navigation, or bulk actions, gate it behind a feature flag and fall back to the existing table while keeping failure-state fixes.
- If the new save state machine causes duplicate writes or stale overwrites, disable optimistic updates and ship conservative confirmed-save behavior.
- If tablet adaptations destabilize desktop density, isolate them behind breakpoint-scoped styles/components.
- If upload compression/validation blocks legitimate workflows, fall back to server-side validation with clear client messaging.

**Ship order:** save/error recovery first, drawer accessibility second, table/filter performance third, responsive/data hardening fourth, motion/copy polish last.
