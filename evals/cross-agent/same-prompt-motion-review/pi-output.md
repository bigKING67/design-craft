## 1. Evidence level and design read

**Evidence level:** static-source review only. The snippet proves explicit values and missing branches in the shown code; it cannot prove actual smoothness, frame rate, touch feel, computed styles, inherited CSS, or browser/device behavior.

**Reading this as:** a high-frequency web operations bottom sheet for keyboard-heavy staff, with calm utility motion, optimized for preserving task context while moving between `collapsed`, `half`, and `full`.

**Verdict:** **Block implementation approval.** The motion has a valid job, but the current implementation breaks direct manipulation, interruption, performance expectations, and Reduced Motion requirements.

---

## 2. Should this motion exist?

**Yes, narrowly.** Motion should exist only to preserve causality between the dragged sheet and its settled state.

**Should animate:**
- The post-release settle from current presentation position to the chosen snap point.
- Small pointer-down affordance on the drag handle/sheet header.
- Optional state feedback: handle color, elevation/tokenized shadow, snap-state label, or subtle opacity changes.

**Should not animate:**
- 1:1 drag tracking; the sheet should stay attached to the pointer, not transition behind it.
- `top`, layout, or `transition: all`.
- Whole-sheet `scale(0.96)` during active drag; it distorts dense operations content and conflicts with transform-based dragging.
- Large spatial travel in Reduced Motion.

---

## 3. Prioritized blocking findings

1. **Drag is not 1:1 direct manipulation.**  
   `pointermove` sets `sheet.style.top = event.clientY`, which likely snaps the sheet’s top edge to the pointer and ignores grab offset. It also appears to run without an explicit “dragging” state.

2. **Input is locked during settle.**  
   `if (animating) return` blocks pointer-down while the sheet is animating. A gesture sheet must be interruptible from its current on-screen value; users should be able to grab it mid-flight without a jump.

3. **Motion uses layout properties and conflicting animation systems.**  
   `top`, `offsetTop`, `transition: all`, and WAAPI `top` animation create layout/reflow risk and unclear ownership. Direct manipulation should use compositor-friendly `transform: translateY(...)` or a single composed transform owner.

4. **Settle physics are wrong for a grabbed object.**  
   `duration: 480` and `ease-in` make the beginning slow exactly when the user expects immediate continuation from release. There is no measured release velocity, velocity handoff, projected endpoint, damping, or hysteresis.

5. **Reduced Motion is absent.**  
   The implementation provides no `prefers-reduced-motion` branch. For this product, Reduced Motion must still communicate state while avoiding long positional travel and elastic/large movement.

---

## 4. Concrete design moves

1. **Pointer-down feedback:**  
   On pointer down, show immediate but quiet feedback: active handle color, cursor/grab state, or a tiny header-only compression. Avoid scaling the whole sheet and its table/form content.

2. **Intent threshold and pointer capture:**  
   Track active pointer id, call pointer capture after drag intent is established, and use an `8–12px` threshold so taps, text selection, and scroll do not accidentally become drags.

3. **1:1 tracking with grab offset:**  
   Store `grabOffset = pointerY - currentSheetY`. During drag, render `translateY(pointerY - grabOffset)` in CSS pixels. Do not transition while actively dragging.

4. **Single transform owner:**  
   Use one explicit transform pipeline, e.g. `translateY(var(--sheet-y))` on the sheet and any press feedback on a nested handle/header wrapper. Do not combine `transition: all`, WAAPI `top`, and `:active transform`.

5. **Presentation-value interruption:**  
   If the user grabs during settle, cancel/read the current presentation value, set that as the new drag origin, preserve current velocity if available, and continue without snapping back to the previous logical target.

6. **Velocity handoff:**  
   Record recent pointer samples with monotonic timestamps; compute release velocity in **CSS px/s**. Start the settle animation from the current position and feed that measured velocity into the spring/animation API, converting units if needed.

7. **Projected endpoint and target choice:**  
   Keep product-owned snap semantics explicit. If momentum targeting is approved, compute a bounded projected endpoint from current position + release velocity, clamp it to valid sheet bounds, then choose nearest `collapsed` / `half` / `full`. Otherwise keep nearest-current-position targeting but still use velocity for continuity.

8. **Soft boundaries and Reduced Motion:**  
   Add progressive resistance past min/max sheet positions instead of hard jumps. Under `prefers-reduced-motion`, remove bounce/elasticity and long travel; use instant or very short settle, plus static state feedback such as selected snap indicator, handle state, or accessible text update.

---

## 5. Verified vs unverified claims

**Verified from supplied code:**
- `top` is mutated during pointer move.
- WAAPI animates `top` with `480ms ease-in`.
- `transition: all 300ms` is present.
- `:active` applies `transform: scale(0.96)`.
- `animating` blocks pointer-down.
- No Reduced Motion branch is shown.
- No pointer capture, velocity sampling, boundary resistance, or interruption path is shown.

**Unverified / runtime-dependent:**
- Actual frame rate, jank, and layout cost.
- Whether inherited CSS or surrounding code compensates for missing drag state.
- Whether `transition: all` applies to the observed drag path in the browser.
- Real touch feel on trackpad, mouse, touchscreen, 60 Hz, or 120 Hz hardware.
- Computed transform/top interaction and final visual position after WAAPI `fill: forwards`.

---

## 6. Minimal validation plan before approval

1. **Browser interaction smoke:** mouse + touch/trackpad drag through all three states; verify no jump on grab, no lag during drag, and no accidental drag on tap.
2. **Interruption test:** release toward a snap point, grab mid-settle, reverse direction, confirm continuity from current visual position.
3. **Velocity test:** slow drag vs quick flick; verify target choice matches approved product semantics.
4. **Boundary test:** drag past collapsed/full bounds; confirm soft resistance and clean recovery.
5. **Reduced Motion run:** enable `prefers-reduced-motion`; verify state feedback remains clear without large animated travel.
6. **Performance check:** DevTools performance trace during repeated drags over the real operations page/table; confirm no layout-thrashing hot path.
7. **Accessibility check:** keyboard/focus behavior, visible focus, handle name/role/instructions, and state announcement if the sheet state changes programmatically.

Selected skill: `design-craft` motion/interaction-physics critique. No files edited; no browser or device validation performed.
