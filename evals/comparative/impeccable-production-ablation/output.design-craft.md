## 1. Correct sequence + verdict

**Sequence:** read-only audit → data/state hardening → accessibility + responsive hardening → measurement-led performance optimization → restrained visual polish → validation + rollback gates.

**Verdict:** This is not a redesign problem; it is a production hardening issue with P0 data-recovery risk and P1 accessibility, tablet, and 10,000-row performance risks that should be fixed before polish.

## 2. Prioritized findings ledger

| ID | Pri | Source evidence | Runtime hypothesis / unknown | Concrete repair | Acceptance evidence needed |
|---|---:|---|---|---|---|
| F1 | P0 | `catch {}` swallows save failures; global `saving`; missing 409/offline/retry/partial failure states; Escape closes drawer during pending save. | API may have server-side safeguards, but UI currently gives no reliable recovery path. | Replace boolean with explicit save state per product/drawer/batch: `idle/dirty/saving/saved/error/conflict/offline/retrying`. Preserve dirty draft, block or confirm close during pending/dirty state, show conflict resolution, retry, and partial-batch result summaries. | Failed save is visible; user can retry or discard intentionally; conflict cannot silently overwrite; pending save cannot be lost by Escape/close. |
| F2 | P1 | `{rows.map(...)}` renders all rows; notes say 10,000 rows and synchronous filtering on every keystroke. | Static source proves unbounded work, but actual latency/INP/memory requires measurement. | Bound table work using existing project pattern: virtualization, pagination, or server/windowed querying. Defer/debounce filter input appropriately, memoize derived rows, keep row props stable, preserve selection across windows/pages. | 10,000-row route stays within ratified input, long-task, memory, and mounted-row budgets. |
| F3 | P1 | Drawer lacks focus trap/background isolation; Save/Close are icon-only; `.icon-button` is 28×28 and `outline: none`; keyboard/screen-reader/focus-visible not described. | Components may add labels elsewhere, but supplied facts do not prove accessible operation. | Treat drawer as modal or non-modal explicitly. If modal: dialog semantics, labelled title, focus trap, focus restore, inert/background block. Add accessible names to icon buttons, visible `:focus-visible`, disabled/loading labels, and effective tablet target size near 44px. | Keyboard-only user can open, edit, save, close, and recover focus; labels are announced; focus is visible; background cannot be accidentally edited. |
| F4 | P1 | `.page { min-width:1180px }`; fixed grid columns; drawer fixed `520px`; tablet support required; translations expand labels by 60%. | A horizontal data-table region may be acceptable if intentional, but fixed page/drawer can make actions unreachable on tablets. | Keep desktop-first table density, but isolate overflow to the table, not the whole page. Use `minmax()`/responsive column rules, sticky critical columns/actions, drawer width `min()/clamp()`, and translation-safe labels. | Tablet viewport retains filters, bulk actions, drawer controls, and save status without page-level clipping. |
| F5 | P1 | Initial/filter loading render blank table body; empty, 401/403, 409, 429, 500, timeout, offline, retry, partial batch failure states absent. | Actual API/error taxonomy may differ, but the UI state contract is incomplete. | Add owned loading skeleton/rows, empty result copy, permission-specific affordances, rate-limit backoff, timeout/offline banners, retry actions, conflict state, and partial-batch success/failure report. | Each listed state renders specific context, user action, and recovery path without losing current filters/selection/draft. |
| F6 | P2 | Product names 1–200 chars; prices may be missing; images absent or 8MB; image dimensions not reserved. | Real data distribution and CDN behavior unknown. | Use resilient cells: truncation with accessible full-name disclosure, missing-price placeholder/status, absent-image fallback, reserved image aspect ratio, size limits, upload validation/compression/progress/error states. | No layout jump from images; long names do not break actions; missing fields remain understandable. |
| F7 | P2 | Bulk selection and permission-specific affordances are route requirements but not represented in the snippet/notes. | Selection implementation may live inside child components. | Ensure selection model is stable across filtering/windowing, with “selected visible/all matching” clarity, permission-aware disabled states, and partial-batch reconciliation. | Bulk actions never apply to an ambiguous set; denied actions explain why and preserve selection safely. |
| F8 | P3 | `.product-row, .drawer { transition: all 300ms ease-in; }`; reduced motion not described. | Actual animated properties unknown. | Narrow transitions to intentional properties, preferably `transform/opacity`; remove row-wide transition unless needed; add reduced-motion behavior; align status/motion copy with existing design tokens. | No broad `transition: all`; motion is purposeful, interruptible, and reduced-motion compatible. |

