## 1. Recon summary

- **Stack signals:** React/TSX components, plain CSS, CSS custom properties, Tailwind-style arbitrary animation utility, and JS-driven drag animation.
- **Where motion currently lives:**
  - Global/system CSS: `src/styles/motion.css`
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`
  - Inline utility class in TSX: `src/components/CommandPalette.tsx`
  - Pointer/JS animation logic: `src/components/SortableQueue.tsx`
- **Existing conventions from evidence:**
  - Semantic tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
  - Correct local precedent exists in `Button.css`: transform-only transition, tokenized timing/easing, `prefers-reduced-motion` fallback to `80ms`.
- **Product personality:** calm, crisp, continuity-preserving, optimized for repeated desktop use and keyboard-heavy operators.
- **Frequency map:**
  - Very frequent: buttons, command palette.
  - Frequent/contextual: popovers.
  - Intermittent but attention-grabbing: toasts.
  - Intensive during task bursts: sortable queue drag/reorder.
- **Evidence level:** static code-only audit. No runtime, computed style, accessibility tree, trace, screen recording, or user validation was performed.

---

## 2. Vetted priority table

| Priority | Finding | Evidence | Risk to product goal | Recommendation |
|---:|---|---|---|---|
| P0 | Reduced Motion is not consistently implemented | `Button.css` has `prefers-reduced-motion`; popover, palette, toast, and queue snippets do not show it | Operators who request reduced motion may still get long spatial motion | Apply the button precedent: preserve feedback, shorten to `80ms`, reduce spatial travel |
| P0 | Motion bypasses semantic tokens | `360ms`, `420ms`, `500ms`, `400`, `ease-in` appear outside tokens | Inconsistent feel; hard to govern system-wide | Replace hardcoded values with existing duration/easing conventions |
| P1 | Layout-affecting or broad animation is present | `.popover { transition: all ... }`; toast animates `top` | Can create unnecessary layout work and unpredictable property animation | Restrict to `transform` and `opacity`; never use `transition: all` |
| P1 | Several entrance motions are likely too slow for high-frequency ops UI | `420ms`, `500ms`, `400ms`, `ease-in` | Motion may delay perceived response and reduce throughput | Use `--duration-fast` for feedback and `--duration-panel` for larger surfaces |
| P1 | Command palette motion is hidden in an arbitrary class | `className="animate-[palette_420ms_ease-in_both]"` | Harder to audit, theme, reduce, and align with system rules | Move to named class/CSS using tokens and data state |
| P2 | Drag release uses hardcoded settle timing | `animateTo(nearestSlot(currentY), { duration: 400 })` | Direct manipulation may feel disconnected on release | Tokenize settle duration; preserve 1:1 drag, shorten/reduce release motion |

---

## 3. Implementation plans

### Plan A — Normalize overlay and command-palette motion

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

- Popovers and command palette feel immediate, calm, and causally connected.
- Animate only `opacity` and `transform`.
- Use existing semantic timing/easing.
- Support both opening and closing states through `data-open`.
- Reduced Motion preserves visible state feedback without long spatial movement.

**Project conventions to follow**

- Prefer `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the `Button.css` precedent for reduced motion: `80ms`.
- Do not introduce decorative bounce, overshoot, or unrelated visual styling.

**Ordered steps**

1. Replace `.popover` transition with explicit properties only:
   - `opacity`
   - `transform`
2. Replace `360ms ease-in` with existing tokens.
   - Use `--duration-fast` for small popovers.
   - Use `--duration-panel` only if the popover is visually panel-like or large.
3. Move command palette animation out of the arbitrary TSX class into a named CSS class.
4. Keep `data-open={open}` as the state hook.
5. Define closed/open styles using transform and opacity, for example:
   - closed: slightly translated or scaled, transparent
   - open: neutral transform, opaque
6. Add `@media (prefers-reduced-motion: reduce)`:
   - duration `80ms`
   - remove or minimize spatial travel
   - preserve opacity/state feedback
7. Ensure focus styling is untouched.

**Hard boundaries**

- Do not change command palette contents, search behavior, result ordering, focus target, or keyboard shortcuts.
- Do not add new motion tokens unless the existing design authority explicitly allows it.
- Do not replace semantic state with mount/unmount behavior unless already supported elsewhere.

**Mechanical checks**

- No `transition: all` remains for `.popover`.
- No `420ms`, `360ms`, or `ease-in` remains for these overlay motions.
- Command palette class is named and auditable.
- Reduced Motion branch exists for the new class.
- Only `opacity` and `transform` are animated.

**Runtime / feel checks for later validation**

- Open and close command palette repeatedly from keyboard.
- Confirm motion does not delay text input readiness.
- Confirm focus remains visible during and after open.
- Confirm popover opening preserves anchor causality.
- Confirm Reduced Motion still gives clear state change without spatial travel.

**Reduced Motion behavior**

- Use `80ms`.
- Prefer opacity-only or near-zero transform distance.
- No spring, bounce, or long slide.

**Source-drift stop condition**

Stop and re-plan if `CommandPalette` now conditionally unmounts, uses a transition library, has focus-management changes, or if `motion.css` token names differ from the excerpt.

---

### Plan B — Convert toast entrance to compositor-safe feedback

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

- Toast appears promptly without layout-position animation.
- Motion communicates arrival, not decoration.
- Duration and easing match the system.
- Reduced Motion keeps feedback but removes meaningful travel.

