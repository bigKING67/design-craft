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

**Verdict: Not production-ready for a calm, repeated-use operations sheet.**  
**Evidence from snippet:** the sheet is moved with `top`, animated with fixed `ease-in` timing, blocks or corrupts interaction during animation, has no velocity-aware snap, no reduced-motion path, and CSS `transition: all` conflicts with gesture tracking.  
**Impact:** users will see jumps, lag, non-interruptible motion, inconsistent snap behavior, and potentially large spatial travel that violates the Reduced Motion requirement.

---

## Prioritized findings

### P0 — Drag is not true direct manipulation
**Evidence:** `startY` is recorded but never used; `pointermove` sets `sheet.style.top = event.clientY`.  
**Problem:** the sheet jumps so its top equals the pointer position instead of preserving the grab offset. A drag from the middle of the sheet will snap the sheet top to the cursor/finger.  
**Fix direction:** track `grabOffset = pointerY - sheetTop`; set position to `pointerY - grabOffset`.

### P0 — Gesture motion is non-interruptible and internally inconsistent
**Evidence:** `if (animating) return` in `pointerdown`, but `pointermove` has no `dragging` or `animating` guard.  
**Problem:** users cannot intentionally grab a moving sheet, yet stray pointer moves can still mutate `top`. This is the worst of both worlds: blocked agency plus unstable state.  
**Fix direction:** allow interruption; cancel the current animation on pointerdown, read the current visual position, then continue from there.

### P0 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` handling; release always animates up to `480ms` with spatial travel.  
**Problem:** collapsed/half/full transitions can move a large surface across the viewport. Reduced Motion must preserve feedback without large travel.  
**Fix direction:** in reduced motion, avoid long sheet travel; use immediate state placement plus short opacity, handle, border, shadow, or state-label feedback.

### P1 — `top` animation causes layout work and weak frame reliability
**Evidence:** gesture updates `sheet.style.top`; release reads `sheet.offsetTop`; animation changes `top`.  
**Problem:** `top` affects layout and `offsetTop` can force synchronous layout. On a 10,000-row operations surface, this risks jank.  
**Fix direction:** position with `transform: translateY(...)`; keep a numeric `currentY` state; read layout only at gesture start or resize.

### P1 — CSS transition conflicts with gesture tracking
**Evidence:** `.sheet { transition: all 300ms; }` while JS updates `top` on every `pointermove`.  
**Problem:** each drag frame may be eased by CSS instead of following 1:1. `transition: all` also animates unrelated changes and can fight the WAAPI animation.  
**Fix direction:** remove broad transitions from the draggable surface; animate only explicit properties, and disable transitions during active drag.

### P1 — Release behavior ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only considers current position.  
**Problem:** a fast upward flick near the half point may incorrectly snap back instead of continuing to full. A slow deliberate drag and a high-velocity throw are treated the same.  
**Fix direction:** compute release velocity, project the likely resting endpoint, then choose collapsed/half/full from that projected value.

### P1 — Fixed `480ms ease-in` feels wrong for a sheet
**Evidence:** `{ duration: 480, easing: "ease-in" }`.  
**Problem:** `ease-in` starts slowly after the user releases, creating perceived hesitation. A fixed duration also makes short snaps feel sluggish and long snaps feel abrupt.  
**Fix direction:** use a velocity-aware spring or responsive easing that starts from the release velocity; keep calm damping, avoid decorative bounce unless caused by a flick.

### P2 — `fill: "forwards"` risks state drift
**Evidence:** WAAPI animation fills visually but the code does not commit the final `top` style.  
**Problem:** visual position and DOM/style state can diverge; later `offsetTop` or style reads may not match what the user sees.  
**Fix direction:** on finish, commit/cancel the animation and set the canonical position value.

### P2 — Press feedback is too heavy and not state-specific
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Problem:** shrinking an entire operations sheet can make dense content pulse, reduce legibility, and conflict with transform-based sheet movement.  
**Fix direction:** give feedback on the handle or grip area, not the whole sheet; use subtle handle compression, shadow change, or background elevation.

