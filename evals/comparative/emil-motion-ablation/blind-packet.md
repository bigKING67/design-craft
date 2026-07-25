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

## Evidence-labeled verdict

**Verdict: Not production-ready for a calm repeated-use operations sheet.**  
**Evidence:** The implementation moves layout with `top` on every `pointermove`, animates `top` with a slow `ease-in`, has no reduced-motion branch, no pointer capture/cancel handling, no velocity-aware snapping, and CSS applies `transition: all` plus `:active` scale. These choices make the sheet feel laggy, jumpy, and fragile under repeated direct manipulation.

---

## Prioritized findings

### P0 — Direct manipulation is not actually anchored to the user’s drag
**Evidence:** `startY = event.clientY` is recorded but never used; `pointermove` sets `sheet.style.top = event.clientY`.  
**Impact:** The sheet’s top edge jumps to the pointer position instead of preserving the grab offset. This breaks the “attached to finger/cursor” illusion.

### P0 — Motion uses layout properties instead of compositor transforms
**Evidence:** `sheet.style.top`, `sheet.offsetTop`, and WAAPI keyframes on `top`.  
**Impact:** Dragging forces layout reads/writes and can jank under a 10,000-row operations surface. Use `transform: translateY(...)` for drag and snap motion.

### P0 — Reduced Motion requirement is unmet
**Evidence:** Fixed `{ duration: 480, easing: "ease-in" }`; no `prefers-reduced-motion` branch.  
**Impact:** Large spatial travel remains mandatory. The product requirement says reduced motion must preserve state feedback without large spatial travel.

### P1 — Snap behavior ignores velocity, direction, and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only considers final position.  
**Impact:** A fast upward flick near the half point may incorrectly snap down; slow precise drags and intentional flings are treated the same.

### P1 — Animation can become inconsistent or stuck
**Evidence:** `animating = true`; `.finished.then(...)` only resets on success; no `pointercancel`, no animation cancellation, no rejection handling.  
**Impact:** If the animation is interrupted or canceled, `animating` can remain true and block future drags.

### P1 — CSS conflicts with interaction model
**Evidence:** `.sheet { transition: all 300ms; }` and `.sheet:active { transform: scale(0.96); }`.  
**Impact:** `transition: all` may animate unrelated changes and fight scripted motion. `:active` scaling shrinks content during drag, causes visual instability, and conflicts with transform-based sheet movement.

### P1 — Pointer lifecycle is incomplete
**Evidence:** No `setPointerCapture`, no pointer id tracking, no `pointercancel`, no bounds checking, no “dragging” guard in `pointermove`.  
**Impact:** Movement can continue without a valid drag start, lose control when the pointer leaves the sheet, and mishandle multi-pointer cases.

### P2 — Motion language is too heavy for calm operations use
**Evidence:** 480ms `ease-in` snap.  
**Impact:** `ease-in` accelerates toward the end, which can feel unresponsive at release and abrupt near arrival. For repeated work, snaps should feel immediate, stable, and predictable.

### P2 — Accessibility/state semantics are absent
**Evidence:** No explicit collapsed/half/full state model exposed to keyboard or assistive tech.  
**Impact:** Gesture-only operation excludes keyboard-heavy users and makes state recovery unclear.

---

## Concrete direct-manipulation moves

1. **Use a real state model**
   - Track `currentState: "collapsed" | "half" | "full"`.
   - Store snap points as measured pixel offsets or CSS variables.
   - Commit state after every snap.

2. **Drag with transform, not top**
   - Keep layout position stable.
   - Apply `transform: translateY(var(--sheet-y))`.
   - During drag, update only the transform value.

3. **Preserve grab offset**
   - On `pointerdown`, record:
     - pointer id
     - start pointer Y
     - current sheet Y
   - On `pointermove`, calculate `nextY = startSheetY + event.clientY - startPointerY`.

4. **Clamp movement**
   - Constrain between full and collapsed snap points.
   - Optionally add small resistance beyond bounds, but do not let the sheet freely escape.

5. **Capture the pointer**
   - Use pointer capture on drag start.
   - Ignore moves from other pointer ids.
   - Handle `pointerup`, `pointercancel`, and lost capture the same way.

