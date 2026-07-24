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

# Comparative scorecard

Generated from `scorecard.json`; do not edit by hand.

| Criterion | Weight | Full credit |
|---|---:|---|
| Evidence honesty | 15 | Labels the input as static and avoids smoothness or runtime claims. |
| Motion necessity | 10 | Separates causal feedback from decorative or unnecessary animation. |
| Direct manipulation | 15 | Catches input lockout, pointer capture, grab offset, and one-to-one tracking. |
| Interruption and presentation value | 15 | Requires interruption from the current on-screen value without jumps. |
| Velocity and projection | 15 | Preserves release velocity, units, projected endpoints, and snap selection. |
| Property and performance discipline | 10 | Rejects layout-property motion, transition-all, and conflicting transform ownership. |
| Accessibility | 10 | Defines a non-vestibular Reduced Motion path with preserved feedback. |
| Actionability and scope | 10 | Gives prioritized implementation moves and a minimal runtime plan within the output budget. |
| **Total** | **100** | |


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

## Verdict — **Block**

**Evidence:** The sheet is a direct-manipulation control with collapsed/half/full states, but the implementation behaves like a layout animation attached to pointer coordinates. It lacks grab offset, pointer capture, active-drag guards, velocity handoff, interruption, reduced-motion behavior, and uses slow/ease-in/layout-property motion. For a calm operations app used repeatedly, this will likely feel laggy, jumpy, and over-animated.

## Prioritized findings

1. **P0 — Not true direct manipulation**
   - **Evidence:** `sheet.style.top = \`${event.clientY}px\`;`
   - The sheet top is set to the pointer’s viewport Y, not to `initialTop + dragDelta`.
   - Result: the sheet can jump so its top aligns under the pointer instead of preserving where the user grabbed it.
   - `startY` is stored but never used.

2. **P0 — Drag can run without an active gesture**
   - **Evidence:** `pointermove` updates `top` unconditionally.
   - Any pointer move over the sheet can move it, even if no valid `pointerdown` started the drag.
   - During `animating`, `pointermove` can still mutate `top`, creating conflicting state.

3. **P0 — Input is locked during settle**
   - **Evidence:** `if (animating) return;` and `animating = true` until `.finished`.
   - A user cannot grab and reverse the sheet mid-animation.
   - Gesture sheets should be interruptible from the current on-screen position, not forced to wait 480ms.

4. **P0 — Layout-property animation on the gesture hot path**
   - **Evidence:** JS writes `top` on every `pointermove`; WAAPI animates `top`; CSS has `transition: all 300ms`.
   - This risks layout/reflow and delayed tracking.
   - `transition: all` can also animate unintended properties and makes direct drag feel like it is chasing the finger.

5. **P0 — Reduced Motion requirement is missing**
   - **Evidence:** No `prefers-reduced-motion` branch.
   - The current settle may travel a large distance over 480ms.
   - Product requirement says reduced motion must preserve state feedback without large spatial travel.

6. **P1 — Settle motion is poorly matched to user release**
   - **Evidence:** `{ duration: 480, easing: "ease-in" }`
   - `ease-in` starts slowly exactly when the user expects immediate release response.
   - Fixed duration ignores distance and release speed; small snaps may feel slow, long snaps may feel heavy.

7. **P1 — No release velocity or bounded projection**
   - **Evidence:** `nearestSnapPoint(sheet.offsetTop)` only uses final layout position.
   - A quick flick and a slow drag to the same point resolve identically.
   - If the product wants momentum-based snapping, this will feel unresponsive. If nearest-position semantics are intentional, velocity still needs to be handed into the settle for continuity.

8. **P1 — No pointer capture / cancellation handling**
   - **Evidence:** No `setPointerCapture`, `pointercancel`, or lost-capture path.
   - Dragging outside the sheet can lose tracking.
   - Multi-pointer or interrupted gestures are undefined.

9. **P1 — Transform ownership conflict is likely**
   - **Evidence:** `.sheet:active { transform: scale(0.96); }`
   - If drag is moved to `transform: translateY(...)`, this active scale will conflict unless transform composition is explicitly owned.
   - For a calm ops tool, `scale(0.96)` on the entire sheet may feel too toy-like or spatially unstable.

