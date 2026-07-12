## 1. Recon summary

**Stack signals**
- CSS custom properties are already present for motion timing/easing.
- Component styling appears mixed: global CSS, component CSS, and utility/arbitrary animation classes.
- React/TSX components use state/data attributes for UI state.

**Where motion lives**
- `src/styles/motion.css`: global motion tokens and `.popover`.
- `src/components/CommandPalette.tsx`: inline arbitrary animation class.
- `src/components/toast.css`: keyframes and toast animation.
- `src/components/SortableQueue.tsx`: imperative drag/update animation.
- `src/components/Button.css`: local precedent for tokenized, reduced-motion-aware interaction.

**Existing conventions**
- Semantic tokens:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Good precedent:
  - animate `transform`
  - use semantic duration/easing tokens
  - reduced motion shortens feedback to `80ms` rather than removing it entirely

**Product personality**
- Calm, crisp, workday-long desktop console.
- Motion should explain causality and state continuity without delaying keyboard-heavy workflows.

**Frequency map**
- Highest frequency: sortable queue drag/release, command palette, button feedback.
- Medium frequency: popovers.
- Lower frequency but attention-sensitive: toast entry.

**Evidence level**
- Static excerpt audit only.
- No runtime, computed-style, browser, device, trace, accessibility-tree, or user-test validation was performed.
- Findings below are implementation risks inferred from source snippets, not observed runtime defects.

---

## 2. Vetted priority table

| Priority | Finding | Static evidence | Why it matters | Target |
|---|---|---|---|---|
| P0 | Reduced Motion coverage is inconsistent | Button has a reduced path; popover, command palette, toast, and sortable release snippets do not show one | Existing design authority requires reduced motion while preserving feedback | Add explicit reduced-motion behavior to each motion surface |
| P0 | High-use motion uses slow/ease-in timing | Command palette `420ms ease-in`; drag release `400`; toast `500ms ease-in`; popover `360ms ease-in` | Ease-in and long durations can feel delayed for keyboard-heavy operators | Move frequent UI to `160ms–240ms` with `--ease-responsive` |
| P1 | Popover uses `transition: all` | `.popover { transition: all 360ms ease-in; }` | Over-broad transitions are hard to control and can accidentally animate layout/color/etc. | Restrict to `opacity, transform` or proven properties only |
| P1 | Toast animates `top` | `from { top: -24px; } to { top: 0; }` | Layout-affecting animation is less suitable than transform/opacity for crisp feedback | Use `transform: translateY(...)` plus opacity |
| P1 | Arbitrary animation string bypasses motion conventions | `animate-[palette_420ms_ease-in_both]` | Timing/easing becomes harder to govern and audit | Move palette motion to named class/keyframes or stateful CSS using tokens |
| P2 | Pointer move updates are unframed in snippet | `style.setProperty("--drag-y", ...)` on every pointer move | Pointer-heavy paths need guardrails to avoid unnecessary per-event work | Gate writes with `requestAnimationFrame` if current CSS uses transform |

---

## 3. Implementation plans

### Plan A — Normalize shared motion contract and popover behavior

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

**Target behavior**
- Popovers feel crisp and causal, not delayed.
- Only intentional visual properties animate.
- Reduced Motion keeps state feedback but minimizes travel/duration.

**Project conventions to preserve**
- Reuse existing semantic tokens.
- Match the button precedent: tokenized `transform`, responsive easing, reduced path at `80ms`.
- Do not introduce new global tokens unless inspection proves the existing set is insufficient.

**Ordered steps**
1. Inspect actual `.popover` usage and state selectors before editing.
2. Confirm whether open/closed state is represented by class, data attribute, ARIA state, mounted/unmounted behavior, or framework wrapper.
3. Replace broad transition with explicit properties, likely:
   - `transition-property: opacity, transform;`
   - `transition-duration: var(--duration-panel);`
   - `transition-timing-function: var(--ease-responsive);`