### P2 — Missing pointer lifecycle handling
**Evidence:** no `setPointerCapture`, `pointercancel`, `lostpointercapture`, drag threshold, or `touch-action`.  
**Problem:** dragging can be lost when the pointer leaves the sheet; browser scroll/selection may compete with the gesture; cancellation may leave stale state.  
**Fix direction:** capture the pointer on drag start, release it on end/cancel, define `touch-action`, and reset state on cancellation.

---

## Concrete direct-manipulation moves

1. **Use a canonical Y model**
   - `collapsedY`, `halfY`, `fullY`
   - `currentY`
   - `targetY`
   - render with `transform: translate3d(0, currentYpx, 0)`

2. **Start drag from the current visual position**
   - On `pointerdown`, cancel active animation.
   - Read the current presentation Y, not the old target.
   - Store `grabOffset = event.clientY - currentY`.

3. **Track only while dragging**
   - Set `dragging = true`.
   - Use `setPointerCapture(event.pointerId)`.
   - Ignore unrelated `pointermove`s.

4. **Make movement 1:1**
   - On move: `nextY = event.clientY - grabOffset`.
   - Clamp or rubber-band beyond full/collapsed bounds.
   - Update inside `requestAnimationFrame`.

5. **Record velocity**
   - Keep the last few `{ y, time }` samples.
   - On release, compute px/s velocity.

6. **Snap from projected intent**
   - `projectedY = currentY + projectedDistanceFromVelocity`.
   - Choose nearest of collapsed/half/full from `projectedY`, not only `currentY`.

7. **Hand off velocity into the settle animation**
   - The release animation should begin at the same speed the pointer had at release.
   - Prefer a calm, critically damped or lightly damped spring over fixed `ease-in`.

8. **Make animation interruptible**
   - A new pointerdown during settle should immediately grab the sheet at its visible position.
   - No `animating` lockout that forces the user to wait.

9. **Replace whole-sheet active scale**
   - Move feedback to the drag handle.
   - Example feedback: handle darkens/widens, sheet shadow firms, or header compresses by 1–2px.

10. **Reduced Motion path**
   - On state change, place the sheet with little or no travel.
   - Preserve feedback with a short opacity/elevation/outline/handle-state change.
   - Avoid bounce, long slides, and large spatial displacement.

---

## Verified / unverified boundaries

**Verified from provided code**
- Uses `top` for drag and animation.
- Uses `offsetTop` for snap calculation.
- Uses fixed `480ms ease-in`.
- Uses `transition: all 300ms`.
- Uses whole-sheet `:active` scale.
- Has no shown Reduced Motion branch.
- Has no shown pointer capture, velocity tracking, cancellation, or keyboard handling.

**Not verified from static snippet**
- Actual snap point values.
- Sheet dimensions and viewport constraints.
- Whether another layer manages ARIA, focus, keyboard shortcuts, or scroll locking.
- Runtime frame rate, input latency, or device behavior.
- Whether CSS outside the snippet overrides these rules.

---

## Smallest runtime validation plan

1. **Pointer continuity**
   - Drag from handle, header, and mid-sheet.
   - Confirm no jump on grab and no lost drag when pointer leaves bounds.

2. **Interruptibility**
   - Start collapsed → full animation.
   - Grab mid-flight and reverse.
   - Pass only if the sheet follows immediately from its visible position.

3. **Snap intent**
   - Test slow drags and fast flicks between collapsed, half, and full.
   - Confirm velocity changes the chosen target predictably.

4. **Reduced Motion**
   - Enable reduced motion.
   - Confirm state feedback remains visible but large spatial travel and bounce are removed.

5. **Performance smoke**
   - Drag over the real operations table.
   - Inspect for forced layout, dropped frames, and pointer latency.

6. **Accessibility smoke**
   - Keyboard open/collapse/expand.
   - Focus remains visible and recoverable.
   - Screen reader state names match collapsed/half/full.


## Output B

## Verdict