10. **P2 — Animation fill leaves state fragile**
    - **Evidence:** `fill: "forwards"` without committing/setting final logical state.
    - The visual end state can diverge from inline `top`, layout state, and the next `offsetTop` read.
    - State should be explicitly committed to collapsed/half/full after settle.

## Concrete direct-manipulation moves

1. Track an explicit drag lifecycle:
   - `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, `currentY`.

2. Preserve grab offset:
   - On down: read the sheet’s current presentation Y.
   - On move: `nextY = startSheetY + (event.clientY - startPointerY)`.
   - Do not set sheet position directly to `event.clientY`.

3. Use pointer capture:
   - Capture on committed drag.
   - Release on `pointerup`, `pointercancel`, and lost capture.

4. Add a small intent threshold:
   - Around `8–12px` before treating movement as a drag, so taps and handle clicks are not hijacked.

5. Move with compositor-friendly transforms:
   - Prefer `transform: translateY(...)` on a motion layer.
   - Keep press scale on a child/wrapper or compose transforms in one owner.

6. Remove hot-path transitions:
   - No `transition: all`.
   - Disable transitions while dragging.
   - Use a controlled settle animation only after release.

7. Make settle interruptible:
   - Cancel any running animation on new pointerdown.
   - Start the new drag from the current presented Y, not from the last snap state.

8. Separate target choice from velocity handoff:
   - Measure release velocity in CSS px/s from recent pointer samples.
   - Choose target by the product’s rule: nearest snap point unless momentum targeting is explicitly desired.
   - Feed measured velocity into the settle animation so release continuity is preserved.

9. If momentum targeting is desired:
   - Compute a bounded projected endpoint from current Y + velocity.
   - Clamp to collapsed/half/full range.
   - Snap to nearest valid state from that projected endpoint.

10. Use calmer settle motion:
   - Replace `ease-in` with a spring-like or strong ease-out curve.
   - Avoid bounce by default.
   - Keep most short settles under ~300ms; allow longer only for large travel and only if it remains responsive.

11. Implement Reduced Motion:
   - Keep state change immediate or near-immediate.
   - Preserve feedback with handle color, label/state text, backdrop opacity, subtle border/elevation, or a short fade.
   - Avoid large spatial travel, elastic overshoot, and long transitions.

12. Commit final state:
   - Store `collapsed | half | full`.
   - Set final transform/top explicitly after animation.
   - Clear transient drag/animation objects.

## Verified from the supplied snippet

- The code animates and mutates `top`.
- `pointermove` has no active-drag guard.
- `startY` is unused.
- `animating` blocks pointerdown but not pointermove.
- Settle uses fixed `480ms` and `ease-in`.
- CSS uses `transition: all 300ms`.
- CSS applies active scale to the sheet.
- No reduced-motion branch is shown.
- No pointer capture, cancellation path, velocity sampling, or state commit is shown.

## Unverified boundaries

- Actual snap-point positions and whether nearest-position targeting is the intended product rule.
- Whether other CSS or wrappers compensate for transform ownership.
- Whether surrounding code handles state, cancellation, keyboard control, ARIA, or reduced motion.
- Actual frame rate, touch feel, browser behavior, and device performance.
- Whether the sheet has a dedicated handle or the entire surface is draggable.

## Smallest runtime validation plan

1. **Desktop pointer smoke**
   - Drag from handle and body.
   - Confirm no jump on grab.
   - Confirm no movement without active drag.
   - Drag outside bounds and release.

2. **Interruption check**
   - Release toward half/full.
   - Re-grab mid-settle.
   - Confirm no visual jump and immediate retargeting.

3. **Velocity check**
   - Slow drag and quick flick from same position.
   - Confirm target behavior matches the intended product rule.
   - Confirm settle starts with continuous velocity.

4. **Reduced Motion check**
   - Enable reduced motion.
   - Move between collapsed/half/full.
   - Confirm state feedback remains clear without large travel.

5. **Performance check**
   - Inspect that drag updates use transform, not layout properties.
   - Check for long tasks or visible lag while dragging over realistic app content.


## Output B

## Verdict

**[Code evidence] Not production-ready for a calm repeated-use operations sheet.**  
The implementation visually moves something, but it does not provide reliable direct manipulation, stateful snapping, reduced-motion behavior, or performant motion. It will feel jumpy, sluggish, and fragile under real pointer use.

---

## Prioritized findings

1. **Drag is not actually state-gated**
   - **[Code evidence]** `pointermove` always runs, even if there was no valid `pointerdown`.
   - **Impact:** Mouse hover or stray pointer movement can reposition the sheet.
   - **Fix direction:** Track `isDragging`, `pointerId`, and ignore unrelated moves.

2. **The sheet jumps to the pointer instead of preserving grab offset**
   - **[Code evidence]** `startY` is recorded but never used; `top = event.clientY`.
   - **Impact:** On drag start, the sheet can snap so its top aligns with the finger/cursor, breaking direct manipulation.
   - **Fix direction:** Store `startY` and `startSheetY`; apply `startSheetY + deltaY`.

3. **No pointer capture or cancellation handling**
   - **[Code evidence]** No `setPointerCapture`, `pointercancel`, or `lostpointercapture`.
   - **Impact:** Drag can break if the pointer leaves the sheet, scrolling begins, or the browser cancels the gesture.
   - **Fix direction:** Capture the active pointer and finalize/cancel cleanly.

4. **Uses `top` for every frame**
   - **[Code evidence]** `sheet.style.top` on move; `sheet.offsetTop` on release.
   - **Impact:** Forces layout work and risks jank, especially in a dense operations UI.
   - **Fix direction:** Use `transform: translateY(...)` during drag and snap animation.

5. **Layout read/write pattern is unsafe**
   - **[Code evidence]** Writes `top`, then reads `offsetTop`.
   - **Impact:** Can force synchronous layout at release.
   - **Fix direction:** Keep a JS position model instead of reading layout as the source of truth.

6. **WAAPI `fill: "forwards"` leaves state ambiguous**
   - **[Code evidence]** The animation visually lands, but the durable style/state is not committed.
   - **Impact:** Later `offsetTop`, CSS transitions, or new animations can disagree with the visible position.
   - **Fix direction:** On finish, set the final transform/state explicitly and cancel/cleanup the animation.

7. **Easing is wrong for snapping**
   - **[Code evidence]** `duration: 480`, `easing: "ease-in"`.
   - **Impact:** Ease-in accelerates into the destination, which feels like the sheet is falling into place instead of settling. 480ms is likely too slow for repeated operational use.
   - **Fix direction:** Use responsive easing, often ease-out or spring-like; shorten and scale duration by distance.

8. **No velocity or intent detection**
   - **[Code evidence]** `nearestSnapPoint(sheet.offsetTop)` only uses final position.
   - **Impact:** A fast upward/downward fling may land in the wrong state.
   - **Fix direction:** Include velocity, direction, thresholds, and current state.

9. **No bounds or resistance**
   - **Code evidence]** `top` can be set to any `clientY`.
   - **Impact:** Sheet can overshoot beyond collapsed/full limits.
   - **Fix direction:** Clamp to valid range; optionally add subtle resistance near edges.

10. **CSS conflicts with JS animation**
    - **[Code evidence]** `.sheet { transition: all 300ms; }` plus JS `animate(...)`.
    - **Impact:** Unpredictable double-motion; unrelated property changes animate accidentally.
    - **Fix direction:** Remove `transition: all`; animate only intentional properties.

11. **Active scale undermines direct manipulation**
    - **[Code evidence]** `.sheet:active { transform: scale(0.96); }`.
    - **Impact:** Conflicts with transform-based sheet travel, shrinks content, and can feel like the sheet slips under the pointer.
    - **Fix direction:** Use handle affordance, shadow, border, or subtle background feedback instead.

12. **Reduced Motion is missing**
    - **[Product evidence]** Reduced Motion must preserve state feedback without large spatial travel.
    - **Code evidence]** No media query or runtime reduced-motion branch.
    - **Impact:** Users requesting reduced motion still get large 480ms spatial movement.
    - **Fix direction:** In reduced motion, snap with very short duration or immediate position change plus non-spatial feedback such as handle state, label, shadow, opacity, or haptic-like visual tick.

---

## Concrete direct-manipulation moves

- Track:
  - `isDragging`
  - `activePointerId`
  - `startPointerY`
  - `startSheetY`
  - `currentSheetY`
  - `currentState: "collapsed" | "half" | "full"`
  - recent pointer samples for velocity

- On `pointerdown`:
  - Ignore if already dragging.
  - Cancel/finish any running snap animation safely.
  - Capture the pointer.
  - Store starting pointer and sheet positions.
  - Mark dragging state.

- On `pointermove`:
  - Ignore if not dragging or wrong pointer.
  - Compute `deltaY = event.clientY - startPointerY`.
  - Set `nextY = clampOrResist(startSheetY + deltaY)`.
  - Apply `transform: translateY(nextY)` through a single motion path.

- On `pointerup` / `pointercancel`:
  - Determine target using position + velocity + direction.
  - Snap to collapsed, half, or full.
  - Commit final state after animation.
  - Release pointer capture and clear drag state.

- Motion tuning:
  - Use transform-only travel.
  - Use distance-aware duration, likely shorter than 480ms for nearby snaps.
  - Prefer responsive/ease-out settling over `ease-in`.
  - Avoid scaling the whole sheet while dragging.

- Reduced Motion:
  - Preserve state change.
  - Avoid large animated travel.
  - Use instant or near-instant position update.
  - Add small non-spatial confirmation: handle highlight, state label update, shadow change, or brief opacity/border feedback.

---

## Verified / unverified boundaries

- **Verified from static code:** Pointer movement is not drag-gated; `startY` is unused; `top` is animated; `transition: all` exists; reduced-motion handling is absent.
- **Verified from product context:** The component has collapsed, half, and full states; the app needs calm repeated use; reduced motion must avoid large spatial travel.
- **Not verified:** Actual DOM structure, sheet size, snap-point math, scroll containment, keyboard behavior, screen-reader labeling, real performance, browser behavior, or device touch behavior.
- **Not claimed:** No browser validation, device validation, profiling, or runtime audit was performed.

---

## Smallest runtime validation plan

1. **Pointer correctness**
   - Drag from handle and body.
   - Move pointer outside the sheet.
   - Cancel gesture mid-drag.
   - Confirm only the active pointer controls the sheet.

2. **Snap behavior**
   - Test slow drags between collapsed, half, and full.
   - Test fast upward/downward flings.
   - Confirm final visual state equals internal state.

3. **Motion quality**
   - Inspect for jump on grab.
   - Confirm no double animation from CSS transition + JS animation.
   - Confirm snap feels responsive, not delayed.

4. **Reduced Motion**
   - Enable reduced motion.
   - Confirm large spatial animation is removed or minimized.
   - Confirm state feedback still remains visible.

5. **Performance**
   - Record a drag interaction.
   - Check for layout thrash, long tasks, dropped frames, and avoidable style recalculation.


## Output C

## Verdict

**Static-code verdict: fail for a production gesture sheet.**  
**Evidence:** the snippet uses absolute `top` writes, fixed-duration `ease-in`, `transition: all`, an `animating` input lock, no velocity, no pointer capture, and no reduced-motion branch. For a calm repeated-use operations app, this will feel laggy, jumpy, and hard to trust.

## Prioritized findings

1. **Not truly direct-manipulated**
   - **Evidence:** `sheet.style.top = \`${event.clientY}px\`;`
   - The sheet is tied to viewport pointer Y, not the user’s grab offset or current sheet position.
   - Likely jump on first move if the user grabs anywhere except the sheet’s top edge.

