## 1) Recon summary

- **Stack signals**: React/TSX components plus plain CSS. Motion appears via CSS transitions, CSS keyframes, utility-style arbitrary animation class syntax, and imperative pointer/settle animation code.
- **Where motion lives**:
  - Global tokens and shared selectors: `src/styles/motion.css`
  - Component-local CSS: `src/components/toast.css`, `src/components/Button.css`
  - Component markup/classes: `src/components/CommandPalette.tsx`
  - Gesture code: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Tokens exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`.
  - Correct local precedent exists in `Button.css`: transform-only transition, tokenized duration/easing, subtle active scale, and a Reduced Motion override that preserves feedback.
- **Product personality**: calm desktop operations console. Motion should be crisp, causal, and quiet; it should not delay keyboard-heavy workflows.
- **Frequency map from evidence/product context**:
  - Very high: command palette, buttons, keyboard-triggered task switching.
  - High: popovers and sortable queue manipulation.
  - Occasional: toasts.
- **Evidence level**: static snippet audit only. No computed styles, runtime behavior, browser/device validation, accessibility-tree review, performance trace, or user test was performed.

## 2) Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose / duration / easing | `src/components/CommandPalette.tsx` | `animate-[palette_420ms_ease-in_both]` is long and ease-in on a keyboard-heavy surface. Static evidence indicates the command palette open state is animated; that conflicts with throughput-first usage. | Remove the open/close animation, or reduce to non-blocking feedback only if required by design. Prefer instant availability and visible focus continuity. |
| 2 | HIGH | Performance / easing / cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This is over the existing panel token, starts slowly, and may animate unintended properties. | Replace with explicit `transform`/`opacity` transitions using existing tokens: `var(--duration-panel)` or faster, `var(--ease-responsive)`. |
| 3 | MEDIUM | Physicality / origin | `src/styles/motion.css` | `.popover { transform-origin: center; }` is suspect for trigger-anchored popovers. If this selector is used for true centered modal content, this part is exempt. | Use a trigger-provided origin variable when available; otherwise keep center only for modal-like surfaces. |
| 4 | HIGH | Performance / accessibility | `src/components/toast.css` | Toast entry animates `top` for `500ms ease-in`. `top` is layout-affecting, duration is long for UI feedback, and the excerpt shows no Reduced Motion path. | Animate `transform` + `opacity` instead, shorten to `var(--duration-panel)`, use `var(--ease-responsive)`, and reduce movement under Reduced Motion. |
| 5 | MEDIUM | Gesture performance / interruptibility | `src/components/SortableQueue.tsx` | Pointer move writes `--drag-y` on `queueRef.current`; pointer up settles with fixed `duration: 400`. Static evidence suggests parent-level style invalidation risk and a long fixed settle for a drag interaction. | Drive `transform` directly on the dragged item, settle with a shorter tokenized transform animation or existing spring support, and add Reduced Motion handling. |
| 6 | MEDIUM | Accessibility / cohesion | Multiple excerpts except `Button.css` | The correct Reduced Motion precedent appears only in `Button.css`; other shown motion paths do not show equivalent handling. | Add local Reduced Motion behavior to each affected motion surface while preserving opacity/focus feedback. |

## 3) Implementation-ready plans

### Plan 1 — Tokenize and de-risk CSS popover/toast motion

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

- Popovers feel immediate and causal: explicit `transform`/`opacity` only, no `transition: all`, no `ease-in`.
- Toasts enter without layout animation: `translate3d`/`opacity`, shorter duration, no delayed ease-in start.
- Reduced Motion keeps feedback but removes travel.

**Project conventions**

- Reuse existing tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Follow the local precedent:

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

1. In `src/styles/motion.css`, change `.popover` from `transition: all 360ms ease-in;` to explicit properties:

```css
.popover {
  transform-origin: var(--popover-transform-origin, center);
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}
```

2. If the implementation already exposes a trigger-origin CSS variable for popovers, replace `--popover-transform-origin` with that existing variable. Do not invent a library-specific variable unless it already exists in the codebase.

3. In `src/components/toast.css`, replace `top` keyframes with transform/opacity keyframes:

```css
@keyframes toast-enter {
  from {
    transform: translate3d(0, -8px, 0);
    opacity: 0;
  }
  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
}

