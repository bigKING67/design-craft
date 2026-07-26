## Evidence-labeled verdict

**Verdict: Not production-ready for a calm, repeated-use operations sheet.**  
**Evidence from snippet:** the sheet is moved with `top`, animated with fixed `ease-in` timing, blocks or corrupts interaction during animation, has no velocity-aware snap, no reduced-motion path, and CSS `transition: all` conflicts with gesture tracking.  
**Impact:** users will see jumps, lag, non-interruptible motion, inconsistent snap behavior, and potentially large spatial travel that violates the Reduced Motion requirement.

---

## Prioritized findings

### P0 — Drag is not true direct manipulation
**Evidence:** `startY` is recorded but never used; `pointermove` sets `sheet.style.top = event.clientY`.  
**Problem:** the sheet jumps so its top equals the pointer position instead of preserving the grab offset. A drag from the middle of the sheet will snap the sheet top to the cursor/finger.  
**Fix direction:** track `grabOffset = pointerY - sheetTop`; set position to `pointerY - grabOffset`.

### P0 — Gesture motion is non-interruptible and internally inconsistent
**Evidence:** `if (animating) return` in `pointerdown`, but `pointermove` has no `dragging` or `animating` guard.  
**Problem:** users cannot intentionally grab a moving sheet, yet stray pointer moves can still mutate `top`. This is the worst of both worlds: blocked agency plus unstable state.  
**Fix direction:** allow interruption; cancel the current animation on pointerdown, read the current visual position, then continue from there.

### P0 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` handling; release always animates up to `480ms` with spatial travel.  
**Problem:** collapsed/half/full transitions can move a large surface across the viewport. Reduced Motion must preserve feedback without large travel.  
**Fix direction:** in reduced motion, avoid long sheet travel; use immediate state placement plus short opacity, handle, border, shadow, or state-label feedback.

### P1 — `top` animation causes layout work and weak frame reliability
**Evidence:** gesture updates `sheet.style.top`; release reads `sheet.offsetTop`; animation changes `top`.  
**Problem:** `top` affects layout and `offsetTop` can force synchronous layout. On a 10,000-row operations surface, this risks jank.  
**Fix direction:** position with `transform: translateY(...)`; keep a numeric `currentY` state; read layout only at gesture start or resize.

### P1 — CSS transition conflicts with gesture tracking
**Evidence:** `.sheet { transition: all 300ms; }` while JS updates `top` on every `pointermove`.  
**Problem:** each drag frame may be eased by CSS instead of following 1:1. `transition: all` also animates unrelated changes and can fight the WAAPI animation.  
**Fix direction:** remove broad transitions from the draggable surface; animate only explicit properties, and disable transitions during active drag.

### P1 — Release behavior ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only considers current position.  
**Problem:** a fast upward flick near the half point may incorrectly snap back instead of continuing to full. A slow deliberate drag and a high-velocity throw are treated the same.  
**Fix direction:** compute release velocity, project the likely resting endpoint, then choose collapsed/half/full from that projected value.

### P1 — Fixed `480ms ease-in` feels wrong for a sheet
**Evidence:** `{ duration: 480, easing: "ease-in" }`.  
**Problem:** `ease-in` starts slowly after the user releases, creating perceived hesitation. A fixed duration also makes short snaps feel sluggish and long snaps feel abrupt.  
**Fix direction:** use a velocity-aware spring or responsive easing that starts from the release velocity; keep calm damping, avoid decorative bounce unless caused by a flick.

### P2 — `fill: "forwards"` risks state drift
**Evidence:** WAAPI animation fills visually but the code does not commit the final `top` style.  
**Problem:** visual position and DOM/style state can diverge; later `offsetTop` or style reads may not match what the user sees.  
**Fix direction:** on finish, commit/cancel the animation and set the canonical position value.

### P2 — Press feedback is too heavy and not state-specific
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Problem:** shrinking an entire operations sheet can make dense content pulse, reduce legibility, and conflict with transform-based sheet movement.  
**Fix direction:** give feedback on the handle or grip area, not the whole sheet; use subtle handle compression, shadow change, or background elevation.

