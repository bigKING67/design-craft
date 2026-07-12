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

**BLOCK — [Static evidence + product-fit risk]**  
This is not a shippable gesture sheet for a calm, repeatedly used operations app. The implementation breaks direct manipulation, animates layout properties, prevents interruption, ignores release velocity, and has no Reduced Motion path. Smoothness and device feel are **unverified** because this is a static review only.

## Prioritized findings

1. **P0 — Drag is not actually stateful direct manipulation.**  
   **[Static evidence]** `pointermove` always writes `sheet.style.top = event.clientY`, with no `dragging` flag, pointer id, threshold, or pointer capture. The sheet can move on hover/stray pointer movement and can lose tracking outside its bounds.

2. **P0 — The sheet will jump under the pointer.**  
   **[Static evidence]** `top = event.clientY` ignores the original sheet position and grab offset. `startY` is recorded but unused. A grabbed sheet should preserve where the user touched it and move by delta, not snap its top edge to the pointer.

3. **P0 — Reduced Motion requirement is unmet.**  
   **[Static evidence]** WAAPI always performs a `480ms` spatial travel animation; CSS also transitions broadly.  
   **[Product risk]** Reduced Motion should preserve collapsed/half/full feedback without large travel, e.g. instant state placement plus subtle handle/color/label feedback.

4. **P0 — Animating `top` is the wrong motion primitive.**  
   **[Static evidence]** pointer move and WAAPI both animate `top`; `offsetTop` is read during release.  
   **[Runtime risk]** This can trigger layout work and jank, especially in an operations app with dense content. Use compositor-friendly `transform: translateY(...)` for the moving layer.

5. **P0 — Interruption is blocked and also inconsistently guarded.**  
   **[Static evidence]** `pointerdown` returns while `animating`, but `pointermove` still updates `top`. There is no animation handle, cancel, retarget, or “start from current presentation value.”  
   **User impact]** If the user changes their mind mid-settle, the sheet should be immediately grabbable without a visual jump.

6. **P1 — Snap choice ignores velocity and intent.**  
   **[Static evidence]** `nearestSnapPoint(sheet.offsetTop)` only uses release position.  
   **Product risk]** A quick flick toward full/collapsed may snap back incorrectly. Sheet snap should use measured release velocity and a projected endpoint, with hysteresis around collapsed/half/full boundaries.

7. **P1 — Timing/easing feel mismatched to the product.**  
   **[Static evidence]** settle uses `480ms` and `ease-in`.  
   **Product fit]** For a repeated calm ops workflow, this is too delayed/cinematic. `ease-in` makes the beginning feel sluggish; settling should respond immediately and finish calmly.

8. **P1 — CSS creates conflicting and excessive motion.**  
   **[Static evidence]** `.sheet { transition: all 300ms; }` can animate unintended properties, including `top` and `transform`. `:active { transform: scale(0.96); }` scales the whole sheet during manipulation.  
   **Runtime risk]** Drag may feel rubbery rather than attached; press scale can fight future transform-based translation unless separated into layers.

9. **P2 — Animation lifecycle is fragile.**  
   **[Static evidence]** `fill: "forwards"` leaves an active animation effect without committing/canceling final styles. There is no cleanup on cancel, pointercancel, lost capture, route change, or rejected `finished` promise.

10. **P2 — Accessibility/state feedback is underspecified.**  
   **[Static evidence]** No keyboard equivalent, announced state, focus handling, or non-motion state feedback is shown.  
   **Product risk]** Collapsed/half/full state should be perceivable without relying on drag animation alone.

## Concrete direct-manipulation moves

1. **Use explicit sheet state.**  
   Model `collapsed | half | full` as snap states with measured pixel positions derived from viewport/container geometry.

2. **Move with transforms, not layout.**  
   Keep layout stable; apply `transform: translateY(var(--sheet-y))` to the motion layer. Avoid animating `top`.

3. **Separate transform ownership.**  
   Use nested wrappers if needed: outer wrapper owns `translateY`, inner wrapper owns subtle press/handle feedback. Do not let drag translation and active scale overwrite each other.

4. **Implement real drag state.**  
   On pointer down: cancel current settle animation, read current visual position, store pointer id, capture pointer, preserve grab offset, and start recording recent positions/timestamps.

