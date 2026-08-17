## 1) Recon summary

- **Stack signals:** React/TSX components, plain CSS, CSS custom-property motion tokens, one Tailwind-style arbitrary animation class, and a custom/unknown `animateTo(...)` helper. No runtime motion library is proven from the excerpts.
- **Where motion lives:**  
  `src/styles/motion.css` global tokens and `.popover`; `src/components/CommandPalette.tsx` inline utility animation; `src/components/toast.css` keyframes; `src/components/SortableQueue.tsx` pointer-driven JS animation; `src/components/Button.css` local precedent.
- **Existing conventions:** semantic duration/easing tokens already exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`. Button precedent correctly uses transform-only feedback and a Reduced Motion duration.
- **Product personality:** calm, crisp, workday operations console. Motion should be fast, causal, low-drama, and should not tax keyboard-heavy throughput.
- **Frequency map from context/snippets:**  
  High: command palette, queue sorting/dragging.  
  Medium: popovers.  
  Occasional: toasts.  
  Baseline precedent: buttons.
- **Evidence level:** static code excerpts only. No line numbers, computed styles, runtime mount behavior, frame timing, accessibility tree, screen recording, or user/device validation available.

---

## 2) Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose, frequency, easing | `src/components/CommandPalette.tsx` | Keyboard-heavy command palette uses `palette_420ms_ease-in_both`; this is long, slow-starting, and high-frequency. | Remove entrance motion or reduce to non-spatial feedback only; preserve instant keyboard throughput. |
| 2 | HIGH | Performance, easing, physicality | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`; broad property animation and slow-start easing conflict with crisp UI. | Transition only `transform, opacity`; use existing tokens; use trigger-derived origin when available. |
| 3 | HIGH | Performance, accessibility | `src/components/toast.css` | Toast animates `top` from `-24px` for `500ms ease-in`; layout property, long duration, slow start, no shown Reduced Motion path. | Animate `transform` + `opacity`, shorten to token duration, add reduced-motion fade/short duration. |
| 4 | MED-HIGH | Gesture performance, interruptibility | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` on `queueRef`; release uses fixed `duration: 400`. Static evidence cannot prove scope, but this risks broad style recalculation and sluggish settling. | Move only the dragged item with direct transform; shorten/retarget settle; add reduced-motion snap behavior. |
| 5 | MEDIUM | Cohesion, accessibility | Multiple excerpts | Hard-coded `360ms`, `420ms`, `500ms`, `400` and `ease-in` diverge from existing tokens; Reduced Motion appears only in the button precedent. | Consolidate to semantic tokens and add Reduced Motion branches where movement remains. |

---

## 3) Implementation plans

### Plan 1 — Make overlay motion tokenized and throughput-safe

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

- Command palette opens/closes without spatial animation by default; keyboard invocation should feel immediate.
- If a visual state cue is required by surrounding styles, use opacity-only feedback no longer than `80ms`; do not use transform movement.
- Popovers use only `transform` and `opacity`, no `transition: all`, no `ease-in`, and no duration above the existing token budget.
- Trigger-anchored popovers should scale from the trigger-origin custom property if the component system emits one; otherwise keep a safe fallback.

**Project conventions**

- Use existing tokens from `src/styles/motion.css`: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Follow the button precedent: transform-only feedback, `var(--duration-fast)`, `var(--ease-responsive)`, and a Reduced Motion duration.

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

2. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class:

   ```tsx
   export function CommandPalette({ open }: { open: boolean }) {
     return (
       <div data-open={open}>
         <SearchResults />
       </div>
     );
   }
   ```

3. Search for `@keyframes palette`. If the keyframe is now unused, delete only that unused keyframe. If it is shared by other components, do not modify it in this plan.
4. Do not add new easing tokens unless another existing file already defines a semantic overlay token.

**Hard boundaries**

- Do not change command search behavior, focus management, result rendering, or mount/unmount logic.
- Do not add dependencies.
- Do not convert the command palette to a new animation library.
- If `.popover` is also used for centered modal content, stop and split the selector before changing transform origin.

**Mechanical checks**

- Confirm no `transition: all 360ms ease-in` remains in `src/styles/motion.css`.
- Confirm no `animate-[palette_420ms_ease-in_both]` remains in `src/components/CommandPalette.tsx`.
- Run the project’s existing typecheck/lint/build gates if present; exact script names are not available from the provided evidence.

**Runtime / feel checks for executor**

- Open the command palette repeatedly via keyboard: it should appear immediately, with no delayed ease-in feel.
- Open a popover slowly in animation tooling: only opacity/transform should animate.
- If trigger-origin variables are present, the popover should originate from the trigger rather than blooming from the center.

**Reduced Motion behavior**

- Command palette remains non-spatial and immediate.
- Popover keeps brief feedback at `80ms`; movement is minimized and feedback is preserved.

**Source-drift stop condition**

- Stop if either excerpt no longer matches materially, if the command palette class also contains non-motion styling, or if `.popover` is not the component class for trigger-anchored popovers.

---

### Plan 2 — Move toast entrance to compositor-safe feedback

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

- Toast entrance is short, crisp, and calm.
- Position is established by static layout, not animated `top`.
- Entrance uses `transform` and `opacity` only.
- Reduced Motion keeps opacity feedback while removing vertical travel.

**Project conventions**

- Reuse `--duration-panel: 240ms` for this occasional UI entrance.
- Reuse `--ease-responsive` for responsive entry.
- Mirror button precedent by shortening duration under `prefers-reduced-motion`.

**Ordered steps**

1. Replace the keyframe with transform/opacity movement:

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
   ```

