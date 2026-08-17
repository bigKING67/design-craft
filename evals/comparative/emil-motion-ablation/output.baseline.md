## Verdict

**Evidence-labeled verdict:** **Not production-ready for a calm repeated-use operations app.**  
The implementation has the right basic intent—drag to snap—but the motion model is not direct, stable, or state-aware enough for collapsed / half / full sheet behavior, and Reduced Motion is not addressed.

---

## Prioritized findings

1. **[Code evidence] Drag is not gated by active pointer state**
   - `pointermove` always runs, even if no valid `pointerdown` occurred.
   - If `animating` blocks `pointerdown`, `pointermove` can still move the sheet.
   - Risk: accidental jumps from hover/move events or ignored-down states.

2. **[Code evidence] Movement is absolute, not relative**
   - `sheet.style.top = event.clientY`.
   - This makes the sheet’s top jump to the pointer position instead of preserving the grab offset.
   - `startY` is recorded but never used.
   - Direct manipulation should keep the sheet “attached” to the finger/cursor from the original grab point.

3. **[Code evidence] No pointer capture or cancellation handling**
   - Missing `setPointerCapture`, `pointercancel`, and lost-capture recovery.
   - Risk: sheet can get stuck or release incorrectly if the pointer leaves the element, the OS cancels input, or scrolling interrupts the gesture.

4. **[Code evidence] Layout property animation**
   - Animating `top` causes layout work and can interact poorly with CSS transitions.
   - For a frequently used sheet, `transform: translateY(...)` is the safer motion primitive.

5. **[Code evidence] CSS transition conflicts with imperative animation**
   - `.sheet { transition: all 300ms; }` can animate unrelated properties and may fight direct drag updates.
   - `transition: all` is too broad for a gesture surface.
   - During drag, the sheet should track immediately, not transition behind the pointer.

6. **[Code evidence] Animation completion state is fragile**
   - `fill: "forwards"` leaves the visual result in animation state rather than committing the final inline position.
   - `sheet.offsetTop` may not reliably represent the visual animated end state afterward.
   - Risk: later snap calculations can use stale or inconsistent geometry.

7. **[Code evidence] Fixed `480ms ease-in` is a poor snap profile**
   - `ease-in` starts slow and ends fast, which can feel like the sheet accelerates into the stop.
   - For a calm operations app, snapping should usually decelerate into rest.
   - Fixed duration ignores travel distance; a small snap and long snap should not both take 480ms.

8. **[Product evidence] No collapsed / half / full state model**
   - The snippet snaps to a target but does not store or expose the resulting sheet state.
   - Missing state feedback affects keyboard users, screen reader users, persistence, and Reduced Motion feedback.

9. **[Product evidence] Reduced Motion requirement is unmet**
   - There is no `prefers-reduced-motion` path.
   - Requirement says state feedback must remain without large spatial travel.
   - Current behavior always performs spatial travel to the target.

10. **[UX evidence] `:active { transform: scale(0.96); }` is risky**
   - Scaling the entire sheet while dragging changes perceived geometry.
   - It can make dense operational content feel unstable.
   - It also competes with transform-based movement if transform is later used for sheet position.

11. **[Interaction evidence] No velocity or intent handling**
   - Snap target appears based only on current offset.
   - A sheet should usually consider drag velocity, direction, distance crossed, and nearby snap thresholds.
   - Otherwise quick flicks and deliberate slow drags can resolve counterintuitively.

12. **[Interaction evidence] No bounds or overscroll model**
   - There is no clamp between collapsed and full limits.
   - The sheet can be dragged beyond intended positions unless `nearestSnapPoint` happens to compensate only on release.
   - Direct manipulation should constrain or intentionally resist out-of-range movement during the drag.

---

## Concrete direct-manipulation moves

