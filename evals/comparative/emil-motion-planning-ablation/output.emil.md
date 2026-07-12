## 1. Recon summary

- **Stack signals**: React/TSX components, plain CSS, CSS custom-property motion tokens, Tailwind-style arbitrary animation class, and a bespoke `animateTo(...)` gesture settle helper. No motion library is evidenced.
- **Where motion lives**:
  - Global tokens/selectors: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility class: `src/components/CommandPalette.tsx`
  - Pointer-driven JS: `src/components/SortableQueue.tsx`
- **Existing conventions**:
  - Semantic durations: `--duration-fast: 160ms`, `--duration-panel: 240ms`
  - Responsive curve: `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct local precedent: button press uses transform-only feedback, tokenized timing, and a Reduced Motion override.
- **Product personality**: calm, crisp desktop operations console. Motion should be causal and nearly invisible, not decorative or throughput-reducing.
- **Frequency map**:
  - Very high: `CommandPalette`, keyboard-driven workflow surfaces.
  - High during interaction: `SortableQueue` pointer movement/settle.
  - Medium/high: popovers in an operations console.
  - Occasional: toasts.
  - Existing good precedent: buttons.
- **Evidence level**: static snippets only. No runtime, computed-style, trace, screen recording, accessibility-tree, device, browser, or user validation was performed. Line numbers are unavailable from the supplied evidence.

## 2. Vetted priority table

| # | Severity | Category | Location | Finding | Fix summary |
|---|---:|---|---|---|---|
| 1 | HIGH | Purpose/frequency, easing | `src/components/CommandPalette.tsx` | High-frequency keyboard UI uses `animate-[palette_420ms_ease-in_both]`. Static evidence shows a long `ease-in` animation on a likely repeated command surface. | Remove open/close animation from the command palette; preserve instant state/focus feedback. |
| 2 | HIGH | Performance, easing, cohesion | `src/styles/motion.css` | `.popover` uses `transition: all 360ms ease-in;`. This bypasses tokens, may animate unintended properties, exceeds small-popover timing, and starts slowly. | Replace with explicit `transform, opacity` transitions using existing duration/easing tokens. |
| 3 | MEDIUM | Physicality/origin | `src/styles/motion.css` | `.popover { transform-origin: center; }` is suspicious for trigger-anchored popovers. Static evidence does not prove which popover primitive is used. | Use a trigger-origin CSS variable with safe fallback; stop if the component is actually a centered modal-like surface. |
| 4 | MEDIUM | Performance, accessibility | `src/components/toast.css` | Toast entry animates `top` for `500ms ease-in` and has no evidenced Reduced Motion path. | Animate `transform` + `opacity`, shorten timing, and add Reduced Motion that keeps opacity feedback without vertical travel. |
| 5 | HIGH | Gesture performance, interruptibility | `src/components/SortableQueue.tsx` | Pointer movement writes `--drag-y` on `queueRef.current`; settle uses fixed `duration: 400`. This is risky for high-frequency drag because parent CSS-var writes can fan out style recalculation and fixed tweens may not preserve gesture continuity. | Drive the dragged element’s `transform` directly; shorten or spring/retarget settle; add Reduced Motion branch. |
| 6 | MEDIUM | Cohesion/accessibility | Cross-cutting snippets | Button shows the desired tokenized + Reduced Motion precedent, while popover, palette, toast, and queue bypass it. | Standardize on existing tokens and local Reduced Motion behavior rather than one-off timings/classes. |

## 3. Implementation plans

### Plan 1 — Tokenize CSS entrances and remove layout animation

**Files/current excerpts**

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

- Popovers feel immediate and anchored, with explicit `transform`/`opacity` transitions only.
- Toasts enter with composited movement, not `top`, and complete quickly.
- Reduced Motion keeps feedback through opacity while removing vertical travel where possible.

**Project conventions**

- Reuse existing semantic tokens from `src/styles/motion.css`.
- Follow the correct precedent in `src/components/Button.css`:

```css
.button {
  transition: transform var(--duration-fast) var(--ease-responsive);
}