5. **Track 1:1 after intent threshold.**  
   Use an 8–12px-ish threshold to distinguish tap/scroll from sheet drag. During drag, update from delta, not absolute `clientY`. Clamp or rubber-band beyond collapsed/full bounds.

6. **Settle from velocity, not just distance.**  
   On release, compute velocity in CSS px/s from recent samples, project the endpoint, choose the nearest intended snap point, then settle with a spring-like curve or critically damped easing. Default to no bounce for this product.

7. **Make interruption first-class.**  
   A new pointerdown during settle should stop/retarget from the current on-screen position, not the old logical target, and should not lock input.

8. **Replace broad CSS motion.**  
   Change `transition: all` to targeted transitions only for non-drag states, e.g. handle color/opacity. Disable transitions during active drag.

9. **Design Reduced Motion separately.**  
   When reduced motion is active: snap state immediately or with a very short non-spatial fade/handle highlight; avoid long travel, elastic overshoot, and large scale changes. Preserve clear collapsed/half/full feedback via label, handle state, shadow/material, or affordance change.

10. **Add cancellation and alternate input paths.**  
   Handle `pointercancel`, `lostpointercapture`, blur/visibility changes, multi-touch rejection, keyboard controls, and visible focus states.

## Verified / unverified boundaries

**Verified by static code review only:**

- Uses `top` for drag and settle animation.
- Uses `transition: all 300ms`.
- Uses `ease-in` and `480ms`.
- Does not show pointer capture, drag gating, velocity tracking, projected snap selection, interruption handling, or Reduced Motion branching.
- `startY` is unused in the shown implementation.

**Not verified:**

- Actual frame rate, smoothness, layout cost, or input latency.
- Browser-specific interaction between CSS `transition: all`, WAAPI `top`, and `fill: forwards`.
- Touch-device feel, scroll conflict, overscroll behavior, or lost pointer behavior.
- Exact snap positions and whether `nearestSnapPoint` handles viewport changes.
- Accessibility tree, keyboard behavior, focus order, or screen reader announcements.

No browser or device validation was performed.

## Smallest runtime validation plan

1. **Instrument one test page/state.**  
   Log current sheet position, active snap state, release velocity, projected endpoint, animation state, and pointer-capture status.

2. **Run five interaction checks.**  
   - Drag from each snap state: no jump on grab.  
   - Move outside sheet bounds: pointer remains captured.  
   - Slow release near midpoint: snaps predictably.  
   - Fast flick toward next state: velocity changes target.  
   - Grab during settle: no lockout and no visual jump.

3. **Run one Reduced Motion check.**  
   Enable reduced motion and verify collapsed/half/full feedback remains clear without large travel.

4. **Run one performance check.**  
   Record a short interaction trace and confirm drag/settle updates are transform/opacity-driven, with no repeated layout animation on `top`.

5. **Escalate only if needed.**  
   If browser results are ambiguous or touch feel matters for release, validate the same five checks on a real touch device before shipping.


## Output B

## Evidence-labeled verdict

**[Verified from snippet] Verdict: Not production-ready for a calm, repeated-use operations app.**  
The implementation will likely feel jumpy, laggy, and hard to trust because it treats the sheet as an absolute `top` value, lacks a real drag state model, conflicts CSS transitions with JS animation, ignores velocity/state intent, and has no Reduced Motion behavior.

---

## Prioritized findings

1. **[Verified] Drag jumps instead of preserving grab position**
   - `startY` is recorded but never used.
   - `pointermove` sets `sheet.style.top = event.clientY`, so the sheet top snaps to the finger/cursor Y, not to the original sheet position plus drag delta.

2. **[Verified] Pointer lifecycle is incomplete**
   - `pointermove` runs even if no valid drag started.
   - No `isDragging`, `pointerId`, `setPointerCapture`, `pointercancel`, or lost-capture handling.
   - During `animating`, `pointerdown` returns, but `pointermove` can still mutate `top`.

3. **[Verified] `top` animation causes layout work and poorer motion**
   - Updating `top` on every move can trigger layout/reflow.
   - A bottom sheet should usually move with `transform: translateY(...)` for direct manipulation.

4. **[Verified] CSS conflicts with JS motion**
   - `.sheet { transition: all 300ms; }` means every `top` write may transition, making the drag lag behind the pointer.
   - `transition: all` also risks animating unrelated properties.
   - WAAPI animation of `top` plus CSS transition on all properties creates competing motion systems.