4. If state selectors exist, ensure closed/open styles use small transform distance and opacity only.
5. Add a reduced-motion rule:
   - duration `80ms`
   - preserve opacity/state feedback
   - remove or greatly reduce spatial travel
6. Search for other `transition: all` motion surfaces and decide whether they are in scope or should become follow-up findings.

**Hard boundaries**
- Do not alter popover placement, focus management, layering, keyboard behavior, or dismissal behavior.
- Do not change semantic tokens globally if that would affect unrelated components without review.
- Do not add spring/bounce motion; product personality is calm and operational.

**Mechanical checks**
- Static search for:
  - `transition: all`
  - `ease-in`
  - `.popover`
  - `prefers-reduced-motion`
- Run the closest CSS/frontend validation command available in the project.
- Verify no syntax errors in CSS.

**Runtime / feel checks to perform later**
- Open/close popover with keyboard and pointer.
- Confirm motion communicates appearance/disappearance without lag.
- Confirm focus ring remains visible throughout transition.
- Confirm no unexpected properties animate.

**Reduced Motion behavior**
- Keep opacity/state feedback.
- Use `80ms`.
- Avoid scale/translation or reduce it to near-zero.

**Source-drift stop condition**
- Stop and re-plan if `.popover` is owned by an external primitive with generated state classes, if placement depends on transform, or if another motion-token file already supersedes `src/styles/motion.css`.

---

### Plan B — Convert command palette and toast to tokenized transform/opacity motion

**Files / current excerpts**

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
- Command palette opens/closes quickly enough for keyboard-heavy workflows.
- Toasts appear with clear feedback but avoid layout-position animation.
- Both use semantic durations/easing and have Reduced Motion behavior.

**Project conventions to preserve**
- Use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Prefer named CSS/state classes over arbitrary one-off animation strings.
- Keep feedback present under Reduced Motion.

**Ordered steps**
1. Inspect existing imports for palette styling and toast CSS loading.
2. For `CommandPalette.tsx`, replace the arbitrary animation class with a stable class name plus `data-open={open}`.
3. Define palette state motion in the appropriate existing stylesheet:
   - open: opacity `1`, transform none or very small settle
   - closed: opacity `0`, small translate/scale only if it supports continuity
   - duration: likely `var(--duration-panel)` for panel appearance
   - easing: `var(--ease-responsive)`
