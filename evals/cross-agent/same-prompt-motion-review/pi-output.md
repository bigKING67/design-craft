## 1. Evidence level and design read

**Evidence level:** Static-source critique only. I can verify explicit code choices, missing branches, and likely design risks. I cannot verify perceived smoothness, frame rate, computed styles, browser behavior, touch feel, Reduced Motion behavior, or real interruption without runtime traces.

**Design read:** Reading this as a **web operations bottom sheet for repeated daily use**, with a **calm utility UI**, optimized for **preserving task context while users drag between collapsed / half / full states**.

**Verdict:** **Block for motion approval.** The current implementation breaks direct manipulation: it animates the wrong properties, locks input during settle, uses lag-inducing easing/timing, and has no Reduced Motion path.

---

## 2. Should this motion exist?

Yes, but only as **causal motion**:

- **Should exist**
  - Immediate pointer-down affordance.
  - 1:1 sheet tracking while dragged.
  - Short, interruptible settle to the chosen snap point.
  - Subtle boundary resistance if pulled beyond valid range.
  - Reduced Motion state feedback without large spatial travel.

- **Should not animate**
  - Continuous drag position via CSS transition.
  - `top` / layout movement during drag or settle, if avoidable.
  - `transition: all`.
  - Whole-sheet `scale(0.96)` during active drag.
  - Long `480ms ease-in` settle after release.
  - Any lockout that prevents grabbing the sheet mid-flight.

---

## 3. Prioritized blocking findings

1. **Drag is not 1:1 because `transition: all 300ms` applies to `top`.**  
   Every `pointermove` sets `sheet.style.top`, but CSS asks the browser to interpolate changes over 300ms. That makes the sheet chase the pointer instead of staying attached to it.

2. **The sheet jumps to the pointer because grab offset is not preserved.**  
   `startY` is recorded but unused; `pointermove` sets `top = event.clientY`. If the user grabs the sheet away from its top edge, the sheet can snap so its top aligns with the finger. Direct manipulation should preserve the initial offset.

3. **Input is locked during settle, so interruption fails.**  
   `if (animating) return` on `pointerdown` prevents users from grabbing the sheet while it is moving. A draggable sheet must retarget from its current presentation value, not wait for a previous animation to finish.

4. **Settle physics are backwards for a utility sheet.**  
   `duration: 480` with `ease-in` delays early response and feels heavy. Release motion should start immediately from current velocity, usually with an ease-out/spring-like settle, not accelerate away after release.

5. **No Reduced Motion branch for meaningful spatial travel.**  
   The interaction depends on large vertical movement and scale feedback, but there is no `prefers-reduced-motion` handling. Reduced Motion should preserve state feedback while removing large travel, elastic effects, and unnecessary scale.

---

## 4. Concrete design moves

1. **Pointer-down feedback**  
   Give feedback on the handle/header, not the whole sheet: e.g. handle color/opacity, slight elevation, cursor change, or a very small `scaleY`/brightness change. Avoid shrinking the entire content area.

2. **1:1 tracking**  
   On drag start, store:
   - current sheet presentation Y in CSS px,
   - pointer Y in CSS px,
   - `grabOffset = pointerY - sheetY`.  
   During drag: `sheetY = pointerY - grabOffset`, after intent threshold.

3. **Use transform ownership instead of `top` animation**  
   Prefer `transform: translateY(...)` for the moving layer. If press feedback also needs transform, use nested wrappers:
   - outer wrapper owns `translateY`,
   - inner wrapper owns press/elevation feedback.

4. **Presentation-value interruption**  
   Do not block `pointerdown` while settling. On new drag:
   - cancel/read the active animation,
   - derive current on-screen Y,
   - continue from that value without a visual jump,
   - preserve or reset velocity intentionally.

5. **Velocity handoff**  
   Track recent pointer samples with monotonic timestamps. Compute release velocity in **CSS px/s**. Start the settle animation from the measured release velocity, bounded to avoid wild throws.

6. **Projected endpoints**  
   Keep current `nearestSnapPoint(current)` semantics unless product approval says momentum should affect target selection. If authorized, use a bounded projected endpoint: current presentation Y + velocity-based projection, clamped to valid snap range, then choose nearest snap.

7. **Soft boundaries**  
   Clamp hard state endpoints, but render overshoot with progressive resistance near collapsed/full bounds. This preserves agency without letting the sheet detach from the app’s spatial model.

8. **Reduced Motion**  
   Under `prefers-reduced-motion: reduce`:
   - remove large animated travel where possible,
   - snap or use very short settle,
   - avoid elastic overshoot and scale,
   - preserve state feedback with handle color, label/state announcement, shadow/elevation change, or short opacity/color transitions.

---

## 5. Verified versus unverified claims

**Verified from static code**

- `top` is mutated on every `pointermove`.
- `transition: all 300ms` exists on `.sheet`.
- `pointerdown` is ignored while `animating`.
- `pointerup` uses `sheet.animate(... top ..., { duration: 480, easing: "ease-in" })`.
- `startY` is stored but not used in the shown code.
- No Reduced Motion branch is shown.
- `.sheet:active` applies `transform: scale(0.96)`.

**Reasoned risks, not runtime-verified**

- Perceived lag during drag.
- Visual jump on grab.
- Layout/reflow cost from animating `top`.
- WAAPI/CSS transition conflicts in specific browsers.
- Exact smoothness, frame drops, or touch feel.
- Whether `fill: forwards` causes later presentation/style mismatch in this environment.
- Whether pointer capture bugs occur when dragging outside the sheet.

---

## 6. Minimal browser/device validation plan before approval

1. **Desktop browser pointer test**
   - Drag from handle and body.
   - Confirm no jump on grab.
   - Confirm sheet stays 1:1 with pointer.
   - Confirm dragging outside bounds continues via pointer capture.

2. **Interruption test**
   - Release toward a snap point.
   - Re-grab mid-settle.
   - Confirm no lockout and no visual jump.

3. **Velocity / target test**
   - Slow drag near thresholds.
   - Fast flick up/down.
   - Verify whether target selection matches the approved product rule.

4. **Reduced Motion test**
   - Enable `prefers-reduced-motion`.
   - Confirm state feedback remains clear without large travel, bounce, or scale.

5. **Touch hardware test**
   - Real touch device or high-fidelity simulator.
   - Check finger attachment, scroll conflict, boundary resistance, and accidental taps.

6. **Performance check**
   - Record timeline while dragging over realistic app content.
   - Confirm compositor-friendly movement, no repeated layout hot path, and stable frame pacing.
