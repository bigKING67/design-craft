## Verdict

**[Code evidence] Not production-ready for a calm repeated-use operations sheet.**  
The implementation visually moves something, but it does not provide reliable direct manipulation, stateful snapping, reduced-motion behavior, or performant motion. It will feel jumpy, sluggish, and fragile under real pointer use.

---

## Prioritized findings

1. **Drag is not actually state-gated**
   - **[Code evidence]** `pointermove` always runs, even if there was no valid `pointerdown`.
   - **Impact:** Mouse hover or stray pointer movement can reposition the sheet.
   - **Fix direction:** Track `isDragging`, `pointerId`, and ignore unrelated moves.

2. **The sheet jumps to the pointer instead of preserving grab offset**
   - **[Code evidence]** `startY` is recorded but never used; `top = event.clientY`.
   - **Impact:** On drag start, the sheet can snap so its top aligns with the finger/cursor, breaking direct manipulation.
   - **Fix direction:** Store `startY` and `startSheetY`; apply `startSheetY + deltaY`.

3. **No pointer capture or cancellation handling**
   - **[Code evidence]** No `setPointerCapture`, `pointercancel`, or `lostpointercapture`.
   - **Impact:** Drag can break if the pointer leaves the sheet, scrolling begins, or the browser cancels the gesture.
   - **Fix direction:** Capture the active pointer and finalize/cancel cleanly.

4. **Uses `top` for every frame**
   - **[Code evidence]** `sheet.style.top` on move; `sheet.offsetTop` on release.
   - **Impact:** Forces layout work and risks jank, especially in a dense operations UI.
   - **Fix direction:** Use `transform: translateY(...)` during drag and snap animation.

5. **Layout read/write pattern is unsafe**
   - **[Code evidence]** Writes `top`, then reads `offsetTop`.
   - **Impact:** Can force synchronous layout at release.
   - **Fix direction:** Keep a JS position model instead of reading layout as the source of truth.

6. **WAAPI `fill: "forwards"` leaves state ambiguous**
   - **[Code evidence]** The animation visually lands, but the durable style/state is not committed.
   - **Impact:** Later `offsetTop`, CSS transitions, or new animations can disagree with the visible position.
   - **Fix direction:** On finish, set the final transform/state explicitly and cancel/cleanup the animation.

7. **Easing is wrong for snapping**
   - **[Code evidence]** `duration: 480`, `easing: "ease-in"`.
   - **Impact:** Ease-in accelerates into the destination, which feels like the sheet is falling into place instead of settling. 480ms is likely too slow for repeated operational use.
   - **Fix direction:** Use responsive easing, often ease-out or spring-like; shorten and scale duration by distance.

8. **No velocity or intent detection**
   - **[Code evidence]** `nearestSnapPoint(sheet.offsetTop)` only uses final position.
   - **Impact:** A fast upward/downward fling may land in the wrong state.
   - **Fix direction:** Include velocity, direction, thresholds, and current state.

9. **No bounds or resistance**
   - **Code evidence]** `top` can be set to any `clientY`.
   - **Impact:** Sheet can overshoot beyond collapsed/full limits.
   - **Fix direction:** Clamp to valid range; optionally add subtle resistance near edges.

10. **CSS conflicts with JS animation**
    - **[Code evidence]** `.sheet { transition: all 300ms; }` plus JS `animate(...)`.
    - **Impact:** Unpredictable double-motion; unrelated property changes animate accidentally.
    - **Fix direction:** Remove `transition: all`; animate only intentional properties.

11. **Active scale undermines direct manipulation**
    - **[Code evidence]** `.sheet:active { transform: scale(0.96); }`.
    - **Impact:** Conflicts with transform-based sheet travel, shrinks content, and can feel like the sheet slips under the pointer.
    - **Fix direction:** Use handle affordance, shadow, border, or subtle background feedback instead.

12. **Reduced Motion is missing**
    - **[Product evidence]** Reduced Motion must preserve state feedback without large spatial travel.
    - **Code evidence]** No media query or runtime reduced-motion branch.
    - **Impact:** Users requesting reduced motion still get large 480ms spatial movement.
    - **Fix direction:** In reduced motion, snap with very short duration or immediate position change plus non-spatial feedback such as handle state, label, shadow, opacity, or haptic-like visual tick.

---

## Concrete direct-manipulation moves

- Track:
  - `isDragging`
  - `activePointerId`
  - `startPointerY`
  - `startSheetY`
  - `currentSheetY`
  - `currentState: "collapsed" | "half" | "full"`
  - recent pointer samples for velocity

- On `pointerdown`:
  - Ignore if already dragging.
  - Cancel/finish any running snap animation safely.
  - Capture the pointer.
  - Store starting pointer and sheet positions.
  - Mark dragging state.

- On `pointermove`:
  - Ignore if not dragging or wrong pointer.
  - Compute `deltaY = event.clientY - startPointerY`.
  - Set `nextY = clampOrResist(startSheetY + deltaY)`.
  - Apply `transform: translateY(nextY)` through a single motion path.

- On `pointerup` / `pointercancel`:
  - Determine target using position + velocity + direction.
  - Snap to collapsed, half, or full.
  - Commit final state after animation.
  - Release pointer capture and clear drag state.

- Motion tuning:
  - Use transform-only travel.
  - Use distance-aware duration, likely shorter than 480ms for nearby snaps.
  - Prefer responsive/ease-out settling over `ease-in`.
  - Avoid scaling the whole sheet while dragging.

- Reduced Motion:
  - Preserve state change.
  - Avoid large animated travel.
  - Use instant or near-instant position update.
  - Add small non-spatial confirmation: handle highlight, state label update, shadow change, or brief opacity/border feedback.

---

## Verified / unverified boundaries

- **Verified from static code:** Pointer movement is not drag-gated; `startY` is unused; `top` is animated; `transition: all` exists; reduced-motion handling is absent.
- **Verified from product context:** The component has collapsed, half, and full states; the app needs calm repeated use; reduced motion must avoid large spatial travel.
- **Not verified:** Actual DOM structure, sheet size, snap-point math, scroll containment, keyboard behavior, screen-reader labeling, real performance, browser behavior, or device touch behavior.
- **Not claimed:** No browser validation, device validation, profiling, or runtime audit was performed.

---

## Smallest runtime validation plan

1. **Pointer correctness**
   - Drag from handle and body.
   - Move pointer outside the sheet.
   - Cancel gesture mid-drag.
   - Confirm only the active pointer controls the sheet.

2. **Snap behavior**
   - Test slow drags between collapsed, half, and full.
   - Test fast upward/downward flings.
   - Confirm final visual state equals internal state.

3. **Motion quality**
   - Inspect for jump on grab.
   - Confirm no double animation from CSS transition + JS animation.
   - Confirm snap feels responsive, not delayed.

4. **Reduced Motion**
   - Enable reduced motion.
   - Confirm large spatial animation is removed or minimized.
   - Confirm state feedback still remains visible.

5. **Performance**
   - Record a drag interaction.
   - Check for layout thrash, long tasks, dropped frames, and avoidable style recalculation.
