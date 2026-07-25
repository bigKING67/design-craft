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

**Evidence-labeled verdict: Block for production gesture feel.**  
From the static code, the sheet is not a direct-manipulation surface yet: it moves by layout `top`, lags via `transition: all`, ignores grab offset and velocity, locks/overrides interaction during animation, and has no Reduced Motion branch despite large spatial travel across collapsed/half/full states.

## Prioritized findings

1. **P0 — Drag is not actually 1:1.**  
   **Evidence:** `pointermove` sets `sheet.style.top = event.clientY`, while `.sheet { transition: all 300ms; }` means every drag update may be animated instead of attached to the pointer.  
   **Impact:** The sheet will feel delayed, slippery, and tiring for repeated operations use.

2. **P0 — Missing drag state and pointer capture.**  
   **Evidence:** `pointermove` runs regardless of whether a valid drag began; `pointerdown` only stores `startY`, which is never used. No `setPointerCapture`, `pointercancel`, or lost-capture handling.  
   **Impact:** Accidental pointer movement can reposition the sheet; tracking may break if the pointer leaves the element.

3. **P0 — Uses layout motion on the hot path.**  
   **Evidence:** Both drag and settle animate `top`; `pointerup` reads `sheet.offsetTop`.  
   **Impact:** Layout/reflow risk during a high-frequency gesture, especially near a large operations table.

4. **P1 — Release motion feels backwards and too slow.**  
   **Evidence:** `{ duration: 480, easing: "ease-in" }`.  
   **Impact:** `ease-in` delays the response immediately after release; 480ms is heavy for a repeatedly used sheet.

5. **P1 — Non-interruptible animation model.**  
   **Evidence:** `animating` blocks `pointerdown`, but `pointermove` can still mutate `top`; `.finished.then()` is the only unlock path.  
   **Impact:** Users cannot grab the sheet mid-settle; state can desync if animation is canceled, interrupted, or errors.

6. **P1 — Snap selection ignores velocity and intent.**  
   **Evidence:** `nearestSnapPoint(sheet.offsetTop)` uses current layout position only.  
   **Impact:** A deliberate flick toward full/half/collapsed may snap opposite to perceived intent.

7. **P1 — No Reduced Motion behavior.**  
   **Evidence:** No `prefers-reduced-motion` check or alternate settle path.  
   **Impact:** Large spatial travel remains, violating the requirement to preserve feedback without large movement.

8. **P2 — Press feedback is too blunt for a sheet.**  
   **Evidence:** `.sheet:active { transform: scale(0.96); }`.  
   **Impact:** Scaling an entire data-heavy panel can make content feel unstable and may conflict with future transform-based drag.

## Concrete direct-manipulation moves

1. Replace `top` dragging with a single transform owner: `translateY(currentY)` on the sheet or an inner motion wrapper.

2. Remove `transition: all`; scope transitions only to intentional non-gesture properties, e.g. `transform`, `opacity`, or state affordance colors.

