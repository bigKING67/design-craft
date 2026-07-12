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

[Verified statically] This implementation is not fit for a calm, repeatedly used three-state operations sheet.  
[Evidence] It treats dragging as raw viewport `top` assignment, has no active drag ownership, conflicts CSS transitions with imperative animation, ignores velocity/state intent, and lacks Reduced Motion handling.  
[Impact] It will likely feel jumpy, laggy, and unpredictable rather than direct, stable, and low-fatigue.

---

## Prioritized findings

1. **Drag is not anchored to the user’s grab point**
   - [Evidence] `startY = event.clientY` is stored but never used.
   - [Evidence] `pointermove` sets `sheet.style.top = event.clientY`.
   - [Impact] The sheet can jump so its top edge follows the pointer instead of preserving the initial offset between finger/cursor and sheet.

2. **Pointer moves are accepted without an active drag state**
   - [Evidence] `pointermove` always mutates `top`; `pointerup` always snaps.
   - [Impact] Hover/move noise, stray pointer events, or interrupted gestures can move or snap the sheet without a valid drag session.

3. **No pointer capture or cancellation handling**
   - [Evidence] No `setPointerCapture`, `pointercancel`, or `lostpointercapture`.
   - [Impact] If the pointer leaves the sheet, a gesture is interrupted, or another pointer participates, the component can end in a stale or partially dragged state.

4. **CSS transition fights direct manipulation**
   - [Evidence] `.sheet { transition: all 300ms; }`
   - [Impact] Every `top` update during drag may be eased, causing the sheet to trail the finger instead of tracking it. `transition: all` also risks animating unrelated future style changes.

5. **Animation state can get stuck**
   - [Evidence] `sheet.animate(...).finished.then(() => { animating = false; })`
   - [Impact] If the animation is canceled or rejects, `animating` may never reset. Also, `pointermove` is not blocked while `animating`.

6. **The snap decision ignores velocity and user intent**
   - [Evidence] `nearestSnapPoint(sheet.offsetTop)` only uses position.
   - [Impact] A clear upward or downward fling may snap to the nearest point instead of the intended collapsed/half/full state.

7. **Easing is wrong for a settling sheet**
   - [Evidence] `{ duration: 480, easing: "ease-in" }`
   - [Impact] Ease-in starts slowly after release, making the sheet feel delayed, then ends fast, which can feel abrupt. A calm sheet should settle decisively with ease-out or spring-like deceleration.

8. **Layout properties are animated on the hot path**
   - [Evidence] Drag and snap both animate `top`.
   - [Impact] Updating layout each move can be less smooth than transform-based motion and may cause unnecessary reflow.

9. **Reduced Motion requirement is unmet**
   - [Evidence] No `prefers-reduced-motion` branch.
   - [Requirement] Reduced Motion must preserve state feedback without large spatial travel.
   - [Impact] A 480ms spatial travel animation may violate the product requirement.

10. **The active scale effect is likely counterproductive**
    - [Evidence] `.sheet:active { transform: scale(0.96); }`
    - [Impact] Scaling the whole sheet during drag can make content wobble, reduce readability, and conflict with transform-based sheet motion. It reads as “button press,” not “stable surface under direct manipulation.”

11. **No clamping to valid sheet range**
    - [Evidence] Raw `clientY` is assigned to `top`.
    - [Impact] The sheet can be dragged past collapsed/full bounds unless `nearestSnapPoint` or external CSS happens to constrain it.

12. **State model is implicit**
    - [Evidence] There is no stored `collapsed | half | full` state, no current snap index, no state feedback.
    - [Impact] Harder to keep visual state, accessibility state, analytics, and Reduced Motion behavior consistent.

---

## Concrete direct-manipulation moves

- Use an explicit gesture state:
  - `isDragging`
  - `activePointerId`
  - `startPointerY`
  - `startSheetY`
  - recent samples for velocity

- On `pointerdown`:
  - cancel any running snap animation;
  - capture the pointer;
  - record current sheet position;
  - disable transition during drag;
  - mark dragging only for the initiating pointer.

- On `pointermove`:
  - ignore events unless `isDragging && event.pointerId === activePointerId`;
  - compute `nextY = clamp(startSheetY + event.clientY - startPointerY, fullY, collapsedY)`;
  - apply position with `transform: translate3d(0, var(--sheet-y), 0)` or equivalent transform-based motion;
  - avoid `top` updates on every frame.

- On `pointerup` / `pointercancel`:
  - release capture;
  - calculate velocity;
  - project the resting position slightly in the direction of travel;
  - choose collapsed/half/full using projected position, thresholds, and hysteresis;
  - commit the target state explicitly.

