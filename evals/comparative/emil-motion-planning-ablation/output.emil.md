## 1. Recon summary

- **Stack signals**: React/TSX components, plain CSS, semantic CSS custom-property tokens, utility-style arbitrary animation classes, imperative pointer/animation code.
- **Where motion lives**:
  - Global tokens and shared selectors: `src/styles/motion.css`
  - Component-local CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility animation: `src/components/CommandPalette.tsx`
  - Gesture/reorder logic: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Durations: `--duration-fast: 160ms`, `--duration-panel: 240ms`
  - Easing: `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct precedent: button press uses `transform`, semantic tokens, and `prefers-reduced-motion` with `80ms`.
- **Product personality**: crisp, calm, low-latency operations UI. Motion should clarify state and causality, not decorate or delay repeated workflows.
- **Frequency map from product context + snippets**:
  - Very high: command palette, keyboard-triggered actions.
  - High: queue sorting/dragging during operational triage.
  - Medium: popovers.
  - Occasional: toasts.
- **Evidence level**: static code excerpt only. No runtime, computed style, trace, screen recording, accessibility tree, or user testing was performed.

---

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency / latency | `src/components/CommandPalette.tsx` | A likely high-frequency keyboard surface animates with `420ms ease-in`. This delays the exact response operators need to feel immediate. | Remove the command palette entrance animation; keep open/closed state instantaneous. |
| 2 | HIGH | Performance / easing / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in`; this can animate unintended properties, exceeds the existing fast/panel token rhythm, and starts slowly. | Restrict to `transform, opacity`; use existing duration/easing tokens; add reduced-motion duration. |
| 3 | MEDIUM | Physicality / origin | `src/styles/motion.css` | `.popover { transform-origin: center; }` is suspicious for trigger-anchored UI. Static evidence does not prove all `.popover` usage is trigger-anchored, so this is conditional. | Use a trigger-origin custom property only if the component already exposes one; otherwise stop and escalate. |
| 4 | HIGH | Performance / accessibility / interruptibility | `src/components/toast.css` | Toast entry animates `top` for `500ms ease-in` via keyframes and has no shown reduced-motion path. `top` is layout-affecting; keyframes are poorer for rapidly changing stacks. | Animate `transform`/`opacity`, cap to existing panel timing, add reduced-motion opacity-only feedback. |
| 5 | HIGH | Gesture / performance / accessibility | `src/components/SortableQueue.tsx` | Pointer move writes a CSS custom property on the queue container; release uses a fixed `400ms` animation. Static evidence does not show velocity, interruptibility, or reduced-motion handling. | Move active item with direct transform, shorten/retarget release motion, add reduced-motion branch. |

No additive “missed opportunity” is supportable from the static snippets alone.

---

# Plan 1 — Make command palette opening immediate

- **Severity**: HIGH  
- **Category**: Purpose / frequency / latency  
- **Estimated scope**: 1 file, small TSX edit

## Current evidence

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

## Target behavior

The command palette should appear/disappear immediately when `open` changes. It is a high-frequency keyboard surface; motion here should not delay task throughput.

Target excerpt:

```tsx
// src/components/CommandPalette.tsx — target
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div data-open={open}>
      <SearchResults />
    </div>
  );
}
```

If the real file contains additional non-motion classes, preserve them and remove only the `animate-[palette_420ms_ease-in_both]` class.

## Project conventions to follow

- Use semantic shared tokens for motion only where motion is justified.
- Existing correct precedent: `src/components/Button.css` uses `transform`, `--duration-fast`, `--ease-responsive`, and a reduced-motion duration.
- Do not introduce a new palette animation token for this surface.

## Ordered steps

1. Open `src/components/CommandPalette.tsx`.
2. Remove `animate-[palette_420ms_ease-in_both]` from the `className`.
3. If `className` becomes empty, remove the `className` prop entirely.
4. Do not change `data-open`, `SearchResults`, focus management, keyboard handling, or markup hierarchy.
5. Search for the `palette` keyframe or utility definition. If it is used nowhere else, leave deletion as a separate cleanup only if project conventions allow dead CSS removal.

## Hard boundaries

- Do **not** add a replacement fade, scale, slide, blur, or stagger.
- Do **not** alter search result rendering or keyboard behavior.
- Do **not** change open-state semantics beyond removing the animation class.

## Mechanical checks

- Confirm `src/components/CommandPalette.tsx` no longer contains `420ms`, `ease-in`, or `animate-[palette`.
- Run the project’s existing lint/type-check command if available.
- If no scripts are known, at minimum ensure the TSX still parses and the component signature is unchanged.