**Project conventions to follow**

- Use semantic duration/easing tokens.
- Prefer transform/opacity.
- Match the `Button.css` reduced-motion duration precedent.

**Ordered steps**

1. Replace `top` animation with `transform`.
2. Use a smaller travel distance than the current `24px` unless design authority requires otherwise.
   - Example target: `translateY(-8px)` to `translateY(0)`.
3. Replace `500ms ease-in` with:
   - `var(--duration-fast)` or `var(--duration-panel)` depending on toast prominence.
   - For an ops console, prefer `--duration-fast` unless toasts are large/persistent.
4. Use `var(--ease-responsive)`.
5. Use `both` or keep `forwards` only if the existing final-state behavior requires it.
6. Add Reduced Motion media query:
   - duration `80ms`
   - opacity transition only, or near-zero travel.

**Hard boundaries**

- Do not change toast placement, stacking, dismissal timing, content, or severity styling.
- Do not add attention-grabbing bounce/shake.
- Do not alter ARIA/live-region behavior unless separately audited.

**Mechanical checks**

- `toast-enter` no longer animates `top`.
- `.toast` no longer uses `500ms ease-in`.
- Animation uses existing duration/easing tokens.
- Reduced Motion branch exists.
- Final visual state remains `opacity: 1` and neutral transform.

**Runtime / feel checks for later validation**

- Trigger one toast and multiple stacked toasts.
- Confirm the toast does not visually push surrounding layout.
- Confirm appearance is noticeable but not slow.
- Confirm Reduced Motion still makes the toast arrival perceivable.

**Reduced Motion behavior**

- `80ms`.
- Opacity-first.
- No meaningful vertical travel.

**Source-drift stop condition**

Stop and re-plan if toast positioning has moved to a portal, animation library, JS timer system, or if multiple toast variants use separate keyframes not shown here.

---

### Plan C — Tokenize sortable queue drag settlement while preserving direct manipulation

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

- During drag: item follows pointer directly with minimal latency.
- On release: item settles to nearest slot quickly and predictably.
- JS animation duration aligns with the CSS motion system.
- Reduced Motion shortens settlement but still preserves state continuity.

**Project conventions to follow**

- Preserve transform-based motion if the CSS consuming `--drag-y` already uses transform.
- Align JS duration with existing semantic token values:
  - normal settle: equivalent to `--duration-panel` / `240ms`
  - reduced settle: `80ms`
- Use the responsive easing if the animation API supports easing.

**Ordered steps**

1. Locate the CSS that consumes `--drag-y`.
2. Confirm it drives `transform`, not `top`, `margin`, or layout positioning.
3. If it currently drives layout, change the consumer to transform-based movement.
4. Keep pointer-move updates outside React state during active drag.
5. Consider coalescing pointer writes with `requestAnimationFrame` only if later profiling shows excessive pointer work.
6. Replace hardcoded `duration: 400` with a named duration aligned to the motion tokens.
7. Add Reduced Motion detection for the release animation:
   - normal: approximately `240ms`
   - reduced: `80ms`
8. If `animateTo` supports easing, pass the responsive easing equivalent.
9. Keep `nearestSlot(currentY)` behavior unchanged.

**Hard boundaries**

- Do not change sorting rules, slot calculation, persistence, selection, or keyboard reorder behavior.
- Do not add physics, bounce, overshoot, or inertia.
- Do not introduce React state updates on every pointer move.
- Do not assume `event.clientY` is wrong without inspecting the CSS coordinate system.

**Mechanical checks**

- No hardcoded `duration: 400` remains for queue settlement.
- Reduced Motion branch exists for release animation.
- Pointer-move path still performs only narrow imperative updates.
- Drag movement is transform-backed after checking the CSS consumer.
- Slot calculation remains unchanged.

**Runtime / feel checks for later validation**

- Drag slowly, quickly, and across multiple slots.
- Confirm item remains visually attached to pointer.
- Release near slot boundaries and verify predictable settle.
- Confirm no delayed snap after pointer up.
- Confirm Reduced Motion release is short but still understandable.
- Confirm keyboard-heavy workflows are not disrupted.

**Reduced Motion behavior**

- Preserve direct drag response.
- Shorten release settlement to `80ms`.
- Avoid bounce, inertia, or large animated travel beyond the required slot correction.

**Source-drift stop condition**

Stop and re-plan if `animateTo` comes from a library with its own duration units/easing model, if `currentY` is derived differently than expected, or if `--drag-y` is no longer the active movement variable.

---

## 4. Recommended execution order

1. **Plan A first:** fixes the highest-frequency operator surfaces and removes the least governable arbitrary animation.
2. **Plan B second:** small, isolated, high-confidence compositor-safety improvement.
3. **Plan C third:** higher interaction risk; inspect the consuming CSS and animation API before changing.

---

## Explicitly unverified states

- Actual computed styles and final cascade order.
- Whether `palette` keyframes already exist elsewhere.
- Whether popover has separate open/closed state styles.
- Whether command palette is mounted while closed or conditionally rendered elsewhere.
- Whether toast container positioning depends on `top` animation side effects.
- Whether `--drag-y` is consumed by `transform` or by layout properties.
- Whether `animateTo` duration is milliseconds and whether it supports easing.
- Actual frame timing, input latency, focus behavior, screen-reader behavior, or user comfort.
- Reduced Motion behavior at runtime.
