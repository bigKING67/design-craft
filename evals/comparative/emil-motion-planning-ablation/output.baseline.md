## 1. Recon summary

**Stack signals**
- React/TSX components with CSS modules/files and global motion tokens.
- CSS custom properties already exist for motion semantics:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Utility-style arbitrary animation appears in `CommandPalette.tsx`.
- Motion currently lives in a mix of global CSS, component CSS, inline style mutation, and component class strings.

**Where motion lives**
- `src/styles/motion.css`: global tokens plus `.popover`.
- `src/components/CommandPalette.tsx`: hard-coded animation utility.
- `src/components/toast.css`: local keyframes and animation.
- `src/components/SortableQueue.tsx`: pointer-driven CSS variable updates and imperative snap animation.
- `src/components/Button.css`: strongest local precedent for tokenized, transform-only, reduced-motion-aware interaction.

**Existing conventions**
- Preferred: semantic duration/easing tokens, transform-based movement, visible interaction feedback, and reduced-motion duration shortening.
- Confirmed good precedent:
  - `transition: transform var(--duration-fast) var(--ease-responsive);`
  - reduced motion keeps feedback but shortens duration to `80ms`.

**Product personality**
- Calm, crisp, desktop operations UI.
- Motion should explain causality and state continuity without adding delay.
- Keyboard-heavy users need quick state changes, predictable focus, and no theatrical animation.

**Frequency map**
- Very frequent: buttons, pointer drag in sortable queue, command palette.
- Frequent/contextual: popovers.
- Background/episodic: toast entrance.
- Highest risk areas are high-frequency or task-blocking motion: command palette and sortable queue.

**Evidence level**
- Static snippet audit only.
- No runtime validation, computed styles, accessibility tree, trace, device testing, or user testing was performed.
- Findings below are limited to what is directly supported by the excerpts.

---

## 2. Priority table

| Priority | Area | Finding | Evidence | Risk | Recommended direction |
|---:|---|---|---|---|---|
| P0 | Reduced Motion coverage | Reduced Motion is present only in the button precedent; other shown motion paths have no reduced-motion branch. | `.button` has media query; `.popover`, palette, toast, queue snippets do not. | Users requesting reduced motion may still receive long or spatial motion. | Apply reduced-motion behavior to every motion path while preserving feedback. |
| P0 | Command palette | Uses hard-coded `420ms ease-in` animation in component class. | `className="animate-[palette_420ms_ease-in_both]"` | Palette is likely high-frequency and task-blocking; hard-coded slow ease-in conflicts with crisp operations feel. | Move to semantic class/tokens, shorter panel duration, state-specific enter/exit. |
| P1 | Popover | Uses `transition: all 360ms ease-in`. | `.popover { transition: all 360ms ease-in; }` | `all` can unintentionally animate layout/color/etc.; 360ms ease-in feels delayed for operational UI. | Restrict to `opacity, transform`; use existing duration/easing tokens. |
| P1 | Toast | Animates `top` for 500ms with `ease-in`. | `@keyframes toast-enter { from { top: -24px; ... } }` | Layout-position animation and long duration are poor fit for lightweight feedback. | Use `transform: translateY(...)` + opacity; reduce duration. |
| P1 | Sortable queue | Pointer move writes CSS var directly; snap uses hard-coded 400ms. | `setProperty("--drag-y", ...)`; `animateTo(..., { duration: 400 })` | Drag feedback and snap duration may feel detached from direct manipulation. | Use transform-driven movement, frame-bounded updates, tokenized snap, reduced-motion snap. |
| P2 | Motion consistency | Durations/easings are fragmented across CSS and TSX. | `160ms`, `240ms`, `360ms`, `400`, `420ms`, `500ms`; mixed `ease-in`. | Inconsistent feel across repeated workflows. | Centralize semantic motion choices and remove arbitrary one-off timings. |

---

## 3. Implementation plans

### Plan A — Normalize overlay/disclosure motion: popover + command palette

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
- Popovers and command palette should feel immediate, explain open/close causality, and avoid sluggish task blocking.
- Use opacity + transform only.
- Use semantic tokens instead of hard-coded `360ms`, `420ms`, and `ease-in`.
- Preserve visible state feedback under Reduced Motion with a short duration, not instant disappearance unless required.