## Runtime / feel checks for executor

- Open/close the command palette repeatedly using the keyboard shortcut.
- Confirm it responds immediately, with no visible entrance delay.
- Confirm focus still lands where it did before.
- In reduced-motion mode, confirm behavior is identical and still immediate.

## Reduced Motion behavior

No separate reduced-motion branch is needed because the motion is removed for all users.

## Source-drift stop condition

Stop and report instead of editing if:
- The animation class is also responsible for visibility/layout, not just motion.
- The component has been rewritten to use a different animation system.
- Removing the class would remove required styling unrelated to motion.

---

# Plan 2 — Normalize popover and toast entrance motion

- **Severity**: HIGH  
- **Category**: Performance / easing / accessibility / cohesion  
- **Estimated scope**: 2 CSS files

## Current evidence

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

## Target behavior

- Popovers transition only compositor-safe properties.
- Toasts enter using `transform` and `opacity`, not `top`.
- Both use existing semantic tokens.
- Reduced Motion preserves opacity feedback while removing movement.

Target excerpt:

```css
/* src/styles/motion.css — target */
:root {
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
}

.popover {
  transform-origin: var(--popover-transform-origin, center);
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

```css
/* src/components/toast.css — target */
.toast {
  top: 0;
  opacity: 1;
  transform: translate3d(0, 0, 0);
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}

