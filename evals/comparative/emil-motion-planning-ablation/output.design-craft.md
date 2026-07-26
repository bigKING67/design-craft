## 1. Recon summary

**Motion diagnosis:** the excerpts show a calm operations product with a useful local motion precedent, but several high-frequency or task-critical motions bypass the token system, use slow `ease-in` timing, animate broad/layout properties, and lack an explicit Reduced Motion path.

- **Stack signals:** React/TSX components, CSS modules/files, global CSS variables, Tailwind-style arbitrary animation class, and at least one JS animation helper (`animateTo`).
- **Where motion lives:**  
  - Global tokens: `src/styles/motion.css`  
  - Component CSS: `src/components/toast.css`, `src/components/Button.css`  
  - Inline/class motion: `src/components/CommandPalette.tsx`  
  - Pointer/gesture logic: `src/components/SortableQueue.tsx`
- **Existing conventions:** semantic duration/easing tokens exist:
  - `--duration-fast: 160ms`
  - `--duration-panel: 240ms`
  - `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`
  - Correct local precedent: button animates only `transform`, uses tokens, and has a Reduced Motion branch.
- **Product personality:** crisp, calm, utility-first desktop operations console; motion should clarify causality without adding perceived latency.
- **Frequency map:**  
  - **Very high:** command palette, keyboard-triggered flows, buttons.  
  - **High/repeated:** popovers, sortable queue manipulation.  
  - **Occasional but noticeable:** toasts.  
- **Evidence level:** static snippets only. No runtime smoothness, interruption quality, computed styles, accessibility-tree behavior, device feel, or performance trace is verified.

---

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | `className="animate-[palette_420ms_ease-in_both]"` | `src/components/CommandPalette.tsx` | Command palette uses a long, arbitrary, `ease-in` animation on a likely high-frequency keyboard surface; no Reduced Motion branch is shown. | Move to named/tokenized CSS state styles, target ~160–200ms, use responsive ease, preserve instant keyboard feedback, add Reduced Motion behavior. |
| P1 | `animateTo(nearestSlot(currentY), { duration: 400 })` | `src/components/SortableQueue.tsx` | Drag settle appears fixed-duration and release-position based; snippet does not show pointer capture, grab offset, measured velocity, interruption from presentation value, or Reduced Motion handling. | Preserve existing `nearestSlot` target semantics, but implement measured release velocity, presentation-value retargeting, pointer capture, and reduced settle motion. |
| P2 | `transition: all 360ms ease-in; transform-origin: center;` | `src/styles/motion.css` | Popover owns all transitioned properties, uses slow-start easing, and has centered origin that may be wrong for trigger-anchored overlays. Static evidence cannot prove which properties change. | Replace with explicit `opacity, transform`; use existing duration/easing tokens; make origin trigger-aware if the positioning layer exposes an origin variable. |
| P2 | `top: -24px → top: 0`, `500ms ease-in` | `src/components/toast.css` | Toast entry animates a layout property and uses a slow 500ms ease-in. This is a performance and feel risk; static evidence does not prove dropped frames. | Animate `transform` + `opacity`, reduce to tokenized 160–240ms, add Reduced Motion branch. |
| P2 | Multiple literals/arbitrary motion values: `360ms`, `420ms`, `500ms`, `400` | Multiple excerpts | Motion vocabulary is fragmented despite existing tokens and a correct local precedent. | Route common UI motion through semantic tokens and reserve literals for documented exceptions. |
| P3 | Button has Reduced Motion precedent; other excerpts do not | `src/components/Button.css` versus others | Reduced Motion behavior is inconsistent in supplied snippets. Shorter duration alone is not a complete path for spatial motion. | For overlays/toasts/drag settle, remove or minimize travel while preserving opacity/color/static state feedback. |

---

## 3. Implementation-ready plans

### Plan A — Tokenize and tighten overlay motion: popover + command palette

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
<div
  data-open={open}
  className="animate-[palette_420ms_ease-in_both]"
