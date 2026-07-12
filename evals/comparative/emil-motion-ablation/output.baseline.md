## Evidence-labeled verdict

**[Verified from snippet] Verdict: Not production-ready for a calm, repeated-use operations app.**  
The implementation will likely feel jumpy, laggy, and hard to trust because it treats the sheet as an absolute `top` value, lacks a real drag state model, conflicts CSS transitions with JS animation, ignores velocity/state intent, and has no Reduced Motion behavior.

---

## Prioritized findings

1. **[Verified] Drag jumps instead of preserving grab position**
   - `startY` is recorded but never used.
   - `pointermove` sets `sheet.style.top = event.clientY`, so the sheet top snaps to the finger/cursor Y, not to the original sheet position plus drag delta.

2. **[Verified] Pointer lifecycle is incomplete**
   - `pointermove` runs even if no valid drag started.
   - No `isDragging`, `pointerId`, `setPointerCapture`, `pointercancel`, or lost-capture handling.
   - During `animating`, `pointerdown` returns, but `pointermove` can still mutate `top`.

3. **[Verified] `top` animation causes layout work and poorer motion**
   - Updating `top` on every move can trigger layout/reflow.
   - A bottom sheet should usually move with `transform: translateY(...)` for direct manipulation.

4. **[Verified] CSS conflicts with JS motion**
   - `.sheet { transition: all 300ms; }` means every `top` write may transition, making the drag lag behind the pointer.
   - `transition: all` also risks animating unrelated properties.
   - WAAPI animation of `top` plus CSS transition on all properties creates competing motion systems.

5. **[Verified] Release motion has the wrong feel**
   - `ease-in` starts slow and ends fast; sheets usually need deceleration into rest.
   - `480ms` is likely too long for a repeatedly used operations surface.
   - No distance-based duration, no velocity-based snap, no interruption model.

6. **[Verified] Snap decision lacks user intent**
   - `nearestSnapPoint(sheet.offsetTop)` ignores drag velocity, direction, thresholds, and hysteresis.
   - A quick upward fling should be able to advance toward full even if nearest point is half.

7. **[Verified] State is not committed cleanly**
   - `fill: "forwards"` visually holds the animation, but the durable state/style may not be synchronized.
   - The next `offsetTop` read may not represent the intended snap state reliably across all conditions.

8. **[Verified] Reduced Motion requirement is unmet**
   - There is no `prefers-reduced-motion` branch.
   - Large spatial travel is always animated over 480ms.
   - State feedback is only spatial motion plus `:active` scale.

9. **[Verified] `:active { transform: scale(0.96); }` is risky**
   - Scaling the sheet during drag can make the contact point feel unstable.
   - It conflicts conceptually with transform-based sheet movement.
   - It is not a clear collapsed/half/full state cue.

10. **[Inferred] Missing bounds will allow unnatural positions**
   - No clamp to collapsed/full limits is shown.
   - Users may drag beyond valid snap points unless constrained elsewhere.

---

## Concrete direct-manipulation moves

- Use a real gesture model:
  - `isDragging`
  - `activePointerId`
  - `grabOffsetY`
  - `currentY`
  - `currentState: "collapsed" | "half" | "full"`
  - `activeAnimation`

- On `pointerdown`:
  - Cancel any running settle animation.
  - Capture the pointer.
  - Measure current sheet position.
  - Store the pointer-to-sheet offset so the sheet does not jump.

- On `pointermove`:
  - Ignore non-active pointers.
  - Compute `nextY = event.clientY - grabOffsetY`.
  - Clamp or apply resistance beyond full/collapsed bounds.
  - Move with `transform: translateY(...)`, not `top`.

- On `pointerup` / `pointercancel`:
  - Release capture.
  - Calculate recent velocity.
  - Choose snap using position + velocity + direction + hysteresis.
  - Animate to target with an ease-out or critically damped spring-like curve.
  - Commit the final state after animation.

- Replace CSS:
  - Remove `transition: all`.
  - Avoid `:active` scale for the whole sheet.
  - Use specific transitions only for non-positional feedback, e.g. handle color, shadow, backdrop opacity.
  - Add temporary `will-change: transform` only while dragging/settling.

- Reduced Motion behavior:
  - Preserve direct state feedback without large travel.
  - Snap immediately or with a very short low-distance transition.
  - Use non-spatial feedback: handle highlight, state label, elevation/backdrop change, or subtle opacity change.
  - Keep collapsed/half/full state clearly perceivable.

---

## Verified / unverified boundaries

**Verified from static code only**
- Drag uses `top`.
- `startY` is unused.
- `pointermove` is not guarded by drag state.
- CSS has `transition: all`.
- Release animation uses `ease-in`, `480ms`, `fill: "forwards"`.
- No visible Reduced Motion handling.

**Unverified**
- Actual `nearestSnapPoint` behavior.
- Existing CSS positioning, viewport constraints, and snap coordinates.
- Whether other code handles accessibility, keyboard control, focus, or ARIA state.
- Real frame rate, browser behavior, and touch-device behavior.
- No browser or device validation has been performed here.

---

## Smallest runtime validation plan

1. **Gesture correctness**
   - Drag from collapsed, half, and full.
   - Confirm no jump on initial contact.
   - Confirm movement stays under the pointer/finger.
   - Confirm bounds and resistance feel intentional.

2. **Snap correctness**
   - Slow release near each threshold.
   - Fast upward and downward flicks.
   - Confirm velocity can override nearest-position snap where appropriate.

3. **Interruption correctness**
   - Start a drag during settle animation.
   - Cancel pointer mid-drag.
   - Leave/re-enter bounds while dragging.
   - Confirm no stuck `animating` state.

4. **Reduced Motion check**
   - Enable reduced motion.
   - Confirm state changes remain clear.
   - Confirm there is no large animated spatial travel.

5. **Performance smoke check**
   - During continuous drag, confirm movement is transform-driven and visually tracks input without delayed CSS transition behavior.
