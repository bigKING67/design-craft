## Evidence-labeled verdict

**Verdict: Not production-ready for a calm repeated-use operations sheet.**  
**Evidence:** The implementation drives motion with `top`, `transition: all`, non-interruptible WAAPI animation, no reduced-motion branch, no drag state guard, no pointer capture/cancel handling, and no stable collapsed/half/full state model. It will feel laggy, jumpy, and fragile under repeated use.

---

## Prioritized findings

### P0 — Direct manipulation is broken
**Evidence:** `pointermove` always runs and sets `sheet.style.top = event.clientY`, even without an active drag. `startY` is recorded but never used.  
**Impact:** The sheet can jump to the pointer’s absolute viewport Y instead of preserving the grab offset. Any pointer movement over the sheet may move it.

### P0 — Animation state can desync from visual state
**Evidence:** `sheet.animate(..., { fill: "forwards" })` visually holds the end frame, but the underlying `style.top` may remain stale. Later `sheet.offsetTop` can read layout state, not the visually filled animation state.  
**Impact:** Repeated drags can snap from incorrect positions or appear to “teleport.”

### P0 — Reduced Motion requirement is unmet
**Evidence:** There is no `prefers-reduced-motion` branch. Snap animation always travels over `480ms`.  
**Impact:** Users who request reduced motion still get large spatial travel. The product requirement says state feedback must remain without large travel.

### P1 — Uses layout-position animation instead of composited motion
**Evidence:** Drag and snap both animate `top`; `pointermove` writes layout-affecting style every event.  
**Impact:** This risks layout/reflow cost, input lag, and poor table/workspace performance. A sheet should generally move with `transform: translateY(...)`.

### P1 — CSS conflicts with JS motion
**Evidence:** `.sheet { transition: all 300ms; }` applies to every changed property, including `top` and potentially `transform`.  
**Impact:** Pointer tracking may lag because every `top` update can transition. `transition: all` also creates accidental animations for unrelated style changes.

### P1 — Snap motion feels wrong for direct manipulation
**Evidence:** Snap uses `duration: 480` and `easing: "ease-in"`.  
**Impact:** `ease-in` starts slowly and accelerates toward the end, which feels like the sheet is escaping the user. Snap-to-state motion should feel responsive, interruptible, and settle naturally.

### P1 — No interruption or cancellation model
**Evidence:** `animating` blocks `pointerdown`, but `pointermove` is not guarded and no active animation handle is cancelled on a new drag.  
**Impact:** User input can conflict with in-flight animation. A direct manipulation surface should let the user grab and redirect the sheet.

### P1 — Pointer lifecycle is incomplete
**Evidence:** No `setPointerCapture`, `pointercancel`, `lostpointercapture`, or drag cleanup path.  
**Impact:** If the pointer leaves the sheet, the gesture is interrupted, or the browser cancels input, the component can remain in a bad state.

### P2 — No velocity, hysteresis, or intent threshold
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only considers final position.  
**Impact:** A quick upward or downward fling will not behave naturally. Small accidental movement near a midpoint may snap unpredictably.

### P2 — Active scale harms operational clarity
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** Scaling the whole sheet during drag reduces text stability and can conflict with translate-based motion. For dense operations UI, feedback should be subtle and preserve readability.

### P2 — Scroll-versus-drag conflict is unresolved
**Evidence:** The snippet does not distinguish dragging the sheet handle from scrolling sheet content.  
**Impact:** Users may accidentally move the sheet when trying to scroll content, or vice versa.

---

## Concrete direct-manipulation moves

1. **Use a real drag state**
   - Track `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, and current sheet position.
   - Ignore `pointermove` unless dragging and the pointer id matches.

2. **Capture the pointer**
   - On valid handle `pointerdown`, call `setPointerCapture(event.pointerId)`.
   - Clean up on `pointerup`, `pointercancel`, and `lostpointercapture`.

3. **Move with transform, not top**
   - Store sheet state as a numeric `translateY`.
   - Apply `transform: translate3d(0, var-or-value, 0)`.
   - Avoid layout reads like `offsetTop` during drag.

4. **Preserve grab offset**
   - Compute `nextY = startSheetY + (event.clientY - startPointerY)`.
   - Clamp or apply resistance beyond collapsed/full bounds.

5. **Make snap state canonical**
   - Maintain explicit states: `collapsed`, `half`, `full`.
   - After animation, commit the final numeric position and state instead of relying on `fill: "forwards"`.

6. **Use position + velocity for snap**
   - Choose target by projected position, velocity, and thresholds.
   - Add hysteresis so tiny moves near a boundary do not flip states unexpectedly.

7. **Make snap animation interruptible**
   - Keep the animation handle.
   - On new drag, cancel the running animation and continue from the current visual position.

8. **Replace `transition: all`**
   - Use narrow transitions only for intentional properties.
   - Example intent: transform duration/easing only during settle, not while dragging.

9. **Remove full-sheet active scaling**
   - Prefer handle affordance, shadow/elevation shift, or small grip highlight.
   - If scale is used, apply it to the handle only, not the readable content panel.

10. **Reduced Motion behavior**
   - For reduced motion, shorten or remove spatial travel.
   - Snap immediately or with a very short fade/outline/state change.
   - Preserve state feedback through label, handle state, shadow, border, or status text.

11. **Separate drag handle from content scroll**
   - Start sheet drag from the handle or a defined drag zone.
   - Let inner content scroll normally.
   - Use `touch-action` deliberately, not globally by accident.

---

## Verified / unverified boundaries

**Verified from static code:**
- Motion is driven by `top`.
- `startY` is unused.
- `pointermove` lacks a dragging guard.
- WAAPI uses `fill: "forwards"`.
- CSS uses `transition: all`.
- Active state scales the sheet.
- No reduced-motion branch is present in the snippet.
- No pointer capture/cancel handling is present in the snippet.

**Not verified from static code:**
- Actual snap-point values.
- Whether the listener is attached to the full sheet or only a handle.
- Whether surrounding code provides keyboard support, ARIA state, focus management, or scroll locking.
- Real device performance.
- Browser-specific WAAPI behavior in the deployed environment.
- Interaction with the full 10,000-row table or edit drawer.

---

## Smallest runtime validation plan

1. **Keyboard-free pointer smoke**
   - Drag from collapsed → half → full and back.
   - Confirm no jump on initial grab and no movement before an active drag.

2. **Interruption test**
   - Start a snap animation, grab mid-animation, reverse direction.
   - Expected: animation cancels cleanly and follows the pointer.

3. **State consistency test**
   - Complete several snap cycles.
   - Confirm visual position, internal state, and next drag start position all match.

4. **Reduced Motion test**
   - Enable reduced motion.
   - Confirm state changes remain clear without large spatial travel.

5. **Performance check**
   - Record a short drag interaction.
   - Expected: transform-only updates, no repeated layout thrash, no visible input lag.

6. **Scroll conflict check**
   - Scroll content inside the sheet and drag the handle.
   - Expected: content scroll and sheet drag do not steal from each other.