**[Static evidence] Not production-ready for a calm repeated-use operations sheet.**  
The implementation does not provide true direct manipulation, has no Reduced Motion path, animates layout properties, and can create lag, jumps, and conflicting motion. The collapsed / half / full model is only implied at release, not represented as stable interactive states during drag.

---

## Prioritized findings

### 1. Drag does not track intent reliably

**Evidence:** `startY = event.clientY` is stored but never used. `pointermove` sets `sheet.style.top = event.clientY`.

**Impact:** The sheet can jump because movement is based on absolute pointer position, not the sheet’s starting offset plus drag delta. This breaks the “attached to finger / cursor” feel.

**Fix direction:** Track:

```js
delta = event.clientY - startY
nextY = startSheetY + delta
```

Then clamp or resist beyond snap bounds.

---

### 2. Motion uses `top`, causing layout work during drag and settle

**Evidence:** `sheet.style.top = ...`, `sheet.offsetTop`, and animation keyframes use `top`.

**Impact:** `top` changes can trigger layout and paint on every pointer move. `offsetTop` also forces layout reads. This is risky for a 10,000-row operations surface where the sheet may sit over expensive content.

**Fix direction:** Use `transform: translateY(...)` for drag and snap animation. Keep snap state in JS, but render position through transform.

---

### 3. CSS transition conflicts with gesture control

**Evidence:** `.sheet { transition: all 300ms; }`

**Impact:** Every `top` change during pointermove may be transitioned, causing the sheet to lag behind the pointer. `transition: all` can also accidentally animate unrelated properties.

**Fix direction:** Remove `transition: all`. Use explicit transition only for non-drag settle:

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

---

### 4. Release animation feels wrong for a responsive sheet

**Evidence:** `{ duration: 480, easing: "ease-in" }`

**Impact:** `ease-in` starts slowly and accelerates into the target, which can feel like the sheet is sliding away rather than settling. `480ms` is long for repeated operations use.

**Fix direction:** Use a responsive deceleration/ease-out style curve and shorter duration, ideally velocity-aware. Example target behavior: quick catch-up, smooth settle, no dramatic travel.

---

### 5. No Reduced Motion path

**Evidence:** No `prefers-reduced-motion` handling and no alternate state feedback.

**Impact:** Users who prefer reduced motion still get large spatial travel over 480ms plus active scaling.

**Fix direction:** In Reduced Motion:
- avoid long animated travel;
- snap position immediately or within a very short duration;
- preserve feedback with handle highlight, state label, border/color change, or subtle opacity change;
- avoid `scale(0.96)`.

---

### 6. Pointer lifecycle is incomplete

**Evidence:** There is no `dragging` flag, no pointer capture, and no pointer cancel handling.

**Impact:** `pointermove` can mutate the sheet even when a valid drag was not started. If the pointer leaves the sheet or the gesture is interrupted, state may become inconsistent.

**Fix direction:** On pointerdown:
- set `dragging = true`;
- capture the pointer;
- record pointer id, start Y, and sheet position.

On pointermove:
- ignore events unless `dragging` and pointer id matches.

On pointerup / pointercancel:
- release capture;
- settle to snap point;
- clear dragging state.

---

### 7. Snap decision ignores velocity and direction

**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only uses final position.

**Impact:** A fast intentional upward or downward flick may choose the wrong snap point if the final offset is near the previous state.

**Fix direction:** Use position + velocity:
- slow drag: nearest snap point;
- fast upward drag: next more-expanded state;
- fast downward drag: next more-collapsed state.

---

### 8. Active scale fights the sheet metaphor

**Evidence:** `.sheet:active { transform: scale(0.96); }`

**Impact:** The sheet shrinks while being dragged, which can make controls move under the pointer and makes the surface feel like a button rather than a panel.

**Fix direction:** Keep the panel spatially stable. Use handle affordance feedback instead: handle color, shadow, border emphasis, or cursor change.

---

## Concrete direct-manipulation moves

1. **Represent state explicitly**
   - `collapsed`, `half`, `full`
   - expose current snap point as data/state, not only pixel position.

2. **Use transform-based positioning**
   - render with `translateY(currentY)`;
   - avoid writing `top` during drag.

