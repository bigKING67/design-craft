## Motion diagnosis

Static evidence shows a calm operations UI with a useful token precedent, but several motion paths drift into slow `ease-in`, broad/property-expensive animation, and missing visible Reduced Motion branches; the highest-risk item is the draggable queue because direct manipulation needs continuity, interruption, and velocity handling that are not proven by the snippet.

---

## 1. Recon summary

- **Stack signals:** React/TSX components, CSS stylesheets, Tailwind-style arbitrary animation class, imperative pointer handler, and an `animateTo(...)` helper.
- **Where motion lives:** `src/styles/motion.css`, component CSS, TSX class names, keyframes, pointer event handlers, and imperative settle animation.
- **Existing conventions:** semantic tokens exist: `--duration-fast`, `--duration-panel`, `--ease-responsive`; the button precedent limits animated property ownership to `transform` and has a Reduced Motion duration of `80ms`.
- **Product personality:** calm, crisp desktop operations console; motion should explain causality and preserve state continuity without cinematic delay.
- **Frequency map:**
  - **Very high / keyboard-heavy:** command palette.
  - **High direct manipulation:** sortable queue.
  - **Repeated utility:** popovers.
  - **Occasional transient feedback:** toast.
  - **High-frequency local precedent:** button, already aligned.
- **Evidence level:** static excerpts only. No computed styles, browser observation, screen recording, performance trace, accessibility tree, or user/device validation.

---

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | `animate-[palette_420ms_ease-in_both]` on a keyboard-heavy command surface | `src/components/CommandPalette.tsx` | Static evidence shows hardcoded 420ms `ease-in` motion outside tokens. For frequent command use, this risks delayed perceived response. Reduced Motion is not shown in the excerpt. | Replace with tokenized `opacity`/small `transform` transition, `160ms` or bounded `160–200ms`, `--ease-responsive`, and an explicit Reduced Motion branch removing travel. |
| P1 | `onPointerMove` writes `--drag-y`; release calls `animateTo(nearestSlot(currentY), { duration: 400 })` | `src/components/SortableQueue.tsx` | Direct manipulation settle is duration-based in the excerpt, with no shown pointer capture, grab offset, presentation-value interruption, or measured velocity handoff. Static evidence cannot prove feel, but this is the highest interaction-risk surface. | Preserve current target semantics, add pointer capture/grab offset/velocity sampling, start settle from current presentation value, and pass measured CSS px/s velocity into a spring/interactive settle if the API supports it. |
| P2 | `transition: all 360ms ease-in; transform-origin: center;` | `src/styles/motion.css` | Broad transition ownership, slow timing for small overlay motion, `ease-in`, and centered origin are inconsistent with crisp utility overlays unless this is truly a centered surface. Reduced Motion is not shown. | Limit to `opacity, transform`, use existing tokens, set trigger-relative origin where the popover is anchored, and add Reduced Motion duration/travel reduction. |
| P2 | `top` keyframe from `-24px` to `0`; `500ms ease-in` | `src/components/toast.css` | Layout-position animation and long `ease-in` entry are a static performance/feel risk for transient feedback. No Reduced Motion branch is shown. | Keep layout position static, animate `transform: translateY(...)` plus `opacity`, use tokenized `200–240ms` max, and reduce to short fade/no travel under Reduced Motion. |
| P2 | Hardcoded `360ms`, `420ms`, `500ms`, `400` and repeated `ease-in` | Multiple excerpts | Motion vocabulary is fragmented despite existing semantic tokens and a correct local precedent. | Normalize high-frequency and utility motion to existing duration/easing tokens; allow component-specific values only when justified and bounded. |
| P3 | Button precedent is correct but isolated | `src/components/Button.css` | The codebase already contains the desired pattern, but other snippets do not reuse its property specificity and Reduced Motion shape. | Treat the button as the local implementation model: specific properties, semantic tokens, and `80ms` Reduced Motion feedback. |

---

## 3. Implementation plans

### Plan 1 — Normalize command palette and popover motion

**Current excerpts**

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

