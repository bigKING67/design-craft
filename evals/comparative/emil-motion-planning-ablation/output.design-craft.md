## 1. Recon summary

Reading this as a calm desktop operations console for keyboard-heavy support/revenue operators, where motion should explain state continuity without becoming latency.

- **Stack signals:** React/TSX components, CSS modules/global CSS, Tailwind-style arbitrary animation class, and an imperative `animateTo(...)` path for drag settling.
- **Where motion lives:**  
  `src/styles/motion.css` tokens + `.popover`; `CommandPalette.tsx` inline animation class; `toast.css` keyframes; `SortableQueue.tsx` pointer-driven style mutation and release animation; `Button.css` as the clean local precedent.
- **Existing conventions:** semantic tokens exist: `--duration-fast: 160ms`, `--duration-panel: 240ms`, `--ease-responsive: cubic-bezier(0.23, 1, 0.32, 1)`. The button precedent correctly uses transform-only motion, semantic tokens, and a Reduced Motion duration of `80ms`.
- **Product personality:** crisp, quiet, utility-first, low-drama. Ease should feel responsive; long ease-in entrances are mismatched for repeated work.
- **Frequency map:**  
  High: command palette, buttons, drag/reorder queue.  
  Medium: popovers.  
  Occasional but burst-prone: toasts/status feedback.  
- **Evidence level:** static excerpts only. No runtime smoothness, computed cascade, actual keyframe definitions beyond shown snippets, browser behavior, accessibility tree, user testing, trace, or device feel was verified.

---

## 2. Vetted priority table

| Priority | Evidence | Location | Finding | Smallest safe correction |
|---|---|---|---|---|
| P1 | `animate-[palette_420ms_ease-in_both]` | `src/components/CommandPalette.tsx` | Command palette is likely high-frequency/keyboard-driven, but uses a long hard-coded ease-in keyframe. Static evidence shows delayed-feeling timing risk, not observed lag. | Replace with tokenized state transition using opacity + small transform, `--duration-fast`/`--ease-responsive`, and Reduced Motion opacity-only/80ms. |
| P1 | `animateTo(nearestSlot(currentY), { duration: 400 })` | `src/components/SortableQueue.tsx` | Direct manipulation release is fixed-duration and shown without velocity handoff, presentation-value retargeting, pointer capture, grab offset, or Reduced Motion path. | Preserve `nearestSlot` target semantics, but settle from current presentation value with measured CSS px/s velocity and an interruptible spring/settle primitive. |
| P2 | `top: -24px` → `top: 0`; `500ms ease-in` | `src/components/toast.css` | Toast entrance animates a layout property and uses a long ease-in. This is a performance and perceived-response risk; no dropped frames are proven. | Keep static positioning, animate `transform: translateY(...)` + opacity, use `--duration-panel` or faster, and add opacity-only Reduced Motion. |
| P2 | `transition: all 360ms ease-in`; `transform-origin: center` | `src/styles/motion.css` | Popover owns all properties and uses center-origin/ease-in. For anchored overlays this risks mismatched causality; actual anchor usage is unverified. | Limit transition to `opacity, transform`; use existing tokens; set trigger-relative origin where available, with center only for truly centered overlays. |
| P2 | Hard-coded `360/400/420/500ms` and `ease-in` appear beside semantic tokens | Multiple snippets | Motion vocabulary is fragmented despite a correct button precedent. This increases drift and makes Reduced Motion harder to keep consistent. | Normalize transient UI to `--duration-fast`, larger panels to `--duration-panel`, and `--ease-responsive`; keep exceptions documented locally. |

---

## 3. Implementation plans

### Plan A — Tokenize high-frequency overlays: command palette + popover

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

- Command palette opens/closes immediately enough for keyboard repetition.
- Motion is subtle: opacity plus small vertical/scale change, not a long keyframe.
- Popovers transition only transform/opacity and originate from their trigger when the component has anchor data.
- Existing token names remain the source of timing/easing truth.

**Project conventions to preserve**

- Use `--duration-fast`, `--duration-panel`, `--ease-responsive`.
- Follow the button precedent: transform-only, tokenized, Reduced Motion `80ms`.
- Do not introduce a new animation library for this plan.

**Ordered steps**

