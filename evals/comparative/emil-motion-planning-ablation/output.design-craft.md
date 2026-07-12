Diagnosis: the motion system has a solid local precedent, but several high-value surfaces bypass it with long `ease-in` timings, broad property ownership, layout-position animation, and no static evidence of equivalent Reduced Motion handling.

## 1. Recon summary

- **Stack signals:** TSX components plus CSS; React-like component model; CSS keyframes/transitions; Tailwind-style arbitrary animation class; one imperative drag/settle path via `animateTo(...)`.
- **Where motion lives:**
  - Global tokens: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Component class animation: `src/components/CommandPalette.tsx`
  - Pointer-driven interaction: `src/components/SortableQueue.tsx`
- **Existing conventions:**
  - Tokens: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct local precedent: button uses transform-only motion, tokenized timing/easing, and a Reduced Motion branch that preserves feedback.
- **Product personality:** calm desktop operations console; motion should be crisp, quiet, causal, and throughput-preserving.
- **Frequency map:**
  - Very high: command palette, buttons, keyboard-heavy workflows.
  - High/direct manipulation: sortable queue drag/reorder.
  - Medium: popovers/dropdowns depending on use.
  - Occasional but repeatable: toasts.
- **Evidence level:** static snippets only. No computed style, runtime trace, frame-rate measurement, screen recording, browser validation, accessibility-tree inspection, or user testing was performed.

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | Static source | `src/components/CommandPalette.tsx` | Command palette uses `animate-[palette_420ms_ease-in_both]` on a keyboard-heavy surface. The duration/easing are outside the local crisp-token precedent. | Replace with tokenized opacity/transform transition or tokenized animation using `--duration-fast`/`--duration-panel` and `--ease-responsive`; add Reduced Motion behavior that preserves open/close feedback without spatial travel. |
| P1 | Static source | `src/components/SortableQueue.tsx` | Direct manipulation has a fixed `animateTo(..., { duration: 400 })`; supplied evidence does not show pointer capture, grab offset, velocity handoff, projected snap, interruption, transform ownership, or Reduced Motion. | Rework settle behavior around explicit gesture state, current presentation value, measured velocity, projected nearest slot, and Reduced Motion no-overshoot settle. Runtime validation required. |
| P2 | Static source | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in` and `transform-origin: center`; broad transition ownership and delayed-start easing conflict with crisp operations-console motion. | Limit properties to `opacity, transform`; use existing tokens; set trigger-relative origin when this is an anchored popover, preserving `center` only for genuinely centered overlays. |
| P2 | Static source | `src/components/toast.css` | Toast animates `top` from `-24px` to `0` over `500ms ease-in`; this is a layout-property animation risk and slow for workday feedback. | Convert to `transform: translateY(...)` plus opacity; shorten to tokenized timing/easing; add Reduced Motion crossfade/static-position feedback. |
| P2 | Static source | Multiple excerpts | Hard-coded `360ms`, `420ms`, `500ms`, `400` and `ease-in` appear beside existing semantic tokens. | Normalize listed motion to existing tokens first; only add new semantic tokens if repeated needs remain after component fixes. |
| P3 | Static source | `src/components/Button.css` | Positive precedent: transform-only active feedback with tokenized timing and Reduced Motion. | Preserve as reference; use its pattern as the implementation baseline for other small feedback motion. |

## 3. Implementation-ready plans

### Plan A — Normalize command palette and popover motion

**Current excerpts**

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

- Command palette opens/closes immediately enough for keyboard-heavy operators.
- Use opacity plus a very small transform only if it helps state continuity.
- Popovers transition only owned visual properties.
- Easing should feel responsive at the start, using `--ease-responsive`.
- Durations should use `--duration-fast` for small overlays or `--duration-panel` where panel scale requires slightly more continuity.

**Project conventions**

- Reuse `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Follow the button precedent: transform-only where possible, tokenized transition, Reduced Motion branch.
- Preserve visible focus and do not delay keyboard interaction.

**Ordered steps**