@media (prefers-reduced-motion: reduce) {
  .button { transition-duration: 80ms; }
}
```

**Ordered steps**

1. In `src/styles/motion.css`, replace the `.popover` block with explicit properties:

```css
.popover {
  transform-origin: var(--radix-popover-content-transform-origin, var(--transform-origin, center));
  transition:
    transform var(--duration-panel) var(--ease-responsive),
    opacity var(--duration-panel) var(--ease-responsive);
}
```

2. Add a Reduced Motion override in `src/styles/motion.css`:

```css
@media (prefers-reduced-motion: reduce) {
  .popover {
    transition:
      opacity 80ms var(--ease-responsive),
      transform 80ms var(--ease-responsive);
  }
}
```

3. In `src/components/toast.css`, replace the toast keyframes with transform-based movement:

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
  animation: toast-enter 200ms var(--ease-responsive) forwards;
}
```

4. Add a Reduced Motion override to `src/components/toast.css`:

```css
@media (prefers-reduced-motion: reduce) {
  @keyframes toast-enter {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .toast {
    animation-duration: 120ms;
  }
}
```

**Hard boundaries**

- Do not change popover markup, placement logic, z-index, focus handling, or visibility state.
- Do not introduce new tokens unless existing token names are absent in the real file.
- Do not animate `top`, `left`, `width`, `height`, margin, or padding.
- If `.popover` is confirmed to be a centered modal rather than a trigger-anchored popover, stop and do not change `transform-origin`.
- If either exact current excerpt is not present, stop and report source drift.

**Mechanical checks**

- Search targeted CSS for `transition: all`, `360ms ease-in`, `500ms ease-in`, and `top:` inside `toast-enter`; none should remain in these excerpts.
- Run the project’s existing lint/typecheck/build commands if available. If package scripts are unknown, record that mechanical validation is limited to static inspection.

**Runtime/feel checks**

- Open/close a popover repeatedly and confirm it starts promptly rather than easing in slowly.
- In slow playback, confirm popover motion uses its trigger-origin when the underlying primitive exposes one; otherwise it should safely fall back without breaking.
- Trigger a toast and confirm it slides a short distance without pushing layout.
- No browser/device validation was performed as part of this audit; these are executor checks.

**Reduced Motion behavior**

- Popover: shortened feedback, no long travel.
- Toast: opacity feedback remains; vertical movement is removed.

**Source-drift stop condition**

- Stop if the supplied `.popover`, `toast-enter`, or `.toast` snippets no longer match closely enough to make the edits mechanically.

---

### Plan 2 — Remove command palette open animation

**File/current excerpt**

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

- Command palette state changes should not be slowed by decorative entrance motion.
- Opening from keyboard should feel instant and preserve focus/causality.
- Reduced Motion path is identical to default because there is no movement to reduce.

**Project conventions**

- Existing design direction favors crisp motion and visible focus.
- Use the button precedent only for tactile press feedback, not for high-frequency palette open/close animation.
- Do not add new animation tokens for this surface.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, remove the arbitrary animation utility from the wrapper:

```tsx
export function CommandPalette({ open }: { open: boolean }) {
  return (
    <div data-open={open}>
      <SearchResults />
    </div>
  );
}
```

2. If the real component has additional class names not shown, remove only `animate-[palette_420ms_ease-in_both]` and preserve all layout, theme, focus-ring, and state classes.
3. Search for the `palette` keyframes or Tailwind animation definition. If it is unused after this change, remove only that unused palette animation definition in the same change; otherwise leave it.

**Hard boundaries**

- Do not change command search behavior, keyboard shortcuts, focus management, result rendering, or open-state logic.
- Do not replace the removed animation with fade, scale, blur, or stagger.
- Do not add a dependency or motion library.
- If the component depends on animation end events for mounting/unmounting, stop and report; do not improvise.

**Mechanical checks**

- Search for `animate-[palette_420ms_ease-in_both]`; it should not remain on the command palette.
- Type-check the TSX file with the project’s existing command if available.
- If unused keyframes are removed, search for `palette` references before deleting.

**Runtime/feel checks**

- Open the command palette via keyboard several times in a row.
- Confirm the palette is available immediately and search input focus is not delayed.
- Confirm there is no visual “wait” before the first typed character appears.
- Confirm visible focus remains intact.

**Reduced Motion behavior**

- Same as default: no movement animation.
- Any existing focus/selection feedback should remain visible.

**Source-drift stop condition**

- Stop if the exact animation class is absent, renamed, or tied to lifecycle cleanup logic.

---

### Plan 3 — Make sortable drag motion direct, interruptible, and reduced-motion aware

**File/current excerpt**

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