1. **Use a gesture state object**
   - Track: `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, `currentY`, `lastY`, `lastTime`, `velocityY`, `currentState`.

2. **Use pointer capture**
   - On valid `pointerdown`, call `sheet.setPointerCapture(event.pointerId)`.
   - Ignore moves from other pointers.
   - Handle `pointerup`, `pointercancel`, and lost capture with the same cleanup path.

3. **Move by delta, not absolute pointer position**
   - Compute: `nextY = startSheetY + (event.clientY - startPointerY)`.
   - Clamp or resist between full and collapsed limits.

4. **Use transform for visual movement**
   - Prefer `translateY(...)` for the sheet position.
   - Avoid animating `top`.
   - Keep layout position stable and treat the sheet offset as a logical value.

5. **Disable transition during active drag**
   - Drag should have immediate 1:1 response.
   - Only the release-to-snap phase should animate.

6. **Replace `transition: all`**
   - Use explicit properties only.
   - Example intent: transform for sheet motion, opacity/color for small state feedback.
   - Do not transition layout, size, or unrelated properties by default.

7. **Use distance-aware snap timing**
   - Short travel: shorter duration.
   - Long travel: capped duration.
   - Use decelerating easing for normal motion, not `ease-in`.

8. **Use velocity-aware snap selection**
   - If velocity exceeds a threshold, snap in the gesture direction.
   - Otherwise snap to the nearest state by position.
   - This makes flicks and careful placement feel intentional.

9. **Store the resolved state**
   - After settling, commit one of: `collapsed`, `half`, `full`.
   - Update attributes such as `data-state`.
   - Use that state for visual affordances and non-motion feedback.

10. **Reduced Motion behavior**
   - If Reduced Motion is requested:
     - Avoid large animated travel.
     - Commit immediately or use a very short fade/opacity/outline/state-label change.
     - Preserve clear state feedback: handle position, state text, shadow/outline, or header affordance.
   - Do not remove feedback entirely.

11. **Replace full-sheet scale press feedback**
   - Prefer a handle highlight, slight shadow change, or header affordance.
   - If scale is used at all, apply it to a small drag handle, not the entire operational sheet.

12. **Add touch behavior contract**
   - Define `touch-action` intentionally.
   - If vertical sheet dragging owns the gesture, prevent page scroll conflicts.
   - If internal content can scroll, coordinate sheet dragging versus content scrolling.

---

## Verified / unverified boundaries

**Verified from provided code:**
- Pointer movement is not gated by an active drag.
- `startY` is unused.
- The sheet is moved and animated with `top`.
- `transition: all 300ms` is present.
- `:active` scales the sheet.
- The release animation uses `duration: 480`, `easing: "ease-in"`, and `fill: "forwards"`.
- No Reduced Motion branch is shown.
- No pointer capture/cancel handling is shown.

**Verified from product context:**
- The sheet has collapsed, half, and full states.
- The app should feel calm and is used repeatedly during the day.
- Reduced Motion must preserve state feedback without large spatial travel.

**Unverified:**
- Actual rendered dimensions.
- Existing `nearestSnapPoint` behavior.
- Whether CSS elsewhere constrains the sheet.
- Real pointer, touch, trackpad, keyboard, or assistive technology behavior.
- Runtime performance, dropped frames, or browser/device-specific behavior.

---

## Smallest runtime validation plan

1. **Gesture correctness**
   - Press near the sheet handle, drag slowly, verify no initial jump.
   - Move pointer outside the sheet, release, verify it still settles correctly.
   - Trigger cancellation path, verify no stuck dragging state.

2. **Snap behavior**
   - Test slow drags near collapsed / half / full thresholds.
   - Test quick flicks upward and downward.
   - Confirm resolved state matches user intent.

3. **Motion feel**
   - Compare short versus long snap distances.
   - Confirm the sheet decelerates into rest and does not accelerate into the final stop.
   - Confirm repeated use does not feel bouncy, jumpy, or distracting.

4. **Reduced Motion**
   - Enable Reduced Motion.
   - Change between collapsed / half / full.
   - Confirm large spatial travel is removed or minimized while state feedback remains clear.

5. **State and accessibility**
   - Confirm final state is stored and exposed in the DOM.
   - Confirm keyboard or non-drag controls can reach collapsed / half / full.
   - Confirm focus is not lost or hidden behind the sheet after state changes.

6. **Performance sanity**
   - During drag, confirm updates use transform-like visual movement rather than layout-heavy positioning.
   - Confirm no broad `transition: all` side effects occur during direct manipulation.