### P2 — Missing pointer lifecycle handling
**Evidence:** no `setPointerCapture`, `pointercancel`, `lostpointercapture`, drag threshold, or `touch-action`.  
**Problem:** dragging can be lost when the pointer leaves the sheet; browser scroll/selection may compete with the gesture; cancellation may leave stale state.  
**Fix direction:** capture the pointer on drag start, release it on end/cancel, define `touch-action`, and reset state on cancellation.

---

## Concrete direct-manipulation moves

1. **Use a canonical Y model**
   - `collapsedY`, `halfY`, `fullY`
   - `currentY`
   - `targetY`
   - render with `transform: translate3d(0, currentYpx, 0)`

2. **Start drag from the current visual position**
   - On `pointerdown`, cancel active animation.
   - Read the current presentation Y, not the old target.
   - Store `grabOffset = event.clientY - currentY`.

3. **Track only while dragging**
   - Set `dragging = true`.
   - Use `setPointerCapture(event.pointerId)`.
   - Ignore unrelated `pointermove`s.

4. **Make movement 1:1**
   - On move: `nextY = event.clientY - grabOffset`.
   - Clamp or rubber-band beyond full/collapsed bounds.
   - Update inside `requestAnimationFrame`.

5. **Record velocity**
   - Keep the last few `{ y, time }` samples.
   - On release, compute px/s velocity.

6. **Snap from projected intent**
   - `projectedY = currentY + projectedDistanceFromVelocity`.
   - Choose nearest of collapsed/half/full from `projectedY`, not only `currentY`.

7. **Hand off velocity into the settle animation**
   - The release animation should begin at the same speed the pointer had at release.
   - Prefer a calm, critically damped or lightly damped spring over fixed `ease-in`.

8. **Make animation interruptible**
   - A new pointerdown during settle should immediately grab the sheet at its visible position.
   - No `animating` lockout that forces the user to wait.

9. **Replace whole-sheet active scale**
   - Move feedback to the drag handle.
   - Example feedback: handle darkens/widens, sheet shadow firms, or header compresses by 1–2px.

10. **Reduced Motion path**
   - On state change, place the sheet with little or no travel.
   - Preserve feedback with a short opacity/elevation/outline/handle-state change.
   - Avoid bounce, long slides, and large spatial displacement.

---

## Verified / unverified boundaries

**Verified from provided code**
- Uses `top` for drag and animation.
- Uses `offsetTop` for snap calculation.
- Uses fixed `480ms ease-in`.
- Uses `transition: all 300ms`.
- Uses whole-sheet `:active` scale.
- Has no shown Reduced Motion branch.
- Has no shown pointer capture, velocity tracking, cancellation, or keyboard handling.

**Not verified from static snippet**
- Actual snap point values.
- Sheet dimensions and viewport constraints.
- Whether another layer manages ARIA, focus, keyboard shortcuts, or scroll locking.
- Runtime frame rate, input latency, or device behavior.
- Whether CSS outside the snippet overrides these rules.

---

## Smallest runtime validation plan

1. **Pointer continuity**
   - Drag from handle, header, and mid-sheet.
   - Confirm no jump on grab and no lost drag when pointer leaves bounds.

2. **Interruptibility**
   - Start collapsed → full animation.
   - Grab mid-flight and reverse.
   - Pass only if the sheet follows immediately from its visible position.

3. **Snap intent**
   - Test slow drags and fast flicks between collapsed, half, and full.
   - Confirm velocity changes the chosen target predictably.

4. **Reduced Motion**
   - Enable reduced motion.
   - Confirm state feedback remains visible but large spatial travel and bounce are removed.

5. **Performance smoke**
   - Drag over the real operations table.
   - Inspect for forced layout, dropped frames, and pointer latency.

6. **Accessibility smoke**
   - Keyboard open/collapse/expand.
   - Focus remains visible and recoverable.
   - Screen reader state names match collapsed/half/full.