1. Confirm the pasted excerpts still match `src/styles/motion.css` and `src/components/CommandPalette.tsx`.
2. Locate any existing `@keyframes palette` or command-palette CSS. If it already encodes open/close, focus, or Reduced Motion behavior, stop and reconcile instead of replacing blindly.
3. Replace the arbitrary palette animation class with a stable class, for example `className="command-palette"`, while preserving `data-open={open}`.
4. Add or update CSS so closed/open states are driven by `data-open`:
   - closed: `opacity: 0; transform: translateY(-4px) scale(0.98);`
   - open: `opacity: 1; transform: translateY(0) scale(1);`
   - transition: `opacity var(--duration-fast) var(--ease-responsive), transform var(--duration-fast) var(--ease-responsive)`
5. For `.popover`, replace `transition: all 360ms ease-in` with explicit transform/opacity transitions using existing tokens.
6. Change `.popover` origin to `var(--popover-origin, center)` or an existing anchor-origin variable if one already exists. Do not invent anchor math without component evidence.
7. Add Reduced Motion branch: remove translate/scale travel, keep opacity feedback at `80ms`.

**Hard boundaries**

- Do not change search behavior, result rendering, keyboard shortcut wiring, focus ownership, or mount/unmount semantics unless the current component already requires it.
- Do not animate layout properties.
- Do not add new global token names unless multiple components demonstrably need them.

**Mechanical checks**

- Search changed files for remaining `palette_420ms`, `transition: all`, and `ease-in` on these surfaces.
- Run existing local checks if available: lint, type-check, and build. If script names differ or are absent, record that rather than inventing a pass.

**Runtime/feel checks to perform after implementation**

- Keyboard open/close repeat: no visible restart jump.
- Open while results are long/empty/loading if those states exist.
- Confirm focus indicator remains visible during and after transition.
- Inspect with motion slowed in devtools before final tuning.
- No browser/device validation has been performed for this audit.

**Reduced Motion behavior**

- `transform: none` or no spatial delta.
- `opacity` may transition for state feedback.
- Duration `80ms`, matching the button precedent.

**Source-drift stop condition**

Stop before editing if `CommandPalette` no longer renders the shown `data-open` wrapper, if `palette` keyframes already provide state-specific Reduced Motion behavior, or if `.popover` is shared by centered modal content where `center` origin is intentional.

---

### Plan B — Repair toast entrance to avoid layout animation and long ease-in

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

- Toast appears as a quick status confirmation, not a slow banner.
- Final layout position remains stable; only transform/opacity animate.
- Bursts of toasts should not require layout-property animation.

**Project conventions to preserve**

- Use existing semantic duration/easing tokens.
- Keep the toast’s existing placement and stacking model unless current CSS proves the keyframe is the only positioning source.
- Reduced Motion must preserve feedback, not remove the toast state change.

**Ordered steps**

1. Confirm `src/components/toast.css` still contains the shown `toast-enter` and `.toast` animation.
2. Inspect nearby toast positioning rules. If `top: 0` is only defined inside the keyframe, move the final `top` value into the static `.toast` positioning rule before changing the animation.
3. Replace keyframes with transform-based movement:
   - from: `transform: translateY(-24px); opacity: 0;`
   - to: `transform: translateY(0); opacity: 1;`
4. Change `.toast` timing to a semantic token:
   - preferred initial value: `animation: toast-enter var(--duration-panel) var(--ease-responsive) forwards;`
   - if toasts are used for rapid autosave/status feedback, test `--duration-fast` instead.
5. Add Reduced Motion keyframes or branch:
   - no translate movement
   - opacity-only feedback
   - `80ms`
6. If an exit animation exists elsewhere, align it separately; do not invent one in this plan.

**Hard boundaries**

- Do not change toast dismissal timers, live-region behavior, severity colors, stacking order, or message content.
- Do not claim performance improvement until runtime/trace evidence exists.
- Do not add `will-change` unless a measured problem remains.

**Mechanical checks**

- Verify `@keyframes toast-enter` no longer animates `top`.
- Search `toast.css` for hard-coded `500ms ease-in`.
- Run existing lint/build checks if available.

**Runtime/feel checks to perform after implementation**

- Trigger one toast and a burst of toasts.
- Check top-of-viewport placement does not jump before animation starts.
- Verify screen-reader/live-region behavior is unchanged if applicable.
- Check Reduced Motion OS/browser setting.
- No runtime behavior has been verified in this audit.

**Reduced Motion behavior**

- Toast still appears.
- Use opacity-only transition at `80ms`.
- No vertical travel, bounce, parallax, or delayed entrance.

**Source-drift stop condition**

Stop if toast positioning/stacking depends on animated `top` for collision management, if there is already a shared toast transition utility, or if the component has entered/exiting lifecycle requirements not visible in the excerpt.