3. Track gesture lifecycle explicitly: `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, and `grabOffset`.

4. On pointer down, capture the pointer after intent threshold and preserve offset:  
   `nextY = clamp(startSheetY + event.clientY - startPointerY, minY, maxY)`.

5. Add `touch-action: none` or a narrower `touch-action` policy on the drag handle so browser scrolling does not compete with the sheet gesture.

6. Maintain a short position/time history and compute release velocity in CSS px/s.

7. Separate target selection from settle physics:  
   - conservative rule: snap to nearest collapsed/half/full from current presentation value;  
   - optional momentum rule: choose from a bounded projected endpoint when product behavior allows flick targeting.

8. Use an interruptible settle animation that starts from the current presentation value and can be retargeted mid-flight; prefer a critically damped or lightly damped spring-like curve over fixed `ease-in`.

9. Reduced Motion: avoid large animated travel; jump or very-short-settle to the target while preserving state feedback through handle color, label/status change, subtle opacity, or a short non-spatial transform.

10. Replace full-sheet `scale(0.96)` with a calmer handle affordance: grip highlight, slight handle scale, shadow/color change, or pressed handle translation only.

## Verified / unverified boundaries

**Verified from static evidence:**  
- Layout property `top` is used for drag and settle.  
- `transition: all` applies globally to the sheet.  
- No Reduced Motion branch is present.  
- No pointer capture/cancel handling is present.  
- `startY` is stored but unused.  
- Snap target is chosen from `offsetTop`, not velocity.

**Not verified:**  
- Actual frame rate, jank, or input latency.  
- Whether CSS positioning makes `top` visually effective in the real layout.  
- Real touch feel on trackpad, mouse, or mobile hardware.  
- Whether surrounding app code clamps snap points or handles state elsewhere.  
- Assistive tech behavior, focus management, and keyboard equivalents.

## Smallest runtime validation plan

1. **Pointer lifecycle smoke:** drag from handle, leave sheet bounds, release, cancel, and re-grab during settle. Confirm no jumps.

2. **Motion feel check:** verify 1:1 tracking, grab-offset preservation, and snap to collapsed/half/full from slow drags and quick flicks.

3. **Performance check:** record a short trace while the 10,000-row table is present; confirm no layout-heavy work on every pointer move.

4. **Reduced Motion check:** enable `prefers-reduced-motion`; confirm large travel is removed or shortened while state feedback remains visible.

5. **Accessibility check:** confirm keyboard path to collapsed/half/full states, visible focus, named controls, and no focus loss during sheet state changes.


## Output B

## Evidence-labeled verdict

**Verdict: not production-ready for a calm repeated-use operations sheet.**  
From the static code, the sheet is neither truly direct-manipulated nor interruptible. It uses layout-position animation, fixed timing, input lockout, and no reduced-motion path. The likely feel is jumpy, lagged, and occasionally stuck or misleading.

---

## Prioritized findings

### P0 — Drag is not actually 1:1 direct manipulation
**Evidence:** `pointermove` sets `sheet.style.top = event.clientY`.  
Problems:
- Ignores where inside the sheet the user grabbed it, so the sheet can jump to the pointer.
- `startY` is recorded but unused.
- No active-drag guard, so any pointer move over the sheet can move it.
- No `setPointerCapture`, so tracking can break when the pointer leaves the sheet.

**Impact:** The sheet will not feel attached to the hand/mouse.

---

### P0 — Motion is non-interruptible
**Evidence:** `if (animating) return;` on `pointerdown`.  
Problem: users cannot grab the sheet mid-flight and redirect it.

**Impact:** This is especially hostile in repeated operations work, where users expect to correct gestures immediately.

---

### P0 — Uses layout properties on the hot path
**Evidence:** `style.top`, `offsetTop`, and WAAPI animation of `top`.  
Problems:
- `top` changes can trigger layout.
- `offsetTop` reads can force layout.
- This is risky for a large operations UI with tables/drawers behind it.

**Impact:** Higher chance of jank under real data load. Use compositor-friendly `transform: translateY(...)` instead.

---

### P1 — Release animation has the wrong physical feel
**Evidence:** `{ duration: 480, easing: "ease-in" }`.  
Problems:
- `ease-in` starts slowly after release, creating a visible seam from finger velocity to animation.
- It accelerates into the snap point, which feels like the sheet is pulled away rather than settling.
- Fixed 480ms ignores distance and release speed.

**Impact:** The sheet will feel scripted, not responsive.

---

### P1 — Snap choice ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)`.  
Problem: target is based only on current position, not release velocity or projected endpoint.

**Impact:** A fast flick toward full/closed may snap back to the nearest current state, violating user intent.

---

