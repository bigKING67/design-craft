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

## Verdict

**Evidence-labeled verdict:** **Not production-ready for a calm repeated-use operations app.**  
The implementation has the right basic intent—drag to snap—but the motion model is not direct, stable, or state-aware enough for collapsed / half / full sheet behavior, and Reduced Motion is not addressed.

---

## Prioritized findings

1. **[Code evidence] Drag is not gated by active pointer state**
   - `pointermove` always runs, even if no valid `pointerdown` occurred.
   - If `animating` blocks `pointerdown`, `pointermove` can still move the sheet.
   - Risk: accidental jumps from hover/move events or ignored-down states.

2. **[Code evidence] Movement is absolute, not relative**
   - `sheet.style.top = event.clientY`.
   - This makes the sheet’s top jump to the pointer position instead of preserving the grab offset.
   - `startY` is recorded but never used.
   - Direct manipulation should keep the sheet “attached” to the finger/cursor from the original grab point.

3. **[Code evidence] No pointer capture or cancellation handling**
   - Missing `setPointerCapture`, `pointercancel`, and lost-capture recovery.
   - Risk: sheet can get stuck or release incorrectly if the pointer leaves the element, the OS cancels input, or scrolling interrupts the gesture.

4. **[Code evidence] Layout property animation**
   - Animating `top` causes layout work and can interact poorly with CSS transitions.
   - For a frequently used sheet, `transform: translateY(...)` is the safer motion primitive.

5. **[Code evidence] CSS transition conflicts with imperative animation**
   - `.sheet { transition: all 300ms; }` can animate unrelated properties and may fight direct drag updates.
   - `transition: all` is too broad for a gesture surface.
   - During drag, the sheet should track immediately, not transition behind the pointer.

6. **[Code evidence] Animation completion state is fragile**
   - `fill: "forwards"` leaves the visual result in animation state rather than committing the final inline position.
   - `sheet.offsetTop` may not reliably represent the visual animated end state afterward.
   - Risk: later snap calculations can use stale or inconsistent geometry.

7. **[Code evidence] Fixed `480ms ease-in` is a poor snap profile**
   - `ease-in` starts slow and ends fast, which can feel like the sheet accelerates into the stop.
   - For a calm operations app, snapping should usually decelerate into rest.
   - Fixed duration ignores travel distance; a small snap and long snap should not both take 480ms.

8. **[Product evidence] No collapsed / half / full state model**
   - The snippet snaps to a target but does not store or expose the resulting sheet state.
   - Missing state feedback affects keyboard users, screen reader users, persistence, and Reduced Motion feedback.

9. **[Product evidence] Reduced Motion requirement is unmet**
   - There is no `prefers-reduced-motion` path.
   - Requirement says state feedback must remain without large spatial travel.
   - Current behavior always performs spatial travel to the target.

10. **[UX evidence] `:active { transform: scale(0.96); }` is risky**
   - Scaling the entire sheet while dragging changes perceived geometry.
   - It can make dense operational content feel unstable.
   - It also competes with transform-based movement if transform is later used for sheet position.

11. **[Interaction evidence] No velocity or intent handling**
   - Snap target appears based only on current offset.
   - A sheet should usually consider drag velocity, direction, distance crossed, and nearby snap thresholds.
   - Otherwise quick flicks and deliberate slow drags can resolve counterintuitively.

12. **[Interaction evidence] No bounds or overscroll model**
   - There is no clamp between collapsed and full limits.
   - The sheet can be dragged beyond intended positions unless `nearestSnapPoint` happens to compensate only on release.
   - Direct manipulation should constrain or intentionally resist out-of-range movement during the drag.

---

## Concrete direct-manipulation moves

