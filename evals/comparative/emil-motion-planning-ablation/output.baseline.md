## 1. Recon summary

**Stack signals**
- React/TSX components with CSS files.
- CSS custom properties for semantic motion tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Mixed motion implementation styles:
  - global CSS selector: `.popover`
  - component class animation: `animate-[palette_420ms_ease-in_both]`
  - component CSS keyframes: `toast-enter`
  - imperative pointer animation: `animateTo(...)`

**Where motion currently lives**
- `src/styles/motion.css`: shared duration/easing tokens plus `.popover`.
- `src/components/CommandPalette.tsx`: inline utility animation string.
- `src/components/toast.css`: keyframe animation using `top`.
- `src/components/SortableQueue.tsx`: pointer-driven custom property and hardcoded snap animation.
- `src/components/Button.css`: good local precedent for semantic tokens and Reduced Motion.

**Existing conventions**
- Prefer `transform` over layout properties.
- Prefer semantic duration/easing tokens over literal durations/easings.
- Reduced Motion should preserve feedback, not erase it.
- Existing local precedent uses:
  - `transition: transform var(--duration-fast) var(--ease-responsive);`
  - `@media (prefers-reduced-motion: reduce) { ... transition-duration: 80ms; }`

**Product personality**
- Calm desktop operations surface.
- Motion should clarify causality and state continuity.
- Motion should not slow high-frequency keyboard workflows.
- Avoid decorative, delayed, or “presentation” motion.

**Frequency map, based only on component roles**
- Very high frequency: buttons, command palette open/close, popovers.
- Medium frequency: toasts/status feedback.
- Episodic but interaction-sensitive: sortable queue drag/snap.
- Unknown: exact invocation counts, user paths, mount/unmount behavior, and whether these components appear in dense table workflows.

**Evidence level**
- Static code evidence only.
- No runtime, computed-style, animation trace, browser, device, accessibility-tree, screen recording, or user testing evidence.
- All performance and accessibility risks below are implementation risks, not observed runtime failures.

---

## 2. Priority table

| Priority | Finding | Static evidence | Risk | Target |
|---:|---|---|---|---|
| P0 | Motion system is inconsistent across files | `360ms ease-in`, `420ms ease-in`, `500ms ease-in`, `400`, plus tokenized button precedent | Operators may experience uneven timing and delayed feedback across frequent UI actions | Standardize around existing semantic tokens: `--duration-fast`, `--duration-panel`, `--ease-responsive`, with `80ms` Reduced Motion precedent |
| P0 | Reduced Motion exists only in the button evidence | `Button.css` has `prefers-reduced-motion`; other excerpts do not | Users requesting reduced motion may still receive long entrance/snap animations | Add Reduced Motion branches to palette, popover, toast, and sortable snap while preserving state feedback |
| P1 | `.popover` uses `transition: all` | `transition: all 360ms ease-in;` | Future style changes may accidentally animate layout, color, size, or shadow | Restrict to `transform, opacity` or the exact properties intentionally animated |
| P1 | Toast animates layout property `top` | `from { top: -24px; opacity: 0; } to { top: 0; opacity: 1; }` | Layout-position animation can be harder to reason about and less composited than transform-based feedback | Use `transform: translateY(...)` plus opacity |
| P1 | Command palette uses hardcoded arbitrary animation | `className="animate-[palette_420ms_ease-in_both]"` | Keyboard-heavy entry point may feel slower than the system’s own panel duration | Move to named class/data-state CSS using `--duration-panel` and responsive easing |
| P2 | Sortable queue snap is hardcoded and pointer updates are ungoverned | `setProperty("--drag-y", event.clientY)` and `animateTo(... { duration: 400 })` | Direct manipulation may feel detached if the dragged item does not track pointer/snap with system timing | Use transform-backed drag variables, requestAnimationFrame coalescing, tokenized snap duration, and Reduced Motion snap behavior |

---

## 3. Implementation plans

### Plan A — Normalize shared motion tokens and popover behavior

**Files and current excerpts**

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

**Target behavior**
- Popovers should open/close crisply using only intentional composited properties.
- Timing should align with the panel token, not a longer hardcoded duration.
- Reduced Motion should still show state change, but with shortened duration.

**Project conventions to preserve**
- Keep existing token names.
- Follow the button precedent: transform-based feedback, semantic duration/easing, `80ms` Reduced Motion.
- Do not introduce decorative bounce, overshoot, blur, or shadow animation.

**Ordered steps**
1. Replace `.popover` transition from `all 360ms ease-in` to explicit properties.
2. Use `var(--duration-panel)` and `var(--ease-responsive)`.
3. Add a Reduced Motion branch using `80ms`.
4. Do not change selector naming unless existing markup requires a different selector.
5. If open/closed states already exist elsewhere, only wire timing/easing to those states; do not invent new visibility logic without checking consumers.