**Project conventions to follow**
- Reuse `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the button precedent: transform-based motion and `80ms` reduced-motion duration.
- Avoid `transition: all`.
- Avoid arbitrary animation strings for core repeated UI.

**Ordered steps**
1. In `src/styles/motion.css`, replace `.popover` transition with explicit properties:
   - `opacity var(--duration-fast) var(--ease-responsive)`
   - `transform var(--duration-fast) var(--ease-responsive)`
2. Keep `transform-origin: center` only if the visual treatment still needs centered scale; otherwise choose an origin that matches trigger geometry.
3. Add state selectors for `.popover[data-open="true"]` and `.popover[data-open="false"]`, or align with the existing state API if already present outside the snippet.
4. Use a small transform delta:
   - closed: slight translate/scale plus `opacity: 0`
   - open: `transform: translateY(0) scale(1); opacity: 1`
5. Replace the command palette arbitrary animation class with a named class, for example `className="commandPaletteMotion"`, while preserving `data-open={open}`.
6. Define command palette motion in the appropriate component CSS or shared motion CSS:
   - open: opacity to `1`, transform to settled state.
   - closed: opacity to `0`, transform to a small offset/scale.
   - duration: `var(--duration-panel)` for panel-scale movement.
   - easing: `var(--ease-responsive)`.
7. Add Reduced Motion branch:
   - keep opacity/state feedback.
   - reduce duration to `80ms`.
   - remove or nearly eliminate spatial travel/scale.

**Hard boundaries**
- Do not change command search behavior, result rendering, focus management, or keyboard shortcuts in this motion pass.
- Do not introduce new timing constants unless a new semantic token is explicitly approved.
- Do not animate layout properties, dimensions, or `all`.
- Do not remove `data-open`; it is useful for state styling and testing.

**Mechanical checks**
- Search for remaining `transition: all` in touched motion files.
- Search for `animate-[palette_420ms_ease-in_both]` and confirm it is removed.
- Confirm no new hard-coded overlay durations like `360ms`, `400ms`, `420ms`, or `500ms` are introduced.
- Run the closest static checks available for TSX/CSS formatting and type safety.

**Runtime/feel checks to perform later**
- Open and close command palette repeatedly by keyboard.
- Confirm it feels responsive rather than delayed.
- Confirm close motion does not trap attention.
- Confirm popover origin visually relates to its trigger.
- Confirm focus indicator remains visible before, during, and after the motion.

**Reduced Motion behavior**
- Duration: `80ms`.
- Prefer opacity-only or minimal transform.
- Feedback remains visible; state change should not become ambiguous.

**Source-drift stop condition**
- Stop before implementation if `CommandPalette` already uses another animation/state library outside the excerpt, or if `.popover` is generated/owned by a third-party component contract not shown here.

---

### Plan B — Convert toast entrance to compositor-safe feedback

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
- Toasts should appear as lightweight confirmation, not a slow event.
- Entrance should be short, calm, and compositor-friendly.
- Movement should preserve causality from the top area without animating `top`.

**Project conventions to follow**
- Use existing semantic tokens.
- Prefer transform + opacity.
- Use `var(--ease-responsive)`.
- Keep Reduced Motion feedback with shorter duration.

**Ordered steps**
1. Replace keyframes that animate `top` with keyframes that animate `transform`.
2. Suggested shape:
   - from: `transform: translateY(-8px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
3. Replace `500ms ease-in` with a semantic duration:
   - likely `var(--duration-fast)` for transient feedback.
4. Replace `ease-in` with `var(--ease-responsive)`.
5. Add `@media (prefers-reduced-motion: reduce)`:
   - animation duration `80ms`.
   - reduce translation to `0` or a very small offset.
6. Ensure the toast’s final positioning is set by normal layout/static styles, not by the animation’s final `top`.

**Hard boundaries**
- Do not change toast queueing, dismissal timing, message content, severity styling, or live-region behavior in this pass.
- Do not rely on `forwards` to establish required layout position.
- Do not animate `top`, `left`, `right`, `bottom`, width, height, or margins.

**Mechanical checks**
- Confirm `toast-enter` no longer contains `top`.
- Confirm `.toast` no longer uses `500ms ease-in`.
- Confirm final position is represented outside the keyframe if positioning is required.
- Confirm Reduced Motion branch exists in `src/components/toast.css`.

**Runtime/feel checks to perform later**
- Trigger success, warning, and error toasts if those variants exist.
- Confirm the toast feels informative, not attention-grabbing.
- Confirm multiple toasts do not create excessive motion.
- Confirm reduced-motion mode still communicates arrival.

**Reduced Motion behavior**
- Use `80ms`.
- Prefer opacity-only.
- If movement remains, keep it very small and non-essential.

**Source-drift stop condition**
- Stop if toast positioning depends on the `top` animation to reach its final layout state; first separate static positioning from entrance animation.

---

### Plan C — Make sortable queue drag and snap feel directly manipulated

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
- Dragged item should track pointer movement directly.
- Reorder snap should be quick and causal, not a separate slow animation.
- Timing should use semantic project motion values.
- Reduced Motion should preserve the snap/placement feedback while minimizing travel animation.

**Project conventions to follow**
- Use transform-driven movement via CSS variable.
- Tokenize duration and easing.
- Follow the local precedent of shortened `80ms` Reduced Motion.
- Keep high-frequency pointer work lightweight.

**Ordered steps**
1. Confirm `--drag-y` is consumed by `transform`, not by `top` or layout-position properties. If not, move the visual displacement to `transform: translateY(...)`.
2. Change the CSS variable meaning if needed from absolute viewport `clientY` to a local delta, for example `--drag-y: ${deltaY}px`, so the transform maps to item movement rather than page position.
3. Bound pointer updates to animation frames:
   - store latest pointer value.
   - schedule one visual write per frame.
   - avoid multiple style writes in the same frame.
4. Replace `animateTo(nearestSlot(currentY), { duration: 400 })` with a token-aligned duration:
   - likely `var(--duration-panel)` or a JS constant mapped to the same `240ms` value.
5. Use the shared easing equivalent of `--ease-responsive` for the snap animation if the animation API accepts easing.
6. Add a Reduced Motion path:
   - snap duration `80ms`.
   - no overshoot/bounce.
   - still clearly lands in the nearest slot.
7. Ensure `setDragging(false)` does not remove the visual dragged state before the snap target is applied, unless the animation system already handles handoff.

**Hard boundaries**
- Do not redesign sorting rules, hit testing, item identity, persistence, or keyboard reordering in this pass.
- Do not add physics/bounce unless explicitly approved; this product needs calm causality.
- Do not block pointer handling with expensive layout reads inside `onPointerMove`.
- Do not claim performance improvement until measured later.

**Mechanical checks**
- Confirm no hard-coded `duration: 400` remains in this component.
- Confirm the drag visual path uses transform-based CSS.
- Confirm pointer move does not perform repeated layout reads/writes beyond the intended CSS variable update.
- Confirm Reduced Motion can be determined by the same mechanism used elsewhere in the app or by a local media-query-backed utility.

**Runtime/feel checks to perform later**
- Drag slowly, quickly, and across multiple slots.
- Release near slot boundaries and confirm the snap target feels predictable.
- Confirm dragged item does not lag behind the pointer in ordinary use.
- Confirm reduced-motion mode lands clearly without unnecessary spatial travel.
- Confirm keyboard users have an equivalent clear reorder state if keyboard sorting exists.

**Reduced Motion behavior**
- Direct manipulation during active drag can remain because it is user-controlled.
- Programmatic snap should shorten to `80ms`.
- Avoid bounce, overshoot, or decorative easing.

**Source-drift stop condition**
- Stop if `animateTo` comes from an animation system with its own token integration, cancellation behavior, or reduced-motion handling not visible in the snippet; inspect that contract before changing durations.

---

## 4. Recommended execution order

1. **Plan A first**: fixes the most visible consistency issues and removes hard-coded task-blocking overlay motion.
2. **Plan B second**: small, contained conversion from layout-position animation to transform animation.
3. **Plan C third**: highest interaction complexity; should be implemented after token/easing conventions are settled.

## Explicitly unverified states

- Actual rendered timing, easing feel, and computed styles.
- Whether `palette` keyframes exist elsewhere and what they animate.
- Whether `.popover` is attached to a specific component library or generated markup.
- Whether toast has live-region semantics, dismissal timing, stacking behavior, or severity variants.
- Whether `--drag-y` currently drives `transform` or layout properties.
- Whether `animateTo` already handles cancellation, easing, Reduced Motion, or token mapping.
- Actual performance, frame rate, input latency, focus behavior, and accessibility-tree output.
