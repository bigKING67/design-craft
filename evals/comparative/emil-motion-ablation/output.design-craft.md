## Verdict

**[Static evidence] Block for direct-manipulation quality.** The sheet is implemented as a layout-position animation with no active-drag state, no grab offset, no velocity handoff, no interruption, and no Reduced Motion path. For a calm, repeatedly used operations app, this will likely feel laggy, jumpy, and over-animated.

## Prioritized findings

1. **[Static evidence] Drag is not actually tied to a gesture lifecycle**
   - `pointermove` always writes `sheet.style.top`, even when no pointer is down.
   - `startY` is recorded but unused.
   - There is no `activePointerId`, no pointer capture, no `pointercancel`, and no guard against multi-touch or lost pointer-up.

2. **[Static evidence] The sheet jumps to the pointer instead of preserving the grab point**
   - `top = event.clientY` treats the pointer’s viewport Y as the sheet’s top.
   - If the user grabs the handle or middle of the sheet, the sheet can snap so its top aligns with the finger.
   - Correct direct manipulation should preserve `grabOffset = pointerY - currentSheetY`.

3. **[Static evidence] Motion fights the user**
   - `.sheet { transition: all 300ms; }` means every `top` update during drag may be transitioned.
   - That prevents 1:1 tracking and can create a trailing/lagging sheet.
   - `transition: all` also risks animating unrelated properties.

4. **[Static evidence] Layout animation is the wrong primitive**
   - The code animates `top` and reads `offsetTop`.
   - That couples motion to layout instead of compositor-friendly transforms.
   - For a frequently used operations surface, this is a performance and feel risk.

5. **[Static evidence] Release behavior ignores velocity**
   - `nearestSnapPoint(sheet.offsetTop)` only considers final position.
   - A quick upward flick near the half state should be able to resolve to full; a slow drag should resolve by proximity.
   - Current implementation cannot distinguish those cases.

6. **[Static evidence] Interaction is not interruptible**
   - `if (animating) return` blocks new drags while settling.
   - A sheet should be grabbable mid-flight and retarget from its current on-screen position.
   - Worse: `pointermove` has no `animating` guard, so movement during animation may still mutate `top`.

7. **[Static evidence] Easing and duration are mismatched to product context**
   - `480ms` with `ease-in` delays the beginning of motion and feels heavy.
   - A calm operations app used repeatedly should favor crisp, low-drama response.
   - Settling should feel immediate and controlled, not cinematic.

8. **[Static evidence] Reduced Motion is missing**
   - There is no `prefers-reduced-motion` handling.
   - The requirement says Reduced Motion must preserve state feedback without large spatial travel.
   - Current release animation can travel a large distance over 480ms.

9. **[Static evidence] Press feedback conflicts with sheet manipulation**
   - `.sheet:active { transform: scale(0.96); }` scales the whole sheet while it is being grabbed.
   - This changes the perceived anchor under the finger and may conflict with future transform-based dragging.
   - Press feedback should usually be on the handle or a separate wrapper, not the entire moving surface.

10. **[Static evidence] Visual/logical state can drift**
   - WAAPI uses `fill: "forwards"` but does not commit the final `top` to inline style.
   - Future `offsetTop`, inline style, and visual presentation can diverge after animation completion.

## Concrete direct-manipulation moves

1. **Introduce explicit sheet state**
   - Track `collapsed | half | full`.
   - Store snap positions in one coordinate space, e.g. CSS pixels from viewport top or transform Y.

2. **Use a real drag lifecycle**
   - On `pointerdown`: capture pointer, record `activePointerId`, stop any running animation, read current presentation Y, compute `grabOffset`.
   - On `pointermove`: only respond to the active pointer after a small movement threshold.
   - On `pointerup` / `pointercancel`: release capture and settle.

3. **Track 1:1 with the finger**
   - Compute `nextY = event.clientY - grabOffset`.
   - Clamp or rubber-band beyond collapsed/full boundaries.
   - During drag, disable transitions.

4. **Move with transform, not top**
   - Prefer `transform: translate3d(0, var(--sheet-y), 0)`.
   - Keep press scale on a nested handle or compose transforms deliberately with separate wrappers.

5. **Use velocity-aware snapping**
   - Keep a short sample history of `{ y, time }`.
   - On release, compute velocity in CSS px/s.
   - Choose target from a projected endpoint, not only current position.

6. **Make settling interruptible**
   - Do not lock out input while the sheet is animating.
   - A new pointerdown should stop the current animation and start from the current visual Y.
   - Preserve or reset velocity intentionally; do not restart from stale logical state.

7. **Use calmer settle motion**
   - Replace `ease-in` with a controlled ease-out or spring-like settle.
   - Keep normal settle responsive; roughly `220–320ms` is a better starting range than `480ms` for frequent use.
   - Avoid bounce unless the product explicitly wants playful motion.

8. **Add Reduced Motion behavior**
   - For `prefers-reduced-motion: reduce`, avoid large animated travel on release.
   - Commit the state immediately or with a very short non-spatial cue.
   - Preserve feedback through handle emphasis, backdrop opacity, state label, subtle color, or a short opacity/scale cue that does not move the sheet across the screen.

## Verified / unverified boundaries

**Verified from static code only**
- `top` is mutated during pointer movement.
- `top` is animated on release.
- `transition: all 300ms` applies to the sheet.
- `ease-in` and `480ms` are used for settling.
- There is no visible Reduced Motion branch.
- There is no visible pointer capture, velocity sampling, grab-offset preservation, or cancellation handling.

**Unverified / requires runtime evidence**
- Actual perceived smoothness or jank.
- Whether `transition: all` visibly lags pointer tracking in the target browsers.
- Whether page scroll competes with the gesture.
- Whether snap points are correct; `nearestSnapPoint` is not shown.
- Whether WAAPI `fill: forwards` causes observable visual/logical drift in this exact DOM/CSS setup.
- Touch feel on 60Hz/120Hz devices.
- Accessibility behavior with keyboard, screen readers, and reduced-motion settings.

**Validation not performed**
- No browser validation.
- No device validation.
- No performance trace.
- No screenshot/video capture.

## Smallest runtime validation plan

1. **Gesture lifecycle check**
   - Drag from handle, middle, and edge.
   - Verify no jump on pointerdown and no movement when hovering without active drag.

2. **Tracking check**
   - Drag slowly and quickly.
   - Confirm the sheet stays attached to the finger without trailing.

3. **Release check**
   - Test slow drags near each snap point.
   - Test quick flicks up/down from collapsed, half, and full.
   - Confirm target selection matches intent.

4. **Interruption check**
   - Start a settle animation, then grab the sheet mid-flight.
   - Confirm it continues from the current visual position without a jump.

5. **Reduced Motion check**
   - Enable Reduced Motion.
   - Confirm state changes remain clear without large animated travel.

6. **Performance check**
   - Record a short interaction trace during a data-heavy page state.
   - Confirm drag updates avoid layout thrash and maintain smooth frames.
