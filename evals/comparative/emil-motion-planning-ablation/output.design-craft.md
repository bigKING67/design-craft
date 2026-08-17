## 1. Recon summary

Reading this as: a calm desktop operations console for keyboard-heavy operators, optimized for fast state comprehension without decorative delay.

- **Stack signals:** React/TSX components, CSS custom properties, component CSS, and a Tailwind arbitrary animation class.
- **Where motion lives:** `src/styles/motion.css`, component-level CSS, inline style mutation in `SortableQueue`, and class-driven animation in `CommandPalette`.
- **Existing conventions:** semantic motion tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`; `Button.css` is the strongest local precedent: transform-only, tokenized timing/easing, and a Reduced Motion branch.
- **Product personality:** crisp, calm, low-drama utility motion; motion should confirm causality and continuity, not create waiting time.
- **Frequency map:**
  - Very high: command palette, keyboard-triggered surfaces.
  - High/direct: sortable queue dragging.
  - Medium: popovers.
  - Occasional: toasts.
  - Local precedent: button press feedback.
- **Evidence level:** static snippet audit only. No runtime, computed-style, trace, screen recording, device, accessibility-tree, or user-test evidence was performed.

## 2. Vetted priority table

| ID | Priority | Evidence | Finding | Smallest safe correction |
|---|---:|---|---|---|
| F1 | P1 | `CommandPalette.tsx`: `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard surface uses long arbitrary timing and `ease-in`, which risks delayed perceived response. Static code proves the timing/easing choice, not actual feel. | Replace with tokenized, short opacity/transform state transition; preserve instant keyboard throughput and Reduced Motion feedback. |
| F2 | P1 | `motion.css`: `.popover { transform-origin: center; transition: all 360ms ease-in; }` | Popover motion has broad property ownership, centered origin, long duration, and `ease-in`. If this is trigger-anchored UI, causality is weakened. | Use explicit `opacity, transform`; tokenized duration/easing; trigger-relative origin when the primitive exposes it. Stop if this selector is actually for centered modal content. |
| F3 | P2 | `toast.css`: `top` keyframes, `500ms ease-in` | Toast entrance animates layout position and uses a long `ease-in` keyframe. Static source proves layout-property animation risk, not dropped frames. | Move entrance to `transform: translateY(...)` + opacity, shorten to token range, and add Reduced Motion behavior. |
| F4 | P1 | `SortableQueue.tsx`: pointer move writes `--drag-y`; release `animateTo(..., { duration: 400 })` | Direct manipulation excerpt lacks visible evidence of pointer capture, grab offset, measured velocity, presentation-value interruption, or Reduced Motion settle behavior. These may exist elsewhere, so treat as an implementation risk. | Audit the full drag owner, then make drag 1:1, interruptible, transform-owned, and velocity-aware while preserving current snap semantics unless explicitly changed. |
| F5 | P2 | All snippets except `Button.css` omit Reduced Motion handling | Design authority requires a Reduced Motion path that preserves feedback; only the button precedent shows one. | Add component-specific Reduced Motion branches: reduce travel/overshoot, keep opacity/color/focus/static feedback. |
| F6 | P2 | `160ms/240ms` tokens vs `360/400/420/500ms` ad hoc values | Motion vocabulary is drifting from existing semantic tokens. | Reuse existing tokens first; introduce new semantic tokens only if repeated use justifies them. |

## 3. Implementation-ready plans

### Plan A — Normalize high-frequency overlay motion

**Files / current excerpts**

`src/styles/motion.css`

```css
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

`src/components/CommandPalette.tsx`

```tsx
<div
  data-open={open}
  className="animate-[palette_420ms_ease-in_both]"
>
```

**Target behavior**

- Command palette: immediate, keyboard-friendly state feedback; no cinematic entrance.
- Popover: explicit transform/opacity transition, responsive easing, and trigger-relative origin when available.
- All timings use existing semantic tokens unless source review proves a missing repeated semantic need.

**Project conventions**

- Reuse `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the `Button.css` precedent: transform-only where possible, tokenized easing, Reduced Motion branch.
- Do not add dependencies.

**Ordered steps**

1. Confirm `src/styles/motion.css` is the correct global motion home.
2. Replace `.popover` broad transition with explicit properties:
   - `opacity`
   - `transform`
3. Change popover duration from `360ms` to `var(--duration-fast)` or `var(--duration-panel)` based on actual component size:
   - small anchored popover: `--duration-fast`
   - larger panel-like popover: `--duration-panel`
4. Before changing `transform-origin`, inspect the popover primitive/state contract:
   - if it exposes a trigger/collision origin variable, use it with a safe fallback;
   - if this selector is for centered modal-like content, stop and split modal/popover selectors instead.
