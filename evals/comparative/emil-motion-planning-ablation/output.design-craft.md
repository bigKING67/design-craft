## 1. Recon summary

**Diagnosis:** the snippets show a calm, utility-oriented console with solid token precedent, but several high-frequency or repeated motions use slow `ease-in`, broad property ownership, layout-property animation, or incomplete direct-manipulation evidence.

- **Stack signals:** web frontend with TSX components, CSS modules/global CSS, Tailwind-style arbitrary animation class, imperative pointer handling, and a JS `animateTo(...)` primitive.
- **Where motion lives:**  
  `src/styles/motion.css` tokens + global `.popover`; `src/components/CommandPalette.tsx` class-level animation; `src/components/toast.css` keyframes; `src/components/SortableQueue.tsx` pointer/settle logic; `src/components/Button.css` local precedent.
- **Existing conventions:** semantic durations `--duration-fast: 160ms`, `--duration-panel: 240ms`; responsive ease token `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`; Reduced Motion precedent keeps feedback but shortens duration to `80ms`; button uses explicit `transform` transition only.
- **Product personality:** calm desktop operations console; motion should be crisp, causal, low-drama, and throughput-preserving.
- **Frequency map:**  
  High: command palette, buttons, sortable queue.  
  Common: popovers.  
  Occasional but repeated: toasts.  
  Direct manipulation: sortable queue drag/snap.
- **Evidence level:** static snippets only. No runtime, computed style, animation trace, screen recording, accessibility tree, or user testing was performed.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
| --- | --- | --- | --- | --- |
| P1 | Static | `src/components/CommandPalette.tsx` | High-frequency keyboard surface uses `animate-[palette_420ms_ease-in_both]`: slow duration, delayed-start easing, arbitrary value, and no shown Reduced Motion branch. | Replace with tokenized, explicit opacity/transform transition around `160–240ms` using `--ease-responsive`; Reduced Motion keeps feedback with opacity/static state and short duration. |
| P1 | Static | `src/components/SortableQueue.tsx` | Direct manipulation excerpt shows raw `clientY` CSS-var updates and fixed `animateTo(..., { duration: 400 })`; no evidence of grab offset, pointer capture, velocity handoff, projected snap, or interruption from presentation value. | Audit full component, then implement 1:1 local-coordinate drag with capture/offset/sampled velocity and token/spring-based settle; Reduced Motion removes overshoot/long travel. |
| P2 | Static | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`; broad ownership and delayed response are mismatched for common anchored overlays. | Limit to `opacity, transform`; use `--duration-fast` or `--duration-panel` + `--ease-responsive`; use trigger-aware origin unless confirmed centered. |
| P2 | Static | `src/components/toast.css` | Toast enters by animating `top` for `500ms ease-in`; this is a layout-property animation risk and slower than existing panel token. | Animate `transform` + `opacity` instead; use `--duration-panel` + `--ease-responsive`; Reduced Motion removes vertical travel while preserving appearance feedback. |
| P3 | Static | Cross-snippet | Motion vocabulary is split between semantic tokens, arbitrary Tailwind animation, raw milliseconds, and component keyframes. | During the fixes above, normalize to existing semantic tokens rather than adding a new motion system. |
| Positive precedent | Static | `src/components/Button.css` | Button already demonstrates explicit property transition, semantic token use, and Reduced Motion preservation. | Treat as local pattern for similar micro-feedback. |

## 3. Implementation plans

### Plan A — Tokenize and shorten overlay motion

**Files/current excerpts**

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
  <SearchResults />
</div>
```

**Target behavior**

- Popovers and command palette respond immediately and settle calmly.
- Use existing tokens: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Animate only `opacity` and `transform`.
- Command palette, as a keyboard-heavy surface, should not spend `420ms` entering.
- Reduced Motion preserves open/closed feedback without spatial travel.

**Project conventions**

- Follow the button precedent: explicit animated property, semantic duration token, Reduced Motion override.
- Do not introduce new animation libraries or new global timing vocabulary unless repeated usage proves it necessary.

**Ordered steps**

1. In `src/styles/motion.css`, change `.popover` from `transition: all 360ms ease-in` to explicit properties, for example:
   ```css
   transition:
     opacity var(--duration-fast) var(--ease-responsive),
     transform var(--duration-fast) var(--ease-responsive);
   ```
2. Re-evaluate `transform-origin: center` before keeping it.  
   - If the popover is anchored to a trigger, set origin from existing placement data/custom properties if available.  
   - Keep `center` only for truly centered overlays.