5. **[Verified] Release motion has the wrong feel**
   - `ease-in` starts slow and ends fast; sheets usually need deceleration into rest.
   - `480ms` is likely too long for a repeatedly used operations surface.
   - No distance-based duration, no velocity-based snap, no interruption model.

6. **[Verified] Snap decision lacks user intent**
   - `nearestSnapPoint(sheet.offsetTop)` ignores drag velocity, direction, thresholds, and hysteresis.
   - A quick upward fling should be able to advance toward full even if nearest point is half.

7. **[Verified] State is not committed cleanly**
   - `fill: "forwards"` visually holds the animation, but the durable state/style may not be synchronized.
   - The next `offsetTop` read may not represent the intended snap state reliably across all conditions.

8. **[Verified] Reduced Motion requirement is unmet**
   - There is no `prefers-reduced-motion` branch.
   - Large spatial travel is always animated over 480ms.
   - State feedback is only spatial motion plus `:active` scale.

9. **[Verified] `:active { transform: scale(0.96); }` is risky**
   - Scaling the sheet during drag can make the contact point feel unstable.
   - It conflicts conceptually with transform-based sheet movement.
   - It is not a clear collapsed/half/full state cue.

10. **[Inferred] Missing bounds will allow unnatural positions**
   - No clamp to collapsed/full limits is shown.
   - Users may drag beyond valid snap points unless constrained elsewhere.

---

## Concrete direct-manipulation moves

- Use a real gesture model:
  - `isDragging`
  - `activePointerId`
  - `grabOffsetY`
  - `currentY`
  - `currentState: "collapsed" | "half" | "full"`
  - `activeAnimation`

- On `pointerdown`:
  - Cancel any running settle animation.
  - Capture the pointer.
  - Measure current sheet position.
  - Store the pointer-to-sheet offset so the sheet does not jump.

- On `pointermove`:
  - Ignore non-active pointers.
  - Compute `nextY = event.clientY - grabOffsetY`.
  - Clamp or apply resistance beyond full/collapsed bounds.
  - Move with `transform: translateY(...)`, not `top`.

- On `pointerup` / `pointercancel`:
  - Release capture.
  - Calculate recent velocity.
  - Choose snap using position + velocity + direction + hysteresis.
  - Animate to target with an ease-out or critically damped spring-like curve.
  - Commit the final state after animation.

- Replace CSS:
  - Remove `transition: all`.
  - Avoid `:active` scale for the whole sheet.
  - Use specific transitions only for non-positional feedback, e.g. handle color, shadow, backdrop opacity.
  - Add temporary `will-change: transform` only while dragging/settling.

- Reduced Motion behavior:
  - Preserve direct state feedback without large travel.
  - Snap immediately or with a very short low-distance transition.
  - Use non-spatial feedback: handle highlight, state label, elevation/backdrop change, or subtle opacity change.
  - Keep collapsed/half/full state clearly perceivable.

---

## Verified / unverified boundaries

**Verified from static code only**
- Drag uses `top`.
- `startY` is unused.
- `pointermove` is not guarded by drag state.
- CSS has `transition: all`.
- Release animation uses `ease-in`, `480ms`, `fill: "forwards"`.
- No visible Reduced Motion handling.

**Unverified**
- Actual `nearestSnapPoint` behavior.
- Existing CSS positioning, viewport constraints, and snap coordinates.
- Whether other code handles accessibility, keyboard control, focus, or ARIA state.
- Real frame rate, browser behavior, and touch-device behavior.
- No browser or device validation has been performed here.

---

## Smallest runtime validation plan

1. **Gesture correctness**
   - Drag from collapsed, half, and full.
   - Confirm no jump on initial contact.
   - Confirm movement stays under the pointer/finger.
   - Confirm bounds and resistance feel intentional.

2. **Snap correctness**
   - Slow release near each threshold.
   - Fast upward and downward flicks.
   - Confirm velocity can override nearest-position snap where appropriate.

3. **Interruption correctness**
   - Start a drag during settle animation.
   - Cancel pointer mid-drag.
   - Leave/re-enter bounds while dragging.
   - Confirm no stuck `animating` state.

4. **Reduced Motion check**
   - Enable reduced motion.
   - Confirm state changes remain clear.
   - Confirm there is no large animated spatial travel.

5. **Performance smoke check**
   - During continuous drag, confirm movement is transform-driven and visually tracks input without delayed CSS transition behavior.


## Output C

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