6. **Use velocity-aware snapping**
   - If release velocity exceeds a threshold, bias toward the next state in the drag direction.
   - Otherwise snap to the nearest state with hysteresis so small accidental moves do not change state.

7. **Use calm snap timing**
   - Prefer a responsive decelerating curve, not `ease-in`.
   - Shorter duration for short travel, bounded duration for long travel.
   - Example behavior: quick settle for nearby snap, slightly longer but still controlled settle for full travel.

8. **Remove `transition: all`**
   - Limit transitions to intentional properties only.
   - Do not let CSS transitions implicitly animate layout, size, color, or transform during drag.

9. **Remove active scale from the whole sheet**
   - If feedback is needed, apply it to the grab handle only.
   - Better: use handle color, shadow, or subtle affordance change instead of shrinking the full panel.

10. **Reduced Motion behavior**
   - Avoid large animated travel.
   - On release, snap immediately or with a very short duration.
   - Preserve feedback through state label, handle emphasis, shadow change, or brief non-spatial highlight.

11. **Keyboard parity**
   - Provide controls for collapsed/half/full.
   - Ensure focus is not lost when state changes.
   - Expose the current state with accessible naming or state text.

---

## Verified / unverified boundaries

**Verified from static code only**
- Drag writes `top` on every `pointermove`.
- `startY` is unused.
- Snap animation uses `top`, `480ms`, and `ease-in`.
- Reduced Motion handling is absent.
- CSS uses `transition: all`.
- CSS scales the entire sheet on `:active`.
- Pointer capture, cancel handling, velocity, and keyboard handling are not shown.

**Unverified**
- Actual frame rate or jank on target devices.
- Whether surrounding code adds accessibility semantics.
- Whether `nearestSnapPoint` includes bounds, hysteresis, or state persistence.
- Whether CSS elsewhere overrides this behavior.
- Real browser/device behavior under touch, pen, trackpad, or assistive technology.

---

## Smallest runtime validation plan

1. **Drag fidelity**
   - Press on handle, move slowly, confirm the sheet stays attached without jumping.

2. **Snap intent**
   - Test slow drags and fast flicks between collapsed, half, and full.
   - Confirm direction and velocity affect the final state predictably.

3. **Performance**
   - Record a drag while the large table is present.
   - Check for layout thrash, long frames, and dropped frames.

4. **Reduced Motion**
   - Enable reduced motion.
   - Confirm state changes still provide feedback without large animated travel.

5. **Pointer resilience**
   - Drag outside the sheet, cancel mid-drag, use multi-pointer input.
   - Confirm the sheet recovers and remains interactive.

6. **Keyboard/accessibility**
   - Navigate and change states using keyboard only.
   - Confirm visible focus, state announcement or label, and stable focus after snapping.


## Output B

## Verdict

**Block — static evidence only.** The implementation is not production-ready for a calm, repeatedly used operations sheet because it breaks direct manipulation, animates layout properties, locks input during settle, lacks velocity/interruptibility, and has no Reduced Motion path.

## Prioritized findings

1. **P0 — Drag is not actually gated or captured.**  
   **Evidence:** `pointermove` always writes `sheet.style.top`, even if no valid drag started; `pointerdown` only records `startY`; no `setPointerCapture`, no active pointer id, no grab offset.  
   **Impact:** The sheet can jump to the pointer’s viewport Y, lose tracking outside bounds, and confuse taps with drags.

2. **P0 — Uses layout-position animation in the hot path.**  
   **Evidence:** drag and WAAPI animate `top`; settle reads `sheet.offsetTop`. CSS also declares `transition: all 300ms`.  
   **Impact:** This risks forced layout, broad style transitions, and poor behavior in a dense operations surface. Sheet motion should be compositor-friendly.

3. **P0 — Interaction is non-interruptible.**  
   **Evidence:** `if (animating) return;` rejects new `pointerdown` until `.finished`; animation starts from `sheet.offsetTop`, not necessarily the current visual presentation value.  
   **Impact:** A user cannot grab the sheet mid-flight; repeated daily use will feel laggy and untrustworthy.

