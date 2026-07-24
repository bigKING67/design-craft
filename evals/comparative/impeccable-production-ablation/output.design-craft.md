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