1. Inspect actual palette CSS/keyframes for `palette`; stop if it already encodes a broader state contract not shown here.
2. Replace `animate-[palette_420ms_ease-in_both]` with a state-driven class or CSS selector tied to `data-open`.
3. Implement palette open/closed styles using only `opacity` and `transform`.
4. Use `var(--duration-fast)` for the first pass; allow `var(--duration-panel)` only if the palette is visually large and runtime review shows `160ms` is too abrupt.
5. In `.popover`, replace `transition: all 360ms ease-in` with explicit properties, e.g. `opacity var(--duration-fast) var(--ease-responsive), transform var(--duration-fast) var(--ease-responsive)`.
6. Audit `.popover` positioning in source before changing `transform-origin`.
   - If anchored to a trigger, set origin from the trigger/placement mechanism or a placement class.
   - If truly centered, keep `center`.
7. Add Reduced Motion rules for palette and popover: remove/reduce translate/scale travel while preserving opacity or instant state feedback.
8. Search for remaining hard-coded palette/popover `ease-in`, `420ms`, `360ms`, and `transition: all` instances in these files.

**Hard boundaries**

- Do not change `SearchResults` data behavior.
- Do not alter focus management, keyboard shortcuts, or open/close state semantics.
- Do not introduce a new animation library.
- Do not replace semantic tokens with one-off cubic-beziers.
- Do not assert trigger-relative origin until actual placement source is inspected.

**Mechanical checks**

- Static search: no `animate-[palette_420ms_ease-in_both]` remains.
- Static search: `.popover` no longer uses `transition: all`.
- Static search: new motion uses existing duration/easing tokens.
- Run the project’s closest available type/lint/build checks after identifying scripts.

**Runtime/feel checks to perform later**

- Keyboard open/close palette repeatedly; confirm no perceived waiting before content is usable.
- Verify focus ring remains visible throughout open/close.
- Open popovers from each placement; confirm origin matches the trigger relationship.
- Test rapid open/close interruption for visual jumps.

**Reduced Motion behavior**

- Palette/popover should avoid meaningful spatial travel.
- Preserve feedback through opacity, immediate state change, focus, border, or background state.
- Do not remove feedback entirely.

**Source-drift stop condition**

- Stop before editing if `CommandPalette` no longer contains the cited arbitrary animation class, if `.popover` transition/origin have already changed materially, or if the motion tokens in `src/styles/motion.css` have been renamed/redefined.

---

### Plan B — Rebuild toast entrance as transform/opacity feedback

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

- Toasts should appear promptly without cinematic delay.
- Entrance should communicate arrival while avoiding layout-position animation.
- Motion should stay calm and non-blocking for repeated operational feedback.

**Project conventions**

- Use existing tokens from `src/styles/motion.css`.
- Prefer `transform` and `opacity`.
- Add Reduced Motion behavior equivalent to the button precedent.

**Ordered steps**

1. Inspect toast positioning CSS around `.toast` before editing; confirm whether `top` is also used for static placement.
2. Keep static placement separate from animation state.
3. Replace keyframe `top` changes with `transform: translateY(...)` and `opacity`.
4. Use `var(--duration-panel)` only if the toast travels a visible distance; otherwise use `var(--duration-fast)`.
5. Replace `ease-in` with `var(--ease-responsive)`.
6. Ensure final state is stable without requiring animated `top`.
7. Add `@media (prefers-reduced-motion: reduce)` branch:
   - no vertical travel, or at most a very small transform;
   - shorter duration or immediate transform;
   - opacity/static state feedback preserved.
8. Search for other toast animation declarations before assuming this is the only toast path.

**Hard boundaries**

- Do not change toast queueing, dismissal timing, z-index, or content.
- Do not animate layout properties for the entrance.
- Do not add `will-change` unless runtime measurement shows benefit.
- Do not make toasts invisible until JavaScript starts.

**Mechanical checks**

- Static search: `toast-enter` no longer animates `top`.
- Static search: `.toast` no longer uses `500ms ease-in`.
- Static search: Reduced Motion branch exists for toast motion.
- Run the project’s closest available CSS/lint/build checks after identifying scripts.

**Runtime/feel checks to perform later**

- Trigger one toast and several consecutive toasts.
- Confirm toast placement does not shift surrounding layout.
- Confirm entrance is noticeable but does not steal attention from keyboard work.
- Confirm dismissal behavior, if separately animated, remains coherent.

**Reduced Motion behavior**

- Remove vertical travel.
- Preserve arrival feedback through opacity or immediate static presentation.
- Keep dismissal feedback similarly restrained if dismissal animation exists.

**Source-drift stop condition**

- Stop before editing if `toast-enter` no longer animates `top`, if `.toast` no longer owns entrance animation, or if toast positioning depends on `top` in a way that requires a broader layout decision.

