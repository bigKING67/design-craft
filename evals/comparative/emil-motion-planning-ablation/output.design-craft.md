## 1. Recon summary

Motion diagnosis: the shown system has one good local precedent, but the active surface snippets drift toward slow `ease-in`, ad-hoc durations, keyframe restarts, layout-property motion, and under-specified Reduced Motion for high-frequency operator workflows.

- **Stack signals**: React/TSX components, CSS custom-property tokens, component CSS, Tailwind-style arbitrary animation class, imperative pointer/animation code via `animateTo(...)`.
- **Where motion lives**:
  - Global tokens and `.popover`: `src/styles/motion.css`
  - Command palette entry/visibility: `src/components/CommandPalette.tsx`
  - Toast keyframes: `src/components/toast.css`
  - Drag/reorder gesture: `src/components/SortableQueue.tsx`
  - Correct local precedent: `src/components/Button.css`
- **Existing conventions**:
  - Semantic tokens: `--duration-fast`, `--duration-panel`, `--ease-responsive`
  - Preferred property pattern: transform-only transition
  - Reduced Motion precedent: shorten to `80ms` while preserving feedback
- **Product personality**: calm, crisp, non-decorative desktop operations motion; motion should explain causality without taxing keyboard-heavy repeated use.
- **Frequency map**:
  - Very high: command palette, buttons, queue dragging/reordering
  - Medium/high: popovers in operational workflows
  - Occasional: toasts
- **Evidence level**: static snippets only. No runtime smoothness, frame pacing, computed styles, browser behavior, focus behavior, or accessibility-tree state was verified.

## 2. Vetted priority table

| Priority | Evidence | Finding | Smallest safe correction |
|---|---|---|---|
| P1 | `CommandPalette.tsx`: `animate-[palette_420ms_ease-in_both]` | High-frequency keyboard surface uses slow ad-hoc keyframe timing and `ease-in`, which delays perceived response by design. Reduced Motion path is not shown. | Replace with tokenized opacity/very small transform transition, `var(--duration-fast)`, `var(--ease-responsive)`, and an explicit Reduced Motion branch. |
| P1 | `SortableQueue.tsx`: pointer move writes `--drag-y`; release uses `animateTo(..., { duration: 400 })` | Direct manipulation lacks demonstrated pointer capture, grab offset, presentation-value interruption, measured release velocity, and velocity handoff. Static evidence cannot prove feel, but the release API shown is fixed-duration. | Preserve existing `nearestSlot(currentY)` target semantics, but measure release velocity in CSS px/s and feed it into an interruptible settle primitive if the API supports it. |
| P2 | `motion.css`: `.popover { transform-origin: center; transition: all 360ms ease-in; }` | Broad `transition: all`, non-token duration/easing, and center origin are risky for anchored overlays. Static evidence does not prove anchoring, so origin must be conditional. | Transition only intended properties; use tokens; preserve center fallback via `var(--popover-origin, center)`. |
| P2 | `toast.css`: `top` keyframe over `500ms ease-in` | Toast entry animates a layout-position property and uses slow `ease-in`; no Reduced Motion branch is shown. Static evidence indicates performance/accessibility risk, not measured jank. | Keep layout position static, animate `transform` + `opacity`, tokenize duration/easing, add Reduced Motion opacity-only/short branch. |
| P2 | Button has Reduced Motion precedent; other shown motion does not | Reduced Motion handling is inconsistent across meaningful motion surfaces in the snippets. | Add local `prefers-reduced-motion: reduce` branches that remove/reduce spatial travel while keeping opacity/static state feedback. |
| P3 | Multiple hard-coded values: `360ms`, `420ms`, `500ms`, `400`, `ease-in` | Motion vocabulary is fragmenting away from semantic tokens and the product’s crisp-motion authority. | Normalize to existing tokens first; introduce no new token unless repeated need remains after implementation. |

## 3. Implementation plans

### Plan A — Normalize popover and command-palette overlay motion

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

