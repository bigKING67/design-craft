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

**Block for production.** Static evidence shows this sheet is not a true direct-manipulation interaction: it mutates layout `top`, lacks drag ownership/capture/interruption, uses delayed settling motion, and has no Reduced Motion path for a high-frequency operations surface.

## Prioritized findings

1. **P0 — Drag is not actually stateful**
   - **Evidence:** `pointermove` always runs and sets `sheet.style.top`, with no `dragging`, `pointerId`, button, or capture guard.
   - **Impact:** Incidental pointer movement over the sheet can move it; multi-pointer/out-of-bounds behavior is undefined.
   - **Fix:** Use explicit states: `idle → dragging → settling`; only move for the captured active pointer.

2. **P0 — The sheet jumps instead of preserving grab offset**
   - **Evidence:** `startY` is recorded but unused; move sets `top = event.clientY`.
   - **Impact:** The sheet’s top edge snaps to the pointer rather than staying attached where the user grabbed it.
   - **Fix:** Store `grabOffset = pointerY - currentSheetY`; drag to `pointerY - grabOffset`.

3. **P0 — Non-interruptible motion**
   - **Evidence:** `if (animating) return` blocks `pointerdown`; settle animation must finish before another drag can begin.
   - **Impact:** Re-grabbing during settle can feel broken, especially in repeated operations work.
   - **Fix:** On new pointerdown, cancel/retarget from the current presentation value and carry current/release velocity forward.

4. **P0 — Layout-property animation on a hot gesture path**
   - **Evidence:** `sheet.style.top`, `sheet.offsetTop`, WAAPI `{ top: ... }`, plus `.sheet { transition: all 300ms; }`.
   - **Impact:** Dragging can trigger layout/reflow and the CSS transition can smear every pointermove, breaking 1:1 tracking.
   - **Fix:** Use `transform: translate3d(0, y, 0)` for drag/settle; disable transitions while dragging; avoid `transition: all`.

5. **P0 — Reduced Motion requirement is unmet**
   - **Evidence:** No `prefers-reduced-motion` branch; settle always performs spatial travel for up to `480ms`.
   - **Impact:** Violates the stated requirement: state feedback must remain without large spatial travel.
   - **Fix:** In reduced motion, snap state immediately or within ~80–120ms using opacity/color/elevation/handle/status feedback, not large travel or bounce.

6. **P1 — Settling feels delayed for a grabbed surface**
   - **Evidence:** `{ duration: 480, easing: "ease-in" }`.
   - **Impact:** `ease-in` starts slow exactly when the user releases; 480ms can feel heavy in a calm, repeated-use ops app.
   - **Fix:** Use a critically damped or lightly damped spring, or a shorter responsive ease-out/ease-in-out settle.

7. **P1 — Snap semantics ignore velocity and hysteresis**
   - **Evidence:** `nearestSnapPoint(sheet.offsetTop)` uses only release position.
   - **Impact:** A deliberate flick may be ignored; near boundaries the sheet may chatter between collapsed/half/full.
   - **Fix:** Measure release velocity in CSS px/s; apply hysteresis between states; only use projected endpoint targeting if product semantics authorize momentum.

8. **P1 — CSS transform ownership conflict**
   - **Evidence:** `.sheet:active { transform: scale(0.96); }`.
   - **Impact:** If drag is moved to `transform`, press scale and translate will fight; scaling the whole sheet also deforms dense content.
   - **Fix:** Put press feedback on a handle or inner wrapper, or compose transform ownership explicitly.

9. **P1 — Failure/cancel paths are missing**
   - **Evidence:** No `pointercancel`, `lostpointercapture`, `.catch()`, animation cancellation, or cleanup.
   - **Impact:** Interrupted gestures or rejected animations can leave `animating = true` or stale visual state.
   - **Fix:** Centralize cleanup and always commit final logical state.

## Concrete direct-manipulation moves

1. Track `activePointerId`, `dragging`, `settlingAnimation`, `currentY`, `targetState`.
2. On `pointerdown`: cancel existing settle, read current presentation Y, store `grabOffset`, capture pointer.
3. Add an `8–12px` intent threshold so clicks/taps on sheet controls are not stolen.
4. During drag: update only `transform: translate3d(0, var(--sheet-y), 0)` via rAF; no CSS transition.
5. Keep a short `{time, y}` history and compute release velocity in **CSS px/s**.
6. Choose target by product-owned rules: nearest/hysteresis by default; projected endpoint only if momentum targeting is intended.
7. Settle from the current presentation value with measured velocity as initial velocity; allow immediate re-grab.
8. Separate layers: outer sheet translates; handle/affordance may scale or change color for press feedback.
9. Commit final state after settle: collapsed/half/full class, ARIA/state label, final transform value.
10. Reduced Motion: avoid long travel; use immediate state jump plus subtle handle, border, shadow, opacity, or label feedback.

