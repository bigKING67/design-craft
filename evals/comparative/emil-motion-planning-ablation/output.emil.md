## 1. Recon summary

- **Stack signals**: React/TSX components plus CSS. Tailwind-style arbitrary animation utility appears in `CommandPalette.tsx`. No runtime motion library is proven from the evidence.
- **Where motion lives**:
  - Global motion tokens in `src/styles/motion.css`.
  - Component CSS in `src/components/toast.css` and `src/components/Button.css`.
  - Inline utility class in `src/components/CommandPalette.tsx`.
  - Imperative pointer/settle code in `src/components/SortableQueue.tsx`.
- **Existing conventions**:
  - Tokens: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`.
  - Correct local precedent: button press uses `transform`, tokenized duration/easing, and a reduced-motion duration of `80ms`.
- **Product personality**: calm, crisp, workday operations console. Motion should explain causality/state continuity, not decorate or delay throughput.
- **Frequency map**:
  - Command palette: likely very high-frequency, keyboard-heavy; should be instant or near-instant.
  - Sortable queue: likely high-frequency during queue work; gesture response must preserve continuity.
  - Popovers: likely frequent operational controls; should be short and anchored.
  - Toasts: occasional feedback; can animate, but should be fast and non-layout.
- **Evidence level**: static snippets only. No runtime behavior, computed styles, trace, accessibility tree, browser/device validation, or user testing was performed.

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`. For a keyboard-heavy console, a 420ms ease-in entrance is too slow for a high-frequency command surface. | Remove the entrance animation; make open/close immediate. |
| 2 | HIGH | Easing / performance / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This is slow, starts sluggishly, and may animate unintended properties. | Limit transition to `transform, opacity`; use existing tokens and ≤200ms timing. |
| 3 | MEDIUM | Physicality / origin | `src/styles/motion.css` | `.popover` uses `transform-origin: center;`. For trigger-anchored popovers, center origin can break spatial causality. Static evidence does not prove the popover is modal-like. | Use trigger-provided origin variables when available, with safe fallback. |
| 4 | MEDIUM | Performance / easing / accessibility | `src/components/toast.css` | Toast enter animates `top` for `500ms ease-in`; this is layout-affecting and longer than the existing panel token. No reduced-motion branch is shown. | Animate `transform` + `opacity`, use `--duration-panel` and `--ease-responsive`, add reduced-motion fade-only path. |
| 5 | MEDIUM | Gesture / interruptibility | `src/components/SortableQueue.tsx` | Drag move writes `--drag-y` imperatively, and release uses fixed `duration: 400`. Static evidence does not show how `--drag-y` is consumed, but the settle motion is likely not velocity-aware. | Move only the dragged item/layer via transform; use interruptible spring settle if supported; shorten/no-bounce path for reduced motion. |

No additive “missed opportunity” is justified from these snippets alone.

---

## 3. Implementation plans

### Plan 1 — Make the command palette immediate

**Files / current excerpt**

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

- Opening/closing the command palette must not wait on a 420ms animation.
- Keyboard invocation should reveal the command surface immediately.
- Reduced Motion behavior is identical: no movement and no delayed entrance.

**Project conventions**

- Follow the existing crisp-motion direction and semantic token use.
- Do not replace this with another long transition.
- Existing correct precedent: `src/components/Button.css` uses tokenized transform feedback and reduced-motion timing, but command palette frequency is higher than a button press and should be more direct.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, confirm the current wrapper still contains only the animation utility shown above.
2. Remove the `className="animate-[palette_420ms_ease-in_both]"` prop.
3. Leave `data-open={open}` intact.
4. Leave `<SearchResults />`, focus handling, open-state logic, keyboard shortcuts, and markup structure unchanged.

