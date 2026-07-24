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
