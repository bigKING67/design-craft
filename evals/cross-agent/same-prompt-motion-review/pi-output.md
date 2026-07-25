## 1. Evidence level and design read

**Evidence level: static-code review only.** The prompt proves the shown JS/CSS values and missing branches inside the snippet; it does **not** prove runtime smoothness, computed-style conflicts, frame rate, touch feel, or full-component accessibility.

**Design read:** Reading this as a **desktop web operations bottom sheet** for repeated staff workflows, with a **calm utility UI**, optimized for **context-preserving direct manipulation between collapsed / half / full states**.

**Verdict: Block for implementation approval.** The interaction has the right product reason to exist, but the current motion model fights direct manipulation.

---

## 2. Should this motion exist?

**Yes, but narrowly.**

Should exist:
- Immediate pointer-down acknowledgement.
- 1:1 drag tracking.
- A short, causal settle from release position to the chosen snap point.
- State feedback for collapsed / half / full.

Should not animate:
- Drag tracking itself should not be eased or delayed.
- Layout properties like `top` should not be animated on a hot gesture path.
- The whole sheet should not shrink with `scale(0.96)` during drag.
- `transition: all` should not exist on the sheet.
- Reduced Motion should not perform large spatial travel or elastic movement.

---

## 3. Prioritized findings

### P0 — Drag is not true direct manipulation
**Evidence:** `pointermove` sets `sheet.style.top = event.clientY`.

This does not preserve grab offset, does not show an active-drag state, does not require a committed drag, and does not use pointer capture. It likely makes the sheet’s top edge chase the pointer instead of keeping the grabbed point attached. Also, `pointermove` is not gated by an active pointer in the snippet.

**Design impact:** Operators lose causality: the object feels controlled by page coordinates, not by their hand.

---

### P0 — The sheet is locked during settle instead of interruptible
**Evidence:** `if (animating) return;` on `pointerdown`; `animating = true` until `.finished`.

A draggable sheet must be grabbable mid-flight from its current presentation value. Locking input until animation completion makes the UI feel modal and laggy, especially in repeated operations work.

**Design impact:** Fast corrections become impossible; the user has to wait for motion to finish before regaining control.

---

### P0 — Release physics are wrong for a gesture surface
**Evidence:** target is `nearestSnapPoint(sheet.offsetTop)` and settle is `duration: 480`, `easing: "ease-in"`.

There is no measured release velocity, no initial velocity handoff, no bounded projected endpoint, and no hysteresis. `ease-in` is especially poor here because it starts slowly exactly when the user expects immediate response.

**Design impact:** Slow drags, flicks, and reversals collapse into the same mechanical behavior; the sheet feels algorithmic rather than physical.

---

### P1 — Animation ownership conflicts are likely
**Evidence:** JS animates `top`; CSS declares `transition: all 300ms`; CSS also applies `transform: scale(0.96)` on `:active`.

`transition: all` can accidentally animate gesture updates and unrelated properties. `top` animation is layout-affecting. The active scale changes the sheet geometry while the user is trying to drag it, which undermines spatial continuity.

**Design impact:** The sheet may feel sticky, delayed, shrunken, or visually unstable during the exact moment precision matters.

---

### P1 — No Reduced Motion path is present in the snippet
**Evidence:** no `prefers-reduced-motion` branch is shown; settle uses large spatial travel with `480ms`.

Reduced Motion does not mean no feedback, but it should avoid long positional travel, bounce, and vestibular movement.

**Design impact:** Accessibility requirement is unmet in the supplied implementation evidence.

---

## 4. Concrete design moves

1. **Pointer-down feedback**
   - On `pointerdown`, set active drag state, capture the pointer, store pointer id, and preserve the grab offset.
   - Use subtle handle feedback: color, shadow, or cursor change.
   - Avoid scaling the whole sheet; if scale is needed, apply it only to a handle affordance.

