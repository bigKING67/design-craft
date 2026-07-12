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

**[Evidence: code/CSS + product context] Not production-ready for a calm repeated-use operations app.**  
The sheet moves, but it is not a true direct-manipulation component: it jumps to the pointer, ignores velocity, blocks interruption, animates layout properties, and has no reduced-motion path. The result will likely feel sticky, surprising, and tiring over repeated daily use.

## Prioritized findings

1. **Critical — not actually 1:1 dragging**
   - **[Code]** `sheet.style.top = event.clientY` anchors the sheet’s top edge to the pointer.
   - This ignores where the user grabbed the sheet, so the sheet can jump on first move.
   - `startY` is recorded but unused.

2. **Critical — animations are not interruptible**
   - **[Code]** `if (animating) return;` blocks new gestures during snap animation.
   - A moving sheet should be grabbable mid-flight and redirected from its current visible position.

3. **Critical — release ignores velocity and intent**
   - **[Code]** `nearestSnapPoint(sheet.offsetTop)` chooses only from current position.
   - Flicks should project momentum, then choose collapsed / half / full from the projected endpoint.
   - Without velocity, a quick upward throw and a slow drag to the same point resolve identically.

4. **High — wrong easing for sheet settling**
   - **[Code]** `easing: "ease-in"` starts slow after release and accelerates into the target.
   - That creates a visible seam: the user lets go with speed, then the sheet hesitates.
   - Prefer velocity-aware spring settling; for a calm app, use critically damped or lightly damped motion.

5. **High — layout-position animation is expensive and fragile**
   - **[Code/CSS]** `top`, `offsetTop`, and `transition: all` invite layout work and unintended transitions.
   - Prefer a stable layout position plus `transform: translateY(...)` for drag and snap.

6. **High — CSS conflicts with gesture animation**
   - **[CSS]** `.sheet { transition: all 300ms; }` can animate unrelated property changes, including gesture-driven writes.
   - **[CSS]** `.sheet:active { transform: scale(0.96); }` competes with any future `transform: translateY(...)`.
   - The scale is also heavy for a calm operations surface; it may feel like the whole workspace compresses.

7. **Medium — no pointer capture or drag state**
   - **[Code]** `pointermove` runs without checking an active drag.
   - Missing `setPointerCapture` means tracking can break if the pointer leaves the sheet.
   - Missing pointer-id tracking can mix multiple pointers.

8. **Medium — no bounds, rubber-banding, or snap-state model**
   - **[Code]** No clamp to collapsed/full bounds.
   - No soft resistance past limits.
   - No explicit current state: collapsed / half / full should be a first-class state, not inferred only from pixels.

9. **Medium — reduced motion requirement is unmet**
   - **[Context]** Reduced Motion must preserve state feedback without large travel.
   - Current implementation always performs spatial travel over 480ms.
   - Needs a reduced path: immediate state change or very short opacity/elevation/handle feedback, not large sliding.

10. **Low/medium — animation lifecycle can get stuck**
   - **[Code]** `.finished.then(...)` has no `catch`/`finally`.
   - If the animation is canceled, rejected, or the element is removed, `animating` can remain true.

## Concrete direct-manipulation moves

- On `pointerdown`:
  - Capture pointer.
  - Store `grabOffset = pointerY - currentSheetY`.
  - Cancel or retarget any active animation.
  - Start from the sheet’s current visible transform, not the last logical target.

- On `pointermove`:
  - Only move while dragging the captured pointer.
  - Set `translateY = pointerY - grabOffset`.
  - Apply bounds with soft rubber-band resistance beyond collapsed/full.
  - Update on `requestAnimationFrame` if move events are frequent.

- On `pointerup` / `pointercancel`:
  - Compute release velocity from recent pointer history.
  - Project the resting point using velocity.
  - Choose nearest snap point from projected position, not raw position.
  - Animate to collapsed / half / full with a spring or spring-like curve that accepts initial velocity.
  - Keep state and visual position synchronized when the animation completes.

- For calm operations use:
  - No dramatic scale on the whole sheet.
  - Subtle handle, shadow, elevation, or background-state feedback.
  - Fast response on contact, gentle settle after release.
  - No bounce unless the user clearly flicked with momentum.

- For reduced motion:
  - Preserve collapsed / half / full state changes.
  - Avoid large animated travel.
  - Use short opacity, shadow, border, handle, or label feedback.
  - Consider instant reposition plus a brief non-spatial confirmation pulse.

## Verified / unverified boundaries

