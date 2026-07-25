## 1. Evidence level and design read

**Evidence level: static implementation evidence only.** No runtime, computed-style, pointer trace, Reduced Motion, responsive, or device validation was performed.

**Reading this as:** a web operations bottom sheet for repeated daily use, with calm utility motion optimized for preserving task context while moving between `collapsed`, `half`, and `full`.

**Verdict: Block for implementation approval.** The interaction has the right product reason to move, but the current motion model breaks direct manipulation, interruption, accessibility expectations, and likely performance constraints.

---

## 2. Should this motion exist?

**Yes, partially.** Motion should exist for:

- 1:1 drag tracking while the user directly manipulates the sheet.
- A short causal settle from release position to the selected snap point.
- Minimal pointer-down feedback that confirms “this is grabbed.”

**Should not animate:**

- `top` / layout position.
- `transition: all`.
- Large whole-sheet `scale(0.96)` during drag.
- A fixed `480ms ease-in` settle.
- Any large spatial travel in Reduced Motion mode.
- Any laggy transition during active pointer tracking.

---

## 3. Prioritized findings

### P0 — Drag is not true direct manipulation

**Evidence:** `pointermove` sets `sheet.style.top = event.clientY`; `startY` is captured but unused. No grab offset, drag threshold, pointer capture, or dragging guard is shown.

**Why it matters:** The sheet can jump so its top aligns to the pointer instead of preserving where the user grabbed it. It also appears to update on every pointer move over the sheet, not only during an active drag.

**Design impact:** This violates the primary job: moving the sheet without losing task context.

---

### P0 — The sheet is non-interruptible

**Evidence:** `if (animating) return` on `pointerdown`; `animating = true` until `.finished`.

**Why it matters:** A user cannot re-grab the sheet while it is settling. Gesture surfaces must be interruptible from the current presentation value, not locked until an animation completes.

**Design impact:** The interface feels modal and delayed instead of physically attached to the operator’s hand.

---

### P0 — Wrong settle physics for a gesture sheet

**Evidence:** release uses `nearestSnapPoint(sheet.offsetTop)` and animates `{ duration: 480, easing: "ease-in" }`; no velocity history, velocity handoff, projected endpoint, or spring behavior is present.

**Why it matters:** `ease-in` starts slowly exactly when the user expects immediate continuation from release. A fixed duration ignores how fast or far the user moved.

**Design impact:** A quick flick and a careful drag receive the same kind of settle, weakening causality.

---

### P0 — Reduced Motion requirement is unmet

**Evidence:** no `prefers-reduced-motion` branch is present in the supplied JS or CSS.

**Why it matters:** The product requirement says Reduced Motion must preserve state feedback without large spatial travel.

**Design impact:** Users who request reduced motion may still get full sheet travel and scale effects.

---

### P1 — Layout animation and CSS conflicts create jank risk

**Evidence:** JS mutates `top`; WAAPI animates `top`; CSS has `.sheet { transition: all 300ms; }`; `.sheet:active { transform: scale(0.96); }`.

**Why it matters:** `top` animation can trigger layout; `transition: all` may animate unintended properties; active scale can conflict with future transform-based dragging or visually shrink dense content.

**Design impact:** Risk of lag, blurred context, and unpredictable mixed CSS/WAAPI behavior.

---

## 4. Concrete design moves

1. **Pointer-down feedback**
   - On `pointerdown`, capture the pointer, record `pointerId`, current presentation Y, grab offset, and recent sample history.
   - Use subtle feedback on the drag handle or sheet chrome, not whole-sheet `scale(0.96)`.
   - Example intent: handle color/elevation/cursor change, maybe `scale(0.99)` only on a handle wrapper.

2. **1:1 tracking**
   - After an `8–12px` intent threshold, track `translateY` in CSS pixels using `pointerY - grabOffset`.
   - Disable settle transitions while dragging.
   - Use `transform: translateY(...)`, not `top`.