2. **Input is locked during animation**
   - **Evidence:** `if (animating) return;`
   - A moving sheet cannot be grabbed, stopped, or reversed mid-flight.
   - This breaks the core expectation of a gesture surface: the user should remain in control at all times.

3. **Release animation ignores gesture velocity**
   - **Evidence:** `nearestSnapPoint(sheet.offsetTop)` and fixed `duration: 480`
   - A fast flick and a slow drag ending at the same pixel choose the same target.
   - The sheet should project momentum, then snap to collapsed / half / full from the projected endpoint.

4. **Bad easing for handoff**
   - **Evidence:** `easing: "ease-in"`
   - On release, `ease-in` starts slowly, while the user’s finger may be moving quickly.
   - This creates a visible seam: drag → sudden deceleration → delayed travel.

5. **Animating `top` causes layout work**
   - **Evidence:** JS writes `top`; WAAPI animates `top`; CSS transitions `all`.
   - `top` affects layout and can force repeated layout/reflow.
   - Gesture sheets should generally move with `transform: translateY(...)` so motion stays compositor-friendly.

6. **CSS fights the gesture**
   - **Evidence:** `.sheet { transition: all 300ms; }`
   - Every `top` write during drag may be transitioned, so the sheet can lag behind the pointer.
   - `transition: all` also risks animating unrelated properties and creating unpredictable motion.

