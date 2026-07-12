## Verdict — **Block for gesture quality and accessibility**

**[Static evidence]** This implementation treats a draggable sheet like a fixed keyframe animation: it animates `top`, locks input during settle, ignores velocity/grab offset, and has no Reduced Motion path. For a calm, repeated-use operations app, the result is likely to feel laggy, jumpy, and over-animated rather than directly manipulated.

---

## Prioritized findings

1. **Layout-position animation in the hot path**
   - **Evidence:** `sheet.style.top = ...`, WAAPI animates `{ top: ... }`, CSS has `transition: all 300ms`.
   - **Impact:** `top` causes layout work and `transition: all` may make drag updates lag behind the pointer instead of staying attached 1:1.

2. **No true direct manipulation contract**
   - **Evidence:** `startY` is stored but unused; pointer move sets `top` to `event.clientY`; no grab offset, threshold, pointer capture, bounds, or `pointercancel`.
   - **Impact:** The sheet can jump to the pointer’s page coordinate and lose tracking if the pointer leaves the element.

3. **Input lockout during animation**
   - **Evidence:** `if (animating) return;` on `pointerdown`.
   - **Impact:** Users cannot interrupt a settling sheet. A sheet should be re-grabbable from its current on-screen position without a visual jump.

4. **Wrong easing/duration for release**
   - **Evidence:** `duration: 480`, `easing: "ease-in"`.
   - **Impact:** `ease-in` delays the initial response after release; 480ms is heavy for a repeatedly used operations surface. Settling should feel immediate and calm, not cinematic.

5. **Missing Reduced Motion behavior**
   - **Evidence:** No `prefers-reduced-motion` branch.
   - **Impact:** Large spatial travel remains mandatory. Requirement says Reduced Motion must preserve state feedback without large travel.

6. **State and presentation can diverge**
   - **Evidence:** WAAPI uses `fill: "forwards"` but does not commit the final logical style/state in the snippet.
   - **Impact:** Future `offsetTop`, snap calculations, or interruptions may read stale layout while the visual sheet appears elsewhere.

7. **Snap target ignores release intent**
   - **Evidence:** `nearestSnapPoint(sheet.offsetTop)` only uses current position.
   - **Impact:** A fast, intentional flick toward collapsed/half/full may be ignored unless it crosses enough distance. Velocity behavior is absent.

8. **Press feedback is too broad and conflicts with drag semantics**
   - **Evidence:** `.sheet:active { transform: scale(0.96); }`
   - **Impact:** Scaling the whole sheet while dragging makes the grabbed object feel unstable. If drag later moves to `transform`, scale/translate ownership will conflict unless layered.

---

## Concrete direct-manipulation moves

1. **Use `transform: translateY(...)` for sheet position**
   - Keep `top`/layout static; drive visible movement with a single transform owner.

2. **Preserve grab offset**
   - On pointer down, compute:
     - current sheet Y in CSS px,
     - pointer Y in CSS px,
     - `grabOffset = pointerY - currentSheetY`.
   - During drag: `sheetY = pointerY - grabOffset`.

3. **Add pointer capture and drag state**
   - On committed drag: `setPointerCapture(event.pointerId)`.
   - Handle `pointerup`, `pointercancel`, and lost capture.

4. **Add small intent hysteresis**
   - Start drag after roughly `8–12px` vertical movement so taps/handle interactions do not become accidental drags.

5. **Track velocity explicitly**
   - Keep recent `{ y, time }` samples using monotonic timestamps.
   - Release velocity unit: **CSS px/s**.

6. **Separate velocity handoff from target selection**
   - If existing product semantics are “nearest current position,” keep `nearestSnapPoint(currentY)`.
   - If momentum targeting is desired, use a bounded projected endpoint:
     - measure release velocity in CSS px/s,
     - compute projected endpoint,
     - clamp to collapsed/half/full bounds,
     - choose nearest snap point to that projected endpoint.

7. **Make settling interruptible**
   - Do not block pointerdown while settling.
   - On new pointerdown, stop the current animation, read the current presentation Y, and continue from there.

8. **Use calm spring-like settling**
   - Prefer a spring/animation primitive with velocity handoff.
   - Starting feel: no/low bounce, damping around critical to lightly damped, response around `0.3–0.4s`.
   - If using duration/easing fallback: shorter, ease-out-like, and interruptible.

9. **Layer transform responsibilities**
   - Outer layer: `translateY`.
   - Inner handle/content layer: subtle press feedback if needed.
   - Avoid the same element owning both drag translation and active scale.

10. **Reduced Motion path**
   - Avoid long spatial travel.
   - Snap state immediately or with very short non-spatial feedback.
   - Preserve state feedback via handle label, selected snap indicator, shadow/border/color change, or subtle opacity—not large travel or elastic motion.

---

## Suggested behavior contract

- **Collapsed / half / full** are explicit logical states.
- Drag uses bounded `translateY` in CSS px.
- Overshoot beyond min/max gets progressive resistance, not a hard jump.
- Release:
  - choose target from current position or authorized projected endpoint,
  - settle from current presentation value,
  - carry measured velocity,
  - commit final logical state and final transform.
- Reduced Motion:
  - no long travel animation,
  - state feedback remains visible and immediate.

---

## Verified / unverified boundaries

### Verified from static snippet
- Animates and mutates `top`.
- Uses `transition: all 300ms`.
- Uses `ease-in` and `480ms` release animation.
- Locks new pointerdown while `animating`.
- Stores but does not use `startY`.
- No visible pointer capture, velocity tracking, bounds, hysteresis, pointercancel, or Reduced Motion handling.
- Whole sheet scales on `:active`.

### Not verified
- Actual runtime smoothness or frame rate.
- Whether browser compositing promotes the element.
- Whether `nearestSnapPoint` has additional threshold logic.
- Whether other code handles ARIA state, focus, scroll locking, or snap announcements.
- Real device/touch feel.
- Behavior at 60Hz vs 120Hz.
- Interaction with page scrolling.

---

## Smallest runtime validation plan

1. **Static-state checks**
   - Confirm collapsed, half, full Y positions and logical state updates.
   - Confirm final committed style/state after animation.

2. **Pointer interaction checks**
   - Drag from handle and body.
   - Move outside sheet bounds while dragging.
   - Release slowly near each snap point.
   - Interrupt while sheet is settling.

3. **Velocity checks**
   - Slow drag vs quick flick toward each state.
   - Confirm target selection matches the intended product rule.

4. **Reduced Motion check**
   - Enable `prefers-reduced-motion`.
   - Confirm no large travel animation.
   - Confirm state feedback remains clear.

5. **Performance check**
   - Inspect whether drag updates avoid layout-property animation.
   - Test while the operations view is under representative data/render load.
