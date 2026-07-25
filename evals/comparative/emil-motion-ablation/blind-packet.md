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
**Evidence:** The implementation drives motion with `top`, `transition: all`, non-interruptible WAAPI animation, no reduced-motion branch, no drag state guard, no pointer capture/cancel handling, and no stable collapsed/half/full state model. It will feel laggy, jumpy, and fragile under repeated use.

---

## Prioritized findings

### P0 — Direct manipulation is broken
**Evidence:** `pointermove` always runs and sets `sheet.style.top = event.clientY`, even without an active drag. `startY` is recorded but never used.  
**Impact:** The sheet can jump to the pointer’s absolute viewport Y instead of preserving the grab offset. Any pointer movement over the sheet may move it.

### P0 — Animation state can desync from visual state
**Evidence:** `sheet.animate(..., { fill: "forwards" })` visually holds the end frame, but the underlying `style.top` may remain stale. Later `sheet.offsetTop` can read layout state, not the visually filled animation state.  
**Impact:** Repeated drags can snap from incorrect positions or appear to “teleport.”

### P0 — Reduced Motion requirement is unmet
**Evidence:** There is no `prefers-reduced-motion` branch. Snap animation always travels over `480ms`.  
**Impact:** Users who request reduced motion still get large spatial travel. The product requirement says state feedback must remain without large travel.

### P1 — Uses layout-position animation instead of composited motion
**Evidence:** Drag and snap both animate `top`; `pointermove` writes layout-affecting style every event.  
**Impact:** This risks layout/reflow cost, input lag, and poor table/workspace performance. A sheet should generally move with `transform: translateY(...)`.

### P1 — CSS conflicts with JS motion
**Evidence:** `.sheet { transition: all 300ms; }` applies to every changed property, including `top` and potentially `transform`.  
**Impact:** Pointer tracking may lag because every `top` update can transition. `transition: all` also creates accidental animations for unrelated style changes.

### P1 — Snap motion feels wrong for direct manipulation
**Evidence:** Snap uses `duration: 480` and `easing: "ease-in"`.  
**Impact:** `ease-in` starts slowly and accelerates toward the end, which feels like the sheet is escaping the user. Snap-to-state motion should feel responsive, interruptible, and settle naturally.

### P1 — No interruption or cancellation model
**Evidence:** `animating` blocks `pointerdown`, but `pointermove` is not guarded and no active animation handle is cancelled on a new drag.  
**Impact:** User input can conflict with in-flight animation. A direct manipulation surface should let the user grab and redirect the sheet.

### P1 — Pointer lifecycle is incomplete
**Evidence:** No `setPointerCapture`, `pointercancel`, `lostpointercapture`, or drag cleanup path.  
**Impact:** If the pointer leaves the sheet, the gesture is interrupted, or the browser cancels input, the component can remain in a bad state.

### P2 — No velocity, hysteresis, or intent threshold
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only considers final position.  
**Impact:** A quick upward or downward fling will not behave naturally. Small accidental movement near a midpoint may snap unpredictably.

### P2 — Active scale harms operational clarity
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** Scaling the whole sheet during drag reduces text stability and can conflict with translate-based motion. For dense operations UI, feedback should be subtle and preserve readability.

### P2 — Scroll-versus-drag conflict is unresolved
**Evidence:** The snippet does not distinguish dragging the sheet handle from scrolling sheet content.  
**Impact:** Users may accidentally move the sheet when trying to scroll content, or vice versa.

---

## Concrete direct-manipulation moves

