## Verdict

**[Static-code verdict] Not production-ready for a calm, repeatedly used gesture sheet.**  
The implementation is position-snapping code, not direct manipulation. It will likely feel jumpy, laggy, non-interruptible, and inconsistent across collapsed / half / full states. Reduced Motion is not addressed.

---

## Prioritized findings

1. **Input is locked during animation**
   - **[Observed]** `if (animating) return;`
   - **[Risk]** Users cannot grab the sheet mid-flight, reverse direction, or correct mistakes. This makes the sheet feel like it “belongs to the app,” not the user.

2. **Drag does not preserve grab offset**
   - **[Observed]** `sheet.style.top = \`${event.clientY}px\`;`
   - **Risk]** The sheet’s top jumps to the pointer’s Y coordinate instead of staying under the original grab point. This breaks direct manipulation immediately.

3. **Pointer movement is not scoped to an active drag**
   - **[Observed]** `pointermove` always mutates the sheet.
   - **[Risk]** Any pointer movement over the sheet can reposition it, even if no drag was intentionally started.

4. **No pointer capture**
   - **[Observed]** No `setPointerCapture(event.pointerId)`.
   - **[Risk]** Drag tracking can fail when the pointer leaves the sheet bounds, especially during fast pulls.

5. **No velocity, projection, or gesture intent**
   - **[Observed]** `nearestSnapPoint(sheet.offsetTop)` uses only current position.
   - **[Risk]** A fast flick and a slow drag ending at the same point behave identically. The sheet will feel dull and sometimes wrong.

6. **Uses `top` for continuous motion**
   - **[Observed]** JS writes `style.top`; WAAPI animates `top`; code reads `offsetTop`.
   - **[Risk]** This can trigger layout work during drag and animation. For a frequently used operations app, this risks visible stutter.

7. **CSS transition conflicts with gesture tracking**
   - **[Observed]** `.sheet { transition: all 300ms; }`
   - **[Risk]** Every `top` write may trail behind the pointer instead of tracking 1:1. `transition: all` also animates unrelated property changes unpredictably.

8. **Release animation easing is backwards for settling**
   - **[Observed]** `easing: "ease-in"`
   - **[Risk]** The snap accelerates into the destination instead of decelerating or settling. It may feel like the sheet is being pulled away from the user.

9. **Fixed 480ms duration is likely too slow and non-adaptive**
   - **[Observed]** `{ duration: 480 }`
   - **[Risk]** A small snap and a large snap take the same time. Repeated daily use benefits from quick, calm, distance-aware motion.

10. **State is not explicit**
   - **[Observed]** No stored state for `collapsed`, `half`, `full`.
   - **[Risk]** Visual position, logical state, accessibility state, and reduced-motion feedback can drift apart.

11. **Reduced Motion is missing**
   - **[Observed]** No `prefers-reduced-motion` handling.
   - **[Risk]** Large spatial travel remains mandatory. The stated requirement is not met.

12. **Whole-sheet active scale is questionable**
   - **[Observed]** `.sheet:active { transform: scale(0.96); }`
   - **[Risk]** Scaling the full sheet during drag can distort spatial mapping, affect perceived position, and feel playful rather than calm. A handle/header affordance would be safer.

---

## Concrete direct-manipulation moves

1. **Model the sheet as a stateful Y transform**
   - Use `collapsedY`, `halfY`, `fullY`.
   - Store current state separately from visual position.
   - Move with `transform: translateY(...)`, not `top`.

2. **Track an active drag session**
   - On `pointerdown`: record `pointerId`, sheet’s current visual Y, pointer Y, and grab offset.
   - Call `setPointerCapture`.
   - Ignore unrelated pointer moves.

3. **Move 1:1 during drag**
   - New position should be based on:  
     `startSheetY + (event.clientY - startPointerY)`
   - Not raw `event.clientY`.

4. **Disable CSS transitions during active drag**
   - No transition should mediate pointer movement.
   - The sheet should stay visually attached to the pointer.

5. **Track recent pointer samples**
   - Keep a small history of `{ y, time }`.
   - On release, compute velocity in px/s.

6. **Choose snap target from projected endpoint**
   - Use current Y + velocity projection.
   - Snap to collapsed / half / full nearest to that projected endpoint.
   - This lets flicks carry intent.

7. **Use an interruptible spring-like settle**
   - Start from the current visual transform.
   - Hand off release velocity.
   - Favor critically damped or lightly damped motion: calm, quick, no theatrical bounce.

8. **Allow interruption**
   - If the user presses during settle, cancel/retarget from the current visual position.
   - Do not block pointerdown because an animation exists.

9. **Add soft bounds**
   - Above full or below collapsed, apply progressive resistance instead of hard clamping.
   - On release, settle back to the nearest valid state.

10. **Reduced Motion behavior**
   - Preserve state changes without large travel:
     - update state immediately or with very short opacity/color/handle feedback;
     - avoid long slides, bounce, and overshoot;
     - keep clear collapsed / half / full affordance through label, handle state, shadow, or scrim intensity.

---

## Verified / unverified boundaries

**Verified from static code only**
- The implementation mutates `top`.
- It uses `transition: all`.
- It blocks input while `animating`.
- It does not preserve grab offset.
- It does not use pointer capture.
- It does not calculate velocity.
- It does not handle Reduced Motion.
- It uses fixed-duration `ease-in` release animation.

**Not verified**
- Actual frame rate or jank.
- Browser-specific WAAPI behavior.
- Touch-device behavior.
- Pointer cancellation behavior.
- Snap-point correctness.
- Visual feel of the scale transform.
- Accessibility state exposure.
- Reduced Motion behavior in runtime.

---

## Smallest runtime validation plan

1. **Manual interaction checks**
   - Drag slowly from collapsed → half → full.
   - Flick up/down from each state.
   - Grab while the sheet is settling and reverse direction.
   - Drag outside sheet bounds after starting inside.
   - Overscroll past full/collapsed and release.

2. **Motion checks**
   - Confirm no jump on pointerdown.
   - Confirm sheet stays under the grab point.
   - Confirm release begins from current visual position.
   - Confirm small moves settle quickly and large moves do not feel sluggish.
   - Confirm flick direction can override nearest-position-only snapping.

3. **Reduced Motion checks**
   - Enable reduced motion.
   - Change between collapsed / half / full.
   - Confirm state feedback remains clear without large spatial travel, bounce, or long sliding.

4. **Performance checks**
   - Record a short drag trace.
   - Look for layout/recalculate-style spikes during pointermove.
   - Confirm motion uses compositor-friendly properties where possible.
