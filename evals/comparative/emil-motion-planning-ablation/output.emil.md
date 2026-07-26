## 1. Recon summary

- **Stack signals:** React/TSX components, plain CSS, CSS custom properties, utility-class animation syntax, and an imperative pointer/animation path for drag sorting.
- **Where motion lives:**  
  - Global motion tokens: `src/styles/motion.css`  
  - Component CSS/keyframes: `src/components/toast.css`, `src/components/Button.css`  
  - Inline utility animation: `src/components/CommandPalette.tsx`  
  - Imperative gesture handling: `src/components/SortableQueue.tsx`
- **Existing conventions:**  
  - Durations: `--duration-fast: 160ms`, `--duration-panel: 240ms`  
  - Primary responsive curve: `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`  
  - Correct local precedent: button press uses `transform`, tokenized timing/easing, and a reduced-motion override that preserves feedback.
- **Product personality:** calm, crisp, high-throughput desktop operations UI. Motion should clarify cause/effect and state continuity, not add delay or decoration.
- **Frequency map:**  
  - Very high: `CommandPalette` for keyboard-heavy operators.  
  - High/dynamic: `SortableQueue` drag/reorder.  
  - Medium: `.popover` interactions.  
  - Occasional: `.toast` notifications.  
  - Local precedent: `.button:active` likely frequent and currently aligned.
- **Evidence level:** static snippet audit only. No runtime timing, computed style, device, trace, screen recording, accessibility-tree, or user validation was performed.

---

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose, frequency, duration | `src/components/CommandPalette.tsx` | High-frequency keyboard surface uses `animate-[palette_420ms_ease-in_both]`. Static evidence shows a slow `ease-in` animation on a command surface operators may invoke repeatedly. | Remove the open/close animation or reduce to non-spatial instant/near-instant feedback. Do not delay search availability. |
| 2 | HIGH | Easing, performance, cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This bypasses existing tokens, animates unintended properties, exceeds the small-popover budget, and starts slowly. | Restrict to `transform, opacity`; use existing duration/easing tokens; add reduced-motion override. |
| 3 | MEDIUM | Physicality, causality | `src/styles/motion.css` | `.popover { transform-origin: center; }` is suspicious for trigger-anchored popovers. Static evidence cannot confirm trigger geometry, but the class name indicates anchored UI rather than a centered modal. | Prefer a trigger-origin variable when available; keep a safe fallback only if no origin source exists. |
| 4 | HIGH | Performance, accessibility | `src/components/toast.css` | Toast enters by animating `top` from `-24px` to `0` over `500ms ease-in`. This is layout-affecting, slow for UI feedback, and has no shown reduced-motion path. | Replace `top` animation with `transform: translateY(...)` + opacity, tokenized timing, and reduced-motion opacity-only feedback. |
| 5 | HIGH | Gesture, interruptibility | `src/components/SortableQueue.tsx` | Drag path writes `--drag-y` during pointer move and settles with `animateTo(..., { duration: 400 })`. Static evidence shows fixed-duration settling rather than velocity-aware direct manipulation. | Drive the dragged item with direct `transform` updates; settle with existing spring/velocity support if present; avoid fixed 400ms tween. |
| 6 | MEDIUM | Accessibility, cohesion | Multiple snippets | Only the button excerpt shows `prefers-reduced-motion`. Palette, popover, toast, and queue snippets do not show reduced-motion behavior. | Add per-component reduced-motion branches that preserve opacity/focus/state feedback while dropping or shortening spatial movement. |

---

## 3. Implementation-ready plans

### Plan 1 — Make popover motion tokenized, specific, and reduced-motion aware

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

**Target behavior**

- Popovers feel immediate and crisp.
- Only `transform` and `opacity` transition.
- Duration uses existing tokens.
- Easing uses the existing responsive curve.
- Reduced Motion keeps feedback but removes/shortens spatial motion.

**Project conventions to preserve**