3. Replace `CommandPalette.tsx` arbitrary animation class with a named class or existing utility pattern that uses:
   - normal motion: `opacity` plus very small `transform` delta, `160–240ms`, `--ease-responsive`;
   - no long keyframe restart for repeated open/close.
4. Add or reuse a Reduced Motion media block:
   ```css
   @media (prefers-reduced-motion: reduce) {
     .popover,
     .command-palette-motion {
       transition-duration: 80ms;
       transform: none;
     }
   }
   ```
   Use the actual class name selected in step 3.
5. Confirm focus styles remain visible and are not hidden behind delayed animation.

**Hard boundaries**

- Do not change `SearchResults` behavior, search data loading, command execution, keyboard bindings, or focus ownership.
- Do not add dependencies.
- Do not globally redefine existing tokens without a broader design-system decision.

**Mechanical checks**

- Run the project’s existing type check for `CommandPalette.tsx`.
- Run the existing CSS/lint/build gate that covers `src/styles/motion.css`.
- Search for the old arbitrary class and confirm no stale `palette_420ms_ease-in_both` usage remains unless intentionally documented.

**Runtime/feel checks to perform later**

- Open/close command palette repeatedly by keyboard.
- Interrupt open with close and close with open.
- Verify no visible focus loss and no delayed input readiness.
- Check popover open/close from representative trigger positions.

**Reduced Motion behavior**

- No slide/scale travel.
- Opacity or instant state change still confirms open/closed state.
- Focus indicator remains visible.

**Source-drift stop condition**

Stop before editing if `palette` keyframes are defined elsewhere with behavior not shown here, if `.popover` is also used for centered modal content, or if `DESIGN.md`/tokens have changed materially from the provided excerpt.

---

### Plan B — Convert toast entry from layout motion to transform motion

**Files/current excerpt**

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

- Toast appears promptly without animating layout-position properties.
- Motion communicates arrival but does not distract operators.
- Use `--duration-panel: 240ms` and `--ease-responsive`.
- Reduced Motion removes vertical travel while preserving feedback.

**Project conventions**

- Use semantic duration/easing tokens from `src/styles/motion.css`.
- Match the button precedent: explicit motion property and Reduced Motion branch.
- Keep toast stacking/positioning logic separate from entry animation.

**Ordered steps**

1. Keep layout position as static CSS outside the keyframe, if needed:
   ```css
   .toast {
     top: 0;
   }
   ```
   Only do this if the existing layout requires `top`.
2. Replace keyframes with transform/opacity:
   ```css
   @keyframes toast-enter {
     from { transform: translateY(-8px); opacity: 0; }
     to { transform: translateY(0); opacity: 1; }
   }
   ```
3. Change animation timing:
   ```css
   .toast {
     animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
   }
   ```
4. Add Reduced Motion:
   ```css
   @media (prefers-reduced-motion: reduce) {
     @keyframes toast-enter {
       from { opacity: 0; transform: none; }
       to { opacity: 1; transform: none; }
     }

     .toast {
       animation-duration: 80ms;
     }
   }
   ```
5. If exit animation exists elsewhere, align it to the same property set; do not create an enter/exit mismatch.

**Hard boundaries**

- Do not alter toast queueing, timeout duration, ARIA/live-region behavior, severity styling, or dismissal behavior.
- Do not animate height, margin, top, or left for the entry effect.
- Do not claim performance improvement without a later trace; this plan only removes a known static risk.

**Mechanical checks**

- Run CSS lint/build gate.
- Search for `toast-enter` references and confirm all consumers still receive the expected animation name.
- Verify no duplicate `@keyframes toast-enter` definitions conflict.

**Runtime/feel checks to perform later**

- Trigger one toast, then several in quick succession.
- Confirm entry feels prompt and non-blocking.
- Confirm stacking does not jump when multiple toasts appear.
- Confirm keyboard focus is not moved unexpectedly.

**Reduced Motion behavior**

- Toast still appears/fades in.
- No vertical movement.
- Duration shortened to match existing local precedent.

**Source-drift stop condition**

Stop before editing if `top` is dynamically used for stacked toast positioning in a way that the keyframe intentionally coordinates, if there is already a separate Reduced Motion toast branch, or if token names differ from the provided excerpt.

---

### Plan C — Make sortable queue drag and snap physically accountable

**Files/current excerpt**

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

- Dragged item tracks the pointer in the correct local coordinate space.
- The item does not jump on grab.
- Drag remains tracked after pointer leaves the original bounds.
- Release chooses a slot from current position plus measured velocity/projection, not only a stale logical value.
- Settle motion is interruptible from current presentation value.
- Reduced Motion keeps direct manipulation but removes overshoot and long animated travel.