- Command palette responds immediately for keyboard users: short fade and at most tiny vertical travel.
- Popovers use specific `opacity`/`transform` transitions, not `all`.
- Existing tokens remain the primary authority: `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Reduced Motion preserves open/closed feedback with opacity/static state, removes or neutralizes travel, and uses `80ms`.

**Ordered steps**

1. In `src/components/CommandPalette.tsx`, replace the arbitrary keyframe class with tokenized transition classes or the project’s equivalent local class:
   - animate only `opacity` and `transform`;
   - use `var(--duration-fast)` or a bounded `160–200ms`;
   - use `var(--ease-responsive)`;
   - map `data-open=true/false` to visible/hidden visual states without introducing lifecycle changes.
2. In `src/styles/motion.css`, change `.popover` to explicit property ownership:
   - `transition-property: opacity, transform;`
   - `transition-duration: var(--duration-fast);`
   - `transition-timing-function: var(--ease-responsive);`
3. Replace hardcoded `transform-origin: center` with an anchored default only if usage confirms this selector is for anchored overlays; otherwise preserve `center` for centered surfaces and split anchored popovers into a separate selector.
4. Add a `@media (prefers-reduced-motion: reduce)` branch for `.popover` and the command palette class/state that uses `80ms` and removes positional travel.

**Hard boundaries**

- Do not change command search behavior, focus order, result rendering, keyboard shortcuts, or mount/unmount semantics.
- Do not introduce a new animation dependency.
- Do not replace project tokens with new duration/easing names unless broader token ownership is explicitly approved.

**Mechanical checks**

- Run the project’s existing type and lint gates if available.
- Static grep check after edits: no remaining `animate-[palette_420ms_ease-in_both]`; no `.popover { transition: all ... }`.
- Verify no focus outline or focus-visible style is removed.

**Runtime/feel checks to perform later, not performed here**

- Open/close command palette repeatedly via keyboard; acceptance: response starts immediately, no sluggish entry, focus remains predictable.
- Open popover from its trigger; acceptance: origin visually supports the trigger relationship.
- Interrupt open/close rapidly; acceptance: no obvious restart flash or stuck hidden state.

**Reduced Motion behavior**

- Command palette: opacity/static state feedback only, no meaningful travel, about `80ms`.
- Popover: short opacity transition or instant transform-neutral state, focus visibility unchanged.

**Source-drift stop condition**

- Stop before editing if `CommandPalette` already moved to another motion abstraction, if `palette` keyframes define required non-visual lifecycle behavior, or if `.popover` is shared with centered modals where changing origin would alter intended geometry.

---

### Plan 2 — Rework toast entry from layout travel to transform feedback

**Current excerpt**

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

- Toast appears as quick, calm feedback: opacity plus small compositor-friendly vertical transform.
- Layout position is stable outside the keyframe.
- Duration uses existing token range, preferably `--duration-panel` at most, with `--ease-responsive`.
- Reduced Motion preserves noticeability without spatial travel.

**Ordered steps**

1. Set the toast’s resting layout position outside the animation, if not already set by surrounding CSS.
2. Replace `top` keyframes with:
   - `from { transform: translateY(-8px); opacity: 0; }`
   - `to { transform: translateY(0); opacity: 1; }`
   using the smallest travel that still explains arrival.
3. Change `.toast` animation timing to `var(--duration-panel) var(--ease-responsive)` or shorter if runtime feel shows delay.
4. Add `@media (prefers-reduced-motion: reduce)`:
   - remove vertical travel;
   - use opacity/static state change around `80ms`;
   - do not suppress the toast’s informational feedback.

**Hard boundaries**

- Do not change toast placement, queueing, timeout duration, ARIA/live-region behavior, or dismissal behavior.
- Do not animate `height`, `margin`, `padding`, `top`, or `left` for entry.
- Do not add `will-change` unless a later trace shows benefit.

**Mechanical checks**

- CSS check: `toast-enter` no longer animates `top`.
- CSS check: `.toast` no longer uses `500ms ease-in`.
- Existing type/lint/build checks if available.

**Runtime/feel checks to perform later, not performed here**

- Trigger single and repeated toasts.
- Acceptance: toast is noticeable but does not feel like a banner sliding through the workspace.
- Under rapid toast creation/dismissal, no visual jump, stuck opacity, or layout shift should be observed.

**Reduced Motion behavior**

- Use fade/static appearance only; remove vertical movement.
- Keep the toast visible and perceivable; Reduced Motion must not mean “no feedback.”

**Source-drift stop condition**

- Stop if `top` animation is compensating for missing fixed/sticky positioning, if toast placement is managed by a third-party library API, or if another stylesheet already overrides `toast-enter`/`.toast` motion.

---

### Plan 3 — Make sortable queue release continuous and interruptible

**Current excerpt**

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

- Dragged item tracks 1:1 after intent threshold, without snapping away from the grab point.
- Release settle starts from the current on-screen position.
- Release velocity is measured in CSS px/s and handed into the settle animation.
- Existing target-selection semantics are preserved: keep `nearestSlot(currentY)` unless product authority explicitly approves momentum-based slot selection.
- Reduced Motion keeps direct tracking but removes bounce/overshoot and shortens settle.

**Ordered steps**

1. On pointer down, record:
   - pointer id;
   - starting pointer position in CSS pixels;
   - item/current presentation position;
   - grab offset;
   - short timestamped position history using monotonic time.
2. Use pointer capture once drag intent is confirmed; ignore unrelated pointers during the active drag.
3. On pointer move:
   - compute local drag translation from the recorded start plus grab offset;
   - update a transform-owned element, not an unconstrained parent variable, unless CSS confirms `--drag-y` only drives the dragged item’s transform.
4. Before release, compute velocity from recent samples in CSS px/s.
5. On pointer up:
   - set `dragging` false only after the presentation value is captured;
   - choose target using current project behavior: `nearestSlot(currentY)`;
   - pass measured velocity into the settle if `animateTo` supports velocity/spring parameters.
6. If `animateTo` only supports fixed duration, stop and decide whether to extend the existing helper or use an already-present animation primitive; do not silently add a new dependency.
7. Optional, separately authorized only: compute bounded projected endpoint from current position and velocity, then use it for target selection only if momentum-based queue behavior is approved.

**Hard boundaries**

- Do not change reorder semantics, slot calculation, data mutation timing, selection state, keyboard reorder behavior, or accessibility announcements.
- Do not introduce bounce by default in this operations surface.
- Do not let press feedback and drag translation compete for the same `transform`; use wrapper layers or a single composed transform owner.

**Mechanical checks**

- Type check around pointer event types and animation helper signature.
- Static checks:
  - pointer capture path exists for active drag;
  - velocity samples use consistent CSS px/s units;
  - `nearestSlot(currentY)` behavior is preserved unless explicitly changed;
  - no broad layout reads/writes are added to every pointer move.

**Runtime/feel checks to perform later, not performed here**

- Drag slowly, drag quickly, release near slot boundaries, reverse direction mid-settle, and start a new drag during settle.
- Acceptance: no jump on grab, no jump on interruption, release continues from current position, target is predictable.
- Validate under a large queue/data load before claiming performance quality.

**Reduced Motion behavior**

- Pointer tracking remains direct.
- Release uses no overshoot/bounce, minimal duration around `80ms` or immediate snap with clear static/focus state if that is the project’s accessibility choice.
- No projection-based fling in Reduced Motion unless explicitly approved.

**Source-drift stop condition**

- Stop if `animateTo` already wraps a spring with velocity support, if `--drag-y` is consumed by scoped child transforms only, if `currentY` is not the presentation value, or if queue semantics already define momentum-based target selection elsewhere.

---

## 4. Recommended execution order

1. **Plan 3 first** if sortable queue is on a core workflow: direct manipulation has the highest continuity/accessibility risk.
2. **Plan 1 second:** fixes the high-frequency command palette and repeated popover vocabulary while reinforcing tokens.
3. **Plan 2 third:** bounded polish/performance-risk reduction for transient feedback.

If implementation capacity is limited, do Plan 3 plus the command-palette part of Plan 1 before touching lower-frequency toast polish.

---

## Explicitly unverified states

- Actual animation smoothness, frame rate, compositing, layout shift, and style recalculation cost.
- Whether `.popover` is anchored, centered, shared with modals, or overridden elsewhere.
- The actual `palette` keyframes and command palette mount/unmount lifecycle.
- Whether Reduced Motion exists in other files not shown.
- Pointer capture, grab offset, keyboard reorder behavior, screen-reader announcements, and focus behavior for the queue.
- `animateTo(...)` API capabilities, current presentation-value access, and velocity/spring support.
- Toast live-region behavior, dismissal timing, stacking behavior, and real placement CSS.
