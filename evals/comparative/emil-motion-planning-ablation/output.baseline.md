No files were edited. This is a static-evidence audit only.

## 1. Recon summary

**Stack signals**
- React/TSX components with CSS styling.
- Global CSS motion tokens in `src/styles/motion.css`.
- Component-scoped CSS in `src/components/toast.css` and `src/components/Button.css`.
- Utility-style arbitrary animation class in `CommandPalette.tsx`, likely compiled by the styling pipeline.
- Imperative pointer animation in `SortableQueue.tsx`.

**Where motion currently lives**
- Shared tokens: `src/styles/motion.css`.
- Local component precedent: `src/components/Button.css`.
- Inline/arbitrary component animation: `src/components/CommandPalette.tsx`.
- Component keyframes: `src/components/toast.css`.
- Imperative drag/snap behavior: `src/components/SortableQueue.tsx`.

**Existing conventions**
- Semantic duration tokens exist:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
- Semantic easing exists:
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Correct local precedent uses:
  - transform-only transition
  - tokenized duration/easing
  - Reduced Motion override that preserves feedback at `80ms`

**Product personality**
- Calm, crisp, desktop operations console.
- Motion should clarify cause/effect and state continuity.
- Motion should not create delay for keyboard-heavy support/revenue workflows.

**Frequency map, based only on component roles**
- Very high frequency: buttons, command palette, sortable queue interactions.
- Medium/high frequency: popovers.
- Intermittent but attention-sensitive: toasts.
- No runtime frequency measurement was performed.

**Evidence level**
- Static snippets only.
- No computed styles, browser validation, device testing, traces, accessibility tree, screen recording, or user testing.

---

## 2. Priority table

| Priority | Finding | Static evidence | Why it matters | Target direction |
|---:|---|---|---|---|
| P0 | Motion contract is fragmented | Tokens exist, but palette/toast/drag use hardcoded `420ms`, `500ms`, `400`, `ease-in`, and arbitrary animation syntax | Inconsistent tempo can make a workday console feel less predictable | Route common UI motion through existing semantic tokens and Reduced Motion convention |
| P0 | Popover uses broad transition and slow accelerating ease | `.popover { transition: all 360ms ease-in; }` | `all` can animate unintended properties; `ease-in` delays perceived response | Restrict to `opacity, transform`; use `--duration-panel` or `--duration-fast` and `--ease-responsive` |
| P0 | Command palette animation is long, hardcoded, and not visibly Reduced Motion-aware | `animate-[palette_420ms_ease-in_both]` | Command palette is likely high-frequency for keyboard operators; 420ms may feel like throughput friction | Use tokenized transform/opacity state transition; add Reduced Motion path preserving open/close feedback |
| P1 | Toast enters by animating layout property | `@keyframes toast-enter { from { top: -24px; ... } }` and `500ms ease-in` | Animating `top` is less aligned with transform-only precedent; 500ms may overemphasize transient feedback | Animate `transform` + `opacity`; shorten to token duration; Reduced Motion uses brief opacity/position confirmation |
| P1 | Sortable queue snap duration is hardcoded and pointer updates are direct per event | `setProperty("--drag-y", ...)`; `animateTo(... { duration: 400 })` | Drag/drop is task-critical; motion should track causality without lingering | Use frame-coalesced updates if needed; reduce snap duration; honor Reduced Motion with near-immediate settle |
| P2 | Focus continuity is an explicit requirement but not evidenced here | No focus excerpts provided | Keyboard-heavy workflows depend on visible focus through animated state changes | Treat focus as a required implementation checkpoint, not as a proven defect from these snippets |

---

## 3. Implementation plans

### Plan A — Normalize overlay motion for popovers and command palette

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
- Popovers and command palette open/close with short, crisp opacity/transform motion.
- No `transition: all`.
- No hardcoded long overlay durations.
- Command palette remains responsive for keyboard-heavy use.
- Reduced Motion still communicates state change, but with minimal duration/displacement.

**Project conventions to apply**
- Use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the button precedent: transform-based motion, tokenized timing, `80ms` Reduced Motion path.
- Preserve visible focus; do not hide outlines during animation.