- For snapping:
  - use duration based on distance, capped to a calm range;
  - prefer ease-out / critically damped spring behavior over `ease-in`;
  - set the final style/state after animation, not only `fill: "forwards"`;
  - use `finally` or equivalent so animation cleanup always runs.

- For Reduced Motion:
  - avoid large spatial travel on snap;
  - move immediately or nearly immediately to the target;
  - preserve feedback with a subtle state label, handle highlight, shadow/opacity change, or brief non-spatial emphasis;
  - keep collapsed/half/full state visible and understandable.

- For calm repeated use:
  - remove full-sheet `:active` scaling;
  - if feedback is needed, apply it to the drag handle only;
  - keep motion short, predictable, and non-bouncy;
  - avoid surprise transitions from `transition: all`.

---

## Verified / unverified boundaries

- [Verified statically] The critique is based only on the provided JS and CSS.
- [Verified statically] The code lacks active drag ownership, pointer capture, cancellation handling, velocity-aware snap logic, and Reduced Motion branching.
- [Unverified] Actual DOM structure, snap point math, sheet positioning strategy, scroll containment, and accessibility markup are not provided.
- [Unverified] No browser, device, touch, trackpad, keyboard, or assistive-technology validation has been performed.
- [Unverified] Performance characteristics are inferred from the use of `top` and `transition: all`; no runtime profiling was performed.

---

## Smallest runtime validation plan

1. **Gesture correctness**
   - Drag from different grab points.
   - Confirm the sheet does not jump.
   - Confirm it tracks the pointer directly.

2. **State snapping**
   - Slow-drag to each of collapsed, half, and full.
   - Fling upward/downward from near thresholds.
   - Confirm velocity and intent affect the result.

3. **Interruption handling**
   - Release outside the sheet.
   - Trigger pointer cancellation.
   - Start a new drag during snap animation.
   - Confirm no stuck `animating` state.

4. **Reduced Motion**
   - Enable reduced-motion preference.
   - Move among all three states.
   - Confirm state feedback remains clear without large animated travel.

5. **Scroll and accessibility basics**
   - Test sheet content scrolling versus sheet dragging.
   - Confirm keyboard-accessible state changes and visible focus.
   - Confirm state names are exposed consistently.

Rules applied: quality review and frontend interaction review.


## Output B

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


## Output C

## Verdict

**Static-evidence verdict: not production-ready for a calm repeated-use operations app.**  
The implementation treats the sheet as a timed animation target, not a directly manipulated object. It will likely feel laggy, jumpy, non-interruptible, and inconsistent across collapsed / half / full states. Reduced Motion requirements are currently unmet.

---

## Prioritized findings

1. **[Static evidence] Drag is not 1:1 with the grab point**
   - `startY` is recorded but never used.
   - `sheet.style.top = event.clientY` snaps the sheet’s top edge to the pointer, so grabbing lower on the sheet causes an immediate jump.
   - **Impact:** breaks direct manipulation immediately.

2. **[Static evidence] Pointer state is incomplete**
   - `pointermove` runs without checking whether a drag is active.
   - No `pointerId`, `setPointerCapture`, `pointercancel`, or lost-capture handling.
   - **Impact:** dragging can fail when the pointer leaves the sheet; unrelated pointer movement may mutate position.

3. **[Static evidence] The animation is intentionally non-interruptible**
   - `if (animating) return;` blocks new grabs during motion.
   - **Impact:** users cannot catch, reverse, or correct a moving sheet; this feels especially bad in a repeatedly used tool.

4. **[Static evidence] CSS transition fights the gesture**
   - `.sheet { transition: all 300ms; }` means `top` changes during drag may be eased instead of glued to the pointer.
   - It also risks animating unrelated properties.
   - **Impact:** perceived input latency and unpredictable side effects.

5. **[Static evidence] Uses layout-position animation instead of compositor motion**
   - Animating `top` and reading `offsetTop` can cause layout work.
   - **Impact:** higher risk of jank than `transform: translateY(...)`, especially with rich sheet content.

6. **[Static evidence] Release motion ignores velocity**
   - Snap target is based on `nearestSnapPoint(sheet.offsetTop)` only.
   - No release velocity, projected endpoint, or flick intent.
   - **Impact:** a fast upward flick may still settle to the nearest current point instead of the intended full state.

7. **[Static evidence] Easing is backwards for physical settling**
   - `ease-in` starts slowly and ends quickly.
   - A sheet should usually leave the finger with current velocity and decelerate into rest.
   - **Impact:** release feels detached and may “crash” into the target.