4. **P1 — Settle physics are backwards for UI response.**  
   **Evidence:** `{ duration: 480, easing: "ease-in" }`.  
   **Impact:** `ease-in` delays the beginning of a user-triggered response; 480ms is heavy for a frequent operations control unless the distance is very large and intentional.

5. **P1 — Snap target ignores velocity and hysteresis.**  
   **Evidence:** `nearestSnapPoint(sheet.offsetTop)` only uses release position; no movement threshold, velocity samples, bounded projection, or boundary resistance.  
   **Impact:** Quick flicks and slow drags resolve the same way; small accidental motion may move the sheet.

6. **P1 — Reduced Motion requirement is absent.**  
   **Evidence:** no `prefers-reduced-motion` branch; same large spatial travel always runs.  
   **Impact:** Violates the stated requirement. Reduced Motion should preserve state feedback without long travel.

7. **P2 — Transform ownership conflicts.**  
   **Evidence:** `.sheet:active { transform: scale(0.96); }` while the interaction should ideally use `transform: translateY(...)`; `transition: all` may animate unrelated properties.  
   **Impact:** Press feedback can overwrite or fight drag transforms unless separated into nested layers.

## Concrete direct-manipulation moves

1. **Track an explicit drag session.**  
   On `pointerdown`, store `pointerId`, `startPointerY`, current sheet Y, and `grabOffset`; call `setPointerCapture(pointerId)` after intent is established.

2. **Add intent hysteresis.**  
   Require about `8–12px` vertical movement before committing to sheet drag, so clicks/taps on controls inside the sheet remain usable.

3. **Move with transform, not top.**  
   Represent sheet position as `translateY(y)` on a dedicated moving layer. Keep layout snap points as numbers, not live `offsetTop` reads during the gesture.

4. **Separate transform owners.**  
   Use an outer layer for `translateY(...)` and an inner layer for press feedback like `scale(0.98)`, or compose both transforms in one controlled value.

5. **Update on the display frame.**  
   Coalesce pointermove values and apply one transform update per animation frame; avoid layout reads/writes in the pointermove hot path.

6. **Make settle interruptible.**  
   If the user presses during settle, cancel/read the current presentation Y, preserve current velocity, and retarget from that visible position without jumping.

7. **Measure release velocity.**  
   Keep recent samples in CSS px and monotonic time; compute release velocity in CSS px/s. Use it as the initial velocity for the settle animation.

8. **Separate target semantics from physics.**  
   Keep the product’s existing collapsed/half/full target rule if nearest-current-position is intentional. If momentum targeting is desired, compute a bounded projected endpoint, clamp it, then choose the nearest valid snap point.

9. **Use calm settle motion.**  
   Prefer a critically damped or near-damped spring, or a short responsive curve. Avoid `ease-in`; use immediate response at release.

10. **Implement Reduced Motion.**  
   Under `prefers-reduced-motion: reduce`, skip large animated travel or compress it to a very short state change; preserve feedback with state labels, subtle opacity/color, focus, or a brief non-spatial affordance.

## Verified / unverified boundaries

**Verified from the supplied static snippet:**

- No visible Reduced Motion branch is present.
- Pointer capture is not used.
- Drag writes `top` directly.
- Settle animates `top`.
- CSS uses `transition: all`.
- Settle uses `480ms ease-in`.
- Input is blocked while `animating` is true.
- Release target is based on `nearestSnapPoint(sheet.offsetTop)` only.
- `:active` writes `transform: scale(...)`.

**Not verified from static code:**

- Actual frame rate, jank, or layout cost.
- Whether surrounding CSS constrains `top` safely.
- Whether `nearestSnapPoint` has hidden hysteresis or clamping.
- Whether other code handles keyboard access, ARIA state, focus management, or snap-state announcements.
- Touch-device feel, trackpad behavior, browser differences, or 60/120Hz smoothness.
- Whether product semantics require nearest-position snapping or momentum-based snapping.

## Smallest runtime validation plan

1. **Gesture correctness:** drag from each snap state; verify no jump on pickup, pointer remains captured outside sheet bounds, and taps inside the sheet are not stolen before threshold.  
2. **Interruption:** release toward half/full, grab mid-settle, reverse direction; verify the sheet starts from the visible position with no snap-back.  
3. **Targeting:** compare slow drag vs fast flick using logged release velocity in CSS px/s; confirm whether product-approved target semantics are followed.  
4. **Reduced Motion:** enable reduced motion; verify state changes remain understandable without large spatial travel.  
5. **Performance smoke:** record one drag/settle under representative table load; confirm transform-only frame updates and no repeated layout reads in the gesture path.