## Verified / unverified boundaries

**Verified from the supplied static snippet**
- Uses layout `top` for drag and settle.
- Uses `offsetTop` reads during release.
- Uses `transition: all`.
- Uses `ease-in` with `480ms`.
- Blocks new pointerdown while `animating`.
- Lacks visible Reduced Motion handling in the supplied code.
- Lacks visible pointer capture, pointercancel, velocity, hysteresis, and grab-offset use.

**Not verified**
- Actual frame rate, input latency, device feel, or browser-specific animation behavior.
- Whether surrounding code adds accessibility, keyboard controls, snap-state announcements, or reduced-motion overrides.
- Whether the sheet contains scrollable regions that require gesture arbitration.
- Whether product semantics want nearest-position snapping or momentum-based flick snapping.

## Smallest runtime validation plan

1. **Pointer behavior:** drag from handle/body, release outside sheet, re-grab mid-settle, cancel pointer, try multi-touch/secondary pointer.
2. **Continuity check:** confirm no jump on grab, no jump on interruption, and settle starts from current visual position.
3. **Snap check:** test collapsed ↔ half ↔ full around thresholds; verify hysteresis prevents flicker.
4. **Reduced Motion check:** emulate `prefers-reduced-motion: reduce`; confirm no large spatial travel and state feedback remains clear.
5. **Performance check:** record one drag/settle trace; verify transform-only animation, no repeated layout on pointermove, and no transition-smearing.
6. **Accessibility check:** keyboard state changes, focus retention, visible focus, and announced collapsed/half/full state.


## Output B

## Evidence-labeled verdict

**Verdict: Not production-ready for a calm repeated-use operations sheet.**  
**Static evidence:** the implementation animates `top`, uses `transition: all`, ignores reduced motion, has no drag state/pointer capture, and uses a long `ease-in` settle.  
**Likely user impact:** laggy direct manipulation, accidental jumps, scroll/drag conflicts, inaccessible state changes, and excessive spatial motion for Reduced Motion users.

---

## Prioritized findings

### P0 — Direct manipulation is broken
**Evidence:** `pointermove` always sets `sheet.style.top = event.clientY`.  
**Problem:** the sheet jumps to the pointer’s viewport Y instead of preserving the grab offset. `startY` is stored but unused.  
**Impact:** the panel will feel detached from the finger/mouse, especially when grabbed from different vertical positions.

### P0 — No drag ownership or cancellation model
**Evidence:** no `dragging` flag, no `setPointerCapture`, no `pointercancel`, no `lostpointercapture`.  
**Problem:** moves can apply without a valid drag, and the interaction can get stuck or leak across pointers.  
**Impact:** unreliable under touch, stylus, trackpad, iframe boundaries, browser gestures, or interrupted drags.

### P0 — Motion uses layout properties instead of compositor-safe transforms
**Evidence:** `style.top`, `offsetTop`, WAAPI over `top`, and `.sheet { transition: all 300ms; }`.  
**Problem:** `top` triggers layout; `offsetTop` forces layout reads; `transition: all` can accidentally animate drag updates.  
**Impact:** frame drops are likely on a dense operations surface, especially beside a large table.

### P0 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` handling; settle duration is always `480ms`; spatial travel remains full.  
**Problem:** Reduced Motion must preserve state feedback without large travel.  
**Impact:** fails a stated product requirement and may cause discomfort.

### P1 — Snap behavior lacks intent modeling
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only considers position.  
**Problem:** no velocity, direction, hysteresis, thresholds, or “commit/cancel” distinction.  
**Impact:** sheet may snap contrary to user intent, especially with quick flicks or near the midpoint.

### P1 — Easing and duration are wrong for an operational sheet
**Evidence:** `{ duration: 480, easing: "ease-in" }`.  
**Problem:** `ease-in` starts slowly and accelerates into the destination, which feels like the sheet is slipping away.  
**Impact:** not calm or responsive. Repeated use will feel sluggish and imprecise.

