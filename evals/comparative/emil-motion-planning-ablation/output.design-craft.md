Diagnosis: the system already has a good crisp-motion precedent, but several transient and direct-manipulation paths bypass it with long `ease-in`, broad/property-heavy motion, and incomplete Reduced Motion coverage.

## 1. Recon summary

- **Stack signals:** React/TSX components, CSS files, Tailwind-style arbitrary animation class, inline style mutation for drag, and a custom `animateTo(...)` helper.
- **Where motion lives:**  
  - Global tokens and `.popover`: `src/styles/motion.css`  
  - Component animation class: `src/components/CommandPalette.tsx`  
  - Toast keyframes: `src/components/toast.css`  
  - Direct manipulation: `src/components/SortableQueue.tsx`  
  - Correct local precedent: `src/components/Button.css`
- **Existing conventions:**  
  - Tokens: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`  
  - Preferred property precedent: explicit `transform`, not `all`  
  - Reduced Motion precedent: preserve feedback, shorten to `80ms`
- **Product personality:** calm, workday operations console; motion should be crisp, causal, and non-performative.
- **Frequency map:**  
  - High-frequency / keyboard-heavy: command palette, buttons  
  - Repeated operational overlays: popovers  
  - Occasional but potentially repeated: toasts  
  - Direct manipulation: sortable queue drag/reorder
- **Evidence level:** static excerpts only. No runtime behavior, computed styles, traces, screen recordings, accessibility-tree output, or user testing were observed.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | Static | `src/components/CommandPalette.tsx` | `animate-[palette_420ms_ease-in_both]` conflicts with high-frequency keyboard use and token precedent; `ease-in` delays initial response by definition. | Replace arbitrary long keyframe with tokenized opacity/very small transform transition; add Reduced Motion branch. |
| P1 | Static | `src/components/SortableQueue.tsx` | Drag release uses fixed `duration: 400` with no visible velocity, projection, pointer capture, grab-offset, or interruption contract in the excerpt. | Audit/implement direct-manipulation physics: capture pointer, preserve offset, track velocity, snap from projected endpoint, settle interruptibly. |
| P2 | Static | `src/components/toast.css` | Toast animates `top` for `500ms ease-in`; this is a layout-property animation risk and is slower than the project’s panel token. | Animate `transform` + `opacity` with existing tokens; Reduced Motion removes vertical travel but keeps feedback. |
| P2 | Static | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`; broad property ownership and non-token timing diverge from local precedent. | Restrict to `opacity, transform`; use project tokens; verify whether origin should be trigger-relative before changing it. |
| P2 | Static | Multiple excerpts | Reduced Motion is only proven for `.button`; other meaningful motion excerpts do not show a Reduced Motion path. | Add per-component Reduced Motion branches that preserve state feedback without spatial travel. |

## 3. Implementation plans

### Plan 1 — Normalize command palette and popover transient motion

**Evidence level:** static only.

**Current excerpts**

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

- Command palette opens/closes immediately enough for keyboard-heavy use.
- Motion uses existing tokens: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Palette feedback is primarily opacity plus a tiny scale/translate, not a long entrance.
- Popover transitions only own `opacity` and `transform`.
- Popover origin is trigger-relative if the component has a positioning contract for it; otherwise preserve current origin and only fix timing/property scope.

**Project conventions**