1. **Use a real drag state**
   - Track `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, and current sheet position.
   - Ignore `pointermove` unless dragging and the pointer id matches.

2. **Capture the pointer**
   - On valid handle `pointerdown`, call `setPointerCapture(event.pointerId)`.
   - Clean up on `pointerup`, `pointercancel`, and `lostpointercapture`.

3. **Move with transform, not top**
   - Store sheet state as a numeric `translateY`.
   - Apply `transform: translate3d(0, var-or-value, 0)`.
   - Avoid layout reads like `offsetTop` during drag.

4. **Preserve grab offset**
   - Compute `nextY = startSheetY + (event.clientY - startPointerY)`.
   - Clamp or apply resistance beyond collapsed/full bounds.

5. **Make snap state canonical**
   - Maintain explicit states: `collapsed`, `half`, `full`.
   - After animation, commit the final numeric position and state instead of relying on `fill: "forwards"`.

6. **Use position + velocity for snap**
   - Choose target by projected position, velocity, and thresholds.
   - Add hysteresis so tiny moves near a boundary do not flip states unexpectedly.

7. **Make snap animation interruptible**
   - Keep the animation handle.
   - On new drag, cancel the running animation and continue from the current visual position.

8. **Replace `transition: all`**
   - Use narrow transitions only for intentional properties.
   - Example intent: transform duration/easing only during settle, not while dragging.

9. **Remove full-sheet active scaling**
   - Prefer handle affordance, shadow/elevation shift, or small grip highlight.
   - If scale is used, apply it to the handle only, not the readable content panel.

10. **Reduced Motion behavior**
   - For reduced motion, shorten or remove spatial travel.
   - Snap immediately or with a very short fade/outline/state change.
   - Preserve state feedback through label, handle state, shadow, border, or status text.

11. **Separate drag handle from content scroll**
   - Start sheet drag from the handle or a defined drag zone.
   - Let inner content scroll normally.
   - Use `touch-action` deliberately, not globally by accident.

---

## Verified / unverified boundaries

**Verified from static code:**
- Motion is driven by `top`.
- `startY` is unused.
- `pointermove` lacks a dragging guard.
- WAAPI uses `fill: "forwards"`.
- CSS uses `transition: all`.
- Active state scales the sheet.
- No reduced-motion branch is present in the snippet.
- No pointer capture/cancel handling is present in the snippet.

**Not verified from static code:**
- Actual snap-point values.
- Whether the listener is attached to the full sheet or only a handle.
- Whether surrounding code provides keyboard support, ARIA state, focus management, or scroll locking.
- Real device performance.
- Browser-specific WAAPI behavior in the deployed environment.
- Interaction with the full 10,000-row table or edit drawer.

---

## Smallest runtime validation plan

1. **Keyboard-free pointer smoke**
   - Drag from collapsed → half → full and back.
   - Confirm no jump on initial grab and no movement before an active drag.

2. **Interruption test**
   - Start a snap animation, grab mid-animation, reverse direction.
   - Expected: animation cancels cleanly and follows the pointer.

3. **State consistency test**
   - Complete several snap cycles.
   - Confirm visual position, internal state, and next drag start position all match.

4. **Reduced Motion test**
   - Enable reduced motion.
   - Confirm state changes remain clear without large spatial travel.

5. **Performance check**
   - Record a short drag interaction.
   - Expected: transform-only updates, no repeated layout thrash, no visible input lag.

6. **Scroll conflict check**
   - Scroll content inside the sheet and drag the handle.
   - Expected: content scroll and sheet drag do not steal from each other.


## Output B

## Evidence-labeled verdict

**Verdict: Block for production gesture motion.**  
[E: code] The sheet is moved and animated with `top`, `offsetTop`, `transition: all`, fixed `480ms ease-in`, and an `animating` input lock.  
[E: product] This is a repeated-use operations surface with collapsed / half / full states and a Reduced Motion requirement.  
[Assessment] The implementation will likely feel laggy, jumpy, non-interruptible, and expensive under table/editor load; it also lacks a reduced-motion contract.

## Prioritized findings

### P0 — Direct manipulation is not actually 1:1
- [E: code] `pointermove` sets `sheet.style.top = event.clientY` regardless of whether a drag is active.
- [E: code] `startY` is captured but never used, so grab offset is not preserved.
- [E: code] `event.clientY` is viewport-relative, while `top` is relative to the positioned containing block.
- [Impact] The sheet can jump under the pointer, move without an intentional drag, and snap from the wrong coordinate space.
- [Fix] Track `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, and use `current = startSheetY + deltaY`, clamped to valid sheet bounds.

### P0 — CSS transition fights the drag
- [E: code] `.sheet { transition: all 300ms; }`
- [E: code] Drag updates `top` on every `pointermove`.
- [Impact] Each drag frame may be eased by CSS instead of staying attached to the pointer; `all` also risks animating unrelated properties.
- [Fix] Disable settle transitions while dragging; animate only explicit properties. Prefer `transform: translateY(...)` for drag and settle.

### P0 — Non-interruptible settle breaks gesture feel
- [E: code] `if (animating) return` blocks new drags while the settle animation is running.
- [E: code] The animation starts from `sheet.offsetTop`, not necessarily the current presented visual value if interrupted.
- [Impact] Users cannot grab the sheet mid-flight; repeated operators will feel the UI ignoring them.
- [Fix] Allow interruption: cancel/retarget the current animation from the current visual position and hand off measured release velocity.