7. **Presentation and state can diverge**
   - **Evidence:** `fill: "forwards"` without committing final state.
   - The visual position may be held by the animation effect while the app’s logical sheet state remains elsewhere.
   - Future drags, layout reads, resize handling, and state restoration can desynchronize.

8. **No gesture ownership**
   - **Evidence:** no `setPointerCapture`, no `pointerId`, no `pointercancel`, no drag flag.
   - `pointermove` runs even if no valid drag was started.
   - If the pointer leaves the sheet, another pointer enters, or the gesture is cancelled, behavior is undefined.

9. **No boundary behavior**
   - **Evidence:** direct assignment to `event.clientY`.
   - Users can drag beyond collapsed/full bounds with no resistance model.
   - Hard clamps feel frozen; no clamp can expose broken layout.

10. **Reduced Motion is absent**
   - **Evidence:** no `prefers-reduced-motion` branch.
   - Product requirement says reduced motion must preserve feedback without large spatial travel.
   - This implementation always uses large positional travel.

11. **Press scale is too blunt**
   - **Evidence:** `.sheet:active { transform: scale(0.96); }`
   - Scaling the whole sheet during drag can make dense operational content feel unstable.
   - If feedback is needed, apply it subtly to the drag handle or surface elevation, not the entire data panel.

