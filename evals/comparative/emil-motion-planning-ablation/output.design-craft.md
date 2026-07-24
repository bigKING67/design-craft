One-sentence diagnosis: the snippets show a useful motion-token seed and one good button precedent, but several high-frequency/causal interactions bypass those conventions with slow `ease-in`, hard-coded keyframes, broad property ownership, layout-position animation, and incomplete Reduced Motion evidence.

## 1. Recon summary

- **Stack signals:** React/TSX components, CSS custom properties, global/component CSS, Tailwind-style arbitrary animation utility, PointerEvent-driven drag, and an unknown `animateTo` helper.
- **Where motion lives:** `src/styles/motion.css`, component CSS keyframes, TSX utility classes, and pointer gesture handlers.
- **Existing conventions:** semantic tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`; `Button.css` is the correct local precedent: transform-only transition, tokenized timing/easing, Reduced Motion duration shortened to `80ms`.
- **Product personality:** calm desktop operations console; motion should be crisp, causal, low-latency, and non-decorative.
- **Frequency map:**
  - Very high: command palette, keyboard-triggered overlays, button press feedback.
  - High/medium: sortable queue drag/reorder.
  - Medium: popovers.
  - Occasional: toasts.
- **Evidence level:** static snippets only. No runtime feel, computed styles, frame traces, accessibility tree, browser/device validation, or actual package-script discovery.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
| --- | --- | --- | --- | --- |
| P1 | `animate-[palette_420ms_ease-in_both]` | `src/components/CommandPalette.tsx` | High-frequency keyboard surface uses a hard-coded 420ms `ease-in` keyframe; this likely delays perceived response and bypasses tokens. Runtime feel unverified. | Replace with tokenized opacity/transform transition using `--duration-fast` + `--ease-responsive`; Reduced Motion: `80ms`, no travel. |
| P1 | `animateTo(nearestSlot(currentY), { duration: 400 })` | `src/components/SortableQueue.tsx` | Direct manipulation settle is shown as fixed-duration with no visible velocity handoff, interruption-from-presentation-value, or Reduced Motion branch in the excerpt. | Preserve `nearestSlot` semantics, but measure release velocity in CSS px/s and pass it into an interruptible settle if the existing API supports it. |
| P1 | Reduced Motion only shown in `Button.css` | Multiple excerpts | `popover`, command palette, toast, and queue snippets show meaningful movement without a visible Reduced Motion path, conflicting with the stated authority within supplied evidence. | Add per-surface Reduced Motion behavior: remove/reduce spatial travel while preserving opacity/color/state feedback. |
| P2 | `transition: all 360ms ease-in` | `src/styles/motion.css` | Popover owns all transitionable properties, runs longer than existing tokens, and uses `ease-in`. `transform-origin: center` may be wrong for anchored popovers, but anchoring is unverified. | Restrict to `opacity, transform`; use token duration/easing; expose trigger-relative origin variable with safe fallback. |
| P2 | `top` keyframe, `500ms ease-in` | `src/components/toast.css` | Toast entrance animates a layout-position property and uses slow `ease-in`; static evidence cannot prove jank, but this is a clear performance/feel risk. | Animate `transform` + `opacity`; use `--duration-panel` or shorter token; add Reduced Motion opacity-only variant. |
| P3 | Mixed hard-coded durations: `360/420/500/400ms` | Supplied snippets | Motion vocabulary is fragmented despite available semantic tokens. | Normalize to existing tokens first; introduce new tokens only after repeated need is proven. |

## 3. Implementation plans

### Plan 1 — Make command palette motion immediate, tokenized, and Reduced Motion-safe

**Current excerpt**

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

- Opening/closing feels immediate for keyboard use.
- Motion uses opacity plus very small vertical transform only.
- Duration/easing use existing conventions: `--duration-fast`, `--ease-responsive`.
- Reduced Motion keeps state feedback but removes travel and shortens to `80ms`.
- No keyframe restart dependency for repeated open/close.

**Project conventions**

- Follow `Button.css`: transform-only transition, semantic duration/easing, `prefers-reduced-motion` duration of `80ms`.
- Do not add decorative bounce or cinematic timing.

**Ordered steps**

1. Confirm whether the `palette` keyframe exists elsewhere and whether the palette remains mounted when `open=false`.
2. Replace the arbitrary animation class with a state-driven transition.
3. If Tailwind data variants and `motion-reduce` utilities are available, use tokenized utilities directly, e.g. conceptually:
   ```tsx
   className="
     transition-[opacity,transform]
     duration-[var(--duration-fast)]
     ease-[var(--ease-responsive)]
     data-[open=true]:opacity-100 data-[open=true]:translate-y-0
     data-[open=false]:opacity-0 data-[open=false]:-translate-y-1
     motion-reduce:duration-[80ms] motion-reduce:translate-y-0
   "
   ```
4. If those utilities are not supported, move the same behavior into the nearest existing command-palette stylesheet; do not place component-specific selectors in global CSS unless that is already the project convention.
5. Remove or stop referencing the old `palette_420ms_ease-in_both` animation only after confirming no other component depends on it.

**Hard boundaries**

- Do not change search behavior, focus behavior, result rendering, keyboard shortcuts, mount/unmount semantics, or data fetching.
- Do not add a motion dependency.
- Do not introduce new duration/easing tokens unless existing tokens cannot express the behavior.

**Mechanical checks**

- Run the project’s existing type-check/lint/build gates after discovering package scripts.
- If no such scripts exist, record that rather than inventing script names.
- Search for remaining `palette_420ms` / `animate-[palette` references.

**Runtime/feel checks to perform later, not claimed here**

- Open/close repeatedly via keyboard shortcut.
- Type immediately after opening; palette should not feel delayed.
- Interrupt open with close and close with open; no visual reset/jump.
- Verify closed state does not leave hidden interactive content focusable, if the component remains mounted.

**Reduced Motion behavior**

- Keep opacity/state feedback.
- Remove vertical travel.
- Use `80ms` duration.

**Source-drift stop condition**

- Stop before editing if `CommandPalette.tsx` no longer contains the supplied class, if `open` no longer maps to visual state, or if the project has a newer command-palette motion abstraction.

---

### Plan 2 — Normalize popover and toast motion to transform/opacity plus semantic tokens

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

- Popovers respond crisply without owning unrelated properties.
- Toasts enter with compositor-friendly movement and opacity, not animated `top`.
- Both use existing semantic tokens and a Reduced Motion path.
- Popover origin can be trigger-relative when anchored, while preserving a safe fallback for genuinely centered overlays.

**Project conventions**

- Prefer `transform` and `opacity`.
- Use `--duration-fast` for small overlays/popovers and `--duration-panel` for larger transient panels/toasts.
- Use `--ease-responsive`, which is already an ease-out-like responsive curve.
- Mirror the local Reduced Motion precedent of `80ms`.

**Ordered steps**

1. In `src/styles/motion.css`, replace broad popover transition with explicit property ownership:
   ```css
   .popover {
     transform-origin: var(--popover-transform-origin, center);
     transition-property: opacity, transform;
     transition-duration: var(--duration-fast);
     transition-timing-function: var(--ease-responsive);
   }
   ```
2. Before changing call sites, inspect actual popover placement:
   - If popovers are anchored to triggers, set `--popover-transform-origin` at the placement layer.
   - If the surface is truly centered, keep the `center` fallback.
3. Add a Reduced Motion branch:
   ```css
   @media (prefers-reduced-motion: reduce) {
     .popover { transition-duration: 80ms; }
   }
   ```
4. In `src/components/toast.css`, replace `top` animation with transform/opacity:
   ```css
   @keyframes toast-enter {
     from { transform: translateY(-8px); opacity: 0; }
     to { transform: translateY(0); opacity: 1; }
   }

   .toast {
     animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
   }
   ```
5. Add Reduced Motion toast behavior:
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

- Do not change toast stacking, position, dismiss timing, z-index, live-region behavior, or message lifecycle.
- Do not change popover open/close semantics, focus behavior, or placement logic except for transform-origin if the placement layer already owns that data.
- Do not use `will-change` unless later measurement proves it helps.

**Mechanical checks**

- Run existing lint/build/style checks.
- Search for `transition: all`, `toast-enter`, and `.popover` references to ensure no dependent behavior expects `top` animation or broad transitions.
- Confirm no other selector depends on `.toast` animated `top` values.

**Runtime/feel checks to perform later, not claimed here**

- Open popovers from each supported placement; origin should match trigger direction where applicable.
- Trigger multiple toasts; stacking should remain stable.
- Interrupt/replace toasts if the product supports that.
- Verify no layout jump when toast enters.

**Reduced Motion behavior**

- Popover: shortened transition, no added travel beyond existing state transform.
- Toast: opacity-only `80ms` feedback; no vertical movement.

**Source-drift stop condition**

- Stop if token names or values have changed, `.popover` is no longer the active selector, toast positioning no longer uses `top`, or toast entry is already handled by a different animation system.

---

### Plan 3 — Upgrade sortable queue drag settle for direct manipulation continuity

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

- Dragged item tracks the pointer 1:1 in a clear coordinate space.
- Release starts from the current on-screen value.
- Release velocity is measured in CSS px/s and handed into the settle animation.
- Existing `nearestSlot(currentY)` target-selection semantics are preserved unless product authority explicitly approves momentum-based target selection.
- Reduced Motion preserves direct manipulation but removes overshoot/elastic travel.

**Project conventions**

- Prefer transform ownership over layout movement.
- Keep motion crisp and non-playful for operations work.
- Use existing animation helper if it supports current value + velocity; do not add a dependency without approval.

**Ordered steps**

1. Inspect surrounding `pointerdown`, queue item CSS, and `animateTo` signature before editing.
2. Ensure drag state stores:
   - `pointerId`
   - grab offset from pointer to item
   - container/item bounds used for local coordinates
   - recent samples `{ y: CSS px, t: performance.now() }`
3. On drag start, use pointer capture if not already present.
4. On pointer move, convert `event.clientY` to local drag translation instead of storing absolute viewport Y directly.
5. Scope `--drag-y` to the dragged item or a dedicated transform wrapper, not a broad queue parent, unless current CSS proves parent-scoped variable updates are intentional and cheap.
6. Batch visual writes with `requestAnimationFrame` if pointer events can arrive faster than paint.
7. On pointer up:
   - release pointer capture;
   - compute release velocity from recent samples in CSS px/s;
   - read or preserve the current presentation value;
   - keep `const target = nearestSlot(currentY)` unless momentum targeting is separately authorized;
   - call the existing animation primitive with initial velocity if supported.
8. If `animateTo` only accepts fixed duration and cannot preserve velocity/current value, stop and request an animation-primitive decision instead of silently adding a dependency.
9. If momentum-based target selection is later authorized, use a bounded projected endpoint only for choosing the target; still keep velocity handoff as a separate step.

**Hard boundaries**

- Do not change reorder data semantics.
- Do not change `nearestSlot` behavior without explicit approval.
- Do not alter keyboard reorder behavior, selection state, persistence, or queue filtering.
- Do not add spring/gesture dependencies unless existing primitives cannot meet the requirements and the change is approved.

**Mechanical checks**

- Run existing type-check/lint/build gates.
- Add or update focused tests for `nearestSlot` only if existing tests already cover this area; do not invent product semantics.
- Search for all writers of `--drag-y` and all callers/signatures of `animateTo`.

**Runtime/feel checks to perform later, not claimed here**

- Drag slowly, quickly, and outside the original item bounds.
- Release while item is moving; settle should continue from current position without a jump.
- Interrupt a settling item by grabbing it again.
- Reorder near slot boundaries.
- Test under a large queue if that state exists, because parent-scoped CSS variable updates may affect style recalculation.

**Reduced Motion behavior**

- Keep direct 1:1 drag tracking; this is causality, not decorative motion.
- On release, use no overshoot, no elastic bounce, and a short settle or immediate snap with clear selected/drop state feedback.
- Preserve non-motion confirmation such as final position, highlight, or announcement if already present.

**Source-drift stop condition**

- Stop if `onPointerMove`, `onPointerUp`, `--drag-y`, `nearestSlot`, or `animateTo` no longer match the supplied excerpts, or if another gesture system already owns velocity/interruption.

## 4. Recommended execution order

1. **Plan 1: Command palette** — highest-frequency keyboard surface and likely low change size.
2. **Plan 2: Popover/toast CSS** — establishes tokenized transient-motion hygiene and Reduced Motion coverage.
3. **Plan 3: Sortable queue** — high impact but requires API and runtime feel decisions; do after source/API preflight.

## Explicitly unverified states

- Actual package manager, scripts, build gates, and CSS pipeline.
- Whether `palette` keyframes are defined or reused elsewhere.
- Whether command palette remains mounted while closed.
- Actual computed styles, frame rate, compositing behavior, or layout cost.
- Whether `.popover` is anchored, centered, or placement-aware.
- Toast stacking/lifecycle/live-region behavior.
- Pointer capture, grab offset, velocity tracking, and transform ownership outside the shown queue excerpt.
- `animateTo` API capabilities.
- Real keyboard throughput, interruption feel, Reduced Motion behavior, browser/device behavior, and accessibility-tree output.
