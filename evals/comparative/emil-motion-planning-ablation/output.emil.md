## 1. Recon summary

- **Stack signals**: React/TSX components plus CSS/Tailwind-style arbitrary animation classes. Motion appears to be mostly CSS transitions/keyframes with some JS-driven gesture animation.
- **Where motion lives**:
  - Global tokens and shared classes: `src/styles/motion.css`
  - Component-local animation CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility animation: `src/components/CommandPalette.tsx`
  - Gesture JS: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Tokens exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`.
  - Correct local precedent exists in `Button.css`: transform-only transition, tokenized duration/easing, and a Reduced Motion branch that shortens rather than removes feedback.
- **Product personality**: calm desktop operations console. Motion should be crisp, causal, and low-latency; decorative or sluggish motion is a throughput cost.
- **Frequency map from provided context**:
  - Very high frequency / keyboard-heavy: command palette.
  - High sensitivity / direct manipulation: sortable queue drag/release.
  - Occasional but visible: popovers and toasts.
  - Correct precedent: button press feedback.
- **Evidence level**: static snippet audit only. Findings below are based on explicit code values/properties shown. No runtime feel, computed style, browser trace, accessibility tree, or device validation was performed.

---

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`. For keyboard-heavy operators, a 420ms ease-in entrance delays a high-frequency action. | Remove the entrance animation or reduce it to immediate state change; preserve focus/visibility without motion. |
| 2 | HIGH | Performance / easing / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This animates unintended properties, exceeds existing token rhythm, and starts slowly. | Transition only `transform` and `opacity` using existing tokens; add Reduced Motion handling. |
| 3 | HIGH | Gesture / interruptibility | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` on the queue root, and release uses fixed `duration: 400`. Static evidence suggests parent-wide style recalculation risk and non-velocity-aware release. | Drive transform on the dragged item, preserve velocity into release, use a spring-like settle if supported, and branch for Reduced Motion. |
| 4 | MEDIUM | Performance / accessibility | `src/components/toast.css` | Toast animates `top` from `-24px` to `0` over `500ms ease-in`; this is layout-affecting, slow, and has no shown Reduced Motion path. | Animate `transform` + `opacity` with existing panel duration/easing; Reduced Motion should keep opacity feedback and remove travel. |
| 5 | MEDIUM | Reduced Motion coverage | Multiple snippets | Only `Button.css` shows `prefers-reduced-motion`. Popover, command palette, toast, and queue snippets do not. | Copy the button precedent: preserve feedback, shorten/remove movement, avoid disabling all state indication. |
| 6 | MEDIUM | Token cohesion | `CommandPalette.tsx`, `toast.css`, `motion.css` | Motion values are hand-authored: `420ms ease-in`, `500ms ease-in`, `360ms ease-in`, despite available semantic tokens. | Route common UI motion through existing duration/easing tokens and avoid arbitrary one-off values. |

---

## 3. Implementation plans

### Plan 1 — Remove delayed command-palette motion

**Exact file/current excerpt**

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

- Opening/closing the command palette must feel immediate for keyboard-heavy repeated use.
- Remove the 420ms ease-in animation from the palette container.
- Do not add replacement decorative motion.
- Preserve `data-open={open}` because it may be used by styling/tests.
- Preserve focus behavior and search result rendering.

**Project conventions to follow**

- Existing motion tokens prefer crisp durations and `--ease-responsive`.
- Existing correct precedent: `src/components/Button.css` keeps subtle transform feedback and Reduced Motion support.
- For this specific high-frequency keyboard surface, the preferred motion is no entrance animation.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove only the arbitrary animation class:
   ```tsx
   <div data-open={open}>
     <SearchResults />
   </div>
   ```
2. If removing `className` would break existing class composition in the real file, keep the other classes and remove only:
   ```tsx
   animate-[palette_420ms_ease-in_both]
   ```
3. Search for the `palette` keyframe/animation definition. If it is now unused, remove it only if it is local to the command palette and not referenced elsewhere.
4. Do not replace this with a shorter transition unless product/design review explicitly requests one.

**Hard boundaries**

- Do not change command search logic, shortcut handling, focus management, or result rendering.
- Do not add a motion library.
- Do not add enter/exit state machines.
- If the palette relies on the animation class for visibility, mounting, or pointer-event state, stop and report source drift instead of guessing.

**Mechanical checks**

- Confirm no `animate-[palette_420ms_ease-in_both]` remains in `src/components/CommandPalette.tsx`.
- Search targeted files for `palette_420ms` / `@keyframes palette`; remove only confirmed dead local code.
- Run the project’s existing lint/typecheck gate if available.

**Runtime/feel checks for executor**

- Open the palette via keyboard shortcut repeatedly.
- Confirm it appears immediately without a slow fade/slide.
- Confirm search input focus is not delayed.
- Confirm closing/reopening rapidly does not show stale transitional states.

**Reduced Motion behavior**

- No special branch required if the animation is removed.
- Reduced Motion users should receive the same immediate state change.

**Source-drift stop condition**

- Stop if the real component has additional class composition, visibility styles, or transition hooks not shown here and the animation class cannot be removed independently.

---

### Plan 2 — Tokenize and de-risk popover/toast motion

**Exact files/current excerpts**

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

- Popovers: transition only compositor-safe properties; use existing duration/easing tokens; avoid `transition: all`; include Reduced Motion duration reduction.
- Toasts: enter using `transform` and `opacity`, not `top`; use existing `--duration-panel` and `--ease-responsive`; Reduced Motion keeps opacity feedback and removes vertical travel.
- Keep the calm operations-console feel: quick, legible, not bouncy.

**Project conventions to follow**

- Use existing tokens:
  ```css
  --duration-fast: 160ms;
  --duration-panel: 240ms;
  --ease-responsive: cubic-bezier(0.23, 1, 0.32, 1);
  ```
- Follow the existing button precedent:
  ```css
  @media (prefers-reduced-motion: reduce) {
    .button { transition-duration: 80ms; }
  }
  ```

**Ordered steps**

1. In `src/styles/motion.css`, replace the popover transition with explicit properties:
   ```css
   .popover {
     transform-origin: center;
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
2. If the real popover is trigger-anchored and the component system exposes a trigger-origin CSS variable, replace `center` with that variable. If no such variable exists in the codebase, keep `center` rather than inventing geometry.
3. In `src/components/toast.css`, replace layout animation with transform animation:
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
       from {
         transform: none;
         opacity: 0;
       }
       to {
         transform: none;
         opacity: 1;
       }
     }

     .toast {
       animation-duration: 80ms;
     }
   }
   ```
4. If redefining `@keyframes toast-enter` inside the media query conflicts with the project’s CSS tooling, create a separate reduced-motion keyframe:
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

- Do not change toast placement, stacking logic, dismissal timing, or content.
- Do not animate `top`, `left`, `width`, `height`, `margin`, or `padding`.
- Do not introduce new token names unless the existing token file explicitly requires aliases.
- Do not change `.button`; it is the correct precedent.

**Mechanical checks**

- Confirm targeted files no longer contain:
  - `transition: all`
  - `360ms ease-in`
  - `500ms ease-in`
  - `from { top:`
- Confirm popover/toast use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Run existing lint/build/style checks if available.

**Runtime/feel checks for executor**

- Trigger popovers repeatedly and confirm there is no sluggish start.
- Trigger a toast and confirm it slides/fades quickly without layout jump.
- In slow-motion DevTools playback, confirm the toast moves via `transform`, not `top`.
- Toggle Reduced Motion and confirm toast movement is removed while fade feedback remains.

**Reduced Motion behavior**

- Popover: duration shortens to `80ms`; no extra travel should be added.
- Toast: movement removed; opacity feedback remains over `80ms`.

**Source-drift stop condition**

- Stop if `.popover` or `.toast` are not the real rendered classes, or if visibility/positioning depends on the removed animation properties.

---

### Plan 3 — Make sortable queue drag directly manipulated and motion-safe

**Exact file/current excerpt**

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

- During drag, the actively dragged item follows the pointer directly.
- Do not drive child movement through a parent-level CSS variable unless the real implementation proves that only one isolated element depends on it.
- On release, settle to the nearest slot with interruptible, velocity-aware motion if the existing `animateTo` helper supports it.
- Reduced Motion should avoid travel animation while preserving the committed reorder/state feedback.

**Project conventions to follow**

- Existing motion is token-based and crisp.
- For direct manipulation, visual response should track input immediately.
- Fixed 400ms release is too slow for a throughput-focused queue unless justified elsewhere in code.

**Ordered steps**

1. Inspect the real `SortableQueue.tsx` around the drag refs/state before editing.
2. Identify the dragged item element ref. If none exists, add a local ref to the dragged item only; do not attach movement styles to the queue root.
3. Replace parent CSS-variable updates with direct dragged-item transform updates. Target pattern:
   ```tsx
   function onPointerMove(event: PointerEvent) {
     const nextY = event.clientY;
     currentY = nextY;

     draggedItemRef.current?.style.setProperty(
       "transform",
       `translate3d(0, ${nextY - dragStartY}px, 0)`
     );
   }
   ```
   Use the real state/ref names from the file; do not invent parallel drag state if equivalents already exist.
4. Track release velocity using the last pointer positions/timestamps:
   ```tsx
   const velocityY = (currentY - previousY) / Math.max(1, now - previousTime);
   ```
5. On pointer up, project the target slightly by velocity before selecting the nearest slot:
   ```tsx
   const projectedY = currentY + velocityY * 120;
   const targetSlot = nearestSlot(projectedY);
   ```
6. If `animateTo` supports spring-style options, replace fixed duration with:
   ```tsx
   animateTo(targetSlot, {
     type: "spring",
     duration: 0.5,
     bounce: 0.2,
     velocity: velocityY
   });
   ```
7. If `animateTo` does not support spring or velocity, reduce the fixed settle duration to the existing panel token equivalent if the helper accepts tokenized duration, or `240` ms if it requires a number:
   ```tsx
   animateTo(targetSlot, { duration: 240 });
   ```
   Do not add a new animation dependency.
8. Add a Reduced Motion branch using `window.matchMedia("(prefers-reduced-motion: reduce)")` or the project’s existing reduced-motion helper if one exists:
   - normal motion: drag follows pointer and settles with spring/short tween.
   - reduced motion: commit to `nearestSlot(currentY)` immediately or with an `80ms` opacity/color/state cue, but no travel animation.

**Hard boundaries**

- Do not rewrite queue data modeling or reorder semantics.
- Do not add dependencies.
- Do not change keyboard reordering behavior unless it already shares this animation path.
- Do not introduce bounce beyond `0.2`.
- If multiple queue children intentionally depend on `--drag-y` for collision/preview positioning, stop and split this into a larger queue-motion design task.

**Mechanical checks**

- Confirm `queueRef.current?.style.setProperty("--drag-y"` is removed or proven isolated.
- Confirm the dragged element receives `transform: translate3d(...)`.
- Confirm no layout property is animated for drag settle.
- Confirm `duration: 400` is removed from the release path or justified by an explicit existing design comment.
- Run existing typecheck/lint gate if available.

**Runtime/feel checks for executor**

- Drag slowly: item should stay under the pointer without visible lag.
- Drag quickly and release: settle should continue the release direction rather than stopping then restarting.
- Interrupt by dragging again during settle: motion should retarget cleanly, not jump from the original start.
- Toggle Reduced Motion: reordering should remain understandable without travel animation.

**Reduced Motion behavior**

- Pointer tracking can remain direct while the user is actively dragging.
- Release animation should be removed or shortened to `80ms` non-spatial feedback.
- State continuity should be preserved through slot highlight, opacity, or final placement—not through long movement.

**Source-drift stop condition**

- Stop if the real queue uses a drag library, virtualization, collision engine, or CSS-variable choreography not visible in the snippet. In that case, produce a smaller follow-up plan for that concrete implementation rather than applying this generic refactor.

---

## 4. Recommended execution order

1. **Command palette** — highest throughput impact and smallest safe change.
2. **Popover/toast tokenization** — removes broad `transition: all`, layout animation, slow ease-in, and adds Reduced Motion coverage.
3. **Sortable queue** — highest craft payoff but most source-dependent; execute only after inspecting the real drag implementation.

## Explicitly unverified states

- Actual framework/library choices beyond React/CSS/Tailwind-style class evidence.
- Whether `.popover` is trigger-anchored, modal-like, or used for multiple component types.
- Whether the command palette animation controls visibility or only decorative entrance.
- Whether `animateTo` supports spring, velocity, cancellation, or tokenized durations.
- Actual focus behavior, keyboard shortcut flow, accessibility tree, frame rate, layout cost, and user-perceived feel.
- Existing package scripts, lint/typecheck/build commands, and CSS tooling support for media-scoped keyframes.
