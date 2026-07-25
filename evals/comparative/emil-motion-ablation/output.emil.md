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
