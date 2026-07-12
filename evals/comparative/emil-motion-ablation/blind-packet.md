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

**Verdict — Block [static evidence + product context]**  
This is not ready for a calm, repeatedly used operations sheet. The snippet treats the sheet like a timed layout animation, not a direct-manipulation surface with collapsed/half/full state, interruption, velocity, and reduced-motion behavior.

## Prioritized findings

1. **Drag is not 1:1 direct manipulation [static evidence]**  
   `pointermove` sets `top = event.clientY`, so the sheet’s top jumps to the pointer instead of preserving the grab offset. `startY` is recorded but unused.

2. **Pointer tracking is unsafe [static evidence]**  
   There is no active-drag flag, pointer id, pointer capture, `pointercancel`, or lost-capture handling. A move can update the sheet even after an ignored `pointerdown` or during an animation.

3. **Release physics are wrong for a snap sheet [static evidence]**  
   Snap target is based only on `sheet.offsetTop`, not release velocity or projected endpoint. Quick flicks and slow drags at the same release position will resolve identically.

4. **The sheet is non-interruptible [static evidence]**  
   `animating` blocks new starts until `.finished`; a user cannot grab the sheet mid-settle and retarget it from the current visual position. This will feel especially wrong in repeated daily use.

5. **Animation timing/easing fights responsiveness [static evidence + product fit]**  
   `480ms` with `ease-in` delays the beginning of the release response. For a functional ops surface, the settle should feel immediate, calm, and short, usually spring-like or ease-out/critically damped.

6. **Performance risk from layout animation [static evidence]**  
   Animating and repeatedly writing `top`, then reading `offsetTop`, risks layout work during the gesture. `transition: all 300ms` can also animate unintended properties and make drag updates lag behind the finger.

7. **CSS motion conflicts with gesture ownership [static evidence]**  
   `.sheet:active { transform: scale(0.96); }` gives `transform` to press feedback while JS owns `top`. If the sheet later moves via `transform`, scale and translation will conflict unless separated into layers.

8. **Reduced Motion requirement is unmet [static evidence + requirement]**  
   There is no `prefers-reduced-motion` branch. Reduced Motion must still show state feedback without large spatial travel; this implementation always performs spatial travel.

9. **Final state may desync [static evidence]**  
   `fill: "forwards"` preserves the visual animation result but does not make the final `top` the durable source of truth. Future reads/state can drift unless the final value is committed.

10. **State model is missing [static evidence]**  
   Collapsed/half/full are implied only by `nearestSnapPoint`; there is no explicit current state, state announcement, keyboard path, or reduced-motion state feedback.

## Concrete direct-manipulation moves

1. **Introduce explicit sheet state**  
   Track `state: "collapsed" | "half" | "full"` plus a numeric `y` presentation value.

2. **Use pointer capture and an active pointer id**  
   On `pointerdown`, capture the pointer, store `pointerId`, starting pointer Y, current sheet Y, and grab offset. Ignore other pointers until release/cancel.

3. **Preserve grab offset**  
   Move by delta: `nextY = sheetStartY + (event.clientY - pointerStartY)`, not by absolute `clientY`.

4. **Move with compositor-friendly transforms**  
   Use `transform: translate3d(0, ypx, 0)` for the sheet motion. Remove `transition: all`; animate only named properties. If press scale remains, put it on an inner wrapper or compose transforms explicitly.

5. **Add intent threshold and scroll coordination**  
   Use roughly an 8–12px vertical threshold before committing to drag. Coordinate with page scroll using an appropriate handle region and `touch-action` strategy.

6. **Measure velocity**  
   Keep recent `{ y, time }` samples and compute release velocity in CSS px/s.

7. **Choose snap by projected endpoint**  
   Resolve target from projected release position, not just current position. This lets a quick flick to full/collapsed work naturally.

8. **Settle with an interruptible spring**  
   Start the settle from the current presentation value with current velocity. Allow a new pointerdown to cancel/retarget without a jump.

9. **Add soft boundaries**  
   Clamp snap targets, but apply gentle resistance when dragging beyond collapsed/full instead of a hard stop.

10. **Commit final state after settle**  
   Write the final durable value and semantic state; do not rely on `fill: forwards` as the state source.

11. **Reduced Motion path**  
   For reduced motion, avoid large animated travel: snap state immediately or with a very short non-spatial cue, such as handle highlight, opacity change, label/state indicator, or subtle elevation change. No overshoot or elastic travel.