**Verified from provided code**
- Uses `top` writes during pointer movement.
- Uses `offsetTop` for snap selection.
- Blocks pointerdown while animating.
- Uses fixed 480ms `ease-in` animation.
- Uses global `transition: all 300ms`.
- Has no visible reduced-motion branch.

**Unverified**
- Actual snap point values.
- Sheet dimensions, scroll containment, and viewport bounds.
- Whether inner sheet content scrolls.
- Keyboard/focus behavior.
- Screen reader state announcement.
- Real frame rate, latency, or device feel.
- Browser/device behavior; no validation was performed.

## Smallest runtime validation plan

1. **Pointer continuity**
   - Drag from top handle, middle, and lower area.
   - Confirm no jump on first move.
   - Confirm the grabbed point stays under the pointer.

2. **Interruption**
   - Release toward half/full, then grab mid-animation.
   - Confirm the sheet follows immediately without waiting.

3. **Snap intent**
   - Slow drag near boundaries.
   - Fast flick upward/downward from the same release point.
   - Confirm velocity changes the chosen state appropriately.

4. **Bounds**
   - Pull beyond full and collapsed.
   - Confirm soft resistance and clean return.

5. **Reduced motion**
   - Enable reduced motion.
   - Trigger collapsed ↔ half ↔ full.
   - Confirm state remains clear without large travel.

6. **Performance smoke test**
   - Record a short interaction trace.
   - Check for layout thrash, long tasks, and dropped frames during drag.


## Output B

**Verdict — Block.**  
[Static evidence] This is not yet a safe gesture sheet: it animates layout `top`, loses 1:1 drag fidelity, cannot be interrupted correctly, ignores release velocity, and has no Reduced Motion path.  
[Product fit] For a calm operations app used repeatedly, the 480ms `ease-in` settle and 4% sheet scale read as heavy and distracting rather than steady.

## Prioritized findings

1. **P0 — Drag is not direct manipulation.**  
   [Static evidence] `startY` is recorded but unused; `pointermove` sets `top = event.clientY`, so the sheet top can jump to the finger instead of preserving the grab offset.  
   [Impact] Users who grab the middle/handle will see the sheet detach and snap.

2. **P0 — Gesture interruption is broken.**  
   [Static evidence] `animating` blocks `pointerdown`, but `pointermove` still writes `top` during animation; WAAPI and inline style can fight.  
   [Impact] A sheet must be re-grabbable mid-flight from its current visual position, not locked until `.finished`.

3. **P0 — Release physics ignore intent.**  
   [Static evidence] Snap target uses `nearestSnapPoint(sheet.offsetTop)` only. No velocity history, projected endpoint, threshold, or flick handling.  
   [Impact] A fast upward flick near the lower snap may collapse/settle incorrectly, making the sheet feel stubborn.

4. **P0 — Layout-property animation creates jank risk.**  
   [Static evidence] Both drag and settle mutate/animate `top`; CSS also declares `transition: all 300ms`.  
   [Impact] Pointer moves can trigger layout and the CSS transition may add lag to every drag frame. Use compositor-friendly transform ownership instead.

5. **P0 — Reduced Motion requirement is unmet.**  
   [Static evidence] No `prefers-reduced-motion` branch.  
   [Impact] Large spatial travel remains mandatory; state feedback is not preserved through non-travel cues.

6. **P1 — Timing/easing is wrong for a high-frequency operations surface.**  
   [Static evidence] `duration: 480`, `easing: "ease-in"`.  
   [Impact] `ease-in` delays response at release; 480ms is likely too cinematic for repeated sheet state changes.

7. **P1 — Pointer lifecycle is incomplete.**  
   [Static evidence] No `setPointerCapture`, `pointercancel`, `lostpointercapture`, `pointerId`, or multi-touch handling.  
   [Impact] Drag can fail when the pointer leaves the sheet, scrolling starts, or a second touch appears.

8. **P1 — Boundaries and state model are underspecified.**  
   [Static evidence] No clamping/rubber-banding, no explicit collapsed/half/full state update, no cancellation behavior.  
   [Impact] The sheet can overshoot, settle ambiguously, or desync visual and logical state.

9. **P1 — Press scale conflicts with sheet movement.**  
   [Static evidence] `.sheet:active { transform: scale(0.96); }` while the component should likely use `transform` for drag.  
   [Impact] Scale and translate need separate layers or a composed transform owner; 0.96 is also strong for a calm utility surface.

## Concrete direct-manipulation moves

