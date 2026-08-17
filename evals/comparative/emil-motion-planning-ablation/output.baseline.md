## 1. Recon summary

- **Stack signals:** TSX components, CSS files, CSS custom-property tokens, component-local styles, and an arbitrary animation class in `className`.
- **Where motion lives:**
  - Global-ish motion tokens and shared selectors: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Component markup animation hook: `src/components/CommandPalette.tsx`
  - Pointer-driven JS animation: `src/components/SortableQueue.tsx`
- **Existing conventions visible in evidence:**
  - Semantic tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`
  - Correct local precedent: `Button.css` uses explicit `transform` transition, semantic tokens, and a Reduced Motion branch that shortens rather than removes all feedback.
  - Existing authority requires crisp motion, token usage, visible focus, and Reduced Motion feedback preservation.
- **Product personality:** calm desktop operations console; motion should clarify cause/effect and state continuity while staying fast enough for repeated keyboard-heavy workflows.
- **Frequency map from snippets only:**
  - Very high: buttons, command palette
  - High: popovers
  - Medium: toasts / async feedback
  - Lower but high-salience: sortable queue drag/drop
- **Evidence level:** static snippets only. No runtime, computed-style, trace, screen recording, accessibility-tree, device, or user validation was performed.

---

## 2. Priority table

| Priority | Finding | Static evidence | Risk / product fit issue | Direction |
|---:|---|---|---|---|
| P0 | Command palette motion is long and non-tokenized | `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard surface may feel delayed; arbitrary timing bypasses semantic system | Move to named/tokenized motion, shorten, add Reduced Motion path |
| P0 | Popover uses broad transition and slow ease-in | `.popover { transition: all 360ms ease-in; }` | `all` may animate unintended properties; ease-in delays feedback; no Reduced Motion branch visible | Restrict to `opacity, transform`; use existing tokens/ease |
| P1 | Toast enters via `top` over 500ms | `from { top: -24px; opacity: 0; }` and `500ms ease-in` | Slow feedback for operational alerts; position-property animation is not the crisp precedent shown elsewhere | Use stable position plus `transform`/`opacity`, tokenized duration |
| P1 | Sortable snap duration is hard-coded and slow for direct manipulation | `animateTo(..., { duration: 400 })` | Drop completion may lag user intent; no visible Reduced Motion branch | Token-align snap duration; add Reduced Motion duration branch |
| P2 | Pointer move writes style on every event | `style.setProperty("--drag-y", ...)` inside `onPointerMove` | Could over-update during drag; needs direct-manipulation smoothness without extra work | Coalesce writes with animation frame if full code confirms no existing throttle |
| P2 | Reduced Motion is inconsistent across snippets | Only `Button.css` shows `@media (prefers-reduced-motion: reduce)` | Product authority requires feedback-preserving Reduced Motion path | Apply same pattern to palette, popover, toast, sortable snap |

---

## 3. Implementation plans

### Plan A — Normalize command palette and popover overlay motion

**Files / current excerpts**

```css
/* src/styles/motion.css */
:root {
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
}

.popover {
  transform-origin: center;
  transition: all 360ms ease-in;
}
```

```tsx
// src/components/CommandPalette.tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div
      data-open={open}
      className="animate-[palette_420ms_ease-in_both]"
    >
      <SearchResults />
    </div>
  );
}
```

**Target behavior**

- Command palette and popovers should appear promptly, using small opacity/transform changes to preserve causality.
- No broad `transition: all`.
- No long `ease-in` entry on high-frequency surfaces.
- Reduced Motion should keep state feedback through short opacity/focus/visibility changes, not remove all response.

**Project conventions to follow**

