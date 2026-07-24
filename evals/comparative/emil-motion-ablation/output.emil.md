## Verdict

**[Static evidence]** This is **not production-ready gesture motion** for a calm repeated-use operations app. It behaves like a scripted `top` animation attached to pointer events, not like a directly manipulated sheet with stable state, velocity, interruption, reduced-motion handling, or low-latency feedback.

**[Impact]** Users will see jumps, lag, wrong snap decisions, non-interruptible motion, and potentially stuck states—especially harmful for operators who repeatedly open, resize, and dismiss the sheet throughout the day.

---

## Prioritized findings

### P0 — Direct manipulation is broken

**[Static evidence]**
- `pointermove` sets `sheet.style.top = event.clientY`.
- `startY` is captured but not used.
- No grab offset is preserved.
- No active-drag guard is shown for `pointermove`.

**[Impact]**
- The sheet can jump so its top edge aligns with the pointer instead of preserving where the user grabbed it.
- Pointer movement may affect the sheet even when no valid drag is active.
- The interaction will feel detached rather than “under the hand.”

**[Fix direction]**
- Track `dragStartPointerY`, `dragStartSheetY`, and `grabOffset`.
- Move the sheet to `dragStartSheetY + deltaY`, not raw `clientY`.
- Ignore moves unless the current pointer is captured and dragging.

---

### P0 — The sheet is non-interruptible

**[Static evidence]**
- `if (animating) return;` on `pointerdown`.
- New gestures are blocked while the release animation is running.

**[Impact]**
- Users cannot grab the sheet mid-flight and reverse direction.
- This creates a “dead” interval after every release.
- Repeated operations will feel sluggish and authoritarian.

**[Fix direction]**
- On new `pointerdown`, cancel or retarget the current animation from the live visual position.
- Never lock out direct manipulation.
- Preserve current velocity when retargeting if using a spring.

---

### P0 — Uses layout properties on the input path

**[Static evidence]**
- Drag writes `style.top`.
- Release reads `sheet.offsetTop`.
- Animation interpolates `top`.

**[Impact]**
- `top` and `offsetTop` can force layout work.
- Animating `top` is not compositor-friendly.
- A 10,000-row operations surface is especially vulnerable to input jank.

**[Fix direction]**
- Represent sheet position as `translateY(...)`.
- Store logical sheet position in JS state.
- Use `requestAnimationFrame` to batch pointer-driven writes.
- Avoid layout reads during drag.

---

### P1 — Snap behavior ignores velocity and intent

**[Static evidence]**
- `nearestSnapPoint(sheet.offsetTop)` uses position only.
- No release velocity is measured.
- No momentum projection or directional threshold exists.

**[Impact]**
- A quick flick may snap back to the nearest point instead of continuing toward the intended state.
- Slow careful drags and fast throws are treated the same.
- Collapsed / half / full state changes will feel unpredictable.

**[Fix direction]**
- Keep a short pointer history of `{ y, time }`.
- Compute release velocity.
- Project the likely endpoint.
- Choose the snap point nearest the projected endpoint, with hysteresis to avoid accidental state changes.

---

### P1 — Release animation has the wrong character

**[Static evidence]**
- `{ duration: 480, easing: "ease-in" }`.

**[Impact]**
- `ease-in` starts slowly and ends fast, which is usually the opposite of a settling sheet.
- Fixed 480ms travel can feel heavy for repeated desktop work.
- It does not inherit release velocity.

**[Fix direction]**
- Prefer an interruptible spring-like settle.
- Use calmer, critically damped motion for normal state changes.
- Only allow slight overshoot if the user created momentum with a flick.
- If using duration-based fallback, use a decelerating curve and shorter travel-aware durations.

---

### P1 — CSS conflicts with gesture motion

**[Static evidence]**
- `.sheet { transition: all 300ms; }`
- `.sheet:active { transform: scale(0.96); }`

**[Impact]**
- `transition: all` can accidentally animate layout, size, color, shadow, and future properties.
- It may add lag to direct pointer updates.
- Scaling the entire sheet during drag deforms operational content and can conflict with transform-based movement.