**Project conventions**

- Preserve throughput for operators; avoid decorative bounce.
- Prefer transform-based movement and direct style writes for pointer-move hot path.
- Use existing `--duration-fast`, `--duration-panel`, and `--ease-responsive` if the existing `animateTo` primitive is duration-based.
- Use existing animation primitive if it supports springs/current-value/velocity; do not add a heavy dependency by default.

**Ordered steps**

1. Inspect the full component before editing:
   - pointer down handler;
   - CSS consuming `--drag-y`;
   - definition/import of `animateTo`;
   - how `currentY` is updated;
   - list size and render path.
2. On pointer down, record:
   - active `pointerId`;
   - queue/container bounding rect;
   - item starting presentation Y;
   - grab offset between pointer and item origin;
   - recent `{time, y}` samples.
   Call `setPointerCapture(pointerId)` if not already present.
3. On pointer move:
   - ignore non-active pointers;
   - compute local pointer Y, not raw viewport `clientY`;
   - subtract grab offset;
   - write a transform-owned value, for example `--drag-y: <localY>px`;
   - update velocity samples without React state on every frame.
4. On pointer up/cancel:
   - release pointer capture when held;
   - compute velocity in CSS px/s from recent samples;
   - compute a projected endpoint and choose `nearestSlot(projectedEndpoint)`;
   - start settle from the current presentation value.
5. Replace fixed `400ms` settle:
   - if `animateTo` supports spring/velocity: use critically damped or near-critically damped settle with supplied velocity and no decorative bounce;
   - if it only supports duration/easing: use `var(--duration-panel)`/`240ms` as the initial cap and document that true velocity handoff requires the existing primitive to support it.
6. Ensure transform ownership is explicit if press feedback and drag both use `transform`; use wrapper layers or a composed transform so one does not overwrite the other.
7. Add Reduced Motion handling:
   - direct drag remains 1:1;
   - release snap is instant or `80ms`;
   - no overshoot, elastic travel, or long glide.

**Hard boundaries**

- Do not rewrite queue ordering data structures unless the current drag state requires it.
- Do not add a new animation package unless the existing primitive cannot read current value or accept velocity and the team approves the dependency.
- Do not move sorting, persistence, or revenue/support workflow logic.
- Do not use React state for every pointer-move frame unless the current architecture already proves it is cheap.

**Mechanical checks**

- Run TypeScript check covering `SortableQueue.tsx`.
- Run lint for pointer event typing and hook dependency correctness.
- Run existing unit/component tests for queue ordering if present.
- Search for all `--drag-y` consumers and confirm transform ownership is clear.

**Runtime/feel checks to perform later**

- Grab item near top, center, and bottom; verify no jump.
- Drag outside queue bounds; verify tracking continues until release/cancel.
- Release slowly near a boundary and quickly with a flick; verify projected slot selection feels causal.
- Interrupt a settling item by grabbing again; verify no visual jump.
- Test with keyboard reorder path if one exists; it must remain usable.

**Reduced Motion behavior**

- Drag still directly follows pointer.
- Snap has no overshoot and uses instant or very short settle.
- Static slot highlight or clear final placement preserves feedback.

**Source-drift stop condition**

Stop before editing if `animateTo` already handles current-value interruption and velocity under a different API, if `--drag-y` is intentionally viewport-based in CSS, if pointer capture/grab offset already exists outside the excerpt, or if the queue is virtualized in a way that changes coordinate ownership.

## 4. Recommended execution order

1. **Plan A** first: fixes high-frequency keyboard overlay and common popover vocabulary while reinforcing tokens.
2. **Plan B** second: small, isolated, high-confidence conversion from layout motion to transform/opacity.
3. **Plan C** third: highest interaction complexity; requires full-source inspection and runtime feel validation.

## Explicitly unverified states

- Actual rendered smoothness, frame rate, compositing, and layout cost.
- Whether popovers are anchored or centered in real usage.
- Whether `palette` keyframes exist elsewhere and what properties they animate.
- Whether command palette remains input-ready during animation.
- Whether toast stacking uses `top` dynamically.
- Whether `SortableQueue` already implements pointer capture, grab offset, velocity, cancellation, or keyboard reordering outside the excerpt.
- Actual Reduced Motion behavior in browser settings.
- Accessibility-tree behavior, focus order, screen-reader announcement timing, and live-region behavior.
