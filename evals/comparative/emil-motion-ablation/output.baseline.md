## Evidence-labeled verdict

**Verdict: Not production-ready for a calm repeated-use operations sheet.**  
**Evidence:** The implementation moves layout with `top` on every `pointermove`, animates `top` with a slow `ease-in`, has no reduced-motion branch, no pointer capture/cancel handling, no velocity-aware snapping, and CSS applies `transition: all` plus `:active` scale. These choices make the sheet feel laggy, jumpy, and fragile under repeated direct manipulation.

---

## Prioritized findings

### P0 — Direct manipulation is not actually anchored to the user’s drag
**Evidence:** `startY = event.clientY` is recorded but never used; `pointermove` sets `sheet.style.top = event.clientY`.  
**Impact:** The sheet’s top edge jumps to the pointer position instead of preserving the grab offset. This breaks the “attached to finger/cursor” illusion.

### P0 — Motion uses layout properties instead of compositor transforms
**Evidence:** `sheet.style.top`, `sheet.offsetTop`, and WAAPI keyframes on `top`.  
**Impact:** Dragging forces layout reads/writes and can jank under a 10,000-row operations surface. Use `transform: translateY(...)` for drag and snap motion.

### P0 — Reduced Motion requirement is unmet
**Evidence:** Fixed `{ duration: 480, easing: "ease-in" }`; no `prefers-reduced-motion` branch.  
**Impact:** Large spatial travel remains mandatory. The product requirement says reduced motion must preserve state feedback without large spatial travel.

### P1 — Snap behavior ignores velocity, direction, and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only considers final position.  
**Impact:** A fast upward flick near the half point may incorrectly snap down; slow precise drags and intentional flings are treated the same.

### P1 — Animation can become inconsistent or stuck
**Evidence:** `animating = true`; `.finished.then(...)` only resets on success; no `pointercancel`, no animation cancellation, no rejection handling.  
**Impact:** If the animation is interrupted or canceled, `animating` can remain true and block future drags.

### P1 — CSS conflicts with interaction model
**Evidence:** `.sheet { transition: all 300ms; }` and `.sheet:active { transform: scale(0.96); }`.  
**Impact:** `transition: all` may animate unrelated changes and fight scripted motion. `:active` scaling shrinks content during drag, causes visual instability, and conflicts with transform-based sheet movement.

### P1 — Pointer lifecycle is incomplete
**Evidence:** No `setPointerCapture`, no pointer id tracking, no `pointercancel`, no bounds checking, no “dragging” guard in `pointermove`.  
**Impact:** Movement can continue without a valid drag start, lose control when the pointer leaves the sheet, and mishandle multi-pointer cases.

### P2 — Motion language is too heavy for calm operations use
**Evidence:** 480ms `ease-in` snap.  
**Impact:** `ease-in` accelerates toward the end, which can feel unresponsive at release and abrupt near arrival. For repeated work, snaps should feel immediate, stable, and predictable.

### P2 — Accessibility/state semantics are absent
**Evidence:** No explicit collapsed/half/full state model exposed to keyboard or assistive tech.  
**Impact:** Gesture-only operation excludes keyboard-heavy users and makes state recovery unclear.

---

## Concrete direct-manipulation moves

1. **Use a real state model**
   - Track `currentState: "collapsed" | "half" | "full"`.
   - Store snap points as measured pixel offsets or CSS variables.
   - Commit state after every snap.

2. **Drag with transform, not top**
   - Keep layout position stable.
   - Apply `transform: translateY(var(--sheet-y))`.
   - During drag, update only the transform value.

3. **Preserve grab offset**
   - On `pointerdown`, record:
     - pointer id
     - start pointer Y
     - current sheet Y
   - On `pointermove`, calculate `nextY = startSheetY + event.clientY - startPointerY`.

4. **Clamp movement**
   - Constrain between full and collapsed snap points.
   - Optionally add small resistance beyond bounds, but do not let the sheet freely escape.

5. **Capture the pointer**
   - Use pointer capture on drag start.
   - Ignore moves from other pointer ids.
   - Handle `pointerup`, `pointercancel`, and lost capture the same way.

6. **Use velocity-aware snapping**
   - If release velocity exceeds a threshold, bias toward the next state in the drag direction.
   - Otherwise snap to the nearest state with hysteresis so small accidental moves do not change state.

7. **Use calm snap timing**
   - Prefer a responsive decelerating curve, not `ease-in`.
   - Shorter duration for short travel, bounded duration for long travel.
   - Example behavior: quick settle for nearby snap, slightly longer but still controlled settle for full travel.

8. **Remove `transition: all`**
   - Limit transitions to intentional properties only.
   - Do not let CSS transitions implicitly animate layout, size, color, or transform during drag.

9. **Remove active scale from the whole sheet**
   - If feedback is needed, apply it to the grab handle only.
   - Better: use handle color, shadow, or subtle affordance change instead of shrinking the full panel.

10. **Reduced Motion behavior**
   - Avoid large animated travel.
   - On release, snap immediately or with a very short duration.
   - Preserve feedback through state label, handle emphasis, shadow change, or brief non-spatial highlight.

11. **Keyboard parity**
   - Provide controls for collapsed/half/full.
   - Ensure focus is not lost when state changes.
   - Expose the current state with accessible naming or state text.

---

## Verified / unverified boundaries

**Verified from static code only**
- Drag writes `top` on every `pointermove`.
- `startY` is unused.
- Snap animation uses `top`, `480ms`, and `ease-in`.
- Reduced Motion handling is absent.
- CSS uses `transition: all`.
- CSS scales the entire sheet on `:active`.
- Pointer capture, cancel handling, velocity, and keyboard handling are not shown.

**Unverified**
- Actual frame rate or jank on target devices.
- Whether surrounding code adds accessibility semantics.
- Whether `nearestSnapPoint` includes bounds, hysteresis, or state persistence.
- Whether CSS elsewhere overrides this behavior.
- Real browser/device behavior under touch, pen, trackpad, or assistive technology.

---

## Smallest runtime validation plan

1. **Drag fidelity**
   - Press on handle, move slowly, confirm the sheet stays attached without jumping.

2. **Snap intent**
   - Test slow drags and fast flicks between collapsed, half, and full.
   - Confirm direction and velocity affect the final state predictably.

3. **Performance**
   - Record a drag while the large table is present.
   - Check for layout thrash, long frames, and dropped frames.

4. **Reduced Motion**
   - Enable reduced motion.
   - Confirm state changes still provide feedback without large animated travel.

5. **Pointer resilience**
   - Drag outside the sheet, cancel mid-drag, use multi-pointer input.
   - Confirm the sheet recovers and remains interactive.

6. **Keyboard/accessibility**
   - Navigate and change states using keyboard only.
   - Confirm visible focus, state announcement or label, and stable focus after snapping.