4. Ensure closing behavior is compatible with mount/unmount semantics. If the component unmounts immediately elsewhere, do not fake an exit animation without confirming lifecycle support.
5. For `toast.css`, replace `top` keyframes with transform/opacity:
   - from: `transform: translateY(-8px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
   - duration: likely `var(--duration-panel)` or `var(--duration-fast)` depending on existing toast density
6. Add `@media (prefers-reduced-motion: reduce)` for both:
   - `80ms`
   - opacity feedback retained
   - no or minimal translation

**Hard boundaries**
- Do not change search result rendering, command execution, focus trap, keyboard shortcuts, or toast content/lifetime.
- Do not introduce delayed animations that block input readiness.
- Do not rely on runtime-only class generation unless the project already supports it safely.

**Mechanical checks**
- Search for:
  - `animate-[palette`
  - `@keyframes toast-enter`
  - `animation:`
  - `ease-in`
- Run type-check/lint for TSX changes.
- Run CSS/build validation if available.

**Runtime / feel checks to perform later**
- Open command palette repeatedly via keyboard shortcut.
- Type immediately after opening; confirm input readiness is not visually or functionally delayed.
- Trigger a toast during active work; confirm it is noticeable but not theatrical.
- Test Reduced Motion setting and confirm feedback remains visible.

**Reduced Motion behavior**
- Palette: opacity transition only, `80ms`; no meaningful scale/slide.
- Toast: opacity transition only or near-zero transform, `80ms`.
- Feedback remains visible; no silent disappearance.

**Source-drift stop condition**
- Stop and re-plan if palette animation is defined elsewhere by the utility build config, if exit animation requires a presence/lifecycle wrapper not shown, or if toast positioning uses `top` for layout rather than visual entry.

---

### Plan C — Make sortable queue drag/release crisp, framed, and reduced-motion-aware

**Files / current excerpts**

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
- Drag movement stays directly coupled to pointer position.
- Release-to-slot communicates continuity without slowing throughput.
- Pointer-heavy updates avoid unnecessary work.
- Reduced Motion preserves snap feedback with shorter duration or instant positional resolution plus visible state change.

**Project conventions to preserve**
- Use token-equivalent timing: `160ms` or `240ms`, not `400ms`, unless later testing proves otherwise.
- Prefer transform-driven movement.
- Maintain keyboard and pointer usability.

**Ordered steps**
1. Inspect the full component and any related CSS consuming `--drag-y`.
2. Confirm whether `--drag-y` feeds `transform` only. If it affects layout properties, rework CSS first or stop.
3. Frame pointer writes:
   - store latest `clientY`
   - schedule one `requestAnimationFrame`
   - write `--drag-y` once per frame
   - cancel pending frame on cleanup/unmount
4. Shorten release animation:
   - default target: `var(--duration-fast)` equivalent, or numeric `160` if the animation API requires milliseconds
   - use responsive easing if the API supports easing
5. Add or route Reduced Motion behavior:
   - release duration `80ms` or immediate snap if the animation system cannot express a short reduced path
   - retain visible selected/dragging/drop state feedback
6. Ensure `setDragging(false)` timing does not remove visual continuity before the release animation can run. If current behavior depends on it, adjust only after inspecting actual state flow.

**Hard boundaries**
- Do not change sorting rules, nearest-slot logic, data order persistence, selection state, or pointer capture behavior unless inspection identifies a direct bug.
- Do not add inertia, bounce, overshoot, or decorative physics.
- Do not introduce global drag abstractions for this local fix.

**Mechanical checks**
- Type-check the component.
- Search for cleanup-sensitive APIs:
  - `requestAnimationFrame`
  - `cancelAnimationFrame`
  - `animateTo`
  - `--drag-y`
- Confirm no stale frame callback can write after unmount.
- Confirm animation duration units match the animation helper contract.

**Runtime / feel checks to perform later**
- Drag slowly and quickly through the queue.
- Release near slot boundaries.
- Confirm snap is legible but not sluggish.
- Confirm repeated drags do not leave stale transforms.
- Confirm Reduced Motion still gives clear drop confirmation.

**Reduced Motion behavior**
- Pointer tracking remains direct.
- Release snap uses `80ms` maximum, or immediate movement with non-motion feedback if required.
- No long glide, bounce, or overshoot.

**Source-drift stop condition**
- Stop and re-plan if `animateTo` is a physics/spring helper that does not accept duration as shown, if `currentY` is derived asynchronously in a way not visible here, or if `--drag-y` is consumed by layout properties rather than transform.

---

## 4. Recommended execution order

1. **Plan A first** — establishes the shared motion contract and fixes the broadest CSS risk.
2. **Plan B second** — brings high-visibility command palette and toast motion into the same system.
3. **Plan C third** — handles the highest-interaction pointer path after confirming full component behavior.

---

## Explicitly unverified states

- Actual rendered timing, easing, and computed styles.
- Whether shown CSS is imported on every relevant surface.
- Whether components mount/unmount in ways that permit exit motion.
- Whether `--drag-y` is consumed by transform, layout, or both.
- Whether `animateTo` accepts duration/easing exactly as implied.
- Keyboard focus behavior during palette/popover transitions.
- Reduced Motion behavior in an actual OS/browser setting.
- Performance characteristics under real pointer movement.
- Visual feel on target displays or with real operator workflows.

Applied the required quality and frontend planning constraints; no files were edited.
