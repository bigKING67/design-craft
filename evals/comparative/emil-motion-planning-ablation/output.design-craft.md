## 1. Recon summary

**One-sentence diagnosis:** the motion system has a good local precedent, but several higher-frequency or state-continuity surfaces bypass it with long `ease-in`, broad-property, layout-property, or direct-manipulation motion that is not shown to have a Reduced Motion equivalent.

- **Stack signals:** React/TSX components, CSS modules/global CSS, CSS custom-property motion tokens, Tailwind-style arbitrary animation utility, and imperative JS animation for drag settle.
- **Where motion lives:**  
  - `src/styles/motion.css`: global tokens and `.popover` transition.  
  - `src/components/CommandPalette.tsx`: inline utility animation class.  
  - `src/components/toast.css`: keyframe animation.  
  - `src/components/SortableQueue.tsx`: pointer-driven CSS variable updates plus `animateTo(...)`.  
  - `src/components/Button.css`: correct local precedent.
- **Existing conventions:** `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`, explicit property transitions, transform-based press feedback, and a `prefers-reduced-motion` branch.
- **Product personality:** calm, crisp, workday desktop utility; motion should clarify causality and state continuity without adding waiting time.
- **Frequency map:**  
  - Very high: command palette, buttons, keyboard-triggered actions.  
  - High/interactive: sortable queue drag.  
  - Medium: popovers.  
  - Occasional but visible: toasts.  
- **Evidence level:** static snippets only. No runtime behavior, computed styles, frame pacing, accessibility tree, user testing, or browser/device validation was performed.