>
```

**Target behavior**

- Popovers and palette feel immediate, crisp, and causal.
- Only `opacity` and `transform` are animated unless a specific property is intentionally added.
- Command palette does not impose a long keyboard-path delay.
- Reduced Motion keeps visibility/state feedback without meaningful travel.

**Project conventions to use**

- Use `--duration-fast`, `--duration-panel`, and `--ease-responsive`.
- Follow the button precedent: explicit animated property, semantic tokens, Reduced Motion branch.
- Preserve visible focus; do not replace focus feedback with motion.

**Ordered steps**

1. In `src/styles/motion.css`, add/standardize named overlay motion rules for `.popover` and a command-palette class.
2. Replace `.popover { transition: all 360ms ease-in; }` with explicit properties, for example:
   - `opacity var(--duration-fast) var(--ease-responsive)`
   - `transform var(--duration-fast) var(--ease-responsive)`
3. Replace `transform-origin: center` with a trigger-aware origin only if the positioning primitive exposes one; otherwise use a safe fallback such as `var(--popover-transform-origin, center)` and document the fallback.
4. In `src/components/CommandPalette.tsx`, replace the arbitrary animation class with the named class while preserving `data-open={open}`.
5. Define closed/open state selectors using `data-open`, e.g. opacity and a very small scale/translate only when open/closed state is known.
6. Add a `prefers-reduced-motion: reduce` branch:
   - remove scale/translate travel;
   - keep short opacity or color/state transition, around the local 80ms precedent;
   - preserve focus visibility.

**Hard boundaries**

- Do not change command search behavior, result ordering, focus model, or keyboard shortcuts.
- Do not introduce a new animation library for these CSS-state overlays.
- Do not change button motion except as a reference for consistency.
- Do not assume the popover is trigger-anchored unless the component/positioning code proves it.

**Mechanical checks**

- Search for remaining `animate-[palette_` and `.popover { transition: all`.
- Search for new `ease-in` on overlay enter paths.
- Run the project’s closest static checks if available: type-check, lint, CSS lint/build.
- Confirm no focus-visible selector was removed.

**Runtime/feel checks required later, not performed here**

- Open/close command palette repeatedly by keyboard.
- Reverse open/close mid-transition.
- Inspect popover origin for each placement/collision side.
- Confirm no interaction is blocked while animation plays.

**Reduced Motion behavior**

- No scale/position travel for palette/popover.
- Opacity or static state feedback remains.
- Focus ring remains visible and unaffected.

**Source-drift stop condition**

Stop before editing if `CommandPalette` no longer uses `data-open`, `.popover` is owned by a third-party primitive with different state attributes, the token names changed, or the style authority no longer defines crisp tokenized motion as the target.

---

### Plan B — Convert toast entrance from layout keyframes to tokenized transform/opacity

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

- Toast entry is quick enough for operations work and does not feel like a blocking banner.
- Motion communicates arrival without layout-position animation.
- Toast Reduced Motion preserves noticeability without vertical travel.

**Project conventions to use**

- Use existing duration/easing tokens.
- Prefer `transform` and `opacity`.
- Follow local Reduced Motion precedent from button CSS.

**Ordered steps**

1. Replace `top` animation in `@keyframes toast-enter` with `transform: translateY(...)` and `opacity`.
2. Reduce duration from `500ms` to a tokenized value:
   - default start: `var(--duration-panel)` if the toast is more banner-like;
   - use `var(--duration-fast)` if it is small and frequent.
3. Replace `ease-in` with `var(--ease-responsive)`.
4. If the toast component has explicit lifecycle state such as `data-state="open"` / `closed`, prefer transitions over one-shot keyframes so repeated triggers can retarget more naturally.
5. Add a Reduced Motion branch:
   - no vertical transform;
   - short opacity transition or immediate opacity change;
   - keep any icon/color/status semantics intact.
6. If toast stacking exists, verify the CSS does not create animated gaps that break pointer hit regions.

**Hard boundaries**

- Do not change toast copy, severity colors, dismissal semantics, timers, or announcement behavior.
- Do not infer stacked-toast behavior from this CSS alone.
- Do not claim performance improvement until runtime is measured.

**Mechanical checks**

- Search `toast-enter` for remaining `top:` animation.
- Search `toast.css` for `500ms ease-in`.
- Run the project’s CSS/static checks if available.
- Verify no severity/focus/dismiss selectors were removed.

**Runtime/feel checks required later, not performed here**

- Trigger multiple toasts quickly.
- Dismiss during entry.
- Check document hidden/visible behavior if timers exist.
- Confirm screen-reader announcement behavior if toast is announced.
- Toggle Reduced Motion and confirm arrival feedback remains.

**Reduced Motion behavior**

- Remove vertical travel.
- Preserve visibility through opacity/static state.
- Keep dismissal and focus behavior unchanged.

**Source-drift stop condition**

Stop before editing if toast markup lacks a stable `.toast` class, the lifecycle is controlled by a library with required animation hooks, or toast positioning depends on `top` for actual layout rather than visual entry.

---

### Plan C — Make sortable queue drag settle interruptible and direct-manipulation safe

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

- Dragged item tracks the pointer without snapping unexpectedly.
- Release settle starts from the current on-screen value.
- Existing `nearestSlot(currentY)` target semantics are preserved unless product owners explicitly approve momentum-based target selection.
- Reduced Motion removes bounce/large settle travel while keeping reorder feedback.

**Project conventions to use**

- Use existing motion tokens when CSS timing is involved.
- Avoid broad parent style invalidation on large trees where possible.
- Preserve calm, non-bouncy operations-console motion.

**Ordered steps**

1. On pointer down, record:
   - pointer id;
   - initial pointer Y;
   - item’s current visual Y;
   - grab offset between pointer and item origin.
2. Call pointer capture once drag intent is established, so movement continues outside the original bounds.
3. On pointer move:
   - compute local drag Y using the recorded offset, not raw `event.clientY`;
   - update only the dragged item or a narrow wrapper, not a broad queue parent, unless current CSS proves the variable is scoped narrowly;
   - coalesce writes through `requestAnimationFrame` if pointer events are high frequency.
4. Maintain a short timestamped sample history in CSS pixels and monotonic time.
5. On pointer up:
   - compute release velocity in CSS px/s;
   - preserve `nearestSlot(currentY)` as the target rule for the first implementation;
   - pass current presentation Y and bounded release velocity into the settle animation if `animateTo` supports it.
6. If `animateTo` cannot start from presentation value or accept velocity, replace only the settle primitive with an existing project-approved animation mechanism; do not add a new dependency without approval.
7. Add cancellation handling for pointer cancel/lost capture.
8. Add Reduced Motion branch:
   - no elastic overshoot;
   - immediate or very short settle;
   - static selected/reordered feedback remains visible.

**Hard boundaries**

- Do not change queue ordering rules, nearest-slot semantics, persistence, selection, or keyboard reorder behavior.
- Do not add momentum-based target selection by default.
- Do not introduce bounce unless explicitly authorized and verified.
- Do not make source-wide animation abstractions from this one component.

**Mechanical checks**

- Type-check `PointerEvent` handling.
- Verify pointer capture cleanup paths exist.
- Search for competing writers to `--drag-y` or the dragged element’s `transform`.
- Run unit tests for reorder logic if present.
- Run lint/type-check/build if available.

**Runtime/feel checks required later, not performed here**

- Drag slowly and release.
- Flick quickly and release.
- Reverse direction during settle.
- Drag outside original bounds.
- Trigger pointer cancel/lost capture.
- Test keyboard reorder path still works.
- Verify Reduced Motion settle.

**Reduced Motion behavior**

- Keep direct tracking while dragging; it is causal input feedback.
- On release, remove bounce/overshoot and minimize settle duration.
- Preserve clear final-slot feedback through static position, color, outline, or status text.

**Source-drift stop condition**

Stop before editing if `animateTo` already has a spring/presentation-value API not shown here, `currentY` is no longer the release coordinate, `--drag-y` is consumed by multiple descendants, or queue ordering semantics changed from nearest-slot to a different rule.

---

## 4. Recommended execution order

1. **Plan A first:** highest frequency and easiest cohesion win; establishes shared overlay vocabulary.
2. **Plan B second:** small, isolated correction from layout/slow toast motion to tokenized transient feedback.
3. **Plan C third:** highest interaction complexity; requires careful runtime feel verification and should not be rushed from static evidence alone.

## Explicitly unverified states

- Actual visual smoothness, frame pacing, compositing, and layout cost.
- Whether popovers are trigger-anchored, centered, or library-positioned.
- Command palette focus trapping/restoration and keyboard timing.
- Toast lifecycle, stacking, timers, dismissal, and announcements.
- Sortable queue grab offset, pointer capture, transform ownership, velocity behavior, and keyboard reorder parity.
- Reduced Motion behavior outside the button excerpt.
- Computed styles, browser support, device refresh rate, and real operator perception.