@starting-style {
  .toast {
    opacity: 0;
    transform: translate3d(0, -8px, 0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .toast {
    transition-duration: 80ms;
    transform: none;
  }

  @starting-style {
    .toast {
      opacity: 0;
      transform: none;
    }
  }
}
```

## Project conventions to follow

- Reuse existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Match the local button precedent: animate `transform`; use `80ms` in reduced-motion mode.
- Do not create parallel hard-coded duration/easing values.

## Ordered steps

1. In `src/styles/motion.css`, replace `.popover { transition: all 360ms ease-in; }` with explicit `transform` and `opacity` transitions using `--duration-fast` and `--ease-responsive`.
2. Replace `transform-origin: center` with `transform-origin: var(--popover-transform-origin, center)`.
3. If actual popover code already exposes a trigger-origin variable, set `--popover-transform-origin` there. If no such source exists, leave the fallback and report that trigger-origin wiring needs component context.
4. Add the reduced-motion media query for `.popover` with `transition-duration: 80ms`.
5. In `src/components/toast.css`, remove `@keyframes toast-enter`.
6. Replace `.toast { animation: toast-enter 500ms ease-in forwards; }` with the target transition-based block.
7. Add the `@starting-style` block and reduced-motion override.
8. Preserve existing toast placement rules not shown in the snippet.

## Hard boundaries

- Do **not** animate `top`, `left`, `width`, `height`, `margin`, or `padding`.
- Do **not** introduce new dependencies.
- Do **not** change toast lifetime, stacking logic, dismissal behavior, or ARIA/live-region behavior.
- Do **not** assume every `.popover` is trigger-anchored unless the component evidence confirms it.

## Mechanical checks

- `src/styles/motion.css` should no longer contain `transition: all` or `360ms ease-in`.
- `src/components/toast.css` should no longer contain `@keyframes toast-enter`, `top: -24px`, `500ms`, or `ease-in`.
- Confirm both files include a `prefers-reduced-motion: reduce` path.
- Run the project’s existing lint/build checks if available.

## Runtime / feel checks for executor

- Open a popover slowly and confirm no unintended color/layout properties animate.
- If trigger-origin wiring exists, confirm scale/opacity appears connected to the trigger rather than the viewport center.
- Trigger a toast and confirm it moves only slightly, settles within the panel-duration rhythm, and does not feel delayed.
- In reduced-motion mode, confirm toast movement is removed but opacity feedback remains.

## Reduced Motion behavior

- Popover: keep a short `80ms` transition.
- Toast: remove translate movement; keep opacity feedback at `80ms`.

## Source-drift stop condition

Stop and report instead of editing if:
- Toast mounting is not compatible with `@starting-style` and requires a JS-mounted state.
- `.toast` relies on the keyframe’s final `top: 0` for layout in a way not represented elsewhere.
- `.popover` has been replaced by a component-scoped animation system.
- The project already has a different reduced-motion utility that should be reused.

---

# Plan 3 — Make sortable queue drag motion direct, shorter, and reduced-motion aware

- **Severity**: HIGH  
- **Category**: Gesture / performance / accessibility  
- **Estimated scope**: 1 TSX file, possible local CSS adjustment if `--drag-y` is consumed nearby

## Current evidence

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

## Target behavior

- Pointer movement should update only the actively dragged item’s transform, not a queue-level custom property that may invalidate a larger subtree.
- Release motion should be shorter and interruptible where the existing animation adapter supports it.
- Reduced Motion should preserve slot feedback but shorten/remove travel.

Target release shape:

```tsx
// src/components/SortableQueue.tsx — target shape
function onPointerUp() {
  setDragging(false);

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  animateTo(
    nearestSlot(currentY),
    prefersReducedMotion
      ? { duration: 80 }
      : { type: "spring", duration: 0.5, bounce: 0.2 }
  );
}
```

Target pointer-move principle:

```tsx
// target principle: apply transform to the active dragged item, not queue container
draggedItemRef.current?.style.setProperty(
  "transform",
  `translate3d(0, ${currentDragY}px, 0)`
);
```

`currentDragY` must be the existing drag delta or rendered drag offset, not blindly `event.clientY` if that value is viewport-relative.

## Project conventions to follow

- Existing CSS precedent favors `transform` over layout properties.
- Existing reduced-motion precedent uses `80ms`.
- Use existing animation infrastructure; do not add a new animation dependency for this change.

## Ordered steps

1. Open `src/components/SortableQueue.tsx`.
2. Locate where `--drag-y` is consumed. If it controls many children from the queue root, replace that pattern with a ref/style update on the actively dragged row/item.
3. Add or reuse an existing `draggedItemRef` for the active item only.
4. During `onPointerMove`, compute or reuse the current drag delta and set `transform: translate3d(0, <delta>, 0)` on the dragged item.
5. Remove the queue-root write: `queueRef.current?.style.setProperty("--drag-y", ...)`.
6. In `onPointerUp`, replace `{ duration: 400 }` with:
   - `{ duration: 80 }` when `prefers-reduced-motion: reduce` matches.
   - `{ type: "spring", duration: 0.5, bounce: 0.2 }` if the existing `animateTo` adapter supports spring configs.
7. If `animateTo` does not support spring configs, use the existing closest interruptible/retargetable option. If none exists, reduce normal duration to `240` and report the lack of an interruptible adapter as follow-up.
8. Ensure cleanup clears the dragged item’s inline `transform` after it reaches the slot.

## Hard boundaries

- Do **not** add dependencies.
- Do **not** rewrite queue ordering, selection, keyboard controls, or data persistence.
- Do **not** use `top`, `left`, margin, or padding for drag movement.
- Do **not** apply transform to the whole queue unless the whole queue is intentionally moving.

## Mechanical checks

- `src/components/SortableQueue.tsx` should no longer contain `style.setProperty("--drag-y"` inside `onPointerMove`.
- `duration: 400` should be removed from the release path.
- A reduced-motion branch using `80` should exist.
- Drag movement should be expressed as `transform` / `translate3d`.

## Runtime / feel checks for executor

- Drag one item through a dense queue and confirm only the active item follows the pointer.
- Release near a slot and confirm the item settles without a long glide.
- Interrupt by dragging again quickly and confirm motion retargets rather than fighting the pointer.
- In reduced-motion mode, confirm the item still communicates final placement but with minimal travel and `80ms` timing.

## Reduced Motion behavior

- During active drag, direct manipulation should still track the pointer.
- On release, settle with `80ms` timing and avoid decorative bounce.

## Source-drift stop condition

Stop and report instead of editing if:
- `animateTo` does not accept either duration or spring-like options as shown.
- `--drag-y` is already scoped to only the active item despite being set on `queueRef`.
- The queue has keyboard reorder behavior coupled to the same motion path and the effect is unclear from code.

---

## Recommended execution order

1. **Plan 1 — Command palette**: highest frequency, smallest safe change.
2. **Plan 2 — Popover/toast CSS**: removes broad unsafe motion patterns and aligns with existing tokens.
3. **Plan 3 — Sortable queue**: highest interaction complexity; should be handled after the simpler token/cohesion fixes.

## Explicitly unverified states

- Actual route/component hierarchy.
- Whether `.popover` is always trigger-anchored.
- Whether `palette` keyframes are used elsewhere.
- Package scripts for lint/type-check/build.
- Runtime feel, frame pacing, computed styles, browser support, and reduced-motion behavior.
- Accessibility tree, focus management, live-region behavior, and keyboard reorder behavior.
- Whether `animateTo` supports spring or velocity-aware options.
