## 1. Recon summary

- **Stack signals**: React/TSX components, plain CSS, semantic CSS custom properties, Tailwind-style arbitrary animation class in `CommandPalette`, and an unknown JS `animateTo(...)` helper for drag release.
- **Where motion lives**:
  - Global tokens/rules: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline/utility animation: `src/components/CommandPalette.tsx`
  - Pointer-driven JS motion: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Tokens: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct precedent: button press uses `transform`, semantic duration/easing tokens, and `prefers-reduced-motion` keeps feedback at `80ms`.
- **Product personality**: calm, crisp, low-latency desktop operations UI. Motion should clarify cause/effect, not decorate or delay frequent work.
- **Frequency map**:
  - Very high: command palette, likely keyboard-triggered.
  - Medium/high: popovers in operational workflows.
  - Medium: sortable queue dragging when used.
  - Occasional: toasts.
- **Evidence level**: static snippet audit only. No runtime timing, computed style, browser validation, accessibility tree, performance trace, or device gesture validation was performed.

---

## 2. Vetted priority table

| # | Severity | Location | Evidence | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | `src/components/CommandPalette.tsx` | `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard UI is animated for `420ms` with `ease-in`, delaying the exact action operators expect to feel instant. | Remove command palette entrance/exit animation; rely on immediate open state and visible focus. |
| 2 | HIGH | `src/components/SortableQueue.tsx` | `setProperty("--drag-y", ...)` on `queueRef`; `animateTo(..., { duration: 400 })` | Drag motion is likely routed through a parent CSS variable and release uses a fixed `400ms` tween; this risks style recalculation, weak direct manipulation, and no velocity continuity. | Move the dragged item with direct `transform`; release with velocity-aware spring if supported; reduced motion snaps/settles quickly. |
| 3 | HIGH | `src/styles/motion.css` | `.popover { transform-origin: center; transition: all 360ms ease-in; }` | Popovers use `transition: all`, slow `ease-in`, over-budget duration, and center origin for a trigger-anchored surface. | Restrict to `transform, opacity`; use existing tokens; source origin from trigger/positioner; add reduced-motion duration. |
| 4 | MEDIUM | `src/components/toast.css` | `top` keyframes; `500ms ease-in` | Toast enter animates layout property `top`, lasts too long for operations UI, starts slowly, and lacks reduced-motion handling. | Animate `transform` + `opacity` only; shorten to `--duration-panel`; reduced motion keeps opacity feedback without vertical travel. |
| 5 | MEDIUM | Cross-cutting snippets | Button uses tokens/reduced motion; other excerpts bypass them | Motion system is inconsistent: semantic tokens exist, but several components hard-code `360/420/500ms`, `ease-in`, arbitrary classes, or no reduced-motion path. | Consolidate high-traffic motion onto existing tokens and the button precedent. |

---

## 3. Implementation-ready plans

### Plan 1 — Make command palette instant

**Files / current excerpt**

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

- Opening/closing the command palette should be immediate.
- No `420ms`, no `ease-in`, no keyframe/utility entrance motion.
- Feedback should come from state continuity and visible focus, not panel motion.
- Reduced Motion behavior is identical because the baseline has no movement.

**Project conventions**

- Prefer existing semantic tokens and local precedents when motion remains.
- Existing correct precedent:

```css
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove the arbitrary animation class.
2. Target shape:

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div data-open={open}>
      <SearchResults />
    </div>
  );
}
```

3. If another stylesheet depends on the removed class/keyframe only for visibility, replace that dependency with explicit open/closed state styling, not animation.
4. If a `palette` keyframe exists only for this component and becomes unused, remove it in the same change; if it is shared elsewhere, stop and report the shared usage.

**Hard boundaries**

- Do not change `SearchResults`.
- Do not add a new animation, fade, scale, or transition as a substitute.
- Do not change command behavior, keyboard shortcuts, search state, or focus management.
- If the class is required for mount/unmount correctness rather than decoration, stop and report before editing further.