2. Update `.toast` so the final position is static and the animation is tokenized:

   ```css
   .toast {
     top: 0;
     animation: toast-enter var(--duration-panel) var(--ease-responsive) both;
   }
   ```

3. Add a reduced-motion keyframe and media query:

   ```css
   @keyframes toast-enter-reduced {
     from { opacity: 0; }
     to { opacity: 1; }
   }

   @media (prefers-reduced-motion: reduce) {
     .toast {
       animation-name: toast-enter-reduced;
       animation-duration: 120ms;
     }
   }
   ```

**Hard boundaries**

- Do not alter toast content, stacking logic, dismissal timing, ARIA/live-region behavior, or z-index.
- Do not introduce blur, bounce, or decorative stagger.
- Do not change the toast’s final layout position except making `top: 0` explicit if the current keyframe was providing it.

**Mechanical checks**

- Confirm `top: -24px` no longer appears in `src/components/toast.css`.
- Confirm `animation: toast-enter 500ms ease-in forwards` no longer appears.
- Confirm a `prefers-reduced-motion: reduce` block exists in `src/components/toast.css`.
- Run existing project CSS/type/build gates if present; exact commands are not available from the evidence.

**Runtime / feel checks for executor**

- Trigger one toast: it should enter quickly without feeling delayed at the start.
- Trigger multiple toasts if supported: no layout-position animation should be visible.
- In slow playback, confirm the toast translates subtly from `-8px` to `0`, not from `top: -24px`.

**Reduced Motion behavior**

- Toast fades in over `120ms`.
- No vertical travel in Reduced Motion.

**Source-drift stop condition**

- Stop if toast positioning is no longer controlled by `top`, if the class name changed, or if a separate toast animation system already replaced this CSS.

---

### Plan 3 — Make sortable queue dragging direct, shorter, and interruptible

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

- During drag, only the actively dragged item moves.
- Drag movement is direct and pointer-causal, using `transform: translate3d(...)`.
- Release settle is shorter than the current `400ms`, retargetable/cancelable if the user starts another drag.
- Reduced Motion preserves drag feedback but shortens automated settling.

**Project conventions**

