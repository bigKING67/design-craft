## Verdict — not production-ready for a calm repeated-use operations sheet

**Evidence:** the implementation moves `top` on every `pointermove`, blocks input while animating, snaps only from `offsetTop`, uses fixed `480ms ease-in`, has `transition: all`, and has no reduced-motion branch.  
**Impact:** it will feel laggy, jumpy, non-interruptible, and tiring during repeated daily use; it also risks layout work on every frame.

---

## Prioritized findings

### P0 — Direct manipulation is broken
**Evidence:** `sheet.style.top = \`${event.clientY}px\`;`  
- The sheet jumps to the pointer’s absolute Y instead of preserving the grab offset.
- `startY` is recorded but never used.
- `pointermove` runs even when no drag is active.
- No `setPointerCapture`, so dragging can break if the pointer leaves the sheet.

**Fix direction:** track `dragStartY`, `sheetStartY`, `grabOffset`, active `pointerId`, and only update while dragging.

---

### P0 — The sheet is not interruptible
**Evidence:** `if (animating) return;`  
- Users cannot grab a settling sheet mid-flight.
- This creates a dead period after release, especially bad in a high-frequency operations surface.
- `.finished.then(...)` has no cancel/error path, so state can become stale if animation is interrupted later.

**Fix direction:** allow pointerdown during animation, cancel or retarget from the current presented position, and carry current velocity into the next settle.

---

### P0 — Uses layout properties for motion
**Evidence:** animates and mutates `top`; reads `sheet.offsetTop`.  
- `top` animation can trigger layout and paint.
- `offsetTop` reads layout state and can force synchronization.
- For a 10,000-row operations app, this competes with table/editor work.

**Fix direction:** use `transform: translateY(...)` as the sole moving value; keep snap state in JS; read layout only at gesture start or resize.

---

### P0 — Snap target ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)`  
- A fast upward flick near the collapsed point may incorrectly return to collapsed.
- A slow drag past a threshold and a decisive flick are treated the same.
- Collapsed / half / full sheets need projected landing, not nearest current position only.

**Fix direction:** compute release velocity from recent pointer samples, project the likely resting point, then choose collapsed/half/full from that projection.

---

### P1 — Easing and duration fight the physical model
**Evidence:** `{ duration: 480, easing: "ease-in" }`  
- `ease-in` starts slowly after the user releases, creating a visible seam.
- It accelerates toward the end, then abruptly stops at the snap point.
- `480ms` is heavy for repeated operational use.

**Fix direction:** use a velocity-aware spring or a short responsive curve. Default should feel quick, calm, and interruptible; reserve bounce only for strong flicks.

---

### P1 — CSS conflicts with gesture animation
**Evidence:** `.sheet { transition: all 300ms; }` and WAAPI also animates `top`.  
- `transition: all` can accidentally animate unrelated properties.
- It may fight explicit JS/WAAPI motion.
- It makes future state changes unpredictable.

**Fix direction:** never use `transition: all` on a gesture surface. Scope transitions to non-positional feedback like `box-shadow`, `background`, or `opacity`.

---

### P1 — Press feedback is too blunt
**Evidence:** `.sheet:active { transform: scale(0.96); }`  
- Scaling the entire sheet while dragging changes the coordinate relationship under the pointer.
- It can make dense table/editor content blur or pulse.
- It conflicts with using `transform` for sheet translation unless transforms are composed carefully.

**Fix direction:** apply pressed feedback to the drag handle or header only: subtle opacity, elevation, handle color, or 1–2px compression, not whole-sheet scaling.

---

### P1 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` handling.  
- The product requires preserving state feedback without large spatial travel.
- Current behavior always performs large vertical travel.

**Fix direction:** in reduced motion, avoid long sheet travel when programmatically changing states; use instant/very short position change plus opacity, border, header label, shadow, or snap-state affordance.

---