- Follow the button precedent: explicit transform transition, semantic tokens, Reduced Motion duration of `80ms`.
- Preserve visible focus and keyboard throughput.
- Do not introduce decorative bounce.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` transition with explicit properties:

   ```css
   .popover {
     transform-origin: var(--popover-transform-origin, center);
     transition:
       opacity var(--duration-panel) var(--ease-responsive),
       transform var(--duration-panel) var(--ease-responsive);
   }
   ```

2. Before relying on `--popover-transform-origin`, inspect the popover implementation:
   - If a trigger-relative origin variable already exists, map it to `--popover-transform-origin`.
   - If no such positioning signal exists, keep `center` and do not invent geometry.

3. Replace the command palette arbitrary animation with a named class, for example:

   ```tsx
   <div
     data-open={open}
     className="commandPalette"
   >
   ```

4. Add the command palette motion rule in the existing motion stylesheet or the component’s established stylesheet, whichever is already imported for this component:

   ```css
   .commandPalette {
     opacity: 1;
     transform: scale(1);
     transition:
       opacity var(--duration-fast) var(--ease-responsive),
       transform var(--duration-fast) var(--ease-responsive);
   }

   .commandPalette[data-open="false"] {
     opacity: 0;
     transform: scale(0.98);
     pointer-events: none;
   }
   ```

5. Add Reduced Motion coverage:

   ```css
   @media (prefers-reduced-motion: reduce) {
     .popover,
     .commandPalette {
       transition-duration: 80ms;
     }

     .commandPalette,
     .commandPalette[data-open="false"] {
       transform: none;
     }
   }
   ```

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change command execution, focus trapping, keyboard shortcuts, or palette mounting semantics.
- Do not add dependencies.
- Do not add new duration/easing tokens unless a broader token migration is explicitly approved.

**Mechanical checks**

- Run the closest existing checks after inspecting package scripts:
  - type check, if present
  - lint, if present
  - component/unit tests touching command palette or popover, if present
- Verify there are no remaining references to `animate-[palette_420ms_ease-in_both]`.

**Runtime/feel checks to perform later**

- Open/close palette repeatedly by keyboard.
- Interrupt open with close and close with open.
- Confirm focus remains visible and usable throughout.
- Open popover from each supported side/alignment and confirm origin feels spatially attached if trigger-origin data exists.

**Reduced Motion behavior**

- Palette: no scale/positional travel; short opacity feedback remains.
- Popover: no added spatial travel beyond existing open/closed state; duration capped to `80ms`.

**Source-drift stop condition**

Stop before editing if:
- `CommandPalette` no longer contains the cited arbitrary animation.
- `.popover` already has explicit tokenized properties.
- the popover is actually a centered modal-like surface rather than an anchored transient surface.
- `DESIGN.md` or local tokens have replaced the cited motion contract.

---

### Plan 2 — Convert toast entry from layout travel to tokenized transform feedback

**Evidence level:** static only.

**Current excerpt**

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

- Toast entry remains noticeable but calm.
- Vertical travel is small and compositor-friendly.
- Timing uses existing `--duration-panel` and `--ease-responsive`.
- Reduced Motion removes vertical travel while keeping opacity confirmation.

**Project conventions**

- Use existing semantic tokens.
- Prefer `transform` and `opacity`.
- Preserve the toast’s final layout, stacking, live-region behavior, dismissal timing, and focus behavior.

**Ordered steps**

1. Replace `top` animation with transform-based keyframes:

   ```css
   @keyframes toast-enter {
     from {
       transform: translateY(var(--toast-enter-y, -8px));
       opacity: 0;
     }
     to {
       transform: translateY(0);
       opacity: 1;
     }
   }
   ```

2. Replace the toast animation rule:

   ```css
   .toast {
     animation: toast-enter var(--duration-panel) var(--ease-responsive) both;
   }
   ```

3. Add Reduced Motion behavior:

   ```css
   @media (prefers-reduced-motion: reduce) {
     .toast {
       --toast-enter-y: 0px;
       animation-duration: 80ms;
     }
   }
   ```

4. Inspect for existing toast exit animations. If an exit exists, apply the same principles there: no layout-property animation, no long `ease-in`, no large travel in Reduced Motion.

**Hard boundaries**

- Do not change toast positioning model except removing animated `top`.
- Do not change stacking order, auto-dismiss duration, ARIA/live-region behavior, or toast content.
- Do not add new animation libraries.
- Do not make the toast invisible until JavaScript starts.

**Mechanical checks**

- CSS parse/build check through the project’s existing frontend build or lint command.
- Search for remaining `top` animation inside `toast.css`.
- Search for duplicate `toast-enter` definitions before editing.

**Runtime/feel checks to perform later**

- Trigger one toast and multiple consecutive toasts.
- Confirm entry feels prompt and does not visually push layout.
- Confirm auto-dismiss and manual dismiss still work.
- Confirm no toast content becomes unreachable during animation.

**Reduced Motion behavior**

- Toast fades in over `80ms`.
- No vertical movement.
- State feedback is preserved through opacity and final placement.

**Source-drift stop condition**

Stop before editing if:
- `toast-enter` no longer matches the cited keyframes.
- toast positioning depends on animated `top` for final layout rather than entry effect.
- a separate toast lifecycle system already owns entry/exit animation.

---

### Plan 3 — Rework sortable queue release around direct-manipulation physics

**Evidence level:** static only.

**Current excerpt**

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
- Grab offset is preserved; the item does not jump under the pointer.
- Pointer capture keeps the drag active outside the original bounds.
- Release chooses a slot from projected endpoint, not only the release position.
- Release animation starts from the current presented position and measured velocity.
- Reduced Motion keeps direct tracking but removes elastic/large settle effects.

**Project conventions**

- Preserve throughput and precision for operators.
- Use existing animation utilities first.
- Keep drag work out of React render loops where possible.
- Avoid broad CSS variable updates on large parent trees if the variable affects many descendants.

**Ordered steps**

1. Inspect the full component for:
   - pointer-down handler
   - item identity and active dragged element
   - `currentY` source
   - `nearestSlot(...)`
   - `animateTo(...)` implementation/signature
   - CSS consuming `--drag-y`

2. On pointer down, create a drag session ref:

   ```ts
   {
     pointerId,
     containerTop,
     grabOffsetY,
     currentY,
     samples: Array<{ y: number; t: number }>
   }
   ```

   Cache layout measurements once at drag start, not on every move.

3. Call pointer capture on the interactive drag target once drag intent is confirmed:

   ```ts
   event.currentTarget.setPointerCapture(event.pointerId);
   ```

4. On pointer move:
   - Ignore non-active pointer IDs.
   - Compute list-local CSS pixels, not raw viewport `clientY`:

     ```ts
     const y = event.clientY - containerTop - grabOffsetY;
     ```

   - Update only the dragged item’s transform owner, for example via a local CSS variable on that item, not a parent variable that may invalidate the full queue.
   - Track recent samples using monotonic timestamps for velocity.

5. On pointer up:
   - Release pointer capture.
   - Compute velocity in CSS px/s from recent samples.
   - Project endpoint from current position and velocity.
   - Choose `nearestSlot(projectedY)`.
   - Start the settle animation from the current presentation value.
   - Pass velocity to the animation primitive if supported.

6. Replace fixed `duration: 400` with an interruptible settle:
   - preferred: existing spring/physics API with no or minimal overshoot
   - acceptable fallback only if no spring exists: bounded tokenized duration based on distance, using `--ease-responsive`, while marking velocity handoff as not fully satisfied

7. Ensure a new drag during the settle cancels/retargets from the current visible position, not the previous logical target.

**Hard boundaries**

- Do not change queue ordering data semantics.
- Do not change keyboard reorder behavior, if present.
- Do not add an animation dependency unless the existing `animateTo` helper cannot be extended locally and the dependency decision is explicitly approved.
- Do not combine press scale and drag translate on the same uncoordinated `transform` owner; use wrapper layers or one composed transform.

**Mechanical checks**

- Type check the component.
- Run existing tests for queue ordering/reordering, if present.
- Add or update unit tests for `nearestSlot(projectedY)` if the function is testable.
- Static check that the drag hot path does not call React state setters on every pointer move.

**Runtime/feel checks to perform later**

- Drag slowly across slots.
- Flick quickly toward a neighboring and a farther slot.
- Release, then immediately re-grab during settle; confirm no jump.
- Move pointer outside the item while dragging; confirm capture keeps tracking.
- Confirm grab offset is preserved.
- Test under a long queue if that state exists.

**Reduced Motion behavior**

- Direct pointer tracking remains; direct manipulation is not removed.
- Release settle uses no bounce/overshoot and a short duration.
- Large elastic travel, decorative recoil, or parallax is disabled.
- Slot change feedback remains visible through final position/state styling.

**Source-drift stop condition**

Stop before editing if:
- `animateTo` already implements velocity-aware interruption and the excerpt is stale.
- `--drag-y` is not used for the dragged item’s transform.
- the queue is not reorderable direct manipulation in current source.
- `nearestSlot` semantics changed from pixel position to index/data-based snapping.

## 4. Recommended execution order

1. **Plan 1:** fixes the highest-frequency keyboard/overlay motion and aligns the system with existing tokens.  
2. **Plan 2:** isolated, low-risk cleanup that removes layout-property toast motion.  
3. **Plan 3:** highest interaction complexity; do after the token/overlay cleanup because it needs runtime feel validation and possibly animation-helper inspection.

## Explicitly unverified states

- Actual imported CSS order and selector specificity.
- Whether `palette` keyframes exist elsewhere.
- Computed durations/easing in the browser.
- Real smoothness, frame pacing, layout shift, or paint/composite cost.
- Focus trap behavior, keyboard focus visibility, and accessibility-tree output.
- Actual Reduced Motion behavior outside the button excerpt.
- Pointer capture, grab offset, interruption, velocity handoff, and touch/device feel for the sortable queue.
- Toast ARIA/live-region behavior and dismissal lifecycle.

No files were edited; this is an evidence-bound implementation roadmap only.