---

### Plan C — Make `SortableQueue` release motion interruptible and velocity-aware

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

- Dragged content tracks 1:1 in a clear coordinate space.
- Release settles from the current on-screen position.
- Release velocity is measured in CSS px/s and passed into the settle animation.
- Existing target-selection semantics remain `nearestSlot(currentY)` unless product behavior explicitly authorizes momentum-based target selection.

**Project conventions to preserve**

- Keep transform-based drag via CSS variable if current CSS uses `--drag-y` for transform.
- Keep current queue ordering/data persistence behavior.
- Use Reduced Motion to remove elastic/large travel while preserving direct manipulation feedback.

**Ordered steps**

1. Confirm the shown handlers still exist in `src/components/SortableQueue.tsx`.
2. Inspect the CSS consumer of `--drag-y`. Stop if it drives layout properties instead of transform; plan a CSS ownership fix first.
3. Inspect `animateTo` API:
   - Can it cancel an active animation?
   - Can it read or start from current presentation value?
   - Can it accept spring/velocity parameters?
   - What velocity units does it expect?
4. On pointer down, store:
   - `pointerId`
   - start client position
   - current presentation Y
   - grab offset / queue-local origin
   - short sample history using monotonic timestamps
5. Use pointer capture after drag intent is established so movement remains tracked outside the original bounds.
6. On pointer move, compute queue-local/presentation delta instead of writing raw `event.clientY` directly. Update `--drag-y` through one explicit transform owner.
7. Keep hot-path work minimal: no layout reads or React state updates on every pointer move unless already batched safely.
8. On pointer up:
   - release pointer capture
   - read current presentation Y
   - compute release velocity in CSS px/s from recent samples
   - choose target with existing `nearestSlot(currentY)` behavior
   - call an interruptible settle from current Y to target with initial velocity
9. If momentum-based snap targeting is later authorized, compute a bounded projected endpoint separately and use it only for target choice; do not bundle that semantic change into this repair.
10. Cancel/retarget any in-flight settle when a new drag begins, starting from the current presentation value.

**Hard boundaries**

- Do not change which item/slot is selected unless separately approved.
- Do not block pointer input until animation completion.
- Do not introduce a large animation dependency without confirming existing project dependency policy.
- Do not combine drag translate and press scale on the same `transform` owner unless composed explicitly.

**Mechanical checks**

- Type-check the handler changes.
- Search for remaining fixed drag settle `duration: 400` on this path.
- Verify `--drag-y` is written in one coordinate convention.
- Run existing lint/type/build checks if available.

**Runtime/feel checks to perform after implementation**

- Drag slowly, flick quickly, reverse direction before release, and grab again mid-settle.
- Drag outside queue bounds and confirm capture/cleanup.
- Verify no visual jump on pointer down or interruption.
- Test long queues if this component can render many items.
- Check 60Hz and high-refresh displays if release feel is critical.
- No such runtime checks were performed for this audit.

**Reduced Motion behavior**

- Keep direct pointer tracking; it is user-controlled feedback.
- Remove bounce/elastic overshoot.
- Use short no-overshoot settle, or immediate snap with visible state confirmation if the product prefers.
- Clamp or ignore release velocity in Reduced Motion if it causes large travel.

**Source-drift stop condition**

Stop if `animateTo` already handles presentation-value interruption and velocity internally, if `nearestSlot` already uses projected endpoints, if `--drag-y` is not the active transform driver, or if pointer handlers have moved into a shared gesture abstraction.

---

## 4. Recommended execution order

1. **Plan A first:** fixes the most visible token drift and the high-frequency command surface while also correcting popover defaults.
2. **Plan B second:** small, isolated repair with clear performance-risk reduction and Reduced Motion parity.
3. **Plan C third:** highest interaction complexity; requires API inspection and runtime feel validation before approval.

## Explicitly unverified states

- Actual computed styles and cascade.
- Existence or contents of `@keyframes palette`.
- Whether global Reduced Motion rules already cover these components.
- Command palette mount/unmount behavior, focus management, and accessibility semantics.
- Popover anchoring model and whether `center` origin is intentional for some usages.
- Toast stacking, live-region behavior, and dismissal lifecycle.
- `SortableQueue` CSS transform ownership, pointer capture, grab offset, current coordinate system, `animateTo` capabilities, and release feel.
- Frame rate, layout cost, paint/composite behavior, device feel, and user perception.
