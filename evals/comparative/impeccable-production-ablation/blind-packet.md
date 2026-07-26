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

**Correct sequence:** read-only audit → P0 hardening for save/failure/state integrity → P1 accessibility and recovery fixes → table/filter/image performance optimization → responsive tablet adaptation → final polish pass → re-audit with runtime measurements.

**One-line verdict:** This surface is not production-ready for high-volume operations use: the static evidence shows silent data-loss risk, missing failure states, inaccessible drawer/actions, and a 10,000-row render path likely to degrade core task flow.

---

## 2. Prioritized findings: source evidence vs runtime hypotheses

### P0 — Blocking / release-stopping

**P0.1 Silent save failure and false “saved” state**  
- **Source evidence:** `catch {}` swallows `api.save(product)` failures; `setSaving(false)` runs without error state, retry, rollback, or user-visible failure.  
- **Impact:** Operators can believe product edits were saved when they were not. This is a production data-integrity risk.  
- **Runtime hypothesis:** Actual backend failure frequency, autosave timing, and conflict behavior need runtime/API context, but the silent failure path is decisive from source.

**P0.2 Missing conflict, auth, rate-limit, timeout, offline, and partial batch states**  
- **Source evidence:** Additional notes say 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.  
- **Impact:** Operators cannot distinguish “not allowed,” “stale data,” “try later,” “server failed,” or “some rows failed.”  
- **Runtime hypothesis:** Exact copy, retry policy, and batch semantics depend on API contracts, but absence of represented states is decisive.

**P0.3 Drawer can close during pending save**  
- **Source evidence:** “Escape closes it even while a save is pending.”  
- **Impact:** User can lose state continuity mid-write, especially with autosave and image upload latency.  
- **Runtime hypothesis:** Whether data is actually discarded depends on drawer implementation, but allowing close during pending write is a decisive risk.

**P0.4 All 10,000 rows render at once**  
- **Source evidence:** `{rows.map((row) => <ProductRow ... />)}` with product context of 10,000 rows.  
- **Impact:** Initial render, filtering, selection updates, and drawer edits can become sluggish or lock the main thread.  
- **Runtime hypothesis:** Exact latency needs profiling, but rendering 10,000 product rows synchronously is a decisive hot-path smell.

---

### P1 — Major / fix before production

**P1.1 Synchronous filtering on every keystroke**  
- **Source evidence:** Notes state filtering recalculates synchronously on every keystroke.  
- **Impact:** Typing into filters may stutter; operators lose keyboard flow.  
- **Runtime hypothesis:** Severity depends on filter complexity and device class; still high risk at 10,000 rows.

**P1.2 Blank table body during initial and filter loading**  
- **Source evidence:** Notes state initial and filter loading render a blank table body.  
- **Impact:** Users cannot tell whether data is loading, empty, failed, filtered out, or broken.  
- **Runtime hypothesis:** Duration and perceived severity need network/device timing.

**P1.3 No empty-results state**  
- **Source evidence:** Empty results are not represented.  
- **Impact:** Operators get no recovery path when filters exclude all rows.  
- **Fix priority:** Include active-filter summary and one-action reset.

**P1.4 Drawer has no focus trap and does not block background interaction**  
- **Source evidence:** Notes state drawer traps neither focus nor background interaction.  
- **Impact:** Keyboard and screen-reader users can interact with stale background content while editing a product.  
- **WCAG relevance:** Focus order, modal/dialog behavior, keyboard operation.  
- **Runtime hypothesis:** Exact tab sequence needs accessibility-tree/browser validation, but the missing trap is decisive for a fixed edit drawer.

**P1.5 Icon-only save and close without described accessible names**  
- **Source evidence:** “Save and close are icon-only”; screen-reader labels are not described.  
- **Impact:** Assistive-tech users may encounter unlabeled controls.  
- **Runtime hypothesis:** Hidden labels may exist outside the snippet, so final failure needs DOM confirmation; static notes make it a strong risk.

**P1.6 Focus indicator removed on icon buttons**  
- **Source evidence:** `.icon-button { ... outline: none; }`; focus-visible is not described.  
- **Impact:** Keyboard-heavy operators may lose track of active control.  
- **Runtime hypothesis:** A separate `.icon-button:focus-visible` rule could exist; absent that, this is a major static signal.

**P1.7 Touch targets are too small for tablet support**  
- **Source evidence:** `.icon-button { width: 28px; height: 28px; }`; tablet support required.  
- **Impact:** Close/save/bulk actions become error-prone on touch.  
- **Runtime hypothesis:** Adjacent spacing and hit-area wrappers need inspection, but visible target size is below expected touch comfort.

