## 1. Recon summary

**Stack signals**
- React/TSX components with CSS files.
- Global semantic motion tokens exist in `src/styles/motion.css`.
- Component-local CSS is used for buttons/toasts.
- Utility/arbitrary animation syntax appears in `CommandPalette.tsx`.

**Where motion currently lives**
- Global tokens and `.popover`: `src/styles/motion.css`
- Component-local animation: `src/components/toast.css`
- Inline utility animation: `src/components/CommandPalette.tsx`
- Imperative drag/snap behavior: `src/components/SortableQueue.tsx`
- Good local precedent: `src/components/Button.css`

**Existing conventions**
- Preferred tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Correct precedent uses `transform`, semantic duration/easing, and a Reduced Motion override to `80ms`.

**Product personality**
- Calm desktop operations console.
- Keyboard-heavy, repeated daily use.
- Motion should explain cause/effect and state continuity, not feel decorative or delay throughput.

**Frequency map**
- Very high frequency: button press, drag movement, queue sorting.
- High frequency: command palette open/close, popovers.
- Medium frequency: toasts.
- Lower tolerance for slow/ease-in motion on command, drag, and repeated overlay interactions.

**Evidence level**
- Static code excerpts only.
- No runtime, computed-style, trace, screen recording, accessibility-tree, device, or user validation was performed.

---

## 2. Vetted priority table

| Priority | Finding | Evidence | Risk | Recommended direction |
|---:|---|---|---|---|
| P0 | Popover uses broad, slow, non-token transition | `.popover { transition: all 360ms ease-in; }` | `all` may animate unintended/layout properties; `360ms ease-in` feels delayed for repeated ops use | Limit to `opacity, transform`; use existing tokens; add Reduced Motion |
| P0 | Drag/snap path uses hardcoded duration and high-frequency direct writes | `setProperty("--drag-y", ...)`; `animateTo(..., { duration: 400 })` | Direct manipulation path may feel laggy/inconsistent; no visible Reduced Motion policy | Keep drag immediate; snap with semantic duration; coalesce pointer updates; reduced snap duration |
| P1 | Command palette bypasses semantic tokens | `animate-[palette_420ms_ease-in_both]` | Slow command surface; arbitrary duration/easing; no visible Reduced Motion path | Move to named class/CSS using tokens; ensure open/closed states are explicit |
| P1 | Toast animates layout property | `top: -24px → 0`; `500ms ease-in` | Layout-affecting animation and slow entrance for operational feedback | Use `transform: translateY(...)` + `opacity`; tokenized duration/easing; reduced path |
| P2 | Reduced Motion exists only in local precedent | Button has media query; other snippets do not | Inconsistent accessibility behavior | Standardize reduced behavior across overlay, toast, command palette, queue snap |
| P2 | Motion governance is fragmented | Global CSS, local CSS, arbitrary utility, imperative JS | Drift risk and inconsistent feel | Use global semantic tokens and small component-local classes; avoid arbitrary one-off timings |

---

## 3. Implementation plans

### Plan A — Normalize transient overlay motion: popover + command palette

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
- Popovers and command palette should feel immediate, calm, and causally connected.
- Opening: subtle opacity + transform using `--duration-panel` and `--ease-responsive`.
- Closing: same properties, not slower than opening.
- Avoid `transition: all`.
- Avoid arbitrary one-off animation strings for core surfaces.
- Reduced Motion keeps feedback but compresses duration to `80ms`.

**Project conventions to preserve**
- Use existing semantic tokens from `src/styles/motion.css`.
- Follow the button precedent: transform-only motion, tokenized duration/easing, reduced duration.
- Do not introduce decorative spring/bounce behavior.
- Do not alter search result rendering or command behavior.

**Ordered steps**
1. In `src/styles/motion.css`, replace `.popover` transition with explicit properties:
   - `opacity`
   - `transform`
2. Keep `transform-origin: center` unless another anchored origin is already defined elsewhere.
3. Add stateful selectors for popover visibility if the app already uses attributes/classes for open state.
   - Preferred shape: `[data-open="true"]` / `[data-open="false"]`
   - Stop if current app uses a different state convention.
