## 1. Recon summary

- **Stack signals:** React/TSX components, CSS modules/global CSS, Tailwind-style arbitrary animation class in `CommandPalette`, imperative JS animation call in `SortableQueue`.
- **Where motion lives:** semantic tokens in `src/styles/motion.css`; component CSS in `toast.css` and `Button.css`; inline utility animation in `CommandPalette.tsx`; imperative gesture settle in `SortableQueue.tsx`.
- **Existing conventions:** `--duration-fast`, `--duration-panel`, `--ease-responsive`; correct local precedent animates only `transform`, uses semantic tokens, and shortens duration under `prefers-reduced-motion`.
- **Product personality:** calm, crisp, utilitarian desktop operations surface; motion should explain causality and preserve continuity, not add cinematic delay.
- **Frequency map:**  
  - High frequency: buttons, command palette, queue dragging.  
  - Medium frequency: popovers.  
  - Episodic: toasts.  
- **Evidence level:** static snippets only. No runtime feel, computed styles, trace, accessibility tree, browser, device, or user validation was performed.

## 2. Priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | `animate-[palette_420ms_ease-in_both]` | `src/components/CommandPalette.tsx` | Command palette uses a long, accelerating entry for a keyboard-heavy surface. Static evidence also shows no local Reduced Motion branch. | Move to named CSS using semantic duration/easing tokens; make open/closed states retargetable; reduce travel and duration under Reduced Motion. |
| P1 | `transition: all 360ms ease-in; transform-origin: center;` | `src/styles/motion.css` | Popover motion is broad, slow, accelerating, and center-origin by default. For anchored overlays this risks weak causality; static evidence does not prove actual placement. | Limit transitioned properties, use existing tokens, and make origin trigger-aware where the component can supply placement. |
| P1 | `animateTo(nearestSlot(currentY), { duration: 400 })` | `src/components/SortableQueue.tsx` | Drag settle appears fixed-duration and does not show velocity handoff, pointer capture, grab offset, or Reduced Motion behavior. Static evidence cannot prove gesture feel, but this is the highest-risk direct-manipulation path. | Preserve current target semantics, add measured release velocity and presentation-value settle; add Reduced Motion non-elastic settle. |
| P2 | `@keyframes` changes `top`; `.toast { animation: ... 500ms ease-in }` | `src/components/toast.css` | Toast enter animates layout-position property with long ease-in timing and no shown Reduced Motion path. Static evidence cannot prove dropped frames. | Animate `transform` + `opacity`, shorten to panel/fast token range, and reduce vertical travel under Reduced Motion. |
| P2 | Multiple hard-coded durations/easings: `360ms ease-in`, `420ms ease-in`, `500ms ease-in`, `400` | Multiple | Motion language is fragmented despite existing semantic tokens and a correct local precedent. | Route transient UI through the existing motion tokens; add only narrowly scoped new tokens if current tokens are insufficient. |
| P3 | Correct precedent exists: transform-only button with Reduced Motion duration | `src/components/Button.css` | Good local pattern is not propagated to overlays, toast, and gesture settle. | Use the button pattern as the minimum convention: explicit animated properties, semantic timing, Reduced Motion feedback retained. |

## 3. Implementation plans

### Plan 1 — Normalize command palette and popover transient motion

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

- Command palette opens immediately enough for keyboard-heavy use: short opacity/transform transition, no long accelerating delay.
- Popovers animate only properties that communicate entrance/exit, typically `opacity` and `transform`.
- Anchored overlays should originate from the trigger or placement when that information exists; centered origin is acceptable only for genuinely centered surfaces.
- Reduced Motion keeps state feedback through opacity/color/static state, with little or no spatial travel.

**Project conventions**

