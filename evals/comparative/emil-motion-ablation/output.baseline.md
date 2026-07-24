## Evidence-labeled verdict

**Verdict: Not production-ready for a calm repeated-use operations sheet.**  
**Static evidence:** the implementation animates `top`, uses `transition: all`, ignores reduced motion, has no drag state/pointer capture, and uses a long `ease-in` settle.  
**Likely user impact:** laggy direct manipulation, accidental jumps, scroll/drag conflicts, inaccessible state changes, and excessive spatial motion for Reduced Motion users.

---

## Prioritized findings

### P0 — Direct manipulation is broken
**Evidence:** `pointermove` always sets `sheet.style.top = event.clientY`.  
**Problem:** the sheet jumps to the pointer’s viewport Y instead of preserving the grab offset. `startY` is stored but unused.  
**Impact:** the panel will feel detached from the finger/mouse, especially when grabbed from different vertical positions.

### P0 — No drag ownership or cancellation model
**Evidence:** no `dragging` flag, no `setPointerCapture`, no `pointercancel`, no `lostpointercapture`.  
**Problem:** moves can apply without a valid drag, and the interaction can get stuck or leak across pointers.  
**Impact:** unreliable under touch, stylus, trackpad, iframe boundaries, browser gestures, or interrupted drags.

### P0 — Motion uses layout properties instead of compositor-safe transforms
**Evidence:** `style.top`, `offsetTop`, WAAPI over `top`, and `.sheet { transition: all 300ms; }`.  
**Problem:** `top` triggers layout; `offsetTop` forces layout reads; `transition: all` can accidentally animate drag updates.  
**Impact:** frame drops are likely on a dense operations surface, especially beside a large table.

### P0 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` handling; settle duration is always `480ms`; spatial travel remains full.  
**Problem:** Reduced Motion must preserve state feedback without large travel.  
**Impact:** fails a stated product requirement and may cause discomfort.

### P1 — Snap behavior lacks intent modeling
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` only considers position.  
**Problem:** no velocity, direction, hysteresis, thresholds, or “commit/cancel” distinction.  
**Impact:** sheet may snap contrary to user intent, especially with quick flicks or near the midpoint.

### P1 — Easing and duration are wrong for an operational sheet
**Evidence:** `{ duration: 480, easing: "ease-in" }`.  
**Problem:** `ease-in` starts slowly and accelerates into the destination, which feels like the sheet is slipping away.  
**Impact:** not calm or responsive. Repeated use will feel sluggish and imprecise.

### P1 — Animation state can desynchronize from DOM state
**Evidence:** WAAPI uses `fill: "forwards"` but does not commit the final `top` to the element’s actual style/model.  
**Problem:** visual state and logical state can diverge across later reads, resize, rerender, or style changes.  
**Impact:** future snaps may start from stale or inconsistent positions.

### P1 — CSS conflicts with JS motion
**Evidence:** `.sheet { transition: all 300ms; }` plus `sheet.animate(...)`.  
**Problem:** global transition can compete with drag writes and WAAPI animations.  
**Impact:** double easing, delayed pointer tracking, hard-to-debug motion artifacts.

### P1 — `:active` scale damages spatial continuity
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Problem:** scaling the whole sheet during drag changes perceived position and can make content visually pulse.  
**Impact:** hostile to precision use; conflicts with transform-based sheet movement unless composed carefully.

### P2 — Missing accessibility state and alternate controls
**Evidence:** no role/state updates, keyboard handling, labels, or focus behavior shown.  
**Problem:** collapsed/half/full states need non-pointer operation and announced state changes.  
**Impact:** keyboard-heavy operators and assistive tech users cannot reliably operate the sheet.

---

## Concrete direct-manipulation moves

1. **Use an explicit interaction state**
   - Track `isDragging`, `pointerId`, `startPointerY`, `startSheetY`, and current snap state.
   - Ignore unrelated pointers.
   - Handle `pointercancel` and `lostpointercapture`.

2. **Capture the pointer on drag start**
   - On `pointerdown`, call `setPointerCapture(event.pointerId)`.
   - Add `touch-action: none` or a narrower value only on the drag handle, not necessarily the whole sheet.

3. **Move with `transform`, not `top`**
   - Represent position as `translateY(...)`.
   - Keep snap positions in a model value.
   - Avoid layout reads during drag.

4. **Make drag 1:1**
   - `nextY = clamp(startSheetY + event.clientY - startPointerY, fullY, collapsedY)`.
   - Apply immediately via `transform`.
   - Batch pointer updates with `requestAnimationFrame` if needed.

5. **Disable CSS transition during drag**
   - Use classes such as `.is-dragging` and `.is-settling`.
   - Never use `transition: all`.
   - Transition only the intended property: `transform`.

6. **Snap by intent, not only distance**
   - Use position + velocity + direction.
   - Add hysteresis so the sheet does not jitter between half/full near boundaries.
   - Example intent: fast upward flick promotes to fuller state; fast downward flick demotes.

7. **Use responsive settle motion**
   - Prefer a short, decelerating or spring-like settle.
   - Avoid `ease-in`.
   - Duration should scale with remaining distance but stay bounded.

8. **Implement Reduced Motion as state feedback, not travel**
   - For reduced motion, shorten duration dramatically or jump position.
   - Preserve feedback through opacity, border, shadow, handle color, status text, or subtle 80ms affordance.
   - Do not animate large vertical travel.

9. **Commit final state**
   - After settle, set the canonical state: `collapsed | half | full`.
   - Commit the final transform/model value.
   - Update ARIA/state labels from the same source of truth.

10. **Keep press feedback separate from sheet position**
   - Replace full-sheet `scale(0.96)` with a subtle handle/button affordance.
   - If scale is used, compose transforms carefully and disable it during drag.

---

## Verified / unverified boundaries

**Verified from static code:**
- `top` is used for drag and animation.
- `transition: all` is present.
- `startY` is unused.
- no reduced-motion branch is present.
- no pointer capture/cancel handling is present.
- no keyboard or semantic state handling is shown.
- settle uses `480ms ease-in`.

**Not verified:**
- actual frame rate or input latency.
- behavior on real touch hardware.
- behavior inside the full product layout.
- interaction with scrolling containers.
- whether surrounding code adds accessibility, state, or resize handling.
- whether `nearestSnapPoint` clamps, debounces, or understands velocity.

---

## Smallest runtime validation plan

1. **Pointer correctness**
   - Drag from handle, middle, and lower sheet area.
   - Confirm no initial jump and 1:1 pointer tracking.

2. **Snap intent**
   - Slow drag near each midpoint.
   - Fast flick up/down.
   - Confirm expected collapsed/half/full result.

3. **Interruption handling**
   - Start drag, leave viewport, cancel gesture, multi-touch, release outside sheet.
   - Confirm no stuck dragging or stale animation lock.

4. **Performance smoke**
   - Record a drag and settle on a dense page.
   - Check for layout thrash, long tasks, dropped frames, and forced reflow around `pointermove`.

5. **Reduced Motion**
   - Enable reduced motion.
   - Confirm state still changes clearly but without large animated travel.

6. **Keyboard and assistive flow**
   - Operate collapsed/half/full without pointer.
   - Confirm focus order, visible focus, labels, and announced state.
