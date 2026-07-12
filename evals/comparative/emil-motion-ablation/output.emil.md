## Verdict

**Evidence-based: not shippable for a repeated-use operations app.**  
The implementation has the shape of a bottom sheet, but the motion model is not direct, interruptible, velocity-aware, or accessibility-complete. It will likely feel jumpy, locked, and imprecise rather than calm and controllable.

---

## Prioritized findings

### P0 — Breaks direct manipulation

**Evidence:**  
```js
sheet.style.top = `${event.clientY}px`;
```

The sheet’s top edge is set to the pointer’s viewport Y on every move. This ignores where the user grabbed the sheet, so the sheet can jump under the pointer instead of staying attached.

**Impact:**  
The sheet feels like it is being repositioned by code, not held by the user.

**Fix direction:**  
Track grab offset:

```js
grabOffset = event.clientY - currentSheetY;
nextY = event.clientY - grabOffset;
```

---

### P0 — Animations are not interruptible

**Evidence:**  
```js
if (animating) return;
animating = true;
```

The user cannot grab the sheet while it is settling.

**Impact:**  
A calm operations tool should preserve agency. Locking input during motion makes the sheet feel modal and brittle.

**Fix direction:**  
On `pointerdown`, cancel any active animation, read the current visual position, and continue from there.

---

### P0 — No velocity handoff or flick behavior

**Evidence:**  
```js
const target = nearestSnapPoint(sheet.offsetTop);
```

The snap point is chosen only from the release position, not from gesture velocity.

**Impact:**  
A slow drag and a fast flick ending at the same position produce the same result. That removes physical believability.

**Fix direction:**  
Track recent pointer samples, compute release velocity, project the likely endpoint, then choose the nearest snap point from that projected value.

---

### P0 — Uses layout properties for gesture motion

**Evidence:**  
```js
sheet.style.top = ...
sheet.offsetTop
animate([{ top: ... }])
```

`top` and `offsetTop` involve layout. This is the wrong primitive for high-frequency gesture motion.

**Impact:**  
Higher risk of jank, layout thrash, and inconsistent frame pacing.

**Fix direction:**  
Use `transform: translateY(...)` for dragging and settling. Keep logical state separately.

---

### P1 — Easing is backwards for settling

**Evidence:**  
```js
{ duration: 480, easing: "ease-in" }
```

`ease-in` accelerates away from the user’s release and then stops abruptly at the target.

**Impact:**  
The release seam feels artificial. For a sheet, the motion should continue from the gesture and decelerate into place.

**Fix direction:**  
Use a spring-like settle or a decelerating curve. In a calm app, prefer critically damped or near-critically-damped motion; reserve bounce for clear flick momentum.

---

### P1 — Fixed duration ignores distance

**Evidence:**  
```js
duration: 480
```

Collapsed → full and half → full take the same time.

**Impact:**  
Short moves feel sluggish; long moves feel too fast or too heavy.

**Fix direction:**  
Use spring response parameters or duration derived from distance and velocity.

---

### P1 — CSS transition fights the gesture

**Evidence:**  
```css
.sheet { transition: all 300ms; }
```

This may animate properties during direct manipulation and can conflict with JS-driven animation.

**Impact:**  
The sheet may lag behind the pointer or animate unintended properties.

**Fix direction:**  
Remove broad transitions from the draggable surface. Apply explicit transitions only to non-positional feedback, such as shadow, opacity, or handle color.

---

### P1 — Whole-sheet active scale is disorienting

**Evidence:**  
```css
.sheet:active { transform: scale(0.96); }
```

Scaling the whole sheet during drag changes the geometry of the thing being dragged. If transform is also used for position, this will conflict.

**Impact:**  
The sheet can appear to shrink away from the user’s finger. In an operations app, this is likely too playful and imprecise.

**Fix direction:**  
Apply subtle press feedback to the drag handle only, not the entire sheet. Prefer handle color, shadow, or a tiny handle compression.

---

### P1 — Pointer handling is incomplete

**Evidence:**  
No `setPointerCapture`, no active pointer tracking, no `pointercancel`, no drag state.

**Impact:**  
Dragging can break if the pointer leaves the element. Multi-pointer or cancelled gestures can leave stale state.

**Fix direction:**  
Capture the pointer on down, ignore non-active pointer IDs, release/cancel cleanly.

---

### P2 — No bounds or rubber-banding

**Evidence:**  
Pointer movement maps directly to `clientY`.

**Impact:**  
The sheet can overshoot collapsed/full positions with no resistance model.

**Fix direction:**  
Clamp within valid snap range, with progressive rubber-band resistance outside the range.

---

### P2 — Reduced Motion is missing

**Evidence:**  
No `prefers-reduced-motion` branch.

**Impact:**  
The product requirement is unmet: reduced motion must preserve state feedback without large spatial travel.

**Fix direction:**  
For reduced motion, avoid large animated travel. Use immediate state placement plus short opacity, scrim, shadow, border, or handle-state feedback.

---

## Concrete direct-manipulation moves

1. **Represent state explicitly**
   - `collapsed`, `half`, `full`
   - Store snap Y values and current logical state.

2. **Use transform-only movement**
   - `translateY(currentY)`
   - Avoid `top` during interaction.

3. **On pointer down**
   - Cancel active settle animation.
   - Read current visual Y.
   - Store `pointerId`.
   - Call `setPointerCapture`.
   - Store grab offset.
   - Begin collecting position/time samples.

4. **On pointer move**
   - Ignore unrelated pointers.
   - Compute `nextY = event.clientY - grabOffset`.
   - Apply clamping or rubber-band resistance.
   - Update transform in `requestAnimationFrame`.

5. **On pointer up**
   - Compute release velocity from recent samples.
   - Project endpoint.
   - Snap to nearest of collapsed/half/full based on projection.
   - Animate from current visual Y to target Y with velocity handoff.

6. **During settling**
   - Remain interruptible.
   - A new pointerdown should stop the current animation and continue from the current visual position.

7. **Reduced Motion**
   - Commit the new state without large travel.
   - Use short non-spatial feedback: handle emphasis, shadow change, opacity/scrim adjustment, or state label announcement.

---

## Verified / unverified boundaries

### Verified from the provided code

- Input is locked during animation.
- Dragging uses `top`, not transform.
- Grab offset is not used.
- Velocity is not tracked.
- Snap target uses release position only.
- Reduced Motion handling is absent.
- `transition: all` can affect unintended properties.
- Whole-sheet `:active` scale conflicts with sheet positioning.

### Not verified here

- Actual frame rate or jank.
- Behavior on specific browsers or devices.
- Interaction with internal sheet scrolling.
- Keyboard support and focus management.
- Screen reader announcements.
- Visual styling quality beyond the provided CSS.
- Whether `nearestSnapPoint` itself is correct.

---

## Smallest runtime validation plan

1. **Directness**
   - Press at top, middle, and handle area.
   - Confirm the sheet does not jump on first move.

2. **Interruptibility**
   - Release toward a snap point, then grab mid-settle.
   - Confirm the sheet follows immediately from its current visual position.

3. **Velocity**
   - Compare slow drag vs quick flick from the same release position.
   - Confirm flicks can advance to the projected snap point.

4. **Bounds**
   - Drag beyond full and collapsed.
   - Confirm resistance, not a hard stop or unlimited travel.

5. **Reduced Motion**
   - Enable reduced motion.
   - Change collapsed/half/full states.
   - Confirm state feedback remains clear without large animated travel.

6. **Performance smoke check**
   - Inspect whether drag updates stay on `transform`.
   - Confirm no broad `transition: all` affects positional movement.