- Replace `top` motion with a single `translateY(...)` owner; keep logical snap state separate from visual position.
- On pointer down: read current presentation Y, preserve grab offset, capture the pointer, and start from the current visual value even if settling.
- Add an 8–12px-ish drag intent threshold so taps do not reposition the sheet.
- Track recent `{time, y}` samples and compute release velocity in CSS px/s.
- Choose collapsed/half/full target from a projected endpoint, not just release position.
- Settle with a spring-like curve or tuned drawer easing; default to no bounce for this product, with subtle velocity-aware response only when useful.
- Add soft boundary resistance above full and below collapsed instead of hard jumps.
- Separate layers: outer wrapper owns drag `translateY`; inner content/handle owns any small press affordance.
- Replace `transition: all` with explicit properties and durations.
- Reduced Motion: avoid large animated travel; snap state with brief opacity/color/handle-state feedback, shadow/scrim change, and clear state label/affordance.

## Verified / unverified boundaries

- [Verified statically] `top` is mutated during drag and animated on release.
- [Verified statically] `transition: all`, `ease-in`, fixed 480ms duration, and `:active` scale are present.
- [Verified statically] No Reduced Motion handling appears in the snippet.
- [Verified statically] No pointer capture, velocity sampling, projected snap, or cancellation handling appears in the snippet.
- [Unverified] Actual frame rate, layout cost, scroll interaction, and visual smoothness.
- [Unverified] Real touch feel, 60/120Hz behavior, browser-specific WAAPI/CSS interaction, and accessibility behavior.
- [Unverified] Whether surrounding code clamps snap points, owns state, or provides keyboard/ARIA support.

## Smallest runtime validation plan

1. Verify drag start from handle, middle, and lower sheet body: no jump; grab offset preserved.
2. Drag outside the sheet bounds and release: pointer capture keeps control; `pointercancel` is safe.
3. Flick slowly/quickly between collapsed, half, and full: target follows projected intent, not only final position.
4. Interrupt while settling: re-grab starts from current visual position with no lockout or jump.
5. Toggle Reduced Motion: large travel is removed or minimized while collapsed/half/full feedback remains clear.
6. Inspect one performance trace under representative page load: no repeated layout on pointermove; transform remains the hot-path property.

Process note: assessed using frontend interaction, motion, accessibility, and validation guardrails; no browser or device validation was performed.


## Output C

## Evidence-labeled verdict

**Verdict: Not production-ready for a calm, repeatedly used three-state sheet.**  
**Evidence:** Static code inspection shows broken direct-manipulation mapping, conflicting CSS/JS motion, no active pointer lifecycle, no reduced-motion path, and layout-driven animation that can feel laggy or abrupt.  
**Boundary:** This is a static critique only; no browser, device, or runtime validation was performed.

---

## Prioritized findings

### P0 — Drag can mutate without an active gesture
**Evidence:** `pointermove` always runs `sheet.style.top = ...`; it does not check `dragging`, `pointerId`, or `animating`.  
**Impact:** Hover/move events, stray pointers, or moves after cancellation can reposition the sheet unexpectedly.  
**Fix direction:** Track `dragging`, capture the initiating pointer, ignore all other pointers, and clear state on `pointerup`, `pointercancel`, and lost capture.

### P0 — Finger-to-sheet mapping is wrong
**Evidence:** `startY` is stored but never used; `top` is set directly to `event.clientY`.  
**Impact:** The sheet jumps so its top edge snaps to the pointer, instead of preserving the grab offset. This violates direct manipulation.  
**Fix direction:** On down, record `baseY` and `grabY`; on move, apply `baseY + (event.clientY - grabY)`.

### P0 — Reduced Motion requirement is unmet
**Evidence:** Every release animates spatial travel for `480ms`; CSS also scales the sheet on active press.  
**Impact:** Users requesting reduced motion still get large movement and scale changes.  
**Fix direction:** Under reduced motion, avoid long travel: snap state immediately or use a very short non-spatial cue such as handle color, elevation, label update, or subtle opacity/state indicator.

### P1 — CSS transition conflicts with gesture and WAAPI animation
**Evidence:** `.sheet { transition: all 300ms; }` applies during every `top` write and can also conflict with `sheet.animate(...)`.  
**Impact:** Drag may lag behind the pointer; unrelated properties may animate accidentally; motion becomes hard to reason about.  
**Fix direction:** Remove `transition: all`; only transition explicit non-gesture properties, and disable transitions while dragging.

