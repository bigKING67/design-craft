## 1. Evidence level and design read

**Evidence level:** static-code critique only. The snippet proves property choices, timing/easing, missing guards, and missing Reduced Motion branches. It does **not** prove actual frame rate, perceived smoothness, browser behavior, touch feel, or computed-style conflicts.

**Reading this as:** a calm desktop web operations bottom sheet for keyboard-heavy staff, optimized for preserving task context while moving between `collapsed`, `half`, and `full` without surprise or delay.

**Verdict:** **Block implementation approval.** The interaction has the right product reason to use motion, but the current motion model violates direct manipulation, interruption, accessibility, and performance expectations for a frequently used operational control.

---

## 2. Should this motion exist?

**Should exist:**
- Immediate pointer-down acknowledgement.
- 1:1 drag tracking while the user is holding the sheet.
- A short settle motion from release position to the chosen snap state.
- Subtle state feedback when snap state changes.

**Should not animate / should be removed:**
- `transition: all 300ms`; broad animation is unsafe and can animate unrelated layout/style changes.
- Continuous drag via `top`; drag should not animate layout properties.
- `ease-in` settle; it delays response at the moment the user releases.
- Large whole-sheet `scale(0.96)` on active drag; it compresses the workspace and competes with direct manipulation.
- Large spatial travel in Reduced Motion mode.

---

## 3. Prioritized blocking findings

### P0 — Drag is not true direct manipulation
`startY` is recorded but unused, and `sheet.style.top = event.clientY` makes the sheet top chase the pointer rather than preserving the grab offset. This can cause a visible jump on first move and breaks the “attached to my finger” model.

### P0 — Input is locked during animation
`if (animating) return` rejects pointer-down during settle. A sheet users manipulate repeatedly must be interruptible from the current on-screen value; locking creates lag and loss of agency.

### P0 — Layout-property animation on the gesture hot path
Both drag and settle use `top`, plus `offsetTop` reads. This risks layout/reflow on every move and during animation. For a bottom sheet, motion ownership should be compositor-friendly, normally `transform: translateY(...)`.

### P0 — No Reduced Motion path
The implementation has no `prefers-reduced-motion` branch. This is blocking because the primary feedback involves large positional travel. Reduced Motion should preserve state recognition without a full spatial slide.

### P1 — Release physics ignore velocity and boundaries
`nearestSnapPoint(sheet.offsetTop)` uses current position only. A quick flick and a slow drag ending at the same pixel produce the same target. There is also no pointer capture, intent threshold, soft boundary, or rubber-band resistance.

---

## 4. Concrete design moves

1. **Pointer-down feedback:** use a subtle handle/content affordance, e.g. handle color/elevation or `scale(0.98)` on a separate handle layer only; avoid scaling the entire operational sheet.

2. **1:1 tracking:** on drag start, store `grabOffset = pointerY - currentSheetY`; during drag set `translateY(pointerY - grabOffset)` so the sheet remains attached without jumping.

3. **Pointer capture and gesture state:** call `setPointerCapture(event.pointerId)` after intent is clear; track `isDragging`, ignore stray `pointermove`, and release capture on end/cancel.

4. **Presentation-value interruption:** remove the `animating` lockout. On pointer-down during settle, sample the current presented `translateY`, cancel the settle animation, and continue from that exact value.

5. **Velocity handoff:** keep a short history of `{ y, time }` samples using monotonic timestamps; compute release velocity in **CSS px/s** and pass that velocity into the settle spring/animation as initial velocity.

6. **Projected endpoints:** if product semantics allow momentum targeting, compute a bounded projected endpoint from current position + release velocity, clamp to valid sheet range, then choose the nearest snap point to that projection. If not authorized, keep nearest-current-position targeting but still hand velocity into the settle.

7. **Soft boundaries:** clamp hard logical states but apply progressive resistance past min/max during drag, so overdrag communicates limits without a dead stop. Use hysteresis around snap thresholds to avoid jitter.

8. **Reduced Motion:** replace large travel with immediate or very short state changes: shorter duration, no elastic overshoot, no large scale, clear snap-state indicator, updated handle/state label, and focus/ARIA feedback where applicable.

---

## 5. Verified versus unverified claims

**Verified from static evidence:**
- Uses `top` for drag and WAAPI settle.
- Uses `offsetTop` for target selection.
- Uses `duration: 480` and `easing: "ease-in"`.
- Uses `transition: all 300ms`.
- Uses `.sheet:active { transform: scale(0.96) }`.
- Has no visible Reduced Motion branch in the supplied snippet.
- Has no pointer capture, velocity tracking, bounds, hysteresis, or interruption logic in the supplied snippet.

**Unverified / requires runtime evidence:**
- Actual frame rate or jank.
- Whether CSS transition and WAAPI visibly conflict in the target browser.
- Whether `fill: "forwards"` causes a visible/logical position mismatch in this app’s full implementation.
- Real touch feel, scroll conflict, pointer cancellation behavior, and 60 Hz / 120 Hz behavior.
- Whether other unseen code supplies accessibility state, snap labels, keyboard controls, or Reduced Motion handling.

---

## 6. Minimal browser/device validation plan before approval

1. **Desktop browser smoke:** drag between all three states; interrupt settle mid-flight; verify no jump and no input lockout.
2. **Pointer trace check:** confirm grab offset preservation, pointer capture outside sheet bounds, and correct `pointercancel` behavior.
3. **Performance trace:** record drag and settle under representative table/app load; verify no repeated layout thrash from the gesture path.
4. **Reduced Motion run:** enable `prefers-reduced-motion`; confirm state feedback remains but large travel, bounce, and scale are removed or minimized.
5. **Touch hardware check:** test on at least one real touch device or trackpad/touchscreen browser for scroll conflict, velocity feel, and boundary resistance.
6. **Accessibility pass:** verify keyboard alternatives, focus visibility, state announcement/labeling, and that focus is not lost when the sheet changes state.