```css
/* src/components/Button.css - existing correct local precedent */
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

**Ordered steps**

1. In `src/styles/motion.css`, replace the `.popover` rule with:

   ```css
   .popover {
     transform-origin: var(--popover-transform-origin, center);
     transition:
       transform var(--duration-fast) var(--ease-responsive),
       opacity var(--duration-fast) var(--ease-responsive);
   }

   @media (prefers-reduced-motion: reduce) {
     .popover {
       transition:
         opacity 80ms var(--ease-responsive);
     }
   }
   ```

2. If the project already exposes a popover trigger-origin custom property, use that existing property name instead of `--popover-transform-origin`.

3. Do not invent geometry math from the CSS file alone. If no trigger-origin source exists in the actual popover implementation, keep the fallback and report the missing origin hook separately.

**Hard boundaries**

- Do not change popover markup, positioning, focus behavior, or portal behavior.
- Do not add dependencies.
- Do not use `transition: all`.
- Do not introduce a second easing system when `--ease-responsive` already exists.

**Mechanical checks**

- Confirm `src/styles/motion.css` no longer contains `.popover { ... transition: all ... }`.
- Confirm `.popover` transition properties are only `transform` and `opacity` in normal motion.
- Confirm a `prefers-reduced-motion: reduce` override exists for `.popover`.
- Run the existing frontend lint/type/build checks if available; do not add scripts.

**Runtime/feel checks for executor**

- Open and close a popover repeatedly.
- At slow playback, confirm the popover does not start sluggishly.
- If trigger-origin support exists, confirm it appears to originate from the trigger, not the screen center.
- Toggle Reduced Motion and confirm spatial movement is removed or greatly reduced while opacity/state feedback remains.

**Reduced Motion behavior**

- Normal: transform + opacity over `var(--duration-fast)`.
- Reduced: opacity-only over `80ms`.

**Source-drift stop condition**

- Stop if `.popover` no longer exists, if motion tokens were renamed, or if the popover implementation already defines a different trigger-origin contract. Report the new current excerpt instead of improvising.

---

### Plan 2 — Remove slow command-palette animation from the high-frequency keyboard path

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

- Opening the command palette does not wait on decorative motion.
- Search results and focus behavior are available immediately.
- The `open` state remains visible through existing rendering/state logic.
- Reduced Motion path is naturally identical because the high-frequency animation is removed.

**Project conventions to preserve**

- Keep semantic state via `data-open={open}`.
- Follow the product requirement for crisp motion and visible focus.
- Do not replace this with another long animation or custom curve.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class:

   ```tsx
   export function CommandPalette({ open }: { open: boolean }) {
     return (
       <div data-open={open}>
         <SearchResults />
       </div>
     );
   }
   ```

2. If other non-motion classes exist in the real file, preserve them and remove only `animate-[palette_420ms_ease-in_both]`.

3. Search for the `palette` keyframes or equivalent animation definition. If it is now unused, remove only that unused keyframe definition.

4. Do not add a replacement entrance animation unless product/design explicitly reclassifies this as an occasional surface rather than a high-frequency keyboard tool.

**Hard boundaries**

- Do not change command search behavior, result ordering, focus management, keyboard shortcuts, or open/close state ownership.
- Do not add transitions to child result rows as compensation.
- Do not remove `data-open={open}` unless the full component proves it is unused and tests cover the change.

**Mechanical checks**

- Confirm `CommandPalette.tsx` no longer contains `420ms`, `ease-in`, or `animate-[palette`.
- Confirm no remaining command-palette open animation exceeds `80ms`.
- Confirm TypeScript/JSX still compiles.
- Run existing frontend lint/type/build checks if available; do not add scripts.

**Runtime/feel checks for executor**

- Invoke the command palette repeatedly by keyboard.
- Confirm the palette is ready for typing immediately.
- Confirm no delayed search-result reveal blocks task throughput.
- Toggle Reduced Motion and confirm behavior is still immediate and state feedback remains clear.

**Reduced Motion behavior**

- Same as normal: no spatial command-palette animation.
- Preserve focus ring, selected result state, and open/closed state indicators.

**Source-drift stop condition**

- Stop if the class no longer exists, if the animation class also carries required visibility styles through a generated system, or if the palette is now unmounted/remounted by a different component. Report the current open/close mechanism before changing behavior.

---

### Plan 3 — Replace layout/fixed-duration dynamic movement with transform-based, interruptible motion

**Current excerpts**

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

- Toast entry uses compositor-friendly `transform` + `opacity`, not `top`.
- Toast timing is short and tokenized.
- Dragging updates the actual moving item with direct transform writes, not a parent CSS variable that may invalidate a wider subtree.
- Reorder settle uses velocity-aware spring behavior if the existing animation utility supports it; otherwise stop and flag the utility gap.
- Reduced Motion keeps opacity/state feedback and avoids spatial movement.

**Project conventions to preserve**

```css
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

**Ordered steps**

1. In `src/components/toast.css`, replace the `top` keyframe with transform/opacity entry:

   ```css
   @keyframes toast-enter {
     from {
       transform: translateY(-24px);
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

2. If the project supports `@starting-style` for mounted toast entry, prefer a transition version:

   ```css
   .toast {
     transform: translateY(0);
     opacity: 1;
     transition:
       transform var(--duration-panel) var(--ease-responsive),
       opacity var(--duration-panel) var(--ease-responsive);
   }

   @starting-style {
     .toast {
       transform: translateY(-24px);
       opacity: 0;
     }
   }

   @media (prefers-reduced-motion: reduce) {
     .toast {
       transform: none;
       transition: opacity 80ms var(--ease-responsive);
     }

     @starting-style {
       .toast {
         opacity: 0;
       }
     }
   }
   ```

   Use this transition version only if browser support/fallback policy is already acceptable for the project.

3. In `src/components/SortableQueue.tsx`, change the drag move path so the dragged item receives a direct transform update. The final code should follow this shape, adapted to the actual dragged element ref:

   ```tsx
   function onPointerMove(event: PointerEvent) {
     draggedItemRef.current?.style.setProperty(
       "transform",
       `translate3d(0, ${event.clientY}px, 0)`
     );
   }
   ```

   If the real code stores deltas rather than absolute viewport coordinates, use the existing delta value instead of `event.clientY`.

4. Replace the fixed `400` settle duration with the existing project’s spring/velocity option if `animateTo` supports one. Target shape:

   ```tsx
   function onPointerUp() {
     setDragging(false);
     animateTo(nearestSlot(currentY), {
       type: "spring",
       duration: 0.5,
       bounce: 0.2,
       velocity: currentVelocity,
     });
   }
   ```

5. If `animateTo` does not support spring or velocity, do not invent a new animation system in this change. Stop and report that the queue needs an animation utility decision.

**Hard boundaries**

- Do not change queue ordering rules, nearest-slot calculation, selection state, or persistence behavior.
- Do not add a new animation dependency.
- Do not animate `top`, `left`, `width`, `height`, margin, or padding.
- Do not keep the fixed `duration: 400` settle for drag release.
- Do not claim velocity support unless the actual `animateTo` API supports it.

**Mechanical checks**

- Confirm `toast.css` no longer animates `top`.
- Confirm toast normal motion is `transform` + `opacity`.
- Confirm toast has a `prefers-reduced-motion` branch.
- Confirm `SortableQueue.tsx` no longer drives drag position only through `queueRef.current?.style.setProperty("--drag-y", ...)`.
- Confirm no fixed `{ duration: 400 }` remains in queue release motion.
- Run existing frontend lint/type/build checks if available; do not add scripts.

**Runtime/feel checks for executor**

- Trigger multiple toasts and confirm entry is quick, not sluggish.
- In slow playback, confirm toast movement is vertical transform, not layout jump.
- Drag a queue item, reverse direction mid-drag, and confirm motion follows the pointer without lag.
- Release with small and larger velocity; confirm settle feels connected rather than a fixed-time glide.
- Toggle Reduced Motion and confirm toast uses opacity-only feedback and queue drag remains direct while nonessential settle movement is reduced.

**Reduced Motion behavior**

- Toast: opacity-only, `80ms`.
- Queue: direct pointer tracking remains because it is input feedback; nonessential release animation should be shortened or simplified. If a spring branch exists, use lower/no bounce and shorter travel feedback.

**Source-drift stop condition**

- Stop if toast styling moved, if `toast-enter` no longer exists, if `queueRef` is not involved in drag positioning, or if `animateTo` has a different API than shown. Report the new excerpts before changing behavior.

---

## 4. Recommended execution order

1. **Plan 2 — Command palette:** highest throughput impact; removes delay from a frequent keyboard path with minimal scope.
2. **Plan 1 — Popover:** fixes broad token/easing/performance debt likely shared by many small interactions.
3. **Plan 3 — Toast and sortable queue:** addresses performance and direct-manipulation quality; queue work may require checking the existing animation utility before implementation.

## Explicitly unverified states

- Actual command-palette mount/unmount behavior, focus timing, and whether the animation class also affects visibility.
- The definition of `palette` keyframes.
- Whether `.popover` is trigger-anchored, modal-like, library-backed, or manually positioned.
- Whether a trigger-origin custom property already exists.
- Toast stacking, dismissal, interrupt behavior, and DOM structure.
- Whether `--drag-y` is consumed by one element or a larger subtree.
- The `animateTo` API, spring support, and velocity availability.
- Existing package scripts, CI gates, browser support policy, and computed Reduced Motion behavior.
