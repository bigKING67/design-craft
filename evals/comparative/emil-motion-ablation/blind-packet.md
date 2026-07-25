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

## Verdict — **Block for production gesture quality**

**Evidence basis:** static source only. The snippet proves layout-property dragging, non-interruptible settling, no Reduced Motion branch, and no real drag state machine. It cannot prove actual frame rate or device feel, but the implementation is structurally unlikely to feel calm or reliable in a repeated-use operations app.

## Prioritized findings

### P0 — Drag is not actually controlled by an active gesture
**Evidence:** `pointermove` always runs and writes `sheet.style.top`, regardless of whether a pointer is down. `startY` is recorded but never used.  
**Impact:** hovering/moving over the sheet can reposition it; the sheet may jump to the pointer’s viewport Y instead of preserving the grab point.

### P0 — Non-interruptible motion breaks direct manipulation
**Evidence:** `if (animating) return` blocks new drags during settle; the running animation is not cancelled or retargeted from the current visual position.  
**Impact:** operators cannot reverse or correct a sheet mid-flight; repeated use will feel laggy and “owned by the animation,” not by the user.

### P0 — Animates `top`, causing layout work on the hot path
**Evidence:** pointermove writes `style.top`; release reads `offsetTop`; WAAPI animates `top`; CSS also has `transition: all`.  
**Impact:** likely layout/reflow pressure and possible lag, especially in a data-heavy app. Gesture position should be compositor-friendly, typically `transform: translateY(...)`.

### P0 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` branch; release always performs up to `480ms` of spatial travel.  
**Impact:** violates the stated requirement. Reduced Motion should preserve state feedback while avoiding large sheet travel.

### P1 — Timing/easing are wrong for a grabbed sheet
**Evidence:** settle uses `{ duration: 480, easing: "ease-in" }`.  
**Impact:** `ease-in` delays initial response after release; 480ms is heavy for a frequently used operations control. A sheet should settle promptly, usually with spring-like or strong ease-out behavior.

### P1 — Animation state and layout state can diverge
**Evidence:** `fill: "forwards"` keeps the visual animation result but does not necessarily update the underlying authored `top` as the source of truth.  
**Impact:** the next `offsetTop`/drag may start from stale layout state and jump unless final state is explicitly committed.

### P1 — No velocity, projection, hysteresis, or boundaries
**Evidence:** target is `nearestSnapPoint(sheet.offsetTop)` only; no sampled pointer history, velocity units, threshold, clamp, or rubber-band logic.  
**Impact:** a quick flick and a slow drag ending at the same point behave identically; accidental taps may become drags; overdrag behavior is undefined.

### P1 — CSS transform ownership conflict
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** if the sheet is moved with `transform`, press scale will overwrite or fight translate unless separated into wrapper layers. Scaling the entire sheet while dragging may also make dense operations UI feel unstable.

### P2 — Missing pointer robustness
**Evidence:** no `setPointerCapture`, `pointerId`, `pointercancel`, `lostpointercapture`, or multi-touch guard.  
**Impact:** dragging outside the sheet, OS interruption, or additional touches can leave the sheet in an inconsistent state.

## Concrete direct-manipulation moves

1. **Introduce a real gesture state machine**  
   Track `idle | dragging | settling`, `activePointerId`, `startY`, `startSheetY`, and `grabOffset`. Ignore unrelated pointers.

2. **Use pointer capture and cancellation paths**  
   On committed drag: `setPointerCapture(event.pointerId)`. Handle `pointercancel` and `lostpointercapture` by settling or restoring safely.

3. **Preserve the grab offset**  
   Compute movement from `startSheetY + (event.clientY - startY)`, not `top = event.clientY`.

4. **Move with transforms, not layout**  
   Drive a single position owner such as `translateY(var(--sheet-y))`. Avoid `top` animation and remove `transition: all`.

5. **Batch drag writes with `requestAnimationFrame`**  
   Store the latest pointer Y, then update transform once per frame. Keep layout reads out of `pointermove`.

6. **Make settling interruptible**  
   On pointerdown during settle, cancel the current animation, read the current presented Y, and continue from that exact value without a jump.

7. **Separate target selection from velocity handoff**  
   Measure release velocity in CSS px/s from recent samples.  
   - If product semantics are “nearest current snap,” keep `nearestSnapPoint(currentY)`.  
   - If momentum is authorized, choose from a bounded projected endpoint.  
   Either way, feed measured velocity into the settle animation when the API supports it.