- Popovers and command palette respond immediately and calmly.
- Use existing `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Avoid `transition: all`.
- Command palette should use minimal travel because it is keyboard-heavy.
- Reduced Motion should preserve open/closed feedback without meaningful spatial movement.

**Project conventions**

- Follow the button precedent: transform-based motion, semantic tokens, `80ms` Reduced Motion.
- Do not introduce decorative bounce, large scale, or new easing tokens.

**Ordered steps**

1. In `src/styles/motion.css`, replace `.popover` with property-specific transitions:

   ```css
   .popover {
     transform-origin: var(--popover-origin, center);
     transition:
       transform var(--duration-panel) var(--ease-responsive),
       opacity var(--duration-fast) var(--ease-responsive);
   }
   ```

2. Add a command-palette motion class in the existing loaded motion stylesheet, only if that stylesheet is confirmed global/imported:

   ```css
   .commandPaletteMotion {
     opacity: 1;
     transform: translateY(0) scale(1);
     transition:
       opacity var(--duration-fast) var(--ease-responsive),
       transform var(--duration-fast) var(--ease-responsive);
   }

   .commandPaletteMotion[data-open="false"] {
     opacity: 0;
     transform: translateY(-4px) scale(0.99);
   }
   ```

3. In `src/components/CommandPalette.tsx`, replace the arbitrary animation class:

   ```tsx
   className="commandPaletteMotion"
   ```

4. Add Reduced Motion in `src/styles/motion.css`:

   ```css
   @media (prefers-reduced-motion: reduce) {
     .popover,
     .commandPaletteMotion {
       transition-duration: 80ms;
     }

     .commandPaletteMotion,
     .commandPaletteMotion[data-open="false"] {
       transform: none;
     }
   }
   ```

**Hard boundaries**

- Do not change `SearchResults`.
- Do not change command filtering, focus management, keyboard shortcuts, or open/close state semantics.
- Do not invent new duration/easing tokens for this pass.
- Do not force popover origin away from `center` unless the component provides trigger-relative origin data.

**Mechanical checks**

- Run the project’s type check and lint commands if available, e.g. `npm run typecheck` and `npm run lint`.
- Search for remaining `animate-[palette_420ms_ease-in_both]` references.
- Search for `.popover` overrides that depend on `transition: all`.

**Runtime/feel checks to perform later**

- Open/close the command palette repeatedly via keyboard.
- Interrupt open/close rapidly.
- Verify the palette feels immediate and does not visually lag input.
- Verify popover opacity/transform still transition where expected.
- No browser/device validation was performed for this audit.

**Reduced Motion behavior**

- Palette: no translate/scale travel; opacity/state feedback remains over `80ms`.
- Popover: shortened transition; no additional travel introduced by this plan.

**Source-drift stop condition**

Stop before editing if `CommandPalette` no longer uses `data-open`, if the palette animation class has already been replaced, if `src/styles/motion.css` is not loaded globally, or if `.popover` has component-specific transition/property ownership elsewhere.

---

### Plan B — Convert toast entry from layout motion to tokenized transform feedback

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

- Toast appears promptly without animating `top`.
- Motion explains arrival but does not feel cinematic.
- Layout position remains stable; visual entrance uses `transform` and `opacity`.
- Reduced Motion uses opacity/static state feedback only.

**Project conventions**

- Use existing `--duration-panel` or `--duration-fast`; start with `--duration-panel` because toasts are occasional but should still be crisp.
- Use `--ease-responsive`.
- Match the button precedent for Reduced Motion duration: `80ms`.

**Ordered steps**

1. Replace keyframes in `src/components/toast.css`:

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
   ```

2. Ensure the resting layout position is owned outside the animation:

   ```css
   .toast {
     top: 0;
     animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;
   }
   ```

3. Add Reduced Motion:

   ```css
   @media (prefers-reduced-motion: reduce) {
     @keyframes toast-enter {
       from {
         transform: none;
         opacity: 0;
       }
       to {
         transform: none;
         opacity: 1;
       }
     }

     .toast {
       animation-duration: 80ms;
     }
   }
   ```

**Hard boundaries**

- Do not change toast content, dismissal timing, queueing, stacking, or ARIA/live-region behavior in this motion pass.
- Do not add `will-change` unless later measurement shows a benefit.
- Do not change positioning strategy beyond keeping the final `top: 0` state stable.

**Mechanical checks**

- Run CSS lint if available.
- Search for code that expects `toast-enter` to animate `top`.
- Confirm no duplicate `@keyframes toast-enter` definitions conflict.

**Runtime/feel checks to perform later**

- Trigger single and multiple toasts.
- Verify stacking still appears in the correct position.
- Verify no visual jump at animation end.
- Verify rapid toast creation does not restart unrelated existing toasts unexpectedly.
- No runtime behavior was observed during this audit.

**Reduced Motion behavior**

- Remove vertical travel.
- Preserve a short opacity fade so users still receive arrival feedback.
- Keep final layout and visibility unchanged.

**Source-drift stop condition**

Stop before editing if toast positioning/stacking has moved to another file, if `.toast` already has transform ownership for another purpose, or if `top` animation is intentionally part of a documented stacking algorithm.

