## Verdict

**Not acceptable for a calm, repeatedly used operations sheet.**  
Evidence basis: **static code/CSS review only**; no browser, device, or runtime validation performed.

The implementation treats the sheet as a fixed-duration animation target, not as a directly manipulated object. It will likely feel jumpy, laggy, non-interruptible, and unpredictable across collapsed / half / full states.

---

## Prioritized findings

1. **Direct manipulation is broken** — `[code]`  
   `sheet.style.top = event.clientY` makes the sheet’s top snap to the pointer instead of preserving the grab offset. If the user grabs the handle or middle of the sheet, the surface can jump immediately.

2. **Animation is not interruptible** — `[code]`  
   `if (animating) return` blocks re-grabbing during motion. A sheet should be catchable mid-flight and redirected from its current visual position.

3. **Pointer tracking is unsafe** — `[code]`  
   There is no active drag flag, `pointerId`, `setPointerCapture`, `pointercancel`, or lost-capture handling. `pointermove` can move the sheet even when the user is not intentionally dragging.

4. **CSS transition conflicts with gesture tracking** — `[code]`  
   `.sheet { transition: all 300ms; }` can animate `top` changes during drag, causing the sheet to trail the pointer instead of tracking 1:1. `transition: all` also risks accidental animation of unrelated properties.

5. **Uses layout properties on every frame** — `[code]`  
   Animating and reading `top` / `offsetTop` causes layout work. Gesture motion should use a transform-backed position model, e.g. `translateY`, updated on animation frames.

6. **Snap decision ignores velocity** — `[code]`  
   `nearestSnapPoint(sheet.offsetTop)` only considers current position. A flick toward full or collapsed should project momentum and choose the likely destination, not merely the nearest point.

7. **Release animation has the wrong feel** — `[code]`  
   `duration: 480` and `easing: "ease-in"` means the sheet starts slowly after release and accelerates into the target. That creates a visible seam and an unnatural arrival. A calm sheet wants a quick, damped settle that inherits release velocity.

8. **State can become visually/logically inconsistent** — `[code]`  
   `fill: "forwards"` keeps the animation’s visual end state but does not necessarily commit the actual layout/style state cleanly. Future `offsetTop` reads may not match what the user sees.

9. **No bounds or resistance** — `[code]`  
   The sheet can be dragged beyond collapsed/full limits without clamping or rubber-band resistance. Hard stops or unbounded travel both feel poor.

10. **Reduced Motion is absent** — `[context]`  
   The product requires reduced motion to preserve state feedback without large spatial travel. Current code always performs a large spatial animation.

11. **The press scale is too blunt** — `[code/context]`  
   `.sheet:active { transform: scale(0.96); }` scales the whole sheet while dragging may also need transform. It can feel playful/heavy for a calm operations app and may visually fight the drag motion.

12. **No gesture arbitration with sheet content** — `[inference]`  
   A real sheet likely contains scrollable content. This code does not distinguish dragging the handle from scrolling inside the sheet.

---

## Concrete direct-manipulation moves

1. **Use a real sheet position model**  
   Keep `currentY`, `targetY`, and `state` as data. Render with:

   ```css
   transform: translate3d(0, var(--sheet-y), 0);
   ```

   Avoid `top` for gesture motion.

2. **On pointer down: capture and preserve offset**  
   - Ignore non-primary pointers.
   - Store `pointerId`.
   - Call `setPointerCapture`.
   - Cancel any running animation.
   - Read the current visual position.
   - Store `grabOffset = pointerY - currentSheetY`.

3. **During drag: track 1:1**  
   - Only move while dragging the active pointer.
   - Compute `nextY = pointerY - grabOffset`.
   - Clamp inside bounds.
   - Apply soft rubber-band resistance outside bounds.
   - Batch DOM writes with `requestAnimationFrame`.

4. **Track recent velocity**  
   Store the last few `{ y, time }` samples. On release, compute release velocity in px/s.

5. **Project the landing point**  
   Choose collapsed / half / full from a projected endpoint, not only the release position:

   ```js
   projectedY = currentY + projectedDistanceFromVelocity(velocityY);
   target = nearestSnapPoint(projectedY);
   ```

6. **Animate with an interruptible damped settle**  
   Use a spring-like settle from the current visual position to the target, seeded with release velocity. For this product, prefer low/no overshoot by default; reserve any bounce for deliberate, high-velocity flicks, if at all.

7. **Keep feedback calm and local**  
   Instead of scaling the whole sheet to `0.96`, use subtler feedback:
   - handle highlight,
   - slight handle compression,
   - shadow/material change,
   - scrim opacity tied to sheet progress,
   - state label or affordance update.

8. **Respect Reduced Motion**  
   For reduced motion:
   - keep direct drag response while the user is actively manipulating, if appropriate;
   - avoid large automatic travel after release;
   - commit to the target with minimal or instant spatial movement;
   - preserve state feedback through handle color, opacity, shadow, label, or short non-spatial fade;
   - remove overshoot and elastic effects.

9. **Separate handle drag from content scroll**  
   Prefer dragging from a handle/header region. If content scroll participates, arbitrate intent after a small threshold and avoid hijacking normal vertical scroll.

---

## Verified / unverified boundaries

**Verified from static code**  
- Uses `top`, `offsetTop`, WAAPI `animate`, `ease-in`, fixed duration, `fill: forwards`.  
- Blocks pointerdown while `animating`.  
- Has no pointer capture, velocity tracking, bounds, reduced-motion branch, or pointer-cancel handling.  
- CSS applies `transition: all 300ms` and active-state whole-sheet scale.

**Unverified**  
- Actual frame rate, latency, browser behavior, and device feel.  
- Whether `offsetTop` matches final visual state in the target runtime.  
- Interaction with scrollable sheet content.  
- Accessibility semantics, focus management, keyboard support, and screen-reader state announcements.  
- Exact snap-point geometry and visual design context.

---

## Smallest runtime validation plan

1. **Gesture-state tests**  
   Verify: pointer capture, active pointer only, cancel/lost-capture cleanup, no movement without active drag.

2. **Position tests**  
   Verify: no grab jump, correct offset preservation, bounded movement, rubber-band behavior, collapsed/half/full target selection.

3. **Velocity tests**  
   Verify: slow drag snaps by position; flick snaps by projected endpoint; reversal during animation starts from current visual position.

4. **Reduced-motion tests**  
   Verify: no large automatic spatial travel, no overshoot, state feedback remains visible.

5. **Performance smoke plan**  
   Record whether drag writes are transform-only and frame-batched; ensure no per-move layout reads are required during active dragging.
