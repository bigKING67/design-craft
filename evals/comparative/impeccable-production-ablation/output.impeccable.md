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