8. **Use bounded snap geometry**  
   Define explicit collapsed/half/full Y values, clamp within safe bounds, update on viewport/container resize, and apply soft resistance beyond edges.

9. **Replace global active scale**  
   Put position transform on the outer sheet and optional press feedback on an inner handle/control layer. Keep scale subtle and disable it while dragging if it destabilizes content.

10. **Add Reduced Motion behavior**  
   Under `prefers-reduced-motion: reduce`, avoid large animated travel: snap state immediately or with a very short transition, and preserve feedback through handle state, opacity, elevation, label, or focus-visible changes.

11. **Expose state accessibly**  
   Maintain a source-of-truth state: `collapsed | half | full`; provide keyboard controls and visible/focusable affordances for changing state.

## Verified / unverified boundaries

**Verified from snippet**
- `pointermove` is ungated.
- `startY` is unused.
- `top` is written and animated.
- `offsetTop` is read during release.
- `ease-in` and `480ms` are used.
- `transition: all 300ms` is present.
- Reduced Motion is absent in supplied CSS/JS.
- Pointer capture/cancel handling is absent in supplied JS.

**Not verified**
- Actual frame rate, dropped frames, or perceived smoothness.
- Whether surrounding code adds bounds, keyboard support, ARIA, focus management, or Reduced Motion elsewhere.
- Whether `nearestSnapPoint` encodes product-approved threshold logic.
- Real touch behavior on trackpad, mouse, stylus, or mobile hardware.

## Smallest runtime validation plan

1. **Gesture continuity:** drag from collapsed → half → reverse mid-settle; confirm no jump and no input lockout.  
2. **Pointer robustness:** drag outside sheet bounds, cancel pointer, add second touch; confirm state recovers.  
3. **Performance trace:** record drag with table/data load present; confirm transform-only updates and no repeated layout in the move loop.  
4. **Velocity behavior:** compare slow drag vs quick flick with same release point; confirm intended snap semantics.  
5. **Reduced Motion:** emulate reduced motion; confirm no large spatial travel while state feedback remains clear.  
6. **Keyboard/accessibility pass:** operate collapsed/half/full without pointer; confirm focus visibility and announced/current state.


## Output B

## Verdict — static evidence only

**Not production-ready for a calm repeated-use operations sheet.**  
The implementation breaks direct manipulation, uses layout-bound motion, conflicts CSS transitions with JS animation, lacks reduced-motion behavior, and has incomplete pointer lifecycle handling. It will likely feel laggy, jumpy, and hard to trust during repeated operator use.

---

## Prioritized findings

### P0 — Drag is not actually anchored to the gesture
**Evidence:** `startY = event.clientY;` is stored but never used; `pointermove` sets `sheet.style.top = event.clientY`.

**Impact:** The sheet will jump so its top tracks the pointer’s viewport Y, not the user’s drag delta. A pointerdown at the handle midpoint can cause an immediate discontinuity.

**Fix direction:** Track `startY`, `startOffset`, and apply `next = startOffset + (event.clientY - startY)`.

---

### P0 — Motion uses `top`, causing layout work during drag and animation
**Evidence:** `sheet.style.top`, `sheet.offsetTop`, and `animate([{ top }, { top }])`.

**Impact:** `top` updates can trigger layout/paint. `offsetTop` reads after writes can force synchronous layout. This is risky for a 10,000-row operations surface and harms drag latency.

**Fix direction:** Use `transform: translateY(...)` as the single motion primitive. Keep logical sheet state separately from visual transform.

---

### P0 — CSS transition conflicts with gesture movement
**Evidence:** `.sheet { transition: all 300ms; }`.

**Impact:** Every drag update to `top`, `transform`, color, size, etc. may transition. During pointermove this can add 300ms lag and make the sheet chase the finger instead of following it.

**Fix direction:** Never use `transition: all` on an interactive sheet. Disable transitions during drag; apply a specific transform transition only during snap settle.

---

### P1 — Snap animation is too slow and uses the wrong easing
**Evidence:** `{ duration: 480, easing: "ease-in" }`.

**Impact:** `ease-in` starts slowly and accelerates away from the user’s release point, which feels unresponsive. 480ms is long for repeated operational use.

**Fix direction:** Use a responsive settle curve, typically faster and decelerating: e.g. `180–260ms` with an ease-out or custom responsive cubic-bezier. Let distance/velocity influence duration within a bounded range.