3. **Separate drag from settle**
   - during drag: no transition, 1:1 pointer tracking;
   - after release: animate to snap point.

4. **Clamp with resistance**
   - hard clamp within full/collapsed bounds, or add slight resistance past edges;
   - never allow uncontrolled off-screen movement.

5. **Use pointer capture**
   - preserve drag continuity if the pointer leaves the handle/sheet.

6. **Make snap velocity-aware**
   - slow movement chooses nearest point;
   - fast flick advances one state in flick direction.

7. **Constrain gesture start area**
   - prefer handle/header drag area;
   - avoid hijacking scrollable sheet content.

8. **Add Reduced Motion behavior**
   - no large animated travel;
   - very short transform update or immediate snap;
   - visible state feedback through handle/status styling.

9. **Avoid transform conflict**
   - do not use `scale()` on the same element that uses `translateY`;
   - if visual press feedback is needed, apply it to an inner handle only.

---

## Verified / unverified boundaries

**Verified from static code:**
- `top` is mutated on every pointermove.
- `offsetTop` is read on release.
- animation duration is `480ms`.
- easing is `ease-in`.
- CSS uses `transition: all 300ms`.
- CSS applies `transform: scale(0.96)` on active.
- no Reduced Motion branch is present.
- no pointer capture, pointercancel, drag flag, or velocity logic is present.
- `startY` is assigned but unused.

**Not verified here:**
- actual frame rate or dropped frames.
- behavior on touch hardware.
- interaction with scrollable content inside the sheet.
- exact visual jank from `transition: all`.
- accessibility tree, focus order, or keyboard support.
- whether surrounding code adds missing state or Reduced Motion handling elsewhere.

---

## Smallest runtime validation plan

1. **Gesture correctness**
   - drag from collapsed to half and full;
   - confirm no initial jump;
   - confirm pointer and sheet stay visually attached.

2. **Snap behavior**
   - slow drag near boundaries chooses nearest snap;
   - fast flick moves one state in flick direction;
   - pointercancel leaves sheet in a valid state.

3. **Reduced Motion**
   - enable reduced motion;
   - confirm no long spatial animation;
   - confirm state feedback remains visible.

4. **Performance smoke**
   - drag over the populated table;
   - check for obvious lag, layout spikes, or delayed pointer tracking.

5. **Interaction safety**
   - drag from handle;
   - scroll sheet content;
   - confirm scrolling and dragging do not fight each other.


## Output C

## Evidence-labeled verdict

**Verdict: Block for production.**  
[Static evidence] The sheet is moved with `top` on every `pointermove`, has `transition: all 300ms`, settles with `480ms ease-in`, lacks visible Reduced Motion handling, and uses a global `animating` lock.  
[Product evidence] This is a repeatedly used operations surface with collapsed / half / full states; the motion should feel immediate, interruptible, calm, and state-preserving. This implementation is likely to feel laggy, non-direct, and fragile.

## Prioritized findings

1. **P0 — Drag is not truly direct manipulation.**  
   [Static] `pointermove` always writes `sheet.style.top = event.clientY`; `startY` is recorded but unused. There is no dragging flag, grab offset, pointer capture, direction threshold, or boundary clamp.  
   [Impact] The sheet can jump to the pointer, move without an intentional drag, lose tracking outside the element, and collide with page scrolling or accidental taps.

2. **P0 — `transition: all` fights the drag.**  
   [Static] `.sheet { transition: all 300ms; }` applies while `top` is updated during pointer moves.  
   [Impact] Each drag frame can be eased instead of staying 1:1 under the pointer, creating lag. It also risks animating unrelated future property changes.

3. **P0 — Layout-property animation is a performance risk.**  
   [Static] The hot path writes `top`; release animation also animates `top`; `pointerup` reads `sheet.offsetTop`.  
   [Impact] This can trigger layout work during the most latency-sensitive part of the interaction. A sheet should generally move with `transform: translateY(...)`.