5. Replace `CommandPalette` arbitrary animation class with a named class, for example `className="command-paletteMotion"`, keeping `data-open={open}`.
6. Define the command palette motion in `src/styles/motion.css` or the established component stylesheet:
   - open: `opacity: 1; transform: scale(1);`
   - closed: `opacity: 0; transform: scale(0.98);`
   - transition: `opacity var(--duration-fast) var(--ease-responsive), transform var(--duration-fast) var(--ease-responsive)`
7. Preserve `SearchResults` rendering and focus ownership; do not move data loading or keyboard handlers.
8. Add `@media (prefers-reduced-motion: reduce)`:
   - remove or minimize scale/travel;
   - keep short opacity feedback around `80ms`, matching the button precedent.

**Hard boundaries**

- Do not change command search behavior, focus restoration, keyboard shortcuts, or result ordering.
- Do not replace the popover primitive.
- Do not introduce new global animation names unless existing usage requires compatibility.
- Do not delete `palette` keyframes unless a static search proves no remaining consumers.

**Mechanical checks**

- Static search for remaining `animate-[palette`, `transition: all`, and `360ms ease-in`.
- Run the project’s closest type-check and lint scripts from the package manifest.
- If style tooling exists, run the CSS/style validation command.
- Verify no new hard-coded duration/easing values were introduced except the Reduced Motion `80ms` precedent.

**Runtime / feel checks to perform later**

- Toggle the command palette repeatedly by keyboard and ensure it does not block typing or focus.
- Open/close popovers from multiple placements and inspect computed `transform-origin`.
- Reverse open/close mid-transition.
- Use browser slow-motion animation inspection for opacity/scale sequencing.

**Reduced Motion behavior**

- Command palette and popover retain visibility/state feedback.
- Positional/scale travel is removed or minimized.
- Focus visibility remains unchanged and visible.

**Source-drift stop condition**

Stop before editing if any of these changed materially: the cited class no longer exists, `open` no longer controls visibility, `.popover` is no longer an anchored overlay, the motion tokens were renamed, or design authority changed the motion contract.

---

### Plan B — Repair toast entrance motion without layout animation

**File / current excerpt**

`src/components/toast.css`

```css
@keyframes toast-enter {
  from { top: -24px; opacity: 0; }
  to { top: 0; opacity: 1; }
}

.toast {
  animation: toast-enter 500ms ease-in forwards;
}
```

**Target behavior**

- Toast appears promptly and calmly.
- Movement uses transform rather than `top`.
- Timing aligns with existing motion tokens.
- Reduced Motion preserves feedback without vertical travel.

**Project conventions**

- Prefer existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the local button precedent for Reduced Motion.
- Keep toast semantics, announcements, dismissal, and timer behavior unchanged unless the toast owner already exposes state needed for transition.

**Ordered steps**

1. Replace `top` animation with transform/opacity.
2. Prefer a transition-based entrance if the toast lifecycle exposes a mounted/open/closed state.
3. If no state attribute/class exists and adding one would require unknown lifecycle changes, use an entrance-only transform/opacity keyframe as the safe first repair.
4. Initial CSS target:
   - from: `transform: translateY(-25%); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
   - duration: `var(--duration-panel)` for larger toast content, otherwise `var(--duration-fast)`
   - easing: `var(--ease-responsive)`
5. If a `[data-state="closed"]` or equivalent already exists, add exit transition using the same properties instead of creating a new lifecycle model.
6. Add `@media (prefers-reduced-motion: reduce)`:
   - no vertical transform;
   - opacity transition only, approximately `80ms`.
7. Keep toast stacking, z-index, placement, ARIA live-region behavior, and dismissal controls untouched.

**Hard boundaries**

- Do not change toast copy, timeout duration, live-region semantics, or dismissal behavior.
- Do not add swipe dismissal or gesture behavior in this plan.
- Do not introduce a new toast state machine unless the current toast owner already supports state and only lacks styling.

**Mechanical checks**

- Static search confirms no `top` remains in `toast-enter`.
- Static search confirms `500ms ease-in` is removed from toast motion.
- Run closest type-check/lint/style checks available from project scripts.
- Check for remaining toast animation consumers before deleting `@keyframes toast-enter`.

**Runtime / feel checks to perform later**

- Trigger single and stacked toasts.
- Trigger toasts repeatedly in quick succession.
- Confirm no visual gap breaks pointer access to dismiss controls.
- Hide and restore the document while toast timers are active if the toast lifecycle owns timers.

**Reduced Motion behavior**

- Toast appears with opacity/static feedback.
- No vertical travel.
- Dismiss/focus/announcement behavior remains intact.

**Source-drift stop condition**

Stop before editing if `toast.css` no longer owns toast entrance styling, if `top` is being used for required layout placement rather than animation, or if the toast component has been migrated to another motion API.

---

### Plan C — Harden sortable queue drag and settle behavior

**File / current excerpt**

`src/components/SortableQueue.tsx`

```tsx
function onPointerMove(event: PointerEvent) {
  queueRef.current?.style.setProperty("--drag-y", `${event.clientY}px`);
}