---

### P1 — Reduced Motion requirement is unmet
**Evidence:** No `prefers-reduced-motion` handling; product requires “Reduced Motion must preserve state feedback without large spatial travel.”

**Impact:** The sheet will still perform large spatial travel between collapsed, half, and full states.

**Fix direction:** In reduced motion, avoid animated travel. Snap nearly immediately, use short opacity/border/elevation/handle-state feedback, and preserve clear state labels.

---

### P1 — Pointer lifecycle is incomplete
**Evidence:** No `setPointerCapture`, no active pointer tracking, no `pointercancel`, no lost-capture handling, no guard in `pointermove`.

**Impact:** Drag can continue from unrelated pointer moves, get stuck if the pointer leaves the sheet, or fail on touch cancellation. Multi-touch/pen/mouse interactions are not controlled.

**Fix direction:** Track `dragging`, `pointerId`, call `setPointerCapture`, ignore other pointers, and end cleanly on `pointerup`, `pointercancel`, and `lostpointercapture`.

---

### P1 — Animation state can desynchronize
**Evidence:** `animating = true`; `.finished.then(...)`; `fill: "forwards"`; final style is not explicitly committed.

**Impact:** If the animation is interrupted/canceled, `animating` may stay wrong unless handled. `fill: forwards` can leave visual state in animation output while layout/style state remains stale.

**Fix direction:** Cancel prior animations, commit final transform/style explicitly, handle rejection/finally, and store canonical state: `collapsed | half | full`.

---

### P2 — Active scale is hostile for a bottom sheet
**Evidence:** `.sheet:active { transform: scale(0.96); }`.

**Impact:** This changes the whole sheet’s size while the user is trying to drag it, distorting spatial mapping and potentially fighting the translation transform.

**Fix direction:** Put press feedback on the handle, not the entire panel. Use subtle handle color/elevation/state feedback instead of panel scale.

---

### P2 — Snap decision lacks velocity, bounds, and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only.

**Impact:** A fast intentional fling and a slow small drag to the same position resolve identically. No visible clamping means the sheet may overshoot invalid ranges during drag.

**Fix direction:** Use position + release velocity + thresholds. Clamp movement between full and collapsed bounds. Bias toward the next state when velocity exceeds a small threshold.

---

## Concrete direct-manipulation moves

1. **Model sheet state explicitly**
   - `state = "collapsed" | "half" | "full"`
   - `snapPoints = { collapsed, half, full }`
   - `currentY` is visual position; `state` is semantic position.

2. **Use transform-only movement**
   - During drag: `sheet.style.transform = translate3d(0, ${y}px, 0)`
   - Avoid `top`, `offsetTop`, and `transition: all`.

3. **Anchor drag to initial offset**
   - On pointerdown:
     - save `startPointerY`
     - save `startSheetY`
     - capture pointer
   - On pointermove:
     - `delta = event.clientY - startPointerY`
     - `nextY = clamp(startSheetY + delta, fullY, collapsedY)`

4. **Separate drag and settle modes**
   - Dragging: no transition, direct rAF-batched transform updates.
   - Settling: one transform animation to the chosen snap point.

5. **Choose target using position + velocity**
   - Low velocity: nearest snap.
   - Upward velocity: bias toward fuller state.
   - Downward velocity: bias toward more collapsed state.
   - Still respect bounds and disabled states.

6. **Reduced Motion behavior**
   - No long sheet travel animation.
   - Snap position quickly, e.g. `0–80ms`.
   - Preserve feedback with handle state, selected snap indicator, subtle elevation/border change, and accessible state announcement.

7. **Replace whole-panel active scale**
   - Remove `.sheet:active { transform: scale(...) }`.
   - Use handle-only pressed affordance:
     - small color/elevation change
     - cursor/grab state
     - visible focus ring for keyboard users

8. **Make interruption safe**
   - If user grabs while settling, cancel animation and continue from current visual transform.
   - Always finalize canonical transform and semantic state.

---

## Verified / unverified boundaries

**Verified from static snippet:**
- Uses `top` for drag and animation.
- Reads `offsetTop` for snap decision.
- Has unused `startY`.
- Uses `transition: all 300ms`.
- Uses whole-sheet `:active` scale.
- Has no visible reduced-motion branch.
- Has no visible pointer capture/cancel handling.