3. **Presentation-value interruption**
   - On new pointer-down during settle, cancel the running animation/spring.
   - Read the current on-screen Y from the animation state or computed transform.
   - Start the new drag from that value without visual jump.

4. **Velocity handoff**
   - Keep a short history of pointer samples with monotonic timestamps.
   - Compute release velocity in **CSS px/s**.
   - Feed that velocity into the settle animation as the initial velocity; do not restart from zero.

5. **Target selection / projected endpoint**
   - Preserve current nearest-snap semantics unless product authority approves momentum targeting.
   - If authorized, compute a bounded projected endpoint from current Y + release velocity, clamp to snap range, then choose the nearest valid snap.
   - Keep target selection separate from velocity handoff.

6. **Settle motion**
   - Replace `480ms ease-in` with a spring-like settle.
   - Starting point: drawer/sheet response around `0.3–0.4s`, damping near `0.8–1.0`, minimal or no bounce for calm operations UI.
   - For non-spring fallback, prefer a short ease-out/ease-in-out curve, not ease-in.

7. **Soft boundaries**
   - Clamp valid snap range, but apply progressive resistance beyond min/max instead of hard stops.
   - Allow re-entry: if the user drags back inside bounds, tracking should return smoothly.
   - Avoid destructive or context-losing transitions from a small accidental overshoot.

8. **Reduced Motion**
   - Under `prefers-reduced-motion: reduce`, remove large settle travel and elastic behavior.
   - Snap state immediately or with a very short non-spatial transition.
   - Preserve feedback via state text, handle highlight, selected detent indicator, focus-visible state, or a brief opacity/color change.

---

## 5. Verified vs unverified claims

**Verified from supplied code:**

- `pointermove` writes `top` directly.
- `startY` is captured but not used in the shown snippet.
- No shown pointer capture.
- No shown drag-state guard for `pointermove`.
- Release animation uses `top`, `480ms`, `ease-in`, and `fill: "forwards"`.
- Input is locked during animation via `animating`.
- CSS uses `transition: all 300ms`.
- CSS uses whole-sheet active `scale(0.96)`.
- No shown Reduced Motion branch.

**Unverified / requires runtime or broader source:**

- Actual frame rate, jank, layout cost, or dropped frames.
- Whether other code clamps bounds, prevents default scrolling, or handles keyboard.
- Whether `nearestSnapPoint` includes hysteresis or semantic rules.
- Exact visual jump amount on pointer-down.
- Computed transform/top interaction in the final stylesheet.
- Touch behavior on real devices.
- Screen reader state announcement.
- Responsive behavior across viewport heights.

---

## 6. Minimal validation plan before approval

1. **Desktop browser pointer test**
   - Drag from `collapsed`, `half`, and `full`.
   - Verify no jump on grab, 1:1 tracking, preserved grab offset, and no movement without active drag.

2. **Interruption test**
   - Release toward a snap point, then re-grab mid-settle.
   - Expected: animation cancels, sheet starts from current visual Y, no lockout or jump.

3. **Velocity test**
   - Compare slow drag vs quick flick.
   - Verify measured release velocity affects settle continuity; if momentum targeting is approved, verify projected endpoint target choice.

4. **Boundary test**
   - Pull beyond top and bottom limits.
   - Verify progressive resistance, safe clamping, and smooth re-entry.

5. **Reduced Motion run**
   - Enable `prefers-reduced-motion`.
   - Verify no large spatial settle/elastic motion, but state feedback remains clear.

6. **Performance trace**
   - Record under representative app load.
   - Confirm compositor-friendly transform animation, no avoidable layout thrash during pointermove, and stable frame pacing.

7. **Touch device test**
   - Validate on real touch hardware, not only mouse simulation.
   - Check pointer capture, scroll conflict, finger tracking, and release feel.

**Mode:** read-only critique.  
**Selected skill used:** design-craft.  
**Browser/device validation:** not performed, per prompt.