function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), { duration: 400 });
}
```

**Target behavior**

- Dragged item tracks the pointer 1:1 after intent is established.
- Release settles from the current on-screen value, not a stale logical value.
- Current nearest-slot behavior is preserved unless product authority explicitly approves momentum-based target selection.
- Reduced Motion removes bounce/large settle flourish but keeps direct manipulation feedback.

**Project conventions**

- Use existing animation utility `animateTo` only if it can start from current presentation value and accept or preserve velocity.
- Prefer transform-owned movement over layout-position changes.
- Do not add a new animation library unless existing primitives cannot satisfy the contract and the change is separately approved.

**Ordered steps**

1. Inspect the full drag owner around `SortableQueue.tsx` before editing.
2. Confirm whether pointer capture is set on drag start; if absent, add it when drag intent begins.
3. Preserve grab offset:
   - record pointer position and item position at drag start;
   - compute movement relative to that offset, not raw `event.clientY` alone.
4. Move `--drag-y` ownership as narrowly as possible:
   - preferred: dragged item transform owner;
   - avoid updating a broad parent variable if it invalidates a large subtree.
5. Track short time/position history using monotonic timestamps.
6. On release, calculate velocity in CSS px/s.
7. Preserve target semantics initially:
   - keep `nearestSlot(currentY)` as the snap target unless a separate product decision authorizes projected-endpoint targeting.
8. Ensure `animateTo` starts from the current rendered/presentation Y.
9. If `animateTo` cannot start from presentation value or accept velocity, stop and propose a primitive-level change rather than faking interruption with fixed-duration restart.
10. Replace fixed `duration: 400` with either:
   - existing spring/settle config if available; or
   - a bounded tokenized settle using `--duration-panel` only as a temporary non-gesture-grade fallback.
11. Ensure a new drag can interrupt an in-flight settle without visual jump.
12. Add Reduced Motion branch:
   - direct drag remains 1:1;
   - release settle is short, non-bouncy, and can snap immediately if that is the clearest feedback.

**Hard boundaries**

- Do not change queue ordering rules, slot calculation, persistence, keyboard sorting, or data model.
- Do not switch from nearest-slot to momentum-targeted slot selection without explicit approval.
- Do not combine drag translate and press scale on the same `transform` owner unless composed deliberately.
- Do not claim performance improvement without trace evidence.

**Mechanical checks**

- Type-check the component.
- Lint for pointer event cleanup and stale refs.
- Static check that pointer listeners are removed/cancelled.
- Static check that drag writes are scoped to the dragged item or documented transform owner.
- Confirm no new dependency was added.

**Runtime / feel checks to perform later**

- Drag slowly, quickly, and outside the original bounds.
- Release during movement and immediately re-grab during settle.
- Verify no jump on interruption.
- Verify grab offset is preserved.
- Verify keyboard queue operation still works.
- Test Reduced Motion mode.
- If release feel is release-critical, capture a performance trace under representative queue size.

**Reduced Motion behavior**

- User-controlled dragging remains direct.
- Release settle avoids bounce and large travel.
- State change remains understandable through position, focus, and static feedback.

**Source-drift stop condition**

Stop before editing if the cited handlers no longer own drag behavior, `animateTo` was replaced, `nearestSlot` semantics changed, keyboard sorting was added nearby and unreviewed, or queue movement is no longer transform-compatible.

## 4. Recommended execution order

1. **Plan A first:** fixes the highest-frequency keyboard and overlay motion while establishing token discipline.
2. **Plan B second:** low-risk CSS repair with clear performance/accessibility upside.
3. **Plan C third:** highest interaction complexity; should run after simpler token/RM conventions are settled.

## Explicitly unverified states

- Actual rendered timing, smoothness, frame pacing, compositing, or layout cost.
- Whether popovers are trigger-anchored, centered modal-like, or both.
- Whether command palette animation blocks focus or typing.
- Whether toast lifecycle supports open/closed transition states.
- Whether `SortableQueue` already has pointer capture, velocity tracking, grab-offset preservation, or interruption handling outside the excerpt.
- Reduced Motion behavior beyond the one provided button precedent.
- Browser, device, refresh-rate, accessibility-tree, keyboard-flow, and screen-reader behavior.
