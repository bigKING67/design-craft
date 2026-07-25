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
