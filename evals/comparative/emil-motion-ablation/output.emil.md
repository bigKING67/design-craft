## Evidence-labeled verdict

**Verdict: not production-ready for a calm repeated-use operations sheet.**  
**Static evidence:** the implementation moves a layout property (`top`) directly from `event.clientY`, uses a fixed `ease-in` animation, blocks interaction with `animating`, has no velocity/projection model, no pointer capture, no reduced-motion branch, and a broad `transition: all`. The result is likely jumpy, laggy, non-interruptible, and inaccessible for a collapsed/half/full bottom sheet.

---

## Prioritized findings

### P0 — Drag is not true direct manipulation
**Evidence:** `startY = event.clientY` is recorded but never used; `pointermove` sets `sheet.style.top = event.clientY`.  
**Impact:** the sheet will jump so its top aligns to the pointer, ignoring where the user grabbed it. It also updates on every pointer move over the sheet, not only during an active drag.  
**Fix direction:** track `isDragging`, grab offset, current sheet position, and apply `current + delta`.

### P0 — Motion is non-interruptible
**Evidence:** `if (animating) return` on `pointerdown`; animation promise resets `animating` only after completion.  
**Impact:** users cannot grab a moving sheet and redirect it. In a repeated operations workflow, this makes the UI feel locked and slow.  
**Fix direction:** allow interruption, cancel the current animation, read the live presentation position, and continue from there.

### P0 — Uses layout properties on the input path
**Evidence:** `sheet.style.top`, `sheet.offsetTop`, and WAAPI animating `top`.  
**Impact:** `top` can trigger layout/reflow; `offsetTop` reads layout; this is risky during pointermove and for large inventory screens.  
**Fix direction:** animate only `transform: translateY(...)`; store logical snap state separately.

### P1 — Release behavior ignores velocity and intent
**Evidence:** `nearestSnapPoint(sheet.offsetTop)` chooses from current position only.  
**Impact:** a fast flick toward full/closed may snap backward if the release point is closer to another state.  
**Fix direction:** compute release velocity, project the likely resting point, then choose collapsed/half/full from that projected endpoint.

### P1 — Easing and duration are wrong for a sheet
**Evidence:** `{ duration: 480, easing: "ease-in" }`.  
**Impact:** `ease-in` starts slowly and accelerates into the target, which feels like the sheet is running away at the end. 480ms is also heavy for repeated operational use.  
**Fix direction:** use a responsive decelerating/spring-like settle, usually faster, with velocity handoff and little/no bounce unless the user flicked.

### P1 — CSS conflicts with gesture motion
**Evidence:** `.sheet { transition: all 300ms; }` and `.sheet:active { transform: scale(0.96); }`.  
**Impact:** `transition: all` may animate unrelated properties and interfere with JS-driven movement. `:active` scaling the whole sheet during drag can make content shrink under the pointer and will conflict if `transform` is also used for translate.  
**Fix direction:** remove `transition: all`; transition only intentional non-gesture properties. Prefer subtle handle, shadow, or scrim feedback instead of scaling the whole sheet.

### P1 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` handling; large spatial travel remains.  
**Impact:** reduced-motion users still get full sheet travel and easing.  
**Fix direction:** preserve state feedback with short opacity/color/handle changes, instant or very short snap, and no overshoot/large animated travel.

### P2 — Pointer lifecycle is incomplete
**Evidence:** no `setPointerCapture`, no `pointercancel`, no `lostpointercapture`, no pointer id tracking.  
**Impact:** dragging can break when the pointer leaves the sheet, when scrolling begins, or when another pointer is introduced.  
**Fix direction:** capture the active pointer, ignore non-active pointers, clean up on cancel/lost capture.

### P2 — Snap states are not represented as accessible state
**Evidence:** code calculates a pixel target but shows no collapsed/half/full state model.  
**Impact:** keyboard users and assistive tech may not know or control the current sheet state.  
**Fix direction:** expose state through semantic controls, labels, keyboard commands, focus management, and visible state feedback.

---

## Concrete direct-manipulation moves

1. **On pointer down**
   - Set `isDragging = true`.
   - Capture pointer.
   - Cancel any running animation.
   - Read the current visual `translateY`.
   - Store `startPointerY`, `startSheetY`, and grab offset.

2. **On pointer move**
   - Only respond if `isDragging` and pointer id matches.
   - Compute `nextY = startSheetY + (event.clientY - startPointerY)`.
   - Apply `transform: translateY(nextY)` inside `requestAnimationFrame`.
   - Record recent `{ y, time }` samples for velocity.

3. **At bounds**
   - Do not hard-stop.
   - Apply progressive resistance past collapsed/full limits so the sheet still follows, but more slowly.

4. **On release**
   - Compute release velocity from recent samples.
   - Project endpoint from velocity.
   - Choose nearest snap among collapsed, half, full using the projected endpoint, not only current position.
   - Animate from current visual position to target with velocity handoff.

5. **During animation**
   - Keep it interruptible.
   - A new pointer down should stop/re-target the current motion immediately.

6. **For reduced motion**
   - Avoid large animated travel.
   - Snap position immediately or in a very short duration.
   - Preserve feedback through handle color, elevation, opacity, state label, or brief non-spatial emphasis.

7. **For calm operations use**
   - Avoid bouncy decoration by default.
   - Use predictable critically damped settling.
   - Keep feedback subtle, fast, and consistent across collapsed/half/full.

---

## Verified / unverified boundaries

**Verified from static code:**
- Drag uses `top`, not `transform`.
- `startY` is unused.
- Pointer move is not gated by an active drag flag.
- Animation uses fixed `480ms ease-in`.
- Snap target is based on `offsetTop`, not projected velocity.
- Animation is locked by `animating`.
- CSS uses `transition: all`.
- No reduced-motion branch is present in the snippet.

**Not verified without runtime/device testing:**
- Actual frame rate or layout cost.
- Whether the sheet visibly jumps in the current DOM positioning context.
- Whether scrolling conflicts occur on touch hardware.
- Whether WAAPI `fill: forwards` causes state mismatch in this exact layout.
- Whether focus management or keyboard controls exist elsewhere.
- Whether snap points are visually correct across viewport sizes.

---

## Smallest runtime validation plan

1. **Pointer continuity**
   - Drag from handle, body, and edge.
   - Confirm no initial jump and no movement before active drag.

2. **Interruptibility**
   - Release toward half/full, then grab mid-animation.
   - Confirm the sheet immediately follows the pointer without waiting.

3. **Velocity intent**
   - Slow drag near midpoint.
   - Fast flick toward each state.
   - Confirm snap target follows intent, not just nearest release position.

4. **Performance smoke**
   - Record one drag interaction.
   - Check for layout thrash, long tasks, and dropped frames during pointermove.

5. **Reduced motion**
   - Enable reduced motion.
   - Confirm collapsed/half/full state changes remain understandable without large spatial travel.

6. **Accessibility basics**
   - Keyboard open/collapse/expand.
   - Focus remains visible and logical.
   - Current sheet state is announced or otherwise perceivable.