12. **Handle cancellation and failures**  
   On `pointercancel`, lost capture, or animation cancellation, settle or restore predictably; ensure `animating` cannot remain stuck after a rejected `.finished`.

## Verified / unverified boundaries

**Verified from the snippet only:**  
- Uses `top` for drag and release animation.  
- Uses `offsetTop` to choose target.  
- Uses fixed `480ms` `ease-in`.  
- Uses `transition: all 300ms`.  
- Has no visible velocity, projection, pointer capture, pointer cancel, reduced-motion, or explicit state branch.  
- No files were edited.

**Unverified:**  
- Actual browser smoothness, frame rate, and device feel.  
- Whether surrounding CSS/layout makes `top` visually worse or partially masked.  
- Whether `nearestSnapPoint` has hysteresis, bounds, or state semantics elsewhere.  
- Touch scrolling conflicts on real hardware.  
- Keyboard/focus/ARIA behavior outside the snippet.  
- Reduced-motion behavior in the complete app.

## Smallest runtime validation plan

1. **Static unit checks**  
   Test snap selection for slow drag, fast upward flick, fast downward flick, and boundary cases.

2. **Pointer interaction smoke**  
   Verify: drag starts after threshold, preserves grab offset, tracks outside sheet via capture, handles cancel, ignores secondary pointers.

3. **Interruption check**  
   Release to settle, then grab mid-animation; sheet must continue from the visible position without jumping.

4. **Three-state behavior**  
   Exercise collapsed → half → full and reverse with both slow drags and flicks.

5. **Reduced Motion check**  
   Enable reduced motion and confirm state changes still provide feedback without large spatial travel, overshoot, or long settling.

6. **Performance check under normal app load**  
   Confirm drag path avoids layout-property animation and does not visibly lag during repeated use.


## Output B

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


## Output C

## Evidence-labeled verdict

**Verdict [code + CSS evidence]: Not production-fit as-is.**  
The implementation is likely to feel jumpy, laggy, and spatially heavy, which conflicts with a calm operations app used repeatedly throughout the day. It also lacks reliable state handling for collapsed / half / full and does not satisfy the Reduced Motion requirement.

---

## Prioritized findings

### P0 — Reduced Motion is missing
**Evidence:** No `prefers-reduced-motion` handling; animation always travels spatially for `480ms`.  
**Impact:** Users who request reduced motion still get large sheet travel.  
**Expected:** State feedback should remain, but large travel should be removed or minimized.

### P0 — Drag is not true direct manipulation
**Evidence:** `pointermove` sets `sheet.style.top = event.clientY`.  
**Impact:** The sheet top snaps to the pointer’s viewport Y instead of preserving the grab offset. This causes jumps, especially when grabbing below the top edge.  
**Expected:** Movement should be based on `deltaY` from pointerdown and clamped to snap bounds.

### P0 — CSS transition fights pointer movement
**Evidence:** `.sheet { transition: all 300ms; }` while JS updates `top` on every move.  
**Impact:** The sheet will chase the finger instead of staying attached to it. This creates lag and imprecision.  
**Expected:** Disable transitions while dragging; animate only on release.

### P0 — Pointer lifecycle is incomplete
**Evidence:** No `setPointerCapture`, no active-drag flag, no `pointercancel`, no primary-pointer check.  
**Impact:** The sheet can keep moving after an unintended pointer sequence, miss release events, or react to stray moves.  
**Expected:** Track one active pointer, capture it, and clean up on `pointerup` / `pointercancel`.

### P1 — Animation state can become inconsistent
**Evidence:** `animating` only blocks `pointerdown`; `pointermove` and `pointerup` can still run.  
**Impact:** A user can mutate position during an animation or trigger new release logic without a valid drag.  
**Expected:** Ignore moves/up unless actively dragging, and cancel/commit existing animations deliberately.

### P1 — `top` causes layout work on every frame
**Evidence:** Per-move writes to `style.top`; release reads `sheet.offsetTop`.  
**Impact:** Layout-bound motion is more likely to stutter than compositor motion.  
**Expected:** Use `transform: translateY(...)` for drag and settle motion.

### P1 — Release motion feels wrong for a calm utility surface
**Evidence:** `duration: 480`, `easing: "ease-in"`.  
**Impact:** `ease-in` accelerates into the snap point and can feel abrupt at the end. `480ms` may feel slow for repeated daily use.  
**Expected:** Use distance-aware duration and an ease-out / critically damped curve with no bounce.