- Use transform-only movement, consistent with the existing button precedent.
- Use the existing responsive easing value: `cubic-bezier(0.23, 1, 0.32, 1)`.
- Prefer existing local helpers over new dependencies.

**Ordered steps**

1. Inspect the component to identify the element representing the actively dragged queue item.
2. If `queueRef` points to the whole list/container, stop using it for per-frame drag motion. Add or reuse a ref for only the dragged item.
3. Track drag start and current offset as relative movement, not absolute viewport `clientY`:

   ```tsx
   const dragStartYRef = useRef(0);
   const currentYRef = useRef(0);
   ```

4. On pointer down/start, set `dragStartYRef.current` to the starting `clientY`.
5. Replace the pointer-move write with direct transform on the dragged item:

   ```tsx
   function onPointerMove(event: PointerEvent) {
     const y = event.clientY - dragStartYRef.current;
     currentYRef.current = y;

     if (draggedItemRef.current) {
       draggedItemRef.current.style.transform = `translate3d(0, ${y}px, 0)`;
     }
   }
   ```

6. Update pointer release to use the tracked offset and a shorter settle:

   ```tsx
   function onPointerUp() {
     setDragging(false);

     const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
     const duration = prefersReducedMotion ? 80 : 220;

     animateTo(nearestSlot(currentYRef.current), {
       duration,
       easing: "cubic-bezier(0.23, 1, 0.32, 1)",
     });
   }
   ```

7. Before starting a new settle animation, cancel or retarget any in-flight settle if the existing `animateTo` helper supports it. If it does not, do not invent a new animation engine in this plan; shorten the duration and document the limitation.

**Hard boundaries**

- Do not change queue ordering rules, slot calculation, persistence, keyboard controls, or data model.
- Do not add a new gesture or animation dependency.
- Do not animate layout properties such as `top`, `left`, `height`, or `margin`.
- Do not apply the drag transform to the whole queue unless the excerpt proves `queueRef` is actually the dragged item.

**Mechanical checks**

- Confirm `setProperty("--drag-y"` no longer appears in `src/components/SortableQueue.tsx`.
- Confirm the release settle no longer uses `{ duration: 400 }`.
- Confirm the drag path writes `transform` to the dragged item only.
- Run existing TypeScript/lint/build gates if present; exact scripts are not available from the provided evidence.

**Runtime / feel checks for executor**

- Drag an item slowly: the item should track the pointer directly with no visible lag from the rest of the list.
- Release near a slot: settle should feel crisp, not languid.
- Start another drag during or immediately after settle: if the helper supports cancellation, motion should retarget instead of fighting the pointer.
- In slow playback, confirm only transform changes during drag/settle.

**Reduced Motion behavior**

- Direct manipulation remains: the item still follows the pointer.
- Automated settle is shortened to `80ms`; no bounce or decorative movement is added.

**Source-drift stop condition**

- Stop if `animateTo` does not accept an easing option and cannot be safely changed locally, if `currentY` has different semantics than drag offset, or if the component has already moved to a dedicated drag library.

---

## 4) Recommended execution order

1. **Plan 1:** highest throughput impact; removes the most visible slow-start overlay motion.
2. **Plan 2:** low-risk compositor/accessibility win for occasional feedback.
3. **Plan 3:** high-value but requires more local code inspection because `animateTo`, refs, and drag semantics are not fully shown.

## Explicitly unverified states

- Actual `DESIGN.md` contents beyond the provided summary.
- Package manager, scripts, build commands, and test gates.
- Runtime mount/unmount behavior for command palette, popovers, and toasts.
- Whether popovers receive trigger-origin CSS variables.
- Whether `queueRef` points to the whole queue or the active dragged item.
- `animateTo` API, cancellation support, easing support, and current interruption behavior.
- Actual frame rate, layout/composite cost, reduced-motion behavior, keyboard focus behavior, and accessibility-tree output.