**Implementation target shape**

```css
.popover {
  transform-origin: center;
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .popover {
    transition-duration: 80ms;
  }
}
```

**Hard boundaries**
- Do not use `transition: all`.
- Do not animate layout properties such as `top`, `left`, `width`, `height`, or margins.
- Do not remove visible focus styles.
- Do not change popover mounting, focus behavior, dismissal behavior, or z-index policy as part of this motion pass.

**Mechanical checks**
- Search for remaining `transition: all`.
- Search for hardcoded `360ms`, `ease-in`, and unrelated popover animation overrides.
- Run the closest available CSS/lint/type/build checks.

**Runtime/feel checks to perform later**
- Verify open and close both communicate state change.
- Verify keyboard-triggered popovers do not feel delayed.
- Verify Reduced Motion still shows a short state transition.
- Verify computed transition properties are limited to `transform` and `opacity`.

**Reduced Motion behavior**
- Preserve feedback with `80ms` transition duration.
- Avoid full removal unless a later accessibility review confirms instant state change is preferable.

**Source-drift stop condition**
- Stop before editing if `.popover` is no longer in `src/styles/motion.css`, if it already has state-specific transitions elsewhere, or if consumers depend on non-transform animated properties.

---

### Plan B — Convert command palette and toast to semantic, transform-based motion

**Files and current excerpts**

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
- Command palette: quick, calm state continuity for a high-frequency keyboard surface.
- Toast: transient feedback should enter without layout-position animation.
- Both should use semantic durations/easing and Reduced Motion.
- Motion should clarify “appeared from here / changed state” without delaying task flow.

**Project conventions to preserve**
- Use existing duration/easing tokens.
- Use transform/opacity.
- Keep existing component structure and `SearchResults`.
- Keep `data-open={open}` as the state hook unless current codebase already uses another state convention.

**Ordered steps**
1. Replace the command palette arbitrary animation class with a named class, for example `className="command-palette"`.
2. Move palette motion into CSS using `[data-open="true"]` and `[data-open="false"]` if the component remains mounted.
3. Use `opacity` and a small `translateY` or `scale` only; avoid large travel.
4. Set duration to `var(--duration-panel)` and easing to `var(--ease-responsive)`.
5. Convert toast keyframes from `top` to `transform: translateY(...)` plus opacity.
6. Set toast duration to `var(--duration-fast)` or `var(--duration-panel)` based on actual visibility need:
   - prefer `--duration-fast` if it is purely status feedback,
   - use `--duration-panel` only if toast carries important reviewable state.
7. Add Reduced Motion branches for both.

**Implementation target shape**

Command palette CSS target:

```css
.command-palette {
  opacity: 0;
  transform: translateY(-4px);
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}

.command-palette[data-open="true"] {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .command-palette {
    transition-duration: 80ms;
    transform: none;
  }
}
```

Toast CSS target:

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
  animation: toast-enter var(--duration-fast) var(--ease-responsive) forwards;
}

@media (prefers-reduced-motion: reduce) {
  .toast {
    animation-duration: 80ms;
  }
}
```

**Hard boundaries**
- Do not change command execution, search result rendering, focus placement, or dismissal rules.
- Do not add decorative scale if it makes text feel unstable.
- Do not animate `top` for toast.
- Do not claim the palette is accessible based only on this change; focus management is unverified.

**Mechanical checks**
- Search for `animate-[palette_420ms_ease-in_both]`.
- Search for `@keyframes toast-enter`.
- Search for `top:` inside toast animation.
- Search for remaining `500ms`, `420ms`, and `ease-in` in these files.
- Run lint/type/build checks available for the project.

**Runtime/feel checks to perform later**
- Open/close command palette repeatedly by keyboard.
- Confirm the palette appears responsive and does not block fast command entry.
- Trigger multiple toasts and verify motion does not stack into visual noise.
- Emulate Reduced Motion and confirm feedback remains perceptible but brief.

**Reduced Motion behavior**
- Palette: keep opacity feedback, remove travel, shorten to `80ms`.
- Toast: keep short fade/appearance feedback, shorten to `80ms`.

**Source-drift stop condition**
- Stop if the palette animation is defined elsewhere by a framework config, if `open=false` unmounts the component immediately, or if toast position relies on the `top` property for layout rather than only animation.

---

### Plan C — Make sortable queue drag/snap feel directly manipulated and tokenized

**File and current excerpt**

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
- During drag, the item should track the pointer directly with no transition lag.
- On release, snap should be short, causal, and aligned with system timing.
- Reduced Motion should remove prolonged travel while preserving final-slot feedback.
- Pointer updates should avoid excessive style writes when events fire rapidly.

**Project conventions to preserve**
- Use transform-backed custom properties where possible.
- Use existing duration/easing tokens or constants derived from them.
- Keep current queue ordering, nearest-slot calculation, and pointer capture behavior unchanged unless separately audited.

**Ordered steps**
1. Inspect the CSS consumer of `--drag-y` before editing.
2. Confirm whether `--drag-y` expects viewport `clientY` or a local delta.
3. If it is currently absolute viewport position, convert to a local drag delta only if all consumers can be updated safely.
4. Coalesce pointer style writes with `requestAnimationFrame`:
   - store latest pointer value,
   - write once per frame,
   - cancel pending frame on pointer up/unmount.
5. Ensure active dragging has no transition on the dragged transform.
6. Replace `duration: 400` with a token-aligned duration:
   - default snap: `240ms` equivalent to `--duration-panel`,
   - shorter snap for small distances if existing animation helper supports it,
   - Reduced Motion snap: `80ms` or immediate final transform plus brief state highlight.
7. If `animateTo` accepts easing, use the responsive easing equivalent.
8. If `animateTo` cannot consume CSS tokens, centralize numeric constants near the component with names matching the semantic tokens.

**Implementation target shape**

```tsx
const SNAP_DURATION_MS = 240;
const REDUCED_MOTION_SNAP_DURATION_MS = 80;

