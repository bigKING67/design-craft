## Evidence-labeled verdict

**Verdict: Not production-ready for a calm, repeatedly used three-state sheet.**  
**Evidence:** Static code inspection shows broken direct-manipulation mapping, conflicting CSS/JS motion, no active pointer lifecycle, no reduced-motion path, and layout-driven animation that can feel laggy or abrupt.  
**Boundary:** This is a static critique only; no browser, device, or runtime validation was performed.

---

## Prioritized findings

### P0 — Drag can mutate without an active gesture
**Evidence:** `pointermove` always runs `sheet.style.top = ...`; it does not check `dragging`, `pointerId`, or `animating`.  
**Impact:** Hover/move events, stray pointers, or moves after cancellation can reposition the sheet unexpectedly.  
**Fix direction:** Track `dragging`, capture the initiating pointer, ignore all other pointers, and clear state on `pointerup`, `pointercancel`, and lost capture.

### P0 — Finger-to-sheet mapping is wrong
**Evidence:** `startY` is stored but never used; `top` is set directly to `event.clientY`.  
**Impact:** The sheet jumps so its top edge snaps to the pointer, instead of preserving the grab offset. This violates direct manipulation.  
**Fix direction:** On down, record `baseY` and `grabY`; on move, apply `baseY + (event.clientY - grabY)`.

### P0 — Reduced Motion requirement is unmet
**Evidence:** Every release animates spatial travel for `480ms`; CSS also scales the sheet on active press.  
**Impact:** Users requesting reduced motion still get large movement and scale changes.  
**Fix direction:** Under reduced motion, avoid long travel: snap state immediately or use a very short non-spatial cue such as handle color, elevation, label update, or subtle opacity/state indicator.

### P1 — CSS transition conflicts with gesture and WAAPI animation
**Evidence:** `.sheet { transition: all 300ms; }` applies during every `top` write and can also conflict with `sheet.animate(...)`.  
**Impact:** Drag may lag behind the pointer; unrelated properties may animate accidentally; motion becomes hard to reason about.  
**Fix direction:** Remove `transition: all`; only transition explicit non-gesture properties, and disable transitions while dragging.

### P1 — Animating `top` causes layout work
**Evidence:** Both drag and snap manipulate `top`; `offsetTop` is read after layout-affecting writes.  
**Impact:** Repeated layout/reflow risk, especially during pointermove.  
**Fix direction:** Use `transform: translateY(...)` for the moving layer, schedule writes through `requestAnimationFrame`, and keep layout reads outside hot paths.

### P1 — Snap behavior ignores velocity, direction, and hysteresis
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` appears distance-only.  
**Impact:** A purposeful upward fling may collapse back if it ends near the prior state; tiny accidental moves may change state.  
**Fix direction:** Use distance plus velocity/direction thresholds, minimum drag distance, and hysteresis around collapsed/half/full states.

### P1 — Animation feel is mismatched to product tone
**Evidence:** `duration: 480` and `easing: "ease-in"` means the sheet accelerates into its destination.  
**Impact:** Feels heavy, late, and potentially abrupt at rest; repeated daily use will feel tiring.  
**Fix direction:** Prefer shorter distance-scaled timing, e.g. ~180–300ms, with ease-out or spring-like settling without bounce.

### P1 — Interaction cannot be interrupted cleanly
**Evidence:** `if (animating) return` blocks new starts; the created animation is not stored or canceled.  
**Impact:** If the user changes intent mid-snap, the UI ignores them. If animation is canceled externally, `finished.then(...)` may not restore state.  
**Fix direction:** Keep the active animation handle, cancel/commit it on new pointerdown, and use `finally`/cancel handling to clear locks.

### P2 — `fill: "forwards"` can leave stale underlying state
**Evidence:** The animation fills visually, but the final `style.top` is not explicitly committed after finish.  
**Impact:** Future reads/writes may start from stale style state or conflict with later transitions.  
**Fix direction:** On finish, set the canonical state position in style/state, then cancel or replace the animation effect.

### P2 — Bounds and container coordinates are unspecified
**Evidence:** `event.clientY` is viewport-relative; no clamp is visible.  
**Impact:** The sheet can be dragged outside intended collapsed/full limits, especially inside nested containers, resized viewports, or mobile browser chrome changes.  
**Fix direction:** Convert pointer coordinates into the sheet container’s coordinate space and clamp between full and collapsed offsets.

### P2 — Press scale harms calm direct manipulation
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** Scaling the whole sheet can make content pulse, shift hit targets, and conflict with transform-based positioning.  
**Fix direction:** Keep the sheet stable; apply small feedback to the handle only, or use color/elevation changes.

---

## Concrete direct-manipulation moves

1. Model explicit states: `collapsed`, `half`, `full`, plus current `y`.
2. On `pointerdown`: cancel any snap animation, capture pointer, record `baseY`, `startClientY`, and current state.
3. On `pointermove`: if active pointer, compute `nextY = clamp(baseY + deltaY)`.
4. Apply movement with `transform: translateY(...)`, not `top`.
5. Add soft resistance only beyond bounds, not inside normal state range.
6. On release: choose target using position + velocity + hysteresis.
7. Snap with distance-scaled ease-out motion; no bounce for this product tone.
8. Under reduced motion: commit target quickly and provide non-spatial state feedback.
9. Keep active state feedback localized to the drag handle, not the whole sheet.
10. Ensure `pointercancel` and lost capture restore or settle to the nearest valid state.

---

## Verified / unverified boundaries

**Verified by static inspection:**
- `startY` is unused.
- `pointermove` has no active-drag guard.
- `top` is used for gesture and animation.
- CSS uses `transition: all`.
- CSS scales the whole active sheet.
- No visible reduced-motion branch.
- No visible pointer capture/cancel handling.
- No visible velocity, hysteresis, or bounds logic.

**Unverified:**
- Actual `nearestSnapPoint` behavior.
- Actual DOM positioning context.
- Real frame rate or input latency.
- Browser/device behavior.
- Accessibility state, keyboard support, focus handling, and ARIA outside this snippet.
- Whether additional code elsewhere mitigates these issues.

---

## Smallest runtime validation plan

1. Instrument pointer lifecycle: down/move/up/cancel, active pointer id, current state, target state.
2. Test three gestures only: slow drag, short accidental drag, fast fling.
3. Check interruption: start a snap, then drag again before it finishes.
4. Check bounds: drag past full and collapsed limits.
5. Check reduced motion: confirm no long spatial snap and that state feedback remains visible.
6. Measure one hot path: pointermove should not force layout every frame.
7. Verify state after animation: visual position and canonical state must match.