---

### Plan C — Harden SortableQueue drag settle and interruption semantics

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

- Dragged item remains attached to the pointer without jumps.
- Release settle starts from the current presentation value.
- Existing target selection, `nearestSlot(currentY)`, is preserved unless product authority explicitly approves momentum-based target changes.
- Release velocity is measured in CSS px/s and handed into the settle animation where the animation API supports it.
- Reduced Motion removes elastic/large travel while preserving clear reorder state feedback.

**Project conventions**

- Prefer transform-driven movement.
- Keep high-frequency operator motion crisp and non-bouncy.
- Do not replace product semantics with physics semantics without explicit approval.

**Ordered steps**

1. Inspect the existing pointer-down path before editing. It must identify dragged item, pointer id, start Y, current presentation Y, and grab offset. If missing, add those before changing release behavior.
2. On pointer down after drag intent is confirmed:
   - call pointer capture on the active element if supported;
   - store `pointerId`;
   - store grab offset and starting presentation position;
   - initialize a short sample buffer using CSS pixels and monotonic timestamps.
3. On pointer move:
   - ignore events from non-active pointers;
   - compute movement relative to the stored start/grab offset, not raw `event.clientY` alone;
   - update the transform owner for the dragged item, not a broad parent variable, unless current CSS proves the parent variable is intentionally scoped;
   - keep hot-path work to style update/sample append only.
4. On pointer up/cancel:
   - release pointer capture;
   - compute release velocity from recent samples in CSS px/s;
   - set `dragging` false only after the visual owner can continue from the current presentation value;
   - choose target with existing `nearestSlot(currentY)` semantics;
   - call the animation primitive with current position and initial velocity.
5. If `animateTo` accepts only `{ duration: 400 }` and cannot accept current value/velocity, stop and introduce an adapter or supported primitive in a separate reviewed change rather than faking velocity handoff.
6. Optional, separately authorized only: compute a bounded projected endpoint for target selection, then choose the nearest slot to that endpoint. Do not make this the default plan.

**Hard boundaries**

- Do not change queue ordering rules, slot calculation semantics, persistence, selection, or keyboard reorder behavior.
- Do not add bounce by default.
- Do not add dependencies unless existing animation utilities cannot support presentation-value interruption and velocity handoff.
- Do not use global document listeners as a substitute for pointer capture unless compatibility requires a documented fallback.

**Mechanical checks**

- Run type check and lint, e.g. `npm run typecheck` and `npm run lint`, if those scripts exist.
- Add or update unit tests for `nearestSlot` preservation if slot logic is testable.
- Add pure tests for release-velocity calculation if extracted.

**Runtime/feel checks to perform later**

- Drag slowly, drag quickly, release near slot boundaries.
- Interrupt a settle by grabbing the item mid-animation.
- Move pointer outside the original item bounds while dragging.
- Cancel pointer interaction and verify state recovers.
- Verify no visual jump on pointer down, move, release, or interruption.
- Performance check under a populated queue should confirm no avoidable broad style recalculation; this was not measured here.

**Reduced Motion behavior**

- Keep direct tracking while dragging, because it is functional feedback.
- On release, use immediate or very short non-elastic settle, around the established `80ms` Reduced Motion precedent.
- Remove projection/overshoot/elastic effects.
- Preserve visible selected/dragging/drop-target state through static styling or opacity/color feedback.

**Source-drift stop condition**

Stop before editing if the pointer-down code already implements capture/grab offset/velocity, if `--drag-y` is consumed by CSS in a way that cannot be moved to the dragged item safely, if `animateTo` already wraps a spring with velocity support, or if target selection is documented as momentum-based rather than nearest-slot.

## 4. Recommended execution order

1. **Plan C first** if queue reordering is central to operator throughput; direct manipulation has the highest feel and correctness risk.
2. **Plan A second** to remove the most visible high-frequency token drift from keyboard and overlay workflows.
3. **Plan B third** as a bounded, low-risk cleanup for transient feedback.

Explicitly unverified states:

- Actual `palette` keyframes and whether they animate transform, opacity, or layout.
- Whether `src/styles/motion.css` is globally loaded.
- Popover anchoring, placement, and whether `center` is intentional for modal-like cases.
- Toast positioning, stacking, live-region behavior, and dismissal lifecycle.
- `animateTo` API capabilities.
- Existing pointer-down/cancel logic in `SortableQueue`.
- Computed styles, focus behavior, Reduced Motion behavior, frame pacing, and perceived smoothness.