## Output C

## Evidence-labeled verdict

**Verdict: Not production-ready for a calm repeated-use operations sheet.**  
**Evidence:** The implementation moves layout via `top`, locks input while animating, snaps by current `offsetTop` only, uses fixed `480ms ease-in`, applies `transition: all`, has no reduced-motion path, and does not preserve drag offset, velocity, interruption, or keyboard/state feedback.

The result will likely feel **laggy, jumpy, non-interruptible, and physically inconsistent**, especially across collapsed / half / full sheet states.

---

## Prioritized findings

### P0 — Drag is not true direct manipulation
**Evidence:** `startY = event.clientY` is stored but never used; `pointermove` sets `sheet.style.top = event.clientY`.  
**Impact:** The sheet jumps so its top edge follows the pointer instead of preserving where the user grabbed it.  
**Fix direction:** Track `grabOffset = pointerY - sheetTop`, then set position to `pointerY - grabOffset`.

---

### P0 — Input is locked during animation
**Evidence:** `if (animating) return;` on `pointerdown`.  
**Impact:** Users cannot grab the sheet mid-flight, reverse direction, or correct an accidental release. This is hostile for repeated operations work.  
**Fix direction:** Allow interruption. Cancel or retarget the current animation from the sheet’s current visual position.

---

### P0 — Uses layout properties for every frame
**Evidence:** `sheet.style.top = ...`, `sheet.offsetTop`, animated `top`.  
**Impact:** `top` and `offsetTop` force layout work and can cause jank, especially inside a dense operations UI.  
**Fix direction:** Use a single motion value mapped to `transform: translateY(...)`; read layout once at gesture start if needed.

---

### P0 — Snap choice ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only considers release position.  
**Impact:** A fast upward flick near the lower state may incorrectly return downward. The gesture does not feel like it carries momentum.  
**Fix direction:** Track recent pointer samples, compute release velocity, project the likely resting point, then choose collapsed / half / full from that projected value.

---

### P1 — Release animation has the wrong feel
**Evidence:** `{ duration: 480, easing: "ease-in" }`.  
**Impact:** `ease-in` starts slowly after the user releases, creating a visible seam between finger motion and sheet motion. A fixed 480ms duration can feel sluggish for short moves and abrupt for long moves.  
**Fix direction:** Use a velocity-aware spring or adaptive timing. Start from the current visual position and carry the release velocity into the settle.

---

### P1 — CSS conflicts with gesture animation
**Evidence:** `.sheet { transition: all 300ms; }` plus JS-driven `top` animation.  
**Impact:** `transition: all` may animate unrelated properties, fight imperative animation, and create unpredictable delays.  
**Fix direction:** Remove `transition: all`; only transition non-gesture properties intentionally, e.g. opacity, shadow, or handle color.

---

### P1 — Press feedback is spatially misleading
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** Scaling the entire sheet during drag can detach content from the pointer, shift perceived geometry, and feel decorative rather than useful.  
**Fix direction:** Put press feedback on the drag handle or header only: subtle handle highlight, shadow lift, or grip state.

---

### P1 — Reduced Motion requirement is unmet
**Evidence:** No `prefers-reduced-motion` handling; full spatial travel remains.  
**Impact:** Users requesting reduced motion still get large sheet movement and a 480ms travel animation.  
**Fix direction:** Preserve state feedback with short opacity/color/elevation changes, instant or near-instant position changes, no bounce, no large animated travel.

---

### P2 — Pointer lifecycle is incomplete
**Evidence:** No `setPointerCapture`, no `pointercancel`, no lost-capture handling, no active pointer id.  
**Impact:** Drag can break when the pointer leaves the sheet, another pointer appears, or the browser cancels the gesture.  
**Fix direction:** Capture the initiating pointer, ignore other pointers, clean up on `pointerup`, `pointercancel`, and lost capture.

---