### P1 — CSS transition conflicts with gesture control
**Evidence:** `.sheet { transition: all 300ms; }`.  
Problems:
- `transition: all` can animate unintended properties.
- During drag, `top` changes may be transitioned, causing lag behind the pointer.
- It can conflict with WAAPI animation and produce unclear ownership of motion.

**Impact:** Reduces precision and predictability.

---

### P1 — Reduced Motion requirement is unmet
**Evidence:** No `prefers-reduced-motion` branch.  
Problem: collapsed/half/full changes always involve large spatial travel.

**Impact:** Fails the stated product requirement. Reduced Motion should preserve state feedback without large animated movement.

---

### P2 — Whole-sheet active scaling is inappropriate for dense ops UI
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
Problems:
- Scales dense content, text, controls, and hit targets.
- Can make the panel feel unstable while the user is trying to operate it.
- If transform-based dragging is later added, this conflicts unless transforms are composed carefully.

**Impact:** Decorative feedback competes with task precision.

---

### P2 — Final animation state may be fragile
**Evidence:** WAAPI uses `fill: "forwards"` but does not commit the final `top` to the element style.  
Problem: visual state and layout/style state can diverge after animation.

**Impact:** Later reads, snaps, or re-renders may start from stale state.

---

## Concrete direct-manipulation moves

1. **Track an explicit drag session**
   - On `pointerdown`: store pointer id, current sheet Y, grab offset, timestamped position history.
   - Call `setPointerCapture(event.pointerId)`.
   - Ignore `pointermove` unless dragging that pointer.

2. **Use transform, not top**
   - Maintain logical `y`.
   - Apply `transform: translate3d(0, ${y}px, 0)`.
   - Avoid `offsetTop` in the gesture loop.

3. **Disable generic transitions during drag**
   - Remove `transition: all`.
   - Use specific transitions only for non-gesture properties.
   - During active drag, no transition on the positional transform.

4. **Make release velocity-aware**
   - Estimate release velocity from recent pointer samples.
   - Project the likely endpoint.
   - Choose collapsed/half/full from the projected endpoint, not raw current position.

5. **Use a spring-like settle**
   - Start from the current presented Y.
   - Pass release velocity into the settle animation.
   - Prefer critically damped or lightly damped motion; avoid bouncy motion for calm operations unless tied to a deliberate flick.

6. **Allow interruption**
   - On pointerdown during settle: cancel current animation, read current visual Y, begin drag from there.
   - Do not block input with `animating`.

7. **Add boundary resistance**
   - Clamp hard only at final state.
   - While dragging beyond min/max, apply progressive rubber-band resistance.

8. **Replace whole-sheet scale feedback**
   - Keep the sheet stable.
   - Use handle highlight, shadow change, subtle elevation, or cursor state to indicate grab.
   - Avoid shrinking operational content.

9. **Reduced Motion behavior**
   - Under reduced motion: avoid large animated travel.
   - Snap state quickly or nearly instantly.
   - Preserve feedback via handle color, state label, opacity/elevation change, and clear collapsed/half/full affordance.
   - Avoid overshoot, bounce, and long spatial transitions.

---

## Verified / unverified boundaries

**Verified from static code:**
- Uses `top` for drag and animation.
- Uses `offsetTop` for snap calculation.
- Uses fixed `480ms ease-in`.
- Blocks pointerdown while `animating`.
- Has global `transition: all 300ms`.
- Has whole-sheet `:active` scale.
- Has no visible reduced-motion branch.
- Has no visible pointer capture, velocity tracking, keyboard handling, or snap-state semantics.

**Not verified:**
- Actual frame rate or jank under load.
- Browser-specific WAAPI behavior in the target environment.
- Real snap-point values.
- Whether other code adds keyboard support, ARIA state, focus management, or reduced-motion handling.
- Whether the sheet lives over a virtualized table or other expensive layout.
- Touch-device behavior, pointer cancellation behavior, or scroll/drag conflict behavior.

---

## Smallest runtime validation plan

