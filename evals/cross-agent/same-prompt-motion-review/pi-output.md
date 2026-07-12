## 1. Evidence level and design read

**Evidence level:** Static-code review only. I can identify implementation risks and policy violations from the provided JS/CSS, but I cannot verify perceived smoothness, frame rate, touch feel, computed style conflicts, or Reduced Motion behavior without runtime evidence.

**Design read:** Reading this as a high-frequency web operations bottom sheet for focused task work, with calm utility motion optimized for direct manipulation, context preservation, and predictable state changes.

## 2. Should this motion exist?

**Yes, but only narrowly.**

Motion should exist for:

- Immediate pointer-down acknowledgement.
- Continuous 1:1 drag tracking.
- A short settle from release position to the chosen snap state.
- State feedback for `collapsed`, `half`, and `full`.

Motion should **not** exist as:

- Decorative whole-sheet scaling.
- Delayed `ease-in` settling.
- `transition: all`.
- Animated layout `top` during drag.
- Input lockout while the sheet is settling.
- Large spatial travel under Reduced Motion.

## 3. Prioritized blocking findings

1. **Drag is not 1:1 and likely lags behind the pointer.**  
   `transition: all 300ms` means `top` changes from `pointermove` may transition instead of tracking immediately. A dragged sheet must stay attached to the finger/cursor after intent is established.

2. **The sheet jumps to the pointer because grab offset is not preserved.**  
   `sheet.style.top = event.clientY` ignores where inside the sheet the user grabbed. This breaks direct manipulation because the object repositions under the pointer instead of preserving the initial relationship.

3. **Input is locked during animation instead of being interruptible.**  
   `if (animating) return` rejects new grabs while the sheet is settling. A draggable sheet must be interruptible from the current presentation value, not blocked until a prior animation finishes.

4. **Release physics are wrong for a snap sheet.**  
   Snap target is chosen from `sheet.offsetTop` only. There is no measured velocity, projected endpoint, hysteresis, or velocity handoff, so quick flicks and slow drags can resolve to unintuitive states.

5. **Motion ownership and properties are unsafe.**  
   JS/WAAPI animate `top`, CSS transitions `all`, and `:active` writes `transform: scale(0.96)`. This mixes layout animation, broad transitions, and transform feedback. It risks lag, jank, visual mismatch, and future transform conflicts.

## 4. Concrete design moves

1. **Pointer-down feedback:**  
   Use subtle handle/content affordance only: e.g. handle color/opacity change or tiny scale on the grab handle, not `scale(0.96)` on the full sheet. Keep it immediate, around `100–160ms`.

2. **1:1 tracking:**  
   Disable transitions during active drag. Track with `transform: translateY(...)` or an explicit sheet position variable driven per frame. Preserve `grabOffset = pointerY - sheetTop`.

3. **Presentation-value interruption:**  
   On pointer down during settle, cancel the current animation, read the current visual position, and begin the drag from that presentation value. Do not ignore the input.

4. **Velocity handoff:**  
   Keep a short pointer history with timestamps in CSS px. On release, compute velocity in px/s and pass that velocity into the settle animation/spring.

5. **Projected endpoint snap:**  
   Choose `collapsed`, `half`, or `full` from a projected endpoint, not just the release position. This lets quick flicks feel intentional.

6. **Settle animation:**  
   Use a spring-like settle or equivalent curve: calm, mostly critically damped, no theatrical bounce. For this operations app, target roughly `250–350ms` perceived response, with `ease-out`/drawer-like easing if not using a spring. Avoid `ease-in`.

7. **Soft boundaries:**  
   Clamp normal range to the snap limits, but add progressive resistance when pulling beyond min/max. Avoid hard stops while dragging.

8. **Reduced Motion:**  
   Preserve state feedback without large travel: snap state should update immediately or with a very short fade/color/handle-state change. Remove elastic overshoot, long travel, and scale effects.

## 5. Verified versus unverified claims

**Verified from static code:**

- `top` is updated directly on every `pointermove`.
- `top` is animated with WAAPI for `480ms` using `ease-in`.
- CSS applies `transition: all 300ms`.
- CSS applies whole-sheet `transform: scale(0.96)` on `:active`.
- New pointer-down is ignored while `animating` is true.
- Snap target uses current `offsetTop`, with no visible velocity/projection logic.
- No `prefers-reduced-motion` branch is shown.
- No pointer capture, drag threshold, grab-offset use, or boundary resistance is shown.

**Unverified / runtime hypotheses:**

- Actual drag lag and frame rate.
- Whether CSS transition and WAAPI conflict in the target browser.
- Whether `offsetTop` matches the visual presentation value after `fill: forwards`.
- Touch behavior on mobile hardware.
- Responsiveness across viewport sizes.
- Reduced Motion behavior in a real browser.
- Whether the sheet loses events when the pointer leaves its bounds.

## 6. Minimal validation plan before approval

1. **Desktop browser pointer trace:** verify pointer-down feedback, grab offset, 1:1 tracking, and interruption while settling.  
2. **Touch device test:** verify finger tracking, pointer capture, scroll/drag conflict, and boundary behavior.  
3. **Reduced Motion run:** confirm no large animated travel, overshoot, or whole-sheet scaling.  
4. **Performance check:** inspect that drag updates use compositor-friendly properties and do not animate `top`/layout on the hot path.  
5. **Snap behavior test:** slow drags, quick flicks, reversals, and edge pulls should resolve predictably to `collapsed`, `half`, or `full`.

**Verdict:** Block approval. The current motion works against direct manipulation: it animates the wrong properties, blocks interruption, lacks velocity/projection, and has no Reduced Motion path.

Rules/skill used: `design-craft`, `frontend.md`, `motion-quality.md`, and `interaction-physics.md`.