### P1 — Animation state can desynchronize from DOM state
**Evidence:** WAAPI uses `fill: "forwards"` but does not commit the final `top` to the element’s actual style/model.  
**Problem:** visual state and logical state can diverge across later reads, resize, rerender, or style changes.  
**Impact:** future snaps may start from stale or inconsistent positions.

### P1 — CSS conflicts with JS motion
**Evidence:** `.sheet { transition: all 300ms; }` plus `sheet.animate(...)`.  
**Problem:** global transition can compete with drag writes and WAAPI animations.  
**Impact:** double easing, delayed pointer tracking, hard-to-debug motion artifacts.

### P1 — `:active` scale damages spatial continuity
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Problem:** scaling the whole sheet during drag changes perceived position and can make content visually pulse.  
**Impact:** hostile to precision use; conflicts with transform-based sheet movement unless composed carefully.

### P2 — Missing accessibility state and alternate controls
**Evidence:** no role/state updates, keyboard handling, labels, or focus behavior shown.  
**Problem:** collapsed/half/full states need non-pointer operation and announced state changes.  
**Impact:** keyboard-heavy operators and assistive tech users cannot reliably operate the sheet.

---

## Concrete direct-manipulation moves

1. **Use an explicit interaction state**
   - Track `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, and current snap state.
   - Ignore unrelated pointers.
   - Handle `pointercancel` and `lostpointercapture`.

2. **Capture the pointer on drag start**
   - On `pointerdown`, call `setPointerCapture(event.pointerId)`.
   - Add `touch-action: none` or a narrower value only on the drag handle, not necessarily the whole sheet.

3. **Move with `transform`, not `top`**
   - Represent position as `translateY(...)`.
   - Keep snap positions in a model value.
   - Avoid layout reads during drag.

4. **Make drag 1:1**
   - `nextY = clamp(startSheetY + event.clientY - startPointerY, fullY, collapsedY)`.
   - Apply immediately via `transform`.
   - Batch pointer updates with `requestAnimationFrame` if needed.

5. **Disable CSS transition during drag**
   - Use classes such as `.is-dragging` and `.is-settling`.
   - Never use `transition: all`.
   - Transition only the intended property: `transform`.

6. **Snap by intent, not only distance**
   - Use position + velocity + direction.
   - Add hysteresis so the sheet does not jitter between half/full near boundaries.
   - Example intent: fast upward flick promotes to fuller state; fast downward flick demotes.

7. **Use responsive settle motion**
   - Prefer a short, decelerating or spring-like settle.
   - Avoid `ease-in`.
   - Duration should scale with remaining distance but stay bounded.

8. **Implement Reduced Motion as state feedback, not travel**
   - For reduced motion, shorten duration dramatically or jump position.
   - Preserve feedback through opacity, border, shadow, handle color, status text, or subtle 80ms affordance.
   - Do not animate large vertical travel.

9. **Commit final state**
   - After settle, set the canonical state: `collapsed | half | full`.
   - Commit the final transform/model value.
   - Update ARIA/state labels from the same source of truth.

10. **Keep press feedback separate from sheet position**
   - Replace full-sheet `scale(0.96)` with a subtle handle/button affordance.
   - If scale is used, compose transforms carefully and disable it during drag.

---

## Verified / unverified boundaries

**Verified from static code:**
- `top` is used for drag and animation.
- `transition: all` is present.
- `startY` is unused.
- no reduced-motion branch is present.
- no pointer capture/cancel handling is present.
- no keyboard or semantic state handling is shown.
- settle uses `480ms ease-in`.

**Not verified:**
- actual frame rate or input latency.
- behavior on real touch hardware.
- behavior inside the full product layout.
- interaction with scrolling containers.
- whether surrounding code adds accessibility, state, or resize handling.
- whether `nearestSnapPoint` clamps, debounces, or understands velocity.

---

## Smallest runtime validation plan

1. **Pointer correctness**
   - Drag from handle, middle, and lower sheet area.
   - Confirm no initial jump and 1:1 pointer tracking.

2. **Snap intent**
   - Slow drag near each midpoint.
   - Fast flick up/down.
   - Confirm expected collapsed/half/full result.

3. **Interruption handling**
   - Start drag, leave viewport, cancel gesture, multi-touch, release outside sheet.
   - Confirm no stuck dragging or stale animation lock.

4. **Performance smoke**
   - Record a drag and settle on a dense page.
   - Check for layout thrash, long tasks, dropped frames, and forced reflow around `pointermove`.

5. **Reduced Motion**
   - Enable reduced motion.
   - Confirm state still changes clearly but without large animated travel.

6. **Keyboard and assistive flow**
   - Operate collapsed/half/full without pointer.
   - Confirm focus order, visible focus, labels, and announced state.


## Output C

## Verdict

**[Static evidence]** This is **not production-ready gesture motion** for a calm repeated-use operations app. It behaves like a scripted `top` animation attached to pointer events, not like a directly manipulated sheet with stable state, velocity, interruption, reduced-motion handling, or low-latency feedback.

**[Impact]** Users will see jumps, lag, wrong snap decisions, non-interruptible motion, and potentially stuck states—especially harmful for operators who repeatedly open, resize, and dismiss the sheet throughout the day.

---

## Prioritized findings

### P0 — Direct manipulation is broken

**[Static evidence]**
- `pointermove` sets `sheet.style.top = event.clientY`.
- `startY` is captured but not used.
- No grab offset is preserved.
- No active-drag guard is shown for `pointermove`.

**[Impact]**
- The sheet can jump so its top edge aligns with the pointer instead of preserving where the user grabbed it.
- Pointer movement may affect the sheet even when no valid drag is active.
- The interaction will feel detached rather than “under the hand.”

**[Fix direction]**
- Track `dragStartPointerY`, `dragStartSheetY`, and `grabOffset`.
- Move the sheet to `dragStartSheetY + deltaY`, not raw `clientY`.
- Ignore moves unless the current pointer is captured and dragging.

---

### P0 — The sheet is non-interruptible

**[Static evidence]**
- `if (animating) return;` on `pointerdown`.
- New gestures are blocked while the release animation is running.

**[Impact]**
- Users cannot grab the sheet mid-flight and reverse direction.
- This creates a “dead” interval after every release.
- Repeated operations will feel sluggish and authoritarian.

**[Fix direction]**
- On new `pointerdown`, cancel or retarget the current animation from the live visual position.
- Never lock out direct manipulation.
- Preserve current velocity when retargeting if using a spring.

---

### P0 — Uses layout properties on the input path

**[Static evidence]**
- Drag writes `style.top`.
- Release reads `sheet.offsetTop`.
- Animation interpolates `top`.

**[Impact]**
- `top` and `offsetTop` can force layout work.
- Animating `top` is not compositor-friendly.
- A 10,000-row operations surface is especially vulnerable to input jank.

**[Fix direction]**
- Represent sheet position as `translateY(...)`.
- Store logical sheet position in JS state.
- Use `requestAnimationFrame` to batch pointer-driven writes.
- Avoid layout reads during drag.

---

### P1 — Snap behavior ignores velocity and intent

**[Static evidence]**
- `nearestSnapPoint(sheet.offsetTop)` uses position only.
- No release velocity is measured.
- No momentum projection or directional threshold exists.

**[Impact]**
- A quick flick may snap back to the nearest point instead of continuing toward the intended state.
- Slow careful drags and fast throws are treated the same.
- Collapsed / half / full state changes will feel unpredictable.

**[Fix direction]**
- Keep a short pointer history of `{ y, time }`.
- Compute release velocity.
- Project the likely endpoint.
- Choose the snap point nearest the projected endpoint, with hysteresis to avoid accidental state changes.

---

### P1 — Release animation has the wrong character

**[Static evidence]**
- `{ duration: 480, easing: "ease-in" }`.

**[Impact]**
- `ease-in` starts slowly and ends fast, which is usually the opposite of a settling sheet.
- Fixed 480ms travel can feel heavy for repeated desktop work.
- It does not inherit release velocity.

**[Fix direction]**
- Prefer an interruptible spring-like settle.
- Use calmer, critically damped motion for normal state changes.
- Only allow slight overshoot if the user created momentum with a flick.
- If using duration-based fallback, use a decelerating curve and shorter travel-aware durations.

---

### P1 — CSS conflicts with gesture motion

**[Static evidence]**
- `.sheet { transition: all 300ms; }`
- `.sheet:active { transform: scale(0.96); }`

**[Impact]**
- `transition: all` can accidentally animate layout, size, color, shadow, and future properties.
- It may add lag to direct pointer updates.
- Scaling the entire sheet during drag deforms operational content and can conflict with transform-based movement.

**[Fix direction]**
- Do not use `transition: all`.
- Limit transitions to intentional properties.
- Put press feedback on the drag handle, header affordance, shadow, or grip—not the entire data surface.
- Keep drag transform and press feedback composable, e.g. separate wrapper layers.

---

### P1 — Reduced Motion is absent

**[Static evidence]**
- No `prefers-reduced-motion` handling is shown.
- Large spatial travel is always animated.

**[Impact]**
- Users requesting reduced motion still get full sheet travel.
- State changes may be hard to follow if motion is simply removed without replacement feedback.

**[Fix direction]**
- In reduced motion:
  - avoid elastic travel and large animated slides;
  - snap position quickly or nearly instantly;
  - preserve state feedback with opacity, outline, shadow, label, handle state, or subtle content fade;
  - keep state announcements and visual affordances intact.

---

### P2 — Missing pointer lifecycle safety

**[Static evidence]**
- No `setPointerCapture`.
- No `pointercancel`.
- No `lostpointercapture`.
- No pointer id tracking.
- No cleanup path if `.finished` rejects or animation is canceled.

**[Impact]**
- Drag may fail if the pointer leaves the sheet.
- Multi-pointer input can corrupt state.
- `animating` can remain stuck if the animation is interrupted or canceled.

**[Fix direction]**
- Capture the initiating pointer.
- Track `pointerId`.
- Handle `pointerup`, `pointercancel`, and `lostpointercapture`.
- Use `try/finally` or equivalent cleanup around animation completion.

---

## Concrete direct-manipulation moves

1. **State model**
   - Maintain explicit state: `collapsed | half | full`.
   - Maintain numeric `currentY`.
   - Keep snap points in one coordinate system.

2. **Pointer down**
   - Cancel/retarget any running settle animation.
   - Read the current visual position.
   - Capture pointer.
   - Store grab offset and recent movement history.
   - Show immediate but restrained feedback.

3. **Pointer move**
   - Only respond to the captured pointer.
   - Compute `nextY = startSheetY + pointerDeltaY`.
   - Apply bounds with soft rubber-band resistance.
   - Write `transform: translate3d(0, nextYpx, 0)` in a frame-synced batch.
   - Do not read layout every move.

4. **Pointer release**
   - Compute release velocity.
   - Project endpoint from velocity.
   - Choose collapsed / half / full from projected endpoint, not raw position alone.
   - Settle from current visual position to target.
   - Update semantic state when the target is committed.

5. **Reduced motion**
   - Keep snap states.
   - Replace large travel with near-instant reposition plus small opacity/shadow/handle feedback.
   - Remove bounce and long easing.
   - Preserve visible and announced state change.

6. **CSS hygiene**
   - Replace `transition: all` with explicit transitions.
   - Use transforms for motion.
   - Avoid scaling the whole sheet; apply press feedback to the handle or header affordance.

---

## Static-only verified boundaries

**Verified from the snippet**
- Motion is driven by `top`, not transform.
- Release uses fixed-duration WAAPI animation.
- Animation blocks new pointerdown handling.
- Snap decision is position-only.
- CSS uses `transition: all`.
- Whole-sheet active scaling is present.
- No reduced-motion branch is shown.
- No pointer capture or cancellation handling is shown.

**Not verified**
- Actual snap point values.
- Whether other code guards pointer state.
- Whether external CSS sets `touch-action`.
- Actual rendering performance.
- Actual accessibility tree, focus behavior, keyboard controls, or announcements.
- Actual behavior in any runtime, browser, or device environment.

---

## Smallest runtime validation plan

1. Build a minimal fixture with only the sheet, three snap points, and logged `y`, velocity, target state, and active animation status.  
2. Test grabs from top, middle, and handle positions; pass only if there is no initial jump.  
3. Drag slowly across each threshold; pass only if collapsed / half / full decisions are stable.  
4. Flick up and down from near the half point; pass only if velocity changes the target appropriately.  
5. Interrupt the sheet mid-settle and reverse it; pass only if it follows immediately without waiting.  
6. Move the pointer outside the sheet during drag; pass only if capture/cancel paths leave no stuck state.  
7. Enable reduced motion; pass only if state feedback remains clear without large animated travel.  
8. Inspect frame timing during drag; pass only if pointer movement avoids layout-triggering reads/writes on the hot path.