- Use existing semantic tokens first:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive`
- Match the proven `Button.css` pattern: explicit animated property, tokenized duration/ease, Reduced Motion override.

**Ordered steps**

1. Read the complete versions of:
   - `src/styles/motion.css`
   - `src/components/CommandPalette.tsx`
   - any CSS file that defines `palette` keyframes or command palette classes.
2. Confirm whether `.popover` has open/closed state selectors elsewhere.
3. Replace `.popover` transition with explicit properties only:
   - `opacity`
   - `transform`
4. Use `var(--duration-fast)` for small popover transitions unless full-file evidence shows panels are intentionally used.
5. Replace the arbitrary command palette animation class with a named class or existing component class using semantic tokens.
6. Drive open/closed styling from `data-open`.
7. Ensure closed state does not trap focus or preserve interactable hidden controls; if that is already handled elsewhere, do not duplicate behavior.
8. Add Reduced Motion handling consistent with the button precedent:
   - shorten duration, e.g. `80ms`
   - avoid scale/large translation
   - preserve opacity/state feedback.

**Hard boundaries**

- Do not change search behavior, result rendering, keyboard shortcuts, focus ownership, or open/close state management unless full-file review proves motion currently owns them.
- Do not introduce new global tokens unless the complete style system lacks a suitable existing token.
- Do not add decorative bounce, overshoot, blur, or spring effects; this surface should stay operational and calm.

**Mechanical checks**

- Search for remaining `animate-[palette_420ms_ease-in_both]`.
- Search for `.popover` `transition: all`.
- Run the nearest available CSS/TS lint, type-check, and build commands after implementation.

**Runtime / feel checks to perform later, not yet performed**

- Open/close command palette repeatedly by keyboard.
- Confirm first result focus visibility is not obscured by motion.
- Open/close representative popovers.
- Check that rapid repeat invocation does not feel delayed or visually stuck.

**Reduced Motion behavior**

- Command palette: short opacity/state change; no scale or travel-heavy movement.
- Popover: short opacity change with minimal or no transform.
- Feedback remains visible.

**Source-drift stop condition**

Stop before editing if full files show an existing motion abstraction, token, animation utility, or state machine that supersedes the snippets. Re-plan against the actual abstraction rather than layering new CSS beside it.

---

### Plan B — Convert toast entry to crisp transform/opacity feedback

**File / current excerpt**

```css
/* src/components/toast.css */
@keyframes toast-enter {
  from { top: -24px; opacity: 0; }
  to { top: 0; opacity: 1; }
}

.toast {
  animation: toast-enter 500ms ease-in forwards;
}
```

**Target behavior**

- Toasts should communicate arrival quickly without feeling urgent or sluggish.
- Entry should be stable-layout-oriented: use `transform` and `opacity`, not animated `top`.
- Timing should align with existing tokens.
- Reduced Motion should still provide visible arrival feedback.

**Project conventions to follow**

- Prefer `var(--duration-fast)` for quick feedback.
- Use `var(--ease-responsive)`.
- Follow `Button.css` Reduced Motion precedent by shortening duration rather than removing feedback entirely.

**Ordered steps**

1. Read the complete `src/components/toast.css`.
2. Confirm whether `.toast` positioning depends on `top` being animated or whether `top` can be a stable final value.
3. Replace keyframes with transform-based entry:
   - from: slight upward translate plus `opacity: 0`
   - to: `translateY(0)` plus `opacity: 1`
4. Set stable positioning outside the keyframes if needed, e.g. final `top` value on `.toast`.
5. Change animation duration from `500ms` to an existing token, likely `var(--duration-fast)` or at most `var(--duration-panel)` if the full design system treats toasts as panel-like.
6. Replace `ease-in` with `var(--ease-responsive)`.
7. Add `@media (prefers-reduced-motion: reduce)`:
   - reduce duration to the local precedent of `80ms`
   - remove or minimize translate distance
   - keep opacity/state feedback.

**Hard boundaries**

- Do not change toast queueing, dismissal timeout, stacking order, severity styling, or ARIA/live-region behavior unless full-file review shows motion is entangled with them.
- Do not add attention-grabbing shake, bounce, or large travel.
- Do not make Reduced Motion silent; feedback must remain perceivable.

**Mechanical checks**

- Search for other `toast-enter` definitions.
- Search for hard-coded `500ms ease-in` toast animation references.
- Run CSS lint/build or nearest project validation after implementation.

**Runtime / feel checks to perform later, not yet performed**

- Trigger one toast and a stacked sequence.
- Confirm arrival is noticeable but not distracting.
- Confirm toast text remains readable throughout entry.
- Confirm Reduced Motion still signals arrival.

**Reduced Motion behavior**

- Very short opacity transition.
- No meaningful travel.
- Same final visual state.

**Source-drift stop condition**

Stop if complete files reveal the toast position is intentionally animated for stack layout calculations or collision handling. In that case, re-plan with the owning layout logic instead of replacing keyframes in isolation.

---

### Plan C — Token-align sortable queue drag completion and reduce pointer churn

**File / current excerpt**

```tsx
// src/components/SortableQueue.tsx
function onPointerMove(event: PointerEvent) {
  queueRef.current?.style.setProperty("--drag-y", `${event.clientY}px`);
}