**Not verified:**
- Actual DOM structure, handle target, snap-point math, surrounding scroll containers, browser behavior, frame rate, device feel, accessibility tree, or production CSS cascade.
- No browser, device, or runtime validation was performed.

---

## Smallest runtime validation plan

1. **Pointer lifecycle check**
   - Mouse, touch, and pen if available.
   - Verify pointer capture, cancellation, leaving viewport, and multi-touch rejection.

2. **Direct manipulation check**
   - Sheet must not jump on initial drag.
   - Finger/cursor-to-sheet offset must remain stable.

3. **Performance check**
   - Record a drag and snap.
   - Confirm transform-only updates, no repeated forced layout, no `top` animation, no transition lag.

4. **Snap intent check**
   - Slow drag near boundaries.
   - Fast upward/downward release.
   - Confirm expected collapsed/half/full outcomes.

5. **Reduced Motion check**
   - Enable reduced motion.
   - Confirm no large animated travel; state feedback remains clear.

6. **Interruption check**
   - Start snap animation, grab mid-settle, reverse direction.
   - Confirm no stuck `animating` state or visual/logical desync.


## Output C

## Verdict — not production-ready for a calm repeated-use operations sheet

**Evidence:** the implementation moves `top` on every `pointermove`, blocks input while animating, snaps only from `offsetTop`, uses fixed `480ms ease-in`, has `transition: all`, and has no reduced-motion branch.  
**Impact:** it will feel laggy, jumpy, non-interruptible, and tiring during repeated daily use; it also risks layout work on every frame.

---

## Prioritized findings

### P0 — Direct manipulation is broken
**Evidence:** `sheet.style.top = \`${event.clientY}px\`;`  
- The sheet jumps to the pointer’s absolute Y instead of preserving the grab offset.
- `startY` is recorded but never used.
- `pointermove` runs even when no drag is active.
- No `setPointerCapture`, so dragging can break if the pointer leaves the sheet.

**Fix direction:** track `dragStartY`, `sheetStartY`, `grabOffset`, active `pointerId`, and only update while dragging.

---

### P0 — The sheet is not interruptible
**Evidence:** `if (animating) return;`  
- Users cannot grab a settling sheet mid-flight.
- This creates a dead period after release, especially bad in a high-frequency operations surface.
- `.finished.then(...)` has no cancel/error path, so state can become stale if animation is interrupted later.

**Fix direction:** allow pointerdown during animation, cancel or retarget from the current presented position, and carry current velocity into the next settle.

---

### P0 — Uses layout properties for motion
**Evidence:** animates and mutates `top`; reads `sheet.offsetTop`.  
- `top` animation can trigger layout and paint.
- `offsetTop` reads layout state and can force synchronization.
- For a 10,000-row operations app, this competes with table/editor work.

**Fix direction:** use `transform: translateY(...)` as the sole moving value; keep snap state in JS; read layout only at gesture start or resize.

---

### P0 — Snap target ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)`  
- A fast upward flick near the collapsed point may incorrectly return to collapsed.
- A slow drag past a threshold and a decisive flick are treated the same.
- Collapsed / half / full sheets need projected landing, not nearest current position only.

**Fix direction:** compute release velocity from recent pointer samples, project the likely resting point, then choose collapsed/half/full from that projection.

---

### P1 — Easing and duration fight the physical model
**Evidence:** `{ duration: 480, easing: "ease-in" }`  
- `ease-in` starts slowly after the user releases, creating a visible seam.
- It accelerates toward the end, then abruptly stops at the snap point.
- `480ms` is heavy for repeated operational use.

**Fix direction:** use a velocity-aware spring or a short responsive curve. Default should feel quick, calm, and interruptible; reserve bounce only for strong flicks.

---

### P1 — CSS conflicts with gesture animation
**Evidence:** `.sheet { transition: all 300ms; }` and WAAPI also animates `top`.  
- `transition: all` can accidentally animate unrelated properties.
- It may fight explicit JS/WAAPI motion.
- It makes future state changes unpredictable.

**Fix direction:** never use `transition: all` on a gesture surface. Scope transitions to non-positional feedback like `box-shadow`, `background`, or `opacity`.

---

### P1 — Press feedback is too blunt
**Evidence:** `.sheet:active { transform: scale(0.96); }`  
- Scaling the entire sheet while dragging changes the coordinate relationship under the pointer.
- It can make dense table/editor content blur or pulse.
- It conflicts with using `transform` for sheet translation unless transforms are composed carefully.