**P1.8 Fixed desktop minimum width conflicts with tablet support**  
- **Source evidence:** `.page { min-width: 1180px; }`.  
- **Impact:** Tablet users likely get horizontal overflow or clipped workflows.  
- **Runtime hypothesis:** A deliberate horizontal-scroll table shell could be acceptable for dense inventory, but the route needs explicit responsive behavior.

**P1.9 `transition: all 300ms ease-in` on rows and drawer**  
- **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`.  
- **Impact:** Animates unintended properties, can trigger layout/paint work, and ease-in feels sluggish because it starts slowly.  
- **Runtime hypothesis:** Actual jank depends on changed properties; the static pattern is decisively unsafe for a dense table.

**P1.10 Reduced motion not represented**  
- **Source evidence:** Reduced motion is not described; transitions exist.  
- **Impact:** Users requesting reduced motion still receive animated drawer/row transitions.  
- **Runtime hypothesis:** Global reduced-motion CSS could exist, but not in provided facts.

---

### P2 — Moderate / next hardening pass

**P2.1 Hostile data not fully handled**  
- **Source evidence:** Product names may be 1–200 chars; prices may be missing; labels may expand 60%; images may be absent or 8MB.  
- **Impact:** Truncated names, missing price ambiguity, broken image cells, layout shifts, and overflow under translation.  
- **Current partial mitigation:** `.product-name` uses ellipsis.  
- **Gap:** Ellipsis alone hides critical SKU/name data without guaranteed tooltip/detail access.

**P2.2 Image dimensions are not reserved**  
- **Source evidence:** Notes state image dimensions are not reserved.  
- **Impact:** Row height/layout shift during image load; selection/edit targets can move.  
- **Runtime hypothesis:** Severity depends on table row sizing and image loading strategy.

**P2.3 Single global `saving` state for drawer save**  
- **Source evidence:** `const [saving, setSaving] = useState(false)` passed to `EditDrawer`.  
- **Impact:** Concurrent saves, row-specific autosave, uploads, or retries can collapse into one ambiguous status.  
- **Runtime hypothesis:** If only one drawer save can exist, this may be acceptable; autosave and batch context make it risky.

**P2.4 Permission-specific affordances absent**  
- **Source evidence:** Permission-specific affordances are not described.  
- **Impact:** Users may discover denied actions only after failure.  
- **Fix priority:** Disable/hide with reason based on product policy; do not silently remove critical context.

**P2.5 Long labels and translations may overflow fixed columns**  
- **Source evidence:** Fixed grid columns `64px 280px 1fr 120px 96px`; translations may expand labels by 60%.  
- **Impact:** Clipped controls/status labels, especially in 96px/120px columns.  
- **Runtime hypothesis:** Exact overflow needs localized strings and viewport checks.

---

### P3 — Polish / after hardening

**P3.1 Ellipsized product names need recoverable full text**  
- **Source evidence:** `.product-name` truncates with ellipsis.  
- **Impact:** Acceptable in dense tables only if full name is available through row detail, accessible title/description, or drawer.  
- **Fix:** Preserve density but expose full text on focus/hover and in drawer header.

**P3.2 Motion timing should be tuned to task UI**  
- **Source evidence:** 300ms ease-in on drawer/rows.  
- **Impact:** Feels slower than necessary for repeated operator workflows.  
- **Fix:** Use targeted transform/opacity transitions around 150–220ms with reduced-motion fallback.

---

## 3. Concrete fixes

### Hostile data
- Add table-cell renderers for:
  - Missing price: explicit “No price” / “Unset” state, not blank or zero.
  - Missing image: reserved-size placeholder with accessible text where meaningful.
  - 8MB images: generate/display constrained thumbnails; reserve width/height or aspect ratio.
  - 200-character names: keep single-line density, but provide full name in drawer header and accessible expansion on focus/hover.
  - Translation expansion: audit fixed 96px/120px columns; allow labels/status to wrap or use abbreviations with accessible full labels.
- Add test fixtures for min/max product names, missing values, absent image, oversized image, and expanded labels.

### Failures
- Replace `catch {}` with typed error handling:
  - 401/403: session/permission message with safe recovery path.
  - 409: conflict resolution showing local value, server value, and refresh/overwrite policy.
  - 429: rate-limit message with retry-after behavior.
  - 500/timeout/offline: non-destructive retry and local pending state.
  - Partial batch failure: per-row failure summary and retry failed only.
- Never show “saved” after failed save. Use “Saving…”, “Saved”, “Failed — retry”, “Offline — pending”, and “Conflict” states.

### Responsive layout
- Keep desktop-first table workflow, but define tablet behavior:
  - Replace page-level `min-width: 1180px` with a table viewport that intentionally scrolls horizontally if needed.
  - Keep filters and drawer usable at tablet widths.
  - Consider drawer width as `min(520px, 100vw)` or tablet-specific full-height panel behavior.
  - Ensure action columns remain reachable without clipping.
- Do not redesign into cards unless the workflow demands it; preserve dense inventory editing.

### Accessibility
- Implement drawer as a modal/dialog pattern when open:
  - Focus moves into drawer on open.
  - Focus is trapped inside drawer.
  - Background is inert or otherwise unavailable.
  - Escape is disabled or guarded while save/upload is pending.
  - Focus returns to the invoking row/action on close.
- Add accessible names for icon-only save and close controls.
- Replace `outline: none` with visible `:focus-visible` styling.
- Increase touch hit areas to at least comfortable tablet targets, even if the visual icon remains compact.
- Add keyboard navigation expectations for rows, selection, filters, drawer actions, and bulk operations.
- Add reduced-motion CSS that preserves state feedback without full animation.

### State recovery
- Preserve unsaved edits across transient failures.
- Track save state per product/edit session, not just one ambiguous global boolean if concurrent operations are possible.
- Prevent close/navigation during pending save unless user explicitly confirms.
- For autosave, maintain a visible queue/pending/error state and allow retry.
- On conflict, avoid overwriting silently; show deterministic resolution.

### Performance
- Virtualize or window the 10,000-row table while preserving selection, keyboard navigation, row heights, and drawer anchoring.
- Debounce or defer filter input work; memoize filtered results with correct dependencies.
- Move expensive filtering off the immediate keystroke path where needed.
- Use stable row props/callbacks to avoid rerendering unaffected rows.
- Reserve image dimensions and lazy-load thumbnails.
- Replace `transition: all` with targeted properties: drawer `transform`, optional `opacity`; rows only stateful color/background changes if needed.

---

## 4. Static detector-like signals: decisive vs context-dependent

**Decisive from provided static facts**
- `catch {}` around save is a real silent-failure path.
- Missing represented error states are release risks.
- Rendering 10,000 rows with direct `map` is an unsafe hot path.
- Synchronous filtering on every keystroke is a likely interaction bottleneck.
- No focus trap/background isolation for an edit drawer is an accessibility failure pattern.
- Closing during pending save is a state-recovery risk.
- `transition: all` is unsafe for dense product UI.
- Blank table body during loading is ambiguous state design.

**Strong signals that still need project/runtime context**
- `outline: none`: decisive only if no replacement focus-visible style exists elsewhere.
- 28px icon buttons: likely too small, but actual hit area may be larger via wrapper/padding.
- `min-width: 1180px`: problematic for tablet unless intentionally contained in an accessible horizontal-scroll table region.
- Icon-only controls: failure only if accessible names are actually absent.
- Ellipsized names: acceptable if full names are available through accessible detail views.
- Missing reduced motion: needs global CSS/context check.
- Performance severity: needs actual row complexity, device class, profiler measurements, and production data shape.

---

## 5. Measurement-first validation plan with rollback/acceptance

**Validation plan — to run after fixes, not claimed here**
1. **Save-state matrix**
   - Simulate success, 401/403, 409, 429, 500, timeout, offline, and partial batch failure.
   - Acceptance: no silent failures; each state has clear copy, retry/recovery, and no false “saved.”

2. **State recovery**
   - Start save/upload, press Escape, click outside, navigate away, go offline.
   - Acceptance: pending work is protected; user can retry or intentionally discard; focus/state returns predictably.

3. **Accessibility pass**
   - Keyboard-only flow through filters, table rows, bulk selection, drawer open/save/close.
   - Screen-reader name/role/state review for icon buttons, drawer, autosave status, errors, and selection.
   - Acceptance: visible focus, named controls, trapped drawer focus, inert background, reduced-motion alternative.

4. **Performance measurements**
   - Measure initial render, filter keystroke latency, row selection latency, drawer open latency, and image-load layout shift on 10,000 rows.
   - Acceptance targets: keystrokes remain responsive, no long main-thread stalls during routine filtering/selection, drawer opens without perceptible jank, image loading does not move controls.

5. **Responsive/tablet checks**
   - Validate tablet widths, touch input, horizontal table handling, drawer width, filters, and action reachability.
   - Acceptance: no clipped primary actions; touch targets are comfortable; table overflow is intentional and usable.

6. **Hostile-data fixtures**
   - Run with 1-char/200-char names, missing prices, missing images, 8MB image inputs, expanded translations, and permission-restricted users.
   - Acceptance: no broken layout, no ambiguous blanks, no inaccessible hidden critical data.

**Rollback conditions**
- Roll back virtualization/filter changes if they break selection persistence, keyboard row navigation, scroll position, or drawer-row association.
- Roll back drawer changes if they trap focus incorrectly or prevent recovery from pending states.
- Roll back save-state changes if they introduce duplicate writes, lost retries, or stale conflict resolution.
- Roll back responsive changes if they preserve tablet width but make the desktop operator workflow slower or less scannable.

**Final acceptance condition:** existing workflow and design system remain recognizable, while failures become explicit, edits become recoverable, keyboard/touch access is reliable, and the 10,000-row path is measurably responsive.


## Output B

## 1. Sequencing and verdict

**Correct sequence:** audit current failure modes → harden data/save/error handling → restore accessibility and state recovery → optimize table/filter/image hot paths → polish responsive layout, motion, and microcopy within the existing design system.

**Verdict:** Static evidence indicates this surface is not production-ready for a 10,000-row operations workflow until silent failures, drawer accessibility, missing recovery states, and unbounded rendering are hardened.

---

## 2. Prioritized findings

### P0 — Silent save failure can hide data loss

**Source evidence**
- `catch {}` swallows all save errors.
- `setSaving(false)` runs after failure with no user-visible state.
- Missing states are explicitly noted for `409`, `429`, `500`, timeout, offline, retry, and partial batch failure.
- Drawer can close via Escape while save is pending.

**Runtime hypothesis**
- Operators may believe an edit was saved when it failed.
- Closing the drawer during a pending save may discard local context or make recovery unclear.
- Conflicts may overwrite newer server data if no 409 resolution path exists.

**Fix**
- Replace silent catch with typed save states: `idle | saving | saved | failed | conflict | offline | retrying`.
- Keep failed edits locally recoverable in the drawer.
- Disable destructive close while save is pending, or require confirmation with clear “save in progress” copy.
- Show conflict resolution for 409: server value, local value, choose/merge/retry.
- Add retry affordance for timeout/429/500/offline with backoff and non-blocking status.

---

### P0 — Drawer is not accessible or interaction-safe

**Source evidence**
- Drawer traps neither focus nor background interaction.
- Escape closes it even while save is pending.
- Save and close are icon-only.
- `.icon-button { outline: none; }`
- Keyboard navigation, screen-reader labels, and focus-visible are not described.

**Runtime hypothesis**
- Keyboard and screen-reader users may lose position, interact with background rows behind the drawer, or fail to understand icon actions.
- Removing outline may make focused controls invisible.

**Fix**
- Treat drawer as a modal or clearly non-modal panel; if modal, trap focus, restore focus to opener, inert/disable background interaction, and label the dialog.
- Add accessible names to icon-only controls: “Save product”, “Close editor”.
- Replace `outline: none` with a visible `:focus-visible` style using existing tokens.
- Gate Escape behavior: if dirty or saving, show confirm/retry state instead of closing immediately.
- Ensure Save button exposes disabled/busy state with `aria-busy` or equivalent status text.

---

### P0 — Critical production states are absent

**Source evidence**
- Initial and filter loading render a blank table body.
- Empty results, 401/403, 409, 429, 500, timeout, offline, retry, and partial batch failure states are not represented.

**Runtime hypothesis**
- Blank table can be misread as “no products” or a broken page.
- Permission errors may look identical to loading or empty data.
- Batch operations can leave users unsure which products succeeded.

**Fix**
- Add distinct states for loading, empty filtered results, empty inventory, unauthorized, forbidden, server error, timeout, offline, rate-limited, conflict, and partial success.
- Preserve table/header/filter context during loading instead of blanking the body.
- For partial batch failure, show count-level summary plus row-level retry/errors.
- Use existing status/alert components rather than introducing a new notification pattern.

---

### P1 — 10,000-row rendering and filtering are likely hot-path failures

**Source evidence**
- `{rows.map(...)}` renders all rows.
- “All 10,000 rows render at once.”
- Filtering recalculates synchronously on every keystroke.
- Global `saving` state lives on `InventoryPage`, so save state changes can re-render the page tree.

**Runtime hypothesis**
- Typing in filters may jank.
- Save status changes may cause unnecessary row work.
- Initial load may block the main thread and increase memory pressure.

**Fix**
- Virtualize or window the product rows while preserving keyboard and selection semantics.
- Debounce or defer filtering input; memoize filtered results with correct dependencies.
- Move per-row/per-product save state closer to the edited product or store it by product id.
- Use stable row props and memoized row components where appropriate.
- Keep bulk selection state independent from row rendering churn.

---

### P1 — Hostile data is not safely represented

**Source evidence**
- Product names may be 1–200 characters.
- Prices may be missing.
- Labels may expand by 60 percent in translation.
- Images may be absent or 8MB.
- `.product-name` truncates with ellipsis only.
- Image dimensions are not reserved.

**Runtime hypothesis**
- Long names may hide distinguishing information.
- Missing prices may be confused with zero.
- Translated labels may overflow fixed columns.
- Large or absent images may cause layout shift or slow rendering.

**Fix**
- Add explicit missing-value treatment: “Price missing”, “No image”, “Not translated”, etc.
- Preserve full product names via accessible title/details pattern, not only visual ellipsis.
- Reserve image dimensions and use placeholders for absent images.
- Use thumbnails or constrained image loading; avoid loading full 8MB assets in table rows.
- Test expanded labels against the existing grid and drawer layout before shipping.

---

### P1 — Permission-specific affordances are unspecified

**Source evidence**
- Permission-specific affordances are not described.
- 401/403 states are not represented.
- Bulk selection, edit drawer, image uploads, and autosave imply role-sensitive actions.

**Runtime hypothesis**
- Users without edit/upload permission may see controls they cannot use.
- Failed save/upload due to permissions may appear as generic failure.

**Fix**
- Hide or disable unavailable actions with explanatory copy.
- Distinguish authentication failure from authorization failure.
- Make read-only rows and drawer fields visibly read-only, not merely non-functional.
- Preserve auditability for blocked bulk actions: which action, which permission, what to do next.

---

### P2 — Tablet and constrained-width behavior are likely brittle

**Source evidence**
- `.page { min-width: 1180px; }`
- Drawer is fixed at `width: 520px; height: 100vh`.
- Tablet behavior is not described.

**Runtime hypothesis**
- Tablet users may get horizontal overflow, clipped drawer content, or unreachable controls.
- Fixed drawer width may consume too much viewport width.

**Fix**
- Define tablet breakpoints within the current layout system.
- Use responsive drawer sizing such as `width: min(520px, 100vw)` with safe-area handling.
- Keep primary table actions reachable when horizontal scrolling is unavoidable.
- Ensure drawer content scrolls internally without trapping page scroll unpredictably.

---

### P2 — Motion is broad, potentially expensive, and lacks reduced-motion path

**Source evidence**
- `.product-row, .drawer { transition: all 300ms ease-in; }`
- Reduced motion is not described.

**Runtime hypothesis**
- `transition: all` can animate layout-affecting properties and produce jank across many rows.
- Users requesting reduced motion may still receive full transitions.

**Fix**
- Replace `transition: all` with specific properties, ideally `transform` and `opacity` where motion is needed.
- Avoid transitions on 10,000 row elements unless scoped to interacted rows.
- Add reduced-motion CSS that removes or shortens movement while preserving state feedback.

---

### P3 — Autosave status is too global for operator confidence

**Source evidence**
- Single `saving` boolean passed to `EditDrawer`.
- Route includes autosave status, but source only represents global saving true/false.

**Runtime hypothesis**
- Operators may not know which product is saving, saved, failed, or conflicted.
- Rapid edits may race if save responses resolve out of order.

**Fix**
- Track status per product/edit session.
- Include last-saved timestamp or “unsaved changes” indicator where appropriate.
- Ignore stale save responses using request ids or revision tokens.
- Keep status calm and persistent enough for repeated operations work.

---

## 3. Concrete hardening moves by area

### Hostile data
- Render explicit placeholders for missing price/image fields.
- Reserve image boxes and use table-safe thumbnails.
- Support 200-character names with accessible full-value access.
- Validate translated labels at +60% expansion.
- Avoid treating null, zero, empty string, and unknown as the same visual state.

### Failures
- Add typed error states for load, filter, save, upload, auth, conflict, rate limit, offline, and partial batch failure.
- Never swallow save/upload errors.
- Preserve user input across retry.
- Provide row-level and batch-level error summaries.
- Make retry idempotent where possible.

### Responsive layout
- Keep desktop-first table workflow but define tablet constraints.
- Change fixed drawer width to bounded responsive width.
- Ensure controls remain reachable at tablet widths.
- Avoid relying on `min-width: 1180px` as the only tablet strategy.

### Accessibility
- Add drawer focus trap, focus restoration, accessible name, and background inerting if modal.
- Add labels for icon-only buttons.
- Restore visible `:focus-visible`.
- Define keyboard navigation for table rows, selection, drawer open/close, save, and upload.
- Announce loading, saving, saved, failed, and conflict states through appropriate status regions.

### State recovery
- Track dirty state separately from saving state.
- Prevent accidental close during dirty/saving states.
- Store pending edit locally until save succeeds or user explicitly discards.
- Handle offline/timeout retry without losing drawer contents.
- Resolve 409 conflicts without silently overwriting.

### Performance
- Window 10,000 rows.
- Defer/debounce filter computation.
- Memoize derived rows.
- Avoid global state updates that re-render the full table.
- Reserve image dimensions and lazy-load/decode thumbnails.
- Measure keystroke latency, initial render time, row interaction latency, and drawer open latency.

---

## 4. Static signals: decisive vs context-dependent

### Decisive from the provided source
- Silent failure exists: `catch {}` is present.
- All rows are rendered with `rows.map(...)`.
- Save state is only a boolean.
- `transition: all` is present.
- Focus outline is removed on icon buttons.
- Page has fixed minimum width.
- Drawer has fixed width and viewport height.
- Current snippet does not represent the listed failure states.
- Current CSS does not include a reduced-motion branch.

### Needs project/runtime context
- Exact jank severity from 10,000 rows.
- Whether `ProductRow` is memoized internally.
- Whether `Filters` already debounce or defer outside the snippet.
- Whether design-system components add labels, focus styles, or status semantics elsewhere.
- Whether image URLs are thumbnailed by the backend/CDN.
- Whether route-level auth wrappers handle 401/403.
- Whether the drawer is intended to be modal or non-modal.
- Exact tablet breakpoints and supported browser/device matrix.
- Whether autosave uses revision tokens or request cancellation elsewhere.

---

## 5. Measurement-first validation plan

### Baseline before changes
- Record initial render time for 10,000 rows.
- Record filter keystroke latency on representative data.
- Record drawer open/close latency.
- Record save success, failure, timeout, offline, 409, and retry behavior using controlled mocked responses.
- Record image loading layout shift with absent and large images.
- Review keyboard-only path through filters, table, selection, drawer, save, upload, and close.

### Acceptance conditions
- No save failure is silent.
- Dirty or saving edits cannot be lost through Escape or accidental close.
- Loading, empty, permission, conflict, offline, rate-limit, timeout, server-error, retry, and partial-failure states are visible and distinguishable.
- Keyboard users can complete core edit/save/upload flows.
- Focus is always visible and restored after drawer close.
- Reduced-motion users receive minimal movement with preserved state feedback.
- 10,000-row table remains responsive during filtering and row interaction.
- Images do not cause visible row layout jumps.
- Tablet layout keeps primary actions reachable.

### Rollback conditions
- Virtualization breaks selection, row focus, or screen-reader row context.
- Debounced/deferred filtering makes result state feel stale without feedback.
- New save-state handling blocks legitimate operator workflows.
- Drawer focus trapping prevents access to required non-modal reference content.
- Error messaging adds noise without clear recovery actions.
- Responsive changes degrade the primary desktop workflow.

### Production rollout
- Ship hardening behind a narrow feature flag if possible.
- Start with save/error recovery and drawer accessibility before performance polish.
- Monitor save failures, retries, conflicts, abandoned dirty drawers, filter latency, and upload failures.
- Keep rollback scoped: state handling, virtualization, drawer behavior, and responsive sizing should be independently reversible.


## Output C

## 1) Sequencing and verdict

**Correct sequence:** baseline/audit → harden correctness and recovery → measure and optimize hot paths → polish within the existing design system → validate with rollback gates.

**One-line verdict:** As described, this surface is not production-ready for a 10,000-row operations workflow because save failures can be silent, required recovery states are absent, drawer accessibility is unsafe, and the table/filter path is unbounded.

---

## 2) Prioritized findings

### P0 — Silent save failure can mislead operators into data loss
- **Source evidence:** `catch {}` swallows `api.save(product)` errors; `setSaving(false)` runs after failure with no error state.
- **Why it matters:** Operators may believe inventory edits saved when they did not.
- **Runtime hypothesis:** Actual backend/API layer may emit global errors, but that is not shown here and cannot be assumed.
- **Fix:** Return explicit save states: `idle | saving | saved | failed | conflict | offline | unauthorized`; surface retry, last-saved timestamp, field-level/server messages, and telemetry-safe error context.

### P0 — Drawer interaction can interrupt pending writes and lacks modal safety
- **Source evidence:** Drawer does not trap focus/background interaction; Escape closes it while save is pending; save/close are icon-only.
- **Why it matters:** Users can lose context, trigger background actions, or close during a pending save with no recovery path.
- **Runtime hypothesis:** A shared `EditDrawer` may add some behavior internally, but notes explicitly say focus trap/background handling are absent.
- **Fix:** Add modal semantics if it is modal, focus trap, focus restore, inert/blocked background, labeled controls, pending-save close guard, and clear “saving / failed / retry / discard” paths.

### P1 — Required production states are missing
- **Source evidence:** Blank table body during initial/filter loading; no empty, 401/403, 409, 429, 500, timeout, offline, retry, or partial batch failure states.
- **Why it matters:** Operations staff cannot distinguish “no products,” “still loading,” “not authorized,” “rate limited,” “conflict,” or “failed but recoverable.”
- **Runtime hypothesis:** Route-level boundaries may catch some failures, but no state ownership is described for this surface.
- **Fix:** Own a state matrix for initial load, filter load, empty results, permission, auth expiry, conflict, rate limit, server error, timeout, offline, retrying, and partial batch outcomes.

### P1 — Table/filter performance is unbounded for stated scale
- **Source evidence:** `{rows.map(...)}` renders all rows; notes say all 10,000 rows render at once and filtering recalculates synchronously on every keystroke.
- **Why it matters:** This is a clear hot path for keyboard-heavy operators.
- **Runtime hypothesis:** Static code proves unbounded work, not actual latency on target devices; severity stays P1 until measured release-blocking lag is observed.
- **Fix:** Bound rendered rows with existing pagination/windowing patterns, memoize derived rows, defer/debounce filter work appropriately, avoid global state churn, and measure keystroke-to-render latency.

### P1 — Responsive/tablet contract is not credible as written
- **Source evidence:** `.page { min-width: 1180px; }`; fixed drawer width `520px`; fixed row columns; tablet behavior not described.
- **Why it matters:** Tablet support can become horizontal page overflow with unreachable actions.
- **Runtime hypothesis:** A parent shell may provide controlled horizontal scrolling, but no evidence says critical actions remain reachable.
- **Fix:** Keep unavoidable horizontal overflow isolated to the data grid, not the whole page; define tablet breakpoints, drawer width constraints, sticky critical actions, and touch target sizing.

### P1 — Accessibility fundamentals are missing or contradicted
- **Source evidence:** `.icon-button { width: 28px; height: 28px; outline: none; }`; icon-only save/close; no labels, keyboard navigation, focus-visible, screen-reader behavior, or reduced motion described.
- **Why it matters:** Keyboard-heavy operators and assistive tech users need predictable focus, names, target sizes, and reduced-motion behavior.
- **Runtime hypothesis:** Components may add aria labels internally, but the source notes say labels/focus behavior are not described; `outline: none` is a decisive risk unless replaced by visible `:focus-visible`.
- **Fix:** Add accessible names, visible focus states, keyboard row navigation, table/grid semantics, drawer focus management, reduced-motion CSS, and larger effective targets for tablet.

### P2 — Hostile data will break layout and trust
- **Source evidence:** Names can be 1–200 chars; prices may be missing; translations expand labels 60%; images may be absent or 8MB; `.product-name` truncates; fixed grid columns.
- **Why it matters:** Operators need enough context to identify products and avoid editing the wrong row.
- **Runtime hypothesis:** Tooltips/detail drawer may expose full values elsewhere, but not shown.
- **Fix:** Provide full-name access on focus/hover or drawer, missing-price affordance, resilient localized labels, reserved image boxes, fallback thumbnails, image size validation/compression, and non-shifting placeholders.

### P2 — Motion implementation is too broad and may be expensive or inaccessible
- **Source evidence:** `.product-row, .drawer { transition: all 300ms ease-in; }`; reduced motion not described.
- **Why it matters:** `transition: all` can animate layout/paint properties accidentally; `ease-in` can feel sluggish for drawer entry; reduced-motion users get no alternative.
- **Runtime hypothesis:** Actual changed properties are unknown, so jank is not proven.
- **Fix:** Transition only `transform`/`opacity` where appropriate, use purposeful durations/easing, disable or simplify under `prefers-reduced-motion`, and avoid animating many rows.

### P3 — Autosave status is underspecified
- **Source evidence:** Only a boolean `saving` is stored.
- **Why it matters:** A single global boolean cannot distinguish which product is saving, saved, failed, stale, conflicted, or retrying.
- **Runtime hypothesis:** `EditDrawer` may localize details, but not shown.
- **Fix:** Track per-edit lifecycle with timestamps and recoverable error payloads; prevent false “saved” states after failures.

---

## 3) Concrete fixes by area

### Hostile data
- Reserve image dimensions in every row; show absent-image fallback.
- Reject/compress oversized uploads before save where product rules allow; show progress and failure.
- Treat missing price as an explicit state, not blank text.
- Keep 200-character names identifiable: truncate in rows but expose full value via focusable disclosure, title/details, or drawer context.
- Test labels with 60% expansion and long currency/number formats.
- Ensure grid columns can shrink safely; do not let product names push controls offscreen.

### Failures and recovery
- Replace `catch {}` with typed error handling and user-visible outcomes.
- Add specific UI for 401/403, 409 conflict, 429, 500, timeout, offline, retry, and partial batch failure.
- Preserve edits locally while retrying or after failed save.
- For 409, show server version versus local change and require explicit resolve.
- For partial batch failure, identify failed rows and allow retry only failed items.
- Make autosave status truthful: saving, saved at time, failed, retrying, offline queued, conflict.

### Responsive layout
- Remove page-level minimum width as the only tablet strategy.
- Constrain horizontal scrolling to the table region if dense columns must remain.
- Make drawer width `min(520px, viewport-safe-width)` with tablet-specific behavior.
- Keep filters, bulk actions, save/close, and row primary identifiers reachable.
- Define tablet breakpoints and minimum effective target sizes before polish.

### Accessibility
- Add accessible names to icon-only save and close controls.
- Restore visible `:focus-visible`; do not rely on removed outlines without replacement.
- Trap focus in the drawer, restore focus on close, and block background interaction when modal.
- Disable Escape close while saving, or require confirmation with recovery copy.
- Provide keyboard navigation for rows, selection, filters, drawer actions, and bulk actions.
- Use semantic table/grid structure appropriate to the interaction model.
- Respect `prefers-reduced-motion`.
- Confirm screen-reader announcements for loading, save success/failure, conflict, and upload progress.

### State recovery
- Keep unsaved edits across transient failures, drawer close attempts, and auth interruptions where safe.
- Confirm destructive close/discard when pending or failed changes exist.
- Store enough local state to retry without retyping.
- Prevent stale saves from overwriting newer edits; handle out-of-order save responses.
- Make permission-specific affordances explicit: disabled with reason, hidden only when policy requires it.

### Performance
- Bound row rendering via existing table pagination/windowing/virtualization patterns.
- Memoize filtered/sorted rows with correct dependencies.
- Avoid synchronous recalculation on every keystroke; use deferred input or debounced filtering where it preserves operator flow.
- Keep row components memoized and avoid passing unstable props/functions.
- Lazy-load or defer noncritical images; reserve dimensions to prevent layout shift.
- Replace `transition: all` with property-specific transitions.
- Do not introduce a new heavy table dependency unless current project primitives cannot meet measured budgets.

---

## 4) Static detector-like signal reconciliation

**Decisive from the supplied source/notes:**
- `catch {}` means this save path has no local error handling.
- Blank loading body and missing listed states mean this surface does not represent required production states as described.
- Rendering all 10,000 rows and synchronous filtering prove unbounded render/filter work.
- `outline: none` on icon buttons is an accessibility failure unless a replacement focus style exists elsewhere.
- No focus trap/background lock in the drawer is unsafe for a modal edit surface.
- `transition: all` is a concrete implementation smell.
- Fixed `min-width`, fixed grid columns, and fixed drawer width are responsive risks for tablet support.

**Needs project/runtime context before final severity or exact implementation:**
- Actual perceived latency, INP, memory use, and scroll smoothness.
- Whether route-level auth/error boundaries already cover some failures.
- Whether shared components inject aria labels, focus styles, or modal behavior despite this snippet.
- Whether the existing design system already defines table density, drawer motion, error banners, toasts, or upload components.
- Whether server-side filtering, pagination, caching, or API conflict semantics exist.
- Whether horizontal table overflow is an accepted pattern in this product.
- Actual contrast, hit target comfort, screen-reader output, and reduced-motion behavior.
- Real upload constraints, image processing location, and offline policy.

---

## 5) Measurement-first validation plan with rollback/acceptance

### Baseline before changes
- Capture current behavior for 10,000 rows: initial render, filter keystroke latency, row selection, drawer open/close, save success/failure, and image-heavy rows.
- Record mounted row count, long tasks, memory trend, layout shifts, and p95 key-to-visible-results time.
- Exercise state cases with controlled API responses: 401/403, 409, 429, 500, timeout, offline, and partial batch failure.
- Keyboard-only pass: filters → table → bulk selection → drawer → save/close → recovery.
- Assistive-tech-oriented pass: names, roles, announcements, focus order, and focus restoration.
- Responsive pass for desktop and tablet widths.

### Provisional acceptance conditions
- No save failure can end in a false-success or silent state.
- Closing during pending/failed save cannot discard edits without an explicit recoverable choice.
- Every listed loading/empty/error/permission/conflict/offline/partial state renders specific copy and an available next action.
- 10,000-row path has bounded DOM work; mounted row count remains within the chosen table strategy’s expected window/page size.
- Provisional performance budget: p95 filter input-to-visible-update under 150ms on target desktop hardware and under 250ms on supported tablet hardware; no repeated long tasks over 50ms during ordinary filtering/selection.
- Image rows reserve dimensions; no noticeable layout shift from late image load, with CLS budget ratified by the project.
- Keyboard focus is always visible; drawer traps/restores focus; icon-only actions have accessible names.
- Reduced-motion mode preserves state feedback without broad motion.

### Rollback conditions
- Roll back or feature-flag optimization changes if measured input latency, memory, or error rate regresses beyond agreed budget.
- Roll back visual/motion polish if it breaks existing design-system tokens, focus visibility, reduced-motion behavior, or operator task speed.
- Roll back table strategy if it loses selection state, keyboard position, screen-reader usability, or bulk-action correctness.
- Roll back autosave changes if they introduce duplicate writes, stale overwrites, or unrecoverable conflicts.

No runtime detector, browser, build, profiler, accessibility tree, network throttle, or device validation is claimed here; this is a static production audit based only on the supplied facts.