**[Fix direction]**
- Do not use `transition: all`.
- Limit transitions to intentional properties.
- Put press feedback on the drag handle, header affordance, shadow, or grip—not the entire data surface.
- Keep drag transform and press feedback composable, e.g. separate wrapper layers.

---

### P1 — Reduced Motion is absent

**[Static evidence]**
- No `prefers-reduced-motion` handling is shown.
- Large spatial travel is always animated.

**[Impact]**
- Users requesting reduced motion still get full sheet travel.
- State changes may be hard to follow if motion is simply removed without replacement feedback.

**[Fix direction]**
- In reduced motion:
  - avoid elastic travel and large animated slides;
  - snap position quickly or nearly instantly;
  - preserve state feedback with opacity, outline, shadow, label, handle state, or subtle content fade;
  - keep state announcements and visual affordances intact.

---

### P2 — Missing pointer lifecycle safety

**[Static evidence]**
- No `setPointerCapture`.
- No `pointercancel`.
- No `lostpointercapture`.
- No pointer id tracking.
- No cleanup path if `.finished` rejects or animation is canceled.

**[Impact]**
- Drag may fail if the pointer leaves the sheet.
- Multi-pointer input can corrupt state.
- `animating` can remain stuck if the animation is interrupted or canceled.

**[Fix direction]**
- Capture the initiating pointer.
- Track `pointerId`.
- Handle `pointerup`, `pointercancel`, and `lostpointercapture`.
- Use `try/finally` or equivalent cleanup around animation completion.

---

## Concrete direct-manipulation moves

1. **State model**
   - Maintain explicit state: `collapsed | half | full`.
   - Maintain numeric `currentY`.
   - Keep snap points in one coordinate system.

2. **Pointer down**
   - Cancel/retarget any running settle animation.
   - Read the current visual position.
   - Capture pointer.
   - Store grab offset and recent movement history.
   - Show immediate but restrained feedback.

3. **Pointer move**
   - Only respond to the captured pointer.
   - Compute `nextY = startSheetY + pointerDeltaY`.
   - Apply bounds with soft rubber-band resistance.
   - Write `transform: translate3d(0, nextYpx, 0)` in a frame-synced batch.
   - Do not read layout every move.

4. **Pointer release**
   - Compute release velocity.
   - Project endpoint from velocity.
   - Choose collapsed / half / full from projected endpoint, not raw position alone.
   - Settle from current visual position to target.
   - Update semantic state when the target is committed.

5. **Reduced motion**
   - Keep snap states.
   - Replace large travel with near-instant reposition plus small opacity/shadow/handle feedback.
   - Remove bounce and long easing.
   - Preserve visible and announced state change.

6. **CSS hygiene**
   - Replace `transition: all` with explicit transitions.
   - Use transforms for motion.
   - Avoid scaling the whole sheet; apply press feedback to the handle or header affordance.

---

## Static-only verified boundaries

**Verified from the snippet**
- Motion is driven by `top`, not transform.
- Release uses fixed-duration WAAPI animation.
- Animation blocks new pointerdown handling.
- Snap decision is position-only.
- CSS uses `transition: all`.
- Whole-sheet active scaling is present.
- No reduced-motion branch is shown.
- No pointer capture or cancellation handling is shown.

**Not verified**
- Actual snap point values.
- Whether other code guards pointer state.
- Whether external CSS sets `touch-action`.
- Actual rendering performance.
- Actual accessibility tree, focus behavior, keyboard controls, or announcements.
- Actual behavior in any runtime, browser, or device environment.

---

## Smallest runtime validation plan

1. Build a minimal fixture with only the sheet, three snap points, and logged `y`, velocity, target state, and active animation status.  
2. Test grabs from top, middle, and handle positions; pass only if there is no initial jump.  
3. Drag slowly across each threshold; pass only if collapsed / half / full decisions are stable.  
4. Flick up and down from near the half point; pass only if velocity changes the target appropriately.  
5. Interrupt the sheet mid-settle and reverse it; pass only if it follows immediately without waiting.  
6. Move the pointer outside the sheet during drag; pass only if capture/cancel paths leave no stuck state.  
7. Enable reduced motion; pass only if state feedback remains clear without large animated travel.  
8. Inspect frame timing during drag; pass only if pointer movement avoids layout-triggering reads/writes on the hot path.
