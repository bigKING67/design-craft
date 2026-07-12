Applied quality and frontend guardrails; no files were edited and no runtime/browser validation was performed.

## 1. Recon summary

**Stack signals**
- CSS modules/global CSS plus TSX components.
- Utility-style arbitrary animation class appears in `CommandPalette.tsx`.
- Motion tokens exist in `src/styles/motion.css`.
- Component-local CSS exists in `Button.css` and `toast.css`.

**Where motion lives**
- Global semantic tokens: `src/styles/motion.css`
- Component CSS: `src/components/toast.css`, `src/components/Button.css`
- Inline utility animation: `src/components/CommandPalette.tsx`
- Imperative animation: `src/components/SortableQueue.tsx`

**Existing conventions**
- Tokenized duration/easing precedent:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
- Correct local precedent:
  - Button uses `transform`
  - Button uses semantic tokens
  - Button has a Reduced Motion path preserving feedback via shorter duration

**Product personality**
- Calm desktop operations console.
- Keyboard-heavy, throughout-the-day use.
- Motion should clarify cause/effect and continuity without adding wait time or visual noise.
- Crisp, responsive, low-amplitude transitions fit better than slow entrance effects.

**Frequency map from static evidence**
- High frequency: button press feedback, command palette open/close, popovers, sortable queue drag/snap.
- Medium frequency: toast entry, depending on notification volume.
- Potentially continuous: sortable queue pointer movement.
- State-continuity critical: command palette, popovers, sortable queue.
- Feedback critical: button active, toast entry.

**Evidence level**
- Static source excerpts only.
- No runtime, computed-style, performance trace, screen recording, accessibility-tree, device, or user-test evidence.
- Findings below are source-evidence-based risks, not confirmed runtime failures.

---

## 2. Vetted priority table

| Priority | Surface | Finding | Evidence | Risk | Intended fix |
|---:|---|---|---|---|---|
| P0 | Shared motion conventions | Motion tokens exist but are not consistently used | `motion.css` defines tokens; palette/toast/sort hard-code timing/easing | Inconsistent feel and harder Reduced Motion coverage | Route all common UI motion through semantic tokens |
| P0 | Command palette | Hard-coded `420ms ease-in` arbitrary animation | `className="animate-[palette_420ms_ease-in_both]"` | High-frequency keyboard surface may feel delayed; no shown Reduced Motion path | Use panel token duration/easing; add reduced path that preserves open/close feedback |
| P1 | Popover | `transition: all 360ms ease-in` | `.popover { transition: all 360ms ease-in; }` | Unbounded property animation; duration/easing conflicts with token convention | Transition only `opacity, transform` with existing tokens |
| P1 | Toast | Animates `top` for `500ms ease-in` | `@keyframes toast-enter { from { top: -24px; ... } }` | Layout-affecting property and slow entrance on operational feedback | Use `transform` + `opacity`, shorter tokenized duration |
| P1 | Sortable queue | Drag/snap timing is hard-coded and imperative path lacks visible reduced-motion branch in excerpt | `setProperty("--drag-y", ...)`; `animateTo(..., { duration: 400 })` | Continuous interaction could feel laggy or over-animated; accessibility behavior unknown | Tokenize snap, add reduced snap duration/behavior, verify transform-only application |
| P2 | Reduced Motion coverage | Only button excerpt shows Reduced Motion precedent | Button has `@media`; other snippets do not | Users requesting reduced motion may still get full entrance/drag animations | Add per-surface reduced branches that shorten/remove travel while preserving feedback |

---

## 3. Implementation plans

### Plan A — Consolidate semantic motion primitives and fix popover baseline

**Exact file path/current excerpt**

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
- Popovers feel immediate but not abrupt.
- Only composited properties animate: `opacity` and `transform`.
- Timing aligns with existing semantic tokens.
- Reduced Motion preserves state feedback with shortened duration and minimal/no travel.

**Project conventions to preserve**
- Keep existing token names unless real files show a stronger naming convention.
- Match the local button precedent:
  - transform-based motion
  - tokenized duration/easing
  - Reduced Motion branch that shortens duration rather than removing feedback entirely

**Ordered steps**
1. Open the real `src/styles/motion.css` before editing.
2. Confirm the shown tokens still exist and check for additional motion tokens nearby.
3. Replace popover `transition: all 360ms ease-in` with explicit properties:
   - `opacity`
   - `transform`
