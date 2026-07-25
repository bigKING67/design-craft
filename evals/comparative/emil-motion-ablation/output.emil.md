## Evidence-labeled verdict

**Verdict: Not production-ready for a calm repeated-use operations sheet.**  
**Evidence:** The implementation moves layout via `top`, locks input while animating, snaps by current `offsetTop` only, uses fixed `480ms ease-in`, applies `transition: all`, has no reduced-motion path, and does not preserve drag offset, velocity, interruption, or keyboard/state feedback.

The result will likely feel **laggy, jumpy, non-interruptible, and physically inconsistent**, especially across collapsed / half / full sheet states.

---

## Prioritized findings

### P0 — Drag is not true direct manipulation
**Evidence:** `startY = event.clientY` is stored but never used; `pointermove` sets `sheet.style.top = event.clientY`.  
**Impact:** The sheet jumps so its top edge follows the pointer instead of preserving where the user grabbed it.  
**Fix direction:** Track `grabOffset = pointerY - sheetTop`, then set position to `pointerY - grabOffset`.

---

### P0 — Input is locked during animation
**Evidence:** `if (animating) return;` on `pointerdown`.  
**Impact:** Users cannot grab the sheet mid-flight, reverse direction, or correct an accidental release. This is hostile for repeated operations work.  
**Fix direction:** Allow interruption. Cancel or retarget the current animation from the sheet’s current visual position.

---

### P0 — Uses layout properties for every frame
**Evidence:** `sheet.style.top = ...`, `sheet.offsetTop`, animated `top`.  
**Impact:** `top` and `offsetTop` force layout work and can cause jank, especially inside a dense operations UI.  
**Fix direction:** Use a single motion value mapped to `transform: translateY(...)`; read layout once at gesture start if needed.

---

### P0 — Snap choice ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only considers release position.  
**Impact:** A fast upward flick near the lower state may incorrectly return downward. The gesture does not feel like it carries momentum.  
**Fix direction:** Track recent pointer samples, compute release velocity, project the likely resting point, then choose collapsed / half / full from that projected value.

---

### P1 — Release animation has the wrong feel
**Evidence:** `{ duration: 480, easing: "ease-in" }`.  
**Impact:** `ease-in` starts slowly after the user releases, creating a visible seam between finger motion and sheet motion. A fixed 480ms duration can feel sluggish for short moves and abrupt for long moves.  
**Fix direction:** Use a velocity-aware spring or adaptive timing. Start from the current visual position and carry the release velocity into the settle.

---

### P1 — CSS conflicts with gesture animation
**Evidence:** `.sheet { transition: all 300ms; }` plus JS-driven `top` animation.  
**Impact:** `transition: all` may animate unrelated properties, fight imperative animation, and create unpredictable delays.  
**Fix direction:** Remove `transition: all`; only transition non-gesture properties intentionally, e.g. opacity, shadow, or handle color.

---

### P1 — Press feedback is spatially misleading
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** Scaling the entire sheet during drag can detach content from the pointer, shift perceived geometry, and feel decorative rather than useful.  
**Fix direction:** Put press feedback on the drag handle or header only: subtle handle highlight, shadow lift, or grip state.

---

### P1 — Reduced Motion requirement is unmet
**Evidence:** No `prefers-reduced-motion` handling; full spatial travel remains.  
**Impact:** Users requesting reduced motion still get large sheet movement and a 480ms travel animation.  
**Fix direction:** Preserve state feedback with short opacity/color/elevation changes, instant or near-instant position changes, no bounce, no large animated travel.

---

### P2 — Pointer lifecycle is incomplete
**Evidence:** No `setPointerCapture`, no `pointercancel`, no lost-capture handling, no active pointer id.  
**Impact:** Drag can break when the pointer leaves the sheet, another pointer appears, or the browser cancels the gesture.  
**Fix direction:** Capture the initiating pointer, ignore other pointers, clean up on `pointerup`, `pointercancel`, and lost capture.

---