---

### Plan C — Make sortable queue settle interaction physically coherent

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

- Dragged queue item tracks the pointer 1:1 after drag intent is established.
- Release settles to a slot based on current position plus measured velocity/projection, not only the last logical value.
- Interruption starts from the current on-screen value without jumping.
- Reduced Motion removes large travel/overshoot while preserving clear reorder feedback.

**Project conventions**

- Preserve existing component API unless source inspection proves a safer internal boundary.
- Prefer transform ownership for drag movement.
- Avoid broad style recalculation in hot pointer paths where possible.
- Do not add dependencies unless existing project animation utilities cannot read current value/velocity and the tradeoff is approved.

**Ordered steps**

1. Inspect the full component before editing:
   - item DOM structure;
   - how `--drag-y` is consumed;
   - whether transform is also used for press/hover;
   - `animateTo` implementation/signature;
   - how `currentY` is updated.
2. Define the coordinate space explicitly: CSS pixels relative to the queue/container, not raw viewport `clientY`, unless current CSS proves viewport coordinates are intended.
3. On pointer down, store:
   - active pointer id;
   - initial pointer position;
   - item start position;
   - grab offset;
   - recent pointer samples with timestamps.
4. Use pointer capture once drag intent is confirmed.
5. During pointer move, update only the active item’s transform/presentation value where possible; avoid parent-level variables if they invalidate a large subtree.
6. Track velocity from recent samples in CSS px/s.
7. On pointer up/cancel:
   - release pointer capture;
   - compute projected endpoint from current presentation position and velocity;
   - choose `nearestSlot(projectedEndpoint)`;
   - settle from current presentation value, not from stale `currentY`.
8. Replace fixed `duration: 400` with an existing spring/settle primitive if available; otherwise use bounded tokenized duration as a fallback with no bounce.
9. Add Reduced Motion branch:
   - no overshoot/bounce;
   - shortest practical settle;
   - clear static reorder/focus/selection feedback preserved.
10. Add cancellation handling for pointer cancel/lost capture.

**Hard boundaries**

- Do not change queue ordering business rules.
- Do not alter item identity/keying without a separate data-flow review.
- Do not block input until settle animation completes.
- Do not let drag translate and press scale compete for the same raw `transform` string without a composed owner or wrapper split.
- Do not claim gesture quality without runtime interaction testing.

**Mechanical checks**

- Static search: no remaining hard-coded `duration: 400` settle for this interaction unless justified as fallback.
- Type/lint check for pointer event types and cleanup paths.
- Unit or component test, if available, for nearest-slot selection and cancel/up paths.
- Static inspection confirms pointer capture cleanup and no leaked active pointer state.

**Runtime/feel checks to perform later**

- Drag slowly, quickly, and outside queue bounds.
- Release with low and high velocity; confirm projected slot selection feels causal.
- Interrupt a settle by grabbing again; confirm no visual jump.
- Verify keyboard/focus behavior for the reordered item remains visible.
- Check under realistic queue length; measure if pointer updates touch large subtrees.

**Reduced Motion behavior**

- Maintain direct manipulation while dragging.
- On release, use immediate or very short no-overshoot settle.
- Preserve reorder confirmation through position, focus, outline, or static state feedback.

**Source-drift stop condition**

- Stop before editing if `--drag-y` is no longer the drag presentation channel, if `animateTo` signature/semantics differ from the excerpt, if queue coordinates are already container-relative with velocity support, or if a separate drag library owns this interaction.

## 4. Recommended execution order

1. **Plan A:** fixes the highest-frequency keyboard/overlay motion and establishes the tokenized pattern.
2. **Plan B:** low-risk CSS-only correction for toast feedback and layout-animation risk.
3. **Plan C:** highest interaction complexity; do after the token/Reduced Motion pattern is settled, with dedicated runtime validation time.

## Explicitly unverified states

- Actual rendered durations/easing after CSS cascade.
- Whether `palette` keyframes exist elsewhere and what properties they animate.
- Popover placement model and whether `center` origin is intentional.
- Toast queueing/dismissal behavior and final computed positioning.
- Sortable queue DOM size, transform ownership, `animateTo` behavior, and gesture feel.
- Reduced Motion behavior beyond the shown button precedent.
- Frame pacing, compositing, layout shifts, accessibility-tree behavior, and keyboard/focus runtime behavior.