### P0 — Reduced Motion requirement is unmet
- [E: code] No `prefers-reduced-motion` branch.
- [E: product] Reduced Motion must preserve state feedback without large spatial travel.
- [Impact] The current implementation still performs large `top` travel and a 480ms spatial animation.
- [Fix] In reduced motion, avoid long sheet travel where possible: snap state immediately or use a very short opacity/border/handle/status change, while keeping collapsed / half / full state clear.

### P1 — Layout-property animation is a performance risk
- [E: code] `sheet.style.top`, `sheet.offsetTop`, and WAAPI `{ top: ... }`.
- [Impact] `top` mutation and `offsetTop` reads can trigger layout work; this is risky in a dense operations app with large tables and drawers.
- [Fix] Keep the sheet’s logical snap state in JS, but render movement through `transform: translate3d(0, y, 0)`.

### P1 — Timing/easing is wrong for a grabbed object
- [E: code] `{ duration: 480, easing: "ease-in" }`.
- [Impact] `ease-in` delays the first visible response after release; fixed duration ignores drag distance and velocity.
- [Fix] Use a critically damped or near-critically damped spring-like settle, or a shorter distance-aware `ease-out`/drawer curve. Preserve velocity on release.

### P1 — Snap selection ignores velocity and boundaries
- [E: code] `nearestSnapPoint(sheet.offsetTop)` uses only release position.
- [Impact] A fast flick may choose the “nearest” state instead of the intended next state.
- [Fix] Measure recent pointer samples in CSS px/s; compute a bounded projected endpoint; choose collapsed / half / full from that endpoint only if momentum targeting is desired, otherwise keep nearest-position but still hand off velocity to the settle.

### P1 — Pointer lifecycle is incomplete
- [E: code] No `setPointerCapture`, `pointercancel`, `lostpointercapture`, pointer-id filtering, or intent threshold.
- [Impact] The sheet can lose tracking when the pointer leaves the element; scroll/tap conflicts are likely.
- [Fix] Capture the pointer after an 8–12px vertical intent threshold, ignore secondary pointers, and clean up on cancel/lost capture.

### P2 — Press feedback is applied to the wrong object
- [E: code] `.sheet:active { transform: scale(0.96); }`
- [Impact] Scaling the entire sheet during drag feels like the panel is shrinking, not being grabbed. It also conflicts with the recommended `transform`-based translate unless composed carefully.
- [Fix] Put press feedback on the drag handle or use separate wrapper layers: outer wrapper owns `translateY`, inner handle owns subtle press feedback.

### P2 — State and animation completion are fragile
- [E: code] `.finished.then(...)` has no cancellation/error path.
- [E: code] `fill: "forwards"` holds the animation result but does not clearly commit the final logical state.
- [Impact] A canceled animation can leave `animating` stuck or visual and logical positions mismatched.
- [Fix] Commit the final snap state explicitly, clear/cancel animations safely, and keep DOM state attributes such as `data-state="half"` in sync.

## Concrete direct-manipulation moves

1. **Use a single position model**
   - Store snap points as CSS-pixel Y values or percentages resolved once per layout.
   - Render with `transform: translateY(var(--sheet-y))`, not `top`.

2. **Separate drag, settle, and state**
   - `dragging`: no transition, pointer-owned position.
   - `settling`: spring/WAAPI transform animation from current visual value.
   - `settled`: committed `collapsed | half | full` state.

3. **Preserve grab offset**
   - On pointerdown: record `startPointerY` and current sheet Y.
   - On move: `nextY = clamp(startSheetY + event.clientY - startPointerY, minY, maxY)`.

4. **Make release physical but bounded**
   - Keep the last few pointer samples.
   - Calculate release velocity in CSS px/s.
   - Use either nearest snap from current position or an authorized projected endpoint; clamp to collapsed / half / full.

5. **Make the sheet interruptible**
   - If a new drag starts during settle, cancel the running animation and begin from the current visual transform, not the old target.

6. **Replace broad CSS**
   - Before: `transition: all 300ms`.
   - After: explicit transition only for non-gesture visual feedback, e.g. `box-shadow`, `background-color`, or handle affordance.
   - Do not transition drag position during pointer tracking.

