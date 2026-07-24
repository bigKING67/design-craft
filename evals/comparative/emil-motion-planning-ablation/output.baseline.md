## 1. Recon summary

- **Stack signals:** TSX component files, CSS component files, global CSS tokens, utility-style arbitrary animation syntax, imperative pointer motion via JS.
- **Where motion lives:**
  - Global token layer: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Component markup classes: `src/components/CommandPalette.tsx`
  - JS gesture/reorder path: `src/components/SortableQueue.tsx`
- **Existing conventions:**
  - Semantic durations: `--duration-fast: 160ms`, `--duration-panel: 240ms`
  - Semantic easing: `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Reduced Motion precedent: shorten duration to `80ms` while preserving feedback
  - Correct local precedent: button uses `transform`, semantic tokens, and Reduced Motion override
- **Product personality:** calm, crisp, operational, throughput-oriented; motion should clarify causality and state continuity, not create theatrical delay.
- **Frequency map:**
  - Very high: buttons, command palette, popovers
  - High/medium: toasts and transient feedback
  - Lower frequency but high sensitivity: sortable queue drag/release
- **Evidence level:** static excerpt audit only. No runtime behavior, computed styles, frame timing, browser validation, accessibility tree, screen recording, or user testing was performed.

---

## 2. Priority table

| Priority | Finding | Evidence | Risk | Roadmap owner |
|---:|---|---|---|---|
| P0 | Motion contract is inconsistent across surfaces | Tokens exist, but popover/palette/toast/queue use hard-coded durations/easings | Operators experience uneven timing and unclear state continuity | Plan 1 |
| P0 | `transition: all` on popover is too broad | `.popover { transition: all 360ms ease-in; }` | Unintended properties may animate; duration/easing conflict with design authority | Plan 1 |
| P0 | Command palette uses long arbitrary animation | `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard surface may feel delayed; no visible Reduced Motion path in excerpt | Plan 2 |
| P1 | Toast animates layout property and is slow | `top` from `-24px` to `0`, `500ms ease-in` | Layout-affecting motion and long feedback delay are poor fit for operational alerts | Plan 2 |
| P1 | Sortable release animation is hard-coded and long | `animateTo(..., { duration: 400 })` | Drag release may feel detached from direct manipulation; no Reduced Motion path in excerpt | Plan 3 |
| P2 | Reduced Motion is implemented locally, not shown as system-wide | Button has media query; others do not in excerpt | Feedback may be preserved inconsistently for motion-sensitive users | Plans 1–3 |

---

## 3. Implementation plans

### Plan 1 — Normalize global motion contract and popover behavior

**Current file/excerpt**

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

- Popovers use semantic duration/easing.
- Only compositable visual properties transition, primarily `opacity` and `transform`.
- Popover timing matches calm operational surfaces: quick enough for repeated use, clear enough to preserve causality.
- Reduced Motion preserves open/close feedback with a shorter duration, following the button precedent.

**Project conventions to preserve**

- Use existing semantic tokens before adding new ones.
- Keep `--duration-fast`, `--duration-panel`, and `--ease-responsive` as the authority.
- Follow the existing Reduced Motion precedent of `80ms`.
- Keep focus visibility separate from motion; do not hide or delay focus indicators.

**Ordered implementation steps**

1. Replace broad popover transition:
   - From: `transition: all 360ms ease-in;`
   - To: transition only `opacity` and `transform`.
2. Use `var(--duration-panel)` for normal popover open/close.
3. Use `var(--ease-responsive)` instead of `ease-in`.
4. Add a Reduced Motion override for `.popover` using `80ms`.
5. If existing open/closed state selectors are present elsewhere, wire the transition to those selectors without changing state semantics.
6. If no state selectors exist, only change the transition declaration; do not invent visibility or mount behavior from this excerpt.

**Suggested shape**

```css
.popover {
  transform-origin: center;
  transition:
    opacity var(--duration-panel) var(--ease-responsive),
    transform var(--duration-panel) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .popover {
    transition-duration: 80ms;
  }
}
```

**Hard boundaries**

- Do not use `transition: all`.
- Do not add spring libraries or new dependencies.
- Do not alter popover focus management from this motion pass unless existing code requires it.
- Do not change layout, positioning, portal behavior, or dismissal behavior based only on this excerpt.

**Mechanical checks**