**Ordered steps**
1. Inspect actual full contents of:
   - `src/styles/motion.css`
   - `src/components/CommandPalette.tsx`
   - any existing `palette` keyframes or `.popover` state selectors.
2. Replace `.popover` broad transition with explicit properties only:
   - `opacity`
   - `transform`
3. Change popover timing from `360ms ease-in` to tokenized timing:
   - default candidate: `var(--duration-panel) var(--ease-responsive)`
   - if popovers are tiny/contextual, use `var(--duration-fast)`.
4. Replace the arbitrary command palette animation class with a stable class, for example:
   - `className="command-palette"`
   - keep `data-open={open}`.
5. Add tokenized state styles in the existing motion stylesheet or the component’s existing style location, depending on actual project conventions:
   - closed: slightly translated/scaled and transparent
   - open: neutral transform and opaque
6. Add Reduced Motion overrides:
   - duration `80ms`
   - remove or minimize translate/scale
   - preserve opacity/state feedback.
7. Re-check that focus styles are not removed or visually obscured by the new styles.

**Hard boundaries**
- Do not redesign command palette layout.
- Do not change search behavior, keyboard handling, filtering, or focus management unless existing code requires a className merge.
- Do not introduce a new animation library.
- Do not create new global tokens unless existing tokens are insufficient after inspecting the full file.

**Mechanical checks**
- Search for remaining instances of:
  - `transition: all`
  - `420ms`
  - `360ms`
  - `ease-in`
  - `animate-[palette`
- Run the closest available type/lint/build check for the frontend.
- Confirm CSS syntax compiles under the project’s styling pipeline.

**Runtime / feel checks to perform later**
- Open/close command palette by keyboard repeatedly.
- Confirm perceived response starts immediately.
- Confirm focus remains visible before, during, and after open/close.
- Open/close popovers in dense UI areas and confirm no sluggishness or surprise property animation.

**Reduced Motion behavior**
- Keep state change visible.
- Prefer opacity-only or near-opacity-only transition.
- Use `80ms` duration, matching the existing button precedent.

**Source-drift stop condition**
- Stop before editing if:
  - `.popover` is used for multiple unrelated components with incompatible state models.
  - `palette` keyframes are shared elsewhere.
  - the command palette unmounts immediately on close, making close-state CSS impossible without component lifecycle changes.

---

### Plan B — Rework toast enter motion to transform/opacity

**File / current excerpt**

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
- Toast appears promptly without animating layout-position properties.
- Motion is noticeable enough for feedback but not dominant.
- Toast movement is shorter and calmer.
- Reduced Motion keeps feedback through a brief opacity change or instant positional state.

**Project conventions to apply**
- Use existing duration/easing tokens.
- Prefer `transform` over `top`.
- Keep Reduced Motion feedback instead of removing it entirely.

