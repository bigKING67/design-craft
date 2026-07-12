Reading this as: a calm desktop operations console for keyboard-heavy support and revenue operators, optimized for fast state comprehension without decorative delay.

## 1. Recon summary

- **Stack signals:** React/TSX components, CSS modules/global CSS, Tailwind-style arbitrary animation class, CSS custom-property tokens, at least one JS animation helper: `animateTo(...)`.
- **Where motion lives:**  
  `src/styles/motion.css`, `src/components/CommandPalette.tsx`, `src/components/toast.css`, `src/components/SortableQueue.tsx`, `src/components/Button.css`.
- **Existing conventions:** semantic duration/easing tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`; correct local precedent uses transform-only transition and a `prefers-reduced-motion` branch in `Button.css`.
- **Product personality:** crisp, quiet, operational, throughput-first. Motion should confirm cause/effect and preserve continuity, not perform.
- **Frequency map:**
  - Very high: command palette, buttons, keyboard-triggered actions.
  - High/direct manipulation: sortable queue drag/reorder.
  - Medium: popovers.
  - Occasional but interruptible: toasts.
- **Evidence level:** static snippets only. No runtime, computed-style, trace, browser, device, accessibility-tree, or user-test validation was performed.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | Static source | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]`: long, ease-in, arbitrary value on a high-frequency keyboard surface; no Reduced Motion branch shown. | Replace with tokenized open/closed transition using `--duration-fast` or bounded `--duration-panel`, `--ease-responsive`, explicit properties, and reduced spatial motion. |
| P1 | Static source | `src/components/SortableQueue.tsx` | Drag/reorder code shows pointer-position CSS variable updates and a fixed `animateTo(..., { duration: 400 })`; no evidence of pointer capture, grab offset, velocity, projected snap, interruption, transform ownership, or Reduced Motion. | Implement/check a direct-manipulation contract before tuning duration: 1:1 tracking, pointer capture, presentation-value retargeting, velocity-aware snap, reduced overshoot/travel. |
| P2 | Static source | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`; broad property ownership, slower-than-needed timing, delayed response curve, and likely wrong origin for anchored overlays. | Transition only `opacity`/`transform`, use existing responsive easing, shorten to overlay range, and set trigger-relative origin unless the popover is actually centered. |
| P2 | Static source | `src/components/toast.css` | Toast animates `top` over `500ms ease-in`; this is a layout-property animation risk and slow delayed entry for operational feedback. | Animate `transform` + `opacity` with existing tokens; keep feedback visible in Reduced Motion via short fade/static position. |
| P2 | Static source | Multiple snippets | Reduced Motion precedent exists only in `Button.css`; other meaningful movement snippets do not show equivalent handling. | Add component-scoped `prefers-reduced-motion` branches that remove large travel/scale while preserving opacity/color/state feedback. |
| P3 | Static source | Multiple snippets | Motion vocabulary is fragmented: `160ms`, `240ms` tokens coexist with hardcoded `360ms`, `420ms`, `500ms`, `400`. | Consolidate around semantic tokens and component-specific exceptions only when justified by runtime checks. |

## 3. Implementation-ready plans

### Plan 1 — Tokenize and calm transient overlay motion

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

`src/components/CommandPalette.tsx`

```tsx
<div
  data-open={open}
  className="animate-[palette_420ms_ease-in_both]"
>
  <SearchResults />
</div>
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

- Overlays and transient feedback feel immediate and calm.
- Entry starts responsive, settles quickly, and uses existing semantic tokens.
- No `transition: all` for these surfaces.
- No layout-position animation for toast entry.
- Command palette does not impose cinematic delay on keyboard-heavy users.
- Reduced Motion preserves state feedback without meaningful travel.

**Project conventions to use**

- `--duration-fast: 160ms`
- `--duration-panel: 240ms`
- `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Existing local Reduced Motion pattern from `src/components/Button.css`.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` broad transition with explicit properties, for example `opacity, transform`, using `var(--duration-fast)` or `var(--duration-panel)` depending on popover size.
2. Change `.popover` easing from `ease-in` to `var(--ease-responsive)`.
3. Replace default `transform-origin: center` with a trigger-relative origin if the component has placement/origin variables; keep `center` only for genuinely centered overlays.
4. In `src/components/CommandPalette.tsx`, remove the arbitrary `animate-[palette_420ms_ease-in_both]` class.
5. Implement open/closed styling via stable classes or `data-open` selectors using explicit `opacity`/`transform` transitions and existing tokens.
6. In `src/components/toast.css`, replace `top` keyframe movement with transform-based entry, e.g. `translateY(...)` plus `opacity`.
7. Shorten toast duration to the project token range, preferably `--duration-panel` at most unless runtime checks prove it feels abrupt.
8. Add `@media (prefers-reduced-motion: reduce)` branches for popover, command palette, and toast: remove or sharply reduce translate/scale; keep short opacity/state feedback.