2. **1:1 tracking**
   - Track from `startSheetY + (event.clientY - startPointerY)`, not raw `clientY`.
   - Disable transitions during drag.
   - Drive visual position with `transform: translateY(...)`, not `top`.

3. **Presentation-value interruption**
   - Remove the input lockout.
   - If a settle animation is running, cancel it on pointer-down after reading the current on-screen position.
   - Start the new drag from that presentation value so there is no jump.

4. **Velocity handoff**
   - Keep a short pointer sample history using monotonic timestamps.
   - Measure release velocity in CSS px/s.
   - Feed that measured velocity into the settle animation as initial velocity, converting units if the chosen spring API requires it.

5. **Projected endpoints**
   - Keep target-selection semantics explicit.
   - If momentum targeting is authorized: compute a bounded projected endpoint from current presentation value + release velocity, clamp it to valid sheet range, then choose nearest snap point.
   - If not authorized: keep `nearestSnapPoint(current)` but still hand off velocity into the settle.

6. **Soft boundaries and hysteresis**
   - Add an 8–12px intent threshold before committing to drag.
   - Add progressive resistance past collapsed/full bounds instead of hard jumps.
   - Clamp final settle to valid snap points.
   - Ignore additional pointers after the active drag begins.

7. **Motion/property cleanup**
   - Replace `transition: all 300ms` with explicit transitions only for non-gesture visual properties.
   - Use a spring-like settle for the sheet, defaulting to low/no bounce for this serious operations context.
   - If no spring primitive is available, use a short ease-out settle, not `480ms ease-in`.

8. **Reduced Motion**
   - Under `prefers-reduced-motion: reduce`, remove rubber-band, bounce, and long travel.
   - Snap immediately or use a very short 80–120ms non-vestibular state change.
   - Preserve feedback through handle state, state label, focus/ARIA update, or color/opacity—not large spatial movement.

---

## 5. Verified versus unverified claims

Verified from supplied snippet:
- The sheet writes `top` on pointer move.
- The settle animation animates `top`.
- Settle uses `480ms` and `ease-in`.
- Pointer-down is ignored while `animating`.
- CSS includes `transition: all 300ms`.
- CSS includes `:active { transform: scale(0.96); }`.
- No explicit velocity, pointer capture, grab-offset, boundary, interruption, or Reduced Motion branch appears in the snippet.

Unverified:
- Actual frame rate or jank.
- Whether `transition: all` conflicts in computed runtime behavior.
- Whether the sheet has compensating accessibility/state logic elsewhere.
- Whether `nearestSnapPoint` intentionally excludes momentum semantics.
- Real touch feel on device hardware.
- Behavior inside responsive layouts, high-density tables, or 60/120Hz displays.

---

## 6. Minimal validation plan before approval

1. **Desktop browser interaction run**
   - Drag slowly, drag quickly, reverse direction, release near each snap point.
   - Verify no visual jump, no delayed tracking, and no lockout during settle.

2. **Pointer-capture test**
   - Start drag on the handle, move outside the sheet/window region, release.
   - Verify tracking and cleanup remain correct.

3. **Interruption test**
   - Release toward a snap point, immediately grab mid-flight, reverse direction.
   - Verify the new drag starts from the current presentation value.

4. **Physics test**
   - Compare slow release versus fast flick from the same position.
   - Verify release velocity is measured in CSS px/s and handed into settle.

5. **Boundary test**
   - Pull beyond collapsed/full limits.
   - Verify soft resistance during drag and clamped final state.

6. **Reduced Motion run**
   - Enable `prefers-reduced-motion`.
   - Verify no large animated travel or bounce, while state feedback remains clear.

7. **Performance trace**
   - Record drag/release under realistic app load.
   - Verify compositor-friendly transform updates and no layout work per pointer frame.

8. **Real touch hardware smoke**
   - Test at least one touch device or touchscreen browser.
   - Verify finger attachment, release feel, and accidental-tap behavior.
