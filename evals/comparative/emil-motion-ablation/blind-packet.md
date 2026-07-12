# Blind comparative judgment
Judge only the supplied outputs. Do not infer which skill produced a label. Apply the machine-readable scorecard exactly, recompute each total from criterion points, and return only JSON matching the supplied schema.

## Task prompt

# Gesture-sheet motion critique

Critique this static gesture-sheet implementation. Do not edit files and do not
claim browser or device validation.
Do not name, cite, or reveal any skill, repository, author, or upstream source
in the response; the output will be judged blind.

```js
let animating = false;

sheet.addEventListener("pointerdown", (event) => {
  if (animating) return;
  startY = event.clientY;
});

sheet.addEventListener("pointermove", (event) => {
  sheet.style.top = `${event.clientY}px`;
});

sheet.addEventListener("pointerup", () => {
  animating = true;
  const target = nearestSnapPoint(sheet.offsetTop);
  sheet.animate(
    [{ top: `${sheet.offsetTop}px` }, { top: `${target}px` }],
    { duration: 480, easing: "ease-in", fill: "forwards" },
  ).finished.then(() => {
    animating = false;
  });
});
```

```css
.sheet { transition: all 300ms; }
.sheet:active { transform: scale(0.96); }
```

Product context: a calm web operations app used repeatedly during the day. The
sheet has collapsed, half, and full states. Reduced Motion must preserve state
feedback without large spatial travel.

Return a concise evidence-labeled verdict, prioritized findings, concrete
direct-manipulation moves, verified/unverified boundaries, and the smallest
runtime validation plan. Stay within 150 lines.


## Human-readable scorecard

# Blind scorecard

Grade anonymized raw outputs. Do not reward brand or skill-name mentions.

| Criterion | Weight | Full-credit evidence |
|---|---:|---|
| Evidence honesty | 15 | Labels the input as static and avoids smoothness/runtime claims. |
| Motion necessity | 10 | Separates causal feedback from decorative or unnecessary animation. |
| Direct manipulation | 15 | Catches input lockout, pointer capture, grab offset, and 1:1 tracking. |
| Interruption and presentation value | 15 | Requires interruption from the current on-screen value without jumps. |
| Velocity and projection | 15 | Preserves release velocity, units, projected endpoints, and snap selection. |
| Property/performance discipline | 10 | Rejects `top`, `transition: all`, and conflicting transform ownership. |
| Accessibility | 10 | Defines a non-vestibular Reduced Motion path with preserved feedback. |
| Actionability and scope | 10 | Gives prioritized implementation moves and a minimal runtime plan within 150 lines. |

Total: 100.


## Machine-readable scorecard

```json
{
  "schema": "design-craft.comparative-scorecard.v1",
  "total": 100,
  "criteria": [
    {
      "id": "evidence_honesty",
      "label": "Evidence honesty",
      "weight": 15,
      "full_credit": "Labels the input as static and avoids smoothness or runtime claims."
    },
    {
      "id": "motion_necessity",
      "label": "Motion necessity",
      "weight": 10,
      "full_credit": "Separates causal feedback from decorative or unnecessary animation."
    },
    {
      "id": "direct_manipulation",
      "label": "Direct manipulation",
      "weight": 15,
      "full_credit": "Catches input lockout, pointer capture, grab offset, and one-to-one tracking."
    },
    {
      "id": "interruption",
      "label": "Interruption and presentation value",
      "weight": 15,
      "full_credit": "Requires interruption from the current on-screen value without jumps."
    },
    {
      "id": "velocity_projection",
      "label": "Velocity and projection",
      "weight": 15,
      "full_credit": "Preserves release velocity, units, projected endpoints, and snap selection."
    },
    {
      "id": "performance",
      "label": "Property and performance discipline",
      "weight": 10,
      "full_credit": "Rejects layout-property motion, transition-all, and conflicting transform ownership."
    },
    {
      "id": "accessibility",
      "label": "Accessibility",
      "weight": 10,
      "full_credit": "Defines a non-vestibular Reduced Motion path with preserved feedback."
    },
    {
      "id": "actionability",
      "label": "Actionability and scope",
      "weight": 10,
      "full_credit": "Gives prioritized implementation moves and a minimal runtime plan within the output budget."
    }
  ]
}
```