**Hard boundaries**

- Do not change search behavior, command execution, focus management, or toast lifecycle timing.
- Do not add an animation dependency.
- Do not introduce new global motion tokens unless existing tokens cannot express the needed behavior.
- Do not modify `src/components/Button.css` except as a reference check.
- Do not claim performance improvement without runtime measurement.

**Mechanical checks**

- Inspect actual package scripts first.
- Run the closest available checks, in this order when present:
  - type check for TSX changes,
  - lint,
  - build or CSS pipeline check.
- Also grep for removed arbitrary animation names to ensure no orphaned `palette` keyframe/class dependency remains.

**Runtime / feel checks to perform later**

- Open/close command palette repeatedly via keyboard.
- Open/close popovers from different trigger positions.
- Fire multiple toasts in succession.
- Verify no visible delayed start from ease-in behavior.
- Verify focus remains visible and not hidden by entry animation.
- Use DevTools animation inspection or computed styles to confirm only intended properties animate.

**Reduced Motion behavior**

- Command palette: no scale/travel; immediate visibility or very short opacity transition.
- Popover: no origin-based scale travel; opacity/state feedback remains.
- Toast: appears in final position with short fade or static state change; no vertical slide.

**Source-drift stop condition**

Stop before editing if:
- `--duration-fast`, `--duration-panel`, or `--ease-responsive` were renamed/removed;
- `CommandPalette` no longer uses the shown arbitrary animation class;
- toast positioning no longer uses `top`;
- a newer design authority explicitly defines different overlay/toast motion.


### Plan 2 — Repair sortable queue drag/reorder as direct manipulation

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

- Dragged item tracks the pointer 1:1 after intent is established.
- Reorder settle animation begins from the current on-screen value, not a reset target.
- Snap target accounts for release velocity/projected endpoint, not only current release position.
- Drag remains interruptible; user can grab/reverse without waiting for a fixed animation to finish.
- Reduced Motion removes elastic/large travel while preserving clear item placement feedback.

**Project conventions to use**

- Keep existing `animateTo(...)` only if it supports current-value retargeting and velocity/interrupt semantics.
- Use transform-based movement, not layout properties, for per-frame drag visuals.
- Keep motion calm: no unnecessary bounce for a serious operations queue.

**Ordered steps**

1. Inspect the full `SortableQueue.tsx` implementation before editing:
   - where `currentY` is defined,
   - how `--drag-y` is consumed,
   - whether `animateTo` can read current presentation value,
   - whether pointer capture already exists elsewhere.
2. On pointer down/start, store:
   - active pointer id,
   - initial pointer position,
   - item start position,
   - grab offset,
   - short timestamped position history.
3. Use pointer capture once drag intent is confirmed so movement continues outside the original bounds.
4. On pointer move, compute translation in a defined coordinate space, preferably CSS pixels relative to the queue/item container, not raw viewport `clientY` unless the CSS consumer expects viewport coordinates.
5. Ensure one explicit transform owner:
   - either one composed transform string,
   - or nested wrappers separating drag translate from press/settle transforms.
6. On pointer up, compute release velocity from recent samples.
7. Choose the destination slot from a projected endpoint, then call the animation primitive with current position and velocity if supported.
8. If `animateTo` cannot support interruption/presentation-value starts, replace only this local settle path with a minimal internal primitive or project-approved existing helper; do not add a dependency by default.
9. Add Reduced Motion behavior:
   - no elastic overshoot,
   - shorter settle,
   - direct placement or minimal transform,
   - clear selected/dropped state via static styling.

**Hard boundaries**

- Do not change queue ordering semantics, persistence, data loading, or keyboard reordering behavior.
- Do not introduce a gesture library unless existing primitives cannot meet interruption/velocity requirements and the dependency is explicitly approved.
- Do not animate layout properties in the drag hot path.
- Do not allocate large objects or perform expensive DOM reads on every pointer move.
- Do not lock input while the settle animation completes.

**Mechanical checks**

- Type check the component.
- Run lint for event-handler and ref usage.
- Run existing interaction/unit tests if present for queue ordering.
- Add or update tests only if the project already has a nearby pattern for pointer/reorder behavior.

**Runtime / feel checks to perform later**