4. Use existing tokens:
   - likely `var(--duration-panel)` for open/close panel-like movement
   - `var(--ease-responsive)` for responsive easing
5. Keep `transform-origin: center` unless actual popover placement code indicates a better contextual origin.
6. Add or extend a `@media (prefers-reduced-motion: reduce)` block for `.popover`.
7. In reduced mode, shorten duration, avoid large scale/translate deltas if present elsewhere, and preserve opacity/state feedback.
8. Do not introduce new global motion tokens unless at least two modified surfaces need the same missing semantic.

**Hard boundaries**
- Do not change popover layout, positioning, z-index, focus handling, or open/closed state logic.
- Do not convert global CSS architecture.
- Do not use `transition: all`.
- Do not add decorative bounce, spring, blur, or overshoot.

**Mechanical checks**
- Search for `.popover` definitions/usages before changing to avoid conflicting transitions.
- Check CSS syntax.
- Run the closest available static checks after implementation, such as lint/typecheck/build if configured.
- Verify no new hard-coded `360ms`, `ease-in`, or `transition: all` remains for `.popover`.

**Runtime/feel checks to perform later**
- Open/close popovers from mouse and keyboard.
- Confirm focus ring remains visible throughout transition.
- Confirm no delayed pointer/keyboard usability while the popover is entering.
- Confirm the transition communicates continuity without drawing attention.

**Reduced Motion behavior**
- Recommended: `transition-duration: 80ms` or nearest existing reduced token if present.
- Keep opacity feedback.
- Avoid spatial travel if actual open/close styles include translate/scale.

**Source-drift stop condition**
- Stop and reassess if `motion.css` already contains newer motion tokens, a broader animation system, or `.popover` is no longer defined as shown.

---

### Plan B — Tokenize high-frequency entrances: command palette and toast

**Exact file paths/current excerpts**

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
- Command palette opens/closes crisply for keyboard-heavy use.
- Toasts enter clearly without slow drift.
- Both use semantic token timing/easing.
- Toast motion uses transform/opacity, not `top`.
- Reduced Motion keeps feedback but removes or minimizes travel.

**Project conventions to preserve**
- Use `--duration-panel` for panel-like command palette movement.
- Use `--duration-fast` or a nearby existing feedback token for toast entry if present.
- Use `--ease-responsive`.
- Preserve `data-open={open}` as a useful state hook.
- Keep existing component structure unless real files require a local CSS class.

**Ordered steps**
1. Inspect real `CommandPalette.tsx` imports and styling conventions.
2. Find where `palette` keyframes are defined, if at all.
3. Replace the arbitrary hard-coded animation class with a named class or existing project motion utility that can use CSS variables.
4. Define palette motion using `opacity` plus small `transform` only, for example a short translate/scale that reinforces origin without feeling theatrical.
5. Wire open/closed styles to `data-open` if the component remains mounted.
6. Inspect real `toast.css` for other toast states before changing.
7. Rewrite `toast-enter` to use `transform: translateY(...)` and `opacity`.
8. Replace `500ms ease-in` with semantic duration/easing.
9. Add Reduced Motion branches for both surfaces.
10. Keep visual/state semantics intact: command palette still renders `SearchResults`; toast still enters and remains visible.

**Hard boundaries**
- Do not change search behavior, command execution, filtering, selection, or keyboard navigation.
- Do not alter toast queueing, dismissal timing, ARIA/live-region behavior, or notification content.
- Do not introduce extra wrapper elements unless required by current styling.
- Do not add delayed animations that block interaction.
- Do not remove feedback entirely in Reduced Motion.

**Mechanical checks**
- Search for `animate-[palette`, `@keyframes palette`, and `toast-enter`.
- Ensure no remaining hard-coded `420ms ease-in` or `500ms ease-in` on these surfaces.
- Ensure keyframes animate only `opacity` and `transform`.
- Run typecheck/lint/build if available.
- Confirm CSS selectors match actual mounted class names.

**Runtime/feel checks to perform later**
- Open command palette repeatedly via keyboard shortcut.
- Type immediately after opening; confirm perceived readiness is not delayed by animation.
- Move through search results with keyboard while open.
- Trigger one and multiple toasts; confirm entry is noticeable but not attention-grabbing.
- Confirm motion does not obscure text legibility.

**Reduced Motion behavior**
- Command palette:
  - Use near-instant opacity feedback, around 80ms if consistent with button precedent.
  - Remove scale/translate or reduce to negligible distance.