**Mechanical checks**

- Search confirms `animate-[palette_420ms_ease-in_both]` is gone.
- Search confirms this component no longer references `420ms` or `ease-in`.
- Run the closest available lint/typecheck/build command if present.

**Runtime/feel checks for executor**

- Open via keyboard repeatedly: palette appears immediately with no perceptible easing delay.
- Close/reopen rapidly: no animation queues, no delayed visual state.
- Confirm visible focus remains clear on open.
- With Reduced Motion enabled: behavior is the same and still understandable.

**Reduced Motion behavior**

- No movement in either mode.
- Preserve focus visibility and state indication.

**Source-drift stop condition**

- Stop if the current file no longer contains the provided excerpt or if command palette visibility depends on the animation class for correctness.

---

### Plan 2 — Retokenize popover and toast motion

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

- Popovers feel responsive and causally connected to their trigger.
- Toasts enter without layout animation.
- Motion uses existing semantic duration/easing tokens.
- Reduced Motion keeps opacity/state feedback but removes vertical movement.

**Project conventions**

- Use:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Follow the button precedent: transform-only motion, tokenized duration/easing, `80ms` reduced-motion duration.

**Ordered steps**

1. In `src/styles/motion.css`, replace the popover rule with transform/opacity-only transitions:

```css
.popover {
  transform-origin: var(--popover-transform-origin, var(--transform-origin, center));
  transition:
    transform var(--duration-fast) var(--ease-responsive),
    opacity var(--duration-fast) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .popover {
    transition-duration: 80ms;
  }
}
```

2. Verify the popover implementation can set `--popover-transform-origin` or `--transform-origin` from its trigger/positioning system. If not, stop and report rather than leaving all trigger popovers centered by default.
3. If `.popover` is actually used for centered modal surfaces, do not apply this change globally. Split trigger-anchored popovers from centered dialogs first.
4. In `src/components/toast.css`, replace layout animation with transform/opacity:

```css
@keyframes toast-enter {
  from {
    transform: translateY(-24px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.toast {
  animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
}

@media (prefers-reduced-motion: reduce) {
  @keyframes toast-enter {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .toast {
    animation-duration: 80ms;
  }
}
```

**Hard boundaries**

- Do not introduce new duration/easing tokens unless the existing tokens are unavailable.
- Do not animate `top`, `left`, `width`, `height`, margin, or padding.
- Do not use `transition: all`.
- Do not change toast content, dismissal behavior, stacking logic, or ARIA behavior.
- Do not change modal/dialog origin unless the surface is confirmed trigger-anchored.

**Mechanical checks**

- Search confirms no `transition: all` remains on `.popover`.
- Search confirms no `.toast` enter animation uses `top`.
- Search confirms these excerpts no longer use `360ms ease-in` or `500ms ease-in`.
- Run lint/typecheck/build if available.

**Runtime/feel checks for executor**

- Popover: at slow playback, motion originates from the trigger/anchor, not the center.
- Popover: rapid open/close feels responsive and does not start with a sluggish delay.
- Toast: at slow playback, the element moves via transform; surrounding layout should not be pushed by the enter animation.
- Reduced Motion: popover still changes state quickly; toast fades in without vertical travel.

**Reduced Motion behavior**

- Popover: shorten transition to `80ms`.
- Toast: remove vertical movement; keep `80ms` opacity feedback.

**Source-drift stop condition**

- Stop if `.popover` is shared by centered modals/dialogs.
- Stop if no trigger-origin variable can be provided by the current popover implementation.
- Stop if toast mounting/unmounting is controlled by JS that conflicts with the proposed animation timing.

---

### Plan 3 — Make sortable queue drag direct and velocity-aware

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

- While dragging, the dragged item follows the pointer directly with `transform`.
- Do not update a parent CSS variable for every pointer move.
- On release, settle to the nearest slot with velocity continuity if the existing animation helper supports it.
- Reduced Motion preserves direct dragging but avoids a long animated glide on release.