8. **[Static evidence] Reduced Motion is absent**
   - No `prefers-reduced-motion` branch.
   - WAAPI still performs large spatial travel.
   - **Impact:** fails the stated requirement to preserve state feedback without large spatial travel.

9. **[Static evidence] Press scale is too blunt**
   - `.sheet:active { transform: scale(0.96); }` scales the entire sheet.
   - This can conflict with drag transforms and make dense operational content feel unstable.
   - **Impact:** not calm; may distort text and reduce confidence.

10. **[Inference] Snap state model appears underspecified**
   - The code computes a target but does not clearly commit a durable `collapsed | half | full` state.
   - **Impact:** keyboard, accessibility, persistence, analytics, and reduced-motion feedback may drift from visual position.

---

## Concrete direct-manipulation moves

- Track an explicit drag session:
  - `activePointerId`
  - `grabOffsetY`
  - `startSheetY`
  - recent `{ y, time }` samples for velocity
  - active snap state

- On `pointerdown`:
  - allow interruption;
  - cancel or retarget the current animation;
  - read the current presented sheet position;
  - call `setPointerCapture(event.pointerId)`;
  - store `grabOffsetY = event.clientY - currentSheetTop`.

- On `pointermove`:
  - ignore moves from other pointers;
  - only update while dragging;
  - compute `nextY = event.clientY - grabOffsetY`;
  - clamp or rubber-band beyond collapsed/full bounds;
  - update with `transform: translateY(...)`, not `top`;
  - avoid CSS transitions during the drag.

- On `pointerup`:
  - compute release velocity from recent samples;
  - project likely resting position from velocity;
  - choose collapsed / half / full from the projected endpoint, not just current position;
  - animate from the current presented value to the target;
  - pass release velocity into the settling animation where possible.

- Replace fixed `480ms ease-in` with a restrained settling model:
  - default: critically damped or near-critically damped;
  - slight overshoot only for intentional flicks, if appropriate;
  - for a calm operations app, prefer quiet, quick, non-bouncy settling.

- Make the sheet interruptible:
  - a new pointerdown during settle should grab the sheet where it visually is;
  - no global `animating` lock that blocks user correction.

- Separate visual feedback from spatial motion:
  - press feedback should be subtle: handle highlight, shadow/elevation change, or tiny handle compression;
  - avoid scaling the whole sheet during content-heavy operational work.

- Add Reduced Motion behavior:
  - preserve the final collapsed / half / full state;
  - avoid large animated travel after release;
  - use short opacity, shadow, outline, handle, or state-label feedback;
  - if the user physically drags the sheet, keep direct response, but reduce or remove autonomous snap travel.

- Clarify scroll-vs-sheet gesture ownership:
  - likely drag only from a handle/header;
  - let inner content scroll normally;
  - use a small vertical movement threshold before committing to sheet drag.

---

## Verified / unverified boundaries

**Verified from static code only**
- The snippet writes `top` directly during `pointermove`.
- `startY` is unused.
- `pointermove` is not gated by an active drag flag.
- No pointer capture is present.
- Release animation uses fixed duration, `ease-in`, and `top`.
- CSS uses `transition: all`.
- No visible Reduced Motion branch is present.

**Unverified**
- Actual `nearestSnapPoint` behavior.
- Whether the sheet has a dedicated drag handle.
- Whether other CSS overrides `transition`, `top`, or `transform`.
- Real frame rate, input latency, scroll conflict, and device behavior.
- Accessibility semantics, keyboard behavior, focus management, and state announcements.
- User comfort in the real operations workflow.

**Not claimed**
- No browser validation.
- No device validation.
- No performance trace.
- No user testing.

---

## Smallest runtime validation plan

1. **Directness test:** grab the sheet at top, middle, and lower edge; confirm no jump and no trailing lag.
2. **Capture test:** drag outside the sheet bounds; confirm it continues tracking until release.
3. **Interrupt test:** release toward half/full, then grab mid-animation and reverse; confirm no lockout or jump.
4. **Velocity test:** slowly drag vs fast flick from the same position; confirm different intended snap outcomes.
5. **Snap-state test:** verify collapsed / half / full state is committed consistently after every release.
6. **Scroll conflict test:** scroll inner content, then drag the handle; confirm ownership is predictable.
7. **Reduced Motion test:** emulate reduced motion; confirm state feedback remains but large autonomous travel is removed or minimized.
8. **Performance smoke test:** record one drag/release interaction and check for layout thrash, long tasks, and missed frames.