1. **Directness check**
   - Grab sheet from top, middle, and near edge.
   - Confirm no jump on pointerdown.
   - Confirm sheet remains under pointer during drag.

2. **Interruption check**
   - Flick sheet toward full.
   - Grab it mid-animation and reverse direction.
   - Expected: no lockout, no jump, no velocity break.

3. **Snap-intent check**
   - Slowly drag near half.
   - Fast flick from the same position toward full/collapsed.
   - Expected: target follows projected intent, not just nearest current position.

4. **Reduced Motion check**
   - Enable reduced motion.
   - Change between collapsed, half, and full.
   - Expected: minimal spatial animation, clear state feedback remains.

5. **Performance smoke**
   - Test with the largest realistic table/data state.
   - Drag continuously for several seconds.
   - Expected: no visible layout hitching, no delayed trailing motion.

6. **Input/accessibility smoke**
   - Operate with mouse, touch/trackpad pointer, and keyboard.
   - Confirm focus visibility, escape/cancel behavior, and announced state changes.


## Output C

## Verdict

**Not production-ready for a calm, repeated-use operations sheet.**  
**Evidence:** the implementation animates and drags `top`, combines WAAPI with `transition: all`, lacks pointer capture / drag state / reduced-motion handling, and uses a long `ease-in` settle. The result is likely to feel laggy, imprecise, and hard to interrupt.

---

## Prioritized findings

### P0 — Drag is not actually gated to an active gesture
**Evidence:** `pointermove` always runs:

```js
sheet.addEventListener("pointermove", (event) => {
  sheet.style.top = `${event.clientY}px`;
});
```

There is no `isDragging`, no `pointerId`, and no `setPointerCapture`. Any pointer move over the sheet can move it, including after `pointerdown` was ignored because `animating` was true.

**Impact:** accidental jumps, broken multi-pointer behavior, lost drags when the pointer leaves the sheet, and poor trust for repeated operations use.

---

### P0 — Motion is layout-driven instead of transform-driven
**Evidence:** drag and animation mutate `top`; snap reads `sheet.offsetTop`.

```js
sheet.style.top = `${event.clientY}px`;
nearestSnapPoint(sheet.offsetTop);
sheet.animate([{ top: ... }, { top: ... }])
```

**Impact:** `top` changes can trigger layout; `offsetTop` can force layout reads. This is risky for a dense operations app, especially near a large table or drawer.

---

### P0 — CSS and JS animation conflict
**Evidence:**

```css
.sheet { transition: all 300ms; }
```

while JS also updates `top` continuously and uses `sheet.animate(...)`.

**Impact:** direct manipulation may lag behind the pointer because `top` changes are also transitioned. `transition: all` can animate unrelated properties and create surprising motion when state/classes change.

---

### P1 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` branch; snap always uses:

```js
{ duration: 480, easing: "ease-in" }
```

**Impact:** users requesting reduced motion still get large spatial travel. The product requirement says state feedback must remain without large travel.

---

### P1 — Snap behavior ignores velocity, direction, and state intent
**Evidence:** target is based only on current `offsetTop`:

```js
const target = nearestSnapPoint(sheet.offsetTop);
```

**Impact:** a fast intentional fling toward full/closed can be misread if release position is near another snap. Calm does not mean inert; the sheet should respect the user’s drag momentum and direction.

---

### P1 — Animation is not safely interruptible
**Evidence:** `animating = true` blocks `pointerdown`, but `pointermove` still mutates the sheet. The `.finished` promise has no cancellation/error handling.

```js
).finished.then(() => {
  animating = false;
});
```

**Impact:** if the animation is canceled/replaced, the flag can get stuck. Users may be unable to re-grab the sheet during a settle, which makes the component feel non-physical.

---

### P2 — Easing and duration feel wrong for a sheet settle
**Evidence:** `duration: 480`, `easing: "ease-in"`.

