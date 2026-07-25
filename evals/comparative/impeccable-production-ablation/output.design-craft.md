## 1. Correct sequence + verdict

**Sequence:** static audit → define baseline measurements → harden data/failure/recovery/accessibility blockers → optimize measured table/filter/image hot paths → polish visual states within the existing system → release validation with rollback gates.

**Verdict:** Not production-ready for a 10,000-row operations editor: the supplied source shows decisive save-error invisibility, missing recovery states, drawer accessibility gaps, hostile-data fragility, and high-risk unbounded rendering; fix by hardening the existing workflow, not redesigning it.

---

## 2. Prioritized findings: source evidence vs runtime hypotheses

| ID | Pri | Finding | Source evidence | Runtime/context boundary | Concrete fix / acceptance |
|---|---:|---|---|---|---|
| F1 | P0 | Save failures can be silent, causing false confidence and possible data loss. | `catch {}` swallows errors; `setSaving(false)` runs without error state; autosave/status behavior not represented. | Exact server/API semantics and whether parent state mutates optimistically are unknown. | Return typed save result; show success/error/conflict/offline states; retain dirty edits after failure; expose retry; log/report errors; never mark failed save as saved. Acceptance: forced 500/timeout/offline keeps drawer data, announces failure, and allows retry without losing edits. |
| F2 | P0 | Pending save can be interrupted by drawer close. | Notes: Escape closes drawer even while save is pending. | Whether close also discards local edits is not shown, but the interruption path is explicit. | While saving: disable destructive close or require confirmation; allow cancel only if request is abortable and state is recoverable; show “Saving…” with deterministic completion/failure. Acceptance: Escape during pending save cannot silently discard or hide unsaved state. |
| F3 | P1 | Required operational failure states are absent. | Notes explicitly list missing empty, 401/403, 409, 429, 500, timeout, offline, retry, partial batch failure; loading renders blank body. | Exact visual components are unknown, but absence is stated in supplied scope. | Add table-body states: skeleton/progress for loading; empty result with filter reset; permission-specific locked affordances; conflict compare/reload/apply path; rate-limit wait/retry; server/timeout/offline retry; partial batch result summary with per-row status. Acceptance: every listed state renders clear cause, next action, and preserves filters/selection/drawer context where safe. |
| F4 | P1 | Drawer is not accessible as a modal editing surface. | Notes: no focus trap, no background interaction blocking; Save/close are icon-only. CSS: fixed drawer. | Whether drawer is intended modal or non-modal needs product confirmation; current notes describe unsafe modal-like behavior. | If modal: use dialog semantics, labelled title, focus trap, restore focus on close, background inert, Escape policy aware of dirty/saving state. If non-modal: keep table keyboard reachable intentionally and define focus order. Icon buttons need accessible names and visible labels/tooltips where appropriate. |
| F5 | P1 | Keyboard and visible focus support are likely broken for controls. | `.icon-button { width:28px; height:28px; outline:none; }`; notes: keyboard navigation, screen-reader labels, focus-visible not described. | Inherited focus styles could compensate, but `outline:none` is a decisive risk until replaced. | Restore `:focus-visible` ring using existing tokens; ensure 44px-ish tablet hit area or project-approved equivalent; add `aria-label`/text labels; define row, selection, bulk-action, drawer tab order. Acceptance: keyboard-only user can filter, select rows, open/edit/save/close drawer with visible focus. |
| F6 | P1 | 10,000-row rendering and synchronous filtering are hot-path risks. | `rows.map(...)` renders all rows; notes: all 10,000 rows render; filtering recalculates synchronously on every keystroke. | Actual latency/FPS is unmeasured; static source proves unbounded work, not exact user-perceived lag. | Virtualize table/window rows; memoize filtered results; defer or debounce filter input; keep selection state independent of rendered window; avoid recreating row props unnecessarily. Acceptance: defined keystroke and scroll budgets pass on target desktop/tablet hardware. |
| F7 | P1 | Layout is brittle on tablet and constrained desktop widths. | `.page { min-width:1180px; }`; fixed grid columns; `.drawer { width:520px; height:100vh; }`; tablet behavior not described. | Exact tablet viewport targets unknown. | Keep table horizontally scrollable inside data region, not whole page; keep filters and critical actions reachable; bound drawer with `width:min(520px,100vw)` or approved full-screen tablet drawer; reserve safe-area/viewport height handling. Acceptance: tablet can filter, inspect, edit, save without hidden critical actions. |
| F8 | P2 | Hostile data can damage scannability and correctness. | Names 1–200 chars; translations +60%; missing prices; absent/8MB images; `.product-name` truncates only one field. | Actual column renderers unknown. | Define per-field fallbacks: missing price as explicit “Not set”/em dash with edit affordance; long names truncate with accessible full value; labels wrap or use responsive copy; absent images use stable placeholder; reject/compress oversized uploads with progress/error. |
| F9 | P2 | Image loading may cause layout shift and memory/network pressure. | Image dimensions not reserved; some images absent or 8MB. | Actual image components and CDN behavior unknown. | Reserve width/height/aspect ratio; lazy-load offscreen images; generate thumbnails; enforce upload size/type validation; show per-image upload progress and failure. Acceptance: no visible row jump when images load; 8MB upload has clear progress/failure path. |
| F10 | P2 | Motion choices are broad and potentially uncomfortable/performance-hostile. | `.product-row, .drawer { transition: all 300ms ease-in; }`; reduced motion not described. | Actual animated properties and frame behavior need runtime inspection. | Replace `transition: all` with named properties, mostly transform/opacity; use faster, interruptible drawer motion; disable or simplify under reduced motion while preserving state feedback. |
| F11 | P2 | Single `saving` boolean is too coarse for complex operations. | `const [saving,setSaving]`; passed to one `EditDrawer`. | Source does not prove concurrent saves or bulk operations share this flag. | Track save state by product/request ID; distinguish idle/dirty/saving/saved/error/conflict; prevent stale completion from overwriting newer edits. |
| F12 | P3 | Blank loading body and missing disabled states reduce trust. | Notes: blank body during initial/filter loading; disabled/permission affordances not described. | Visual severity depends on surrounding chrome. | Use compact skeleton or progress row; disable unavailable actions with reason; keep existing density and table grammar. |