- Toast:
  - Keep opacity transition or very short transform.
  - Avoid vertical travel from `-24px`.
  - Preserve arrival feedback so notifications do not appear without context.

**Source-drift stop condition**
- Stop and reassess if the real command palette uses a transition library, exit animations, portal lifecycle, or already has centralized animation definitions not visible in the excerpt.
- Stop if toast positioning depends on animated `top` for layout correctness; first identify the layout contract.

---

### Plan C — Make sortable queue drag/snap motion responsive and accessible

**Exact file path/current excerpt**

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
- Drag follows pointer directly without decorative lag.
- Snap to slot communicates causality and final placement.
- Snap timing is shorter and tokenized.
- Reduced Motion preserves final-placement feedback while minimizing animated travel.
- Pointer-move path avoids unnecessary React renders and avoids layout-dependent animation where possible.

**Project conventions to preserve**
- Imperative pointer update is acceptable for continuous drag if it avoids React re-render churn.
- Align snap duration with existing tokens:
  - likely `--duration-panel` if slot movement is panel-like
  - shorter if actual distance is small
- Match responsive easing convention.

**Ordered steps**
1. Inspect full `SortableQueue.tsx` before editing.
2. Identify:
   - how `--drag-y` is consumed in CSS/style
   - whether it drives `transform`, `top`, layout, or calculations
   - where `currentY` is updated
   - what `animateTo` implementation accepts
3. If `--drag-y` is consumed by transform, keep the pointer path but consider requestAnimationFrame coalescing only if current code writes more than necessary.
4. If `--drag-y` is consumed by layout properties, migrate consumption to transform-based movement before tuning duration.
5. Replace hard-coded `duration: 400` with a semantic duration or local constant derived from motion tokens/config.
6. Add Reduced Motion handling at the snap call site or inside `animateTo`, whichever is the narrower reusable boundary.
7. Ensure pointer-up always lands on `nearestSlot(currentY)` even when animation is shortened.
8. Preserve drag state cleanup and pointer capture/release behavior if present.

**Hard boundaries**
- Do not change queue ordering rules, nearest-slot calculation, persistence, or business state.
- Do not introduce React state updates on every pointer move unless already proven cheap.
- Do not add physics/spring behavior unless the project already uses it.
- Do not make Reduced Motion skip the final state update.
- Do not modify unrelated sortable/list components without evidence of shared code.

**Mechanical checks**
- Search for `--drag-y`, `animateTo`, `nearestSlot`, and `prefers-reduced-motion`.
- Confirm TypeScript types for any new duration/reduced-motion helper.
- Confirm pointer handlers still remove listeners/cleanup as before.
- Run typecheck and any component/unit tests if available.
- Confirm no hard-coded `duration: 400` remains for this snap path unless retained with documented reason in code.

**Runtime/feel checks to perform later**
- Drag slowly and quickly; item should track the pointer without visible lag.
- Release near slot boundaries; snap should clarify final placement.
- Drag with keyboard alternative if one exists; confirm focus and order feedback remain clear.
- Test long queues and rapid repeated drags for perceived responsiveness.
- Check Reduced Motion setting: final placement should be immediate or near-immediate, not absent.

**Reduced Motion behavior**
- On release, use immediate placement or very short duration, around 80ms if matching existing button precedent.
- Avoid long spatial interpolation.
- Preserve any visual confirmation of drop/final state through focus, outline, opacity, or short transform feedback.

**Source-drift stop condition**
- Stop and reassess if `animateTo` is a shared abstraction with existing global defaults, if queue movement already uses a motion library, or if `--drag-y` no longer controls visual position as implied.

---

## 4. Recommended execution order

1. **Plan A first** — establish safe global motion baseline and remove `transition: all` from popovers.
2. **Plan B second** — fix the most visible high-frequency entrance patterns: command palette and toast.
3. **Plan C third** — tune sortable queue after inspecting the full imperative drag path, because it has the highest interaction complexity.

## Explicitly unverified states

- Actual computed durations/easings in browser.
- Whether `palette` keyframes exist and what they animate.
- Whether `.popover` has separate open/closed transform or opacity rules.
- Whether toast layout depends on `top`.
- Whether `--drag-y` is consumed by `transform`, `top`, or another property.
- Whether `animateTo` is local or shared.
- Whether Reduced Motion is already centralized elsewhere.
- Keyboard focus behavior, screen-reader behavior, and visual focus persistence.
- Runtime performance, layout/recalc cost, frame pacing, and device-specific feel.
