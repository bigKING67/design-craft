## Verdict

**Evidence-labeled verdict: Block for production gesture feel.**  
From the static code, the sheet is not a direct-manipulation surface yet: it moves by layout `top`, lags via `transition: all`, ignores grab offset and velocity, locks/overrides interaction during animation, and has no Reduced Motion branch despite large spatial travel across collapsed/half/full states.

## Prioritized findings

1. **P0 — Drag is not actually 1:1.**  
   **Evidence:** `pointermove` sets `sheet.style.top = event.clientY`, while `.sheet { transition: all 300ms; }` means every drag update may be animated instead of attached to the pointer.  
   **Impact:** The sheet will feel delayed, slippery, and tiring for repeated operations use.

2. **P0 — Missing drag state and pointer capture.**  
   **Evidence:** `pointermove` runs regardless of whether a valid drag began; `pointerdown` only stores `startY`, which is never used. No `setPointerCapture`, `pointercancel`, or lost-capture handling.  
   **Impact:** Accidental pointer movement can reposition the sheet; tracking may break if the pointer leaves the element.

3. **P0 — Uses layout motion on the hot path.**  
   **Evidence:** Both drag and settle animate `top`; `pointerup` reads `sheet.offsetTop`.  
   **Impact:** Layout/reflow risk during a high-frequency gesture, especially near a large operations table.

4. **P1 — Release motion feels backwards and too slow.**  
   **Evidence:** `{ duration: 480, easing: "ease-in" }`.  
   **Impact:** `ease-in` delays the response immediately after release; 480ms is heavy for a repeatedly used sheet.

5. **P1 — Non-interruptible animation model.**  
   **Evidence:** `animating` blocks `pointerdown`, but `pointermove` can still mutate `top`; `.finished.then()` is the only unlock path.  
   **Impact:** Users cannot grab the sheet mid-settle; state can desync if animation is canceled, interrupted, or errors.

6. **P1 — Snap selection ignores velocity and intent.**  
   **Evidence:** `nearestSnapPoint(sheet.offsetTop)` uses current layout position only.  
   **Impact:** A deliberate flick toward full/half/collapsed may snap opposite to perceived intent.

7. **P1 — No Reduced Motion behavior.**  
   **Evidence:** No `prefers-reduced-motion` check or alternate settle path.  
   **Impact:** Large spatial travel remains, violating the requirement to preserve feedback without large movement.

8. **P2 — Press feedback is too blunt for a sheet.**  
   **Evidence:** `.sheet:active { transform: scale(0.96); }`.  
   **Impact:** Scaling an entire data-heavy panel can make content feel unstable and may conflict with future transform-based drag.

## Concrete direct-manipulation moves

1. Replace `top` dragging with a single transform owner: `translateY(currentY)` on the sheet or an inner motion wrapper.

2. Remove `transition: all`; scope transitions only to intentional non-gesture properties, e.g. `transform`, `opacity`, or state affordance colors.

3. Track gesture lifecycle explicitly: `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, and `grabOffset`.

4. On pointer down, capture the pointer after intent threshold and preserve offset:  
   `nextY = clamp(startSheetY + event.clientY - startPointerY, minY, maxY)`.

5. Add `touch-action: none` or a narrower `touch-action` policy on the drag handle so browser scrolling does not compete with the sheet gesture.

6. Maintain a short position/time history and compute release velocity in CSS px/s.

7. Separate target selection from settle physics:  
   - conservative rule: snap to nearest collapsed/half/full from current presentation value;  
   - optional momentum rule: choose from a bounded projected endpoint when product behavior allows flick targeting.

8. Use an interruptible settle animation that starts from the current presentation value and can be retargeted mid-flight; prefer a critically damped or lightly damped spring-like curve over fixed `ease-in`.

9. Reduced Motion: avoid large animated travel; jump or very-short-settle to the target while preserving state feedback through handle color, label/status change, subtle opacity, or a short non-spatial transform.

10. Replace full-sheet `scale(0.96)` with a calmer handle affordance: grip highlight, slight handle scale, shadow/color change, or pressed handle translation only.

## Verified / unverified boundaries

**Verified from static evidence:**  
- Layout property `top` is used for drag and settle.  
- `transition: all` applies globally to the sheet.  
- No Reduced Motion branch is present.  
- No pointer capture/cancel handling is present.  
- `startY` is stored but unused.  
- Snap target is chosen from `offsetTop`, not velocity.

**Not verified:**  
- Actual frame rate, jank, or input latency.  
- Whether CSS positioning makes `top` visually effective in the real layout.  
- Real touch feel on trackpad, mouse, or mobile hardware.  
- Whether surrounding app code clamps snap points or handles state elsewhere.  
- Assistive tech behavior, focus management, and keyboard equivalents.

## Smallest runtime validation plan

1. **Pointer lifecycle smoke:** drag from handle, leave sheet bounds, release, cancel, and re-grab during settle. Confirm no jumps.

2. **Motion feel check:** verify 1:1 tracking, grab-offset preservation, and snap to collapsed/half/full from slow drags and quick flicks.

3. **Performance check:** record a short trace while the 10,000-row table is present; confirm no layout-heavy work on every pointer move.

4. **Reduced Motion check:** enable `prefers-reduced-motion`; confirm large travel is removed or shortened while state feedback remains visible.

5. **Accessibility check:** confirm keyboard path to collapsed/half/full states, visible focus, named controls, and no focus loss during sheet state changes.