### P1 — Animating `top` causes layout work
**Evidence:** Both drag and snap manipulate `top`; `offsetTop` is read after layout-affecting writes.  
**Impact:** Repeated layout/reflow risk, especially during pointermove.  
**Fix direction:** Use `transform: translateY(...)` for the moving layer, schedule writes through `requestAnimationFrame`, and keep layout reads outside hot paths.

### P1 — Snap behavior ignores velocity, direction, and hysteresis
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` appears distance-only.  
**Impact:** A purposeful upward fling may collapse back if it ends near the prior state; tiny accidental moves may change state.  
**Fix direction:** Use distance plus velocity/direction thresholds, minimum drag distance, and hysteresis around collapsed/half/full states.

### P1 — Animation feel is mismatched to product tone
**Evidence:** `duration: 480` and `easing: "ease-in"` means the sheet accelerates into its destination.  
**Impact:** Feels heavy, late, and potentially abrupt at rest; repeated daily use will feel tiring.  
**Fix direction:** Prefer shorter distance-scaled timing, e.g. ~180–300ms, with ease-out or spring-like settling without bounce.

### P1 — Interaction cannot be interrupted cleanly
**Evidence:** `if (animating) return` blocks new starts; the created animation is not stored or canceled.  
**Impact:** If the user changes intent mid-snap, the UI ignores them. If animation is canceled externally, `finished.then(...)` may not restore state.  
**Fix direction:** Keep the active animation handle, cancel/commit it on new pointerdown, and use `finally`/cancel handling to clear locks.

### P2 — `fill: "forwards"` can leave stale underlying state
**Evidence:** The animation fills visually, but the final `style.top` is not explicitly committed after finish.  
**Impact:** Future reads/writes may start from stale style state or conflict with later transitions.  
**Fix direction:** On finish, set the canonical state position in style/state, then cancel or replace the animation effect.

### P2 — Bounds and container coordinates are unspecified
**Evidence:** `event.clientY` is viewport-relative; no clamp is visible.  
**Impact:** The sheet can be dragged outside intended collapsed/full limits, especially inside nested containers, resized viewports, or mobile browser chrome changes.  
**Fix direction:** Convert pointer coordinates into the sheet container’s coordinate space and clamp between full and collapsed offsets.

### P2 — Press scale harms calm direct manipulation
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** Scaling the whole sheet can make content pulse, shift hit targets, and conflict with transform-based positioning.  
**Fix direction:** Keep the sheet stable; apply small feedback to the handle only, or use color/elevation changes.

---

## Concrete direct-manipulation moves

1. Model explicit states: `collapsed`, `half`, `full`, plus current `y`.
2. On `pointerdown`: cancel any snap animation, capture pointer, record `baseY`, `startClientY`, and current state.
3. On `pointermove`: if active pointer, compute `nextY = clamp(baseY + deltaY)`.
4. Apply movement with `transform: translateY(...)`, not `top`.
5. Add soft resistance only beyond bounds, not inside normal state range.
6. On release: choose target using position + velocity + hysteresis.
7. Snap with distance-scaled ease-out motion; no bounce for this product tone.
8. Under reduced motion: commit target quickly and provide non-spatial state feedback.
9. Keep active state feedback localized to the drag handle, not the whole sheet.
10. Ensure `pointercancel` and lost capture restore or settle to the nearest valid state.

---

## Verified / unverified boundaries

**Verified by static inspection:**
- `startY` is unused.
- `pointermove` has no active-drag guard.
- `top` is used for gesture and animation.
- CSS uses `transition: all`.
- CSS scales the whole active sheet.
- No visible reduced-motion branch.
- No visible pointer capture/cancel handling.
- No visible velocity, hysteresis, or bounds logic.

**Unverified:**
- Actual `nearestSnapPoint` behavior.
- Actual DOM positioning context.
- Real frame rate or input latency.
- Browser/device behavior.
- Accessibility state, keyboard support, focus handling, and ARIA outside this snippet.
- Whether additional code elsewhere mitigates these issues.

---

## Smallest runtime validation plan

1. Instrument pointer lifecycle: down/move/up/cancel, active pointer id, current state, target state.
2. Test three gestures only: slow drag, short accidental drag, fast fling.
3. Check interruption: start a snap, then drag again before it finishes.
4. Check bounds: drag past full and collapsed limits.
5. Check reduced motion: confirm no long spatial snap and that state feedback remains visible.
6. Measure one hot path: pointermove should not force layout every frame.
7. Verify state after animation: visual position and canonical state must match.