### P2 — Animation state can get stuck
**Evidence:** `.finished.then(...)` only resets `animating` on fulfillment.  
**Impact:** If animation is cancelled or rejects, `animating` may remain `true`.  
**Fix direction:** Use `try/finally` semantics or handle both resolve and reject; better, remove the global lock and model animation as interruptible.

---

### P2 — Logical state is not committed
**Evidence:** `fill: "forwards"` visually holds the final frame, but no durable state is shown.  
**Impact:** DOM style, snap state, accessibility state, and business state can diverge.  
**Fix direction:** On settle, commit `currentSnap = "collapsed" | "half" | "full"` and set the actual transform/style to that state.

---

## Concrete direct-manipulation moves

1. **Use transform-based position**
   - Maintain `sheetY` as the single source of truth.
   - Render with `transform: translate3d(0, ${sheetY}px, 0)`.

2. **Respect grab offset**
   - On pointer down: read `sheetTop`.
   - Store `grabOffset = event.clientY - sheetTop`.
   - During drag: `nextY = event.clientY - grabOffset`.

3. **Capture the pointer**
   - Call `setPointerCapture(event.pointerId)`.
   - Track only that pointer until release/cancel.

4. **Add drag hysteresis**
   - Do not commit to dragging until movement passes a small threshold.
   - Prevent accidental sheet movement from clicks on controls inside the sheet.

5. **Track velocity**
   - Store recent `{ y, time }` samples.
   - On release, compute px/s from the last short window.

6. **Project before snapping**
   - `projectedY = currentY + projectedMomentum(velocityY)`.
   - Choose the nearest snap point from `projectedY`, not just `currentY`.

7. **Make release interruptible**
   - If the user presses during settle, cancel/retarget from the current visual transform.
   - Do not block `pointerdown` with `animating`.

8. **Use calm spring behavior**
   - Default: critically damped / no overshoot.
   - Allow only slight momentum response for deliberate flicks.
   - Avoid decorative bounce in an operations app.

9. **Replace full-sheet active scale**
   - Use handle/header feedback:
     - handle darkens slightly,
     - sheet shadow/elevation changes,
     - cursor/pressed state updates.
   - Keep the sheet’s content spatially stable.

10. **Reduced Motion behavior**
    - Position may change immediately or with very short travel.
    - Preserve state feedback via opacity, border, handle color, elevation, or label change.
    - Avoid bounce, long slides, and large viewport movement.

---

## Verified / unverified boundaries

**Verified from static code:**
- `top` is used for drag and animation.
- `offsetTop` is used for snap calculation.
- Input is blocked while `animating` is true.
- Release animation uses `480ms ease-in`.
- CSS uses `transition: all 300ms`.
- CSS scales the entire sheet on `:active`.
- No visible reduced-motion branch exists in the snippet.
- No pointer capture, cancellation handling, velocity tracking, or snap-state commit is shown.

**Not verified from the snippet:**
- Actual snap point values.
- Whether surrounding code handles keyboard state, ARIA, focus management, or scroll locking.
- Whether the sheet contains interactive controls that need gesture disambiguation.
- Actual frame rate, layout cost, or device performance.
- Browser/device behavior.
- Whether external CSS overrides these rules.

---

## Smallest runtime validation plan

1. **Direct manipulation check**
   - Press the sheet at different vertical points.
   - Confirm the grabbed point stays under the pointer without jumping.

2. **Interruption check**
   - Release toward half/full.
   - While it is settling, grab again and reverse direction.
   - Expected: no lockout, no visual jump.

3. **Velocity check**
   - Slowly drag near a boundary.
   - Then perform a fast flick from the same release position.
   - Expected: snap target changes based on intent/velocity.

4. **Performance check**
   - Record a drag session.
   - Confirm motion uses compositor-friendly transforms and avoids repeated layout reads during move.

5. **Reduced Motion check**
   - Enable reduced motion.
   - Move between collapsed / half / full.
   - Expected: state still changes clearly, but without long spatial travel or bounce.

6. **Pointer lifecycle check**
   - Drag outside the sheet, cancel, multi-touch/secondary pointer, and release outside bounds.
   - Expected: no stuck dragging, no stuck animating, final state remains coherent.