4. Replace `transition: all 360ms ease-in` with:
   - `transition-property: opacity, transform;`
   - `transition-duration: var(--duration-panel);`
   - `transition-timing-function: var(--ease-responsive);`
5. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class.
6. Add a stable class, for example `className="command-palette"` while preserving `data-open={open}`.
7. Define command palette motion in the appropriate existing stylesheet, preferably near other motion/component styles:
   - closed: slightly offset/scaled with lower opacity
   - open: `transform: translateY(0) scale(1); opacity: 1`
8. Add a Reduced Motion media query that sets duration to `80ms` and removes distance-heavy transform.

**Hard boundaries**
- Do not change focus management, search behavior, keyboard shortcuts, or result ordering in this plan.
- Do not add new animation libraries.
- Do not add new global tokens unless the existing three are insufficient after inspecting the real file.
- Do not convert the command palette to mount/unmount differently unless existing lifecycle requires it.

**Mechanical checks**
- Search for remaining `transition: all` in touched files.
- Search for remaining `animate-[palette_420ms_ease-in_both]`.
- Confirm all new durations use `var(--duration-fast)`, `var(--duration-panel)`, or `80ms` inside Reduced Motion.
- Confirm animated properties are limited to `opacity` and `transform`.

**Runtime/feel checks to perform later**
- Open/close command palette repeatedly via keyboard.
- Confirm it does not feel slower than task flow.
- Confirm focus ring remains visible during and after animation.
- Confirm popover opening preserves anchor causality.
- Confirm reduced-motion setting still gives clear state change without broad movement.

**Reduced Motion behavior**
- Duration: `80ms`.
- Keep opacity feedback.
- Remove or minimize translate/scale distance.
- Do not make the state change invisible.

**Source-drift stop condition**
- Stop before implementation if `.popover` has additional unseen state rules, if `palette` keyframes are defined elsewhere with required behavior, or if `CommandPalette` class composition is controlled by a shared utility not shown here.

---

### Plan B — Make toast entrance layout-safe and operationally faster

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
- Toast should appear promptly as feedback, not drift slowly into place.
- Animate compositor-friendly properties:
  - `transform`
  - `opacity`
- Use semantic timing and easing.
- Preserve clear feedback in Reduced Motion.

**Project conventions to preserve**
- Existing token names and button precedent.
- Calm, crisp, non-decorative motion.
- No change to toast content, role, timeout, stacking, or dismissal behavior in this plan.

**Ordered steps**
1. Replace keyframe `top` animation with `transform`.
2. Use an entrance offset equivalent in feel to the current `-24px`, but via:
   - `transform: translateY(-8px)` or `translateY(-12px)`
   - avoid the full `-24px` unless product feel requires a stronger entrance.
3. Replace `500ms ease-in` with tokenized timing:
   - likely `var(--duration-fast)` for a simple toast entrance
   - `var(--ease-responsive)` for responsive arrival
4. Keep `opacity: 0 → 1`.
5. Add Reduced Motion media query:
   - duration `80ms`
   - either no vertical offset or a very small one.
6. If toast exit animation exists elsewhere, align its properties and timing with the new entrance model.

**Hard boundaries**
- Do not change toast positioning model outside the animation.
- Do not alter notification semantics, live-region behavior, timers, stacking, or dismissal.
- Do not introduce long easing or bounce.
- Do not animate `top`, `left`, `right`, `bottom`, `height`, or `margin`.

**Mechanical checks**
- Confirm `@keyframes toast-enter` no longer contains `top`.
- Confirm `.toast` no longer uses `500ms ease-in`.
- Confirm animation uses existing duration/easing tokens.
- Confirm Reduced Motion override exists in `src/components/toast.css`.

**Runtime/feel checks to perform later**
- Trigger single toast and stacked toasts.
- Confirm entrance is noticeable but not attention-heavy.
- Confirm no layout jump is visible.
- Confirm repeated toasts do not feel sluggish.
- Confirm Reduced Motion mode still communicates arrival.

**Reduced Motion behavior**
- Use `80ms`.
- Prefer opacity-only or near-zero translate.
- Preserve feedback; do not silently appear without any perceptible state change unless required by user settings.