**Project conventions**

- Use transform-based motion like the button precedent.
- Use existing durations where fixed timing is unavoidable:
  - normal small UI feedback: `--duration-fast` / `160ms`
  - reduced motion: `80ms`
- Do not add a new animation dependency.

**Ordered steps**

1. Identify the actual dragged element ref. If only `queueRef` exists and there is no per-item dragged ref, add the smallest local ref needed for the active dragged item.
2. Replace parent CSS variable updates with direct transform on the dragged element:

```tsx
function onPointerMove(event: PointerEvent) {
  const deltaY = event.clientY - dragStartY.current;
  draggedItemRef.current?.style.setProperty(
    "transform",
    `translate3d(0, ${deltaY}px, 0)`
  );
}
```

3. Track release velocity from recent pointer samples:

```tsx
const now = performance.now();
const dy = event.clientY - lastPointerY.current;
const dt = Math.max(now - lastPointerTime.current, 1);
velocityY.current = dy / dt;
lastPointerY.current = event.clientY;
lastPointerTime.current = now;
```

4. Replace fixed release timing:

```tsx
function onPointerUp() {
  setDragging(false);

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const targetY = nearestSlot(currentY);

  if (reduceMotion) {
    animateTo(targetY, { duration: 80 });
    return;
  }

  animateTo(targetY, {
    type: "spring",
    duration: 0.5,
    bounce: 0.2,
    velocity: velocityY.current,
  });
}
```

5. If `animateTo` does not support spring, bounce, or velocity options, stop and report. Do not approximate with another long fixed-duration tween.
6. Remove any CSS that consumes `--drag-y` for the dragged item once direct transform is in place.

**Hard boundaries**

- Do not change queue ordering rules.
- Do not change `nearestSlot(...)` behavior.
- Do not add a physics/gesture dependency.
- Do not animate layout properties.
- Do not apply transforms to the whole queue when only one item is being dragged.
- Do not invent a spring API if the existing `animateTo` helper cannot support it.

**Mechanical checks**

- Search confirms `setProperty("--drag-y"` is removed from `SortableQueue`.
- Search confirms `{ duration: 400 }` is removed from drag release.
- Typecheck confirms refs and pointer state are valid.
- Lint confirms no stale refs/state are left behind.

**Runtime/feel checks for executor**

- Drag slowly: item remains directly under the pointer with no laggy catch-up.
- Drag quickly and release: item settles in the direction/speed implied by the release, not as a generic fixed tween.
- Interrupt/re-drag during settlement: motion retargets from the current visual position.
- Reduced Motion: drag remains direct; release settles quickly without a long glide or bounce.

**Reduced Motion behavior**

- Direct pointer tracking remains because it is user-controlled feedback.
- Release animation uses `80ms` and no bounce/overshoot.

**Source-drift stop condition**

- Stop if there is no stable dragged-item element to transform directly.
- Stop if `animateTo` cannot accept spring/velocity options.
- Stop if current queue virtualization or layout measurement depends on `--drag-y` globally.

---

## 4. Recommended execution order

1. **Command palette instant open** — highest-frequency, smallest change, biggest throughput win.
2. **Popover/toast retokenization** — removes several systemic anti-patterns: `ease-in`, overlong UI durations, `transition: all`, layout animation, missing reduced-motion paths.
3. **Sortable queue drag** — high impact but requires source confirmation around refs, `animateTo`, and queue layout.

## Explicitly unverified states

- Whether `.popover` is trigger-anchored everywhere or shared with centered modal/dialog UI.
- Whether a positioning library exposes a transform-origin CSS variable.
- Whether `palette` keyframes exist elsewhere or affect mount/unmount behavior.
- Whether `animateTo` supports spring, velocity, interruptibility, or reduced-motion branching.
- Whether the sortable queue is virtualized or has layout measurement constraints.
- Actual frame rate, input latency, compositing behavior, focus behavior, screen-reader announcements, and perceived feel on real hardware.