---

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | Static source | `src/components/CommandPalette.tsx` | `animate-[palette_420ms_ease-in_both]` is long, arbitrary, and `ease-in` for a likely keyboard-heavy surface; it also bypasses shown semantic tokens. | Replace with tokenized opacity/transform state transition around `160–240ms` using `--ease-responsive`; add Reduced Motion branch that preserves feedback without travel. |
| P1 | Static source | `src/components/SortableQueue.tsx` | Direct manipulation settles with `animateTo(nearestSlot(currentY), { duration: 400 })`; snippet does not show grab offset, pointer capture, presentation-value interruption, velocity handling, or Reduced Motion behavior. | Preserve `nearestSlot(...)` semantics, but make drag coordinate space, transform ownership, interruption, and settle behavior explicit; shorten/tokenize or use existing spring primitive if available. |
| P2 | Static source | `src/components/toast.css` | Toast enters by animating `top` over `500ms ease-in`; this is a layout-property animation risk and slower than existing motion tokens. | Animate `transform` + `opacity` instead; use `--duration-panel` or shorter with `--ease-responsive`; add Reduced Motion opacity-only feedback. |
| P2 | Static source | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in`; broad property ownership plus slow-start easing conflicts with crisp tokenized precedent. | Transition only `opacity`/`transform`; use existing duration/easing tokens; verify whether origin should be trigger-relative before changing `transform-origin`. |
| P2 | Static source | Multiple snippets | Reduced Motion is shown only for `.button`; meaningful movement in palette, toast, popover, and queue has no shown equivalent path. | Add per-surface Reduced Motion branches that remove large spatial movement while preserving opacity/color/focus/static state feedback. |
| P3 | Static source | Multiple snippets | Motion vocabulary is fragmented: `160ms`, `240ms`, `360ms`, `400ms`, `420ms`, `500ms`, `ease-in`, `ease-responsive`. | Normalize to existing semantic tokens first; introduce new tokens only if repeated use cases are proven. |

---

## 3. Implementation-ready plans

### Plan A — Tokenize high-frequency overlay motion: command palette + popover

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

```css
/* src/components/Button.css - existing correct local precedent */
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}
```

**Target behavior**

- Command palette opens/closes crisply with no long delayed-feeling entrance.
- Popover motion is bounded to visual properties only.
- Existing tokens remain the motion authority.
- Focus visibility and keyboard flow are not altered.
- Reduced Motion removes spatial travel but keeps clear state feedback.

**Project conventions to follow**

- Use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Prefer explicit `transition-property` over `transition: all`.
- Reuse the button precedent: transform-based feedback, tokenized timing, Reduced Motion branch.

**Ordered steps**

1. Inspect the actual `palette` keyframes before editing; confirm whether they animate only `opacity`/`transform` or something else.
2. In `src/components/CommandPalette.tsx`, replace the arbitrary animation class with a stable class name, for example `className="command-palette-motion"`, while preserving `data-open={open}`.
3. In `src/styles/motion.css`, add tokenized selectors for the command palette:
   - `[data-open="true"]`: `opacity: 1`, `transform: translateY(0) scale(1)`.
   - `[data-open="false"]`: `opacity: 0`, small `translateY(...)` or scale only if the component remains mounted.
   - transition only `opacity` and `transform`.
4. Replace `.popover { transition: all 360ms ease-in; }` with explicit `opacity`/`transform` transitions using existing tokens.
5. For `.popover`, verify whether it is a trigger-anchored popover or a centered overlay:
   - Trigger-anchored: use the positioning primitive’s transform-origin variable if present.
   - Truly centered modal-like overlay: retaining `center` is acceptable.
6. Add `@media (prefers-reduced-motion: reduce)` for both surfaces:
   - remove or minimize `transform` travel;
   - keep short opacity/color feedback;
   - do not hide focus indicators.

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change command execution, focus trapping, Escape behavior, or keyboard shortcuts.
- Do not introduce a new animation dependency.
- Do not invent a transform-origin variable unless the positioning library exposes one.
- Do not alter layout, z-index, or data loading.

**Mechanical checks**

- Search for remaining `palette_420ms_ease-in_both`.
- Search for `.popover` still using `transition: all`.
- Run the closest available static checks, such as type-check, lint, or build.
- Confirm no new hard-coded motion values were added unless intentionally justified.

**Runtime/feel checks to perform later**

- Toggle command palette repeatedly by keyboard.
- Reverse open/close mid-transition.
- Check focus ring remains visible during and after transition.
- Open popovers from different placements if collision/side placement exists.
- Confirm no claim of smoothness until observed in a browser.

**Reduced Motion behavior**

- Palette/popover should avoid positional travel.
- Keep a short opacity or static state change so the user still receives feedback.
- Focus visibility must remain unchanged.

**Source-drift stop condition**

Stop before editing if the `data-open` contract changed, the `palette` animation is no longer present, motion tokens were renamed, `.popover` is no longer the active selector, or authority now defines a different overlay motion language.

---

### Plan B — Repair toast entry to avoid layout-property motion and add Reduced Motion

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

- Toast entry remains noticeable but calm and quick.
- Movement preserves “arrived from above” causality without animating `top`.
- Reduced Motion keeps feedback without vertical travel.
- Existing toast placement and stacking semantics are not changed.

**Project conventions to follow**

- Use existing semantic duration/easing tokens.
- Prefer `transform` and `opacity` for visual motion.
- Keep transient UI motion shorter than current `500ms`.

**Ordered steps**

1. Confirm whether `.toast` already has a static `top` or positioning rule elsewhere; do not remove placement.
2. Rewrite `@keyframes toast-enter` to use `transform: translateY(-24px)` and `opacity: 0` to `transform: translateY(0)` and `opacity: 1`.
3. Change `.toast` animation timing from `500ms ease-in` to a tokenized value, preferably `var(--duration-panel) var(--ease-responsive)` unless a smaller existing toast token exists.
4. Add a Reduced Motion branch:
   - either use an opacity-only keyframe;
   - or set animation duration to a very short tokenized duration and remove transform travel.
5. If exit animation exists elsewhere, align it separately; do not invent a lifecycle rewrite from this snippet alone.

**Hard boundaries**

- Do not change toast queueing, ARIA announcements, dismissal timing, or stacking layout unless those files are explicitly in scope.
- Do not change `top`/positioning used for final placement; only remove `top` from the animation keyframes.
- Do not add blur, bounce, or decorative overshoot.

**Mechanical checks**

- Search `toast-enter` and confirm it no longer animates `top`.
- Search for hard-coded `500ms ease-in` in toast CSS.
- Run available CSS/lint/build checks.
- Confirm the Reduced Motion branch is present in `src/components/toast.css` or the project’s established motion stylesheet.

**Runtime/feel checks to perform later**

- Trigger one toast and multiple rapid toasts.
- Verify the toast appears promptly and remains readable.
- Reverse/dismiss during entry if dismissal exists.
- Validate with Reduced Motion enabled.
- Do not claim frame-rate improvement without tracing or representative observation.

**Reduced Motion behavior**

- No vertical travel.
- Preserve feedback through opacity or immediate visible state.
- Keep announcements and focus behavior unchanged.

**Source-drift stop condition**

Stop before editing if toast positioning has moved to another component, `toast-enter` is unused, a toast animation API replaces this CSS, or a newer design authority defines a different transient notification pattern.

---

### Plan C — Make sortable queue drag settle explicit, interruptible, and reduced-motion safe

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

- Drag tracks in a clearly defined coordinate space.
- The dragged item does not jump under the pointer.
- Release settle starts from the current on-screen value.
- Existing `nearestSlot(currentY)` target-selection semantics are preserved unless product authority explicitly approves momentum-based target selection.
- Reduced Motion avoids long travel/elasticity while preserving the final slot update and state feedback.

**Project conventions to follow**

- Use existing motion tokens where fixed durations remain.
- Keep transform ownership explicit.
- Treat direct manipulation separately from decorative CSS transitions.
- Preserve current queue ordering semantics.

**Ordered steps**

1. Locate the full `SortableQueue.tsx` implementation and the CSS consuming `--drag-y`.
2. Confirm coordinate space:
   - whether `clientY` is converted relative to the queue/container;
   - how `currentY` is derived;
   - whether scrolling affects the calculation.
3. Confirm pointer lifecycle:
   - pointer capture on drag start;
   - pointer release/cancel cleanup;
   - ignored secondary pointers if relevant.
4. Add or verify grab-offset preservation so the item remains attached to the original contact point rather than snapping to `event.clientY`.
5. Identify transform ownership:
   - if drag uses `translateY`, do not let press/hover scale overwrite it;
   - use wrapper layers or composed transform if needed.
6. Replace or parameterize `duration: 400`:
   - if existing animation primitive supports springs/current value, settle from the presentation value;
   - otherwise use a shorter tokenized fallback and document limitation.
7. Optionally measure release velocity in CSS px/s for animation handoff only.
   - Do not use projected endpoint to change `nearestSlot(...)` target selection unless explicitly authorized.
8. Add Reduced Motion behavior:
   - no elastic overshoot;
   - either immediate snap with static highlight/state feedback or very short non-vestibular transition.

**Hard boundaries**

- Do not change `nearestSlot(...)` semantics by default.
- Do not change queue data model, persistence, sorting rules, or revenue/support workflow behavior.
- Do not add a new physics/animation library unless already present and approved.
- Do not mix this with unrelated visual restyling.
- Do not claim touch/device feel from source inspection.

**Mechanical checks**

- Type-check the component.
- Verify pointer cleanup paths compile.
- Search for conflicting writes to `--drag-y` or `transform`.
- Confirm Reduced Motion branch is reachable.
- Confirm no global queue CSS variable update was broadened unnecessarily.

**Runtime/feel checks to perform later**

- Drag slowly, quickly, and outside the original item bounds.
- Release while moving and while stationary.
- Start a new drag during settle; verify no visual jump.
- Test with page/container scroll if the queue can scroll.
- Test Reduced Motion.
- If touch support matters, validate on representative hardware before approving feel.

**Reduced Motion behavior**

- Preserve drag functionality.
- Remove bounce, large animated settle, and decorative elasticity.
- Keep slot change clear through immediate placement, focus/state styling, or short opacity/color feedback.

**Source-drift stop condition**

Stop before editing if `animateTo(...)` API changed, `nearestSlot(currentY)` is no longer the target rule, drag CSS no longer uses `--drag-y`, pointer handlers moved, or a different gesture abstraction owns the queue interaction.

---

## 4. Recommended execution order

1. **Plan A** first: fixes the highest-frequency keyboard/overlay motion and reinforces token conventions.
2. **Plan B** second: localized CSS repair with clear accessibility and performance-risk reduction.
3. **Plan C** third: highest interaction complexity; do it when runtime validation time is available. If the sortable queue is core all-day work, move it before Plan B.

## Explicitly unverified states

- Actual `palette` keyframes and whether the command palette unmounts on close.
- Whether `.popover` is trigger-anchored, centered, or shared by multiple overlay types.
- Toast stacking, exit animation, dismissal timing, ARIA behavior, and visibility-timer behavior.
- `SortableQueue` coordinate system, transform consumption, pointer capture, grab offset, item count, scroll behavior, and animation API capabilities.
- Actual `DESIGN.md` text beyond the provided summary.
- Runtime smoothness, frame pacing, compositing, layout shift, focus order, accessibility tree behavior, and real Reduced Motion behavior.
