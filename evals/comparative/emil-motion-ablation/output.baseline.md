## Evidence-labeled verdict

**Verdict [code + CSS evidence]: Not production-fit as-is.**  
The implementation is likely to feel jumpy, laggy, and spatially heavy, which conflicts with a calm operations app used repeatedly throughout the day. It also lacks reliable state handling for collapsed / half / full and does not satisfy the Reduced Motion requirement.

---

## Prioritized findings

### P0 — Reduced Motion is missing
**Evidence:** No `prefers-reduced-motion` handling; animation always travels spatially for `480ms`.  
**Impact:** Users who request reduced motion still get large sheet travel.  
**Expected:** State feedback should remain, but large travel should be removed or minimized.

### P0 — Drag is not true direct manipulation
**Evidence:** `pointermove` sets `sheet.style.top = event.clientY`.  
**Impact:** The sheet top snaps to the pointer’s viewport Y instead of preserving the grab offset. This causes jumps, especially when grabbing below the top edge.  
**Expected:** Movement should be based on `deltaY` from pointerdown and clamped to snap bounds.

### P0 — CSS transition fights pointer movement
**Evidence:** `.sheet { transition: all 300ms; }` while JS updates `top` on every move.  
**Impact:** The sheet will chase the finger instead of staying attached to it. This creates lag and imprecision.  
**Expected:** Disable transitions while dragging; animate only on release.

### P0 — Pointer lifecycle is incomplete
**Evidence:** No `setPointerCapture`, no active-drag flag, no `pointercancel`, no primary-pointer check.  
**Impact:** The sheet can keep moving after an unintended pointer sequence, miss release events, or react to stray moves.  
**Expected:** Track one active pointer, capture it, and clean up on `pointerup` / `pointercancel`.

### P1 — Animation state can become inconsistent
**Evidence:** `animating` only blocks `pointerdown`; `pointermove` and `pointerup` can still run.  
**Impact:** A user can mutate position during an animation or trigger new release logic without a valid drag.  
**Expected:** Ignore moves/up unless actively dragging, and cancel/commit existing animations deliberately.

### P1 — `top` causes layout work on every frame
**Evidence:** Per-move writes to `style.top`; release reads `sheet.offsetTop`.  
**Impact:** Layout-bound motion is more likely to stutter than compositor motion.  
**Expected:** Use `transform: translateY(...)` for drag and settle motion.

### P1 — Release motion feels wrong for a calm utility surface
**Evidence:** `duration: 480`, `easing: "ease-in"`.  
**Impact:** `ease-in` accelerates into the snap point and can feel abrupt at the end. `480ms` may feel slow for repeated daily use.  
**Expected:** Use distance-aware duration and an ease-out / critically damped curve with no bounce.

### P1 — Snap decision ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only uses position.  
**Impact:** A deliberate upward or downward flick may snap opposite to user intent.  
**Expected:** Use current position plus velocity projection, with clear thresholds for collapsed / half / full.

### P1 — Whole-sheet `:active` scale is disruptive
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** The content compresses under the pointer, visual anchors shift, and it may conflict with transform-based dragging.  
**Expected:** Prefer subtle handle, shadow, scrim, or state-label feedback instead of scaling the entire sheet.

### P2 — `transition: all` is too broad
**Evidence:** CSS transitions every animatable property.  
**Impact:** Future style changes may animate unintentionally, including color, size, shadow, or layout properties.  
**Expected:** Restrict transitions to intentional properties only.

### P2 — No bounds or viewport/safe-area handling shown
**Evidence:** Drag target is raw `clientY`.  
**Impact:** Sheet can be dragged beyond valid collapsed/full limits.  
**Expected:** Clamp to snap range and account for viewport changes and safe areas.

### P2 — Accessibility/state semantics are absent
**Evidence:** Pointer-only implementation; no visible state model shown.  
**Impact:** Keyboard and assistive-technology users may not be able to operate or understand sheet state.  
**Expected:** Provide keyboard controls, focus behavior, and clear state feedback for collapsed / half / full.

---

## Concrete direct-manipulation moves

1. **Track drag state explicitly**
   - On `pointerdown`: require primary pointer, store `pointerId`, capture pointer, cancel any running animation.
   - Store `startPointerY`, `startSheetY`, and current snap state.

2. **Move by delta, not absolute pointer position**
   - On `pointermove`: if active pointer, compute  
     `nextY = clamp(startSheetY + event.clientY - startPointerY, fullY, collapsedY)`.

3. **Use compositor motion**
   - Apply movement with `transform: translate3d(0, nextY, 0)` or a CSS variable driving transform.
   - Avoid `top` during drag.

4. **Disable transitions while dragging**
   - Add an `.is-dragging` class with `transition: none`.
   - Re-enable settle animation only after release.

5. **Snap using intent**
   - On release, calculate velocity from recent pointer samples.
   - Project position slightly forward.
   - Choose collapsed / half / full using both projected position and direction.

6. **Use calm release motion**
   - Prefer short, distance-based duration, e.g. roughly `160–280ms`.
   - Use ease-out or a damped spring without bounce.
   - Avoid `ease-in` for sheet settling.

7. **Preserve state feedback in Reduced Motion**
   - Immediately set the final state or use very short motion.
   - Use non-spatial feedback: handle color, shadow depth, label, border emphasis, or scrim opacity.
   - Avoid large sheet travel animation.

8. **Replace whole-sheet active scale**
   - Remove `scale(0.96)` from the entire sheet.
   - If feedback is needed, animate only the drag handle or surface elevation subtly.

9. **Commit final state**
   - After settle, write the final transform/state as the source of truth.
   - Clear/cancel animation objects so later drags start from a stable value.

---

## Verified / unverified boundaries

**Verified from provided code:**
- No Reduced Motion branch is present.
- Drag uses `top` and raw `clientY`.
- CSS uses `transition: all`.
- Release easing is `ease-in`.
- `startY` is assigned but not used.
- No pointer capture or cancel handling is shown.

**Unverified from provided code:**
- Actual visual frame rate.
- Whether `sheet` is absolutely/fixed positioned.
- Exact snap-point values.
- Existing keyboard/ARIA behavior elsewhere.
- Real device behavior, browser behavior, or touch-scroll conflicts.
- Whether other code prevents conflicting pointer events.

---

## Smallest runtime validation plan

1. **Pointer lifecycle**
   - Drag from handle, content area, and near sheet edge.
   - Release inside and outside the sheet.
   - Trigger `pointercancel` path if supported.

2. **Motion feel**
   - Slow drag to each state.
   - Fast flick upward/downward.
   - Verify snap matches user intent.

3. **Directness**
   - Confirm sheet stays attached to the finger/pointer with no lag while dragging.
   - Confirm no jump on initial grab.

4. **Reduced Motion**
   - Enable reduced motion.
   - Verify final state changes remain clear without large spatial travel.

5. **Bounds/state**
   - Try dragging past collapsed and full limits.
   - Confirm final state is always one of collapsed / half / full.

6. **Keyboard/accessibility**
   - Operate equivalent controls without pointer.
   - Confirm focus remains predictable after state changes.