- Search for remaining `transition: all`.
- Search for hard-coded `360ms`, `420ms`, `500ms`, `400` motion durations after subsequent plans.
- Confirm CSS parses and selectors remain scoped as intended.
- Run the project’s closest style/type/build check after implementation.

**Runtime/feel checks to perform later, not performed now**

- Open/close popover repeatedly with keyboard and pointer.
- Confirm no delayed focus visibility.
- Confirm popover feels crisp rather than slow or theatrical.
- Confirm Reduced Motion still communicates state change.

**Reduced Motion behavior**

- Keep feedback.
- Shorten transition to `80ms`.
- Avoid replacing state change with no visual indication unless the product explicitly chooses that.

**Source-drift stop condition**

Stop before editing if `src/styles/motion.css` no longer contains the shown `.popover` rule, if motion tokens have been renamed, or if popover motion is now defined in a different component/style layer.

---

### Plan 2 — Replace long arbitrary entry animations for command palette and toast

**Current files/excerpts**

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

- Command palette opens with a short, calm transform/opacity transition.
- Toast enters using `transform` and `opacity`, not `top`.
- Both use semantic durations/easing.
- Both provide a Reduced Motion path that preserves feedback.
- Command palette avoids long arbitrary animation syntax for a high-frequency keyboard surface.

**Project conventions to preserve**

- Use existing semantic tokens.
- Use transform/opacity as the preferred motion properties.
- Use `80ms` in Reduced Motion, matching the existing button precedent.
- Keep the command palette optimized for keyboard-heavy repeated use.

**Ordered implementation steps**

1. Replace the command palette arbitrary animation class with a semantic class name.
   - Example target class: `commandPaletteMotion`
   - Keep `data-open={open}` because it is already present and useful.
2. Define command palette motion in the appropriate stylesheet already used by the component, or create a colocated component stylesheet only if that is the existing local convention.
3. Use `opacity` and a small `transform` delta for palette entry/exit.
   - Suggested normal duration: `var(--duration-panel)`.
   - Suggested easing: `var(--ease-responsive)`.
4. Do not change mount/unmount lifecycle unless existing code already supports exit animation.
5. Update toast keyframes:
   - Replace `top` movement with `transform: translateY(...)`.
   - Use `var(--duration-fast)` or `var(--duration-panel)` depending on toast importance.
   - For routine status feedback, prefer `var(--duration-fast)`.
6. Add Reduced Motion overrides for both command palette and toast.
7. If the command palette has existing close animation elsewhere, consolidate rather than duplicate.

**Suggested command palette shape**

```tsx
<div
  data-open={open}
  className="commandPaletteMotion"
>
  <SearchResults />
</div>
```

```css
.commandPaletteMotion {
  opacity: 0;
  transform: translateY(-4px) scale(0.99);
  transition:
    opacity var(--duration-panel) var(--ease-responsive),
    transform var(--duration-panel) var(--ease-responsive);
}

.commandPaletteMotion[data-open="true"] {
  opacity: 1;
  transform: translateY(0) scale(1);
}

@media (prefers-reduced-motion: reduce) {
  .commandPaletteMotion {
    transition-duration: 80ms;
    transform: none;
  }
}
```

**Suggested toast shape**

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

- Do not claim the current command palette animation reruns incorrectly without runtime evidence.
- Do not change search behavior, focus trap behavior, result rendering, or keyboard shortcuts in this motion pass.
- Do not move toast position logic unless required to remove `top` from the animation.
- Do not remove feedback entirely in Reduced Motion.
- Do not introduce new global animation names that collide with existing names.

**Mechanical checks**

- Search for `animate-[palette_420ms_ease-in_both]`.
- Search for `@keyframes toast-enter`.
- Confirm no `top` animation remains in toast enter motion.
- Confirm no new hard-coded `420ms` or `500ms` remains for these paths.
- Run type/style/build checks available in the project.

**Runtime/feel checks to perform later, not performed now**

- Open command palette repeatedly using keyboard.
- Verify search input focus is visible immediately.
- Confirm palette does not feel delayed before typing.
- Trigger multiple toasts and verify feedback is noticeable but not distracting.
- Test Reduced Motion preference and confirm brief feedback remains.

**Reduced Motion behavior**

- Command palette: shorten to `80ms`; remove scale/translation if needed, keeping opacity feedback.
- Toast: shorten to `80ms`; prefer opacity-only or very small transform.
- Preserve causal feedback for open, close, and notification arrival.