### P2 — Missing gesture safety details
**Evidence:** no drag threshold, no axis lock, no bounds, no rubber-banding.  
- Accidental drags can happen during scroll or text interaction.
- Dragging beyond full/collapsed has no controlled resistance.
- No `touch-action` strategy is shown.

**Fix direction:** add small hysteresis, vertical-axis commitment, min/max bounds, and progressive resistance at edges.

---

### P2 — Accessibility/state affordance is incomplete
**Evidence:** pointer-only state transitions.  
- Keyboard users need explicit controls to move collapsed / half / full.
- Assistive tech needs state naming and focus-safe behavior.
- Reduced-motion users still need confirmation that the state changed.

**Fix direction:** expose buttons/shortcuts for each state, announce state changes when meaningful, keep focus stable, and ensure the handle has a clear accessible name.

---

## Concrete direct-manipulation moves

1. **Use a state machine**
   - `idle → dragging → settling`
   - Allow `settling → dragging` interruption.
   - Track current snap state separately from current visual position.

2. **Capture and preserve grab offset**
   - On `pointerdown`: store `pointerId`, `startClientY`, `startTranslateY`, and recent samples.
   - Call `setPointerCapture(event.pointerId)`.
   - Do not move until a small vertical threshold is crossed.

3. **Move with transform only**
   - Use `translateY(currentY)` during drag.
   - Avoid `top`, `offsetTop`, and `transition: all` in the motion path.

4. **Sample velocity**
   - Keep the last few `{ y, time }` samples.
   - On release, compute px/s velocity.
   - Use both projected position and velocity sign to choose collapsed / half / full.

5. **Settle from the live value**
   - Start animation from the current presented `translateY`, not from stale state.
   - If the user grabs during settle, cancel/retarget without a jump.

6. **Use calm snap physics**
   - Normal drag release: critically damped or near-critically damped settle.
   - Strong flick: slight momentum, minimal overshoot if any.
   - Avoid long fixed durations; prioritize perceived responsiveness.

7. **Add boundary resistance**
   - Within bounds: 1:1 tracking.
   - Beyond collapsed/full: progressive rubber-band resistance.
   - On release: settle back cleanly.

8. **Reduced Motion behavior**
   - Keep snap state changes clear, but avoid large animated travel.
   - Use near-instant position update plus short opacity/shadow/header-state feedback.
   - Disable bounce, projection exaggeration, and long spatial interpolation.

---

## Verified / unverified boundaries

**Verified from static code:**
- Uses `top` for drag and animation.
- Uses `offsetTop` for snap decision.
- Blocks pointerdown while `animating`.
- Uses fixed `480ms ease-in`.
- Uses global `transition: all 300ms`.
- Uses whole-sheet `:active` scale.
- No visible reduced-motion branch in the provided snippet.

**Not verified here:**
- Actual browser frame rate.
- Device touch behavior.
- Real snap-point values.
- Interaction with page scroll.
- Accessibility tree, focus behavior, or keyboard support.
- Whether other code wraps/cancels these animations.

---

## Smallest runtime validation plan

1. **Pointer continuity**
   - Drag from handle, body, and edge.
   - Confirm no initial jump and no lost tracking when leaving the sheet bounds.

2. **Interruptibility**
   - Release toward half/full, then grab mid-settle.
   - Confirm the sheet follows immediately from its visible position.

3. **Snap intent**
   - Test slow drag, short flick, fast upward flick, fast downward flick.
   - Confirm projected target matches user intent.

4. **Performance**
   - Record one drag over a populated table.
   - Check for layout/recalculate-style work during pointer movement.
   - Target compositor-only transform updates.

5. **Reduced Motion**
   - Enable reduced motion.
   - Change collapsed / half / full states.
   - Confirm state feedback remains clear without large animated travel.

6. **Keyboard/accessibility**
   - Move between states without pointer input.
   - Confirm focus remains predictable and state changes are perceivable.
