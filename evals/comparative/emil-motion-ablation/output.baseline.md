## Verdict — static evidence only

**Not production-ready for a calm repeated-use operations sheet.**  
The implementation breaks direct manipulation, uses layout-bound motion, conflicts CSS transitions with JS animation, lacks reduced-motion behavior, and has incomplete pointer lifecycle handling. It will likely feel laggy, jumpy, and hard to trust during repeated operator use.

---

## Prioritized findings

### P0 — Drag is not actually anchored to the gesture
**Evidence:** `startY = event.clientY;` is stored but never used; `pointermove` sets `sheet.style.top = event.clientY`.

**Impact:** The sheet will jump so its top tracks the pointer’s viewport Y, not the user’s drag delta. A pointerdown at the handle midpoint can cause an immediate discontinuity.

**Fix direction:** Track `startY`, `startOffset`, and apply `next = startOffset + (event.clientY - startY)`.

---

### P0 — Motion uses `top`, causing layout work during drag and animation
**Evidence:** `sheet.style.top`, `sheet.offsetTop`, and `animate([{ top }, { top }])`.

**Impact:** `top` updates can trigger layout/paint. `offsetTop` reads after writes can force synchronous layout. This is risky for a 10,000-row operations surface and harms drag latency.

**Fix direction:** Use `transform: translateY(...)` as the single motion primitive. Keep logical sheet state separately from visual transform.

---

### P0 — CSS transition conflicts with gesture movement
**Evidence:** `.sheet { transition: all 300ms; }`.

**Impact:** Every drag update to `top`, `transform`, color, size, etc. may transition. During pointermove this can add 300ms lag and make the sheet chase the finger instead of following it.

**Fix direction:** Never use `transition: all` on an interactive sheet. Disable transitions during drag; apply a specific transform transition only during snap settle.

---

### P1 — Snap animation is too slow and uses the wrong easing
**Evidence:** `{ duration: 480, easing: "ease-in" }`.

**Impact:** `ease-in` starts slowly and accelerates away from the user’s release point, which feels unresponsive. 480ms is long for repeated operational use.

**Fix direction:** Use a responsive settle curve, typically faster and decelerating: e.g. `180–260ms` with an ease-out or custom responsive cubic-bezier. Let distance/velocity influence duration within a bounded range.

---

### P1 — Reduced Motion requirement is unmet
**Evidence:** No `prefers-reduced-motion` handling; product requires “Reduced Motion must preserve state feedback without large spatial travel.”

**Impact:** The sheet will still perform large spatial travel between collapsed, half, and full states.

**Fix direction:** In reduced motion, avoid animated travel. Snap nearly immediately, use short opacity/border/elevation/handle-state feedback, and preserve clear state labels.

---

### P1 — Pointer lifecycle is incomplete
**Evidence:** No `setPointerCapture`, no active pointer tracking, no `pointercancel`, no lost-capture handling, no guard in `pointermove`.

**Impact:** Drag can continue from unrelated pointer moves, get stuck if the pointer leaves the sheet, or fail on touch cancellation. Multi-touch/pen/mouse interactions are not controlled.

**Fix direction:** Track `dragging`, `pointerId`, call `setPointerCapture`, ignore other pointers, and end cleanly on `pointerup`, `pointercancel`, and `lostpointercapture`.

---

### P1 — Animation state can desynchronize
**Evidence:** `animating = true`; `.finished.then(...)`; `fill: "forwards"`; final style is not explicitly committed.

**Impact:** If the animation is interrupted/canceled, `animating` may stay wrong unless handled. `fill: forwards` can leave visual state in animation output while layout/style state remains stale.

**Fix direction:** Cancel prior animations, commit final transform/style explicitly, handle rejection/finally, and store canonical state: `collapsed | half | full`.

---

### P2 — Active scale is hostile for a bottom sheet
**Evidence:** `.sheet:active { transform: scale(0.96); }`.

**Impact:** This changes the whole sheet’s size while the user is trying to drag it, distorting spatial mapping and potentially fighting the translation transform.

**Fix direction:** Put press feedback on the handle, not the entire panel. Use subtle handle color/elevation/state feedback instead of panel scale.

---

### P2 — Snap decision lacks velocity, bounds, and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only.

**Impact:** A fast intentional fling and a slow small drag to the same position resolve identically. No visible clamping means the sheet may overshoot invalid ranges during drag.

**Fix direction:** Use position + release velocity + thresholds. Clamp movement between full and collapsed bounds. Bias toward the next state when velocity exceeds a small threshold.

---

## Concrete direct-manipulation moves

1. **Model sheet state explicitly**
   - `state = "collapsed" | "half" | "full"`
   - `snapPoints = { collapsed, half, full }`
   - `currentY` is visual position; `state` is semantic position.

2. **Use transform-only movement**
   - During drag: `sheet.style.transform = translate3d(0, ${y}px, 0)`
   - Avoid `top`, `offsetTop`, and `transition: all`.

3. **Anchor drag to initial offset**
   - On pointerdown:
     - save `startPointerY`
     - save `startSheetY`
     - capture pointer
   - On pointermove:
     - `delta = event.clientY - startPointerY`
     - `nextY = clamp(startSheetY + delta, fullY, collapsedY)`

4. **Separate drag and settle modes**
   - Dragging: no transition, direct rAF-batched transform updates.
   - Settling: one transform animation to the chosen snap point.

5. **Choose target using position + velocity**
   - Low velocity: nearest snap.
   - Upward velocity: bias toward fuller state.
   - Downward velocity: bias toward more collapsed state.
   - Still respect bounds and disabled states.

6. **Reduced Motion behavior**
   - No long sheet travel animation.
   - Snap position quickly, e.g. `0–80ms`.
   - Preserve feedback with handle state, selected snap indicator, subtle elevation/border change, and accessible state announcement.

7. **Replace whole-panel active scale**
   - Remove `.sheet:active { transform: scale(...) }`.
   - Use handle-only pressed affordance:
     - small color/elevation change
     - cursor/grab state
     - visible focus ring for keyboard users

8. **Make interruption safe**
   - If user grabs while settling, cancel animation and continue from current visual transform.
   - Always finalize canonical transform and semantic state.

---

## Verified / unverified boundaries

**Verified from static snippet:**
- Uses `top` for drag and animation.
- Reads `offsetTop` for snap decision.
- Has unused `startY`.
- Uses `transition: all 300ms`.
- Uses whole-sheet `:active` scale.
- Has no visible reduced-motion branch.
- Has no visible pointer capture/cancel handling.

**Not verified:**
- Actual DOM structure, handle target, snap-point math, surrounding scroll containers, browser behavior, frame rate, device feel, accessibility tree, or production CSS cascade.
- No browser, device, or runtime validation was performed.

---

## Smallest runtime validation plan

1. **Pointer lifecycle check**
   - Mouse, touch, and pen if available.
   - Verify pointer capture, cancellation, leaving viewport, and multi-touch rejection.

2. **Direct manipulation check**
   - Sheet must not jump on initial drag.
   - Finger/cursor-to-sheet offset must remain stable.

3. **Performance check**
   - Record a drag and snap.
   - Confirm transform-only updates, no repeated forced layout, no `top` animation, no transition lag.

4. **Snap intent check**
   - Slow drag near boundaries.
   - Fast upward/downward release.
   - Confirm expected collapsed/half/full outcomes.

5. **Reduced Motion check**
   - Enable reduced motion.
   - Confirm no large animated travel; state feedback remains clear.

6. **Interruption check**
   - Start snap animation, grab mid-settle, reverse direction.
   - Confirm no stuck `animating` state or visual/logical desync.