**Source-drift stop condition**
- Stop if toast positioning relies on the animated `top` value for final layout, if there are coordinated stack animations not shown, or if another stylesheet overrides `.toast` animation.

---

### Plan C — Stabilize sortable queue direct manipulation and snap motion

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
- During drag: movement should track pointer directly and immediately.
- On release: snap should be short, causal, and token-consistent.
- Reduced Motion should shorten snap while preserving positional feedback.
- High-frequency pointer movement should avoid unnecessary repeated style writes.

**Project conventions to preserve**
- Prefer transform-driven motion.
- Prefer semantic timing.
- Keep operations-console feel: no playful bounce, overshoot, or elastic effects.
- Do not change queue ordering rules.

**Ordered steps**
1. Inspect the CSS using `--drag-y`.
2. Confirm the variable drives `transform`, not layout properties.
   - If it drives `top`, `margin`, or layout, convert the rendered moving item to use `transform`.
3. Replace raw pointer-move style writes with requestAnimationFrame coalescing:
   - store latest pointer value
   - schedule one frame
   - write `--drag-y` once per animation frame
4. Prefer storing drag delta rather than absolute `clientY` if the CSS represents visual translation.
   - Current `event.clientY` is viewport-relative; verify whether downstream CSS expects absolute or relative input.
5. Replace hardcoded snap duration `400` with a semantic duration:
   - default snap: `240ms` / panel duration equivalent
   - if snap distance is tiny, consider `160ms`
6. Add a reduced-motion branch for snap duration:
   - `80ms`
7. Ensure pointer-up cancels any pending frame before or during snap handoff to avoid stale writes.
8. Ensure the same final slot calculation is preserved:
   - `nearestSlot(currentY)` should remain the source of final position unless a bug is found separately.

**Hard boundaries**
- Do not rewrite the drag-and-drop model.
- Do not change queue data mutation, item identity, nearest-slot math, or persistence behavior.
- Do not add physics unless already present in the animation utility.
- Do not introduce animation that delays the actual committed reorder.

**Mechanical checks**
- Search touched queue styles for layout-property animation.
- Confirm no hardcoded `400` remains for queue snap unless justified by a named constant.
- Confirm reduced-motion detection is centralized or at least consistent with CSS media query behavior.
- Confirm pointer-move writes are frame-coalesced.
- Confirm pending animation frame is cleaned up on pointer up/cancel/unmount.

**Runtime/feel checks to perform later**
- Drag slowly and quickly through multiple slots.
- Release near and far from target slot.
- Confirm no visible lag between pointer and item.
- Confirm snap does not block rapid follow-up actions.
- Confirm keyboard or non-pointer sorting path, if present, remains understandable.
- Confirm Reduced Motion shortens the snap but still makes the final placement clear.

**Reduced Motion behavior**
- Drag remains direct.
- Release snap duration becomes `80ms`.
- Avoid long travel animations; if distance is large, prefer immediate placement with a brief opacity/position confirmation rather than a slow glide.

**Source-drift stop condition**
- Stop if `animateTo` is a shared utility with global duration policy, if `--drag-y` participates in complex layout calculations, or if the queue already has unshown accessibility/keyboard drag behavior coupled to the current timing.

---

## 4. Recommended execution order

1. **Plan A first** — fixes the broadest convention drift: `transition: all`, arbitrary command palette timing, and missing Reduced Motion coverage for common overlays.
2. **Plan C second** — addresses the highest-frequency interaction path where latency and causality matter most.
3. **Plan B third** — contained, low-risk improvement for notification feedback and layout-safe animation.

## Explicitly unverified states

- Actual computed styles.
- Existence and contents of `palette` keyframes.
- Whether components mount/unmount or remain in DOM while closed.
- Focus management, focus trap behavior, and accessibility tree.
- Actual use of `--drag-y` in CSS.
- Behavior of `animateTo`.
- Toast stacking, live-region semantics, dismissal timing, and exit animation.
- Browser performance, frame rate, layout/recalc cost, and paint behavior.
- Device-specific feel, reduced-motion runtime behavior, and user testing outcomes.