function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), { duration: 400 });
}
```

**Target behavior**

- Drag tracking should remain immediate.
- Drop-to-slot completion should be quick enough for operational throughput while preserving spatial continuity.
- Timing should use the same motion language as the rest of the interface.
- Reduced Motion should shorten the snap while preserving a clear commit state.

**Project conventions to follow**

- Prefer token-aligned durations:
  - direct manipulation completion: likely `--duration-fast` or `--duration-panel`
- Avoid decorative motion.
- Preserve feedback under Reduced Motion.

**Ordered steps**

1. Read the complete `src/components/SortableQueue.tsx`.
2. Inspect `animateTo` usage and accepted options:
   - duration units
   - easing support
   - cancellation behavior
   - current Reduced Motion handling, if any.
3. Inspect CSS that consumes `--drag-y`.
4. If no existing pointer throttling exists, coalesce `--drag-y` writes with `requestAnimationFrame`:
   - store latest `clientY`
   - write once per frame
   - cancel pending frame on pointer up/unmount.
5. Replace hard-coded `400` with a local constant derived from the design tokens or an existing shared duration constant.
6. Reduce drop snap duration to a crisp range aligned with tokens:
   - default: `160ms` to `240ms`
   - choose based on whether full code treats slot snapping as a small interaction or panel-like movement.
7. If `animateTo` supports easing, use the responsive ease equivalent.
8. Add Reduced Motion path:
   - duration around `80ms`, or immediate position commit plus visible selected/placed state if the codebase already uses that pattern.
9. Ensure pointer-up cleanup still clears dragging state and pending frame state.

**Hard boundaries**

- Do not change queue ordering rules, nearest-slot calculation, persistence, selection, keyboard behavior, or drag handles unless full-file review proves they are broken by the motion change.
- Do not remove direct visual tracking during drag.
- Do not introduce inertia or overshoot; operators need predictable placement.

**Mechanical checks**

- Search for all `animateTo(` calls to avoid inconsistent duration conventions.
- Search for hard-coded drag durations such as `400`.
- Run type-check and nearest component tests/build after implementation.
- Confirm no animation-frame leak by checking cleanup paths.

**Runtime / feel checks to perform later, not yet performed**

- Drag slowly and quickly, then release near and far from a slot.
- Confirm snap communicates final placement without delaying the next action.
- Confirm rapid repeated drags do not leave stale transforms.
- If keyboard reorder exists, confirm equivalent state feedback is preserved.

**Reduced Motion behavior**

- Drag remains directly coupled to pointer.
- Drop completion is near-immediate but still visibly commits to final slot.
- No travel amplification, bounce, or inertia.

**Source-drift stop condition**

Stop if complete code shows `animateTo` is owned by a shared animation system, physics helper, or accessibility preference layer. Update that owner or use its API instead of adding local preference/duration logic.

---

## 4. Recommended execution order

1. **Plan A first:** highest-frequency keyboard/overlay surfaces and most obvious token violation.
2. **Plan B second:** contained CSS-only improvement with clear precedent.
3. **Plan C third:** requires full interaction-code review and may touch animation scheduling.

---

## Explicitly unverified states

- Actual visual appearance, perceived speed, and interaction feel.
- Whether `palette` keyframes already exist elsewhere.
- Complete token inventory beyond the snippet.
- Actual cascade, specificity, and generated CSS output.
- Popover open/closed state model.
- Command palette focus management and keyboard behavior.
- Toast stacking, live-region behavior, and dismissal timing.
- `animateTo` API, easing support, cancellation, and ownership.
- Reduced Motion behavior outside the shown button precedent.
- Browser/device behavior, frame rate, layout cost, computed styles, and accessibility tree.