// Example only; final wiring depends on existing motion helper APIs.
function onPointerMove(event: PointerEvent) {
  latestDragY.current = event.clientY;

  if (dragFrame.current == null) {
    dragFrame.current = requestAnimationFrame(() => {
      dragFrame.current = null;
      queueRef.current?.style.setProperty("--drag-y", `${latestDragY.current}px`);
    });
  }
}

function onPointerUp() {
  setDragging(false);

  if (dragFrame.current != null) {
    cancelAnimationFrame(dragFrame.current);
    dragFrame.current = null;
  }

  animateTo(nearestSlot(currentY), {
    duration: prefersReducedMotion ? REDUCED_MOTION_SNAP_DURATION_MS : SNAP_DURATION_MS,
  });
}
```

**Hard boundaries**
- Do not change sorting semantics.
- Do not change `nearestSlot(currentY)` behavior without separate tests.
- Do not add inertial/fling behavior; it risks reducing precision in an operations tool.
- Do not use springy overshoot for queue placement unless later user testing validates it.
- Do not claim performance improvement without trace evidence.

**Mechanical checks**
- Find the CSS rule using `--drag-y`.
- Find all `animateTo(...)` calls with hardcoded durations.
- Check for cleanup of animation frames on pointer cancel/up/unmount.
- Run type checks and relevant interaction tests if present.

**Runtime/feel checks to perform later**
- Drag slowly and quickly; the item should remain attached to the pointer.
- Release near slot boundaries; snap should clearly resolve to the intended slot.
- Confirm no transition is applied while actively dragging.
- Emulate Reduced Motion; drag remains direct, release is brief or immediate.
- If performance tooling is available, check for avoidable layout work during pointer movement.

**Reduced Motion behavior**
- Keep direct pointer tracking.
- Shorten release snap to `80ms` or snap immediately while preserving a non-motion state cue such as selected/focused/placed styling.
- Avoid long travel animation after release.

**Source-drift stop condition**
- Stop if `--drag-y` is not transform-backed, if `animateTo` has changed signature, if pointer state is managed by another abstraction, or if the component already has a Reduced Motion hook elsewhere.

---

## 4. Recommended execution order

1. **Plan A first**: establishes the shared contract and removes the highest-risk global `transition: all`.
2. **Plan B second**: fixes high-frequency keyboard/transient feedback and removes layout-based toast motion.
3. **Plan C third**: requires more implementation inspection because pointer math, CSS consumers, and animation helper behavior are unverified.

## Explicitly unverified states

- Actual rendered CSS cascade and computed styles.
- Whether command palette remains mounted when `open=false`.
- Whether `.popover` has separate open/closed selectors elsewhere.
- Whether toast `top` is used for layout positioning outside animation.
- Whether `--drag-y` is consumed by `transform` or by layout-affecting properties.
- Whether `animateTo` supports easing, cancellation, or Reduced Motion configuration.
- Focus management, focus trap behavior, and accessibility-tree output.
- Frame timing, layout/repaint cost, and input latency during drag.
- Real Reduced Motion behavior in browser/device settings.
- User perception of “too fast,” “too slow,” or “clear enough” without runtime review or user testing.
