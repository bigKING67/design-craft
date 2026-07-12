## Evidence-labeled verdict

**Verdict: not acceptable for a calm, repeatedly used operations app.**  
**Evidence:** the implementation is not direct-manipulation-safe, not interruptible, not velocity-aware, and not Reduced Motion compliant. It will likely feel laggy, jumpy, and difficult to trust during repeated daily use.

---

## Prioritized findings

1. **Drag is not actually 1:1.**  
   **Evidence:** `pointermove` sets `sheet.style.top = event.clientY`, ignoring where the sheet was grabbed.  
   **Impact:** the sheet can jump so its top aligns with the pointer instead of preserving the grab offset.

2. **The sheet moves even when no drag is active.**  
   **Evidence:** `pointermove` has no `isDragging` guard.  
   **Impact:** any pointer movement over the sheet can reposition it after a stray hover/move.

3. **Input is locked during animation.**  
   **Evidence:** `if (animating) return;` on `pointerdown`.  
   **Impact:** the user cannot grab and reverse the sheet mid-flight; this breaks direct manipulation and agency.

4. **CSS transition conflicts with gesture tracking.**  
   **Evidence:** `.sheet { transition: all 300ms; }` applies to `top` changes during drag.  
   **Impact:** the sheet will chase the pointer instead of staying attached to it.

5. **Layout-position animation is the wrong primitive.**  
   **Evidence:** both drag and animation use `top`.  
   **Impact:** `top` can trigger layout work and is harder to keep smooth than `transform: translateY(...)`.

6. **Release behavior ignores velocity and intent.**  
   **Evidence:** target is chosen with `nearestSnapPoint(sheet.offsetTop)` only.  
   **Impact:** a fast flick toward full/closed may snap backward because only final position is considered.

7. **The easing is physically backwards for a sheet.**  
   **Evidence:** `{ duration: 480, easing: "ease-in" }`.  
   **Impact:** ease-in starts sluggishly and arrives fast, making the snap feel abrupt rather than settled.

8. **Fixed duration ignores distance.**  
   **Evidence:** every snap uses `480ms`.  
   **Impact:** short corrections feel slow; long moves may feel rushed.

9. **Reduced Motion requirement is unmet.**  
   **Evidence:** no `prefers-reduced-motion` branch; WAAPI always performs spatial travel.  
   **Impact:** users requesting reduced motion still get large sheet movement.

10. **Scale feedback is too blunt for an operations surface.**  
    **Evidence:** `.sheet:active { transform: scale(0.96); }`.  
    **Impact:** shrinking the whole sheet can feel playful or unstable, and it conflicts with transform-based sheet motion.

11. **State model is implicit.**  
    **Evidence:** collapsed/half/full are inferred only from position.  
    **Impact:** harder to maintain, announce, restore, test, or coordinate with content/focus.

12. **No pointer capture.**  
    **Evidence:** no `setPointerCapture(event.pointerId)`.  
    **Impact:** dragging can fail if the pointer leaves the sheet bounds.

---

## Concrete direct-manipulation moves

1. Track explicit gesture state:
   - `isDragging`
   - `pointerId`
   - `startPointerY`
   - `startSheetY`
   - `grabOffset`
   - recent position/time samples for velocity

2. On `pointerdown`:
   - cancel or retarget any active animation
   - read the current visual sheet position
   - capture the pointer
   - provide immediate but subtle pressed feedback

3. On `pointermove`:
   - ignore moves unless actively dragging the captured pointer
   - compute `nextY = startSheetY + (event.clientY - startPointerY)`
   - update with `transform: translateY(...)`, not `top`
   - use no transition during drag

4. At bounds:
   - allow limited rubber-band resistance beyond collapsed/full
   - avoid hard stops

5. On `pointerup`:
   - compute release velocity from recent samples
   - project the likely endpoint using velocity
   - choose collapsed/half/full from the projected endpoint, not only current position
   - animate from the current visual value to the chosen snap point

6. Use a spring-like settle:
   - calm default: critically damped or near-critically damped
   - slight overshoot only for intentional flicks, if product tone allows
   - avoid fixed `ease-in` for the sheet snap

7. Preserve Reduced Motion:
   - keep state changes clear
   - replace large spatial travel with short opacity, shadow, handle, or state-indicator feedback
   - remove bounce/overshoot
   - avoid moving the full sheet across a large distance when reduction is requested

8. Replace whole-sheet active scale:
   - use a subtle handle highlight, shadow change, or small affordance response
   - avoid scaling operational content while dragging

---

## Verified / unverified boundaries

**Verified from static code inspection:**
- Drag uses `top`.
- `startY` is assigned but unused.
- `pointermove` has no dragging guard.
- No pointer capture is present.
- Animation blocks new pointerdown while `animating`.
- Snap target ignores release velocity.
- CSS uses `transition: all`.
- Reduced Motion is not handled in the shown code.

**Unverified and not claimed:**
- Actual frame rate or jank.
- Browser-specific WAAPI behavior.
- Device/touch performance.
- Real snap-point values.
- Visual quality in the product UI.
- Accessibility behavior outside the snippet.
- Whether other code mitigates these issues.

---

## Smallest runtime validation plan

1. **Interaction correctness**
   - Drag from top, middle, and handle area.
   - Confirm the sheet does not jump on grab.
   - Confirm pointer leaving the sheet does not drop the drag.

2. **Interruptibility**
   - Flick the sheet, then grab it mid-animation.
   - Expected: it follows the pointer immediately from its current visual position.

3. **Snap intent**
   - Slowly drag near each snap point.
   - Quickly flick toward collapsed, half, and full.
   - Expected: velocity influences the destination.

4. **Reduced Motion**
   - Enable Reduced Motion.
   - Change between collapsed, half, and full.
   - Expected: state is clear without large spatial travel or bounce.

5. **Regression checks**
   - Ensure no movement occurs from hover-only pointer moves.
   - Ensure content is not scaled during routine drag.
   - Ensure final state is stored as collapsed/half/full, not just a pixel value.
