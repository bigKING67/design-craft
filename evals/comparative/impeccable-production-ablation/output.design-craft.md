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