4. **P0 — The motion is not safely interruptible.**  
   [Static] `animating` blocks `pointerdown`, but `pointermove` still writes `top`; the settle animation is not canceled or retargeted from the current presentation value.  
   [Impact] A user cannot confidently grab the sheet mid-settle. Competing pointer writes and WAAPI animation may create jumps.

5. **P1 — Settle timing/easing is wrong for repeated operations work.**  
   [Static] `{ duration: 480, easing: "ease-in" }`.  
   [Impact] `ease-in` delays the response at the start and accelerates late; 480ms can feel heavy for a high-frequency operations control. The settle should feel responsive, usually shorter or spring-like, and start from release velocity.

6. **P1 — Snap selection ignores velocity and intent.**  
   [Static] `nearestSnapPoint(sheet.offsetTop)` uses current layout position only.  
   [Impact] A quick flick toward half/full/collapsed may be ignored if the release point is closer to another state. If product semantics allow momentum, target choice should consider measured release velocity or a bounded projected endpoint.

7. **P1 — Reduced Motion requirement is unmet in the supplied code.**  
   [Static] No `prefers-reduced-motion` branch or alternate feedback path is shown.  
   [Product] Reduced Motion must preserve state feedback without large spatial travel.  
   [Impact] Users requesting reduced motion may still get full-distance sheet travel.

8. **P2 — Press feedback is too broad and may conflict with sheet movement.**  
   [Static] `.sheet:active { transform: scale(0.96); }`.  
   [Impact] Scaling the whole sheet can make dense content feel unstable. If translation later moves to `transform`, scale and translate need separate wrapper layers or one composed transform owner.

## Concrete direct-manipulation moves

- Replace `top` movement with one position owner: `translate3d(0, ypx, 0)` on a sheet transform layer.
- Remove `transition: all`; transition only explicit non-gesture properties, or disable transition while dragging.
- On `pointerdown`: capture `pointerId`, record start pointer Y, current sheet Y, snap state, and grab offset; cancel any active settle from the current on-screen value.
- On `pointermove`: only respond while dragging the captured pointer; after an `8–12px` intent threshold, update via `requestAnimationFrame`; clamp to collapsed/full bounds with optional soft resistance.
- On `pointerup/cancel`: compute release velocity from recent samples in CSS px/s; choose target by the product’s snap rule, optionally using a bounded projected endpoint if momentum targeting is desired.
- Settle with an interruptible spring or equivalent retargetable animation; default to no bounce for this calm operations context.
- Keep press feedback on a handle or inner affordance, not the whole sheet content; if scale remains, separate it from the translate layer.
- Add Reduced Motion behavior: snap state with no large travel, or use a very short opacity/elevation/color/handle-state change while preserving collapsed/half/full feedback.
- Ensure non-pointer operation: keyboard controls for moving between collapsed/half/full, visible focus, state labels, and focus continuity after state changes.

## Verified / unverified boundaries

**Verified from static code only**
- `top` is mutated during drag and animated on release.
- `transition: all 300ms` applies to the sheet.
- Release animation uses `480ms ease-in`.
- `startY` is unused.
- No pointer capture, velocity sampling, bounds, drag flag, or Reduced Motion branch appears in the supplied snippet.
- The animation lock does not provide clean interruption semantics.

**Not verified**
- Actual frame rate, perceived smoothness, touch-device feel, scroll interaction, snap-point geometry, or final rendered behavior.
- Whether other omitted code provides keyboard support, ARIA/state announcements, focus management, bounds, or Reduced Motion.
- Whether the sheet is inside a layout where `top` has additional constraints or compensating styles.

## Smallest runtime validation plan

1. Verify drag attachment: pointer down, move slowly, leave/re-enter sheet bounds, release from collapsed/half/full.
2. Verify interruption: flick to a snap point, grab mid-settle, reverse direction; confirm no jump or input lock.
3. Verify snap intent: slow drag near thresholds and fast flicks in both directions; record chosen target and release velocity.
4. Verify Reduced Motion: emulate `prefers-reduced-motion`; confirm no large spatial travel while collapsed/half/full state feedback remains clear.
5. Verify performance risk: record one drag under normal app load; check for layout work during pointer moves and dropped frames.