- During drag, update only the actively dragged element or drag layer with `transform`.
- Avoid parent-level CSS-variable writes for every pointer move.
- Settle should feel continuous from the drag and should not use a slow fixed 400ms UI tween.
- Reduced Motion should preserve final placement feedback with shorter, gentler movement.

**Project conventions**

- Prefer transform-only motion, as shown by the button precedent.
- Use existing timing tokens where practical:
  - fast feedback: `160ms`
  - panel/settle ceiling: `240ms`
  - responsive curve: `cubic-bezier(0.23, 1, 0.32, 1)`

**Ordered steps**

1. Inspect the real `SortableQueue.tsx` for the dragged item ref or drag-layer element.
2. If a dragged element ref exists, change pointer movement from parent CSS-var writes to direct transform writes:

```tsx
function onPointerMove(event: PointerEvent) {
  draggedItemRef.current?.style.setProperty(
    "transform",
    `translate3d(0, ${event.clientY}px, 0)`
  );
}
```

3. If the current coordinate system expects a delta rather than viewport `clientY`, preserve the existing math and apply only the resulting Y value through `translate3d(0, ${y}px, 0)`.
4. Replace the fixed 400ms settle with a shorter token-aligned duration unless an existing spring helper is already present:

```tsx
function onPointerUp() {
  setDragging(false);
  animateTo(nearestSlot(currentY), {
    duration: 240,
    easing: "cubic-bezier(0.23, 1, 0.32, 1)",
  });
}
```

5. If `animateTo` already supports spring parameters and the project has an existing spring convention, use that existing convention instead of inventing one. Otherwise keep the explicit 240ms responsive settle.
6. Add a Reduced Motion branch using the project’s existing reduced-motion helper if present. If no helper exists, use `window.matchMedia("(prefers-reduced-motion: reduce)")` at the interaction boundary and shorten settle:

```tsx
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

animateTo(nearestSlot(currentY), {
  duration: prefersReducedMotion ? 80 : 240,
  easing: "cubic-bezier(0.23, 1, 0.32, 1)",
});
```

**Hard boundaries**

- Do not change sorting rules, nearest-slot calculation, queue data, keyboard ordering, or persistence.
- Do not add a new animation library.
- Do not apply transforms to the whole queue if only one item is dragged.
- Do not keep both `--drag-y` parent updates and direct element transforms.
- If there is no stable dragged element or drag-layer ref, stop and report that a safe implementation requires identifying the active visual element first.

**Mechanical checks**

- Search this file for `style.setProperty("--drag-y"`; it should be removed or no longer used for per-pointer drag motion.
- Search for `duration: 400` in sortable settle code; it should be replaced for this interaction.
- Run existing type-check/lint commands if available.

**Runtime/feel checks**

- Drag an item slowly and quickly; confirm the dragged item tracks the pointer without moving unrelated children through inherited CSS variables.
- Release near a slot; confirm settle is crisp and does not feel like a delayed glide.
- Interrupt by starting another drag quickly after release; confirm no stale transform remains on the previous item.
- In slow playback, confirm only transform changes during drag/settle.

**Reduced Motion behavior**

- Drag tracking remains direct because it is user-controlled.
- Programmatic settle duration shortens to `80ms`; avoid extra bounce or decorative travel.

**Source-drift stop condition**

- Stop if `animateTo` does not accept `duration`/`easing`, if the coordinate system is unclear, or if no dragged element/ref can be identified safely.

## 4. Recommended execution order

1. **Plan 2 — Command palette**: highest throughput impact, smallest safest change.
2. **Plan 1 — CSS entrances**: removes broad `transition: all`, slow `ease-in`, and layout animation from shared/component CSS.
3. **Plan 3 — Sortable queue**: important but requires inspecting real drag structure and `animateTo` API before editing.

## Explicitly unverified states

- Actual line numbers, package manager, build scripts, Tailwind config, keyframe definitions, and whether the palette animation is referenced elsewhere.
- Whether `.popover` is backed by a trigger-origin primitive or is actually used for centered modal-like content.
- Actual command palette mount/unmount lifecycle and focus behavior.
- Actual toast stacking/dismiss behavior.
- Actual sortable DOM structure, drag-layer refs, coordinate math, and `animateTo` API.
- Runtime performance, computed styles, accessibility tree, browser behavior, and device feel.

Internal frontend/accessibility and quality planning guardrails were applied. No files were edited or created.