- Drag slowly, quickly, and outside the original queue bounds.
- Release near a boundary with low and high velocity.
- Interrupt the settle animation by grabbing the item mid-flight.
- Verify no jump on drag start; grab offset is preserved.
- Verify pointer cancellation and lost-capture paths reset state.
- Check behavior in a long queue if that state exists.

**Reduced Motion behavior**

- Drag still tracks directly under user control.
- Release settle uses minimal/no overshoot and short duration.
- Placement confirmation remains visible via position/state styling, not large motion.

**Source-drift stop condition**

Stop before editing if:
- `onPointerMove`, `onPointerUp`, `currentY`, or `animateTo` signatures differ materially from the excerpt;
- `--drag-y` is no longer the visual movement mechanism;
- queue reordering has moved to a shared drag abstraction;
- product/design authority explicitly forbids animated reorder settling.


### Plan 3 — Consolidate Reduced Motion as a component-level contract

**Files / current excerpts**

Correct precedent:

`src/components/Button.css`

```css
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

.button:active {
  transform: scale(0.98);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

Uncovered meaningful motion shown in:

- `src/styles/motion.css` — `.popover`
- `src/components/CommandPalette.tsx` — command palette entry animation
- `src/components/toast.css` — toast entry animation
- `src/components/SortableQueue.tsx` — drag settle animation

**Target behavior**

- Every meaningful motion surface shown has a Reduced Motion branch.
- Reduced Motion does not erase feedback; it removes large spatial travel, long duration, and elastic/vestibular effects.
- The branch is local to each component/style file unless the project already has a centralized motion accessibility layer.

**Project conventions to use**

- Follow the local `@media (prefers-reduced-motion: reduce)` precedent.
- Use existing semantic tokens where possible.
- Preserve visible focus and state feedback.

**Ordered steps**

1. Inventory only the cited files first; do not start a full-codebase sweep unless requested.
2. Add component-local Reduced Motion rules for popover, command palette, and toast.
3. In `SortableQueue.tsx`, route the settle behavior through a reduced-motion condition if one already exists; otherwise add the smallest local check compatible with project patterns.
4. For CSS components, reduce duration and remove/reduce translate/scale.
5. For JS-driven settle, avoid bounce/projection exaggeration under Reduced Motion; keep direct placement or a short settle.
6. Confirm focus-visible styles remain independent of motion changes.

**Hard boundaries**

- Do not globally disable all transitions.
- Do not remove press/focus feedback.
- Do not change color, spacing, or layout tokens unrelated to motion accessibility.
- Do not create a new shared utility unless at least two existing files already use or clearly need the same abstraction.

**Mechanical checks**

- CSS syntax/build check through the project’s normal pipeline.
- Type check if a JS/TS reduced-motion hook or condition is added.
- Lint for unused classes/hooks.

**Runtime / feel checks to perform later**

- Emulate `prefers-reduced-motion: reduce`.
- Repeat command palette open/close, popover open/close, toast entry, and queue settle.
- Confirm feedback remains perceivable without large movement.
- Confirm no focus outline is removed or delayed.

**Reduced Motion behavior**

- Popover/command palette: static final position, short opacity/state transition only.
- Toast: no vertical travel; short fade or immediate final state.
- Sortable queue: direct manipulation unchanged while dragging; settle uses minimal distance/time and no bounce.

**Source-drift stop condition**

Stop before editing if:
- a centralized Reduced Motion system already exists and these components should use it instead;
- `Button.css` no longer contains the cited precedent;
- any cited component has been refactored away;
- the design authority changes the Reduced Motion requirement.

## 4. Recommended execution order

1. **Plan 1 first** — highest breadth-to-risk ratio: removes slow/ease-in/arbitrary/layout-motion patterns from overlays and toasts while aligning with existing tokens.
2. **Plan 3 alongside or immediately after Plan 1** — ensures accessibility parity and prevents token cleanup from leaving Reduced Motion incomplete.
3. **Plan 2 last but before release if queue reordering is core workflow** — direct manipulation needs real interaction validation and should not be guessed from static snippets.

## Explicitly unverified states

- Actual rendered smoothness, frame rate, compositing, layout shift, and paint cost.
- Whether `transition: all` currently animates expensive properties in practice.
- Whether `palette` keyframes include transform, opacity, scale, or other properties.
- Whether `animateTo` supports interruption, current-value starts, velocity, or cancellation.
- Pointer capture, grab offset, keyboard reorder parity, and long-list behavior.
- Actual Reduced Motion behavior outside the shown `Button.css` precedent.
- Focus management and accessibility-tree behavior.
- Browser/device-specific feel.

Basis: evidence-only frontend, accessibility, performance, and motion-planning guardrails were applied; no files were edited and no runtime validation was performed.
