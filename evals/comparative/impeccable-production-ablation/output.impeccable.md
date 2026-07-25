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
