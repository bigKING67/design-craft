## 1. Recon summary

- **Stack signals**: React/TSX components with CSS modules/global CSS and utility-style animation classes. No confirmed motion library from the snippets.
- **Where motion lives**:
  - Global semantic motion tokens: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility animation: `src/components/CommandPalette.tsx`
  - Gesture JS: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Tokens already exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct precedent exists in `Button.css`: transform-only transition, semantic duration/easing, Reduced Motion shortened to `80ms`.
- **Product personality**: calm desktop operations console; motion should be crisp, causal, low-latency, and non-decorative.
- **Frequency map**:
  - Very high: command palette, keyboard-driven actions, sortable queue drag.
  - Medium: popovers, buttons.
  - Occasional: toasts.
- **Evidence level**: static snippet audit only. No runtime timing, computed styles, browser behavior, accessibility tree, FPS, pointer-device, or user testing was performed.

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`. For a keyboard-heavy, high-frequency surface, a 420ms ease-in entrance risks making a primary workflow feel delayed. | Remove the entrance animation from the command palette; keep open/close causality immediate. |
| 2 | HIGH | Performance / easing | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This animates unintended properties, exceeds the existing fast/panel token scale, and uses slow-start easing. | Limit to `transform, opacity`; use existing duration/easing tokens; add Reduced Motion duration. |
| 3 | HIGH | Performance / interruptibility | `src/components/toast.css` | Toast enters by animating `top` over `500ms ease-in` via keyframes. `top` is layout-affecting, duration is long for operations feedback, and ease-in delays visibility. | Replace layout animation with transform/opacity using existing tokens; provide Reduced Motion opacity-only feedback. |
| 4 | HIGH | Gesture / direct manipulation | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` to the queue parent; release uses fixed `duration: 400`. Static evidence suggests drag motion may be parent-style driven and release is not velocity-aware. | Drive only the active dragged element with `transform`; settle with interruptible/velocity-aware behavior or stop if `animateTo` cannot support it. |
| 5 | MEDIUM | Accessibility | Multiple snippets | Reduced Motion is shown only in the correct button precedent. Command palette, popover, toast, and sortable release snippets do not show a Reduced Motion branch. | Apply the button precedent: preserve feedback, shorten or remove movement, avoid deleting all state feedback. |
| 6 | MEDIUM | Cohesion / tokens | Multiple snippets | Motion values are split between semantic tokens and hard-coded `360ms`, `420ms`, `500ms`, `ease-in`. | Consolidate frequent UI motion around existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`. |

---

## 3. Implementation plans

### Plan 1 — Remove command palette entrance latency

**Current excerpt**

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

- Opening the command palette should feel immediate for keyboard-heavy repeated use.
- Do not add a replacement entrance animation.
- Preserve `data-open={open}` because it may be used by existing visibility/focus styles outside the snippet.
- Reduced Motion behavior is the same as default: no positional/entrance animation.

**Project conventions to follow**

- Existing correct precedent: `src/components/Button.css` uses semantic motion tokens and keeps Reduced Motion feedback short.
- For this specific high-frequency command surface, prefer no animation over tokenized animation.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove only the arbitrary animation class:
   ```tsx
   <div data-open={open}>
     <SearchResults />
   </div>
   ```
2. If the real file contains additional non-motion classes, keep them and remove only:
   ```tsx
   animate-[palette_420ms_ease-in_both]
   ```
3. Do not add new CSS for palette entrance/exit unless the existing file already has non-motion visibility styles requiring a class hook.

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change command filtering, focus management, keyboard shortcuts, or open-state ownership.
- Do not add dependencies.
- Do not replace this with a shorter animation; the target is immediate command access.

**Mechanical checks**

- Run, if available in the project:
  ```bash
  npm run typecheck
  npm run lint
  npm run build
  ```
- Expected: no TSX syntax errors and no unused-import changes caused by the edit.

**Runtime / feel checks to perform later**

- Open the command palette repeatedly via keyboard.
- Confirm the palette appears without a slow-start visual delay.
- Confirm focus still lands where it did before.
- Confirm closing/reopening quickly does not replay an entrance animation.
- Toggle Reduced Motion and confirm behavior remains immediate.

**Reduced Motion behavior**

- No separate branch required if the animation is fully removed.
- Do not remove visible focus or open-state indication.

**Source-drift stop condition**

- Stop if `CommandPalette.tsx` no longer contains `animate-[palette_420ms_ease-in_both]`.
- Stop if the animation is now managed by a separate transition component or motion library not shown in the snippet.

---

### Plan 2 — Tokenize CSS entrances and remove layout/all-property animation

**Current excerpts**

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

- Popovers: animate only `transform` and `opacity`, using existing semantic tokens.
- Toasts: enter with compositor-friendly `transform` and `opacity`, not `top`.
- Use crisp existing timing: `--duration-fast` for small anchored UI, `--duration-panel` for toast feedback.
- Reduced Motion: preserve opacity feedback, remove positional movement, shorten to `80ms`.

**Project conventions to follow**

Use the local precedent:

```css
/* src/components/Button.css */
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` with:
   ```css
   .popover {
     transform-origin: var(--radix-popover-content-transform-origin, var(--transform-origin, center));
     transition:
       transform var(--duration-fast) var(--ease-responsive),
       opacity var(--duration-fast) var(--ease-responsive);
   }

   @media (prefers-reduced-motion: reduce) {
     .popover {
       transition-duration: 80ms;
     }
   }
   ```
2. If this `.popover` is actually used for centered modal content rather than trigger-anchored popovers, keep `transform-origin: center` and still replace `transition: all 360ms ease-in`.
3. In `src/components/toast.css`, replace layout keyframes with transform/opacity:
   ```css
   @keyframes toast-enter {
     from {
       transform: translateY(-8px);
       opacity: 0;
     }
     to {
       transform: translateY(0);
       opacity: 1;
     }
   }

   .toast {
     animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
   }

   @media (prefers-reduced-motion: reduce) {
     @keyframes toast-enter {
       from { opacity: 0; }
       to { opacity: 1; }
     }

     .toast {
       animation-duration: 80ms;
     }
   }
   ```
4. If redefining `@keyframes toast-enter` inside the media query conflicts with the project’s CSS tooling, instead create:
   ```css
   @keyframes toast-enter-reduced {
     from { opacity: 0; }
     to { opacity: 1; }
   }

   @media (prefers-reduced-motion: reduce) {
     .toast {
       animation-name: toast-enter-reduced;
       animation-duration: 80ms;
     }
   }
   ```

**Hard boundaries**

- Do not change toast markup, stacking logic, dismissal timing, or live-region behavior.
- Do not add new duration/easing tokens unless existing tokens are unavailable in the actual cascade.
- Do not animate `top`, `left`, `width`, `height`, `margin`, or `padding`.
- Do not use `transition: all`.

**Mechanical checks**

- Run, if available:
  ```bash
  npm run lint
  npm run build
  ```
- Search check after editing:
  ```bash
  grep -R "transition: all 360ms ease-in\|top: -24px\|500ms ease-in" src
  ```
- Expected: no remaining instances of the replaced excerpts unless unrelated and intentionally left.

**Runtime / feel checks to perform later**

- Trigger a popover and confirm it does not animate unrelated properties.
- If the popover is trigger-anchored, confirm slow-motion playback appears to originate from the trigger side, not arbitrarily from the center.
- Trigger a toast and confirm it slides a small distance while fading in, without pushing layout.
- Trigger multiple toasts quickly and confirm no obvious jump caused by `top` animation.
- Toggle Reduced Motion and confirm toast movement is removed but opacity feedback remains.

**Reduced Motion behavior**

- Popover: same properties, shortened to `80ms`.
- Toast: opacity-only, `80ms`, no vertical translation.

**Source-drift stop condition**

- Stop if `.popover` has moved to component-scoped styles not represented by `src/styles/motion.css`.
- Stop if `.toast` is no longer CSS-keyframe based or toast positioning is now controlled by a motion/transition component.

---

### Plan 3 — Make sortable drag direct, transform-only, and release-aware

**Current excerpt**

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

- During drag, only the active dragged item moves.
- Movement should be written as `transform: translate3d(...)`, not as a parent CSS variable that may invalidate descendants.
- Release should settle to `nearestSlot(currentY)` with responsive timing and interruption support.
- If the existing `animateTo` helper supports spring/velocity options, use them. If not, use the existing helper with shorter token-aligned duration and stop for a follow-up refactor rather than inventing a new animation engine.
- Reduced Motion should avoid long glide motion while preserving final placement feedback.

**Project conventions to follow**

- Existing motion precedent favors transform-only updates and semantic timing.
- Existing token values to align with:
  ```css
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
  ```

**Ordered steps**

1. Locate the actual dragged item ref in `src/components/SortableQueue.tsx`.
   - If only `queueRef` exists and there is no active item element ref, add an explicit `draggedItemRef` to the element that visually follows the pointer.
2. Replace parent CSS-variable movement:
   ```tsx
   queueRef.current?.style.setProperty("--drag-y", `${event.clientY}px`);
   ```
   with a direct transform on the dragged element:
   ```tsx
   draggedItemRef.current!.style.transform = `translate3d(0, ${event.clientY}px, 0)`;
   ```
3. If the component already tracks a drag origin, use delta instead of absolute viewport Y:
   ```tsx
   const nextY = event.clientY - dragStartYRef.current;
   draggedItemRef.current!.style.transform = `translate3d(0, ${nextY}px, 0)`;
   ```
4. Track last pointer sample for release velocity:
   ```tsx
   lastPointerSampleRef.current = { y: event.clientY, time: performance.now() };
   ```
   Update velocity from the previous sample before overwriting it.
5. Replace fixed release duration:
   ```tsx
   animateTo(nearestSlot(currentY), { duration: 400 });
   ```
   with the best supported option:
   ```tsx
   animateTo(nearestSlot(currentY), {
     type: "spring",
     duration: 0.5,
     bounce: 0.2,
     velocity: releaseVelocityYRef.current
   });
   ```
6. If `animateTo` does not support spring options, use:
   ```tsx
   animateTo(nearestSlot(currentY), {
     duration: 240,
     easing: "cubic-bezier(0.23, 1, 0.32, 1)"
   });
   ```
   and create no new animation abstraction in this pass.
7. Add or reuse a Reduced Motion check. If the project has no hook/helper, use `window.matchMedia("(prefers-reduced-motion: reduce)").matches` at the interaction boundary:
   ```tsx
   const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
   ```
   Then release with:
   ```tsx
   animateTo(nearestSlot(currentY), { duration: 80 });
   ```

**Hard boundaries**

- Do not change queue ordering rules.
- Do not change pointer capture, selection, keyboard reordering, or persistence behavior.
- Do not add a new motion dependency.
- Do not move every child on pointer move.
- Do not implement physics if `animateTo` cannot support interruption or velocity; stop and report that helper capability is the blocker.

**Mechanical checks**

- Run, if available:
  ```bash
  npm run typecheck
  npm run lint
  npm run build
  ```
- Search check after editing:
  ```bash
  grep -R "setProperty(\"--drag-y\"" src/components/SortableQueue.tsx
  ```
- Expected: no parent `--drag-y` pointer-move write remains in this component.

**Runtime / feel checks to perform later**

- Drag an item slowly and confirm it stays directly under the pointer.
- Drag quickly and release; confirm the item settles toward the nearest slot without a fixed-feeling 400ms glide.
- Interrupt by starting a second drag quickly after release; confirm motion does not visibly restart from zero.
- Use performance tools while dragging and confirm no broad child style recalculation is caused by parent CSS-variable updates.
- Toggle Reduced Motion and confirm release movement is shortened while final placement remains clear.

**Reduced Motion behavior**

- Pointer following remains direct because it is user-controlled.
- Release animation shortens to `80ms` or snaps to final transform if that is the project’s existing Reduced Motion convention.
- Do not remove focus, selection, or placement feedback.

**Source-drift stop condition**

- Stop if `SortableQueue.tsx` no longer contains `setProperty("--drag-y"` or `animateTo(nearestSlot(currentY), { duration: 400 })`.
- Stop if `animateTo` is imported from an external helper whose options are unknown and cannot be confirmed from source.

---

## 4. Recommended execution order

1. **Plan 1 — Command palette**: highest workflow impact, smallest safe change.
2. **Plan 2 — CSS entrances**: removes `transition: all`, layout animation, hard-coded slow values, and missing Reduced Motion paths.
3. **Plan 3 — Sortable queue**: highest interaction complexity; execute after confirming `animateTo` capabilities.

## Explicitly unverified states

- Actual rendered appearance, frame rate, interruption behavior, and computed styles.
- Whether `.popover` is always trigger-anchored or sometimes used like a centered modal.
- Whether command palette visibility/focus is controlled elsewhere.
- Whether toast stacking/dismissal logic exists outside `toast.css`.
- Whether `animateTo` supports spring, velocity, cancellation, or Reduced Motion options.
- Package manager and exact available validation scripts.
- Browser support targets for any CSS feature choices.