**Ordered steps**
1. Inspect full `src/components/toast.css` for positioning, stacking, exit animations, and variants.
2. Replace keyframe movement from `top` to `transform`, for example:
   - from: `transform: translateY(-8px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
3. Replace `500ms ease-in` with:
   - `var(--duration-panel) var(--ease-responsive)` for standard toast entrance, or
   - `var(--duration-fast)` if toasts are frequent and should feel more immediate.
4. Ensure `.toast` has a stable final transform state.
5. Add a Reduced Motion override:
   - shorten to `80ms`
   - remove translate distance or reduce it to zero
   - preserve opacity feedback.
6. If there is an exit animation in the full file, align it with the same token/easing system.

**Hard boundaries**
- Do not change toast copy, severity styling, queueing, dismissal logic, or stacking behavior.
- Do not alter layout offsets unless current `top` animation is also being used as static positioning.
- Do not add decorative bounce, spring, overshoot, or attention-grabbing motion.

**Mechanical checks**
- Search for:
  - `toast-enter`
  - `.toast`
  - `top: -24px`
  - `500ms`
- Confirm no remaining toast keyframe animates `top`.
- Run the closest available CSS/build/lint check.

**Runtime / feel checks to perform later**
- Trigger success, error, and neutral toasts if available.
- Confirm toast does not feel delayed.
- Confirm stacked toasts, if supported, do not visually jump.
- Confirm dismissal timing still reads clearly.

**Reduced Motion behavior**
- Toast should appear in final position.
- Use `80ms` opacity feedback or equivalent minimal confirmation.
- Do not silently remove all feedback.

**Source-drift stop condition**
- Stop before editing if:
  - `top` is used by JS to calculate stacking or collision.
  - the same keyframes are reused for non-toast surfaces.
  - there are multiple toast systems and this file is not the active one.

---

### Plan C — Make sortable queue drag/snap motion throughput-safe

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
- Drag motion tracks pointer causality directly.
- Drop/snap motion is brief and clear, not lingering.
- Pointer movement updates avoid unnecessary per-event style work where practical.
- Reduced Motion preserves final-placement feedback with minimal interpolation.

**Project conventions to apply**
- Align timing with existing semantic durations:
  - likely `--duration-fast` for snap feedback
  - avoid hardcoded `400`.
- Keep interaction responsive for high-throughput queue operations.
- Preserve keyboard/focus behavior if sortable controls support it.

**Ordered steps**
1. Inspect full `src/components/SortableQueue.tsx` for:
   - `currentY` source of truth
   - `animateTo` implementation/import
   - cleanup on unmount
   - pointer capture/release
   - keyboard sorting support
   - CSS use of `--drag-y`.
2. Search for all `animateTo(` calls to understand duration conventions.
3. If pointer events are frequent and direct style writes are not already coalesced elsewhere, introduce requestAnimationFrame coalescing around the CSS variable update.
4. Ensure pending animation frame is cancelled on pointer up and unmount.
5. Replace hardcoded snap duration:
   - default candidate: `160ms`
   - use the existing token value if `animateTo` accepts numeric milliseconds only.
6. Add or route through an existing Reduced Motion signal:
   - reduced: `0–80ms` snap, no long interpolation
   - still update final slot visibly.
7. Confirm `nearestSlot(currentY)` still receives the correct final coordinate after any coalescing change.

**Hard boundaries**
- Do not rewrite sorting architecture.
- Do not change item ordering semantics.
- Do not introduce virtualization or a drag/drop dependency.
- Do not change persistence, queue data model, or revenue/support workflow logic.
- Do not claim performance improvement without measurement.

**Mechanical checks**
- Search for:
  - `--drag-y`
  - `onPointerMove`
  - `onPointerUp`
  - `animateTo(`
  - `duration: 400`
- Type-check the component.
- Confirm cleanup paths for animation frames and pointer state.

**Runtime / feel checks to perform later**
- Drag slowly, quickly, and across multiple slots.
- Drop near slot boundaries.
- Confirm snap feels causal and does not delay the next operation.
- Confirm keyboard sorting/focus state, if present, remains visible and predictable.
- Check Reduced Motion mode separately.

**Reduced Motion behavior**
- Drag should still follow the pointer.
- Drop should settle immediately or within `80ms`.
- Preserve final-slot confirmation through position, focus, or non-motion visual state.

**Source-drift stop condition**
- Stop before editing if:
  - `animateTo` uses physics parameters rather than milliseconds.
  - `currentY` is not the same coordinate space as `event.clientY`.
  - `--drag-y` drives layout instead of transform.
  - sorting already has an animation abstraction that should be used instead.

---

## 4. Recommended execution order

1. **Plan A first** — establishes the shared overlay motion contract and removes the most obvious hardcoded/high-frequency mismatch.
2. **Plan B second** — low-risk improvement that aligns toast feedback with transform/token conventions.
3. **Plan C third** — highest interaction sensitivity; inspect more code before changing because drag state, coordinates, and animation utilities may have hidden coupling.

## Explicitly unverified states

- No browser/device validation was performed.
- No computed CSS was inspected.
- No runtime animation timing was measured.
- No performance trace was captured.
- No accessibility tree or screen reader behavior was checked.
- No actual focus-ring behavior was verified.
- No user frequency analytics or task-throughput data was available.
- No source outside the provided snippets was inspected.

Planning guardrails applied: smallest-change, evidence-first implementation discipline; frontend accessibility, focus, and Reduced Motion constraints.