.toast {
  animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
}
```

4. Add Reduced Motion handling in `src/components/toast.css`:

```css
@media (prefers-reduced-motion: reduce) {
  @keyframes toast-enter {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .toast {
    animation-duration: 160ms;
  }
}
```

5. If redefining `@keyframes toast-enter` inside media queries conflicts with project CSS tooling, use a separate `toast-enter-reduced` keyframe instead.

**Hard boundaries**

- Do not change toast markup, queue logic, command palette logic, or unrelated component styles.
- Do not add dependencies.
- Do not remove focus styles or semantic state attributes.
- Do not convert all durations globally; only touch the shown selectors/keyframes.

**Mechanical checks**

- Search changed files and confirm:
  - No `transition: all` remains on `.popover`.
  - No `ease-in` remains in the edited popover/toast motion.
  - `toast-enter` no longer animates `top`.
  - A `prefers-reduced-motion: reduce` branch exists for toast motion.
- Run the project’s existing lint/type/style checks if available.

**Runtime / feel checks for executor**

- Open a popover slowly via DevTools animation playback if possible; confirm it does not appear to grow from the wrong spatial origin.
- Trigger several toasts; confirm entry starts promptly and does not visibly slide a large distance.
- Toggle Reduced Motion; confirm toast feedback remains visible through opacity but vertical travel is removed.

**Reduced Motion behavior**

- Toast: opacity-only, `160ms`.
- Popover: keep opacity/short transform unless existing design authority requires transform removal; if movement feels spatially distracting, reduce to opacity-only at `160ms`.

**Source-drift stop condition**

- Stop if `.popover` is actually used only for centered modal content, because `transform-origin: center` may be intentional.
- Stop if toast positioning depends on animated `top` for layout rather than visual entry; report the dependency instead of patching around it.

---

### Plan 2 — Remove command palette entrance delay

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

- Command palette content is available immediately when opened.
- Keyboard focus and result continuity do the feedback work; motion must not delay operator throughput.
- No `ease-in` or 420ms entrance animation on the palette wrapper.

**Project conventions**

- Use crisp semantic motion only where it preserves state continuity.
- Existing tokenized precedent favors `160ms` transform feedback for buttons, not long open animations.
- Reduced Motion should preserve feedback rather than remove all state indication.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class from the palette wrapper:

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div data-open={open}>
      <SearchResults />
    </div>
  );
}
```

2. If class composition is required in the real file, remove only `animate-[palette_420ms_ease-in_both]` and preserve unrelated classes.

3. Find the `palette` keyframes definition only if it becomes unused after this change. If it is used nowhere else, remove it in the same change; if it is shared, leave it and report the remaining usage.

4. Ensure focus-visible styling remains intact. Do not replace animation with blur, scale, or delayed opacity.

**Hard boundaries**

- Do not alter `SearchResults`.
- Do not change command execution, search state, keyboard handling, or open/close state ownership.
- Do not add a replacement animation unless product/design explicitly requires one.
- Do not remove `data-open={open}` if CSS or tests depend on it.

**Mechanical checks**

- Confirm `CommandPalette.tsx` no longer contains `animate-[palette_420ms_ease-in_both]`.
- Confirm no new `ease-in` command palette animation was introduced.
- Confirm TypeScript/JSX still parses.
- Run the closest existing typecheck/lint command if available.

**Runtime / feel checks for executor**

- Open the command palette repeatedly from the keyboard; confirm results are visible and usable immediately.
- Rapidly open/close; confirm there is no stale entrance animation continuing after state changes.
- Confirm focus remains visible on the intended input/result.

**Reduced Motion behavior**

- Same as default: no entrance motion.
- Preserve visible focus and open-state feedback through styling, not movement.

**Source-drift stop condition**

- Stop if the actual file no longer uses this class or if palette opening is controlled by a separate animation wrapper not shown here.
- Stop if tests or design comments explicitly document the 420ms animation as a required deliberate behavior; report that conflict.

---

### Plan 3 — Make sortable queue dragging direct, shorter, and reduced-motion aware

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

- During drag, only the dragged item moves via compositor-friendly `transform`.
- Pointer movement does not write a parent CSS variable that can affect the whole queue.
- On release, the item settles to `nearestSlot(currentY)` quickly and causally.
- Reduced Motion shortens or removes travel while preserving state feedback.

**Project conventions**

- Prefer transform-only motion, as shown by `Button.css`.
- Use existing duration/easing tokens where CSS is involved:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Do not introduce new motion libraries.

**Ordered steps**

1. Identify the actual ref for the dragged queue item. If only `queueRef` exists and there is no item-level ref or selector, add the smallest local ref needed for the active dragged element.

2. Replace the parent CSS-variable write:

```tsx
queueRef.current?.style.setProperty("--drag-y", `${event.clientY}px`);
```

with a direct transform write on the dragged item, using a delta rather than raw viewport `clientY` if the surrounding code tracks a drag origin:

```tsx
draggedItemRef.current?.style.setProperty(
  "transform",
  `translate3d(0, ${dragDeltaY}px, 0)`
);
```

3. If the existing code genuinely expects absolute `clientY`, first convert it to local queue/item coordinates. Do not pass raw viewport coordinates into `translateY`.

4. On pointer up, reduce fixed settle duration from `400` to a value no longer than `240ms` if `animateTo` is duration-based:

```tsx
animateTo(nearestSlot(currentY), { duration: 240 });
```

5. If `animateTo` already supports spring-style options and carries velocity, prefer the existing spring API with subtle bounce. Do not add a dependency to get spring behavior.

6. Add Reduced Motion branching using the project’s existing preference hook/helper if one exists. If none exists, use `window.matchMedia("(prefers-reduced-motion: reduce)")` behind a client-side guard in this component’s existing browser-only event path.

7. Under Reduced Motion, snap or use a very short settle, for example:

```tsx
animateTo(nearestSlot(currentY), { duration: 80 });
```

and avoid decorative overshoot/bounce.

**Hard boundaries**

- Do not rewrite sorting algorithms.
- Do not change queue data shape, item identity, persistence, or nearest-slot calculation.
- Do not add dependencies.
- Do not introduce global CSS variables for per-frame drag position.
- Do not remove keyboard accessibility or focus indication for sortable items.

**Mechanical checks**

- Confirm `onPointerMove` no longer writes `--drag-y` to `queueRef.current`.
- Confirm drag movement is applied as `transform` on the active item.
- Confirm release duration is not `400`.
- Confirm a Reduced Motion branch exists for release animation.
- Run the project’s closest typecheck/lint command if available.

**Runtime / feel checks for executor**

- Drag an item slowly; confirm the item tracks the pointer without visible offset jumps.
- Release near two slots; confirm it settles to the nearest slot without a long glide.
- Interrupt with rapid drags; confirm motion retargets cleanly and does not restart from an unrelated position.
- Toggle Reduced Motion; confirm the queue still communicates the final placement but avoids long travel or bounce.

**Reduced Motion behavior**

- Pointer tracking remains direct because it is user-controlled.
- Release animation shortens to `80ms` or snaps immediately if even short travel is distracting.
- Preserve focus/selection/placement feedback.

**Source-drift stop condition**

- Stop if `animateTo` is not a visual animation helper or if it does not target the dragged item’s transform.
- Stop if the queue intentionally uses `--drag-y` for multiple coordinated item transforms; report the dependency and propose a larger coordinated refactor instead.

## 4) Recommended execution order

1. **Plan 2 — Command palette**: highest throughput impact, smallest surface.
2. **Plan 1 — Popover/toast CSS**: removes broad `transition: all`, layout animation, long ease-in timing, and adds Reduced Motion coverage.
3. **Plan 3 — Sortable queue**: higher interaction risk; do after the simpler token/CSS corrections.

## Explicitly unverified states

- Actual package scripts, lint/typecheck commands, and CSS tooling behavior.
- Whether `.popover` is ever used for centered modal-like content.
- Whether trigger-origin CSS variables already exist.
- Whether `palette` keyframes are shared elsewhere.
- Whether `animateTo` supports easing, springs, velocity, cancellation, or Reduced Motion hooks.
- Actual computed durations/easings after cascade.
- Runtime feel, frame pacing, accessibility tree, keyboard focus behavior, and device/browser-specific performance.

Governance applied: frontend quality, reduced-motion/accessibility, and evidence-limited delivery discipline.