---

## 3. Concrete hardening/polish moves by area

- **Hostile data:** add field-level display contracts for long names, missing prices, long translations, absent images, oversized uploads, and upload failures; preserve full values through accessible labels/tooltips or detail cells.
- **Failures/recovery:** model request state explicitly: loading, empty, unauthorized, forbidden, conflict, rate-limited, server error, timeout, offline, partial success, dirty, saving, saved, failed; each state needs message, action, and preserved context.
- **Responsive layout:** remove page-level forced overflow as the only strategy; confine horizontal overflow to the table; keep filters/bulk actions/drawer controls reachable; cap drawer width to viewport or switch to an approved tablet full-screen drawer.
- **Accessibility:** restore visible focus, label icon-only controls, define keyboard row navigation/selection, trap or intentionally manage drawer focus, restore focus on close, block background interaction if modal, and announce save/error state changes.
- **State recovery:** never clear local edits or dirty state on failed save; handle 409 with compare/reload/apply choice; protect pending saves from Escape/close; support retry without resetting filters, selection, or drawer content.
- **Performance:** virtualize 10,000 rows, memoize/defer filtering, reserve image dimensions, thumbnail/lazy-load images, isolate row re-renders, and measure before/after rather than relying on static smell alone.

---

## 4. Static detector-like signal reconciliation

**Decisive from supplied source/scope:**
- `catch {}` with no error branch proves save errors are swallowed in this snippet.
- Explicit notes prove missing listed states in the supplied surface description.
- `rows.map` plus 10,000-row note proves unbounded initial row rendering.
- Fixed `min-width:1180px`, fixed columns, and fixed 520px drawer prove responsive constraints exist.
- `outline:none` proves native outline is removed on `.icon-button`.
- Explicit notes prove no drawer focus trap/background blocking and icon-only save/close.

**Needs project/runtime context before final severity or implementation choice:**
- Exact perceived slowness, FPS, input delay, layout shift, and memory impact.
- Whether inherited CSS restores focus visibility despite `outline:none`.
- Whether the drawer is intended modal, modeless inspector, or hybrid.
- Whether optimistic updates mutate `rows` before save confirmation.
- Whether global `saving` conflicts with concurrent saves or bulk operations.
- Exact tablet breakpoints, supported browsers, API retry semantics, image CDN behavior, and permission model.

---

## 5. Measurement-first validation plan with rollback/acceptance

1. **Baseline first, before optimization claims**
   - Measure initial render, filter keystroke latency, scroll responsiveness, drawer open/close responsiveness, image load shift, and save-state transitions on target desktop and tablet-class hardware.
   - Record row count, image mix, network profiles, and browser versions.

2. **Failure-state validation**
   - Inject or mock 401/403/409/429/500/timeout/offline/partial batch responses.
   - Acceptance: every state renders cause + next action; filters/selection/drawer edits survive where appropriate; failed save never appears successful.

3. **Accessibility validation**
   - Keyboard-only pass for filters, table rows, selection, bulk actions, drawer open/save/close.
   - Screen-reader/name pass for icon buttons, drawer title, save status, errors.
   - Acceptance: visible focus at all times, no background focus leak for modal drawer, Escape cannot destroy pending/dirty work.

4. **Responsive validation**
   - Test supported desktop widths and tablet widths/orientations.
   - Acceptance: table may scroll within its region, but primary actions, filters, drawer controls, and status remain reachable.

5. **Performance validation**
   - Compare baseline vs virtualized/deferred implementation.
   - Acceptance targets should be set by the product team, but release should require no obvious typing stalls while filtering, smooth practical scrolling through 10,000 rows, bounded row renders, and no major image-induced layout jumps.

6. **Rollback conditions**
   - Roll back if virtualization breaks selection, row identity, keyboard navigation, screen-reader order, bulk operations, or edit-drawer context.
   - Roll back if new save guards block legitimate recovery, hide API errors, or make offline/conflict resolution worse.
   - Roll back if responsive changes hide columns/actions without an accessible way to reach them.

7. **Release acceptance**
   - Ship only when P0 issues are closed, P1 issues have verified behavior or explicit product sign-off, performance measurements meet agreed budgets, and all newly added states preserve the existing workflow and design system.
