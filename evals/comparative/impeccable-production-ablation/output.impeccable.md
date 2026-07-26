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