**Impact:** `ease-in` starts slowly and accelerates into the destination, which can feel like the sheet is pulled away from the user at the end. A sheet settle usually needs quick response and deceleration into rest.

---

### P2 — `:active` scale harms precision
**Evidence:**

```css
.sheet:active { transform: scale(0.96); }
```

**Impact:** scaling the whole panel during drag compresses content, changes perceived hit targets, and conflicts with transform-based sheet movement. For an operations app, this is decorative feedback at the cost of control.

---

### P2 — No clamping or bounds protection shown
**Evidence:** `sheet.style.top = event.clientY`.

**Impact:** the sheet can be dragged outside valid collapsed/half/full ranges unless hidden elsewhere. Direct manipulation should expose limits clearly, not allow arbitrary sheet placement.

---

## Concrete direct-manipulation moves

1. **Use transform, not `top`.**  
   Keep the sheet positioned by layout once, then move it with:

   ```css
   transform: translate3d(0, var(--sheet-y), 0);
   ```

2. **Remove `transition: all`.**  
   Use a narrow transition only when settling:

   ```css
   .sheet {
     transition-property: transform;
     transition-duration: var(--duration-panel);
     transition-timing-function: var(--ease-responsive);
   }

   .sheet[data-dragging="true"] {
     transition: none;
   }
   ```

3. **Track an actual gesture.**  
   On `pointerdown`: store `pointerId`, `startY`, `startOffset`, set `isDragging = true`, and call `setPointerCapture`.

4. **Clamp during drag.**  
   Compute:

   ```js
   nextOffset = clamp(startOffset + event.clientY - startY, fullY, collapsedY);
   ```

   Apply via transform/CSS variable, ideally batched with `requestAnimationFrame`.

5. **Use velocity-aware snap selection.**  
   On release, choose collapsed/half/full using:
   - current offset,
   - drag direction,
   - release velocity,
   - hysteresis around the current state.

6. **Make settle interruptible.**  
   A new pointerdown should cancel the current animation and continue from the visual position, not wait for a flag.

7. **Replace whole-sheet scale with local feedback.**  
   Prefer handle affordance, shadow density, header compression, or subtle opacity/border changes. Do not scale the full content surface.

8. **Add reduced-motion behavior.**  
   Under `prefers-reduced-motion: reduce`, avoid long travel:
   - snap immediately or within ~80ms,
   - keep visible state feedback through handle, shadow, label, or boundary change,
   - avoid large animated spatial distance.

9. **Add touch behavior explicitly.**  
   Use an appropriate `touch-action` on the drag handle/sheet so vertical dragging does not fight page scroll.

---

## Verified / unverified boundaries

### Verified from static code
- Uses `top` for drag and animation.
- Reads `offsetTop` for snap.
- Has `transition: all 300ms`.
- Has `:active { transform: scale(0.96) }`.
- Has no visible reduced-motion branch.
- Has no visible `isDragging`, `pointerId`, pointer capture, clamping, velocity, or cancellation handling.

### Not verified
- Real snap-point math.
- Actual DOM positioning and containment.
- Browser-specific WAAPI behavior.
- Performance under the real 10,000-row table.
- Touchpad/touch/stylus behavior.
- Screen reader, keyboard, and focus behavior.
- Visual polish on real devices.

---

## Smallest runtime validation plan

1. **Pointer correctness:** drag from collapsed → half → full; verify the sheet moves only after active pointerdown, follows the pointer, clamps to valid bounds, and still works if the pointer leaves the sheet.

2. **Interruptibility:** release toward a snap, then immediately re-grab mid-animation; verify it continues from the current visual position without jumping or locking.

3. **Reduced Motion:** enable reduced motion; verify state changes still show feedback but avoid long spatial travel.

4. **Performance smoke:** record a drag near the real dense table; verify no repeated layout-heavy work per frame and no visible hitching.

5. **State persistence:** after each snap, verify the durable state is exactly collapsed, half, or full, not just a visually filled animation state.
