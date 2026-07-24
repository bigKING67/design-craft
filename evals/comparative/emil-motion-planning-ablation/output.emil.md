## 1) Recon summary

- **Stack signals:** React/TSX components plus CSS; motion is expressed through CSS tokens, component CSS, utility-style animation classes, and imperative JS gesture code. No motion library is evidenced.
- **Where motion lives:**  
  - Global tokens: `src/styles/motion.css`  
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`  
  - Inline utility animation: `src/components/CommandPalette.tsx`  
  - Gesture handler / imperative animation: `src/components/SortableQueue.tsx`
- **Existing conventions:** Semantic tokens already exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`. `Button.css` is the strongest local precedent: transform-only feedback, tokenized duration/easing, and `prefers-reduced-motion` shortening to `80ms`.
- **Product personality:** Calm, crisp, task-throughput-oriented desktop operations UI. Motion should clarify causality and feedback, not add delay or ornament.
- **Frequency map:**  
  - Very high: command palette, buttons, keyboard-triggered actions.  
  - High/bursty: sortable queue dragging.  
  - Medium: popovers.  
  - Occasional: toasts.
- **Evidence level:** Static snippets only. No runtime lifecycle, computed styles, screen recording, trace, accessibility tree, device, or browser validation was performed.

## 2) Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / frequency / easing | `src/components/CommandPalette.tsx` | Command palette declares `animate-[palette_420ms_ease-in_both]`. For a keyboard-heavy, high-frequency surface, this is both slow and delayed by `ease-in`; it also bypasses existing motion tokens. | Remove command-palette entrance motion or reduce to effectively immediate non-spatial feedback; do not animate keyboard throughput paths. |
| 2 | HIGH | Performance / easing / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. `all` can animate unintended properties, `360ms` exceeds the stated crisp UI budget, and `ease-in` delays response. | Restrict to `transform, opacity`; use existing semantic duration/easing tokens; add reduced-motion handling. |
| 3 | HIGH | Performance / accessibility | `src/components/toast.css` | Toast entrance animates `top` for `500ms ease-in`. `top` is layout-affecting, `500ms` is slow for operational feedback, and no reduced-motion path is shown. | Animate `transform` + `opacity` instead; shorten to tokenized panel duration; reduce motion to opacity-only `80ms`. |
| 4 | HIGH | Gesture / interruptibility / performance | `src/components/SortableQueue.tsx` | Drag updates write `--drag-y` on `queueRef`; release uses fixed `duration: 400`. Static evidence does not show direct element transforms, velocity preservation, or reduced-motion branching. | During drag, update the dragged element’s transform directly; on release, use a shorter token-aligned settle or existing spring-capable helper; branch for reduced motion. |
| 5 | MEDIUM | Cohesion / tokens | Multiple snippets | Hardcoded `360ms`, `420ms`, `500ms`, `400`, `ease-in`, and utility animation syntax diverge from the existing semantic token precedent. | Consolidate motion values around existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`; avoid parallel one-off timings. |

## 3) Implementation-ready plans

### Plan 1 — Tokenize and de-layout popover/toast motion

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

- Popovers and toasts should feel immediate, crisp, and operational.
- No `transition: all`.
- No animated `top`.
- Use existing semantic tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Reduced Motion keeps feedback but removes spatial travel where possible.

**Project conventions**

Use `src/components/Button.css` as the local precedent:

```css
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

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
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}
```

2. In the same file, add Reduced Motion handling:

```css
@media (prefers-reduced-motion: reduce) {
  .popover {
    transition-duration: 80ms;
  }
}
```

3. In `src/components/toast.css`, replace the layout-moving keyframes:

```css
@keyframes toast-enter {
  from { transform: translateY(-24px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.toast {
  animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
}
```

4. Add an opacity-only reduced-motion keyframe:

```css
@keyframes toast-enter-reduced {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .toast {
    animation-name: toast-enter-reduced;
    animation-duration: 80ms;
    animation-timing-function: var(--ease-responsive);
  }
}
```

**Hard boundaries**

- Do not change toast markup, queue behavior, command palette behavior, or button styles.
- Do not add new dependencies.
- Do not introduce new duration/easing tokens unless the existing files already require token expansion.
- Do not change `transform-origin: center` unless the actual popover implementation exposes trigger-origin data; if so, use the existing local origin variable only.

**Mechanical checks**

- Search for remaining bad patterns in these files:
  - `transition: all`
  - `500ms ease-in`
  - `360ms ease-in`
  - `from { top:`
- Run the existing project lint/typecheck/build commands if present; do not add scripts.

**Runtime / feel checks for executor**

- Trigger a toast and confirm it enters via vertical transform + opacity, not by reflowing from `top`.
- Trigger a popover and confirm it feels responsive, not delayed at the start.
- At slow animation playback, confirm no unrelated properties animate on `.popover`.
- Toggle Reduced Motion and confirm toast movement is removed while opacity feedback remains.

**Reduced Motion behavior**

- Popover transition duration becomes `80ms`.
- Toast uses opacity-only `80ms`; no `translateY`.

**Source-drift stop condition**

Stop if either current excerpt is no longer present or if toast/popover state styles depend on `top` as a positioning contract rather than only as an entrance animation.

---

### Plan 2 — Remove high-frequency command palette entrance animation

**File / current excerpt**

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

- Opening/closing the command palette should not impose a `420ms` animated delay on a keyboard-heavy workflow.
- Preserve state continuity through immediate visibility, focus, selection highlight, and content stability rather than spatial entrance motion.
- No `ease-in` animation on this high-frequency path.

**Project conventions**

- For frequent feedback, prefer the local button precedent: short, transform-only, tokenized motion.
- For command palette specifically, target no entrance motion rather than merely a nicer curve.

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

2. Search for the `palette` keyframes or utility reference:
   - `animate-[palette_420ms_ease-in_both]`
   - `@keyframes palette`
   - `palette_420ms`
3. If the palette keyframe is used only by `CommandPalette`, remove the unused keyframe definition.
4. If the keyframe is shared elsewhere, do not remove it; only remove this command-palette usage.

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change keyboard handling, focus management, search behavior, or open-state semantics.
- Do not replace the removed animation with another entrance animation.
- Do not add a motion library or new CSS token.

**Mechanical checks**

- Confirm no remaining `animate-[palette_420ms_ease-in_both]`.
- Confirm `CommandPalette` still renders `data-open={open}`.
- Run existing typecheck/lint commands if available.

**Runtime / feel checks for executor**

- Open the command palette repeatedly from the keyboard.
- Confirm it appears immediately and does not feel like it waits before becoming usable.
- Confirm focus indication and result selection remain visible.
- Toggle Reduced Motion and confirm behavior is equivalent, not broken or hidden.

**Reduced Motion behavior**

- Same as default: no entrance motion. Feedback should come from visible focus/selection/state, not movement.

**Source-drift stop condition**

Stop if `CommandPalette` no longer contains the exact arbitrary animation class or if the component’s visibility depends on that class for correctness rather than decoration.

---

### Plan 3 — Make sortable drag direct and shorten release settling

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

- Dragging should track the pointer directly with no parent-wide style-variable churn.
- Release should settle crisply and remain interruptible-feeling.
- Avoid a fixed `400ms` settle for an operational queue.
- Reduced Motion should shorten or eliminate the animated settle while preserving the final position update.

**Project conventions**

- Match the existing token values:
  - Fast feedback: `160ms`
  - Panel-scale movement: `240ms`
  - Responsive curve: `cubic-bezier(0.23, 1, 0.32, 1)`
- Do not add dependencies.

**Ordered steps**

1. Inspect this component for the dragged item element/ref and for where `--drag-y` is consumed.
2. If a dragged item element/ref exists, update that element directly during pointer move:

```tsx
function onPointerMove(event: PointerEvent) {
  draggedItemRef.current?.style.setProperty(
    "transform",
    `translate3d(0, ${event.clientY}px, 0)`
  );
}
```

3. If the component currently needs a delta rather than absolute viewport `clientY`, use the existing drag-start/current-position variables to write the same final transform as `translate3d(0, ${deltaY}px, 0)`.
4. Replace the fixed release duration with a token-aligned duration:

```tsx
function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), {
    duration: prefersReducedMotion ? 80 : 240,
    easing: "cubic-bezier(0.23, 1, 0.32, 1)",
  });
}
```

5. If the existing `animateTo` helper already supports spring-style settling and velocity input, prefer that existing API instead of the duration/easing object:

```tsx
animateTo(nearestSlot(currentY), {
  type: "spring",
  duration: 0.5,
  bounce: 0.2,
  velocity: currentVelocity,
});
```

6. If `prefersReducedMotion` is not already available in this component, derive it without a new dependency using `window.matchMedia("(prefers-reduced-motion: reduce)")`, guarded for environments where `window` is unavailable.

**Hard boundaries**

- Do not rewrite the sorting algorithm.
- Do not change `nearestSlot(currentY)` behavior.
- Do not add a drag-and-drop library.
- Do not drive transforms through a parent CSS variable if a direct dragged element ref exists.
- If no dragged item ref exists and adding one would require restructuring the component tree, stop and report instead of improvising.

**Mechanical checks**

- Confirm no remaining parent write of `queueRef.current?.style.setProperty("--drag-y", ...)` for active drag motion.
- Confirm no remaining `{ duration: 400 }` release settle in `SortableQueue`.
- Confirm TypeScript accepts the `animateTo` options actually supported by the local helper.
- Run existing typecheck/lint commands if available.

**Runtime / feel checks for executor**

- Drag an item slowly and quickly; confirm the item remains visually attached to the pointer.
- Release near a slot and confirm the settle is crisp, not leisurely.
- Interrupt by starting another drag soon after release; confirm the UI does not visibly restart from an unrelated position.
- Toggle Reduced Motion and confirm the item still reaches the correct slot with minimal movement.

**Reduced Motion behavior**

- During direct dragging, pointer tracking remains direct because it is user-controlled.
- On release, settle duration becomes `80ms` or immediate if the local animation helper cannot produce a short non-spatial settle safely.

**Source-drift stop condition**

Stop if `animateTo` does not accept duration/easing or spring options, if `--drag-y` is part of layout calculations rather than only visual translation, or if the dragged element cannot be identified without restructuring.

## 4) Recommended execution order

1. **Plan 1:** Fixes shared CSS motion problems and creates the clearest local pattern for crisp, tokenized, reduced-motion-safe behavior.
2. **Plan 2:** Removes the highest-frequency delay from the keyboard-heavy command path.
3. **Plan 3:** Improves the most interaction-sensitive gesture path; execute after inspecting the actual `animateTo` API and drag DOM structure.

## Explicitly unverified states

- Actual component mount/unmount lifecycle.
- Whether `.popover` is always trigger-anchored or sometimes modal-like.
- Whether `palette` keyframes exist elsewhere.
- How `--drag-y` is consumed.
- `animateTo` API shape and whether it supports easing, spring, or velocity.
- Computed styles, frame rate, layout cost, focus behavior, accessibility tree, and Reduced Motion behavior at runtime.
- Any browser, device, trace, screen-recording, or user-test result.