1. **Use a gesture state object**
   - Track: `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, `currentY`, `lastY`, `lastTime`, `velocityY`, `currentState`.

2. **Use pointer capture**
   - On valid `pointerdown`, call `sheet.setPointerCapture(event.pointerId)`.
   - Ignore moves from other pointers.
   - Handle `pointerup`, `pointercancel`, and lost capture with the same cleanup path.

3. **Move by delta, not absolute pointer position**
   - Compute: `nextY = startSheetY + (event.clientY - startPointerY)`.
   - Clamp or resist between full and collapsed limits.

4. **Use transform for visual movement**
   - Prefer `translateY(...)` for the sheet position.
   - Avoid animating `top`.
   - Keep layout position stable and treat the sheet offset as a logical value.

5. **Disable transition during active drag**
   - Drag should have immediate 1:1 response.
   - Only the release-to-snap phase should animate.

6. **Replace `transition: all`**
   - Use explicit properties only.
   - Example intent: transform for sheet motion, opacity/color for small state feedback.
   - Do not transition layout, size, or unrelated properties by default.

7. **Use distance-aware snap timing**
   - Short travel: shorter duration.
   - Long travel: capped duration.
   - Use decelerating easing for normal motion, not `ease-in`.

8. **Use velocity-aware snap selection**
   - If velocity exceeds a threshold, snap in the gesture direction.
   - Otherwise snap to the nearest state by position.
   - This makes flicks and careful placement feel intentional.

9. **Store the resolved state**
   - After settling, commit one of: `collapsed`, `half`, `full`.
   - Update attributes such as `data-state`.
   - Use that state for visual affordances and non-motion feedback.

10. **Reduced Motion behavior**
   - If Reduced Motion is requested:
     - Avoid large animated travel.
     - Commit immediately or use a very short fade/opacity/outline/state-label change.
     - Preserve clear state feedback: handle position, state text, shadow/outline, or header affordance.
   - Do not remove feedback entirely.

11. **Replace full-sheet scale press feedback**
   - Prefer a handle highlight, slight shadow change, or header affordance.
   - If scale is used at all, apply it to a small drag handle, not the entire operational sheet.

12. **Add touch behavior contract**
   - Define `touch-action` intentionally.
   - If vertical sheet dragging owns the gesture, prevent page scroll conflicts.
   - If internal content can scroll, coordinate sheet dragging versus content scrolling.

---

## Verified / unverified boundaries

**Verified from provided code:**
- Pointer movement is not gated by an active drag.
- `startY` is unused.
- The sheet is moved and animated with `top`.
- `transition: all 300ms` is present.
- `:active` scales the sheet.
- The release animation uses `duration: 480`, `easing: "ease-in"`, and `fill: "forwards"`.
- No Reduced Motion branch is shown.
- No pointer capture/cancel handling is shown.

**Verified from product context:**
- The sheet has collapsed, half, and full states.
- The app should feel calm and is used repeatedly during the day.
- Reduced Motion must preserve state feedback without large spatial travel.

**Unverified:**
- Actual rendered dimensions.
- Existing `nearestSnapPoint` behavior.
- Whether CSS elsewhere constrains the sheet.
- Real pointer, touch, trackpad, keyboard, or assistive technology behavior.
- Runtime performance, dropped frames, or browser/device-specific behavior.

---

## Smallest runtime validation plan

1. **Gesture correctness**
   - Press near the sheet handle, drag slowly, verify no initial jump.
   - Move pointer outside the sheet, release, verify it still settles correctly.
   - Trigger cancellation path, verify no stuck dragging state.

2. **Snap behavior**
   - Test slow drags near collapsed / half / full thresholds.
   - Test quick flicks upward and downward.
   - Confirm resolved state matches user intent.

3. **Motion feel**
   - Compare short versus long snap distances.
   - Confirm the sheet decelerates into rest and does not accelerate into the final stop.
   - Confirm repeated use does not feel bouncy, jumpy, or distracting.

4. **Reduced Motion**
   - Enable Reduced Motion.
   - Change between collapsed / half / full.
   - Confirm large spatial travel is removed or minimized while state feedback remains clear.

5. **State and accessibility**
   - Confirm final state is stored and exposed in the DOM.
   - Confirm keyboard or non-drag controls can reach collapsed / half / full.
   - Confirm focus is not lost or hidden behind the sheet after state changes.

6. **Performance sanity**
   - During drag, confirm updates use transform-like visual movement rather than layout-heavy positioning.
   - Confirm no broad `transition: all` side effects occur during direct manipulation.


## Output B

## Verdict

**Not acceptable for a calm, repeatedly used operations sheet.**  
Evidence basis: **static code/CSS review only**; no browser, device, or runtime validation performed.

The implementation treats the sheet as a fixed-duration animation target, not as a directly manipulated object. It will likely feel jumpy, laggy, non-interruptible, and unpredictable across collapsed / half / full states.

---

## Prioritized findings

1. **Direct manipulation is broken** — `[code]`  
   `sheet.style.top = event.clientY` makes the sheet’s top snap to the pointer instead of preserving the grab offset. If the user grabs the handle or middle of the sheet, the surface can jump immediately.

2. **Animation is not interruptible** — `[code]`  
   `if (animating) return` blocks re-grabbing during motion. A sheet should be catchable mid-flight and redirected from its current visual position.

3. **Pointer tracking is unsafe** — `[code]`  
   There is no active drag flag, `pointerId`, `setPointerCapture`, `pointercancel`, or lost-capture handling. `pointermove` can move the sheet even when the user is not intentionally dragging.

4. **CSS transition conflicts with gesture tracking** — `[code]`  
   `.sheet { transition: all 300ms; }` can animate `top` changes during drag, causing the sheet to trail the pointer instead of tracking 1:1. `transition: all` also risks accidental animation of unrelated properties.

5. **Uses layout properties on every frame** — `[code]`  
   Animating and reading `top` / `offsetTop` causes layout work. Gesture motion should use a transform-backed position model, e.g. `translateY`, updated on animation frames.

6. **Snap decision ignores velocity** — `[code]`  
   `nearestSnapPoint(sheet.offsetTop)` only considers current position. A flick toward full or collapsed should project momentum and choose the likely destination, not merely the nearest point.

7. **Release animation has the wrong feel** — `[code]`  
   `duration: 480` and `easing: "ease-in"` means the sheet starts slowly after release and accelerates into the target. That creates a visible seam and an unnatural arrival. A calm sheet wants a quick, damped settle that inherits release velocity.

8. **State can become visually/logically inconsistent** — `[code]`  
   `fill: "forwards"` keeps the animation’s visual end state but does not necessarily commit the actual layout/style state cleanly. Future `offsetTop` reads may not match what the user sees.

9. **No bounds or resistance** — `[code]`  
   The sheet can be dragged beyond collapsed/full limits without clamping or rubber-band resistance. Hard stops or unbounded travel both feel poor.

10. **Reduced Motion is absent** — `[context]`  
   The product requires reduced motion to preserve state feedback without large spatial travel. Current code always performs a large spatial animation.

11. **The press scale is too blunt** — `[code/context]`  
   `.sheet:active { transform: scale(0.96); }` scales the whole sheet while dragging may also need transform. It can feel playful/heavy for a calm operations app and may visually fight the drag motion.

12. **No gesture arbitration with sheet content** — `[inference]`  
   A real sheet likely contains scrollable content. This code does not distinguish dragging the handle from scrolling inside the sheet.

---

## Concrete direct-manipulation moves

1. **Use a real sheet position model**  
   Keep `currentY`, `targetY`, and `state` as data. Render with:

   ```css
   transform: translate3d(0, var(--sheet-y), 0);
   ```

   Avoid `top` for gesture motion.

2. **On pointer down: capture and preserve offset**  
   - Ignore non-primary pointers.
   - Store `pointerId`.
   - Call `setPointerCapture`.
   - Cancel any running animation.
   - Read the current visual position.
   - Store `grabOffset = pointerY - currentSheetY`.

3. **During drag: track 1:1**  
   - Only move while dragging the active pointer.
   - Compute `nextY = pointerY - grabOffset`.
   - Clamp inside bounds.
   - Apply soft rubber-band resistance outside bounds.
   - Batch DOM writes with `requestAnimationFrame`.

4. **Track recent velocity**  
   Store the last few `{ y, time }` samples. On release, compute release velocity in px/s.

5. **Project the landing point**  
   Choose collapsed / half / full from a projected endpoint, not only the release position:

   ```js
   projectedY = currentY + projectedDistanceFromVelocity(velocityY);
   target = nearestSnapPoint(projectedY);
   ```

6. **Animate with an interruptible damped settle**  
   Use a spring-like settle from the current visual position to the target, seeded with release velocity. For this product, prefer low/no overshoot by default; reserve any bounce for deliberate, high-velocity flicks, if at all.

7. **Keep feedback calm and local**  
   Instead of scaling the whole sheet to `0.96`, use subtler feedback:
   - handle highlight,
   - slight handle compression,
   - shadow/material change,
   - scrim opacity tied to sheet progress,
   - state label or affordance update.

8. **Respect Reduced Motion**  
   For reduced motion:
   - keep direct drag response while the user is actively manipulating, if appropriate;
   - avoid large automatic travel after release;
   - commit to the target with minimal or instant spatial movement;
   - preserve state feedback through handle color, opacity, shadow, label, or short non-spatial fade;
   - remove overshoot and elastic effects.

9. **Separate handle drag from content scroll**  
   Prefer dragging from a handle/header region. If content scroll participates, arbitrate intent after a small threshold and avoid hijacking normal vertical scroll.

---

## Verified / unverified boundaries

**Verified from static code**  
- Uses `top`, `offsetTop`, WAAPI `animate`, `ease-in`, fixed duration, `fill: forwards`.  
- Blocks pointerdown while `animating`.  
- Has no pointer capture, velocity tracking, bounds, reduced-motion branch, or pointer-cancel handling.  
- CSS applies `transition: all 300ms` and active-state whole-sheet scale.

**Unverified**  
- Actual frame rate, latency, browser behavior, and device feel.  
- Whether `offsetTop` matches final visual state in the target runtime.  
- Interaction with scrollable sheet content.  
- Accessibility semantics, focus management, keyboard support, and screen-reader state announcements.  
- Exact snap-point geometry and visual design context.

---

## Smallest runtime validation plan

1. **Gesture-state tests**  
   Verify: pointer capture, active pointer only, cancel/lost-capture cleanup, no movement without active drag.

2. **Position tests**  
   Verify: no grab jump, correct offset preservation, bounded movement, rubber-band behavior, collapsed/half/full target selection.

3. **Velocity tests**  
   Verify: slow drag snaps by position; flick snaps by projected endpoint; reversal during animation starts from current visual position.

4. **Reduced-motion tests**  
   Verify: no large automatic spatial travel, no overshoot, state feedback remains visible.

5. **Performance smoke plan**  
   Record whether drag writes are transform-only and frame-batched; ensure no per-move layout reads are required during active dragging.


## Output C

**Verdict: Block on direct-manipulation quality and Reduced Motion.**  
Evidence level: static source + stated product context only; no browser, device, frame-rate, or feel validation claimed.

## Prioritized findings

**P0 — Reduced Motion is absent for meaningful spatial travel**  
- **Evidence:** `sheet.animate(... duration: 480 ...)` always animates between snap points; no `prefers-reduced-motion` branch.  
- **Risk:** Collapsed/half/full travel can be large, and this app is used repeatedly during the day.  
- **Fix:** In reduced motion, immediately commit the snap state and use non-spatial feedback: state label, handle affordance, opacity/color/outline change, or a very short localized fade.

**P0 — Drag is not actually 1:1 direct manipulation**  
- **Evidence:** `pointermove` sets `sheet.style.top = event.clientY`; CSS has `.sheet { transition: all 300ms; }`.  
- **Risk:** During drag, the sheet may chase the pointer instead of staying attached; `transition: all` can animate every `top` update.  
- **Fix:** Disable transitions during active drag; track `deltaY` from the grabbed presentation position; preserve grab offset.

**P1 — Layout-property animation is on the gesture hot path**  
- **Evidence:** Both drag and settle use `top`; `offsetTop` is read on release.  
- **Risk:** Layout/reflow work can become visible under data-heavy operations views. Static source proves the risky property choice, not measured jank.  
- **Fix:** Own sheet position with `transform: translateY(...)`; keep snap state as data, not layout side effect.

**P1 — Release behavior ignores velocity and interruption**  
- **Evidence:** Target is `nearestSnapPoint(sheet.offsetTop)`; animation is fixed `480ms ease-in`; `animating` blocks new `pointerdown`.  
- **Risk:** A quick flick and a slow drag ending at the same coordinate resolve identically; users cannot re-grab mid-settle cleanly.  
- **Fix:** Track recent pointer samples in CSS px/s; start settle from current presentation value; hand velocity into a spring-like settle; allow interruption.

**P1 — Visual/logical state can diverge after WAAPI fill**  
- **Evidence:** `fill: "forwards"` holds the animated visual value, but the code does not explicitly commit final `top` or update a canonical sheet state.  
- **Risk:** Later `offsetTop`, hit testing, focus scroll, or snap calculations may use a stale layout value depending on implementation details.  
- **Fix:** On finish/cancel, set the canonical state and final transform explicitly; cancel the animation after committing.

**P2 — Gesture ownership is incomplete**  
- **Evidence:** No pointer capture, no `pointercancel`, no active-pointer guard, no bounds/rubber-band, `startY` is unused.  
- **Risk:** The sheet can move without a committed drag, lose tracking outside bounds, or respond to unintended pointers.  
- **Fix:** Capture the initiating pointer after an 8–12px intent threshold; ignore other pointers; handle cancel; clamp or apply boundary resistance.

**P2 — Press feedback is too broad for a sheet surface**  
- **Evidence:** `.sheet:active { transform: scale(0.96); }`.  
- **Risk:** Scaling the entire operations sheet during drag may feel decorative/heavy and can conflict with transform-based positioning unless composed deliberately.  
- **Fix:** Put press feedback on the handle or a separate wrapper layer; keep it subtle, short, and disabled/replaced under reduced motion.

## Concrete direct-manipulation moves

1. Model states explicitly: `collapsed | half | full`, each mapped to a snap `translateY`.
2. On pointer down, record active pointer id, sheet presentation Y, pointer Y, and grab offset.
3. After a small threshold, set `dragging=true`, capture pointer, and remove transition.
4. On move, update only `transform: translateY(currentY)` with clamped or resisted bounds.
5. Keep a short timestamped position history; compute release velocity in CSS px/s.
6. Choose snap target from product semantics: nearest current position by default; projected endpoint only if momentum targeting is approved.
7. Settle with an interruptible spring/retargetable animation, not fixed `ease-in`.
8. Reduced Motion: commit state with minimal travel and local feedback, preserving collapsed/half/full clarity.

## Verified / unverified boundaries

**Verified from static code:** use of `top`, `transition: all`, fixed `480ms ease-in`, missing reduced-motion branch, missing pointer capture/cancel, unused `startY`, and no visible velocity tracking.

**Not verified:** actual smoothness, frame rate, browser-specific WAAPI behavior, touch feel, real snap geometry, focus behavior, or whether surrounding code compensates for these omissions.

## Smallest runtime validation plan

1. Static check: confirm final implementation has no `transition: all` on the sheet and no drag-time `top` animation.
2. Browser interaction check: drag to each state, interrupt during settle, release inside/outside bounds, and verify canonical state matches visual state.
3. Motion check: compare slow drag, fast flick, and reversal; inspect whether target choice and velocity handoff are intentional.
4. Reduced Motion check: enable `prefers-reduced-motion`; verify state feedback remains clear without large spatial travel.
5. Performance check: record one drag while the operations view is under realistic load; flag long tasks or layout work in the drag path.