## 3. Fix coverage by concern

- **Hostile data:** covered by F4/F6/F7 — long names, expanded translations, missing prices, absent/large images, and selection across filtered/windowed data.
- **Failures:** covered by F1/F5 — visible save errors, auth/permission, conflict, rate limit, server error, timeout, offline, retry, and partial-batch states.
- **Responsive layout:** covered by F4 — preserve desktop table density while preventing page-level overflow and unreachable drawer controls on tablets.
- **Accessibility:** covered by F3/F8 — focus management, labelled controls, visible focus, target size, keyboard flow, screen-reader semantics, and reduced motion.
- **State recovery:** covered by F1/F5/F7 — dirty draft preservation, close/escape safeguards, conflict handling, retry, partial success, and stable selection.
- **Performance:** covered by F2/F6/F8 — bounded row rendering/filtering, reserved image dimensions, safer animation properties, and measurement before claiming improvement.

## 4. Static signal reconciliation

**Decisive from supplied source/facts:**

- Rendering `rows.map` for a stated 10,000-row table is unbounded DOM work.
- Synchronous filter recalculation on every keystroke is an input hot-path risk.
- `catch {}` proves save failures can be swallowed at this layer.
- Missing represented states are decisive because the notes explicitly list them as absent.
- Fixed `min-width`, fixed grid columns, and fixed drawer width are real layout constraints.
- `outline: none`, 28px icon buttons, icon-only controls, and no described labels/focus trap are accessibility risks requiring repair or contrary evidence.
- `transition: all` is a real maintainability/performance/motion smell.
- Missing image dimensions create a credible layout-shift risk.

**Needs project/runtime context before final severity or exact implementation:**

- Actual filter latency, INP, memory, scroll smoothness, and frame rate.
- Whether existing table primitives already provide virtualization/pagination patterns.
- Whether child components add accessible names, roles, or keyboard behavior not shown here.
- Whether fixed table width is an accepted design-system pattern with isolated horizontal scroll.
- Whether API contracts provide idempotency, optimistic concurrency, draft persistence, or conflict protection.
- Actual tablet breakpoints, supported browsers, device class, and operational network conditions.
- Final visual quality, contrast, and density; static CSS alone cannot prove the rendered experience.

## 5. Measurement-first validation plan

1. **Baseline before changes**
   - Use representative 10,000-row data with 1, 20, 60, and 200-character names, missing prices, absent images, and large upload candidates.
   - Capture current budgets for initial render, filter keystroke latency, long tasks, DOM node count, JS heap, layout shift, drawer open/close, and save-state transitions.
   - Provisional gates to ratify: filter input p95 ≤100ms desktop / ≤150ms tablet; no long task over 50ms during common input; mounted rows bounded to visible window plus overscan; CLS ≤0.1; no base-to-head memory regression over 20% without justification.

2. **State and recovery validation**
   - Exercise save success, 401/403, 409, 429, 500, timeout, offline, retry, partial-batch failure, pending-save close/Escape, and reload after dirty draft.
   - Acceptance: every state has user-facing copy, next action, preserved context, and no silent data loss.

3. **Accessibility validation**
   - Keyboard-only path through filters, table selection, edit drawer, upload, save, close, and error recovery.
   - Check accessible names for icon buttons, focus trap/restore, background interaction blocking, visible focus, disabled/loading semantics, and reduced-motion behavior.
   - Acceptance: no keyboard trap except intentional modal containment; no unlabeled critical action; focus remains visible.

4. **Responsive validation**
   - Desktop and tablet breakpoints with expanded translations and long product names.
   - Acceptance: filters, table actions, bulk controls, drawer controls, and autosave status remain reachable; unavoidable overflow is isolated to the data table.

5. **Performance validation after fixes**
   - Re-measure the same scenarios against baseline.
   - Acceptance: bounded row rendering/filtering is proven at 10,000 rows; image dimensions prevent layout jumps; drawer motion does not create measurable interaction regression.

6. **Rollback conditions**
   - Roll back or gate the change if save/conflict handling regresses, bulk selection becomes ambiguous, keyboard access is blocked, tablet critical actions become unreachable, or performance misses ratified budgets.
   - Prefer a feature flag or incremental rollout for table virtualization/windowing and revised save-state behavior, because both touch core operational workflows.
