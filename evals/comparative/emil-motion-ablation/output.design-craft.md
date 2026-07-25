## Verdict — **Block for production gesture quality**

**Evidence basis:** static source only. The snippet proves layout-property dragging, non-interruptible settling, no Reduced Motion branch, and no real drag state machine. It cannot prove actual frame rate or device feel, but the implementation is structurally unlikely to feel calm or reliable in a repeated-use operations app.

## Prioritized findings

### P0 — Drag is not actually controlled by an active gesture
**Evidence:** `pointermove` always runs and writes `sheet.style.top`, regardless of whether a pointer is down. `startY` is recorded but never used.  
**Impact:** hovering/moving over the sheet can reposition it; the sheet may jump to the pointer’s viewport Y instead of preserving the grab point.

### P0 — Non-interruptible motion breaks direct manipulation
**Evidence:** `if (animating) return` blocks new drags during settle; the running animation is not cancelled or retargeted from the current visual position.  
**Impact:** operators cannot reverse or correct a sheet mid-flight; repeated use will feel laggy and “owned by the animation,” not by the user.

### P0 — Animates `top`, causing layout work on the hot path
**Evidence:** pointermove writes `style.top`; release reads `offsetTop`; WAAPI animates `top`; CSS also has `transition: all`.  
**Impact:** likely layout/reflow pressure and possible lag, especially in a data-heavy app. Gesture position should be compositor-friendly, typically `transform: translateY(...)`.

### P0 — Reduced Motion requirement is unmet
**Evidence:** no `prefers-reduced-motion` branch; release always performs up to `480ms` of spatial travel.  
**Impact:** violates the stated requirement. Reduced Motion should preserve state feedback while avoiding large sheet travel.

### P1 — Timing/easing are wrong for a grabbed sheet
**Evidence:** settle uses `{ duration: 480, easing: "ease-in" }`.  
**Impact:** `ease-in` delays initial response after release; 480ms is heavy for a frequently used operations control. A sheet should settle promptly, usually with spring-like or strong ease-out behavior.

### P1 — Animation state and layout state can diverge
**Evidence:** `fill: "forwards"` keeps the visual animation result but does not necessarily update the underlying authored `top` as the source of truth.  
**Impact:** the next `offsetTop`/drag may start from stale layout state and jump unless final state is explicitly committed.

### P1 — No velocity, projection, hysteresis, or boundaries
**Evidence:** target is `nearestSnapPoint(sheet.offsetTop)` only; no sampled pointer history, velocity units, threshold, clamp, or rubber-band logic.  
**Impact:** a quick flick and a slow drag ending at the same point behave identically; accidental taps may become drags; overdrag behavior is undefined.

### P1 — CSS transform ownership conflict
**Evidence:** `.sheet:active { transform: scale(0.96); }`.  
**Impact:** if the sheet is moved with `transform`, press scale will overwrite or fight translate unless separated into wrapper layers. Scaling the entire sheet while dragging may also make dense operations UI feel unstable.

### P2 — Missing pointer robustness
**Evidence:** no `setPointerCapture`, `pointerId`, `pointercancel`, `lostpointercapture`, or multi-touch guard.  
**Impact:** dragging outside the sheet, OS interruption, or additional touches can leave the sheet in an inconsistent state.

## Concrete direct-manipulation moves

1. **Introduce a real gesture state machine**  
   Track `idle | dragging | settling`, `activePointerId`, `startY`, `startSheetY`, and `grabOffset`. Ignore unrelated pointers.

2. **Use pointer capture and cancellation paths**  
   On committed drag: `setPointerCapture(event.pointerId)`. Handle `pointercancel` and `lostpointercapture` by settling or restoring safely.

3. **Preserve the grab offset**  
   Compute movement from `startSheetY + (event.clientY - startY)`, not `top = event.clientY`.

4. **Move with transforms, not layout**  
   Drive a single position owner such as `translateY(var(--sheet-y))`. Avoid `top` animation and remove `transition: all`.

5. **Batch drag writes with `requestAnimationFrame`**  
   Store the latest pointer Y, then update transform once per frame. Keep layout reads out of `pointermove`.

6. **Make settling interruptible**  
   On pointerdown during settle, cancel the current animation, read the current presented Y, and continue from that exact value without a jump.

7. **Separate target selection from velocity handoff**  
   Measure release velocity in CSS px/s from recent samples.  
   - If product semantics are “nearest current snap,” keep `nearestSnapPoint(currentY)`.  
   - If momentum is authorized, choose from a bounded projected endpoint.  
   Either way, feed measured velocity into the settle animation when the API supports it.

8. **Use bounded snap geometry**  
   Define explicit collapsed/half/full Y values, clamp within safe bounds, update on viewport/container resize, and apply soft resistance beyond edges.

9. **Replace global active scale**  
   Put position transform on the outer sheet and optional press feedback on an inner handle/control layer. Keep scale subtle and disable it while dragging if it destabilizes content.

10. **Add Reduced Motion behavior**  
   Under `prefers-reduced-motion: reduce`, avoid large animated travel: snap state immediately or with a very short transition, and preserve feedback through handle state, opacity, elevation, label, or focus-visible changes.

11. **Expose state accessibly**  
   Maintain a source-of-truth state: `collapsed | half | full`; provide keyboard controls and visible/focusable affordances for changing state.

## Verified / unverified boundaries

**Verified from snippet**
- `pointermove` is ungated.
- `startY` is unused.
- `top` is written and animated.
- `offsetTop` is read during release.
- `ease-in` and `480ms` are used.
- `transition: all 300ms` is present.
- Reduced Motion is absent in supplied CSS/JS.
- Pointer capture/cancel handling is absent in supplied JS.

**Not verified**
- Actual frame rate, dropped frames, or perceived smoothness.
- Whether surrounding code adds bounds, keyboard support, ARIA, focus management, or Reduced Motion elsewhere.
- Whether `nearestSnapPoint` encodes product-approved threshold logic.
- Real touch behavior on trackpad, mouse, stylus, or mobile hardware.

## Smallest runtime validation plan

1. **Gesture continuity:** drag from collapsed → half → reverse mid-settle; confirm no jump and no input lockout.  
2. **Pointer robustness:** drag outside sheet bounds, cancel pointer, add second touch; confirm state recovers.  
3. **Performance trace:** record drag with table/data load present; confirm transform-only updates and no repeated layout in the move loop.  
4. **Velocity behavior:** compare slow drag vs quick flick with same release point; confirm intended snap semantics.  
5. **Reduced Motion:** emulate reduced motion; confirm no large spatial travel while state feedback remains clear.  
6. **Keyboard/accessibility pass:** operate collapsed/half/full without pointer; confirm focus visibility and announced/current state.