7. **Reduced Motion contract**
   - Normal: transform-based settle with velocity-aware response.
   - Reduced: no elastic travel, no long glide; snap quickly and confirm state through handle position, label, shadow/border, or short color/opacity feedback.

8. **Accessible state parity**
   - Provide keyboard controls for collapsed / half / full.
   - Expose current state textually.
   - Keep focus visible and do not rely on `:active` motion as the only feedback.

## Verified / unverified boundaries

- **Verified from static code:** layout-property animation, broad transition, missing reduced-motion branch, missing pointer capture/cancel handling, unused `startY`, fixed `ease-in` settle, input lock while animating.
- **Inferred risk, not runtime-proven:** jank severity, exact jump distance, whether CSS transition visibly lags pointer tracking, and whether `offsetTop` mismatches the visual position in the target browser.
- **Not validated:** real browser behavior, touch-device feel, 60Hz/120Hz smoothness, reduced-motion OS setting behavior, screen-reader output, keyboard flow, or performance under the 10,000-row table load.

## Smallest runtime validation plan

1. **Desktop pointer smoke**
   - Drag from handle and sheet body.
   - Verify no jump on pointerdown, no movement before drag intent, and tracking continues outside the sheet.

2. **Interruption check**
   - Release toward half/full, then grab mid-settle.
   - Expected: no input lock, no visual jump, retargets from current position.

3. **Snap behavior check**
   - Slow drag near thresholds and fast flick between collapsed / half / full.
   - Record whether target choice matches the intended contract.

4. **Reduced Motion check**
   - Enable `prefers-reduced-motion`.
   - Expected: state still changes clearly, but large spatial glide/elastic motion is removed or sharply shortened.

5. **Performance check**
   - Test while the dense table/editor surface is populated.
   - Inspect for layout thrash from `top`/`offsetTop`; target compositor-driven transform updates.


## Output C

## Evidence-labeled verdict

**Verdict: not production-ready for a calm repeated-use operations sheet.**  
**Static evidence:** the implementation moves a layout property (`top`) directly from `event.clientY`, uses a fixed `ease-in` animation, blocks interaction with `animating`, has no velocity/projection model, no pointer capture, no reduced-motion branch, and a broad `transition: all`. The result is likely jumpy, laggy, non-interruptible, and inaccessible for a collapsed/half/full bottom sheet.

---

## Prioritized findings

### P0 — Drag is not true direct manipulation
**Evidence:** `startY = event.clientY` is recorded but never used; `pointermove` sets `sheet.style.top = event.clientY`.  
**Impact:** the sheet will jump so its top aligns to the pointer, ignoring where the user grabbed it. It also updates on every pointer move over the sheet, not only during an active drag.  
**Fix direction:** track `isDragging`, grab offset, current sheet position, and apply `current + delta`.

### P0 — Motion is non-interruptible
**Evidence:** `if (animating) return` on `pointerdown`; animation promise resets `animating` only after completion.  
**Impact:** users cannot grab a moving sheet and redirect it. In a repeated operations workflow, this makes the UI feel locked and slow.  
**Fix direction:** allow interruption, cancel the current animation, read the live presentation position, and continue from there.

### P0 — Uses layout properties on the input path
**Evidence:** `sheet.style.top`, `sheet.offsetTop`, and WAAPI animating `top`.  
**Impact:** `top` can trigger layout/reflow; `offsetTop` reads layout; this is risky during pointermove and for large inventory screens.  
**Fix direction:** animate only `transform: translateY(...)`; store logical snap state separately.

### P1 — Release behavior ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` chooses from current position only.  
**Impact:** a fast flick toward full/closed may snap backward if the release point is closer to another state.  
**Fix direction:** compute release velocity, project the likely resting point, then choose collapsed/half/full from that projected endpoint.

### P1 — Easing and duration are wrong for a sheet
**Evidence:** `{ duration: 480, easing: "ease-in" }`.  
**Impact:** `ease-in` starts slowly and accelerates into the target, which feels like the sheet is running away at the end. 480ms is also heavy for repeated operational use.  
**Fix direction:** use a responsive decelerating/spring-like settle, usually faster, with velocity handoff and little/no bounce unless the user flicked.