**Target excerpt**

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div data-open={open}>
      <SearchResults />
    </div>
  );
}
```

**Hard boundaries**

- Do not add a replacement animation.
- Do not alter search result rendering, keyboard behavior, focus management, ARIA attributes, or mounting logic.
- Do not remove `data-open`; other styles may depend on it.

**Mechanical checks**

- Run the project’s existing TypeScript and lint checks, if available.
- Search for `palette_420ms_ease-in_both`; expected result after edit: no remaining usage unless deliberately defined elsewhere for unrelated code.

**Runtime / feel checks to perform after implementation**

- Trigger the palette repeatedly with the keyboard shortcut.
- Confirm the palette is available immediately, without a slow fade/slide.
- Confirm visible focus is preserved when opened.
- Toggle Reduced Motion and confirm behavior remains immediate.

**Reduced Motion behavior**

- Same as default: no autonomous movement.

**Source-drift stop condition**

- Stop if the file no longer matches this structure, if the animation class is gone already, or if the class also carries required non-motion styling. Report drift instead of improvising.

---

### Plan 2 — Normalize popover and toast motion to tokenized transform/opacity

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

- Popovers feel responsive and only animate properties intended for motion.
- Trigger-anchored popovers use a trigger-provided transform origin when available.
- Toasts enter with compositor-friendly movement and opacity, not `top`.
- Reduced Motion keeps feedback but removes positional movement.

**Project conventions**

- Reuse existing tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Follow the local reduced-motion precedent from `src/components/Button.css`:
  - reduced duration: `80ms`.

**Ordered steps**

1. In `src/styles/motion.css`, replace the `.popover` rule with explicit transform/opacity transitions.
2. Use trigger-origin variables with fallback, so the rule works with common anchored-popover implementations without requiring a new dependency.
3. Add a reduced-motion branch that shortens the existing transition rather than removing feedback.
4. In `src/components/toast.css`, change `toast-enter` to animate `transform` and `opacity`.
5. Add a separate reduced-motion keyframe that fades only.
6. Change `.toast` to use existing duration/easing tokens.
7. Do not add new global tokens unless the existing tokens are missing in the real file.

**Target excerpts**

`src/styles/motion.css`

```css
.popover {
  transform-origin: var(
    --radix-popover-content-transform-origin,
    var(--transform-origin, center)
  );
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

`src/components/toast.css`

```css
@keyframes toast-enter {
  from {
    transform: translate3d(0, -24px, 0);
    opacity: 0;
  }
  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
}

@keyframes toast-enter-reduced {
  from { opacity: 0; }
  to { opacity: 1; }
}

.toast {
  animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
}

@media (prefers-reduced-motion: reduce) {
  .toast {
    animation-name: toast-enter-reduced;
    animation-duration: 80ms;
  }
}
```

**Hard boundaries**

- Do not change toast positioning outside the keyframes unless required by existing layout.
- Do not change toast lifetime, stacking, dismissal, copy, icons, or severity styling.
- Do not change popover markup or component API.
- Do not introduce a new motion library.

**Mechanical checks**

- Run existing lint/build checks if available.
- Confirm there is no remaining `transition: all 360ms ease-in` in `src/styles/motion.css`.
- Confirm `@keyframes toast-enter` no longer animates `top`.
- Confirm all referenced tokens exist in the final CSS cascade.

**Runtime / feel checks to perform after implementation**

- Open a popover at slow animation playback and confirm it does not animate unrelated properties.
- If the popover is trigger-anchored, confirm it appears to grow from the trigger side when the origin variable is present.
- Trigger a toast and confirm it enters quickly without pushing layout during the animation.
- Toggle Reduced Motion and confirm the toast fades without vertical travel.

**Reduced Motion behavior**

- Popover: keep brief opacity/transform feedback at `80ms`.
- Toast: fade-only at `80ms`; no translate movement.

**Source-drift stop condition**

- Stop if `.popover` is actually used for centered modal content rather than anchored popovers.
- Stop if toast positioning depends on animating `top` for layout correctness.
- Stop if `--duration-fast`, `--duration-panel`, or `--ease-responsive` are absent or renamed in the real file.

---

### Plan 3 — Make sortable queue release motion interruptible and input-connected

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

- While dragging, the item should track the pointer directly.
- The dragged item/layer should move via `transform`, not a parent-level CSS variable that may invalidate unrelated descendants.
- Release-to-slot should preserve continuity with an interruptible settle.
- Reduced Motion should still allow direct pointer tracking, but the autonomous settle should be very short and non-bouncy.

**Project conventions**

- Use existing token direction where CSS is involved: transform-only motion, crisp durations, reduced path preserving feedback.
- Do not add a new dependency.
- If the existing `animateTo` helper already supports spring-style options, use it; otherwise stop and report that the helper needs an adapter rather than faking a spring with a long tween.

**Ordered steps**

1. Open the full `src/components/SortableQueue.tsx`.
2. Identify the exact element that visually moves during drag.
3. If the code already has a ref for the dragged row or drag layer, use that ref for pointer-move transforms.
4. Replace parent-level `queueRef.current?.style.setProperty("--drag-y", ...)` with a transform write on only the moving element/layer.
5. Track recent pointer velocity from the last two pointer move events.
6. Replace the fixed `duration: 400` release with:
   - default: spring-style settle `{ type: "spring", duration: 0.5, bounce: 0.2, velocity: <trackedYVelocity> }` if supported by `animateTo`;
   - reduced motion: `{ duration: 80 }` or the closest supported non-bouncy equivalent.
7. Clear any inline transform after the item has settled, if the current implementation expects layout to own the final position.

**Representative target shape**

```tsx
function onPointerMove(event: PointerEvent) {
  const nextY = event.clientY;
  updateDragVelocity(nextY, performance.now());
  draggedItemRef.current?.style.setProperty(
    "transform",
    `translate3d(0, ${nextY - dragStartY}px, 0)`
  );
}

function onPointerUp() {
  setDragging(false);

  const target = nearestSlot(currentY);
  animateTo(
    target,
    prefersReducedMotion()
      ? { duration: 80 }
      : { type: "spring", duration: 0.5, bounce: 0.2, velocity: dragVelocityY }
  );
}
```

**Hard boundaries**

- Do not change queue ordering logic.
- Do not change `nearestSlot` behavior.
- Do not alter keyboard sorting behavior, if present.
- Do not introduce a dependency for springs.
- Do not keep the fixed `400`ms settle if the helper supports an interruptible spring.
- Do not implement a custom animation loop unless the file already uses one.

**Mechanical checks**

- Run existing TypeScript/lint checks if available.
- Confirm no pointer-move path writes `--drag-y` to the queue root unless another non-motion purpose is found.
- Confirm release no longer uses `{ duration: 400 }` as the default settle path.
- Confirm reduced-motion detection is safe for the rendering environment used by the app.

**Runtime / feel checks to perform after implementation**

- Drag slowly and quickly; the item should remain visually attached to the pointer.
- Release near a slot; it should settle without a sluggish 400ms glide.
- Start a second drag before the previous settle visually completes; it should not jump back to an old start point.
- Toggle Reduced Motion; direct dragging still follows the pointer, while release settles quickly without bounce.

**Reduced Motion behavior**

- User-driven drag movement remains direct because it is input-controlled.
- Autonomous release animation uses `80ms` and no bounce.

**Source-drift stop condition**

- Stop if there is no per-item or drag-layer ref to target.
- Stop if `animateTo` does not support spring, velocity, or reduced-duration options.
- Stop if `--drag-y` is consumed by a broader layout algorithm rather than visual motion.

---

## 4. Recommended execution order

1. **Plan 1 — Command palette immediate**: highest throughput impact, smallest scope.
2. **Plan 2 — Popover/toast normalization**: fixes shared timing, easing, performance, and reduced-motion issues.
3. **Plan 3 — Sortable queue release**: highest interaction complexity; do after simpler token/CSS fixes.

## Explicitly unverified states

- Actual framework version, package scripts, and build tooling.
- Whether `.popover` is always trigger-anchored or sometimes modal-like.
- Whether command palette mounting/focus behavior depends on the animation class.
- Whether toast stacking/dismissal has additional CSS not shown.
- How `--drag-y` is consumed.
- Whether `animateTo` supports spring, velocity, or reduced-duration options.
- Actual computed styles, performance traces, accessibility tree, keyboard focus behavior, and user-perceived feel.