## Concrete direct-manipulation moves

- Track `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, and `grabOffset`.
- Use `sheet.setPointerCapture(event.pointerId)` on `pointerdown`.
- Cancel or retarget any active animation when a new drag begins.
- Move with `transform: translateY(var(--sheet-y))`, not `top`.
- Update position inside `requestAnimationFrame` to avoid excess style writes.
- Keep a short history of `{ y, time }` samples to calculate release velocity.
- On release:
  - compute current Y,
  - compute release velocity,
  - project likely endpoint,
  - choose nearest snap point from the projected endpoint,
  - animate from the live current transform to the target,
  - hand velocity into the settling motion.
- Use distance/velocity-aware spring-like settling rather than fixed `480ms ease-in`.
- Add rubber-band resistance beyond min/max sheet bounds.
- Make collapsed / half / full explicit state, not just pixels.
- Commit final visual position into state and clear completed animation effects.
- Reduced Motion path:
  - avoid long sheet travel where possible,
  - use immediate state placement plus short opacity/elevation/outline feedback,
  - no bounce/overshoot,
  - preserve clear collapsed/half/full state indication.

## Verified boundaries

- **Verified from static code:** layout-affecting `top` animation, input lock, no velocity, no pointer capture, no reduced-motion handling, broad CSS transition, aggressive active scale.
- **Verified from product context:** sheet has collapsed / half / full states and must support reduced motion with non-spatial feedback.

## Unverified boundaries

- No browser validation performed.
- No device/touchpad/stylus validation performed.
- No frame-rate, layout-thrash, or accessibility tooling measurements performed.
- Unknown surrounding HTML semantics, focus management, scroll locking, snap-point definitions, and state persistence.
- Unknown whether other code cancels animations, handles keyboard control, or manages reduced-motion elsewhere.

## Smallest runtime validation plan

1. **Pointer continuity**
   - Drag from handle, body, and edge.
   - Confirm no jump on first move.
   - Confirm sheet stays under the pointer.

2. **Interruptibility**
   - Release toward half/full, then grab mid-animation.
   - Confirm it stops immediately and follows the pointer.

3. **Velocity behavior**
   - Slow-drag near midpoint vs. fast-flick from same area.
   - Confirm flick can advance to the intended snap point.

4. **Bounds**
   - Pull beyond collapsed and full.
   - Confirm rubber-band resistance and clean return.

5. **Reduced Motion**
   - Enable reduced motion.
   - Confirm no large animated travel, no bounce, but state change remains visible.

6. **Performance smoke**
   - Record one drag.
   - Check for layout/recalculate-style spikes and missed frames during pointer movement.