### P1 — CSS conflicts with gesture motion
**Evidence:** `.sheet { transition: all 300ms; }` and `.sheet:active { transform: scale(0.96); }`.  
**Impact:** `transition: all` may animate unrelated properties and interfere with JS-driven movement. `:active` scaling the whole sheet during drag can make content shrink under the pointer and will conflict if `transform` is also used for translate.  
**Fix direction:** remove `transition: all`; transition only intentional non-gesture properties. Prefer subtle handle, shadow, or scrim feedback instead of scaling the whole sheet.

### P1 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` handling; large spatial travel remains.  
**Impact:** reduced-motion users still get full sheet travel and easing.  
**Fix direction:** preserve state feedback with short opacity/color/handle changes, instant or very short snap, and no overshoot/large animated travel.

### P2 — Pointer lifecycle is incomplete
**Evidence:** no `setPointerCapture`, no `pointercancel`, no `lostpointercapture`, no pointer id tracking.  
**Impact:** dragging can break when the pointer leaves the sheet, when scrolling begins, or when another pointer is introduced.  
**Fix direction:** capture the active pointer, ignore non-active pointers, clean up on cancel/lost capture.

### P2 — Snap states are not represented as accessible state
**Evidence:** code calculates a pixel target but shows no collapsed/half/full state model.  
**Impact:** keyboard users and assistive tech may not know or control the current sheet state.  
**Fix direction:** expose state through semantic controls, labels, keyboard commands, focus management, and visible state feedback.

---

## Concrete direct-manipulation moves

1. **On pointer down**
   - Set `isDragging = true`.
   - Capture pointer.
   - Cancel any running animation.
   - Read the current visual `translateY`.
   - Store `startPointerY`, `startSheetY`, and grab offset.

2. **On pointer move**
   - Only respond if `isDragging` and pointer id matches.
   - Compute `nextY = startSheetY + (event.clientY - startPointerY)`.
   - Apply `transform: translateY(nextY)` inside `requestAnimationFrame`.
   - Record recent `{ y, time }` samples for velocity.

3. **At bounds**
   - Do not hard-stop.
   - Apply progressive resistance past collapsed/full limits so the sheet still follows, but more slowly.

4. **On release**
   - Compute release velocity from recent samples.
   - Project endpoint from velocity.
   - Choose nearest snap among collapsed, half, full using the projected endpoint, not only current position.
   - Animate from current visual position to target with velocity handoff.

5. **During animation**
   - Keep it interruptible.
   - A new pointer down should stop/re-target the current motion immediately.

6. **For reduced motion**
   - Avoid large animated travel.
   - Snap position immediately or in a very short duration.
   - Preserve feedback through handle color, elevation, opacity, state label, or brief non-spatial emphasis.

7. **For calm operations use**
   - Avoid bouncy decoration by default.
   - Use predictable critically damped settling.
   - Keep feedback subtle, fast, and consistent across collapsed/half/full.

---

## Verified / unverified boundaries

**Verified from static code:**
- Drag uses `top`, not `transform`.
- `startY` is unused.
- Pointer move is not gated by an active drag flag.
- Animation uses fixed `480ms ease-in`.
- Snap target is based on `offsetTop`, not projected velocity.
- Animation is locked by `animating`.
- CSS uses `transition: all`.
- No reduced-motion branch is present in the snippet.

**Not verified without runtime/device testing:**
- Actual frame rate or layout cost.
- Whether the sheet visibly jumps in the current DOM positioning context.
- Whether scrolling conflicts occur on touch hardware.
- Whether WAAPI `fill: forwards` causes state mismatch in this exact layout.
- Whether focus management or keyboard controls exist elsewhere.
- Whether snap points are visually correct across viewport sizes.

---

## Smallest runtime validation plan

1. **Pointer continuity**
   - Drag from handle, body, and edge.
   - Confirm no initial jump and no movement before active drag.

2. **Interruptibility**
   - Release toward half/full, then grab mid-animation.
   - Confirm the sheet immediately follows the pointer without waiting.

3. **Velocity intent**
   - Slow drag near midpoint.
   - Fast flick toward each state.
   - Confirm snap target follows intent, not just nearest release position.

4. **Performance smoke**
   - Record one drag interaction.
   - Check for layout thrash, long tasks, and dropped frames during pointermove.

5. **Reduced motion**
   - Enable reduced motion.
   - Confirm collapsed/half/full state changes remain understandable without large spatial travel.

6. **Accessibility basics**
   - Keyboard open/collapse/expand.
   - Focus remains visible and logical.
   - Current sheet state is announced or otherwise perceivable.