### P2 — Animation state can get stuck
**Evidence:** `.finished.then(...)` only resets `animating` on fulfillment.  
**Impact:** If animation is cancelled or rejects, `animating` may remain `true`.  
**Fix direction:** Use `try/finally` semantics or handle both resolve and reject; better, remove the global lock and model animation as interruptible.

---

### P2 — Logical state is not committed
**Evidence:** `fill: "forwards"` visually holds the final frame, but no durable state is shown.  
**Impact:** DOM style, snap state, accessibility state, and business state can diverge.  
**Fix direction:** On settle, commit `currentSnap = "collapsed" | "half" | "full"` and set the actual transform/style to that state.

---

## Concrete direct-manipulation moves

1. **Use transform-based position**
   - Maintain `sheetY` as the single source of truth.
   - Render with `transform: translate3d(0, ${sheetY}px, 0)`.

2. **Respect grab offset**
   - On pointer down: read `sheetTop`.
   - Store `grabOffset = event.clientY - sheetTop`.
   - During drag: `nextY = event.clientY - grabOffset`.

3. **Capture the pointer**
   - Call `setPointerCapture(event.pointerId)`.
   - Track only that pointer until release/cancel.

4. **Add drag hysteresis**
   - Do not commit to dragging until movement passes a small threshold.
   - Prevent accidental sheet movement from clicks on controls inside the sheet.

5. **Track velocity**
   - Store recent `{ y, time }` samples.
   - On release, compute px/s from the last short window.

6. **Project before snapping**
   - `projectedY = currentY + projectedMomentum(velocityY)`.
   - Choose the nearest snap point from `projectedY`, not just `currentY`.

7. **Make release interruptible**
   - If the user presses during settle, cancel/retarget from the current visual transform.
   - Do not block `pointerdown` with `animating`.

8. **Use calm spring behavior**
   - Default: critically damped / no overshoot.
   - Allow only slight momentum response for deliberate flicks.
   - Avoid decorative bounce in an operations app.

9. **Replace full-sheet active scale**
   - Use handle/header feedback:
     - handle darkens slightly,
     - sheet shadow/elevation changes,
     - cursor/pressed state updates.
   - Keep the sheet’s content spatially stable.

10. **Reduced Motion behavior**
    - Position may change immediately or with very short travel.
    - Preserve state feedback via opacity, border, handle color, elevation, or label change.
    - Avoid bounce, long slides, and large viewport movement.

---

## Verified / unverified boundaries

**Verified from static code:**
- `top` is used for drag and animation.
- `offsetTop` is used for snap calculation.
- Input is blocked while `animating` is true.
- Release animation uses `480ms ease-in`.
- CSS uses `transition: all 300ms`.
- CSS scales the entire sheet on `:active`.
- No visible reduced-motion branch exists in the snippet.
- No pointer capture, cancellation handling, velocity tracking, or snap-state commit is shown.

**Not verified from the snippet:**
- Actual snap point values.
- Whether surrounding code handles keyboard state, ARIA, focus management, or scroll locking.
- Whether the sheet contains interactive controls that need gesture disambiguation.
- Actual frame rate, layout cost, or device performance.
- Browser/device behavior.
- Whether external CSS overrides these rules.

---

## Smallest runtime validation plan

1. **Direct manipulation check**
   - Press the sheet at different vertical points.
   - Confirm the grabbed point stays under the pointer without jumping.

2. **Interruption check**
   - Release toward half/full.
   - While it is settling, grab again and reverse direction.
   - Expected: no lockout, no visual jump.

3. **Velocity check**
   - Slowly drag near a boundary.
   - Then perform a fast flick from the same release position.
   - Expected: snap target changes based on intent/velocity.

4. **Performance check**
   - Record a drag session.
   - Confirm motion uses compositor-friendly transforms and avoids repeated layout reads during move.

5. **Reduced Motion check**
   - Enable reduced motion.
   - Move between collapsed / half / full.
   - Expected: state still changes clearly, but without long spatial travel or bounce.

6. **Pointer lifecycle check**
   - Drag outside the sheet, cancel, multi-touch/secondary pointer, and release outside bounds.
   - Expected: no stuck dragging, no stuck animating, final state remains coherent.