## Required judgment schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["results", "winner", "rationale"],
  "properties": {
    "results": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": {
        "type": "object",
        "required": ["label", "criteria", "total", "summary"],
        "properties": {
          "label": {"enum": ["A", "B", "C"]},
          "criteria": {
            "type": "object",
            "required": [
              "evidence_honesty",
              "motion_necessity",
              "direct_manipulation",
              "interruption",
              "velocity_projection",
              "performance",
              "accessibility",
              "actionability"
            ],
            "additionalProperties": false,
            "properties": {
              "evidence_honesty": {"type": "integer", "minimum": 0, "maximum": 15},
              "motion_necessity": {"type": "integer", "minimum": 0, "maximum": 10},
              "direct_manipulation": {"type": "integer", "minimum": 0, "maximum": 15},
              "interruption": {"type": "integer", "minimum": 0, "maximum": 15},
              "velocity_projection": {"type": "integer", "minimum": 0, "maximum": 15},
              "performance": {"type": "integer", "minimum": 0, "maximum": 10},
              "accessibility": {"type": "integer", "minimum": 0, "maximum": 10},
              "actionability": {"type": "integer", "minimum": 0, "maximum": 10}
            }
          },
          "total": {"type": "integer", "minimum": 0, "maximum": 100},
          "summary": {"type": "string", "minLength": 20}
        },
        "additionalProperties": false
      }
    },
    "winner": {"enum": ["A", "B", "C"]},
    "rationale": {"type": "string", "minLength": 40}
  },
  "additionalProperties": false
}
```

## Output A

## Verdict

**Evidence-based: not production-ready for a calm repeated-use operations sheet.**  
The implementation will feel jumpy, laggy, and hard to control because it treats gesture input as raw absolute positioning, mixes CSS transitions with JS animation, lacks state ownership, and does not honor Reduced Motion requirements.

---

## Prioritized findings

### P0 — Direct manipulation is broken
**Evidence:** `pointermove` always runs and sets `sheet.style.top = event.clientY`.  
**Impact:** The sheet can move without an active drag, jumps to the pointer’s absolute Y position, and ignores the original sheet position.  
**Fix direction:** Track an active pointer, initial pointer Y, and initial sheet Y; move by delta.

---

### P0 — Reduced Motion requirement is unmet
**Evidence:** Release always animates up to `480ms` with large spatial travel. CSS also applies `transform: scale(0.96)` on active.  
**Impact:** Users who request reduced motion still get large movement and scaling.  
**Fix direction:** In reduced motion, snap state immediately or with very short non-spatial feedback: handle highlight, opacity change, state label, subtle border/shadow pulse.

---

### P0 — State is not authoritative
**Evidence:** The code computes `nearestSnapPoint(sheet.offsetTop)` but does not maintain explicit `collapsed | half | full` state.  
**Impact:** Visual position, logical state, and future interactions can drift, especially after animation fill behavior.  
**Fix direction:** Store the current detent as state; commit the final position explicitly after animation.

---

### P1 — CSS transition conflicts with gesture movement
**Evidence:** `.sheet { transition: all 300ms; }` applies to `top`, `transform`, and any future property.  
**Impact:** Dragging can feel delayed because each pointer move may be transitioned instead of matching the finger.  
**Fix direction:** Never transition the property used for live dragging. Scope transitions to safe properties only, e.g. shadow or background.

---

### P1 — `top` causes layout work and weaker motion quality
**Evidence:** The code writes `style.top` during every `pointermove` and reads `offsetTop` on release.  
**Impact:** This risks layout thrash and jank on a frequently used operations UI.  
**Fix direction:** Use `transform: translateY(...)` for live movement and animation; update layout/state only at commit boundaries if needed.

---

### P1 — Release motion feels wrong for a sheet
**Evidence:** `{ duration: 480, easing: "ease-in" }`.  
**Impact:** Ease-in starts sluggish and ends fast, making the sheet feel like it escapes the user. `480ms` is long for repeated daily interactions.  
**Fix direction:** Use an interruptible ease-out/spring-like settle, usually distance-based and shorter, e.g. ~160–280ms.

---

### P1 — No velocity, hysteresis, or intent detection
**Evidence:** Target is chosen only by `nearestSnapPoint(sheet.offsetTop)`.  
**Impact:** A quick upward or downward flick may snap opposite to user intent if the final position is slightly closer to another point.  
**Fix direction:** Project release position using velocity, add hysteresis around the current detent, and support directional flings.

---

### P1 — No bounds or snap constraints during drag
**Evidence:** `event.clientY` is applied directly.  
**Impact:** The sheet can be dragged beyond full/collapsed limits or into invalid visual states.  
**Fix direction:** Clamp live position between full and collapsed detents, with optional resistance past edges.

---

### P2 — Animation is not safely interruptible
**Evidence:** `animating` blocks `pointerdown`, but `pointermove` still writes position. Existing animations are not canceled.  
**Impact:** New gestures can fight old animations; promise handling may be fragile if animations are canceled later.  
**Fix direction:** Keep a reference to the active animation, cancel it on new drag, and always reset state on finish/cancel.

---

### P2 — Missing pointer lifecycle handling
**Evidence:** No `setPointerCapture`, `pointercancel`, `lostpointercapture`, or pointer id tracking.  
**Impact:** Drag can be lost if the pointer leaves the element, another finger touches, or the OS cancels the gesture.  
**Fix direction:** Capture the pointer on drag start, track one pointer id, and clean up on up/cancel/lost capture.

---

### P2 — `:active` scale is risky for this product
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** Scaling the whole sheet during drag can feel playful, unstable, and spatially imprecise. It also conflicts with transform-based sheet movement.  
**Fix direction:** Use calmer feedback: handle compression, shadow change, outline, or slight scrim adjustment.

---

## Concrete direct-manipulation moves

1. **Use a drag handle or clear gesture zone.**  
   Avoid stealing scroll from sheet content.

2. **On pointer down:**  
   - Ignore non-primary pointers.  
   - Cancel any running settle animation.  
   - Capture pointer.  
   - Store `startPointerY`, `startSheetY`, `activePointerId`.

3. **On pointer move:**  
   - Only respond to the active pointer.  
   - Compute `nextY = startSheetY + event.clientY - startPointerY`.  
   - Clamp between `fullY` and `collapsedY`.  
   - Apply via `transform: translateY(nextYpx)`.  
   - Batch writes with `requestAnimationFrame`.

4. **On pointer up/cancel:**  
   - Estimate velocity from recent samples.  
   - Choose target using projected position + velocity + hysteresis.  
   - Commit logical state: `collapsed`, `half`, or `full`.

5. **Settle animation:**  
   - Interruptible.  
   - Distance-based duration.  
   - Ease-out or spring-like, not ease-in.  
   - Commit final transform/state after completion.

6. **Reduced Motion path:**  
   - Avoid large automatic travel.  
   - Snap immediately or use a very short fade/outline/handle pulse.  
   - Preserve state feedback through labels, handle state, shadow, or scrim intensity.

7. **CSS cleanup:**  
   - Replace `transition: all` with targeted transitions.  
   - Do not transition the live drag transform.  
   - Avoid whole-sheet `scale()` during drag.

---

## Verified / unverified boundaries

**Verified from the provided code:**  
- Pointer movement is unconditional.  
- `startY` is stored but unused.  
- Drag position uses absolute `clientY`.  
- Release uses fixed `480ms` ease-in animation.  
- CSS uses `transition: all`.  
- Active state scales the sheet.  
- No explicit reduced-motion branch is present.  
- No pointer capture, cancel handling, velocity, clamping, or state model is shown.

**Unverified:**  
- Actual snap point values.  
- Whether `sheet` is absolutely/fixed positioned.  
- Whether other code handles accessibility, keyboard controls, scroll arbitration, or state.  
- Actual browser/device behavior.  
- Runtime performance.  
- Visual feel in the real product.

---

## Smallest runtime validation plan

1. **Interaction sanity:** drag from collapsed → half → full and back; confirm no jump on first move.  
2. **Interruptibility:** start a drag while settle animation is running; confirm the sheet follows immediately.  
3. **Snap intent:** slow drag near boundaries and quick flicks in both directions; confirm expected detent.  
4. **Bounds:** attempt to drag above full and below collapsed; confirm controlled resistance/clamp.  
5. **Reduced Motion:** enable reduced motion and confirm no large automatic travel, while state feedback remains clear.  
6. **Scroll arbitration:** test sheet content scrolling versus handle dragging.  
7. **Performance check:** inspect for dropped frames during repeated drags; confirm transform-based motion avoids layout-heavy updates.


## Output B

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


## Output C

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