- Use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the local precedent from `src/components/Button.css`: explicit property transition, transform-based feedback, Reduced Motion override.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` broad transition with explicit properties, for example:
   - `transition-property: opacity, transform;`
   - `transition-duration: var(--duration-panel);`
   - `transition-timing-function: var(--ease-responsive);`
2. Do not keep `transition: all`; if other properties currently rely on it, split them into explicit transitions before removal.
3. Change `.popover` origin from unconditional `center` to a placement-aware value only if the component already exposes placement/origin data. If not, keep behavior stable and add a narrow variable contract such as `transform-origin: var(--popover-origin, center);`.
4. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class and use a named class or data-state styles controlled by `data-open={open}`.
5. Define command palette styles in the existing relevant stylesheet location, using `opacity` plus small `translateY`/scale if needed; avoid keyframe restart unless mount/unmount lifecycle requires it.
6. Add `@media (prefers-reduced-motion: reduce)` for both popover and palette: duration around the existing reduced precedent, with spatial movement removed or reduced to a minimal transform.

**Hard boundaries**

- Do not redesign command palette layout, search behavior, focus management, or result rendering.
- Do not add a motion library for this plan.
- Do not introduce new global animation tokens unless existing tokens cannot express the required distinction.
- Do not claim trigger-relative origin is fixed until the actual popover placement API is inspected.

**Mechanical checks**

- Run the project’s existing type check for the TSX change.
- Run the project’s existing CSS/lint/build gate.
- Grep/check that `CommandPalette.tsx` no longer contains `animate-[palette_420ms_ease-in_both]`.
- Grep/check that `.popover` no longer uses `transition: all`.

**Runtime/feel checks to perform later**

- Open/close the command palette repeatedly via keyboard; acceptance: no perceived delay before results become available, no restart jump on rapid toggle.
- Open popovers from each supported placement; acceptance: motion appears anchored to the trigger where placement data exists.
- Check interrupted open/close sequences; acceptance: transition retargets from current visual state.

**Reduced Motion behavior**

- Palette/popover should still communicate open/closed state through opacity or immediate visibility.
- Remove large travel and avoid delayed keyframe entrance.
- Keep focus indicators visible and unaffected by motion reduction.

**Source-drift stop condition**

- Stop before editing if `CommandPalette` no longer renders the shown `data-open` wrapper, if `.popover` is no longer defined in `src/styles/motion.css`, or if motion tokens are renamed/removed.

---

### Plan 2 — Convert toast entrance from layout animation to tokenized transform feedback

**Current excerpt**

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

- Toasts enter briskly without layout-position animation.
- Motion communicates arrival from the notification region but does not feel like a slow banner slide.
- Repeated toasts should not depend on a long keyframe that restarts from an unrelated position.
- Reduced Motion preserves visibility feedback without vertical travel.

**Project conventions**

- Prefer `transform` and `opacity`.
- Use `--duration-panel` or `--duration-fast`; avoid hard-coded `500ms ease-in`.
- Match the existing reduced-duration precedent from `Button.css`.

**Ordered steps**

1. In `src/components/toast.css`, change `@keyframes toast-enter` from `top` animation to `transform` and `opacity`, for example:
   - `from { transform: translateY(-8px); opacity: 0; }`
   - `to { transform: translateY(0); opacity: 1; }`
2. Change `.toast` timing to a semantic token:
   - `animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;`
3. Confirm the toast’s static positioning still owns `top`/placement outside the animation. If `top` is only present in the keyframe, add stable positioning separately before removing animated `top`.
4. Add `@media (prefers-reduced-motion: reduce)`:
   - reduce duration to the local reduced precedent,
   - remove or nearly remove `translateY`,
   - keep opacity feedback.
5. If toast exit animation exists elsewhere, align it with the same property set and Reduced Motion rule; do not invent an exit path if none exists.

**Hard boundaries**

- Do not change toast copy, stacking, dismissal timing, z-index, or notification semantics.
- Do not claim frame-rate improvement without trace evidence.
- Do not add `will-change` unless later profiling proves it helps.

**Mechanical checks**

- Run existing CSS/lint/build gate.
- Static check: `toast-enter` should no longer animate `top`.
- Static check: `.toast` should no longer contain `500ms ease-in`.

**Runtime/feel checks to perform later**

- Trigger single and multiple toasts; acceptance: toast appears promptly, from a short travel distance, without obvious layout jump.
- Trigger toasts while other page content is busy; acceptance requires browser observation or trace, not static inference.
- Verify toast does not block keyboard workflow or focus visibility.

**Reduced Motion behavior**

- Toast appears with short opacity feedback.
- Vertical travel is removed or reduced to a barely perceptible amount.
- State remains understandable; toast must not become invisible until animation completes.

**Source-drift stop condition**

- Stop before editing if toast positioning has moved out of `src/components/toast.css`, if `toast-enter` is already replaced, or if the toast component relies on animated `top` for stacking logic.

---

### Plan 3 — Make queue drag settle interruptible and velocity-aware without changing slot semantics

**Current excerpt**

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

- While dragging, the item tracks the pointer in a clear coordinate space without jumping.
- Release settlement starts from the current on-screen value and carries measured release velocity.
- Existing target selection, `nearestSlot(currentY)`, is preserved unless product authority explicitly approves momentum-based target selection.
- Reduced Motion removes elastic/large travel while retaining deterministic slot placement feedback.

**Project conventions**

- Direct manipulation may use imperative animation, but it must not fight CSS transform ownership.
- Use semantic duration/easing where fixed timing remains necessary.
- Preserve calm operations-console motion: no playful bounce unless already authorized.

**Ordered steps**

1. Inspect the full `SortableQueue.tsx` before editing to identify:
   - coordinate space of `currentY`,
   - how `--drag-y` is consumed,
   - whether the dragged element uses `transform`, `top`, or another property,
   - whether pointer capture and grab offset already exist outside the excerpt.
2. On pointer down/start, capture:
   - pointer id,
   - starting pointer `clientY`,
   - element presentation `y`,
   - grab offset,
   - short movement history with monotonic timestamps.
3. On pointer move, update drag position in component-local CSS pixels, not raw viewport `clientY`, unless existing CSS explicitly expects viewport coordinates.
4. Ensure only one owner composes transforms. If press/drag/settle all write `transform`, split wrapper layers or compose a single transform string.
5. On pointer up, compute release velocity in CSS px/s from recent samples.
6. Keep current target rule initially:
   - `target = nearestSlot(currentY)` or the equivalent current semantic.
   - Feed measured velocity into `animateTo` if the API supports it.
   - If the API does not support velocity, replace or wrap it with a spring/WAAPI mechanism that can start from current presentation value and velocity.
7. Add an explicit authorization checkpoint before momentum target selection:
   - compute bounded projected endpoint only as an experiment,
   - do not use it to choose a slot unless approved by product/runtime evidence.
8. Add Reduced Motion branch:
   - no overshoot,
   - shorter settle,
   - deterministic transform/position update,
   - same final slot.

**Hard boundaries**

- Do not change queue ordering rules, nearest-slot semantics, persistence, selection, or keyboard behavior.
- Do not add a new animation dependency unless existing primitives cannot read current value and accept initial velocity.
- Do not replace slot targeting with momentum projection by default.
- Do not claim touch/device feel correctness without later runtime validation.

**Mechanical checks**

- Run existing type check.
- Run existing unit tests covering queue reorder behavior, if present.
- Add or update tests only if the project already has a suitable test layer for reorder math; otherwise keep this as implementation plus runtime validation.
- Static check that release velocity is measured with units documented in code comments or helper names.
- Static check that Reduced Motion branch exists for the settle path.

**Runtime/feel checks to perform later**

- Drag slowly, release near slot boundary; acceptance: current nearest-slot behavior is preserved.
- Flick and release; acceptance: item settles from current visual position without a jump and without input lockout.
- Interrupt a settling item by grabbing it again; acceptance: no snap back to old logical target.
- Drag outside original bounds; acceptance depends on pointer capture or equivalent behavior.
- Measure under realistic list size before claiming performance quality.

**Reduced Motion behavior**

- Item still lands in the correct slot.
- Remove bounce/elasticity and large secondary motion.
- Keep immediate state feedback through position change, selection/drag state styling, or other non-vestibular cue.

**Source-drift stop condition**

- Stop before editing if `animateTo` has a different signature than assumed, if `nearestSlot(currentY)` is no longer the release target, if `--drag-y` is not used for visual drag position, or if another module owns drag physics.

## 4. Recommended execution order

1. **Plan 3: SortableQueue** — highest interaction risk because direct manipulation needs continuity, interruption, and velocity handling.
2. **Plan 1: Command palette + popover** — high-frequency keyboard/overlay motion and broad `transition: all` cleanup.
3. **Plan 2: Toast** — bounded but worthwhile cleanup from layout-position animation to transform/opacity.

## Explicitly unverified states

- Actual frame rate, paint/layout cost, compositor behavior, and style recalculation scope.
- Real keyboard throughput impact of the command palette animation.
- Popover placement/origin behavior and whether `center` is currently intentional for some surfaces.
- Toast stacking, exit animation, and whether animated `top` is coupled to layout logic.
- Sortable queue pointer capture, grab offset, current-value interruption, transform ownership, and animation API capabilities outside the excerpt.
- Actual Reduced Motion behavior in browser settings.
- Accessibility-tree behavior, focus order, focus visibility during transitions, and screen-reader timing.