**Fix direction:** apply pressed feedback to the drag handle or header only: subtle opacity, elevation, handle color, or 1–2px compression, not whole-sheet scaling.

---

### P1 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` handling.  
- The product requires preserving state feedback without large spatial travel.
- Current behavior always performs large vertical travel.

**Fix direction:** in reduced motion, avoid long sheet travel when programmatically changing states; use instant/very short position change plus opacity, border, header label, shadow, or snap-state affordance.

---

### P2 — Missing gesture safety details
**Evidence:** no drag threshold, no axis lock, no bounds, no rubber-banding.  
- Accidental drags can happen during scroll or text interaction.
- Dragging beyond full/collapsed has no controlled resistance.
- No `touch-action` strategy is shown.

**Fix direction:** add small hysteresis, vertical-axis commitment, min/max bounds, and progressive resistance at edges.

---

### P2 — Accessibility/state affordance is incomplete
**Evidence:** pointer-only state transitions.  
- Keyboard users need explicit controls to move collapsed / half / full.
- Assistive tech needs state naming and focus-safe behavior.
- Reduced-motion users still need confirmation that the state changed.

**Fix direction:** expose buttons/shortcuts for each state, announce state changes when meaningful, keep focus stable, and ensure the handle has a clear accessible name.

---

## Concrete direct-manipulation moves

1. **Use a state machine**
   - `idle → dragging → settling`
   - Allow `settling → dragging` interruption.
   - Track current snap state separately from current visual position.

2. **Capture and preserve grab offset**
   - On `pointerdown`: store `pointerId`, `startClientY`, `startTranslateY`, and recent samples.
   - Call `setPointerCapture(event.pointerId)`.
   - Do not move until a small vertical threshold is crossed.

3. **Move with transform only**
   - Use `translateY(currentY)` during drag.
   - Avoid `top`, `offsetTop`, and `transition: all` in the motion path.

4. **Sample velocity**
   - Keep the last few `{ y, time }` samples.
   - On release, compute px/s velocity.
   - Use both projected position and velocity sign to choose collapsed / half / full.

5. **Settle from the live value**
   - Start animation from the current presented `translateY`, not from stale state.
   - If the user grabs during settle, cancel/retarget without a jump.

6. **Use calm snap physics**
   - Normal drag release: critically damped or near-critically damped settle.
   - Strong flick: slight momentum, minimal overshoot if any.
   - Avoid long fixed durations; prioritize perceived responsiveness.

7. **Add boundary resistance**
   - Within bounds: 1:1 tracking.
   - Beyond collapsed/full: progressive rubber-band resistance.
   - On release: settle back cleanly.

8. **Reduced Motion behavior**
   - Keep snap state changes clear, but avoid large animated travel.
   - Use near-instant position update plus short opacity/shadow/header-state feedback.
   - Disable bounce, projection exaggeration, and long spatial interpolation.

---

## Verified / unverified boundaries

**Verified from static code:**
- Uses `top` for drag and animation.
- Uses `offsetTop` for snap decision.
- Blocks pointerdown while `animating`.
- Uses fixed `480ms ease-in`.
- Uses global `transition: all 300ms`.
- Uses whole-sheet `:active` scale.
- No visible reduced-motion branch in the provided snippet.

**Not verified here:**
- Actual browser frame rate.
- Device touch behavior.
- Real snap-point values.
- Interaction with page scroll.
- Accessibility tree, focus behavior, or keyboard support.
- Whether other code wraps/cancels these animations.

---

## Smallest runtime validation plan

1. **Pointer continuity**
   - Drag from handle, body, and edge.
   - Confirm no initial jump and no lost tracking when leaving the sheet bounds.

2. **Interruptibility**
   - Release toward half/full, then grab mid-settle.
   - Confirm the sheet follows immediately from its visible position.

3. **Snap intent**
   - Test slow drag, short flick, fast upward flick, fast downward flick.
   - Confirm projected target matches user intent.

4. **Performance**
   - Record one drag over a populated table.
   - Check for layout/recalculate-style work during pointer movement.
   - Target compositor-only transform updates.

5. **Reduced Motion**
   - Enable reduced motion.
   - Change collapsed / half / full states.
   - Confirm state feedback remains clear without large animated travel.

6. **Keyboard/accessibility**
   - Move between states without pointer input.
   - Confirm focus remains predictable and state changes are perceivable.