### P1 — Snap decision ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only uses position.  
**Impact:** A deliberate upward or downward flick may snap opposite to user intent.  
**Expected:** Use current position plus velocity projection, with clear thresholds for collapsed / half / full.

### P1 — Whole-sheet `:active` scale is disruptive
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** The content compresses under the pointer, visual anchors shift, and it may conflict with transform-based dragging.  
**Expected:** Prefer subtle handle, shadow, scrim, or state-label feedback instead of scaling the entire sheet.

### P2 — `transition: all` is too broad
**Evidence:** CSS transitions every animatable property.  
**Impact:** Future style changes may animate unintentionally, including color, size, shadow, or layout properties.  
**Expected:** Restrict transitions to intentional properties only.

### P2 — No bounds or viewport/safe-area handling shown
**Evidence:** Drag target is raw `clientY`.  
**Impact:** Sheet can be dragged beyond valid collapsed/full limits.  
**Expected:** Clamp to snap range and account for viewport changes and safe areas.

### P2 — Accessibility/state semantics are absent
**Evidence:** Pointer-only implementation; no visible state model shown.  
**Impact:** Keyboard and assistive-technology users may not be able to operate or understand sheet state.  
**Expected:** Provide keyboard controls, focus behavior, and clear state feedback for collapsed / half / full.

---

## Concrete direct-manipulation moves

1. **Track drag state explicitly**
   - On `pointerdown`: require primary pointer, store `pointerId`, capture pointer, cancel any running animation.
   - Store `startPointerY`, `startSheetY`, and current snap state.

2. **Move by delta, not absolute pointer position**
   - On `pointermove`: if active pointer, compute  
     `nextY = clamp(startSheetY + event.clientY - startPointerY, fullY, collapsedY)`.

3. **Use compositor motion**
   - Apply movement with `transform: translate3d(0, nextY, 0)` or a CSS variable driving transform.
   - Avoid `top` during drag.

4. **Disable transitions while dragging**
   - Add an `.is-dragging` class with `transition: none`.
   - Re-enable settle animation only after release.

5. **Snap using intent**
   - On release, calculate velocity from recent pointer samples.
   - Project position slightly forward.
   - Choose collapsed / half / full using both projected position and direction.

6. **Use calm release motion**
   - Prefer short, distance-based duration, e.g. roughly `160–280ms`.
   - Use ease-out or a damped spring without bounce.
   - Avoid `ease-in` for sheet settling.

7. **Preserve state feedback in Reduced Motion**
   - Immediately set the final state or use very short motion.
   - Use non-spatial feedback: handle color, shadow depth, label, border emphasis, or scrim opacity.
   - Avoid large sheet travel animation.

8. **Replace whole-sheet active scale**
   - Remove `scale(0.96)` from the entire sheet.
   - If feedback is needed, animate only the drag handle or surface elevation subtly.

9. **Commit final state**
   - After settle, write the final transform/state as the source of truth.
   - Clear/cancel animation objects so later drags start from a stable value.

---

## Verified / unverified boundaries

**Verified from provided code:**
- No Reduced Motion branch is present.
- Drag uses `top` and raw `clientY`.
- CSS uses `transition: all`.
- Release easing is `ease-in`.
- `startY` is assigned but not used.
- No pointer capture or cancel handling is shown.

**Unverified from provided code:**
- Actual visual frame rate.
- Whether `sheet` is absolutely/fixed positioned.
- Exact snap-point values.
- Existing keyboard/ARIA behavior elsewhere.
- Real device behavior, browser behavior, or touch-scroll conflicts.
- Whether other code prevents conflicting pointer events.

---

## Smallest runtime validation plan

1. **Pointer lifecycle**
   - Drag from handle, content area, and near sheet edge.
   - Release inside and outside the sheet.
   - Trigger `pointercancel` path if supported.

2. **Motion feel**
   - Slow drag to each state.
   - Fast flick upward/downward.
   - Verify snap matches user intent.

3. **Directness**
   - Confirm sheet stays attached to the finger/pointer with no lag while dragging.
   - Confirm no jump on initial grab.

4. **Reduced Motion**
   - Enable reduced motion.
   - Verify final state changes remain clear without large spatial travel.

5. **Bounds/state**
   - Try dragging past collapsed and full limits.
   - Confirm final state is always one of collapsed / half / full.

6. **Keyboard/accessibility**
   - Operate equivalent controls without pointer.
   - Confirm focus remains predictable after state changes.