**Source-drift stop condition**

Stop before editing if the command palette already imports a different motion stylesheet, if the arbitrary animation has moved into a shared animation system, or if `toast-enter` is no longer the active toast entry animation.

---

### Plan 3 — Make sortable queue drag/release motion direct and preference-aware

**Current file/excerpt**

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

- During drag: movement remains direct and immediate.
- On release: item settles to nearest slot with crisp, short motion.
- Duration uses the same semantic timing contract as the rest of the interface.
- Reduced Motion shortens or minimizes the release animation while preserving state confirmation.
- Pointer movement avoids unnecessary per-event work beyond updating the active transform input.

**Project conventions to preserve**

- Use transform-driven movement if existing CSS maps `--drag-y` into transform.
- Use semantic timing values aligned with `--duration-fast` / `--duration-panel`.
- Keep Reduced Motion feedback at approximately `80ms`.
- Do not change sorting rules or slot calculation during a motion-system pass.

**Ordered implementation steps**

1. Inspect the existing CSS that consumes `--drag-y`.
2. If `--drag-y` currently drives `transform`, keep that path.
3. If it drives layout properties, move the visual drag representation to `transform`.
4. Replace hard-coded release duration:
   - From: `animateTo(nearestSlot(currentY), { duration: 400 });`
   - To: a named duration value derived from the motion contract.
5. Prefer a shorter release duration:
   - Normal: `160ms` for small slot snaps, or `240ms` if the queue item can travel farther.
   - Reduced Motion: `80ms`.
6. Add or reuse a motion preference helper only if one already exists; otherwise keep a small local `matchMedia('(prefers-reduced-motion: reduce)')` check.
7. Consider batching pointer-move style writes with `requestAnimationFrame` only if profiling later shows event pressure; do not add complexity without evidence.

**Suggested implementation shape**

```tsx
const prefersReducedMotion =
  window.matchMedia?.("(prefers-reduced-motion: reduce)").matches ?? false;

const releaseDuration = prefersReducedMotion ? 80 : 160;

function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), { duration: releaseDuration });
}
```

If broader queue travel needs more continuity:

```tsx
const releaseDuration = prefersReducedMotion ? 80 : 240;
```

**Hard boundaries**

- Do not change `nearestSlot(currentY)` behavior without separate interaction tests.
- Do not change queue ordering semantics.
- Do not introduce inertia, overshoot, bounce, or decorative physics for this operational surface.
- Do not claim current pointer movement is janky without profiling.
- Do not remove direct manipulation feedback in Reduced Motion.

**Mechanical checks**

- Search for `animateTo(` and other hard-coded drag durations.
- Confirm TypeScript accepts the motion preference code in the component environment.
- Confirm server-side or non-browser rendering paths are guarded if applicable.
- Confirm no layout property is animated for the dragged visual element.
- Run type/build checks after implementation.

**Runtime/feel checks to perform later, not performed now**

- Drag short and long distances.
- Release near and between slots.
- Confirm release feels attached to the pointer, not delayed.
- Confirm no bounce/overshoot unless already part of the product language.
- Confirm Reduced Motion still shows the item reaching the final slot.

**Reduced Motion behavior**

- Direct drag remains direct.
- Release snap shortens to `80ms`.
- Avoid added scale, bounce, or secondary flourish.
- Preserve final-position feedback.

**Source-drift stop condition**

Stop before editing if `animateTo` has been replaced, if `--drag-y` no longer controls drag motion, or if queue motion has moved into a shared gesture utility.

---

## 4. Recommended execution order

1. **Plan 1 first:** establish the tokenized motion contract and remove the broadest unsafe transition.
2. **Plan 2 second:** fix the highest-frequency keyboard and feedback surfaces.
3. **Plan 3 third:** tune the gesture path after the shared timing direction is clear.

Explicitly defer decorative refinements until the core contract is consistent.

---

## Explicitly unverified states

- Actual computed CSS values.
- Whether command palette mounts/unmounts or remains in DOM.
- Whether `data-open` currently controls any styles elsewhere.
- Whether toast position depends on `top` outside the animation.
- Whether `--drag-y` is consumed by `transform`, layout, or another property.
- Actual frame rate, layout cost, or input latency.
- Keyboard focus order and accessibility tree.
- Existing test/build commands.
- Browser/device behavior.
- User-tested feel or operator throughput impact.
